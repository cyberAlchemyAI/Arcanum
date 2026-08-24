#!/usr/bin/env python3
"""Rehearse downstream closure before emitting an Invoke owner request."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

from jsonschema import Draft202012Validator


INVOKE_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_ROOT = INVOKE_ROOT / "schemas"
MANIFEST_SCHEMA = SCHEMA_ROOT / "preacceptance-closure-manifest-v1.schema.json"
RECEIPT_SCHEMA = SCHEMA_ROOT / "preacceptance-closure-receipt-v1.schema.json"
REVIEW_SCHEMA = SCHEMA_ROOT / "preacceptance-closure-review-v1.schema.json"
ADOPTION_SCHEMA = SCHEMA_ROOT / "preacceptance-closure-adoption-v1.schema.json"
REQUEST_SCHEMA = SCHEMA_ROOT / "owner-acceptance-request-v2.schema.json"

REQUIRED_STAGE_ORDER = [
    "invoke_material_validation",
    "invoke_file_bound_handoff",
    "work_pack_readiness",
    "task_session_until_blocker_preflight",
    "task_session_fast_entry",
    "task_session_mutation_admission",
    "task_session_governance_runner",
    "precloseout",
    "invoke_closeout",
    "task_session_terminal",
    "continuity",
]

REQUIRED_RUNTIME_RECEIPTS = {
    "governance_request",
    "execution_ticket",
    "admission_consumption",
    "executor_receipt",
    "reconciliation",
    "material_commit_disposition",
}

REQUIRED_REVIEW_CHECKS = {
    "final_postimages",
    "execution_projection",
    "consumer_closure",
    "write_partition",
    "runner_identity",
    "schema_locator",
    "runtime_derivation",
    "requested_effect",
    "reflection_adoption",
    "no_effect_determinism",
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def file_digest(path: Path) -> tuple[str, int]:
    content = path.read_bytes()
    return hashlib.sha256(content).hexdigest(), len(content)


def normalized_relative_path(raw_path: str) -> tuple[str | None, str | None]:
    normalized = raw_path.replace("\\", "/")
    candidate = PurePosixPath(normalized)
    if (
        not normalized
        or candidate.is_absolute()
        or PureWindowsPath(raw_path).is_absolute()
        or ".." in candidate.parts
    ):
        return None, f"path escape: {raw_path}"
    cleaned = str(candidate)
    if cleaned in ("", "."):
        return None, f"path escape: {raw_path}"
    return cleaned, None


def resolve_path(repository_root: Path, raw_path: str) -> tuple[Path | None, str | None]:
    normalized, error = normalized_relative_path(raw_path)
    if error:
        return None, error
    root = repository_root.resolve()
    candidate = (root / normalized).resolve(strict=False)
    try:
        candidate.relative_to(root)
    except ValueError:
        return None, f"path escape: {raw_path}"
    return candidate, None


def repository_relative(repository_root: Path, path: Path) -> str:
    return path.resolve().relative_to(repository_root.resolve()).as_posix()


def exact_ref(repository_root: Path, path: Path) -> dict[str, Any]:
    digest, size = file_digest(path)
    return {
        "path": repository_relative(repository_root, path),
        "sha256": digest,
        "size_bytes": size,
    }


def schema_errors(document: Any, schema: dict[str, Any], label: str) -> list[str]:
    errors = sorted(
        Draft202012Validator(schema).iter_errors(document),
        key=lambda item: [str(part) for part in item.absolute_path],
    )
    return [
        f"{label} schema invalid at "
        f"{'/'.join(map(str, error.absolute_path)) or '<root>'}: {error.message}"
        for error in errors
    ]


def validate_exact_ref(
    repository_root: Path, reference: dict[str, Any], label: str
) -> list[str]:
    path, error = resolve_path(repository_root, str(reference.get("path", "")))
    if error:
        return [f"{label} {error}"]
    assert path is not None
    if not path.is_file():
        return [f"missing {label}: {reference.get('path')}"]
    digest, size = file_digest(path)
    blockers: list[str] = []
    if digest != reference.get("sha256"):
        blockers.append(f"{label} digest mismatch: {reference.get('path')}")
    if size != reference.get("size_bytes"):
        blockers.append(f"{label} size mismatch: {reference.get('path')}")
    return blockers


def collect_exact_refs(value: Any, pointer: str = "") -> list[tuple[str, dict[str, Any]]]:
    refs: list[tuple[str, dict[str, Any]]] = []
    if isinstance(value, dict):
        if set(value) == {"path", "sha256", "size_bytes"}:
            refs.append((pointer or "<root>", value))
        else:
            for key, child in value.items():
                refs.extend(collect_exact_refs(child, f"{pointer}/{key}"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            refs.extend(collect_exact_refs(child, f"{pointer}/{index}"))
    return refs


def json_pointer(value: Any, pointer: str) -> tuple[bool, Any]:
    if pointer == "":
        return True, value
    if not pointer.startswith("/"):
        return False, None
    current = value
    for raw_part in pointer[1:].split("/"):
        part = raw_part.replace("~1", "/").replace("~0", "~")
        if isinstance(current, dict) and part in current:
            current = current[part]
        elif isinstance(current, list) and part.isdigit() and int(part) < len(current):
            current = current[int(part)]
        else:
            return False, None
    return True, current


def json_type(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "number"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    return "unknown"


def path_overlaps(left: str, right: str) -> bool:
    left_parts = PurePosixPath(left).parts
    right_parts = PurePosixPath(right).parts
    shorter = min(len(left_parts), len(right_parts))
    return left_parts[:shorter] == right_parts[:shorter]


def validate_postimage_hygiene(path: Path, label: str) -> list[str]:
    content = path.read_bytes()
    blockers: list[str] = []
    if content and not content.endswith(b"\n"):
        blockers.append(f"E16_CREATE_TARGET_HYGIENE final newline missing: {label}")
    for line_number, line in enumerate(content.splitlines(), 1):
        if line.endswith((b" ", b"\t")):
            blockers.append(
                f"E16_CREATE_TARGET_HYGIENE trailing whitespace: {label}:{line_number}"
            )
    return blockers


def repository_state_digest(repository_root: Path) -> str:
    root = repository_root.resolve()
    pieces: list[bytes] = []
    commands = [
        ["git", "-C", str(root), "diff", "--binary", "--no-ext-diff", "HEAD"],
        ["git", "-C", str(root), "diff", "--cached", "--binary", "--no-ext-diff"],
        [
            "git",
            "-C",
            str(root),
            "status",
            "--porcelain=v2",
            "-z",
            "--untracked-files=all",
        ],
    ]
    for command in commands:
        completed = subprocess.run(command, check=False, capture_output=True)
        pieces.append(str(completed.returncode).encode("ascii") + b"\0")
        pieces.append(completed.stdout)
        pieces.append(completed.stderr)
    untracked = subprocess.run(
        [
            "git",
            "-C",
            str(root),
            "ls-files",
            "--others",
            "--exclude-standard",
            "-z",
        ],
        check=False,
        capture_output=True,
    )
    if untracked.returncode == 0:
        for raw_path in sorted(filter(None, untracked.stdout.split(b"\0"))):
            try:
                relative = raw_path.decode("utf-8")
            except UnicodeDecodeError:
                pieces.append(raw_path + b"\0invalid-utf8")
                continue
            path = root / relative
            pieces.append(raw_path + b"\0")
            if path.is_file() and not path.is_symlink():
                pieces.append(hashlib.sha256(path.read_bytes()).digest())
            elif path.is_symlink():
                pieces.append(b"symlink\0" + os.readlink(path).encode("utf-8"))
            else:
                pieces.append(b"non-file")
    return hashlib.sha256(b"".join(pieces)).hexdigest()


def protected_digest(
    repository_root: Path, references: list[dict[str, Any]]
) -> str:
    inventory: list[dict[str, Any]] = []
    seen: set[str] = set()
    for reference in sorted(references, key=lambda item: item["path"]):
        path_string = reference["path"]
        if path_string in seen:
            continue
        seen.add(path_string)
        path, error = resolve_path(repository_root, path_string)
        if error or path is None or not path.is_file():
            inventory.append({"path": path_string, "state": "missing"})
            continue
        digest, size = file_digest(path)
        inventory.append(
            {"path": path_string, "state": "present", "sha256": digest, "size": size}
        )
    return canonical_digest(inventory)


def validate_assertions(
    document: Any, assertions: list[dict[str, Any]], label: str
) -> list[str]:
    blockers: list[str] = []
    for assertion in assertions:
        pointer = assertion["json_pointer"]
        present, value = json_pointer(document, pointer)
        operator = assertion["operator"]
        if operator == "absent" and present:
            blockers.append(f"E02_PENDING_POSTIMAGE expected absent {label}{pointer}")
        elif operator == "equals" and (
            not present or value != assertion.get("value")
        ):
            blockers.append(f"E02_PENDING_POSTIMAGE final assertion failed {label}{pointer}")
        elif operator == "not_equals" and present and value == assertion.get("value"):
            blockers.append(f"E02_PENDING_POSTIMAGE forbidden final value {label}{pointer}")
    return blockers


def validate_adoption_document(adoption: dict[str, Any]) -> list[str]:
    blockers = schema_errors(adoption, load_json(ADOPTION_SCHEMA), "adoption")
    projection = dict(adoption)
    expected_digest = projection.pop("receipt_digest", None)
    if expected_digest != canonical_digest(projection):
        blockers.append("reflection adoption receipt digest mismatch")
    if adoption.get("status") not in ("implemented", "enforced"):
        blockers.append("reflection adoption is not implemented or enforced")
    negative = adoption.get("negative_regression_ref", {})
    cross = adoption.get("cross_capability_regression_ref", {})
    if negative.get("result") != "pass":
        blockers.append("negative regression has not passed")
    if cross.get("result") != "pass":
        blockers.append("E05_ADMISSION_BINDINGS cross-capability regression has not passed")
    return blockers


def validate_manifest(
    manifest: dict[str, Any], repository_root: Path
) -> tuple[list[str], list[dict[str, Any]]]:
    blockers = schema_errors(manifest, load_json(MANIFEST_SCHEMA), "manifest")
    all_refs = [reference for _, reference in collect_exact_refs(manifest)]
    for pointer, reference in collect_exact_refs(manifest):
        blockers.extend(validate_exact_ref(repository_root, reference, pointer))
    if blockers:
        return sorted(set(blockers)), all_refs

    projection = manifest["normalized_execution_projection"]
    requested = manifest["requested_effect"]
    rehearsal = manifest["consumer_rehearsal"]

    if requested["material_approval_owner"] != requested["lifecycle_owner"]:
        blockers.append("E01_OWNER_PROVENANCE material approval owner must equal lifecycle owner")

    final_targets = [item["target_path"] for item in manifest["final_postimages"]]
    if len(final_targets) != len(set(final_targets)):
        blockers.append("duplicate final postimage target")
    if sorted(final_targets) != sorted(requested["target_paths"]):
        blockers.append("requested effect target paths do not equal final postimages")

    if projection["current_unit"] != projection["unit_id"]:
        blockers.append("current unit does not equal selected unit")
    if projection["admitted_frontier"][0] != projection["current_unit"]:
        blockers.append("E04_FRONTIER_BUDGET current unit is not first admitted frontier unit")
    if projection["request_budget"] != 1:
        blockers.append("E04_FRONTIER_BUDGET request budget must equal one")
    if any(route["target"] != projection["current_unit"] for route in projection["routes"]):
        blockers.append("admitted route target differs from current unit")
    if projection["successor_execution_allowed"]:
        blockers.append("E15_CONTINUITY successor execution is forbidden in the current unit")

    partitions = projection["write_partitions"]
    material = set(partitions["material_writes"])
    execution = set(partitions["execution_outputs"])
    transient = set(partitions["transient_outputs"])
    allowed = set(partitions["allowed_writes"])
    protected = set(partitions["protected_paths"])
    if material & execution or material & transient or execution & transient:
        blockers.append("write partitions overlap")
    if material | execution | transient != allowed:
        blockers.append("write partition union does not equal allowed writes")
    if not allowed.issubset(set(requested["authority_write_ceiling"])):
        blockers.append("E14_WRITE_CEILING machine allowed writes exceed owner authority ceiling")
    for write in allowed:
        if any(path_overlaps(write, protected_path) for protected_path in protected):
            blockers.append(f"allowed write overlaps protected path: {write}")

    stage_ids = [stage["stage_id"] for stage in rehearsal["stages"]]
    if stage_ids != REQUIRED_STAGE_ORDER:
        blockers.append("E03_SPLIT_PROJECTION consumer stages are skipped, duplicated, or reordered")
    if rehearsal["determinism_runs"] != 2:
        blockers.append("E09_NONDETERMINISM rehearsal must run exactly twice")
    source_ref = projection["source_ref"]
    for stage in rehearsal["stages"]:
        if stage["projection_ref"] != source_ref:
            blockers.append(f"E03_SPLIT_PROJECTION {stage['stage_id']} uses another execution projection")
        if stage["runner_ref"]["path"] not in stage["argv"]:
            blockers.append(f"runner invocation does not bind exact runner: {stage['stage_id']}")
        if (
            stage["exercised_runner_ref"]["path"] not in stage["argv"]
            and stage["exercised_runner_ref"]["path"]
            not in stage["environment"].values()
        ):
            blockers.append(
                f"consumer invocation does not bind exact exercised runner: {stage['stage_id']}"
            )
        if not stage["strict_exit_propagation"]:
            blockers.append(f"E08_EXIT_MASKING strict failure propagation missing: {stage['stage_id']}")
        if not set(stage["environment_names"]).issubset(
            set(projection["runner"]["environment_names"])
        ):
            blockers.append(f"stage environment exceeds runner allowlist: {stage['stage_id']}")
    governance = rehearsal["stages"][REQUIRED_STAGE_ORDER.index("task_session_governance_runner")]
    if governance["exercised_runner_ref"] != projection["runner"]["ref"]:
        blockers.append("E13_RUNNER_IDENTITY tested governance runner differs from authorized runner")
    if projection["runner"]["ref"]["path"] not in projection["runner"]["argv"]:
        blockers.append("authorized runtime invocation omits exact runner path")

    derivation_classes = {
        derivation["receipt_class"]
        for derivation in manifest["runtime_receipt_derivations"]
    }
    missing_derivations = REQUIRED_RUNTIME_RECEIPTS - derivation_classes
    if missing_derivations:
        blockers.append(
            "E12_CAUSAL_MATERIALIZATION missing runtime receipt derivations: "
            + ", ".join(sorted(missing_derivations))
        )

    for postimage in manifest["final_postimages"]:
        target, _ = resolve_path(repository_root, postimage["target_path"])
        baseline = postimage["baseline"]
        if baseline["state"] == "present":
            if target is None or not target.is_file():
                blockers.append(f"missing live baseline: {postimage['target_path']}")
            else:
                digest, size = file_digest(target)
                if digest != baseline["sha256"] or size != baseline["size_bytes"]:
                    blockers.append(f"live baseline drift: {postimage['target_path']}")
        elif target is not None and target.exists():
            blockers.append(f"absent baseline now exists: {postimage['target_path']}")
        postimage_path, _ = resolve_path(
            repository_root, postimage["postimage_ref"]["path"]
        )
        assert postimage_path is not None
        blockers.extend(
            validate_postimage_hygiene(postimage_path, postimage["postimage_ref"]["path"])
        )
        try:
            postimage_document = load_json(postimage_path)
        except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
            blockers.append(f"final postimage JSON invalid: {error}")
        else:
            blockers.extend(
                validate_assertions(
                    postimage_document,
                    postimage["lifecycle_assertions"],
                    postimage["postimage_ref"]["path"],
                )
            )

    for locator in projection["schemas_and_locators"]:
        if locator["resolution_count"] != 1:
            blockers.append("E06_DOUBLE_ROOT locator must be rooted exactly once")
        if locator["canonical_locator"] != locator["schema_ref"]["path"]:
            blockers.append("E10_EXACT_SCHEMA_LOCATOR equivalent schema path is not canonical locator")
        if locator["allow_equivalent_path"]:
            blockers.append("E10_EXACT_SCHEMA_LOCATOR equivalent schema paths are forbidden")
        document_path, _ = resolve_path(repository_root, locator["document_ref"]["path"])
        assert document_path is not None
        try:
            document = load_json(document_path)
        except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
            blockers.append(f"locator document invalid: {error}")
            continue
        present, value = json_pointer(document, locator["json_pointer"])
        if not present or json_type(value) != locator["expected_json_type"]:
            blockers.append(
                "E07_SCHEMA_TYPE locator JSON type mismatch: "
                f"{locator['document_ref']['path']}{locator['json_pointer']}"
            )

    for stage in rehearsal["stages"]:
        for check in stage["schema_checks"]:
            document_path, _ = resolve_path(repository_root, check["document_ref"]["path"])
            schema_path, _ = resolve_path(repository_root, check["schema_ref"]["path"])
            assert document_path is not None and schema_path is not None
            try:
                document = load_json(document_path)
                schema = load_json(schema_path)
            except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
                blockers.append(f"schema check input invalid: {error}")
                continue
            errors = schema_errors(document, schema, stage["stage_id"])
            if errors:
                blockers.append(f"E11_RECEIPT_SCHEMA {errors[0]}")

    adoption_path, _ = resolve_path(repository_root, manifest["reflection_adoption_ref"]["path"])
    assert adoption_path is not None
    try:
        adoption = load_json(adoption_path)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        blockers.append(f"reflection adoption invalid: {error}")
    else:
        blockers.extend(validate_adoption_document(adoption))

    return sorted(set(blockers)), all_refs


def run_stages(
    manifest: dict[str, Any], repository_root: Path
) -> tuple[list[dict[str, Any]], list[str]]:
    projection = manifest["normalized_execution_projection"]
    results: list[dict[str, Any]] = []
    blockers: list[str] = []
    with tempfile.TemporaryDirectory(prefix="arcanum-preacceptance-") as directory:
        rehearsal_root = Path(directory)
        for stage in manifest["consumer_rehearsal"]["stages"]:
            literal_invocation = {
                "argv": stage["argv"],
                "cwd": stage["cwd"],
                "environment_names": stage["environment_names"],
                "environment": stage["environment"],
                "runner_ref": stage["runner_ref"],
                "exercised_runner_ref": stage["exercised_runner_ref"],
            }
            argv = [
                argument.replace("{rehearsal_root}", str(rehearsal_root))
                for argument in stage["argv"]
            ]
            if stage["cwd"] == ".":
                cwd, path_error = repository_root.resolve(), None
            else:
                cwd, path_error = resolve_path(repository_root, stage["cwd"])
            if path_error or cwd is None or not cwd.is_dir():
                blockers.append(f"invalid stage cwd {stage['stage_id']}: {stage['cwd']}")
                break
            environment = {
                name: os.environ[name]
                for name in stage["environment_names"]
                if name in os.environ
            }
            environment.update(
                {
                    "LC_ALL": "C",
                    "TZ": "UTC",
                    "PYTHONDONTWRITEBYTECODE": "1",
                    "PREACCEPTANCE_REHEARSAL_ROOT": str(rehearsal_root),
                }
            )
            environment.update(
                {
                    name: value.replace("{rehearsal_root}", str(rehearsal_root))
                    for name, value in stage["environment"].items()
                }
            )
            try:
                completed = subprocess.run(
                    argv,
                    cwd=cwd,
                    env=environment,
                    check=False,
                    capture_output=True,
                    timeout=stage["timeout_seconds"],
                )
                exit_code = completed.returncode
            except subprocess.TimeoutExpired:
                exit_code = 124
            schema_check_ids = [
                canonical_digest(check) for check in stage["schema_checks"]
            ]
            result = {
                "stage_id": stage["stage_id"],
                "runner_ref": stage["runner_ref"],
                "invocation_digest": canonical_digest(literal_invocation),
                "exit_code": exit_code,
                "schema_checks": schema_check_ids,
                "result": "pass" if exit_code == 0 else "block",
            }
            results.append(result)
            if exit_code != 0:
                blockers.append(
                    f"consumer stage failed with exit {exit_code}: {stage['stage_id']}"
                )
                break
    if len(results) != len(REQUIRED_STAGE_ORDER):
        blockers.append("consumer rehearsal stopped before complete closure")
    if projection["successor_execution_allowed"]:
        blockers.append("successor execution observed or allowed")
    return results, blockers


def render_receipt(
    manifest_path: Path, repository_root: Path
) -> tuple[dict[str, Any], int]:
    manifest = load_json(manifest_path)
    manifest_ref = exact_ref(repository_root, manifest_path)
    graph_digest = canonical_digest(manifest)
    actual_runner_ref = exact_ref(repository_root, Path(__file__))
    repository_before = repository_state_digest(repository_root)
    refs = [reference for _, reference in collect_exact_refs(manifest)]
    protected_before = protected_digest(repository_root, refs)
    blockers, _ = validate_manifest(manifest, repository_root)
    first_results: list[dict[str, Any]] = []
    run_digests: list[str] = []
    if not blockers:
        for run_index in range(2):
            results, run_blockers = run_stages(manifest, repository_root)
            if run_index == 0:
                first_results = results
            run_digests.append(canonical_digest(results))
            blockers.extend(run_blockers)
            if run_blockers:
                break
    if len(run_digests) < 2:
        run_digests.extend([canonical_digest([])] * (2 - len(run_digests)))
    byte_stable = run_digests[0] == run_digests[1] and not blockers
    if not byte_stable and not blockers:
        blockers.append("E09_NONDETERMINISM rehearsal result changed across two runs")
    protected_after = protected_digest(repository_root, refs)
    repository_after = repository_state_digest(repository_root)
    if protected_before != protected_after:
        blockers.append("protected inputs changed during rehearsal")
    if repository_before != repository_after:
        blockers.append("repository state changed during no-effect rehearsal")
    blockers = sorted(set(blockers))
    receipt: dict[str, Any] = {
        "schema_version": "invoke.preacceptance-closure-receipt.v1",
        "closure_id": str(manifest.get("closure_id", "invalid-closure")),
        "manifest_ref": manifest_ref,
        "closure_graph_digest": graph_digest,
        "runner_ref": actual_runner_ref,
        "result": "pass" if not blockers else "block",
        "blockers": blockers,
        "stage_results": first_results,
        "protected_inputs": {
            "count": len({reference["path"] for reference in refs}),
            "before_digest": protected_before,
            "after_digest": protected_after,
            "unchanged": protected_before == protected_after,
        },
        "repository_state": {
            "before_digest": repository_before,
            "after_digest": repository_after,
            "unchanged": repository_before == repository_after,
        },
        "write_observation": {
            "repository_writes": 0 if repository_before == repository_after else 1,
            "protected_writes": 0 if protected_before == protected_after else 1,
            "external_effects_observed": False,
        },
        "determinism": {
            "runs": 2,
            "run_result_digest": canonical_digest(run_digests),
            "byte_stable": byte_stable,
        },
        "authority_effect": "none",
        "claim_ceiling": (
            "No-effect preacceptance rehearsal evidence only; no acceptance, apply, "
            "execution, publication, Git, deployment, or external authority."
        ),
    }
    receipt["receipt_digest"] = canonical_digest(receipt)
    receipt_errors = schema_errors(receipt, load_json(RECEIPT_SCHEMA), "receipt")
    if receipt_errors:
        raise ValueError("; ".join(receipt_errors))
    return receipt, 0 if receipt["result"] == "pass" else 1


def verify_receipt_digest(document: dict[str, Any], label: str) -> list[str]:
    projection = dict(document)
    expected = projection.pop("receipt_digest", None)
    if expected != canonical_digest(projection):
        return [f"{label} digest mismatch"]
    return []


def validate_review(
    review: dict[str, Any], manifest: dict[str, Any], receipt: dict[str, Any]
) -> list[str]:
    blockers = schema_errors(review, load_json(REVIEW_SCHEMA), "review")
    blockers.extend(verify_receipt_digest(review, "review receipt"))
    check_ids = [check.get("check_id") for check in review.get("checks", [])]
    if set(check_ids) != REQUIRED_REVIEW_CHECKS or len(check_ids) != len(set(check_ids)):
        blockers.append("independent review does not contain exactly the required checks")
    if any(check.get("result") != "pass" for check in review.get("checks", [])):
        blockers.append("independent review contains a blocking check")
    if review.get("result") != "pass":
        blockers.append("independent review did not pass")
    if review.get("closure_graph_digest") != receipt.get("closure_graph_digest"):
        blockers.append("review closure graph digest mismatch")
    runner_role = manifest["normalized_execution_projection"]["runner"]["authority_role"]
    reviewer = review.get("reviewer", {})
    if runner_role not in reviewer.get("independent_from", []):
        blockers.append("reviewer does not declare independence from rehearsal owner")
    if reviewer.get("identity") == runner_role:
        blockers.append("reviewer identity equals rehearsal owner")
    return blockers


def exact_ref_matches(actual: dict[str, Any], expected: dict[str, Any]) -> bool:
    return actual == expected


def emit_request(
    repository_root: Path,
    manifest_path: Path,
    receipt_path: Path,
    review_path: Path,
    adoption_path: Path,
    base_request_path: Path,
) -> dict[str, Any]:
    manifest = load_json(manifest_path)
    receipt = load_json(receipt_path)
    review = load_json(review_path)
    adoption = load_json(adoption_path)
    base_request = load_json(base_request_path)
    blockers: list[str] = []
    blockers.extend(schema_errors(manifest, load_json(MANIFEST_SCHEMA), "manifest"))
    blockers.extend(schema_errors(receipt, load_json(RECEIPT_SCHEMA), "receipt"))
    blockers.extend(verify_receipt_digest(receipt, "closure receipt"))
    blockers.extend(validate_review(review, manifest, receipt))
    blockers.extend(validate_adoption_document(adoption))
    graph_digest = canonical_digest(manifest)
    if receipt.get("result") != "pass":
        blockers.append("closure receipt did not pass")
    if receipt.get("closure_graph_digest") != graph_digest:
        blockers.append("closure receipt graph digest mismatch")
    manifest_ref = exact_ref(repository_root, manifest_path)
    receipt_ref = exact_ref(repository_root, receipt_path)
    review_ref = exact_ref(repository_root, review_path)
    adoption_ref = exact_ref(repository_root, adoption_path)
    if not exact_ref_matches(receipt.get("manifest_ref", {}), manifest_ref):
        blockers.append("closure receipt manifest reference mismatch")
    if not exact_ref_matches(review.get("manifest_ref", {}), manifest_ref):
        blockers.append("review manifest reference mismatch")
    if not exact_ref_matches(review.get("closure_receipt_ref", {}), receipt_ref):
        blockers.append("review closure receipt reference mismatch")
    if not exact_ref_matches(manifest.get("reflection_adoption_ref", {}), adoption_ref):
        blockers.append("manifest reflection adoption reference mismatch")
    if blockers:
        raise ValueError("request emission blocked: " + "; ".join(sorted(set(blockers))))
    base_ref = exact_ref(repository_root, base_request_path)
    request: dict[str, Any] = {
        "schema_version": "invoke.owner-acceptance-request.v2",
        "request_id": str(
            base_request.get("request_id", f"request-{file_digest(base_request_path)[0][:16]}")
        ),
        "base_request_ref": base_ref,
        "base_request": base_request,
        "preacceptance_closure": {
            "manifest_ref": manifest_ref,
            "closure_receipt_ref": receipt_ref,
            "independent_review_ref": review_ref,
            "adoption_ref": adoption_ref,
            "closure_graph_digest": graph_digest,
        },
        "emission_gate": "pass",
        "authority_effect": "none",
        "claim_ceiling": (
            "Owner decision request only. Emission proves consumer closure and independent "
            "review; it does not accept, apply, execute, publish, commit, push, deploy, or "
            "create external effects."
        ),
    }
    request["request_digest"] = canonical_digest(request)
    errors = schema_errors(request, load_json(REQUEST_SCHEMA), "request")
    if errors:
        raise ValueError("; ".join(errors))
    return request


def write_json_idempotent(path: Path, value: dict[str, Any], exclusive: bool) -> None:
    rendered = (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")
    if path.exists():
        if exclusive:
            raise FileExistsError(f"output already exists: {path}")
        if path.read_bytes() != rendered:
            raise FileExistsError(f"existing output differs: {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(rendered)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", default=".")
    subparsers = parser.add_subparsers(dest="command", required=True)

    rehearse = subparsers.add_parser("rehearse")
    rehearse.add_argument("--manifest", required=True)
    rehearse.add_argument("--output", required=True)

    emit = subparsers.add_parser("emit-request")
    emit.add_argument("--manifest", required=True)
    emit.add_argument("--receipt", required=True)
    emit.add_argument("--review", required=True)
    emit.add_argument("--adoption", required=True)
    emit.add_argument("--base-request", required=True)
    emit.add_argument("--output", required=True)

    args = parser.parse_args()
    repository_root = Path(args.repository_root).resolve()
    try:
        if args.command == "rehearse":
            receipt, status = render_receipt(Path(args.manifest), repository_root)
            write_json_idempotent(Path(args.output), receipt, exclusive=False)
            return status
        request = emit_request(
            repository_root,
            Path(args.manifest),
            Path(args.receipt),
            Path(args.review),
            Path(args.adoption),
            Path(args.base_request),
        )
        write_json_idempotent(Path(args.output), request, exclusive=True)
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
