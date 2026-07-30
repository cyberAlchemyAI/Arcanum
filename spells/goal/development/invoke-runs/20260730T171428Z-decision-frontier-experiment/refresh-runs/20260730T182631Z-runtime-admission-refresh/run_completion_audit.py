#!/usr/bin/env python3
"""Build the final receipt-backed audit for the decision-frontier experiment."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path
from typing import Any


RUN = Path(
    "spells/goal/development/invoke-runs/"
    "20260730T171428Z-decision-frontier-experiment"
)
TARGET = Path("spells/goal/development/decision-frontier-experiment")
REFRESH = (
    RUN
    / "refresh-runs"
    / "20260730T182631Z-runtime-admission-refresh"
)
MUTATION_UNITS = [f"SWU-DFE-{index:03d}" for index in range(1, 8)]
ORDERED_UNITS = [*MUTATION_UNITS, "VERIFY-DFE-001", "READINESS-DFE-001"]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_digest(document: Any) -> str:
    payload = json.dumps(
        document,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def artifact_matches(root: Path, artifact: dict[str, Any]) -> bool:
    path = root / artifact["path"]
    return (
        path.is_file()
        and sha256(path) == artifact["sha256"]
        and path.stat().st_size == artifact["size_bytes"]
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--arcanum-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--forbidden-public-token",
        action="append",
        required=True,
        help=(
            "Case-insensitive token forbidden in the public target. "
            "Repeat for each caller-owned boundary marker."
        ),
    )
    args = parser.parse_args()

    root = args.arcanum_root.resolve()
    forbidden_public_tokens = tuple(
        dict.fromkeys(
            token.strip().lower()
            for token in args.forbidden_public_token
            if token.strip()
        )
    )
    if not forbidden_public_tokens:
        parser.error("at least one non-empty --forbidden-public-token is required")
    output = args.output
    if not output.is_absolute():
        output = root / output

    checks: list[dict[str, Any]] = []

    def record(check_id: str, passed: bool, evidence: Any) -> None:
        checks.append(
            {
                "check_id": check_id,
                "status": "pass" if passed else "fail",
                "evidence": evidence,
            }
        )

    work_pack_path = root / RUN / "WORK-PACK.md"
    work_pack_digest = sha256(work_pack_path)

    readiness_path = (
        root
        / RUN
        / "readiness-runs/post-execution/results/work-pack-readiness-report.json"
    )
    readiness = load_json(readiness_path)
    readiness_pass = (
        readiness.get("verdict") == "pass"
        and readiness.get("plan_contract_status") == "pass"
        and readiness.get("runtime_admission_status") == "pass"
        and readiness.get("receipt_semantics_status") == "pass"
        and readiness.get("findings") == []
        and readiness.get("ready_frontier") == []
    )
    record(
        "post-execution-readiness",
        readiness_pass,
        {
            "path": str(readiness_path.relative_to(root)),
            "verdict": readiness.get("verdict"),
            "finding_count": len(readiness.get("findings", [])),
            "ready_frontier": readiness.get("ready_frontier"),
        },
    )

    chain_path = root / RUN / "execution-control/CHAIN-STATE.json"
    chain = load_json(chain_path)
    chain_pass = (
        chain.get("ordered_frontier") == ORDERED_UNITS
        and chain.get("completed") == ORDERED_UNITS
        and chain.get("next_unit") is None
        and chain.get("selected_next") is False
        and chain.get("last_result") == "PASS"
        and chain.get("stop_reason") == "complete"
        and chain.get("authority_effect") == "none"
        and chain.get("background_helper", {}).get("open") == 0
        and chain.get("background_helper", {}).get("spawned") == 1
        and chain.get("background_helper", {}).get("joined") == 1
        and chain.get("background_helper", {}).get("closed") == 1
    )
    record(
        "series-chain",
        chain_pass,
        {
            "path": str(chain_path.relative_to(root)),
            "completed": chain.get("completed"),
            "next_unit": chain.get("next_unit"),
            "stop_reason": chain.get("stop_reason"),
            "background_helper": chain.get("background_helper"),
        },
    )

    context_failures: list[str] = []
    admission_failures: list[str] = []
    for unit in ORDERED_UNITS:
        control = root / RUN / "execution-control" / unit
        context = load_json(control / "CONTEXT-PACK.index.json")
        if not (
            context.get("strict_coverage") is True
            and context.get("covered_count") == context.get("obligation_count")
            and artifact_matches(root, context["context_pack"])
            and artifact_matches(root, context["markdown"])
        ):
            context_failures.append(unit)

        admission = load_json(control / "mutation-admission-receipt.json")
        expected_profile = (
            "material-bound"
            if unit in MUTATION_UNITS
            else "execution-output-only"
        )
        if not (
            admission.get("admissionVerdict") == "admit"
            and admission.get("mutationReady") is True
            and admission.get("reasons") == []
            and admission.get("writeProfile") == expected_profile
            and admission.get("swuId") == unit
        ):
            admission_failures.append(unit)
    record(
        "context-builder-coverage",
        not context_failures,
        {"units_checked": len(ORDERED_UNITS), "failed_units": context_failures},
    )
    record(
        "task-session-admission",
        not admission_failures,
        {"units_checked": len(ORDERED_UNITS), "failed_units": admission_failures},
    )

    package_failures: list[str] = []
    for unit in MUTATION_UNITS:
        package_path = root / REFRESH / "material-packages" / unit / "material-package.json"
        receipt_path = root / REFRESH / "material-packages" / unit / "material-receipt.json"
        admission_path = (
            root / RUN / "execution-control" / unit / "mutation-admission-receipt.json"
        )
        request_path = (
            root / RUN / "execution-control" / unit / "mutation-admission-request.json"
        )
        package = load_json(package_path)
        receipt = load_json(receipt_path)
        admission = load_json(admission_path)
        request = load_json(request_path)
        changes_match = all(
            artifact_matches(root, change["output_ref"])
            and artifact_matches(
                root,
                {
                    "path": change["target_path"],
                    "sha256": change["output_ref"]["sha256"],
                    "size_bytes": change["output_ref"]["size_bytes"],
                },
            )
            for change in package.get("changes", [])
        )
        if not (
            canonical_digest(package) == admission.get("materialPackageDigest")
            and canonical_digest(package) == receipt.get("packageDigest")
            and sha256(receipt_path) == admission.get("materialReceiptDigest")
            and artifact_matches(
                root,
                {
                    "path": request["materialPackage"]["path"],
                    "sha256": request["materialPackage"]["sha256"],
                    "size_bytes": request["materialPackage"]["sizeBytes"],
                },
            )
            and artifact_matches(
                root,
                {
                    "path": request["materialReceipt"]["path"],
                    "sha256": request["materialReceipt"]["sha256"],
                    "size_bytes": request["materialReceipt"]["sizeBytes"],
                },
            )
            and receipt.get("patchVerdict") == "pass"
            and receipt.get("mutationHandoff") == "ready"
            and receipt.get("dependencyResult") == "pass"
            and receipt.get("ownerBoundaryResult") == "pass"
            and receipt.get("publicationBoundaryResult") == "pass"
            and receipt.get("reasons") == []
            and changes_match
        ):
            package_failures.append(unit)
    record(
        "producer-material-integrity",
        not package_failures,
        {"packages_checked": len(MUTATION_UNITS), "failed_units": package_failures},
    )

    expected_target_files: set[str] = set()
    terminal_failures: list[str] = []
    owner_failures: list[str] = []
    validation_statuses: dict[str, str | None] = {}
    for unit in MUTATION_UNITS:
        evidence_root = root / TARGET / "session-evidence" / unit
        receipt_path = evidence_root / "task-session-receipt.json"
        owner_path = evidence_root / "owner-receipt.json"
        receipt = load_json(receipt_path)
        owner = load_json(owner_path)
        artifact_integrity = all(
            artifact_matches(root, artifact)
            for artifact in receipt.get("artifacts", [])
        )
        validation_statuses[unit] = receipt.get("validation_result")
        if not (
            receipt.get("unit_id") == unit
            and receipt.get("work_pack_sha256") == work_pack_digest
            and receipt.get("status") == "pass"
            and receipt.get("validation_result") == "pass"
            and receipt.get("blockers") == []
            and receipt.get("undeclared_writes") == []
            and artifact_integrity
        ):
            terminal_failures.append(unit)
        if not (
            owner.get("unit_id") == unit
            and owner.get("owner") == "invoke:refresh:apply-approved"
            and owner.get("lifecycle_owner") == "spellcraft"
            and owner.get("validation_result") == "pass"
            and owner.get("blockers") == []
            and artifact_matches(root, owner["source_receipt"])
        ):
            owner_failures.append(unit)
        expected_target_files.update(
            artifact["path"] for artifact in receipt.get("artifacts", [])
        )
        expected_target_files.add(str(receipt_path.relative_to(root)))
        expected_target_files.add(str(owner_path.relative_to(root)))
    record(
        "terminal-task-session-receipts",
        not terminal_failures,
        {
            "receipts_checked": len(MUTATION_UNITS),
            "validation_statuses": validation_statuses,
            "failed_units": terminal_failures,
        },
    )
    record(
        "invoke-refresh-closeout-receipts",
        not owner_failures,
        {"receipts_checked": len(MUTATION_UNITS), "failed_units": owner_failures},
    )

    verify_root = root / TARGET / "session-evidence/VERIFY-DFE-001"
    closure_receipt_path = verify_root / "closure-receipt.json"
    closure_receipt = load_json(closure_receipt_path)
    authority_path = verify_root / "authority-hashes.json"
    authority = load_json(authority_path)
    canonical_failures: list[str] = []
    for item in authority.get("canonical_inputs", []):
        canonical_path = root / item["path"]
        if not (
            item.get("match") is True
            and item.get("before_sha256") == item.get("after_sha256")
            and canonical_path.is_file()
            and sha256(canonical_path) == item.get("after_sha256")
            and canonical_path.stat().st_size == item.get("size_bytes")
        ):
            canonical_failures.append(item["path"])
    closure_pass = (
        closure_receipt.get("unit_id") == "VERIFY-DFE-001"
        and closure_receipt.get("work_pack_sha256") == work_pack_digest
        and closure_receipt.get("status") == "pass"
        and closure_receipt.get("validation_result") == "pass"
        and closure_receipt.get("blockers") == []
        and closure_receipt.get("undeclared_writes") == []
        and all(
            artifact_matches(root, artifact)
            for artifact in closure_receipt.get("artifacts", [])
        )
        and authority.get("status") == "pass"
        and authority.get("authority_effect") == "none"
        and authority.get("missing_or_blocked") == []
        and len(authority.get("owner_receipts", [])) == len(MUTATION_UNITS)
        and all(
            artifact_matches(root, artifact)
            for artifact in authority.get("owner_receipts", [])
        )
        and not canonical_failures
    )
    record(
        "authority-closure",
        closure_pass,
        {
            "closure_receipt": str(closure_receipt_path.relative_to(root)),
            "canonical_inputs_checked": len(authority.get("canonical_inputs", [])),
            "canonical_failures": canonical_failures,
            "owner_receipts_checked": len(authority.get("owner_receipts", [])),
            "authority_effect": authority.get("authority_effect"),
        },
    )
    expected_target_files.add(str(authority_path.relative_to(root)))
    expected_target_files.add(str(closure_receipt_path.relative_to(root)))

    lifecycle_path = (
        root / TARGET / "session-evidence/READINESS-DFE-001/lifecycle-decision.json"
    )
    lifecycle = load_json(lifecycle_path)
    source_closure = lifecycle["source_closure"]
    source_closure_path = root / "spells" / source_closure["path"]
    lifecycle_pass = (
        lifecycle.get("status") == "pass"
        and lifecycle.get("unit_id") == "READINESS-DFE-001"
        and lifecycle.get("owner") == "spellcraft"
        and lifecycle.get("decision")
        == "authorize-paired-real-workflow-experiment-proposal"
        and lifecycle.get("promotion") is False
        and lifecycle.get("publication") is False
        and lifecycle.get("authority_effect") == "none"
        and lifecycle.get("selected_swu") is None
        and lifecycle.get("successor") is None
        and lifecycle.get("experiment_harness_status") == "not_applicable"
        and source_closure_path == closure_receipt_path
        and source_closure_path.is_file()
        and sha256(source_closure_path) == source_closure["sha256"]
        and source_closure_path.stat().st_size == source_closure["size_bytes"]
    )
    record(
        "lifecycle-ceiling",
        lifecycle_pass,
        {
            "path": str(lifecycle_path.relative_to(root)),
            "decision": lifecycle.get("decision"),
            "promotion": lifecycle.get("promotion"),
            "publication": lifecycle.get("publication"),
            "authority_effect": lifecycle.get("authority_effect"),
        },
    )
    expected_target_files.add(str(lifecycle_path.relative_to(root)))

    continuation_path = root / RUN / "CONTINUATION.json"
    continuation = load_json(continuation_path)
    final_owner_path = root / RUN / "execution-control/FINAL-CLOSEOUT-OWNER-RECEIPT.json"
    final_owner = load_json(final_owner_path)
    continuation_pass = (
        continuation.get("state") == "complete"
        and continuation.get("first_selectable_swu") is None
        and continuation.get("selected_swu") is None
        and continuation.get("selection_allowed") is False
        and continuation.get("next_route")
        == "spellcraft:paired-real-workflow-experiment-proposal"
        and continuation.get("authority_effect") == "none"
        and final_owner.get("status") == "pass"
        and final_owner.get("blockers") == []
        and final_owner.get("promotion") is False
        and final_owner.get("publication") is False
        and final_owner.get("authority_effect") == "none"
        and artifact_matches(root, final_owner["source_receipt"])
        and sha256(continuation_path) == final_owner["target"]["after_sha256"]
        and continuation_path.stat().st_size
        == final_owner["target"]["after_size_bytes"]
    )
    record(
        "continuation-closeout",
        continuation_pass,
        {
            "continuation": str(continuation_path.relative_to(root)),
            "state": continuation.get("state"),
            "next_route": continuation.get("next_route"),
            "final_owner_receipt": str(final_owner_path.relative_to(root)),
        },
    )

    target_root = root / TARGET
    actual_target_files = {
        str(path.relative_to(root))
        for path in target_root.rglob("*")
        if path.is_file()
    }
    missing_files = sorted(expected_target_files - actual_target_files)
    extra_files = sorted(actual_target_files - expected_target_files)
    record(
        "exact-target-inventory",
        not missing_files and not extra_files,
        {
            "expected_file_count": len(expected_target_files),
            "actual_file_count": len(actual_target_files),
            "missing": missing_files,
            "extra": extra_files,
        },
    )

    json_failures: list[str] = []
    python_failures: list[str] = []
    generated_residue: list[str] = []
    public_boundary_hits: list[dict[str, Any]] = []
    for path in sorted(target_root.rglob("*")):
        if path.is_dir() and path.name == "__pycache__":
            generated_residue.append(str(path.relative_to(root)))
            continue
        if not path.is_file():
            continue
        relative = str(path.relative_to(root))
        if path.suffix == ".json":
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                json_failures.append(relative)
        if path.suffix == ".py":
            try:
                ast.parse(path.read_text(encoding="utf-8"), filename=relative)
            except (UnicodeDecodeError, SyntaxError):
                python_failures.append(relative)
        if path.suffix == ".pyc":
            generated_residue.append(relative)
        try:
            lowered = path.read_text(encoding="utf-8").lower()
        except UnicodeDecodeError:
            continue
        for token in forbidden_public_tokens:
            if token in lowered:
                public_boundary_hits.append({"path": relative, "token": token})
    record(
        "target-syntax-and-residue",
        not json_failures and not python_failures and not generated_residue,
        {
            "json_failures": json_failures,
            "python_failures": python_failures,
            "generated_residue": generated_residue,
        },
    )
    record(
        "public-boundary-scan",
        not public_boundary_hits,
        {"hits": public_boundary_hits},
    )

    observability_path = root / ".arcanum/observability/signals/sigil-invocations.jsonl"
    observations: list[tuple[int, dict[str, Any]]] = []
    with observability_path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            item = json.loads(line)
            if item.get("run_id") == "goal-dfe-work-pack-20260730":
                observations.append((line_number, item))
    observation_pass = (
        len(observations) == 1
        and observations[0][1].get("execution", {}).get("status") == "completed"
        and observations[0][1].get("observer", {}).get("quality_bar_status") == "pass"
        and observations[0][1].get("observer", {}).get("recommendation")
        == "targeted-update"
    )
    record(
        "signal-observer-receipt",
        observation_pass,
        {
            "path": str(observability_path.relative_to(root)),
            "matching_records": len(observations),
            "line": observations[0][0] if observations else None,
        },
    )

    failed_checks = [
        check["check_id"] for check in checks if check["status"] != "pass"
    ]
    report = {
        "schema_version": "goal-dfe-completion-audit.v1",
        "status": "pass" if not failed_checks else "fail",
        "work_pack": {
            "path": str(work_pack_path.relative_to(root)),
            "sha256": work_pack_digest,
            "unit_count": len(ORDERED_UNITS),
        },
        "claim_ceiling": {
            "fixture_behavior": "validated",
            "paired_real_workflow_experiment": "proposal-authorized",
            "canonical_adoption": False,
            "promotion": False,
            "publication": False,
            "authority_effect": "none",
        },
        "summary": {
            "check_count": len(checks),
            "passed_check_count": len(checks) - len(failed_checks),
            "failed_check_count": len(failed_checks),
            "failed_checks": failed_checks,
            "completed_units": len(chain.get("completed", [])),
            "target_file_count": len(actual_target_files),
        },
        "checks": checks,
    }

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "output": str(output.relative_to(root)),
                "status": report["status"],
                **report["summary"],
            },
            sort_keys=True,
        )
    )
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
