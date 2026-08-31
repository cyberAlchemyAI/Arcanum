#!/usr/bin/env python3
"""Independently verify one CUE experiment run or comparison report."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import stat
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable
import yaml


RUN_SCHEMA = "arcanum.cue_schema_experiment.run_report.v1"
DECISION_SCHEMA = "arcanum.cue_schema_experiment.decision_report.v1"
CONFIG_SCHEMA = "arcanum.cue_schema_experiment.config.v1"
REGIME_IDS = ("R0", "R1", "R2", "R3", "R4", "R5", "R6")
EXPECTED_CASE_KIND_COUNTS = {
    "cardinality": 25,
    "invalid_const": 35,
    "invalid_enum": 20,
    "missing_required": 222,
    "pattern": 1,
    "persisted": 23,
    "reference_edge": 79,
    "uniqueness": 16,
    "unknown_property": 15,
    "wrong_type": 87,
}


def canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
        + "\n"
    ).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def file_ref(path: Path, display_path: str | None = None) -> dict[str, Any]:
    data = path.read_bytes()
    return {
        "path": display_path if display_path is not None else path.as_posix(),
        "sha256": sha256_bytes(data),
        "size_bytes": len(data),
    }


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def membership_digest(paths: Iterable[str]) -> str:
    return sha256_bytes(
        json.dumps(sorted(paths), ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    )


def tree_digest(refs: Iterable[dict[str, Any]]) -> str:
    projection = [
        {"path": item["path"], "sha256": item["sha256"], "size_bytes": item["size_bytes"]}
        for item in refs
    ]
    projection.sort(key=lambda item: item["path"])
    return sha256_bytes(canonical_bytes(projection))


def refs(value: Any) -> Iterable[str]:
    if isinstance(value, dict):
        if isinstance(value.get("$ref"), str):
            yield value["$ref"]
        for child in value.values():
            yield from refs(child)
    elif isinstance(value, list):
        for child in value:
            yield from refs(child)


def discover_invoke(root: Path) -> list[str]:
    invoke = root / "arcanum/spells/invoke"
    schemas = {path.name: load_json(path) for path in (invoke / "schemas").glob("*.schema.json")}
    by_id = {item.get("$id"): name for name, item in schemas.items() if isinstance(item.get("$id"), str)}
    catalog = load_json(invoke / "invoke-cli-stage-catalog.json")
    names = {"invoke-cli-stage-catalog-v1.schema.json"}
    for mode in ("define", "design"):
        for stage in catalog["modes"][mode]["stages"].values():
            for field in ("request_schema", "output_schema"):
                if stage.get(field):
                    names.add(stage[field])
    while True:
        before = len(names)
        for name in tuple(names):
            for reference in refs(schemas[name]):
                target = by_id.get(reference.split("#", 1)[0])
                if target:
                    names.add(target)
        if len(names) == before:
            break
    return sorted(f"arcanum/spells/invoke/schemas/{name}" for name in names)


def discover(root: Path, config: dict[str, Any]) -> dict[str, list[str]]:
    cohorts = {
        "invoke": discover_invoke(root),
        "orchestrate": sorted(path.relative_to(root).as_posix() for path in (root / "arcanum/runtime/orchestrate/schemas").glob("*.schema.json")),
        "work_pack_readiness": sorted(path.relative_to(root).as_posix() for path in (root / "arcanum/spells/work-pack-readiness-audit/schemas").glob("*.schema.json")),
        "infra_spec": ["arcanum/formulae/infra-spec/infra-spec.schema.json"],
        "distill": sorted(path.relative_to(root).as_posix() for path in (root / "arcanum/arcana/distill/schemas").glob("*.schema.json")),
    }
    excluded = set(config["census"]["excluded_path_segments"])
    cohorts["census"] = sorted(
        path.relative_to(root).as_posix()
        for path in (root / "arcanum").rglob("*.schema.json")
        if not (set(path.relative_to(root / "arcanum").parts) & excluded)
    )
    return cohorts


def verify_ref(path: Path, expected: dict[str, Any]) -> None:
    identity = {
        "path": expected["path"],
        "sha256": expected["sha256"],
        "size_bytes": expected["size_bytes"],
    }
    observed = file_ref(path, expected["path"])
    if observed != identity:
        raise ValueError(f"physical ref mismatch: {expected['path']}")


def resolve_report_artifact(
    report_path: Path,
    expected: dict[str, Any],
    archive_kind: str,
) -> Path:
    primary = Path(expected.get("physical_path", expected["path"]))
    if primary.is_file():
        return primary
    if report_path.parent.name != "reports":
        return primary
    package_root = report_path.parent.parent
    if archive_kind == "runner":
        return package_root / "scripts" / Path(expected["path"]).name
    if archive_kind == "config":
        return package_root / "experiment.json"
    if archive_kind == "native":
        return package_root / "prototypes/native" / expected["path"]
    if archive_kind == "generated":
        return package_root / "generated-json-schema" / expected["path"]
    if archive_kind == "run":
        return package_root / expected["path"]
    raise ValueError(f"unknown archive kind: {archive_kind}")


def verify_integrity(document: dict[str, Any]) -> None:
    expected = document.get("report_integrity_digest")
    if not isinstance(expected, str):
        raise ValueError("missing report integrity digest")
    projection = dict(document)
    del projection["report_integrity_digest"]
    if sha256_bytes(canonical_bytes(projection)) != expected:
        raise ValueError("report integrity digest")


def reproducibility_projection(report: dict[str, Any]) -> dict[str, Any]:
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


def verify_run_digest(report: dict[str, Any]) -> None:
    expected = sha256_bytes(canonical_bytes(reproducibility_projection(report)))
    if report.get("report_digest") != expected:
        raise ValueError("reproducibility report digest")
    if report.get("determinism_projection_digest") != expected:
        raise ValueError("determinism projection digest")


def verify_decision_digest(report: dict[str, Any]) -> None:
    projection = dict(report)
    projection.pop("report_integrity_digest", None)
    observed = projection.pop("report_digest", None)
    if observed != sha256_bytes(canonical_bytes(projection)):
        raise ValueError("decision report digest")


def verify_command(command: dict[str, Any]) -> None:
    for channel in ("stdout", "stderr"):
        raw = base64.b64decode(command[f"{channel}_base64"], validate=True)
        if len(raw) != command[f"{channel}_size_bytes"]:
            raise ValueError(f"{command['command_id']} {channel} size")
        if sha256_bytes(raw) != command[f"{channel}_sha256"]:
            raise ValueError(f"{command['command_id']} {channel} digest")
    if command["network_isolation"] != "bubblewrap_unshare_net":
        raise ValueError("network isolation")
    if command["expected_result"] != (
        command["expected_exit"] is None or command["exit_status"] == command["expected_exit"]
    ):
        raise ValueError(f"{command['command_id']} expected result")


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


def verify_run(root: Path, cue_bin: Path, report_path: Path, report: dict[str, Any]) -> dict[str, Any]:
    verify_integrity(report)
    verify_run_digest(report)
    if report.get("authority_effect") != "none" or report.get("successor_authorized") is not False:
        raise ValueError("authority ceiling")
    if tuple(report["regimes"]) != REGIME_IDS:
        raise ValueError("regime topology")
    cue_expected = report["tool"]["cue"]
    verify_ref(cue_bin, cue_expected)
    if not (cue_bin.stat().st_mode & stat.S_IXUSR):
        raise ValueError("CUE not executable")
    version = subprocess.run([str(cue_bin), "version"], capture_output=True, check=False)
    if version.returncode != 0 or base64.b64encode(version.stdout).decode("ascii") != cue_expected["version_output_base64"]:
        raise ValueError("CUE version output")
    config_ref = report["tool"]["config"]
    config_path = resolve_report_artifact(report_path, config_ref, "config")
    verify_ref(config_path, config_ref)
    config = load_json(config_path)
    if config.get("schema_version") != CONFIG_SCHEMA:
        raise ValueError("config schema")
    if report["tool"].get("runtime") != config.get("runtime_tools"):
        raise ValueError("runtime tool configuration")
    for name in ("node", "python"):
        expected = config["runtime_tools"][name]
        binary = Path(expected["path"])
        verify_ref(binary, expected)
        version = subprocess.run(
            [str(binary), "--version"], capture_output=True, text=True, check=False
        )
        observed_version = (version.stdout or version.stderr).strip()
        if version.returncode != 0 or observed_version != expected["version"]:
            raise ValueError(f"runtime tool version: {name}")
    runner_ref = report["tool"]["runner"]
    verify_ref(resolve_report_artifact(report_path, runner_ref, "runner"), runner_ref)
    observed_membership = discover(root, config)
    for name, paths in observed_membership.items():
        expected = report["membership"][name]
        if expected["paths"] != paths or expected["count"] != len(paths) or expected["membership_digest"] != membership_digest(paths):
            raise ValueError(f"membership: {name}")
    for case in config["cases"]:
        if case["schema_path"] not in observed_membership[case["cohort"]]:
            raise ValueError(f"case outside frozen cohort: {case['case_id']}")
    cases = report["regimes"]["R0"]["cases"]
    if len({case["case_id"] for case in cases}) != len(cases):
        raise ValueError("duplicate case id")
    observed_kind_counts: dict[str, int] = {}
    for case in cases:
        observed_kind_counts[case["kind"]] = observed_kind_counts.get(case["kind"], 0) + 1
        if case["kind"] != "persisted" and case["expected_valid"] is not False:
            raise ValueError(f"generated expected result: {case['case_id']}")
    if observed_kind_counts != EXPECTED_CASE_KIND_COUNTS:
        raise ValueError("case denominator")
    configured_cases = {case["case_id"]: case for case in config["cases"]}
    persisted_cases = {
        case["case_id"]: case for case in cases if case["kind"] == "persisted"
    }
    if set(persisted_cases) != set(configured_cases):
        raise ValueError("persisted case denominator")
    for case_id, configured in configured_cases.items():
        observed = persisted_cases[case_id]
        if (
            observed["cohort"] != configured["cohort"]
            or observed["schema_path"] != configured["schema_path"]
            or observed["expected_valid"] != configured["expected_valid"]
        ):
            raise ValueError(f"persisted expected result: {case_id}")
    infra_json = load_json(root / "arcanum/formulae/infra-spec/infra-spec.schema.json")
    infra_yaml = yaml.safe_load(
        (root / config["infra_yaml_path"]).read_text(encoding="utf-8")
    )
    parity = report["regimes"]["R0"]["infra_json_yaml_parity"]
    expected_parity = {
        "status": "pass" if infra_json == infra_yaml else "block",
        "json_semantic_digest": sha256_bytes(canonical_bytes(infra_json)),
        "yaml_semantic_digest": sha256_bytes(canonical_bytes(infra_yaml)),
    }
    if parity != expected_parity:
        raise ValueError("InfraSpec JSON/YAML parity")
    current_refs = []
    for expected in report["inputs"]["refs"]:
        path = root / expected["path"]
        verify_ref(path, expected)
        current_refs.append(expected)
    if tree_digest(current_refs) != report["inputs"]["before_tree_digest"] or report["inputs"]["before_tree_digest"] != report["inputs"]["after_tree_digest"] or report["inputs"]["unchanged"] is not True:
        raise ValueError("input tree")
    command_ids = set()
    commands_by_id = {}
    for command in report["commands"]:
        if command["command_id"] in command_ids:
            raise ValueError("duplicate command id")
        command_ids.add(command["command_id"])
        verify_command(command)
        commands_by_id[command["command_id"]] = command
    configured_consumers = {
        command["command_id"]: command for command in config["consumer_commands"]
    }
    consumer_result_groups = [report["regimes"]["R0"]["consumer_results"]]
    consumer_result_groups.extend(
        item.get("results", [])
        for item in report["regimes"]["R5"]["cohorts"].values()
        if item.get("status") in {"pass", "block"}
    )
    for results in consumer_result_groups:
        for result in results:
            configured = configured_consumers[result["command_id"]]
            recorded = commands_by_id[result["record_id"]]
            if (
                recorded["argv"] != configured["argv"]
                or recorded["expected_exit"] != configured["expected_exit"]
            ):
                raise ValueError(f"consumer topology: {result['command_id']}")
            decoded = (
                base64.b64decode(recorded["stdout_base64"])
                + base64.b64decode(recorded["stderr_base64"])
            ).decode("utf-8", "replace")
            missing = [
                marker
                for marker in configured.get("expected_output_contains", [])
                if marker not in decoded
            ]
            expected_status = (
                "pass"
                if recorded["exit_status"] == configured["expected_exit"]
                and not missing
                else "block"
            )
            if result["missing_output_markers"] != missing or result["status"] != expected_status:
                raise ValueError(f"consumer outcome: {result['command_id']}")
    generated = []
    native = []
    for expected in report["native_prototype_tree"]["refs"]:
        path = resolve_report_artifact(report_path, expected, "native")
        verify_ref(path, expected)
        native.append(expected)
    if (
        len(native) != report["native_prototype_tree"]["count"]
        or tree_digest(native) != report["native_prototype_tree"]["digest"]
    ):
        raise ValueError("native prototype tree")
    for expected in report["generated_tree"]["refs"]:
        path = resolve_report_artifact(report_path, expected, "generated")
        verify_ref(
            path,
            {
                "path": expected["path"],
                "sha256": expected["sha256"],
                "size_bytes": expected["size_bytes"],
            },
        )
        generated.append(expected)
    if len(generated) != report["generated_tree"]["count"] or tree_digest(generated) != report["generated_tree"]["digest"]:
        raise ValueError("generated tree")
    if classify(report) != report["classification"]:
        raise ValueError("classification")
    for residue in root.joinpath("arcanum").rglob("__pycache__"):
        if "cue-schema-experiment" in residue.as_posix():
            raise ValueError("repository bytecode residue")
    return {
        "schema_version": "arcanum.cue_schema_experiment.verification.v1",
        "status": "pass",
        "report_kind": "run",
        "classification": report["classification"],
        "determinism_projection_digest": report["determinism_projection_digest"],
        "report": file_ref(report_path),
        "authority_effect": "none",
    }


def verify_decision(root: Path, cue_bin: Path, report_path: Path, report: dict[str, Any]) -> dict[str, Any]:
    verify_integrity(report)
    verify_decision_digest(report)
    if report.get("authority_effect") != "none" or report.get("successor_authorized") is not False:
        raise ValueError("decision authority")
    if len(report.get("run_reports", [])) != 2:
        raise ValueError("run denominator")
    tool = report["tool"]
    verify_ref(
        resolve_report_artifact(report_path, tool["controller"], "runner"),
        tool["controller"],
    )
    verify_ref(
        resolve_report_artifact(report_path, tool["verifier"], "runner"),
        tool["verifier"],
    )
    verify_ref(
        resolve_report_artifact(report_path, tool["config"], "config"),
        tool["config"],
    )
    verify_ref(cue_bin, tool["cue"])
    runs = []
    for expected in report["run_reports"]:
        path = resolve_report_artifact(report_path, expected, "run")
        verify_ref(path, expected)
        run = load_json(path)
        if run.get("schema_version") != RUN_SCHEMA:
            raise ValueError("decision run schema")
        verify_run(root, cue_bin, path, run)
        runs.append(run)
    same_report_digest = runs[0]["report_digest"] == runs[1]["report_digest"]
    same_projection = runs[0]["determinism_projection_digest"] == runs[1]["determinism_projection_digest"]
    same_native = runs[0]["native_prototype_tree"]["digest"] == runs[1]["native_prototype_tree"]["digest"]
    same_generated = runs[0]["generated_tree"]["digest"] == runs[1]["generated_tree"]["digest"]
    same_classification = runs[0]["classification"] == runs[1]["classification"]
    observed = {
        "same_report_digest": same_report_digest,
        "same_determinism_projection": same_projection,
        "same_native_prototype_tree": same_native,
        "same_generated_raw_tree": same_generated,
        "same_classification": same_classification,
    }
    if report["comparison"] != observed:
        raise ValueError("decision comparison")
    classification = runs[0]["classification"] if all(observed.values()) else "reject_cue"
    if report["classification"] != classification:
        raise ValueError("decision classification")
    package_root = report_path.parent.parent
    archive_locations = {
        "native_prototypes": package_root / "prototypes/native",
        "strict_import_census": package_root / "prototypes/strict-import-census",
        "generated_json_schema": package_root / "generated-json-schema",
    }
    for name, directory in archive_locations.items():
        archive = report["archives"][name]
        observed_refs = []
        for expected in archive["refs"]:
            verify_ref(directory / expected["path"], expected)
            observed_refs.append(expected)
        if (
            len(observed_refs) != archive["count"]
            or tree_digest(observed_refs) != archive["digest"]
        ):
            raise ValueError(f"decision archive: {name}")
    if (
        report["archives"]["native_prototypes"]["digest"]
        != runs[0]["native_prototype_tree"]["digest"]
        or report["archives"]["generated_json_schema"]["digest"]
        != runs[0]["generated_tree"]["digest"]
        or report["archives"]["strict_import_census"]["count"]
        != runs[0]["regimes"]["R2"]["census"]["passed"]
    ):
        raise ValueError("decision archive binding")
    expected_basis = {
        "r0_baseline_status": runs[0]["regimes"]["R0"]["status"],
        "r1_false_rejections": len(runs[0]["regimes"]["R1"]["semantic_mismatches"]),
        "r2_strict_import_passed": runs[0]["regimes"]["R2"]["census"]["passed"],
        "r2_strict_import_total": runs[0]["regimes"]["R2"]["census"]["total"],
        "r3_native_prototypes_materialized": runs[0]["native_prototype_tree"]["count"],
        "r3_native_prototypes_targeted": len(runs[0]["regimes"]["R3"]["native_results"]),
        "r3_semantic_mismatches": len(runs[0]["regimes"]["R3"]["semantic_mismatches"]),
        "r3_not_evaluable_cases": len(runs[0]["regimes"]["R3"]["not_evaluable"]),
        "r4_interface_preserving_cohorts": sum(
            item["status"] == "pass"
            for item in runs[0]["regimes"]["R4"]["cohorts"].values()
        ),
        "r4_total_cohorts": len(runs[0]["regimes"]["R4"]["cohorts"]),
        "timed_out_commands": sum(item["timed_out"] for item in runs[0]["commands"]),
        "rule": "Any semantic mismatch or CUE tool failure requires reject_cue.",
    }
    if report["classification_basis"] != expected_basis:
        raise ValueError("decision classification basis")
    return {
        "schema_version": "arcanum.cue_schema_experiment.verification.v1",
        "status": "pass",
        "report_kind": "decision",
        "classification": classification,
        "report": file_ref(report_path),
        "authority_effect": "none",
    }


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--root", type=Path, required=True)
    result.add_argument("--cue-bin", type=Path, required=True)
    result.add_argument("--report", type=Path, required=True)
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        root = args.root.resolve()
        cue_bin = args.cue_bin.resolve()
        report_path = args.report.resolve()
        report = load_json(report_path)
        if report.get("schema_version") == RUN_SCHEMA:
            result = verify_run(root, cue_bin, report_path, report)
        elif report.get("schema_version") == DECISION_SCHEMA:
            result = verify_decision(root, cue_bin, report_path, report)
        else:
            raise ValueError("report schema")
    except Exception as error:
        result = {"schema_version": "arcanum.cue_schema_experiment.verification.v1", "status": "block", "blocker": "E_CUE_EXPERIMENT_VERIFY", "detail": f"{type(error).__name__}: {error}", "authority_effect": "none"}
    sys.stdout.buffer.write(canonical_bytes(result))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
