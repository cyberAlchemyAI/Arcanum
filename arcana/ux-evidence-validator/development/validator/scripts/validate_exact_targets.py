from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


SWU_ID = "SWU-UEV-001"
TARGETS = [
    "arcanum/arcana/ux-evidence-validator/development/validator/contracts/terminal-outcome.schema.json",
    "arcanum/arcana/ux-evidence-validator/development/validator/uev_kernel/terminal.py",
    "arcanum/arcana/ux-evidence-validator/development/validator/scripts/validate_contracts.py",
    "arcanum/arcana/ux-evidence-validator/development/validator/scripts/validate_exact_targets.py",
    "arcanum/arcana/ux-evidence-validator/development/validator/tests/test_terminal_outcome.py",
]


def repository_root() -> Path:
    return Path(__file__).resolve().parents[6]


def whitespace_errors(content: bytes) -> list[str]:
    errors: list[str] = []
    if not content.endswith(b"\n"):
        errors.append("missing final newline")
    if b"\x00" in content:
        errors.append("contains NUL byte")
    for number, line in enumerate(content.decode("utf-8", errors="replace").splitlines(), 1):
        if line.endswith((" ", "\t")):
            errors.append(f"trailing whitespace at line {number}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--swu", required=True)
    args = parser.parse_args()
    if args.swu != SWU_ID:
        print(json.dumps({"reason": "SWU_MISMATCH", "verdict": "block"}, sort_keys=True))
        return 2
    root = repository_root()
    records = []
    errors: list[str] = []
    for relative in TARGETS:
        path = root / relative
        item = {"path": relative, "present": path.is_file()}
        if not path.is_file():
            errors.append(f"missing declared target: {relative}")
            records.append(item)
            continue
        content = path.read_bytes()
        item.update({"sha256": hashlib.sha256(content).hexdigest(), "size_bytes": len(content)})
        target_errors = whitespace_errors(content)
        if relative.endswith(".json"):
            try:
                json.loads(content)
            except (UnicodeDecodeError, json.JSONDecodeError) as error:
                target_errors.append(f"invalid JSON: {error}")
        if target_errors:
            errors.extend(f"{relative}: {error}" for error in target_errors)
        records.append(item)
    result = {
        "declared_target_count": len(TARGETS),
        "errors": errors,
        "schema_version": "uev.exact-target-validation/v1",
        "swu_id": SWU_ID,
        "targets": records,
        "tracking_source": "filesystem-only",
        "verdict": "pass" if not errors else "block",
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
