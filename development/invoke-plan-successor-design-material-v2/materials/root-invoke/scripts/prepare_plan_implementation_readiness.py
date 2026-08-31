#!/usr/bin/env python3
"""Produce one proof-only Implementation Readiness receipt for Invoke Plan."""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


INVOKE_ROOT = Path(__file__).resolve().parents[1]
CAPABILITY_ROOT = INVOKE_ROOT.parent
READINESS_SCRIPTS = CAPABILITY_ROOT / "implementation-readiness" / "scripts"
READINESS_PATH = READINESS_SCRIPTS / "readiness_execution.py"
AUDIT_PATH = (
    CAPABILITY_ROOT / "work-pack-readiness-audit" / "scripts" / "audit_work_pack.py"
)


class AuditCommandError(RuntimeError):
    def __init__(self, returncode: int):
        super().__init__(f"Work Pack Readiness Audit failed with exit {returncode}")
        self.returncode = returncode


def load_readiness() -> Any:
    sys.path.insert(0, str(READINESS_SCRIPTS))
    specification = importlib.util.spec_from_file_location(
        "invoke_plan_implementation_readiness", READINESS_PATH
    )
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot load Implementation Readiness: {READINESS_PATH}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit-config", required=True, type=Path)
    audit_source = parser.add_mutually_exclusive_group(required=True)
    audit_source.add_argument("--audit-output-dir", type=Path)
    audit_source.add_argument("--audit-report", type=Path)
    parser.add_argument("--proof-invocation-id", required=True)
    parser.add_argument("--proof-created-at", required=True)
    parser.add_argument("--output", required=True, type=Path)
    return parser.parse_args()


def produce_audit_report(config_path: Path, output_dir: Path) -> Path:
    completed = subprocess.run(
        [
            sys.executable,
            str(AUDIT_PATH),
            "--config",
            str(config_path),
            "--output-dir",
            str(output_dir),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.stdout:
        sys.stderr.write(completed.stdout)
    if completed.stderr:
        sys.stderr.write(completed.stderr)
    if completed.returncode != 0:
        raise AuditCommandError(completed.returncode)
    return output_dir / "work-pack-readiness-report-v2.json"


def assert_contract_readiness_boundary(report: dict) -> None:
    """WPRA cannot present future implementation output validity as evidence."""
    manifest = report.get("manifest") or report.get("plan_semantic_manifest") or {}
    if report.get("outputs_validated") is True or manifest.get("outputs_validated") is True:
        raise ValueError("WPRA cannot claim future implementation outputs are validated")


def main() -> int:
    args = parse_args()
    try:
        report_path = (
            produce_audit_report(args.audit_config, args.audit_output_dir)
            if args.audit_output_dir is not None
            else args.audit_report
        )
        report = load_json(report_path)
        assert_contract_readiness_boundary(report)
        readiness = load_readiness()
        receipt = readiness.compile_plan_readiness_preflight(
            load_json(args.audit_config),
            report,
            proof_invocation_id=args.proof_invocation_id,
            proof_created_at=args.proof_created_at,
        )
    except AuditCommandError as error:
        print(f"BLOCK: {error}", file=sys.stderr)
        return error.returncode if error.returncode > 0 else 1
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as error:
        print(f"BLOCK: {error}", file=sys.stderr)
        return 2
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "status": receipt["status"],
                "code": receipt["code"],
                "output": str(args.output),
                "audit_report": str(report_path),
                "authority_effect": receipt["authority_effect"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
