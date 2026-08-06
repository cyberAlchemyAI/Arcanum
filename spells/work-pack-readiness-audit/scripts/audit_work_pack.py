#!/usr/bin/env python3
"""Audit a normalized work-pack frontier without executing target commands."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import sys
from collections import Counter, defaultdict, deque
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

from jsonschema import Draft202012Validator

try:
    from plan_semantics import (
        NORMALIZER_VERSION,
        PlanSemanticError,
        build_plan_semantics,
    )
except ModuleNotFoundError:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from plan_semantics import (  # type: ignore[no-redef]
        NORMALIZER_VERSION,
        PlanSemanticError,
        build_plan_semantics,
    )


SPELL_ROOT = Path(__file__).resolve().parents[1]
CONFIG_SCHEMA = SPELL_ROOT / "schemas" / "audit-config.schema.json"
REPORT_SCHEMA = SPELL_ROOT / "schemas" / "audit-report.schema.json"
SIGNAL_SCHEMA = SPELL_ROOT / "schemas" / "refresh-signal-pack.schema.json"
CONFIG_SCHEMA_V2 = SPELL_ROOT / "schemas" / "audit-config-v2.schema.json"
REPORT_SCHEMA_V2 = SPELL_ROOT / "schemas" / "audit-report-v2.schema.json"
MANIFEST_SCHEMA = SPELL_ROOT / "schemas" / "objective-execution-manifest.schema.json"
PLAN_MANIFEST_SCHEMA = SPELL_ROOT / "schemas" / "plan-semantic-manifest.schema.json"
SELECTION_HANDOFF_SCHEMA = SPELL_ROOT / "schemas" / "selection-handoff.schema.json"
STATUS_BLOCK = "block"


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


def digest_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def schema_errors(document: Any, schema: dict[str, Any], label: str) -> list[str]:
    return [
        f"{label} invalid at "
        f"{'/'.join(map(str, error.absolute_path)) or '<root>'}: {error.message}"
        for error in sorted(
            Draft202012Validator(schema).iter_errors(document),
            key=lambda item: list(item.absolute_path),
        )
    ]


def normalized_relative_path(
    raw_path: str, *, allow_attempt_token: bool = False
) -> tuple[str | None, str | None]:
    value = raw_path
    if allow_attempt_token:
        value = value.replace("{attempt_id}", "attempt-id")
    if (
        not value
        or "\x00" in value
        or "$" in value
        or "*" in value
        or "?" in value
        or "[" in value
        or "]" in value
        or "<" in value
        or ">" in value
    ):
        return None, f"unsafe or unresolved path: {raw_path}"
    value = value.replace("\\", "/")
    path = PurePosixPath(value)
    if (
        path.is_absolute()
        or PureWindowsPath(raw_path).is_absolute()
        or ".." in path.parts
    ):
        return None, f"path escape: {raw_path}"
    normalized = str(path)
    if normalized in ("", "."):
        return None, f"invalid relative path: {raw_path}"
    if allow_attempt_token:
        normalized = normalized.replace("attempt-id", "{attempt_id}")
    return normalized, None


def resolve_inside(
    root: Path, raw_path: str, *, must_exist: bool
) -> tuple[Path | None, str | None]:
    normalized, error = normalized_relative_path(raw_path)
    if error:
        return None, error
    assert normalized is not None
    root = root.resolve()
    candidate = root / normalized
    try:
        resolved = candidate.resolve(strict=must_exist)
    except FileNotFoundError:
        return None, f"missing path: {raw_path}"
    try:
        resolved.relative_to(root)
    except ValueError:
        return None, f"symlink or path escape: {raw_path}"
    return resolved, None


def exact_ref_key(reference: dict[str, Any]) -> tuple[str, str, int]:
    return (reference["path"], reference["sha256"], reference["size_bytes"])


def gather_exact_refs(config: dict[str, Any]) -> list[dict[str, Any]]:
    references = [
        config["work_pack"],
        config["task_session_request_schema"],
        config["terminal_receipt_schema"],
        *config["control_artifacts"],
    ]
    if config.get("handoff_state"):
        references.append(config["handoff_state"]["artifact_ref"])
    semantic = config.get("terminal_receipt_semantic_validator")
    if semantic:
        references.append(semantic)
    for unit in config["units"]:
        references.append(unit["contract_ref"])
        material = unit.get("material_package")
        if material:
            references.extend((material["package_ref"], material["receipt_ref"]))
        references.extend(
            item["receipt_ref"] for item in unit["dependency_receipts"]
        )
    unique: dict[str, dict[str, Any]] = {}
    for reference in references:
        previous = unique.get(reference["path"])
        if previous is not None and exact_ref_key(previous) != exact_ref_key(reference):
            raise ValueError(
                f"conflicting exact references for {reference['path']}"
            )
        unique[reference["path"]] = reference
    return [unique[path] for path in sorted(unique)]


def capture_snapshot(
    root: Path, references: list[dict[str, Any]]
) -> tuple[dict[str, tuple[str, int]], list[str]]:
    snapshot: dict[str, tuple[str, int]] = {}
    errors: list[str] = []
    for reference in references:
        candidate, path_error = resolve_inside(
            root, reference["path"], must_exist=True
        )
        if path_error:
            errors.append(path_error)
            continue
        assert candidate is not None
        if not candidate.is_file():
            errors.append(f"exact artifact is not a file: {reference['path']}")
            continue
        content = candidate.read_bytes()
        digest = digest_bytes(content)
        size = len(content)
        if digest != reference["sha256"]:
            errors.append(f"digest mismatch: {reference['path']}")
        if size != reference["size_bytes"]:
            errors.append(f"size mismatch: {reference['path']}")
        snapshot[reference["path"]] = (digest, size)
    return snapshot, errors


def snapshot_digest(snapshot: dict[str, tuple[str, int]]) -> str:
    payload = [
        {"path": path, "sha256": values[0], "size_bytes": values[1]}
        for path, values in sorted(snapshot.items())
    ]
    return digest_bytes(canonical_bytes(payload))


def finding(
    findings: list[dict[str, Any]],
    *,
    category: str,
    scope: str,
    claim: str,
    evidence: list[str],
    target_paths: list[str],
    severity: str = "blocker",
) -> str:
    finding_id = f"WPA-{len(findings) + 1:03d}"
    findings.append(
        {
            "id": finding_id,
            "category": category,
            "severity": severity,
            "scope": scope,
            "claim": claim,
            "evidence": evidence,
            "target_paths": target_paths,
        }
    )
    return finding_id


def graph_checks(
    config: dict[str, Any],
    findings: list[dict[str, Any]],
    unit_blockers: dict[str, list[str]],
) -> list[str]:
    units = config["units"]
    ids = [unit["unit_id"] for unit in units]
    counts = Counter(ids)
    by_id = {unit["unit_id"]: unit for unit in units}
    global_targets = config["refresh_targets"]
    for unit_id, count in counts.items():
        if count > 1:
            blocker = finding(
                findings,
                category="graph",
                scope=unit_id,
                claim="unit ID is duplicated",
                evidence=[f"{unit_id} appears {count} times"],
                target_paths=global_targets,
            )
            unit_blockers[unit_id].append(blocker)

    for unit in units:
        unit_id = unit["unit_id"]
        contract_path = unit["contract_ref"]["path"]
        contract = (Path(config["_root"]) / contract_path).read_text(
            encoding="utf-8"
        )
        if unit["contract_kind"] != "full-task" or unit_id not in contract:
            blocker = finding(
                findings,
                category="closeout",
                scope=unit_id,
                claim="unit has no full task contract",
                evidence=[
                    f"contract_kind={unit['contract_kind']}",
                    f"contract={contract_path}",
                ],
                target_paths=[contract_path],
            )
            unit_blockers[unit_id].append(blocker)
        for dependency in unit["dependencies"]:
            if dependency not in by_id:
                blocker = finding(
                    findings,
                    category="graph",
                    scope=unit_id,
                    claim="dependency is outside the captured work pack",
                    evidence=[f"missing dependency: {dependency}"],
                    target_paths=global_targets,
                )
                unit_blockers[unit_id].append(blocker)
        successor = unit["successor"]
        if successor is not None and successor not in by_id:
            blocker = finding(
                findings,
                category="graph",
                scope=unit_id,
                claim="successor is outside the captured work pack",
                evidence=[f"missing successor: {successor}"],
                target_paths=global_targets,
            )
            unit_blockers[unit_id].append(blocker)
        elif successor is not None and unit_id not in by_id[successor]["dependencies"]:
            blocker = finding(
                findings,
                category="graph",
                scope=unit_id,
                claim="successor does not depend on the current unit",
                evidence=[f"{successor} dependencies omit {unit_id}"],
                target_paths=global_targets,
            )
            unit_blockers[unit_id].append(blocker)

    indegree = {unit_id: 0 for unit_id in by_id}
    children: dict[str, list[str]] = defaultdict(list)
    for unit in units:
        for dependency in unit["dependencies"]:
            if dependency in by_id:
                indegree[unit["unit_id"]] += 1
                children[dependency].append(unit["unit_id"])
    queue = deque(sorted(unit_id for unit_id, degree in indegree.items() if degree == 0))
    visited: list[str] = []
    while queue:
        current = queue.popleft()
        visited.append(current)
        for child in sorted(children[current]):
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
    if len(visited) != len(by_id):
        cyclic = sorted(set(by_id) - set(visited))
        blocker = finding(
            findings,
            category="graph",
            scope="work-pack",
            claim="dependency graph contains a cycle",
            evidence=[f"cyclic or unreachable units: {', '.join(cyclic)}"],
            target_paths=global_targets,
        )
        for unit_id in cyclic:
            unit_blockers[unit_id].append(blocker)

    ready = []
    for unit in units:
        if unit["state"] != "planned":
            continue
        if all(by_id[dep]["state"] == "complete" for dep in unit["dependencies"] if dep in by_id):
            ready.append(unit["unit_id"])
    if len(ready) > 1:
        blocker = finding(
            findings,
            category="graph",
            scope="work-pack",
            claim="ready frontier is ambiguous",
            evidence=[f"ready units: {', '.join(sorted(ready))}"],
            target_paths=global_targets,
        )
        for unit_id in ready:
            unit_blockers[unit_id].append(blocker)
    return sorted(ready)


def command_and_write_checks(
    config: dict[str, Any],
    findings: list[dict[str, Any]],
    unit_blockers: dict[str, list[str]],
) -> None:
    root = Path(config["_root"])
    immutable = config["immutable_paths"]
    writers: dict[str, list[str]] = defaultdict(list)
    for unit in config["units"]:
        unit_id = unit["unit_id"]
        attempt_required = unit["attempt"]["required"]
        for key in ("material_writes", "execution_outputs", "allowed_writes"):
            for raw_path in unit[key]:
                normalized, path_error = normalized_relative_path(
                    raw_path, allow_attempt_token=attempt_required
                )
                if path_error or normalized != raw_path:
                    blocker = finding(
                        findings,
                        category="path",
                        scope=unit_id,
                        claim=f"{key} contains an unsafe or noncanonical path",
                        evidence=[path_error or f"noncanonical path: {raw_path}"],
                        target_paths=[unit["contract_ref"]["path"]],
                    )
                    unit_blockers[unit_id].append(blocker)
                    continue
                writers[raw_path].append(unit_id)
                for immutable_path in immutable:
                    immutable_prefix = immutable_path.rstrip("/") + "/"
                    if raw_path == immutable_path or raw_path.startswith(immutable_prefix):
                        blocker = finding(
                            findings,
                            category="write-algebra",
                            scope=unit_id,
                            claim="declared write intersects immutable scope",
                            evidence=[f"{raw_path} intersects {immutable_path}"],
                            target_paths=[unit["contract_ref"]["path"]],
                        )
                        unit_blockers[unit_id].append(blocker)

        material = set(unit["material_writes"])
        outputs = set(unit["execution_outputs"])
        allowed = set(unit["allowed_writes"])
        if material & outputs or material | outputs != allowed:
            blocker = finding(
                findings,
                category="write-algebra",
                scope=unit_id,
                claim="allowed writes are not an exact disjoint partition",
                evidence=[
                    f"material={sorted(material)}",
                    f"outputs={sorted(outputs)}",
                    f"allowed={sorted(allowed)}",
                ],
                target_paths=[unit["contract_ref"]["path"]],
            )
            unit_blockers[unit_id].append(blocker)
        if unit["task_class"] == "material-mutation" and not material:
            blocker = finding(
                findings,
                category="write-algebra",
                scope=unit_id,
                claim="material mutation declares no material writes",
                evidence=["task_class=material-mutation"],
                target_paths=[unit["contract_ref"]["path"]],
            )
            unit_blockers[unit_id].append(blocker)
        if unit["task_class"] in ("output-only", "audit-only") and material:
            blocker = finding(
                findings,
                category="write-algebra",
                scope=unit_id,
                claim="non-material task declares placeholder material writes",
                evidence=[f"material writes: {sorted(material)}"],
                target_paths=[unit["contract_ref"]["path"]],
            )
            unit_blockers[unit_id].append(blocker)

        if not unit["validation_commands"]:
            blocker = finding(
                findings,
                category="command",
                scope=unit_id,
                claim="unit has no exact validation argv contract",
                evidence=["validation_commands is empty"],
                target_paths=[unit["contract_ref"]["path"]],
            )
            unit_blockers[unit_id].append(blocker)

        command_contracts = [
            ("validation", command)
            for command in unit["validation_commands"]
        ]
        command_contracts.extend(
            ("success teardown", command)
            for command in unit["attempt"]["teardown_on_success"]
        )
        command_contracts.extend(
            ("failure teardown", command)
            for command in unit["attempt"]["teardown_on_failure"]
        )
        for command_kind, command in command_contracts:
            cwd, path_error = resolve_inside(root, command["cwd"], must_exist=True)
            if path_error or cwd is None or not cwd.is_dir():
                blocker = finding(
                    findings,
                    category="command",
                    scope=unit_id,
                    claim=f"{command_kind} cwd is missing or escapes the repository",
                    evidence=[path_error or f"not a directory: {command['cwd']}"],
                    target_paths=[unit["contract_ref"]["path"]],
                )
                unit_blockers[unit_id].append(blocker)
            argv = command["argv"]
            if argv[0] != command["runtime_identity"]["executable"]:
                blocker = finding(
                    findings,
                    category="command",
                    scope=unit_id,
                    claim="argv executable and runtime identity disagree",
                    evidence=[
                        f"argv[0]={argv[0]}",
                        f"runtime executable={command['runtime_identity']['executable']}",
                    ],
                    target_paths=[unit["contract_ref"]["path"]],
                )
                unit_blockers[unit_id].append(blocker)
            if any("\n" in value or "\r" in value for value in argv):
                blocker = finding(
                    findings,
                    category="command",
                    scope=unit_id,
                    claim=f"{command_kind} argv contains control characters",
                    evidence=[repr(argv)],
                    target_paths=[unit["contract_ref"]["path"]],
                )
                unit_blockers[unit_id].append(blocker)
            if command["risk_class"] == "destructive":
                blocker = finding(
                    findings,
                    category="command",
                    scope=unit_id,
                    claim="destructive validation command is not audit-admissible",
                    evidence=[json.dumps(argv)],
                    target_paths=[unit["contract_ref"]["path"]],
                )
                unit_blockers[unit_id].append(blocker)

        attempt = unit["attempt"]
        if attempt["required"]:
            missing = []
            if "{attempt_id}" not in " ".join(unit["execution_outputs"]):
                missing.append("execution output lacks {attempt_id}")
            if not attempt["id_algorithm"]:
                missing.append("attempt ID algorithm is empty")
            if not attempt["teardown_on_success"]:
                missing.append("success teardown is empty")
            if not attempt["teardown_on_failure"]:
                missing.append("failure teardown is empty")
            if missing:
                blocker = finding(
                    findings,
                    category="attempt",
                    scope=unit_id,
                    claim="attempt lifecycle is incomplete",
                    evidence=missing,
                    target_paths=[unit["contract_ref"]["path"]],
                )
                unit_blockers[unit_id].append(blocker)

    shared = {entry["path"]: entry for entry in config["shared_write_owners"]}
    for path, unit_ids in sorted(writers.items()):
        participants = sorted(set(unit_ids))
        if len(participants) < 2:
            continue
        owner = shared.get(path)
        if owner is None or set(owner["ordered_units"]) != set(participants):
            blocker = finding(
                findings,
                category="write-algebra",
                scope="work-pack",
                claim="cross-unit write overlap has no exact shared owner contract",
                evidence=[f"{path}: {', '.join(participants)}"],
                target_paths=config["refresh_targets"],
            )
            for unit_id in participants:
                unit_blockers[unit_id].append(blocker)

    for selector in config["source_selectors"]:
        candidate, path_error = resolve_inside(root, selector, must_exist=True)
        if path_error or candidate is None or not candidate.is_file():
            finding(
                findings,
                category="path",
                scope="source-selector",
                claim="source selector is ambiguous, missing, or escapes the repository",
                evidence=[path_error or f"not a file: {selector}"],
                target_paths=config["refresh_targets"],
            )

    closeout = config["closeout_directory"]
    closeout_path, path_error = resolve_inside(
        root, closeout["path"], must_exist=False
    )
    if path_error:
        finding(
            findings,
            category="closeout",
            scope="work-pack",
            claim="closeout directory path is unsafe",
            evidence=[path_error],
            target_paths=config["refresh_targets"],
        )
    elif closeout_path is not None and closeout_path.exists() and not closeout_path.is_dir():
        finding(
            findings,
            category="closeout",
            scope="work-pack",
            claim="closeout path exists but is not a directory",
            evidence=[closeout["path"]],
            target_paths=config["refresh_targets"],
        )
    elif closeout_path is not None and not closeout_path.exists() and not closeout["create_if_missing"]:
        finding(
            findings,
            category="closeout",
            scope="work-pack",
            claim="closeout directory is absent and has no atomic creation contract",
            evidence=[closeout["path"]],
            target_paths=config["refresh_targets"],
        )


def runtime_checks(
    config: dict[str, Any],
    findings: list[dict[str, Any]],
    runtime_blockers: dict[str, list[str]],
) -> None:
    root = Path(config["_root"])
    request_schema = load_json(root / config["task_session_request_schema"]["path"])
    modes = set(
        request_schema.get("properties", {})
        .get("executionMode", {})
        .get("enum", [])
    )
    material_write_schema = (
        request_schema.get("properties", {}).get("materialWrites")
    )
    output_only_profile_supported = (
        isinstance(material_write_schema, dict)
        and material_write_schema.get("minItems", 0) == 0
    )
    for unit in config["units"]:
        unit_id = unit["unit_id"]
        mode = unit["requested_execution_mode"]
        if mode not in modes:
            blocker = finding(
                findings,
                category="runtime-admission",
                scope=unit_id,
                claim="requested execution mode is absent from the live Task Session schema",
                evidence=[f"mode={mode}", f"live modes={sorted(modes)}"],
                target_paths=[config["task_session_request_schema"]["path"]],
            )
            runtime_blockers[unit_id].append(blocker)
            continue
        task_class = unit["task_class"]
        material = unit["material_writes"]
        outputs = unit["execution_outputs"]
        package = unit.get("material_package")
        if mode in ("routed-mutation", "reusable-mutation"):
            if task_class == "material-mutation" and package is None:
                blocker = finding(
                    findings,
                    category="runtime-admission",
                    scope=unit_id,
                    claim="material mutation lacks current material-package admission evidence",
                    evidence=["material_package is null"],
                    target_paths=[unit["contract_ref"]["path"]],
                )
                runtime_blockers[unit_id].append(blocker)
            if (
                task_class in ("output-only", "audit-only")
                and not material
                and not output_only_profile_supported
            ):
                blocker = finding(
                    findings,
                    category="runtime-admission",
                    scope=unit_id,
                    claim="live routed mutation requires material writes for a non-material task",
                    evidence=[
                        f"task_class={task_class}",
                        f"execution_outputs={len(outputs)}",
                        "no placeholder material write may be invented",
                    ],
                    target_paths=[
                        unit["contract_ref"]["path"],
                        config["task_session_request_schema"]["path"],
                    ],
                )
                runtime_blockers[unit_id].append(blocker)
            if (
                task_class in ("output-only", "audit-only")
                and not material
                and not outputs
            ):
                blocker = finding(
                    findings,
                    category="runtime-admission",
                    scope=unit_id,
                    claim="non-material routed execution has no declared output partition",
                    evidence=[f"task_class={task_class}"],
                    target_paths=[
                        unit["contract_ref"]["path"],
                        config["task_session_request_schema"]["path"],
                    ],
                )
                runtime_blockers[unit_id].append(blocker)
        elif mode == "standalone-nonmutating" and (material or outputs):
            blocker = finding(
                findings,
                category="runtime-admission",
                scope=unit_id,
                claim="standalone-nonmutating mode cannot truthfully admit declared writes",
                evidence=[
                    f"material_writes={len(material)}",
                    f"execution_outputs={len(outputs)}",
                ],
                target_paths=[
                    unit["contract_ref"]["path"],
                    config["task_session_request_schema"]["path"],
                ],
            )
            runtime_blockers[unit_id].append(blocker)

        if unit["state"] == "complete":
            receipt_by_dep = {
                item["dependency_id"]: item for item in unit["dependency_receipts"]
            }
            for dependency in unit["dependencies"]:
                if dependency not in receipt_by_dep:
                    blocker = finding(
                        findings,
                        category="dependency-receipt",
                        scope=unit_id,
                        claim="completed unit lacks exact dependency receipt evidence",
                        evidence=[f"missing receipt for {dependency}"],
                        target_paths=[unit["contract_ref"]["path"]],
                    )
                    runtime_blockers[unit_id].append(blocker)
            for dependency, spec in receipt_by_dep.items():
                document = load_json(root / spec["receipt_ref"]["path"])
                mismatches = []
                expected = {
                    "unit_id": spec["expected_unit_id"],
                    "step_id": spec["expected_step_id"],
                    "status": spec["expected_status"],
                    "work_pack_sha256": spec["work_pack_sha256"],
                }
                for key, value in expected.items():
                    if document.get(key) != value:
                        mismatches.append(
                            f"{key}: expected {value!r}, got {document.get(key)!r}"
                        )
                if mismatches:
                    blocker = finding(
                        findings,
                        category="dependency-receipt",
                        scope=unit_id,
                        claim="dependency receipt semantics do not match the captured frontier",
                        evidence=[f"dependency={dependency}", *mismatches],
                        target_paths=[spec["receipt_ref"]["path"]],
                    )
                    runtime_blockers[unit_id].append(blocker)


def receipt_semantics_checks(
    config: dict[str, Any], findings: list[dict[str, Any]]
) -> str:
    root = Path(config["_root"])
    schema_path = config["terminal_receipt_schema"]["path"]
    schema = load_json(root / schema_path)
    properties = schema.get("properties", {})
    gaps: list[str] = []
    unit_id = properties.get("unit_id", {})
    if unit_id.get("type") != "string":
        gaps.append("unit_id is not explicitly type string")
    artifacts = properties.get("artifacts", {})
    validation = properties.get("validation", {})
    pass_properties: dict[str, Any] = {}
    for rule in schema.get("allOf", []):
        if not isinstance(rule, dict):
            continue
        status_rule = (
            rule.get("if", {})
            .get("properties", {})
            .get("status", {})
        )
        if status_rule.get("const") == "pass":
            pass_properties.update(
                rule.get("then", {}).get("properties", {})
            )
    pass_artifacts = pass_properties.get("artifacts", {})
    pass_validation = pass_properties.get("validation", {})
    pass_blockers = pass_properties.get("blockers", {})
    pass_validation_result = pass_properties.get("validation_result", {})
    if max(artifacts.get("minItems", 0), pass_artifacts.get("minItems", 0)) < 1:
        gaps.append("artifacts may be empty")
    if max(validation.get("minItems", 0), pass_validation.get("minItems", 0)) < 1:
        gaps.append("validation may be empty")
    artifact_item = artifacts.get("items", {})
    validation_item = validation.get("items", {})
    if artifact_item.get("additionalProperties") is not False:
        gaps.append("artifact entries allow unowned fields")
    if validation_item.get("additionalProperties") is not False:
        gaps.append("validation entries allow unowned fields")
    if (
        artifact_item.get("properties", {})
        .get("sha256", {})
        .get("type")
        != "string"
    ):
        gaps.append("artifact sha256 is not explicitly type string")

    if (
        pass_validation_result.get("const") != "pass"
        or pass_blockers.get("maxItems") != 0
    ):
        gaps.append("pass status is not conditionally bound to passing validation and no blockers")
    if not config.get("terminal_receipt_semantic_validator"):
        gaps.append("no semantic validator binds unit/step/work-pack/successor")

    if gaps:
        finding(
            findings,
            category="receipt-semantics",
            scope="terminal-receipt",
            claim="terminal receipt contract is fail-open",
            evidence=gaps,
            target_paths=[schema_path],
        )
        return STATUS_BLOCK
    return "pass"


def handoff_checks(
    config: dict[str, Any], findings: list[dict[str, Any]]
) -> None:
    root = Path(config["_root"])
    state = config.get("handoff_state")
    if state is None:
        finding(
            findings,
            category="handoff",
            scope="work-pack",
            claim="handoff state projection is missing from the audit frontier",
            evidence=["handoff_state is absent"],
            target_paths=config["refresh_targets"],
        )
        return
    artifact_path = state["artifact_ref"]["path"]
    document = load_json(root / artifact_path)
    mismatches = []
    for key, expected in state["expected_fields"].items():
        if document.get(key) != expected:
            mismatches.append(
                f"{key}: expected {expected!r}, got {document.get(key)!r}"
            )
    if mismatches:
        finding(
            findings,
            category="handoff",
            scope="work-pack",
            claim="handoff state contradicts the captured work-pack route",
            evidence=mismatches,
            target_paths=[artifact_path],
        )


def inherit_blockers(
    config: dict[str, Any],
    unit_blockers: dict[str, list[str]],
    runtime_blockers: dict[str, list[str]],
) -> None:
    by_id = {unit["unit_id"]: unit for unit in config["units"]}
    changed = True
    while changed:
        changed = False
        for unit in config["units"]:
            unit_id = unit["unit_id"]
            inherited_plan = {
                blocker
                for dependency in unit["dependencies"]
                if dependency in by_id
                for blocker in unit_blockers[dependency]
            }
            inherited_runtime = {
                blocker
                for dependency in unit["dependencies"]
                if dependency in by_id
                for blocker in runtime_blockers[dependency]
            }
            for target, inherited in (
                (unit_blockers[unit_id], inherited_plan),
                (runtime_blockers[unit_id], inherited_runtime),
            ):
                before = len(target)
                target.extend(sorted(inherited - set(target)))
                changed = changed or len(target) != before


def render_markdown(report: dict[str, Any]) -> str:
    categories = Counter(item["category"] for item in report["findings"])
    lines = [
        "# Work Pack Readiness Audit",
        "",
        f"- Canonical ID: `{report['canonical_spell_id']}`",
        f"- Verdict: `{report['verdict']}`",
        f"- Snapshot: `{report['snapshot']['digest']}`; drift `{str(report['snapshot']['drift']).lower()}`",
        f"- Plan contract: `{report['plan_contract_status']}`",
        f"- Runtime admission: `{report['runtime_admission_status']}`",
        f"- Receipt semantics: `{report['receipt_semantics_status']}`",
        f"- Ready frontier: `{', '.join(report['ready_frontier']) or 'none'}`",
        "- Selected unit: `none`",
        "- Authority effect: `none`",
        "- Mutation ready: `false`",
        "- Next owner: `invoke:refresh`",
        "",
        "## Finding Counts",
        "",
    ]
    if categories:
        for category, count in sorted(categories.items()):
            lines.append(f"- `{category}`: {count}")
    else:
        lines.append("- none")
    lines.extend(["", "## Unit Results", "", "| Unit | Plan | Runtime | Blockers |", "| --- | --- | --- | --- |"])
    for unit in report["unit_results"]:
        lines.append(
            f"| `{unit['unit_id']}` | `{unit['plan_contract']}` | "
            f"`{unit['runtime_admission']}` | "
            f"{', '.join(unit['blocker_ids']) or 'none'} |"
        )
    lines.extend(["", "## Findings", ""])
    if not report["findings"]:
        lines.append("No findings.")
    for item in report["findings"]:
        lines.extend(
            [
                f"### {item['id']} — {item['claim']}",
                "",
                f"- Category: `{item['category']}`",
                f"- Scope: `{item['scope']}`",
                f"- Evidence: {'; '.join(item['evidence'])}",
                f"- Targets: {', '.join(f'`{path}`' for path in item['target_paths'])}",
                "",
            ]
        )
    lines.extend(
        [
            "## Claim Ceiling",
            "",
            "This report is an audit-only preflight. It selects and executes no unit, "
            "authorizes no mutation, and applies no refresh.",
            "",
        ]
    )
    return "\n".join(lines)


def audit(config: dict[str, Any], repository_root: Path) -> dict[str, Any]:
    config = dict(config)
    config["_root"] = str(repository_root.resolve())
    findings: list[dict[str, Any]] = []
    unit_blockers: dict[str, list[str]] = defaultdict(list)
    runtime_blockers: dict[str, list[str]] = defaultdict(list)

    references = gather_exact_refs(config)
    initial_snapshot, snapshot_errors = capture_snapshot(repository_root, references)
    for error in snapshot_errors:
        finding(
            findings,
            category="snapshot",
            scope="work-pack",
            claim="exact artifact snapshot failed",
            evidence=[error],
            target_paths=config["refresh_targets"],
        )

    ready = graph_checks(config, findings, unit_blockers)
    command_and_write_checks(config, findings, unit_blockers)
    runtime_checks(config, findings, runtime_blockers)
    receipt_status = receipt_semantics_checks(config, findings)
    handoff_checks(config, findings)

    if config["publication_class"] == "public" and config["authority_class"] != "public":
        finding(
            findings,
            category="authority",
            scope="work-pack",
            claim="private authority cannot feed a public audit artifact",
            evidence=[
                f"authority_class={config['authority_class']}",
                f"publication_class={config['publication_class']}",
            ],
            target_paths=config["refresh_targets"],
        )

    inherit_blockers(config, unit_blockers, runtime_blockers)

    final_snapshot, drift_errors = capture_snapshot(repository_root, references)
    drift = initial_snapshot != final_snapshot or bool(drift_errors)
    if drift:
        finding(
            findings,
            category="snapshot",
            scope="work-pack",
            claim="captured frontier changed during the audit",
            evidence=drift_errors or ["start and end snapshots differ"],
            target_paths=config["refresh_targets"],
        )

    plan_categories = {
        "snapshot",
        "graph",
        "command",
        "path",
        "write-algebra",
        "attempt",
        "closeout",
        "handoff",
        "authority",
    }
    plan_block = bool(snapshot_errors or drift) or any(
        item["severity"] == "blocker" and item["category"] in plan_categories
        for item in findings
    )
    runtime_block = any(runtime_blockers.values())
    plan_status = STATUS_BLOCK if plan_block else "pass"
    runtime_status = STATUS_BLOCK if runtime_block else "pass"
    verdict = (
        STATUS_BLOCK
        if STATUS_BLOCK in (plan_status, runtime_status, receipt_status)
        else "pass"
    )
    unit_results = []
    for unit in config["units"]:
        unit_id = unit["unit_id"]
        blockers = sorted(set(unit_blockers[unit_id] + runtime_blockers[unit_id]))
        unit_results.append(
            {
                "unit_id": unit_id,
                "plan_contract": STATUS_BLOCK if unit_blockers[unit_id] else "pass",
                "runtime_admission": STATUS_BLOCK
                if runtime_blockers[unit_id]
                else "pass",
                "blocker_ids": blockers,
            }
        )
    report = {
        "schema_version": "1.0.0",
        "audit_id": config["audit_id"],
        "canonical_spell_id": "work-pack-readiness-audit",
        "verdict": verdict,
        "plan_contract_status": plan_status,
        "runtime_admission_status": runtime_status,
        "receipt_semantics_status": receipt_status,
        "snapshot": {
            "digest": snapshot_digest(initial_snapshot),
            "artifact_count": len(initial_snapshot),
            "drift": drift,
        },
        "unit_counts": dict(sorted(Counter(unit["task_class"] for unit in config["units"]).items())),
        "ready_frontier": ready,
        "selected_unit": None,
        "findings": findings,
        "unit_results": unit_results,
        "authority_effect": "none",
        "mutation_ready": False,
        "next_owner": "invoke:refresh",
    }
    return report


def write_outputs(report: dict[str, Any], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    expected_paths = [
        output_dir / "work-pack-readiness-report.json",
        output_dir / "WORK-PACK-READINESS-REPORT.md",
        output_dir / "REFRESH-SIGNAL-PACK.json",
    ]
    existing = [str(path) for path in expected_paths if path.exists()]
    if existing:
        raise ValueError(f"refusing to overwrite audit outputs: {', '.join(existing)}")

    report_errors = schema_errors(report, load_json(REPORT_SCHEMA), "audit report")
    if report_errors:
        raise ValueError("; ".join(report_errors))
    report_bytes = json.dumps(report, indent=2, sort_keys=True).encode("utf-8") + b"\n"
    expected_paths[0].write_bytes(report_bytes)
    expected_paths[1].write_text(render_markdown(report), encoding="utf-8")

    signals = []
    for item in report["findings"]:
        signals.append(
            {
                "id": f"{report['audit_id']}:{item['id']}",
                "signal_type": "artifact_drift"
                if item["category"] == "snapshot"
                else "blocker_opened",
                "claim": item["claim"],
                "evidence": item["evidence"],
                "target_artifacts": item["target_paths"],
                "confidence": "high",
                "mutation_safety": "needs_review",
            }
        )
    if not signals:
        signals.append(
            {
                "id": f"{report['audit_id']}:no-op",
                "signal_type": "no_op",
                "claim": "captured work pack requires no refresh repair",
                "evidence": [f"audit verdict={report['verdict']}"],
                "target_artifacts": ["work-pack-readiness-report.json"],
                "confidence": "high",
                "mutation_safety": "safe",
            }
        )
    targets = sorted(
        {
            path
            for signal in signals
            for path in signal["target_artifacts"]
        }
    )
    signal_pack = {
        "schema_version": "1.0.0",
        "audit_id": report["audit_id"],
        "source_report": {
            "path": "work-pack-readiness-report.json",
            "sha256": digest_bytes(report_bytes),
            "size_bytes": len(report_bytes),
        },
        "mutation_mode": "proposal-only",
        "mutation_ready": False,
        "authority_effect": "none",
        "signals": signals,
        "target_inventory": targets,
        "next_owner": "invoke:refresh",
    }
    signal_errors = schema_errors(
        signal_pack, load_json(SIGNAL_SCHEMA), "refresh signal pack"
    )
    if signal_errors:
        raise ValueError("; ".join(signal_errors))
    expected_paths[2].write_text(
        json.dumps(signal_pack, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _walk_exact_refs(value: Any) -> list[dict[str, Any]]:
    """Collect v2 exact refs without assigning authority to their container."""

    refs: list[dict[str, Any]] = []
    if isinstance(value, dict):
        if set(value) == {"path", "sha256", "size_bytes"}:
            refs.append(value)
        else:
            for child in value.values():
                refs.extend(_walk_exact_refs(child))
    elif isinstance(value, list):
        for child in value:
            refs.extend(_walk_exact_refs(child))
    return refs


def _unique_exact_refs(config: dict[str, Any]) -> tuple[list[dict[str, Any]], list[str]]:
    unique: dict[str, dict[str, Any]] = {}
    errors: list[str] = []
    for reference in _walk_exact_refs(config):
        previous = unique.get(reference["path"])
        if previous is not None and previous != reference:
            errors.append(f"conflicting exact references: {reference['path']}")
        unique[reference["path"]] = reference
    return [unique[path] for path in sorted(unique)], errors


def _resolve_json_pointer(document: Any, pointer: str) -> Any:
    if pointer == "":
        return document
    if not pointer.startswith("/"):
        raise ValueError(f"JSON Pointer must start with '/': {pointer}")
    current = document
    for raw_token in pointer[1:].split("/"):
        token = raw_token.replace("~1", "/").replace("~0", "~")
        if isinstance(current, list):
            try:
                current = current[int(token)]
            except (ValueError, IndexError) as error:
                raise ValueError(f"unresolved JSON Pointer: {pointer}") from error
        elif isinstance(current, dict) and token in current:
            current = current[token]
        else:
            raise ValueError(f"unresolved JSON Pointer: {pointer}")
    return current


def _binding_semantics(binding: dict[str, Any] | None) -> Any:
    if binding is None:
        return None
    return {
        "binding_id": binding["binding_id"],
        "owner_ref": binding["owner_ref"],
        "artifact_sha256": binding["artifact_ref"]["sha256"],
        "selector": binding["selector"],
    }


def _v2_blocker(code: str, binding_id: str, claim: str) -> dict[str, str]:
    return {"code": code, "binding_id": binding_id, "claim": claim}


def _v2_preflight_blockers(config: dict[str, Any]) -> list[dict[str, str]]:
    blockers: list[dict[str, str]] = []
    plan_once = config.get("admission_timing") == "selected-unit-at-task-session"
    unit_ids = {unit["unit_id"] for unit in config["execution_bindings"]}
    expected_material = config.get("expected_material_digests", {})

    for unit in config["execution_bindings"]:
        unit_id = unit["unit_id"]
        package = unit["material_package"]
        strict_material_checks = (
            (
                package["package_ref"] is None,
                "MATERIAL_PACKAGE_REF_MISSING",
                f"{unit_id}:material-package",
                "material package reference is absent",
            ),
            (
                package["producer_owner_ref"] is None,
                "MATERIAL_PRODUCER_OWNER_UNRESOLVED",
                f"{unit_id}:producer-owner",
                "material producer owner is absent or unresolved",
            ),
            (
                package["producer_receipt_ref"] is None,
                "MATERIAL_PRODUCER_RECEIPT_MISSING",
                f"{unit_id}:producer-receipt",
                "material producer receipt is absent",
            ),
            (
                package["schema_ref"] is None,
                "MATERIAL_RECEIPT_SCHEMA_MISSING",
                f"{unit_id}:material-schema",
                "material receipt schema binding is absent",
            ),
            (
                package["target_inventory_ref"] is None,
                "TARGET_INVENTORY_MISSING",
                f"{unit_id}:target-inventory",
                "target inventory binding is absent",
            ),
            (
                not unit["byte_baselines"],
                "EXECUTION_BYTE_BASELINE_MISSING",
                f"{unit_id}:byte-baselines",
                "execution byte baseline set is empty",
            ),
        )
        owner_checks = (
            (
                package["producer_owner_ref"] is None,
                "MATERIAL_PRODUCER_OWNER_UNRESOLVED",
                f"{unit_id}:producer-owner",
                "material producer owner is absent or unresolved",
            ),
        )
        checks = owner_checks if plan_once else strict_material_checks
        for failed, code, binding_id, claim in checks:
            if failed:
                blockers.append(_v2_blocker(code, binding_id, claim))

        material = set(unit["material_writes"])
        outputs = set(unit["execution_outputs"])
        allowed = set(unit["allowed_writes"])
        if material & outputs or material | outputs != allowed:
            blockers.append(
                _v2_blocker(
                    "WRITE_PARTITION_INVALID",
                    f"{unit_id}:allowed-writes",
                    "material and execution writes are not an exact disjoint partition",
                )
            )
        if len(unit["canonical_successors"]) != 1:
            blockers.append(
                _v2_blocker(
                    "CANONICAL_SUCCESSOR_NON_UNIQUE",
                    f"{unit_id}:canonical-successor",
                    "unit must bind exactly one canonical successor, including a terminal sentinel",
                )
            )
        for dependency in unit["dependencies"]:
            if dependency not in unit_ids:
                blockers.append(
                    _v2_blocker(
                        "DEPENDENCY_OUTSIDE_FRONTIER",
                        f"{unit_id}:dependencies",
                        f"dependency is outside the finite frontier: {dependency}",
                    )
                )
        expected_digest = expected_material.get(unit_id)
        if (
            not plan_once
            and
            expected_digest is not None
            and package["declared_sha256"] != expected_digest
        ):
            blockers.append(
                _v2_blocker(
                    "PREROUTE_MATERIAL_DIGEST_MISMATCH",
                    f"{unit_id}:material-digest",
                    "declared material digest differs from the frozen expected digest",
                )
            )

    closeout_by_unit = {
        item["unit_id"]: item for item in config["closeout_bindings"]
    }
    for unit_id in sorted(unit_ids):
        closeout = closeout_by_unit.get(unit_id)
        if closeout is None or closeout["owner_receipt_contract_ref"] is None:
            blockers.append(
                _v2_blocker(
                    "CLOSEOUT_RECEIPT_CONTRACT_MISSING",
                    f"{unit_id}:closeout",
                    "closeout owner receipt contract is absent",
                )
            )
            continue
        if closeout["allowed_delta_policy_ref"] is None:
            blockers.append(
                _v2_blocker(
                    "ALLOWED_DELTA_POLICY_MISSING",
                    f"{unit_id}:delta-policy",
                    "allowed-delta policy binding is absent",
                )
            )

    if config["receipt_bindings"]["terminal_schema_ref"] is None:
        blockers.append(
            _v2_blocker(
                "TERMINAL_RECEIPT_SCHEMA_MISSING",
                "terminal-receipt-schema",
                "terminal receipt schema is absent",
            )
        )
    if config["receipt_bindings"]["semantic_validator_ref"] is None:
        blockers.append(
            _v2_blocker(
                "TERMINAL_RECEIPT_VALIDATOR_MISSING",
                "terminal-receipt-validator",
                "terminal receipt semantic validator is absent",
            )
        )
    if not plan_once and config["runtime_binding"][
        "task_session_admission_receipt_ref"
    ] is None:
        blockers.append(
            _v2_blocker(
                "TASK_SESSION_ADMISSION_RECEIPT_MISSING",
                "runtime-admission",
                "strict full-frontier mode requires a current Task Session admission receipt",
            )
        )
    return blockers


def _plan_once_semantic_repair_entry(
    config: dict[str, Any],
    plan_semantics: dict[str, Any] | None,
    blockers: list[dict[str, str]],
) -> dict[str, Any] | None:
    """Compile one exact declared Refresh entry for repairable semantic drift."""

    codes = {item["code"] for item in blockers}
    if "EPOCH_INVALIDATED_SEMANTIC_CHANGE" not in codes:
        return None
    if codes != {"EPOCH_INVALIDATED_SEMANTIC_CHANGE"} or plan_semantics is None:
        return None
    frontier = plan_semantics.get("ready_frontier") or [
        item["unit_id"] for item in config["execution_bindings"]
    ]
    if not frontier:
        blockers.append(
            _v2_blocker(
                "SEMANTIC_REFRESH_UNIT_MISSING",
                "execution-entry",
                "semantic repair has no deterministic frontier unit",
            )
        )
        return None
    selected_unit = frontier[0]
    routes = [
        route
        for route in config["execution_policy"]["allowed_routes"]
        if route["frontier_swu"] == selected_unit
        and route["capability"] == "invoke"
        and route["mode"] == "refresh"
    ]
    if len(routes) != 1:
        blockers.append(
            _v2_blocker(
                "SEMANTIC_REFRESH_ROUTE_NOT_UNIQUE",
                "execution-entry",
                f"expected one declared Invoke Refresh route for {selected_unit}, got {len(routes)}",
            )
        )
        return None
    route = routes[0]
    return {
        "entry_state": "owner-prerequisite",
        "selected_unit": selected_unit,
        "route_id": route["route_id"],
        "next_owner": {
            "capability": route["capability"],
            "mode": route["mode"],
            "target": route["target"],
        },
        "blocker_code": None,
    }


def _v2_binding_blockers(
    config: dict[str, Any], repository_root: Path
) -> list[dict[str, str]]:
    blockers: list[dict[str, str]] = []

    def visit(value: Any) -> None:
        if isinstance(value, dict):
            if {"binding_id", "owner_ref", "artifact_ref", "selector"} <= set(value):
                selector = value["selector"]
                if selector:
                    path = repository_root / value["artifact_ref"]["path"]
                    try:
                        document = load_json(path)
                        _resolve_json_pointer(document, selector)
                    except (OSError, ValueError, json.JSONDecodeError) as error:
                        blockers.append(
                            _v2_blocker(
                                "BINDING_SELECTOR_UNRESOLVED",
                                value["binding_id"],
                                str(error),
                            )
                        )
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)

    visit(config)
    return blockers


def _binding_selected_value(
    binding: dict[str, Any], repository_root: Path
) -> Any:
    path = repository_root / binding["artifact_ref"]["path"]
    return _resolve_json_pointer(load_json(path), binding["selector"])


def _completion_continuity_projection(
    config: dict[str, Any],
    repository_root: Path,
    *,
    canonical_semantic_digest: str,
    plan_epoch_id: str,
    unit_contract_digests: dict[str, str],
    source_snapshot_digest: str,
) -> tuple[dict[str, Any] | None, list[dict[str, str]]]:
    """Validate and project one immutable historical completion prefix."""

    continuity = config.get("continuity_projection")
    if not isinstance(continuity, dict):
        return None, [
            _v2_blocker(
                "CONTINUITY_PROJECTION_MISSING",
                "continuity-projection",
                "plan-once execution requires an explicit continuity projection",
            )
        ]

    blockers: list[dict[str, str]] = []
    units = config["execution_bindings"]
    frontier = [unit["unit_id"] for unit in units]
    completed_refs = continuity["completed_unit_receipt_refs"]
    closeout_refs = continuity["joined_closeout_receipt_refs"]
    projected = continuity["projected_next_successor"]

    if len(completed_refs) != len(closeout_refs):
        blockers.append(
            _v2_blocker(
                "CONTINUITY_RECEIPT_MISSING",
                "continuity-projection",
                "completed and joined-closeout receipt counts differ",
            )
        )
    if len(completed_refs) > len(frontier):
        blockers.append(
            _v2_blocker(
                "CONTINUITY_FRONTIER_MISMATCH",
                "continuity-projection",
                "completed receipt count exceeds the captured frontier",
            )
        )

    completed_prefix: list[dict[str, Any]] = []
    seen_receipts: set[tuple[str, str, int]] = set()
    pair_count = min(len(completed_refs), len(closeout_refs), len(units))
    for index in range(pair_count):
        unit = units[index]
        completion = completed_refs[index]
        closeout = closeout_refs[index]
        completion_ref = completion["artifact_ref"]
        closeout_ref = closeout["artifact_ref"]
        unit_id = unit["unit_id"]

        if completion["selector"] != "/result":
            blockers.append(
                _v2_blocker(
                    "CONTINUITY_RECEIPT_MISSING",
                    completion["binding_id"],
                    f"{unit_id} completion selector must be /result",
                )
            )
            continue
        if closeout["selector"] != "/lifecycle_owner_validation/status":
            blockers.append(
                _v2_blocker(
                    "CONTINUITY_RECEIPT_MISSING",
                    closeout["binding_id"],
                    f"{unit_id} closeout selector must be /lifecycle_owner_validation/status",
                )
            )
            continue

        if completion_ref != closeout_ref:
            blockers.append(
                _v2_blocker(
                    "CONTINUITY_RECEIPT_MISSING",
                    completion["binding_id"],
                    f"{unit_id} completion and closeout do not bind the same receipt bytes",
                )
            )
            continue
        receipt_identity = exact_ref_key(completion_ref)
        if receipt_identity in seen_receipts:
            blockers.append(
                _v2_blocker(
                    "CONTINUITY_RECEIPT_REPLAY",
                    completion["binding_id"],
                    f"{unit_id} reuses a completion receipt",
                )
            )
            continue
        seen_receipts.add(receipt_identity)
        if completion_ref["path"] not in unit["execution_outputs"]:
            blockers.append(
                _v2_blocker(
                    "CONTINUITY_NON_PREFIX_COMPLETION",
                    completion["binding_id"],
                    f"{unit_id} completion receipt is not a declared unit output",
                )
            )
            continue

        try:
            receipt = load_json(repository_root / completion_ref["path"])
            completion_value = _resolve_json_pointer(
                receipt, completion["selector"]
            )
            closeout_value = _resolve_json_pointer(receipt, closeout["selector"])
        except (OSError, ValueError, json.JSONDecodeError) as error:
            blockers.append(
                _v2_blocker(
                    "CONTINUITY_RECEIPT_MISSING",
                    completion["binding_id"],
                    str(error),
                )
            )
            continue
        if receipt.get("swu_id") != unit.get("swu_id", unit_id):
            blockers.append(
                _v2_blocker(
                    "CONTINUITY_NON_PREFIX_COMPLETION",
                    completion["binding_id"],
                    f"expected {unit_id}, receipt names {receipt.get('swu_id')}",
                )
            )
            continue
        if unit.get("task_id") is not None and receipt.get("task_id") != unit["task_id"]:
            blockers.append(
                _v2_blocker(
                    "CONTINUITY_NON_PREFIX_COMPLETION",
                    completion["binding_id"],
                    f"{unit_id} receipt task identity differs from the unit contract",
                )
            )
            continue
        if completion_value != "pass" or closeout_value != "pass":
            blockers.append(
                _v2_blocker(
                    "CONTINUITY_RECEIPT_MISSING",
                    completion["binding_id"],
                    f"{unit_id} completion and closeout selectors must both resolve pass",
                )
            )
            continue
        completed_prefix.append(
            {
                "unit_id": unit_id,
                "unit_contract_digest": unit_contract_digests[unit_id],
                "completion_binding_id": completion["binding_id"],
                "completion_artifact_ref": completion_ref,
                "closeout_binding_id": closeout["binding_id"],
            }
        )

    prefix_length = len(completed_refs)
    next_unit = frontier[prefix_length] if prefix_length < len(frontier) else None
    expected_cursor = next_unit if next_unit is not None else "__complete__"
    if continuity["cursor"] != expected_cursor:
        blockers.append(
            _v2_blocker(
                "CONTINUITY_CURSOR_CONTRADICTION",
                "continuity-projection",
                f"expected cursor {expected_cursor}, got {continuity['cursor']}",
            )
        )
    if projected["unit_id"] != next_unit:
        blockers.append(
            _v2_blocker(
                "CONTINUITY_FRONTIER_MISMATCH",
                "continuity-projection",
                f"expected projected next unit {next_unit}, got {projected['unit_id']}",
            )
        )
    if next_unit is None:
        blockers.append(
            _v2_blocker(
                "CONTINUITY_CURSOR_CONTRADICTION",
                "continuity-projection",
                "the current plan-once selection handoff cannot represent an already complete frontier",
            )
        )

    successor_bindings = [
        projected["canonical_successor_ref"],
        projected["continuation_router_verification_receipt_ref"],
    ]
    for binding in successor_bindings:
        if binding is None:
            if next_unit is not None:
                blockers.append(
                    _v2_blocker(
                        "CONTINUITY_RECEIPT_MISSING",
                        "continuity-projection",
                        "a non-terminal frontier requires a canonical successor binding",
                    )
                )
            continue
        try:
            selected = _binding_selected_value(binding, repository_root)
        except (OSError, ValueError, json.JSONDecodeError) as error:
            blockers.append(
                _v2_blocker(
                    "CONTINUITY_RECEIPT_MISSING", binding["binding_id"], str(error)
                )
            )
            continue
        if selected != next_unit:
            blockers.append(
                _v2_blocker(
                    "CONTINUITY_FRONTIER_MISMATCH",
                    binding["binding_id"],
                    f"expected successor {next_unit}, got {selected}",
                )
            )

    if blockers:
        return None, blockers

    source_projection = {
        "cursor": continuity["cursor"],
        "completed_unit_receipt_refs": completed_refs,
        "joined_closeout_receipt_refs": closeout_refs,
        "projected_next_successor": projected,
        "source_snapshot_digest": source_snapshot_digest,
    }
    payload = {
        "source_audit_id": config["audit_id"],
        "source_projection_digest": digest_bytes(canonical_bytes(source_projection)),
        "work_pack_semantic_digest": canonical_semantic_digest,
        "plan_epoch_id": plan_epoch_id,
        "completed_prefix": completed_prefix,
        "next_unit": next_unit,
        "authority_effect": "none",
    }
    return {
        **payload,
        "continuity_digest": digest_bytes(canonical_bytes(payload)),
    }, []


def _v2_semantic_components(config: dict[str, Any]) -> dict[str, Any]:
    semantic = config["authority_bindings"]["semantic_bindings"]
    execution = config["execution_bindings"]
    return {
        "objective": _binding_semantics(config["objective_ref"]),
        "owner": {
            "semantic": _binding_semantics(semantic["owner"]),
            "material_producers": [
                {
                    "unit_id": unit["unit_id"],
                    "producer_owner_ref": unit["material_package"][
                        "producer_owner_ref"
                    ],
                }
                for unit in execution
            ],
            "approval_owner_ref": config["approval_policy"]["approval_owner_ref"],
        },
        "graph": [
            {
                "unit_id": unit["unit_id"],
                "dependencies": unit["dependencies"],
                "canonical_successors": unit["canonical_successors"],
            }
            for unit in execution
        ],
        "material": {
            "semantic": _binding_semantics(semantic["material"]),
            "units": [
                {
                    "unit_id": unit["unit_id"],
                    "material_writes": unit["material_writes"],
                    "execution_outputs": unit["execution_outputs"],
                    "allowed_writes": unit["allowed_writes"],
                    "package": {
                        "package_ref": _binding_semantics(
                            unit["material_package"]["package_ref"]
                        ),
                        "producer_receipt_ref": _binding_semantics(
                            unit["material_package"]["producer_receipt_ref"]
                        ),
                        "schema_ref": _binding_semantics(
                            unit["material_package"]["schema_ref"]
                        ),
                        "declared_sha256": unit["material_package"][
                            "declared_sha256"
                        ],
                        "target_inventory_ref": _binding_semantics(
                            unit["material_package"]["target_inventory_ref"]
                        ),
                    },
                    "byte_baselines": unit["byte_baselines"],
                }
                for unit in execution
            ],
        },
        "validation": {
            "semantic": _binding_semantics(semantic["validation"]),
            "commands": [
                {"unit_id": unit["unit_id"], "command": unit["command"]}
                for unit in execution
            ],
        },
        "receipt": {
            "semantic": _binding_semantics(semantic["receipt"]),
            "bindings": config["receipt_bindings"],
        },
        "closeout": {
            "semantic": _binding_semantics(semantic["closeout"]),
            "bindings": config["closeout_bindings"],
        },
        "runtime": config["runtime_binding"],
        "frontier": [unit["unit_id"] for unit in execution],
        "risk_budget": {
            "risk_policy_ref": _binding_semantics(
                config["approval_policy"]["risk_policy_ref"]
            ),
            "run_budget": config["approval_policy"]["run_budget"],
            "allowed_audit_verdicts": config["approval_policy"][
                "allowed_audit_verdicts"
            ],
            "allowed_flag_classes": config["approval_policy"][
                "allowed_flag_classes"
            ],
        },
    }


def compare_manifests_v2(
    prior_manifest: dict[str, Any], current_manifest: dict[str, Any]
) -> str:
    """Classify whether a regenerated projection preserves an approved epoch."""

    prior = prior_manifest["semantic_component_digests"]
    current = current_manifest["semantic_component_digests"]
    if prior == current:
        return "PROJECTION_EQUIVALENCE_PRESERVED"
    code_by_component = {
        "owner": "EPOCH_INVALIDATED_OWNER_CHANGE",
        "material": "EPOCH_INVALIDATED_MATERIAL_CHANGE",
        "validation": "EPOCH_INVALIDATED_VALIDATION_CHANGE",
        "receipt": "EPOCH_INVALIDATED_RECEIPT_CHANGE",
        "closeout": "EPOCH_INVALIDATED_CLOSEOUT_CHANGE",
    }
    changed = sorted(
        name for name in set(prior) | set(current) if prior.get(name) != current.get(name)
    )
    if len(changed) == 1 and changed[0] in code_by_component:
        return code_by_component[changed[0]]
    return "EPOCH_INVALIDATED_SEMANTIC_CHANGE"


def audit_v2(config: dict[str, Any], repository_root: Path) -> dict[str, Any]:
    """Build a deterministic, no-authority projection or one stable block report."""

    plan_once = config.get("admission_timing") == "selected-unit-at-task-session"
    refs, ref_conflicts = _unique_exact_refs(config)
    initial_snapshot, snapshot_errors = capture_snapshot(repository_root, refs)
    blockers = [
        _v2_blocker("EXACT_REFERENCE_CONFLICT", "snapshot", error)
        for error in ref_conflicts
    ]
    blockers.extend(
        _v2_blocker("FROZEN_INPUT_MISMATCH", "snapshot", error)
        for error in snapshot_errors
    )
    blockers.extend(_v2_preflight_blockers(config))
    blockers.extend(_v2_binding_blockers(config, repository_root))

    source_digest = snapshot_digest(initial_snapshot)
    expected_source = config.get("expected_source_snapshot_digest")
    if expected_source is not None and expected_source != source_digest:
        blockers.append(
            _v2_blocker(
                "SOURCE_SNAPSHOT_DIGEST_MISMATCH",
                "snapshot",
                "captured source snapshot differs from the expected digest",
            )
        )

    plan_semantics: dict[str, Any] | None = None
    try:
        if plan_once:
            plan_semantics = build_plan_semantics(config, repository_root)
            component_digests = plan_semantics["semantic_component_digests"]
            semantic_digest = plan_semantics["canonical_semantic_digest"]
        else:
            component_payloads = _v2_semantic_components(config)
            component_digests = {
                name: digest_bytes(canonical_bytes(payload))
                for name, payload in sorted(component_payloads.items())
            }
            semantic_digest = digest_bytes(canonical_bytes(component_digests))
    except PlanSemanticError as error:
        blockers.append(
            _v2_blocker(
                "PLAN_SEMANTIC_NORMALIZATION_FAILED",
                "plan-semantics",
                str(error),
            )
        )
        component_digests = {}
        semantic_digest = None
    expected_semantic = config.get("expected_semantic_digest")
    if (
        expected_semantic is not None
        and semantic_digest is not None
        and expected_semantic != semantic_digest
    ):
        blockers.append(
            _v2_blocker(
                "EPOCH_INVALIDATED_SEMANTIC_CHANGE",
                "canonical-semantic-digest",
                "canonical semantic digest differs from the expected epoch",
            )
        )

    final_snapshot, drift_errors = capture_snapshot(repository_root, refs)
    drift = initial_snapshot != final_snapshot or bool(drift_errors)
    if drift:
        blockers.append(
            _v2_blocker(
                "SNAPSHOT_DRIFT",
                "snapshot",
                "; ".join(drift_errors) or "start and end snapshots differ",
            )
        )

    manifest: dict[str, Any] | None = None
    projection_digest: str | None = None
    if not blockers and semantic_digest is not None:
        finite_frontier = [unit["unit_id"] for unit in config["execution_bindings"]]
        if plan_once:
            assert plan_semantics is not None
            epoch_seed = digest_bytes(
                canonical_bytes(
                    {
                        "normalizer_version": NORMALIZER_VERSION,
                        "canonical_semantic_digest": semantic_digest,
                        "unit_contract_digests": plan_semantics[
                            "unit_contract_digests"
                        ],
                    }
                )
            )
            plan_epoch_id = f"epoch-{epoch_seed[:24]}"
            completion_continuity, continuity_blockers = (
                _completion_continuity_projection(
                    config,
                    repository_root,
                    canonical_semantic_digest=semantic_digest,
                    plan_epoch_id=plan_epoch_id,
                    unit_contract_digests=plan_semantics[
                        "unit_contract_digests"
                    ],
                    source_snapshot_digest=source_digest,
                )
            )
            blockers.extend(continuity_blockers)
            post_continuity_snapshot, post_continuity_errors = capture_snapshot(
                repository_root, refs
            )
            if (
                post_continuity_snapshot != initial_snapshot
                or post_continuity_errors
            ):
                drift = True
                if not any(item["code"] == "SNAPSHOT_DRIFT" for item in blockers):
                    blockers.append(
                        _v2_blocker(
                            "SNAPSHOT_DRIFT",
                            "snapshot",
                            "; ".join(post_continuity_errors)
                            or "continuity inputs changed during projection",
                        )
                    )
            if not blockers:
                assert completion_continuity is not None
                manifest_payload = {
                    "schema_version": "1.0.0",
                    "audit_id": config["audit_id"],
                    "work_pack_id": config["execution_policy"]["work_pack_id"],
                    "normalizer_version": NORMALIZER_VERSION,
                    "admission_timing": "selected-unit-at-task-session",
                    "plan_epoch_id": plan_epoch_id,
                    "canonical_semantic_digest": semantic_digest,
                    "semantic_component_digests": component_digests,
                    "unit_contract_digests": plan_semantics[
                        "unit_contract_digests"
                    ],
                    "ready_frontier": plan_semantics["ready_frontier"],
                    "source_snapshot_digest": source_digest,
                    "completion_continuity": completion_continuity,
                    "selection_required": True,
                    "runtime_admission_status": "pending-selection",
                    "allowed_routes": config["execution_policy"]["allowed_routes"],
                    "allowed_routes_digest": config["execution_policy"][
                        "allowed_routes_digest"
                    ],
                    "execution_entry": {
                        "entry_state": "selection-ready",
                        "selected_unit": None,
                        "route_id": None,
                        "next_owner": {
                            "capability": "implementation-readiness",
                            "mode": "execute",
                            "target": config["execution_policy"]["work_pack_id"],
                        },
                        "blocker_code": None,
                    },
                    "authority_effect": "none",
                    "selected_unit": None,
                    "mutation_ready": False,
                }
                projection_digest = digest_bytes(canonical_bytes(manifest_payload))
                manifest = {
                    **manifest_payload,
                    "manifest_id": f"psm-{projection_digest[:24]}",
                }
                manifest_errors = schema_errors(
                    manifest, load_json(PLAN_MANIFEST_SCHEMA), "plan semantic manifest"
                )
                if manifest_errors:
                    blockers.extend(
                        _v2_blocker("MANIFEST_SCHEMA_INVALID", "manifest", error)
                        for error in manifest_errors
                    )
                    manifest = None
                    projection_digest = None
        else:
            projection_payload = {
                "evidence_ceiling": config["evidence_ceiling"],
                "classifier_version": config["classifier_version"],
                "objective_ref": config["objective_ref"],
                "closure_receipt_refs": config["closure_receipt_refs"],
                "authority_bindings": config["authority_bindings"],
                "execution_bindings": config["execution_bindings"],
                "receipt_bindings": config["receipt_bindings"],
                "closeout_bindings": config["closeout_bindings"],
                "runtime_binding": config["runtime_binding"],
                "status_receipt_refs": config["status_receipt_refs"],
                "lifecycle_status_refs": config["lifecycle_status_refs"],
                "approval_policy": config["approval_policy"],
                "continuity_projection": config["continuity_projection"],
                "source_snapshot_digest": source_digest,
                "canonical_semantic_digest": semantic_digest,
                "semantic_component_digests": component_digests,
            }
            projection_digest = digest_bytes(canonical_bytes(projection_payload))
            epoch_seed = digest_bytes(
                canonical_bytes(
                    {
                        "semantic": semantic_digest,
                        "snapshot": source_digest,
                        "frontier": finite_frontier,
                        "budget": config["approval_policy"]["run_budget"],
                        "risk": _binding_semantics(
                            config["approval_policy"]["risk_policy_ref"]
                        ),
                    }
                )
            )
            manifest = {
                "schema_version": "1.0.0",
                "manifest_id": f"oem-{projection_digest[:24]}",
                "evidence_ceiling": config["evidence_ceiling"],
                "classifier_version": config["classifier_version"],
                "objective_ref": config["objective_ref"],
                "closure_receipt_refs": config["closure_receipt_refs"],
                "authority_bindings": {
                    **config["authority_bindings"],
                    "derived_projection_refs": [
                        {
                            "producer": "work-pack-readiness-audit",
                            "audit_projection_digest": projection_digest,
                            "authority_effect": "none",
                        }
                    ],
                    "execution_byte_baselines": [
                        {
                            "unit_id": unit["unit_id"],
                            "baselines": unit["byte_baselines"],
                        }
                        for unit in config["execution_bindings"]
                    ],
                },
                "canonical_plan_graph": {
                    "units": [
                        {
                            "unit_id": unit["unit_id"],
                            "dependencies": unit["dependencies"],
                            "canonical_successors": unit["canonical_successors"],
                        }
                        for unit in config["execution_bindings"]
                    ],
                    "finite_frontier": finite_frontier,
                },
                "execution_bindings": config["execution_bindings"],
                "receipt_bindings": config["receipt_bindings"],
                "closeout_bindings": config["closeout_bindings"],
                "runtime_binding": config["runtime_binding"],
                "status_receipt_refs": config["status_receipt_refs"],
                "lifecycle_status_refs": config["lifecycle_status_refs"],
                "epoch_binding": {
                    "epoch_id": f"epoch-{epoch_seed[:24]}",
                    "audit_projection_digest": projection_digest,
                    "canonical_semantic_digest": semantic_digest,
                    "source_snapshot_digest": source_digest,
                    "approved_frontier_ref": finite_frontier,
                    "run_budget": config["approval_policy"]["run_budget"],
                    "risk_policy_ref": config["approval_policy"]["risk_policy_ref"],
                    "decision_gate_approval_receipt_ref": config["approval_policy"][
                        "decision_gate_receipt_ref"
                    ],
                    "approval_status": "unapproved",
                },
                "continuity_projection": config["continuity_projection"],
                "semantic_component_digests": component_digests,
                "authority_effect": "none",
                "selected_unit": None,
                "mutation_ready": False,
            }
            manifest_errors = schema_errors(
                manifest, load_json(MANIFEST_SCHEMA), "objective execution manifest"
            )
            if manifest_errors:
                blockers.extend(
                    _v2_blocker("MANIFEST_SCHEMA_INVALID", "manifest", error)
                    for error in manifest_errors
                )
                manifest = None
                projection_digest = None

    semantic_repair_entry = (
        _plan_once_semantic_repair_entry(config, plan_semantics, blockers)
        if plan_once
        else None
    )
    verdict = "block" if blockers else "pass"
    report = {
        "schema_version": "2.0.0",
        "audit_id": config["audit_id"],
        "canonical_spell_id": "work-pack-readiness-audit",
        "verdict": verdict,
        "terminal_code": blockers[0]["code"] if blockers else (
            "PLAN_SEMANTIC_READY" if plan_once else "PROJECTION_READY"
        ),
        "evidence_ceiling": config["evidence_ceiling"],
        "manifest": manifest,
        "blockers": blockers,
        "flags": [],
        "source_snapshot": {
            "digest": source_digest,
            "artifact_count": len(initial_snapshot),
            "drift": drift,
        },
        "semantic_component_digests": component_digests,
        "canonical_semantic_digest": semantic_digest,
        "audit_projection_digest": projection_digest,
        "configured_commands_executed": False,
        "selected_unit": None,
        "authority_effect": "none",
        "mutation_ready": False,
        "next_owner": (
            "implementation-readiness:execute"
            if verdict == "pass" and plan_once
            else "decision-gate"
            if verdict == "pass"
            else "invoke:refresh"
        ),
    }
    if plan_once:
        report["admission_timing"] = "selected-unit-at-task-session"
        report["runtime_admission_status"] = (
            "pending-selection" if verdict == "pass" else "block"
        )
        report["execution_entry"] = (
            manifest["execution_entry"]
            if manifest is not None
            else semantic_repair_entry
            if semantic_repair_entry is not None
            else {
                "entry_state": "blocked",
                "selected_unit": None,
                "route_id": None,
                "next_owner": {
                    "capability": "invoke",
                    "mode": "refresh",
                    "target": config["audit_id"],
                },
                "blocker_code": blockers[0]["code"] if blockers else "PLAN_BLOCKED",
            }
        )
    return report


def write_outputs_v2(report: dict[str, Any], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    report_path = output_dir / "work-pack-readiness-report-v2.json"
    plan_once = report.get("admission_timing") == "selected-unit-at-task-session"
    manifest_path = output_dir / (
        "plan-semantic-manifest.json"
        if plan_once
        else "objective-execution-manifest.json"
    )
    handoff_path = output_dir / "selection-handoff.json"
    targets = [report_path]
    if report["manifest"] is not None:
        targets.append(manifest_path)
        if plan_once:
            targets.append(handoff_path)
    existing = [str(path) for path in targets if path.exists()]
    if existing:
        raise ValueError(f"refusing to overwrite audit outputs: {', '.join(existing)}")
    report_errors = schema_errors(
        report, load_json(REPORT_SCHEMA_V2), "audit report v2"
    )
    if report_errors:
        raise ValueError("; ".join(report_errors))
    report_path.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    if report["manifest"] is not None:
        manifest_bytes = (
            json.dumps(report["manifest"], indent=2, sort_keys=True) + "\n"
        ).encode("utf-8")
        manifest_path.write_bytes(manifest_bytes)
        if plan_once:
            handoff = {
                "schema_version": "1.0.0",
                "audit_id": report["audit_id"],
                "plan_epoch_id": report["manifest"]["plan_epoch_id"],
                "manifest_ref": {
                    "path": manifest_path.name,
                    "sha256": digest_bytes(manifest_bytes),
                    "size_bytes": len(manifest_bytes),
                },
                "ready_frontier": report["manifest"]["ready_frontier"],
                "allowed_routes": report["manifest"]["allowed_routes"],
                "allowed_routes_digest": report["manifest"][
                    "allowed_routes_digest"
                ],
                "execution_entry": report["manifest"]["execution_entry"],
                "next_owner": "implementation-readiness:execute",
                "selection_required": True,
                "authority_effect": "none",
                "mutation_ready": False,
            }
            errors = schema_errors(
                handoff, load_json(SELECTION_HANDOFF_SCHEMA), "selection handoff"
            )
            if errors:
                raise ValueError("; ".join(errors))
            handoff_path.write_text(
                json.dumps(handoff, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config = load_json(args.config)
    schema_version = config.get("schema_version")
    if schema_version not in {"1.0.0", "2.0.0"}:
        raise SystemExit(f"unsupported audit config schema_version: {schema_version!r}")
    is_v2 = schema_version == "2.0.0"
    config_schema = CONFIG_SCHEMA_V2 if is_v2 else CONFIG_SCHEMA
    config_errors = schema_errors(config, load_json(config_schema), "audit config")
    if config_errors:
        raise SystemExit("\n".join(config_errors))
    repository_root = args.config.resolve().parent
    while repository_root.parent != repository_root and not (
        repository_root / ".git"
    ).exists():
        repository_root = repository_root.parent
    if not (repository_root / ".git").exists():
        raise SystemExit("repository root could not be discovered from config path")
    if is_v2:
        report = audit_v2(config, repository_root)
        write_outputs_v2(report, args.output_dir)
    else:
        report = audit(config, repository_root)
        write_outputs(report, args.output_dir)
    print(
        json.dumps(
            {
                "audit_id": report["audit_id"],
                "verdict": report["verdict"],
                "schema_version": report["schema_version"],
                "terminal_code": report.get("terminal_code"),
                "plan_contract_status": report.get("plan_contract_status"),
                "runtime_admission_status": report.get("runtime_admission_status"),
                "receipt_semantics_status": report.get("receipt_semantics_status"),
                "finding_count": len(
                    report.get("findings", report.get("blockers", []))
                ),
                "output_dir": str(args.output_dir),
            },
            sort_keys=True,
        )
    )
    return 0 if report["verdict"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())
