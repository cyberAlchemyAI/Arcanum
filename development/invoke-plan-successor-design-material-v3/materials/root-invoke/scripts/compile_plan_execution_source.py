#!/usr/bin/env python3
"""Validate one Plan machine source and derive WPRA and human projections."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

INVOKE_ROOT = Path(__file__).resolve().parents[1]
SOURCE_SCHEMA = INVOKE_ROOT / "schemas" / "plan-execution-source-v1.schema.json"
WPRA_ROOT = INVOKE_ROOT.parent / "work-pack-readiness-audit"
WPRA_SCHEMA = WPRA_ROOT / "schemas" / "audit-config-v2.schema.json"
WPRA_RUNNER = WPRA_ROOT / "scripts" / "audit_work_pack.py"


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def schema_errors(value: Any, schema: dict[str, Any], label: str) -> list[str]:
    return [
        f"{label} invalid at {'/'.join(map(str, error.absolute_path)) or '<root>'}: {error.message}"
        for error in sorted(Draft202012Validator(schema).iter_errors(value), key=lambda item: list(item.absolute_path))
    ]


def semantic_errors(source: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    config = source["wpra_config"]
    units = config["execution_bindings"]
    unit_ids = [unit["unit_id"] for unit in units]
    unit_set = set(unit_ids)
    policy = config.get("execution_policy", {})
    if len(unit_ids) != len(unit_set):
        errors.append("execution unit ids must be unique")
    if source["work_pack"]["work_pack_id"] != policy.get("work_pack_id"):
        errors.append("work_pack_id must equal execution_policy.work_pack_id")
    if config["approval_policy"]["run_budget"]["max_task_session_requests"] != len(units):
        errors.append("run budget must equal the exact frontier length")

    declared_routes = source["route_contracts"]
    projected_routes = policy.get("allowed_routes", [])
    if canonical_bytes(declared_routes) != canonical_bytes(projected_routes):
        errors.append("allowed routes must equal the canonical route contracts in every field")
    if policy.get("allowed_routes_digest") != digest(declared_routes):
        errors.append("allowed_routes_digest must equal the canonical route contracts digest")

    route_by_unit: dict[str, dict[str, Any]] = {}
    for route in declared_routes:
        unit_id = route["frontier_swu"]
        if unit_id in route_by_unit:
            errors.append(f"{unit_id}: exactly one allowed route is required")
        route_by_unit[unit_id] = route
        if route["target"] != unit_id:
            errors.append(f"{unit_id}: route target must equal the frontier unit")
        if route["capability"] != "task-session" or route["mode"] != "execute":
            errors.append(f"{unit_id}: execution route must be task-session execute")
        if route["effect_class"] != source["requested_effect"]["effect_class"]:
            errors.append(f"{unit_id}: route effect differs from requested effect")
    if set(route_by_unit) != unit_set:
        errors.append("allowed routes must cover the exact execution frontier")

    seen: set[str] = set()
    for unit in units:
        unit_id = unit["unit_id"]
        if any(dependency not in seen for dependency in unit["dependencies"]):
            errors.append(f"{unit_id}: dependencies must reference earlier frontier units")
        seen.add(unit_id)
        allowed = set(unit["allowed_writes"])
        dispositions = {
            target["path"] for target in unit["target_dispositions"]
            if target["disposition"] in {"create", "update", "delete"}
        }
        outputs = {contract["expected_path"] for contract in unit["output_contracts"]}
        if dispositions != allowed or outputs != allowed:
            errors.append(f"{unit_id}: writable dispositions, outputs, and allowed writes must be equal")
        route = route_by_unit.get(unit_id)
        if route is not None and set(route["write_scope"]) != allowed:
            errors.append(f"{unit_id}: route write scope must equal allowed writes")
        phases = {contract["phase"] for contract in unit["validation_contracts"]}
        if any(output["validation_phase"] not in phases for output in unit["output_contracts"]):
            errors.append(f"{unit_id}: every output validation phase requires a command")
    return errors


def validate(source: dict[str, Any]) -> list[str]:
    errors = schema_errors(source, load_json(SOURCE_SCHEMA), "plan execution source")
    if errors:
        return errors
    errors.extend(schema_errors(source["wpra_config"], load_json(WPRA_SCHEMA), "WPRA config"))
    return errors or semantic_errors(source)


def render_human_view(source: dict[str, Any]) -> str:
    work_pack = source["work_pack"]
    lines = [
        f"# WORK-PACK: {work_pack['title']}", "",
        f"Machine source: `{source['source_id']}` (`{source['schema_version']}`).", "",
        "## Objective", "", work_pack["objective"], "", "## Execution frontier", "",
        "| Unit | Dependencies | Producer | Writes |", "| --- | --- | --- | --- |",
    ]
    for unit in source["wpra_config"]["execution_bindings"]:
        dependencies = ", ".join(unit["dependencies"]) or "none"
        lines.append(f"| `{unit['unit_id']}` | {dependencies} | `{unit['producer_id']}` | {', '.join(unit['allowed_writes'])} |")
    lines += ["", "## Boundary", "", "This derived view grants no selection, admission, execution, publication, deployment, or external-effect authority.", ""]
    return "\n".join(lines)


def run_wpra(config_path: Path, output_dir: Path) -> dict[str, Any]:
    completed = subprocess.run(
        [sys.executable, str(WPRA_RUNNER), "--config", str(config_path), "--output-dir", str(output_dir)],
        text=True, capture_output=True, check=False,
    )
    if completed.returncode:
        report_path = output_dir / "work-pack-readiness-report-v2.json"
        details = completed.stderr.strip() or completed.stdout.strip()
        if report_path.is_file():
            report = load_json(report_path)
            codes = [item.get("code", "UNKNOWN") for item in report.get("blockers", [])]
            details = f"terminal={report.get('terminal_code')}; blockers={codes}"
        raise ValueError(f"WPRA failed ({completed.returncode}): {details}")
    return load_json(output_dir / "work-pack-readiness-report-v2.json")


def compile_source(source: dict[str, Any], output_dir: Path) -> dict[str, Any]:
    errors = validate(source)
    if errors:
        raise ValueError("\n".join(errors))
    if output_dir.exists():
        raise ValueError(f"output directory already exists: {output_dir}")
    if not output_dir.parent.is_dir():
        raise ValueError(f"output parent must already exist: {output_dir.parent}")

    stage = Path(tempfile.mkdtemp(prefix=f".{output_dir.name}.stage-", dir=output_dir.parent))
    try:
        config_path = stage / "WPRA-CONFIG.json"
        config_path.write_text(json.dumps(source["wpra_config"], indent=2, sort_keys=True) + "\n")
        (stage / "WORK-PACK.md").write_text(render_human_view(source))
        receipt: dict[str, Any] = {
            "schema_version": "invoke.plan-execution-source-validation-receipt.v1",
            "result": "pass", "source_digest": digest(source),
            "wpra_config_digest": digest(source["wpra_config"]),
            "human_view_generated": True, "configured_commands_executed": False,
            "authority_effect": "none",
        }
        first = run_wpra(config_path, stage / "wpra-run-1")
        second = run_wpra(config_path, stage / "wpra-run-2")
        projection = first.get("audit_projection_digest")
        if first.get("verdict") != "pass" or second.get("verdict") != "pass":
            raise ValueError("both WPRA rehearsals must explicitly PASS")
        if not projection or projection != second.get("audit_projection_digest"):
            raise ValueError("WPRA two-run projection digest is absent or mismatched")
        receipt["wpra_rehearsal"] = {
            "runs": 2, "verdicts": ["pass", "pass"],
            "projection_digest": projection, "configured_commands_executed": False,
        }
        receipt["receipt_digest"] = digest(receipt)
        (stage / "SOURCE-VALIDATION-RECEIPT.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
        os.replace(stage, output_dir)
        return receipt
    except Exception:
        shutil.rmtree(stage, ignore_errors=True)
        raise


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source = load_json(args.source)
    try:
        receipt = compile_source(source, args.output_dir)
    except ValueError as error:
        raise SystemExit(str(error)) from error
    print(json.dumps(receipt, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
