#!/usr/bin/env python3
"""Compile machine-first Context Builder admission input from a closed unit."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/native-context-admission-projection-v1.schema.json"


def load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value


def projection_validator_path() -> Path:
    candidates = [
        ROOT.parents[1] / "arcana/task-session/scripts/execution_entry_projection.py",
        ROOT.parent / "task-session/scripts/execution_entry_projection.py",
    ]
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    raise ValueError("Task Session execution-entry validator is unavailable")


def load_projection_validator() -> Any:
    path = projection_validator_path()
    specification = importlib.util.spec_from_file_location("task_session_execution_entry_projection", path)
    if specification is None or specification.loader is None:
        raise ValueError("cannot load Task Session execution-entry validator")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def compile_projection(source: dict[str, Any], unit_id: str) -> dict[str, Any]:
    validator = load_projection_validator()
    validation = validator.validate_document(source)
    if validation["closure_result"] != "pass":
        raise ValueError("execution-entry closure invalid: " + "; ".join(validation["failures"]))
    units = [item for item in source["units"] if item.get("unit_id") == unit_id]
    if len(units) != 1:
        raise ValueError(f"expected one closed unit: {unit_id}")
    projection = units[0]["native_context_projection"]
    schema = load_object(SCHEMA)
    errors = sorted(Draft202012Validator(schema).iter_errors(projection), key=lambda item: list(item.absolute_path))
    if errors:
        raise ValueError("native projection schema invalid: " + errors[0].message)
    return projection


def machine_digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def human_view(projection: dict[str, Any]) -> str:
    contract = projection["execution_contract"]
    lines = [
        f"# Execution context: {projection['swu_id']}",
        "",
        f"Machine view digest: `{machine_digest(projection)}`",
        f"Task: `{projection['task_id']}`",
        f"Write profile: `{contract['writeProfile']}`",
        f"Lifecycle owner: `{contract['lifecycleOwner']}`",
        "",
        "This human view is derived from the schema-validated machine view and grants no authority.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--unit-id", required=True)
    parser.add_argument("--output")
    parser.add_argument("--human-output")
    args = parser.parse_args()
    projection = compile_projection(load_object(Path(args.source)), args.unit_id)
    rendered = json.dumps(projection, indent=2, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    if args.human_output:
        Path(args.human_output).write_text(human_view(projection), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
