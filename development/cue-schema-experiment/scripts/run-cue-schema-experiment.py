#!/usr/bin/env python3
"""Run one isolated, non-authoritative Arcanum CUE schema experiment."""

from __future__ import annotations

import argparse
import base64
import copy
import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
import urllib.parse
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from jsonschema import FormatChecker
from jsonschema.validators import validator_for
import yaml


REPORT_SCHEMA = "arcanum.cue_schema_experiment.run_report.v1"
EXPERIMENT_SCHEMA = "arcanum.cue_schema_experiment.config.v1"
REGIME_IDS = ("R0", "R1", "R2", "R3", "R4", "R5", "R6")
CANONICAL_ENV = {
    "LANG": "C",
    "LC_ALL": "C",
    "PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
    "PYTHONDONTWRITEBYTECODE": "1",
    "TZ": "UTC",
}


def canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
        + "\n"
    ).encode("utf-8")


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def file_ref(path: Path, display_path: str | None = None) -> dict[str, Any]:
    content = path.read_bytes()
    return {
        "path": display_path if display_path is not None else path.as_posix(),
        "sha256": sha256_bytes(content),
        "size_bytes": len(content),
    }


def membership_digest(paths: Iterable[str]) -> str:
    return sha256_bytes(
        json.dumps(
            sorted(paths), ensure_ascii=False, separators=(",", ":")
        ).encode("utf-8")
    )


def tree_digest(refs: Iterable[dict[str, Any]]) -> str:
    projection = [
        {"path": item["path"], "sha256": item["sha256"], "size_bytes": item["size_bytes"]}
        for item in refs
    ]
    projection.sort(key=lambda item: item["path"])
    return sha256_bytes(canonical_bytes(projection))


def collect_generated_refs(
    generation_results: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    """Collect only materialized generated schemas, including partial R2 failure sets."""
    return sorted(
        (
            item["generated_ref"]
            for item in generation_results.values()
            if item.get("generated_ref") is not None
        ),
        key=lambda item: item["path"],
    )


def physical_ref_path(reference: dict[str, Any]) -> str:
    """Select a run-local physical path while retaining a stable logical path."""
    return reference["physical_path"]


def reproducibility_projection(report: dict[str, Any]) -> dict[str, Any]:
    """Return the run-local-path-free payload whose digest must match across runs."""
    return {
        "membership": {
            key: {
                "count": value["count"],
                "membership_digest": value["membership_digest"],
            }
            for key, value in report["membership"].items()
        },
        "inputs_digest": report["inputs"]["before_tree_digest"],
        "regime_statuses": {
            key: value["status"] for key, value in report["regimes"].items()
        },
        "classification": report["classification"],
        "native_prototype_tree_digest": report["native_prototype_tree"]["digest"],
        "generated_tree_digest": report["generated_tree"]["digest"],
        "case_outcomes": sorted(
            (
                item["case_id"],
                item.get("r0_observed_valid"),
                item.get("r1_observed_valid"),
                item.get("r3_observed_valid"),
            )
            for item in report["regimes"]["R0"]["cases"]
        ),
    }


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def json_pointer(document: Any, pointer: str | None) -> Any:
    if pointer in (None, "", "/"):
        return document
    current = document
    for raw in pointer.lstrip("/").split("/"):
        part = raw.replace("~1", "/").replace("~0", "~")
        current = current[int(part)] if isinstance(current, list) else current[part]
    return current


def pointer_parent(document: Any, pointer: str) -> tuple[Any, str | int]:
    parts = pointer.lstrip("/").split("/")
    current = document
    for raw in parts[:-1]:
        part = raw.replace("~1", "/").replace("~0", "~")
        current = current[int(part)] if isinstance(current, list) else current[part]
    final = parts[-1].replace("~1", "/").replace("~0", "~")
    return current, int(final) if isinstance(current, list) else final


def apply_case_mutation(document: Any, case: dict[str, Any]) -> Any:
    result = copy.deepcopy(document)
    parent, final = pointer_parent(result, case["pointer"])
    if case["operation"] == "remove":
        if isinstance(parent, list):
            parent.pop(final)
        else:
            del parent[final]
    elif case["operation"] == "set":
        parent[final] = copy.deepcopy(case["value"])
    else:
        raise ValueError(f"unsupported mutation operation: {case['operation']}")
    return result


def all_refs(value: Any) -> Iterable[str]:
    if isinstance(value, dict):
        if isinstance(value.get("$ref"), str):
            yield value["$ref"]
        for child in value.values():
            yield from all_refs(child)
    elif isinstance(value, list):
        for child in value:
            yield from all_refs(child)


def discover_invoke(root: Path) -> list[str]:
    invoke_root = root / "arcanum/spells/invoke"
    schema_dir = invoke_root / "schemas"
    schemas = {path.name: load_json(path) for path in schema_dir.glob("*.schema.json")}
    by_id = {
        schema.get("$id"): name
        for name, schema in schemas.items()
        if isinstance(schema.get("$id"), str)
    }
    catalog = load_json(invoke_root / "invoke-cli-stage-catalog.json")
    names = {"invoke-cli-stage-catalog-v1.schema.json"}
    for mode in ("define", "design"):
        for stage in catalog["modes"][mode]["stages"].values():
            for field in ("request_schema", "output_schema"):
                if stage.get(field):
                    names.add(stage[field])
    while True:
        before = len(names)
        for name in tuple(names):
            for reference in all_refs(schemas[name]):
                dependency = by_id.get(reference.split("#", 1)[0])
                if dependency:
                    names.add(dependency)
        if len(names) == before:
            break
    return sorted(f"arcanum/spells/invoke/schemas/{name}" for name in names)


def discover_membership(root: Path, config: dict[str, Any]) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {
        "invoke": discover_invoke(root),
        "orchestrate": sorted(
            path.relative_to(root).as_posix()
            for path in (root / "arcanum/runtime/orchestrate/schemas").glob("*.schema.json")
        ),
        "work_pack_readiness": sorted(
            path.relative_to(root).as_posix()
            for path in (root / "arcanum/spells/work-pack-readiness-audit/schemas").glob("*.schema.json")
        ),
        "infra_spec": ["arcanum/formulae/infra-spec/infra-spec.schema.json"],
        "distill": sorted(
            path.relative_to(root).as_posix()
            for path in (root / "arcanum/arcana/distill/schemas").glob("*.schema.json")
        ),
    }
    excluded = set(config["census"]["excluded_path_segments"])
    result["census"] = sorted(
        path.relative_to(root).as_posix()
        for path in (root / "arcanum").rglob("*.schema.json")
        if not (set(path.relative_to(root / "arcanum").parts) & excluded)
    )
    return result


def schema_store(root: Path, paths: Iterable[str]) -> tuple[dict[str, Any], dict[str, Any]]:
    by_path: dict[str, Any] = {}
    by_id: dict[str, Any] = {}
    for relative in paths:
        schema = load_json(root / relative)
        by_path[relative] = schema
        identifier = schema.get("$id")
        if isinstance(identifier, str):
            by_id[identifier] = schema
    return by_path, by_id


def resolve_schema_reference(
    source_path: str,
    reference: str,
    by_path: dict[str, Any],
    by_id: dict[str, Any],
) -> tuple[str, dict[str, Any], str]:
    base, _, fragment = reference.partition("#")
    if not base:
        return source_path, by_path[source_path], fragment
    source_id = by_path[source_path].get("$id", "")
    for candidate in (base, urllib.parse.urljoin(source_id, base)):
        target = by_id.get(candidate)
        if target is not None:
            target_path = next(
                path for path, document in by_path.items() if document is target
            )
            return target_path, target, fragment
    relative = (Path(source_path).parent / base).as_posix()
    if relative in by_path:
        return relative, by_path[relative], fragment
    raise ValueError(f"unresolved schema reference: {source_path}: {reference}")


def bundle_schema_references(
    value: Any,
    source_path: str,
    by_path: dict[str, Any],
    by_id: dict[str, Any],
    trail: tuple[tuple[str, str], ...] = (),
) -> Any:
    """Inline exact reference targets without altering any carried constraint."""
    if isinstance(value, dict):
        reference = value.get("$ref")
        if isinstance(reference, str):
            target_path, target_schema, fragment = resolve_schema_reference(
                source_path, reference, by_path, by_id
            )
            key = (target_path, fragment)
            if key in trail:
                raise ValueError(f"cyclic schema reference: {key}")
            target = json_pointer(target_schema, fragment or None)
            resolved = bundle_schema_references(
                copy.deepcopy(target),
                target_path,
                by_path,
                by_id,
                (*trail, key),
            )
            siblings = {
                name: bundle_schema_references(
                    child, source_path, by_path, by_id, trail
                )
                for name, child in value.items()
                if name != "$ref"
            }
            return {"allOf": [resolved, siblings]} if siblings else resolved
        return {
            name: bundle_schema_references(child, source_path, by_path, by_id, trail)
            for name, child in value.items()
        }
    if isinstance(value, list):
        return [
            bundle_schema_references(child, source_path, by_path, by_id, trail)
            for child in value
        ]
    return value


def validator(schema: dict[str, Any], store: dict[str, Any]):
    cls = validator_for(schema)
    cls.check_schema(schema)
    try:
        from jsonschema import RefResolver

        resolver = RefResolver.from_schema(schema, store=store)
        return cls(schema, resolver=resolver, format_checker=FormatChecker())
    except Exception:
        return cls(schema, format_checker=FormatChecker())


def wrong_type(schema: dict[str, Any], current: Any) -> Any:
    declared = schema.get("type")
    allowed = set(declared if isinstance(declared, list) else [declared])
    candidates = [None, True, 1, "wrong", [], {}]
    for candidate in candidates:
        kind = (
            "null"
            if candidate is None
            else "boolean"
            if isinstance(candidate, bool)
            else "integer"
            if isinstance(candidate, int)
            else "string"
            if isinstance(candidate, str)
            else "array"
            if isinstance(candidate, list)
            else "object"
        )
        if kind not in allowed and candidate != current:
            return candidate
    return {"unexpected": True}


def root_mutations(case_id: str, document: Any, schema: dict[str, Any]) -> list[dict[str, Any]]:
    if not isinstance(document, dict) or not isinstance(schema, dict):
        return []
    mutations: list[dict[str, Any]] = []
    required = schema.get("required", [])
    for name in required:
        if name in document:
            changed = copy.deepcopy(document)
            del changed[name]
            mutations.append({"case_id": f"{case_id}:missing:{name}", "kind": "missing_required", "document": changed})
    if schema.get("additionalProperties") is False:
        changed = copy.deepcopy(document)
        changed["__cue_experiment_unknown__"] = True
        mutations.append({"case_id": f"{case_id}:unknown", "kind": "unknown_property", "document": changed})
    for name, constraint in schema.get("properties", {}).items():
        if name not in document or not isinstance(constraint, dict):
            continue
        if "type" in constraint:
            changed = copy.deepcopy(document)
            changed[name] = wrong_type(constraint, document[name])
            mutations.append({"case_id": f"{case_id}:wrong-type:{name}", "kind": "wrong_type", "document": changed})
        if "const" in constraint:
            changed = copy.deepcopy(document)
            changed[name] = "__not_the_const__"
            mutations.append({"case_id": f"{case_id}:const:{name}", "kind": "invalid_const", "document": changed})
        elif isinstance(constraint.get("enum"), list) and constraint["enum"]:
            changed = copy.deepcopy(document)
            changed[name] = "__not_in_enum__"
            mutations.append({"case_id": f"{case_id}:enum:{name}", "kind": "invalid_enum", "document": changed})
        if isinstance(constraint.get("minItems"), int) and isinstance(document[name], list):
            changed = copy.deepcopy(document)
            changed[name] = []
            mutations.append({"case_id": f"{case_id}:min-items:{name}", "kind": "cardinality", "document": changed})
        if constraint.get("uniqueItems") is True and isinstance(document[name], list) and document[name]:
            changed = copy.deepcopy(document)
            changed[name] = [document[name][0], document[name][0]]
            mutations.append({"case_id": f"{case_id}:unique:{name}", "kind": "uniqueness", "document": changed})
        if isinstance(constraint.get("pattern"), str) and isinstance(document[name], str):
            changed = copy.deepcopy(document)
            changed[name] = ""
            mutations.append({"case_id": f"{case_id}:pattern:{name}", "kind": "pattern", "document": changed})
        if "$ref" in constraint:
            changed = copy.deepcopy(document)
            changed[name] = None
            mutations.append({"case_id": f"{case_id}:ref:{name}", "kind": "reference_edge", "document": changed})
    unique: dict[str, dict[str, Any]] = {}
    for item in mutations:
        digest = sha256_bytes(canonical_bytes(item["document"]))
        unique.setdefault(digest, item)
    return list(unique.values())


@dataclass
class CommandRecorder:
    output_root: Path
    command_records: list[dict[str, Any]]
    environment_path: str
    sequence: int = 0

    def run(
        self,
        regime: str,
        argv: list[str],
        cwd: Path,
        expected_exit: int | None = 0,
        overlays: dict[Path, Path] | None = None,
        writable_overlays: dict[Path, Path] | None = None,
        timeout: int = 60,
    ) -> subprocess.CompletedProcess[bytes]:
        self.sequence += 1
        command_id = f"{regime}-{self.sequence:04d}"
        writable = self.output_root.resolve()
        for child in ("tmp", "cache", "config", "home"):
            (writable / child).mkdir(parents=True, exist_ok=True)
        sandbox = [
            "/usr/bin/bwrap",
            "--die-with-parent",
            "--unshare-net",
            "--ro-bind",
            "/",
            "/",
            "--dev",
            "/dev",
            "--proc",
            "/proc",
            "--bind",
            str(writable),
            str(writable),
        ]
        for destination, source in sorted((overlays or {}).items(), key=lambda pair: str(pair[0])):
            sandbox.extend(["--ro-bind", str(source.resolve()), str(destination.resolve())])
        for destination, source in sorted(
            (writable_overlays or {}).items(), key=lambda pair: str(pair[0])
        ):
            sandbox.extend(["--bind", str(source.resolve()), str(destination.resolve())])
        environment = {
            **CANONICAL_ENV,
            "PATH": self.environment_path,
            "CUE_REGISTRY": "none",
            "HOME": str(writable / "home"),
            "TMPDIR": str(writable / "tmp"),
            "XDG_CACHE_HOME": str(writable / "cache"),
            "XDG_CONFIG_HOME": str(writable / "config"),
        }
        command = [
            *sandbox,
            "--chdir",
            str(cwd.resolve()),
            "/usr/bin/env",
            "-i",
            *(f"{key}={value}" for key, value in sorted(environment.items())),
            *argv,
        ]
        try:
            result = subprocess.run(command, capture_output=True, timeout=timeout, check=False)
            timed_out = False
        except subprocess.TimeoutExpired as error:
            result = subprocess.CompletedProcess(command, 124, error.stdout or b"", error.stderr or b"")
            timed_out = True
        stdout = result.stdout or b""
        stderr = result.stderr or b""
        self.command_records.append(
            {
                "command_id": command_id,
                "regime": regime,
                "argv": argv,
                "cwd": cwd.resolve().as_posix(),
                "environment": [[key, value] for key, value in sorted(environment.items())],
                "network_isolation": "bubblewrap_unshare_net",
                "expected_exit": expected_exit,
                "exit_status": result.returncode,
                "expected_result": expected_exit is None or result.returncode == expected_exit,
                "timed_out": timed_out,
                "stdout_base64": base64.b64encode(stdout).decode("ascii"),
                "stdout_size_bytes": len(stdout),
                "stdout_sha256": sha256_bytes(stdout),
                "stderr_base64": base64.b64encode(stderr).decode("ascii"),
                "stderr_size_bytes": len(stderr),
                "stderr_sha256": sha256_bytes(stderr),
            }
        )
        return result


def materialize_cases(
    root: Path,
    output_root: Path,
    config: dict[str, Any],
    by_path: dict[str, Any],
    by_id: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    cases: list[dict[str, Any]] = []
    blockers: list[dict[str, Any]] = []
    case_dir = output_root / "materialized-cases"
    case_dir.mkdir(parents=True, exist_ok=True)
    for spec in config["cases"]:
        source = load_json(root / spec["data_path"])
        document = copy.deepcopy(json_pointer(source, spec.get("json_pointer")))
        schema = by_path[spec["schema_path"]]
        check = validator(schema, by_id)
        observed = check.is_valid(document)
        case_path = case_dir / f"{spec['case_id']}.json"
        case_path.write_bytes(canonical_bytes(document))
        item = {
            "case_id": spec["case_id"],
            "cohort": spec["cohort"],
            "schema_path": spec["schema_path"],
            "data_ref": file_ref(case_path),
            "expected_valid": spec["expected_valid"],
            "r0_observed_valid": observed,
            "kind": "persisted",
        }
        cases.append(item)
        if observed != spec["expected_valid"]:
            blockers.append({"code": "E_R0_PERSISTED_CASE", "case_id": spec["case_id"]})
        if spec["expected_valid"]:
            for mutation in root_mutations(spec["case_id"], document, schema):
                mutation_path = case_dir / f"{mutation['case_id'].replace(':', '__')}.json"
                mutation_path.write_bytes(canonical_bytes(mutation["document"]))
                mutation_valid = check.is_valid(mutation["document"])
                mutation_item = {
                    "case_id": mutation["case_id"],
                    "cohort": spec["cohort"],
                    "schema_path": spec["schema_path"],
                    "data_ref": file_ref(mutation_path),
                    "expected_valid": False,
                    "r0_observed_valid": mutation_valid,
                    "kind": mutation["kind"],
                }
                cases.append(mutation_item)
                if mutation_valid:
                    blockers.append({"code": "E_R0_GENERATED_MUTATION", "case_id": mutation["case_id"]})
    return cases, blockers


def materialize_stressor_cases(package_root: Path, output_root: Path) -> list[dict[str, Any]]:
    manifest = load_json(package_root / "fixtures/distill-stressor/cases.json")
    if manifest["expected_case_count"] != len(manifest["cases"]):
        raise ValueError("stressor denominator")
    target = output_root / "stressor-cases"
    target.mkdir(parents=True, exist_ok=True)
    result = []
    for case in manifest["cases"]:
        if "path" in case:
            document = load_json(package_root / case["path"])
        else:
            document = apply_case_mutation(load_json(package_root / case["base"]), case)
        path = target / f"{case['case_id']}.json"
        path.write_bytes(canonical_bytes(document))
        result.append({**case, "data_ref": file_ref(path)})
    return result


def interface_projection(schema: dict[str, Any]) -> dict[str, Any]:
    return {
        "$schema": schema.get("$schema"),
        "$id": schema.get("$id"),
        "root_additional_properties": schema.get("additionalProperties", "unspecified"),
        "external_refs": sorted({ref for ref in all_refs(schema) if not ref.startswith("#")}),
    }


def classify(report: dict[str, Any]) -> str:
    regimes = report["regimes"]
    semantic_failure = bool(
        regimes["R0"]["blockers"]
        or regimes["R1"]["semantic_mismatches"]
        or regimes["R3"]["status"] != "pass"
    )
    tool_failure = any(command["timed_out"] for command in report["commands"])
    if semantic_failure or tool_failure:
        return "reject_cue"
    primary = regimes["R4"]["cohorts"].get("invoke", {})
    generation_ok = primary.get("status") == "pass"
    replay_ok = regimes["R5"]["cohorts"].get("invoke", {}).get("status") == "pass"
    strict_primary = regimes["R2"]["cohorts"].get("invoke", {}).get("status") == "pass"
    if not (strict_primary and generation_ok and replay_ok):
        return "verifier_only"
    passing_controls = sum(
        regimes["R5"]["cohorts"].get(name, {}).get("status") == "pass"
        for name in ("orchestrate", "work_pack_readiness", "infra_spec", "distill")
    )
    census_ok = regimes["R2"]["census"]["status"] == "pass"
    maintenance = regimes["R6"]
    if passing_controls == 4 and census_ok and maintenance.get("status") == "pass" and maintenance.get("median_reduction_percent", 0) >= 25:
        return "broad_adoption_candidate"
    if passing_controls >= 3:
        return "bounded_adoption_candidate"
    return "retain_json_schema"


def run_experiment(args: argparse.Namespace) -> dict[str, Any]:
    root = args.root.resolve()
    cue_bin = args.cue_bin.resolve()
    config_path = args.config.resolve()
    output_root = args.output_dir.resolve()
    if output_root.exists():
        raise ValueError("output directory must be absent")
    if not (root / "arcanum").is_dir():
        raise ValueError("repository root")
    if not cue_bin.is_file() or not (cue_bin.stat().st_mode & stat.S_IXUSR):
        raise ValueError("CUE binary")
    config = load_json(config_path)
    if config.get("schema_version") != EXPERIMENT_SCHEMA:
        raise ValueError("experiment config schema")
    output_root.mkdir(parents=True)
    package_root = config_path.parent
    command_records: list[dict[str, Any]] = []
    runtime_tools = config["runtime_tools"]
    for name in ("node", "python"):
        expected = runtime_tools[name]
        observed = file_ref(Path(expected["path"]))
        if observed != {
            "path": expected["path"],
            "sha256": expected["sha256"],
            "size_bytes": expected["size_bytes"],
        }:
            raise ValueError(f"{name} binary identity")
        version_command = (
            [expected["path"], "--version"]
            if name == "node"
            else [expected["path"], "--version"]
        )
        observed_version = subprocess.run(
            version_command, capture_output=True, text=True, check=False
        )
        version_text = (observed_version.stdout or observed_version.stderr).strip()
        if observed_version.returncode != 0 or version_text != expected["version"]:
            raise ValueError(f"{name} version")
    recorder = CommandRecorder(
        output_root, command_records, runtime_tools["consumer_path"]
    )
    version = subprocess.run([str(cue_bin), "version"], capture_output=True, check=False)
    if version.returncode != 0:
        raise ValueError("CUE version command")
    cue_ref = file_ref(cue_bin)
    if cue_ref["sha256"] != config["cue"]["binary_sha256"]:
        raise ValueError("CUE binary digest")
    if config["cue"]["version"] not in version.stdout.decode("utf-8", "replace"):
        raise ValueError("CUE version mismatch")

    membership = discover_membership(root, config)
    membership_report: dict[str, Any] = {}
    for name, paths in membership.items():
        expected = config["census"] if name == "census" else config["cohorts"][name]
        observed = {"count": len(paths), "membership_digest": membership_digest(paths), "paths": paths}
        membership_report[name] = observed
        if observed["count"] != expected["expected_count"] or observed["membership_digest"] != expected["membership_digest"]:
            raise ValueError(f"membership drift: {name}")
    for case in config["cases"]:
        if case["schema_path"] not in membership[case["cohort"]]:
            raise ValueError(
                f"case outside frozen cohort: {case['case_id']}: {case['schema_path']}"
            )

    input_paths = sorted(set(membership["census"]) | {config["infra_yaml_path"], config["invoke_catalog_path"], config["w1_report_path"]})
    input_refs = [file_ref(root / path, path) for path in input_paths]
    before_digest = tree_digest(input_refs)
    by_path, by_id = schema_store(root, membership["census"])

    regimes: dict[str, Any] = {name: {} for name in REGIME_IDS}

    # R0: native JSON Schema baseline and declared consumers.
    r0_blockers: list[dict[str, Any]] = []
    meta_results = []
    identifiers: dict[str, str] = {}
    for relative in membership["census"]:
        schema = by_path[relative]
        try:
            cls = validator_for(schema)
            cls.check_schema(schema)
            status = "pass"
            detail = None
        except Exception as error:
            status = "block"
            detail = f"{type(error).__name__}: {error}"
            r0_blockers.append({"code": "E_META_SCHEMA", "path": relative, "detail": detail})
        identifier = schema.get("$id")
        if isinstance(identifier, str):
            if identifier in identifiers and identifiers[identifier] != relative:
                r0_blockers.append({"code": "E_DUPLICATE_SCHEMA_ID", "$id": identifier, "paths": [identifiers[identifier], relative]})
            identifiers[identifier] = relative
        meta_results.append({"path": relative, "status": status, "detail": detail})
    cases, case_blockers = materialize_cases(root, output_root, config, by_path, by_id)
    r0_blockers.extend(case_blockers)
    infra_json = by_path["arcanum/formulae/infra-spec/infra-spec.schema.json"]
    infra_yaml = yaml.safe_load(
        (root / config["infra_yaml_path"]).read_text(encoding="utf-8")
    )
    infra_parity = infra_json == infra_yaml
    if not infra_parity:
        r0_blockers.append({"code": "E_INFRA_JSON_YAML_PARITY"})
    invoke_overlay = output_root / "consumer-overlays/arcanum/spells/invoke"
    shutil.copytree(
        root / "arcanum/spells/invoke",
        invoke_overlay,
        symlinks=True,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
    )
    consumer_results = []
    for command in config["consumer_commands"]:
        writable_overlays = (
            {root / "arcanum/spells/invoke": invoke_overlay}
            if command["cohort"] == "invoke"
            else None
        )
        completed = recorder.run(
            "R0",
            command["argv"],
            root / command.get("cwd", "."),
            command["expected_exit"],
            writable_overlays=writable_overlays,
            timeout=command.get("timeout_seconds", 180),
        )
        combined_output = (completed.stdout or b"") + (completed.stderr or b"")
        decoded_output = combined_output.decode("utf-8", "replace")
        missing_markers = [
            marker
            for marker in command.get("expected_output_contains", [])
            if marker not in decoded_output
        ]
        status = (
            "pass"
            if completed.returncode == command["expected_exit"]
            and not missing_markers
            else "block"
        )
        consumer_results.append(
            {
                "command_id": command["command_id"],
                "record_id": command_records[-1]["command_id"],
                "cohort": command["cohort"],
                "baseline_health": command.get("baseline_health", "pass"),
                "missing_output_markers": missing_markers,
                "status": status,
            }
        )
        if status != "pass":
            r0_blockers.append({"code": "E_BASELINE_CONSUMER", "command_id": command["command_id"]})
    regimes["R0"] = {
        "status": "pass" if not r0_blockers else "block",
        "meta_validation": {"passed": sum(item["status"] == "pass" for item in meta_results), "total": len(meta_results), "results": meta_results},
        "cases": cases,
        "infra_json_yaml_parity": {
            "status": "pass" if infra_parity else "block",
            "json_semantic_digest": sha256_bytes(canonical_bytes(infra_json)),
            "yaml_semantic_digest": sha256_bytes(canonical_bytes(infra_yaml)),
        },
        "consumer_results": consumer_results,
        "blockers": r0_blockers,
    }

    # R1: direct CUE validation against original JSON Schema.
    r1_mismatches = []
    r1_schema_results = []
    targeted = sorted(set().union(*(membership[name] for name in config["cohorts"])))
    for relative in targeted:
        result = recorder.run(
            "R1",
            [str(cue_bin), "vet", "-c", "jsonschema+strict+openOnlyWhenExplicit:", str(root / relative)],
            root,
            0,
            timeout=30,
        )
        r1_schema_results.append({"path": relative, "status": "pass" if result.returncode == 0 else "block"})
    for case in cases:
        expected_exit = 0 if case["expected_valid"] else 1
        result = recorder.run(
            "R1",
            [str(cue_bin), "vet", "-c", "jsonschema+strict+openOnlyWhenExplicit:", str(root / case["schema_path"]), "json:", case["data_ref"]["path"]],
            root,
            expected_exit,
            timeout=30,
        )
        case["r1_observed_valid"] = result.returncode == 0
        if case["r1_observed_valid"] != case["expected_valid"]:
            r1_mismatches.append({"case_id": case["case_id"], "expected_valid": case["expected_valid"], "observed_valid": case["r1_observed_valid"]})
    regimes["R1"] = {
        "status": "pass" if not r1_mismatches and all(item["status"] == "pass" for item in r1_schema_results) else "block",
        "schema_results": r1_schema_results,
        "semantic_mismatches": r1_mismatches,
    }

    # R2: strict import census. Each imported root is an explicit #Root definition.
    import_results: dict[str, dict[str, Any]] = {}
    import_root = output_root / "strict-imports"
    for relative in membership["census"]:
        destination = import_root / Path(relative).with_suffix(".cue")
        destination.parent.mkdir(parents=True, exist_ok=True)
        result = recorder.run(
            "R2",
            [str(cue_bin), "import", "-p", "prototype", "-l", "#Root:", "--outfile", str(destination), "jsonschema+strict+openOnlyWhenExplicit:", str(root / relative)],
            root,
            0,
            timeout=30,
        )
        status = "pass" if result.returncode == 0 and destination.is_file() else "block"
        import_results[relative] = {"status": status, "prototype_ref": file_ref(destination) if destination.is_file() else None}
    r2_cohorts = {}
    for name, paths in membership.items():
        if name == "census":
            continue
        passed = sum(import_results[path]["status"] == "pass" for path in paths)
        r2_cohorts[name] = {"status": "pass" if passed == len(paths) else "block", "passed": passed, "total": len(paths)}
    census_passed = sum(item["status"] == "pass" for item in import_results.values())
    regimes["R2"] = {
        "status": "pass" if census_passed == len(import_results) else "block",
        "census": {"status": "pass" if census_passed == len(import_results) else "block", "passed": census_passed, "total": len(import_results)},
        "cohorts": r2_cohorts,
        "results": import_results,
    }

    # R3: complete normalized native-CUE prototypes and hand-authored Distill stressor.
    native_schema_root = output_root / "native-bundled-json-schema"
    native_cue_root = output_root / "native-cue"
    native_results: dict[str, dict[str, Any]] = {}
    for relative in targeted:
        bundled_path = native_schema_root / relative
        bundled_path.parent.mkdir(parents=True, exist_ok=True)
        bundled = bundle_schema_references(
            copy.deepcopy(by_path[relative]), relative, by_path, by_id
        )
        bundled_path.write_bytes(canonical_bytes(bundled))
        prototype_path = native_cue_root / Path(relative).with_suffix(".cue")
        prototype_path.parent.mkdir(parents=True, exist_ok=True)
        result = recorder.run(
            "R3",
            [
                str(cue_bin),
                "import",
                "-p",
                "prototype",
                "-l",
                "#Root:",
                "--outfile",
                str(prototype_path),
                "jsonschema+openOnlyWhenExplicit:",
                str(bundled_path),
            ],
            root,
            0,
            timeout=30,
        )
        native_results[relative] = {
            "status": (
                "pass"
                if result.returncode == 0 and prototype_path.is_file()
                else "block"
            ),
            "bundled_schema_ref": {
                **file_ref(bundled_path, relative),
                "physical_path": bundled_path.resolve().as_posix(),
            },
            "prototype_ref": (
                {
                    **file_ref(
                        prototype_path, Path(relative).with_suffix(".cue").as_posix()
                    ),
                    "physical_path": prototype_path.resolve().as_posix(),
                }
                if prototype_path.is_file()
                else None
            ),
        }
    r3_mismatches = []
    r3_not_evaluable = []
    for case in cases:
        prototype = native_results[case["schema_path"]]["prototype_ref"]
        if prototype is None:
            case["r3_status"] = "not_evaluable"
            r3_not_evaluable.append(
                {"case_id": case["case_id"], "blocker": "native_import_failed"}
            )
            continue
        expected_exit = 0 if case["expected_valid"] else 1
        result = recorder.run(
            "R3",
            [str(cue_bin), "vet", "-c", "-d", "#Root", physical_ref_path(prototype), "json:", case["data_ref"]["path"]],
            root,
            expected_exit,
            timeout=30,
        )
        observed = result.returncode == 0
        case["r3_status"] = "pass" if observed == case["expected_valid"] else "block"
        case["r3_observed_valid"] = observed
        if observed != case["expected_valid"]:
            r3_mismatches.append({"case_id": case["case_id"], "expected_valid": case["expected_valid"], "observed_valid": observed})
    stressor_cases = materialize_stressor_cases(package_root, output_root)
    stressor_source = package_root / "prototypes/distill-stressor/stressor.cue"
    for case in stressor_cases:
        expected_exit = 0 if case["expected_valid"] else 1
        result = recorder.run(
            "R3",
            [str(cue_bin), "vet", "-c", "-d", "#DistillW2Stressor", str(stressor_source), "json:", case["data_ref"]["path"]],
            package_root,
            expected_exit,
            timeout=30,
        )
        observed = result.returncode == 0
        case["observed_valid"] = observed
        case["status"] = "pass" if observed == case["expected_valid"] else "block"
        if case["status"] == "block":
            r3_mismatches.append({"case_id": case["case_id"], "expected_valid": case["expected_valid"], "observed_valid": observed})
    regimes["R3"] = {
        "status": "pass" if not r3_mismatches and not r3_not_evaluable else "block",
        "semantic_mismatches": r3_mismatches,
        "not_evaluable": r3_not_evaluable,
        "native_results": native_results,
        "stressor_cases": stressor_cases,
    }

    # R4: generate JSON Schema and compare external interfaces without repairs.
    generated_root = output_root / "generated-json-schema"
    generation_results: dict[str, dict[str, Any]] = {}
    for relative in targeted:
        prototype = native_results[relative]["prototype_ref"]
        if prototype is None:
            generation_results[relative] = {"status": "not_evaluable", "blockers": ["native_import_failed"]}
            continue
        destination = generated_root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        result = recorder.run(
            "R4",
            [str(cue_bin), "def", "--out", "jsonschema", "--expression", "#Root", "--outfile", str(destination), physical_ref_path(prototype)],
            root,
            0,
            timeout=30,
        )
        blockers = []
        generated = None
        if result.returncode == 0 and destination.is_file():
            try:
                generated = load_json(destination)
                validator_for(generated).check_schema(generated)
            except Exception as error:
                blockers.append(f"generated_meta_validation:{type(error).__name__}:{error}")
        else:
            blockers.append("generation_failed")
        original_projection = interface_projection(by_path[relative])
        generated_projection = interface_projection(generated) if isinstance(generated, dict) else None
        if generated_projection != original_projection:
            blockers.append("interface_projection_mismatch")
        generation_results[relative] = {
            "status": "pass" if not blockers else "block",
            "blockers": blockers,
            "original_interface": original_projection,
            "generated_interface": generated_projection,
            "generated_ref": (
                {
                    **file_ref(destination, relative),
                    "physical_path": destination.resolve().as_posix(),
                }
                if destination.is_file()
                else None
            ),
            "canonical_json_sha256": sha256_bytes(canonical_bytes(generated)) if isinstance(generated, dict) else None,
        }
    r4_cohorts = {}
    for name, paths in membership.items():
        if name == "census":
            continue
        passed = sum(generation_results[path]["status"] == "pass" for path in paths)
        r4_cohorts[name] = {"status": "pass" if passed == len(paths) else "block", "passed": passed, "total": len(paths)}
    regimes["R4"] = {
        "status": "pass" if all(item["status"] == "pass" for item in generation_results.values()) else "block",
        "cohorts": r4_cohorts,
        "results": generation_results,
    }

    # R5: unchanged consumer replay with generated schemas overlaid read-only.
    r5_cohorts = {}
    for name, paths in ((name, membership[name]) for name in config["cohorts"]):
        commands = [item for item in config["consumer_commands"] if item["cohort"] == name]
        if not commands:
            r5_cohorts[name] = {"status": "not_evaluable", "reason": "no_declared_consumer"}
            continue
        if any(generation_results[path]["status"] != "pass" for path in paths):
            r5_cohorts[name] = {"status": "not_evaluable", "reason": "generation_or_interface_blocked"}
            continue
        overlays = {root / path: generated_root / path for path in paths}
        writable_overlays = None
        if name == "invoke":
            replay_overlay = output_root / "consumer-overlays/r5/arcanum/spells/invoke"
            shutil.copytree(
                root / "arcanum/spells/invoke",
                replay_overlay,
                symlinks=True,
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
            )
            for relative in paths:
                relative_in_invoke = Path(relative).relative_to(
                    "arcanum/spells/invoke"
                )
                shutil.copyfile(
                    generated_root / relative, replay_overlay / relative_in_invoke
                )
            overlays = {}
            writable_overlays = {
                root / "arcanum/spells/invoke": replay_overlay
            }
        results = []
        for command in commands:
            completed = recorder.run(
                "R5",
                command["argv"],
                root / command.get("cwd", "."),
                command["expected_exit"],
                overlays=overlays,
                writable_overlays=writable_overlays,
                timeout=command.get("timeout_seconds", 180),
            )
            combined_output = (completed.stdout or b"") + (completed.stderr or b"")
            decoded_output = combined_output.decode("utf-8", "replace")
            missing_markers = [
                marker
                for marker in command.get("expected_output_contains", [])
                if marker not in decoded_output
            ]
            results.append(
                {
                    "command_id": command["command_id"],
                    "record_id": command_records[-1]["command_id"],
                    "missing_output_markers": missing_markers,
                    "status": (
                        "pass"
                        if completed.returncode == command["expected_exit"]
                        and not missing_markers
                        else "block"
                    ),
                }
            )
        r5_cohorts[name] = {"status": "pass" if all(item["status"] == "pass" for item in results) else "block", "results": results}
    regimes["R5"] = {"status": "pass" if all(item["status"] == "pass" for item in r5_cohorts.values()) else "block", "cohorts": r5_cohorts}

    # R6 is meaningful only after an interface-preserving primary prototype exists.
    if r4_cohorts["invoke"]["status"] != "pass":
        regimes["R6"] = {
            "status": "not_evaluable",
            "causal_blockers": ["R4.invoke.interface_preservation"],
            "exercises": [
                {"exercise_id": "shared_primitive", "status": "not_evaluable"},
                {"exercise_id": "tagged_variant", "status": "not_evaluable"},
                {"exercise_id": "conditional_rule", "status": "not_evaluable"},
                {"exercise_id": "new_invoke_stage", "status": "not_evaluable"},
            ],
        }
    else:
        regimes["R6"] = {
            "status": "block",
            "causal_blockers": ["E_MAINTENANCE_EXERCISE_IMPLEMENTATION_REQUIRED"],
            "exercises": [],
        }

    after_refs = [file_ref(root / item["path"], item["path"]) for item in input_refs]
    after_digest = tree_digest(after_refs)
    repository_unchanged = before_digest == after_digest and input_refs == after_refs
    if not repository_unchanged:
        raise ValueError("repository input drift during experiment")

    generated_refs = collect_generated_refs(generation_results)
    native_refs = sorted(
        (
            item["prototype_ref"]
            for item in native_results.values()
            if item.get("prototype_ref") is not None
        ),
        key=lambda item: item["path"],
    )
    report: dict[str, Any] = {
        "schema_version": REPORT_SCHEMA,
        "experiment_id": config["experiment_id"],
        "run_id": output_root.name,
        "authority_effect": "none",
        "claim_ceiling": config["claim_ceiling"],
        "successor_authorized": False,
        "tool": {
            "cue": {**cue_ref, "version_output_base64": base64.b64encode(version.stdout).decode("ascii"), "archive_sha256": config["cue"]["archive_sha256"]},
            "runtime": runtime_tools,
            "runner": file_ref(Path(__file__).resolve()),
            "config": file_ref(config_path),
        },
        "membership": membership_report,
        "inputs": {"before_tree_digest": before_digest, "after_tree_digest": after_digest, "unchanged": repository_unchanged, "refs": input_refs},
        "regimes": regimes,
        "commands": command_records,
        "native_prototype_tree": {
            "count": len(native_refs),
            "digest": tree_digest(native_refs),
            "refs": native_refs,
        },
        "generated_tree": {"count": len(generated_refs), "digest": tree_digest(generated_refs), "refs": generated_refs},
    }
    report["classification"] = classify(report)
    report["report_digest"] = sha256_bytes(
        canonical_bytes(reproducibility_projection(report))
    )
    report["determinism_projection_digest"] = report["report_digest"]
    report["report_integrity_digest"] = sha256_bytes(canonical_bytes(report))
    report_path = output_root / "run-report.json"
    report_path.write_bytes(canonical_bytes(report))
    return {"status": "pass" if report["classification"] not in {"reject_cue"} else "block", "classification": report["classification"], "report": file_ref(report_path), "authority_effect": "none"}


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--root", type=Path, required=True)
    result.add_argument("--cue-bin", type=Path, required=True)
    result.add_argument("--config", type=Path, required=True)
    result.add_argument("--output-dir", type=Path, required=True)
    result.add_argument("--output-format", choices=("json",), required=True)
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        result = run_experiment(args)
    except Exception as error:
        result = {"status": "block", "blocker": "E_CUE_EXPERIMENT_RUN", "detail": f"{type(error).__name__}: {error}", "authority_effect": "none"}
    sys.stdout.buffer.write(canonical_bytes(result))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
