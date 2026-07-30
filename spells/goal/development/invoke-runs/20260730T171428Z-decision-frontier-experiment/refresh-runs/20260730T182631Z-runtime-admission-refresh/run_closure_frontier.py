#!/usr/bin/env python3
"""Execute one output-only DFE closure unit with live admission."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


ARCANUM_ROOT = Path(__file__).resolve().parents[7]
INVOKE_RUN = Path(
    "spells/goal/development/invoke-runs/"
    "20260730T171428Z-decision-frontier-experiment"
)
CONTROL_ROOT = INVOKE_RUN / "execution-control"
EXPERIMENT_ROOT = Path(
    "spells/goal/development/decision-frontier-experiment"
)
MATRIX_PATH = INVOKE_RUN / "work-pack/shared/COMMAND-MATRIX.json"
WORK_PACK_PATH = INVOKE_RUN / "WORK-PACK.md"
TERMINAL_SCHEMA = INVOKE_RUN / "TASK-SESSION-RECEIPT.schema.json"
TERMINAL_VALIDATOR = (
    INVOKE_RUN / "work-pack/shared/validate-task-session-receipt.py"
)
REQUEST_SCHEMA = Path(
    "arcana/task-session/schemas/mutation-admission-request.schema.json"
)
RECEIPT_SCHEMA = Path(
    "arcana/task-session/schemas/mutation-admission-receipt.schema.json"
)
ADMISSION_CONSUMER = Path(
    "arcana/task-session/scripts/verify-mutation-readiness.py"
)
CONTINUITY_SCHEMA = Path("arcana/task-session/continuity.schema.json")
FIXED_TIME = "2026-07-30T18:26:31Z"


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def load_json(path: str | Path) -> dict[str, Any]:
    value = json.loads((ARCANUM_ROOT / path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value


def write_json(path: str | Path, value: Any) -> None:
    target = ARCANUM_ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def exact_ref(path: str | Path, *, camel: bool = False) -> dict[str, Any]:
    relative = str(path)
    content = (ARCANUM_ROOT / relative).read_bytes()
    size_key = "sizeBytes" if camel else "size_bytes"
    return {
        "path": relative,
        "sha256": hashlib.sha256(content).hexdigest(),
        size_key: len(content),
    }


def run(
    argv: list[str],
    *,
    cwd: Path = ARCANUM_ROOT,
    timeout: int = 120,
) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        timeout=timeout,
        check=False,
        capture_output=True,
        text=True,
    )


def schema_check(document: dict[str, Any], schema_path: Path) -> None:
    schema = load_json(schema_path)
    errors = sorted(
        Draft202012Validator(schema).iter_errors(document),
        key=lambda error: list(error.absolute_path),
    )
    if errors:
        raise RuntimeError(
            "; ".join(
                f"{'/'.join(map(str, error.absolute_path)) or '<root>'}: {error.message}"
                for error in errors
            )
        )


def dependency_paths(unit_id: str) -> list[tuple[str, Path]]:
    if unit_id == "VERIFY-DFE-001":
        return [
            (
                f"SWU-DFE-{index:03d}",
                EXPERIMENT_ROOT
                / "session-evidence"
                / f"SWU-DFE-{index:03d}"
                / "owner-receipt.json",
            )
            for index in range(1, 8)
        ]
    return [
        (
            "VERIFY-DFE-001",
            EXPERIMENT_ROOT
            / "session-evidence/VERIFY-DFE-001/closure-receipt.json",
        )
    ]


def build_context(unit: dict[str, Any], control_dir: Path) -> Path:
    unit_id = unit["unit_id"]
    context_path = control_dir / "CONTEXT-PACK.json"
    markdown_path = control_dir / "CONTEXT-PACK.md"
    index_path = control_dir / "CONTEXT-PACK.index.json"
    commands = [" ".join(spec["argv"]) for spec in unit["validation_commands"]]
    dependencies = [
        {"dependency_id": dependency_id, "artifact": exact_ref(path)}
        for dependency_id, path in dependency_paths(unit_id)
    ]
    for dependency in dependencies:
        document = load_json(dependency["artifact"]["path"])
        if unit_id == "VERIFY-DFE-001":
            if document.get("validation_result") != "pass":
                raise RuntimeError(f"blocked dependency: {dependency['dependency_id']}")
        elif document.get("status") != "pass":
            raise RuntimeError(f"blocked dependency: {dependency['dependency_id']}")
    document = {
        "schema_version": "context-builder.runtime-handoff.v1",
        "task_id": Path(unit["task_path"]).stem,
        "swu_id": unit_id,
        "session_id": f"dfe-{unit_id.lower()}-20260730",
        "mode": "lean",
        "handoff": "runtime",
        "strict_coverage": True,
        "obligations": [
            {"id": "dependency-receipts", "status": "covered"},
            {"id": "output-partition", "status": "covered"},
            {"id": "validation-command", "status": "covered"},
            {"id": "authority-ceiling", "status": "covered"},
            {"id": "lifecycle-route", "status": "covered"},
        ],
        "selected_sources": [
            exact_ref(unit["task_path"]),
            exact_ref(WORK_PACK_PATH),
            *[item["artifact"] for item in dependencies],
        ],
        "execution_contract": {
            "writeProfile": "execution-output-only",
            "materialWrites": [],
            "executionOutputs": unit["execution_outputs"],
            "allowedWrites": unit["allowed_writes"],
            "validationCommands": commands,
            "lifecycleOwner": "spellcraft",
            "authorityClass": "public",
            "publicationClass": "public",
        },
        "constraints": [
            "no material writes",
            "no canonical mutation",
            "no successor selection",
            "no promotion or publication",
        ],
        "dependencies": dependencies,
        "blockers": [],
        "provenance": {
            "captured_at": FIXED_TIME,
            "work_pack_sha256": exact_ref(WORK_PACK_PATH)["sha256"],
        },
        "output_paths": {
            "markdown": str(markdown_path),
            "json": str(context_path),
            "index": str(index_path),
        },
    }
    write_json(context_path, document)
    (ARCANUM_ROOT / markdown_path).write_text(
        "\n".join(
            [
                f"# Context Pack: {unit_id}",
                "",
                "- Mode: `lean`",
                "- Strict coverage: `pass`",
                "- Write profile: `execution-output-only`",
                f"- Dependencies: `{len(dependencies)}`",
                "- Authority effect: `none`",
                "",
                "The unit may write only its declared closure evidence and may "
                "not select or execute its successor.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    write_json(
        index_path,
        {
            "schema_version": "context-builder.runtime-index.v1",
            "task_id": document["task_id"],
            "swu_id": unit_id,
            "strict_coverage": True,
            "obligation_count": 5,
            "covered_count": 5,
            "context_pack": exact_ref(context_path),
            "markdown": exact_ref(markdown_path),
        },
    )
    return context_path


def admit(unit: dict[str, Any], context_path: Path, control_dir: Path) -> Path:
    controls = [
        {
            **exact_ref(unit["task_path"], camel=True),
            "role": "task-contract",
            "authorityClass": "public",
        },
        {
            **exact_ref(WORK_PACK_PATH, camel=True),
            "role": "work-pack",
            "authorityClass": "public",
        },
        {
            **exact_ref(context_path, camel=True),
            "role": "context-pack",
            "authorityClass": "public",
        },
    ]
    dependencies = [
        {
            "dependencyId": dependency_id,
            "artifactRef": exact_ref(path, camel=True),
        }
        for dependency_id, path in dependency_paths(unit["unit_id"])
    ]
    commands = [" ".join(spec["argv"]) for spec in unit["validation_commands"]]
    request = {
        "schemaVersion": "1.2.0",
        "executionMode": "reusable-mutation",
        "taskId": Path(unit["task_path"]).stem,
        "swuId": unit["unit_id"],
        "controlArtifacts": controls,
        "dependencyFrontier": dependencies,
        "materialWrites": [],
        "executionOutputs": unit["execution_outputs"],
        "allowedWrites": unit["allowed_writes"],
        "validationCommands": commands,
        "lifecycleOwner": "spellcraft",
        "authorityClass": "public",
        "publicationClass": "public",
    }
    request_path = control_dir / "mutation-admission-request.json"
    receipt_path = control_dir / "mutation-admission-receipt.json"
    write_json(request_path, request)
    result = run(
        [
            "python3",
            str(ADMISSION_CONSUMER),
            str(request_path),
            "--repository-root",
            ".",
            "--request-schema",
            str(REQUEST_SCHEMA),
            "--receipt-schema",
            str(RECEIPT_SCHEMA),
            "--output",
            str(receipt_path),
        ]
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"output-only admission blocked: {load_json(receipt_path)}"
        )
    receipt = load_json(receipt_path)
    if (
        receipt["admissionVerdict"] != "admit"
        or receipt["writeProfile"] != "execution-output-only"
        or receipt["mutationReady"] is not True
        or receipt["reasons"]
    ):
        raise RuntimeError(f"output-only admission invalid: {receipt}")
    return receipt_path


def run_verify(unit: dict[str, Any], control_dir: Path) -> dict[str, Any]:
    output = Path(unit["execution_outputs"][0])
    baseline_core = {
        "unit_id": unit["unit_id"],
        "selected_unit": unit["unit_id"],
        "output": {
            "path": str(output),
            "exists": (ARCANUM_ROOT / output).exists(),
        },
        "canonical_manifest": exact_ref(
            INVOKE_RUN / "DESIGN-SCOPE-MANIFEST.json"
        ),
        "owner_receipts": [
            exact_ref(path) for _, path in dependency_paths(unit["unit_id"])
        ],
    }
    write_json(
        control_dir / "closure-baseline.json",
        {**baseline_core, "baseline_digest": canonical_digest(baseline_core)},
    )
    spec = unit["validation_commands"][0]
    result = run(
        spec["argv"],
        cwd=ARCANUM_ROOT / spec["cwd"],
        timeout=spec["timeout_seconds"],
    )
    if result.returncode != spec["expected_exit_code"]:
        raise RuntimeError(f"closure command blocked: {result.stdout}{result.stderr}")
    authority = load_json(output)
    if authority.get("status") != "pass":
        raise RuntimeError(f"authority closure blocked: {authority}")
    artifact = exact_ref(output)
    terminal = {
        "schema_version": "task-session-terminal-receipt.v1",
        "unit_id": unit["unit_id"],
        "step_id": unit["dispatch_step"],
        "session_id": "dfe-verify-dfe-001-20260730",
        "status": "pass",
        "validation_result": "pass",
        "work_pack_sha256": exact_ref(WORK_PACK_PATH)["sha256"],
        "baseline_digest": canonical_digest(baseline_core),
        "artifacts": [{**artifact, "delta": "added"}],
        "validation": [
            {
                "argv": spec["argv"],
                "exit_code": result.returncode,
                "evidence_path": str(output),
            }
        ],
        "blockers": [],
        "material_writes": [],
        "execution_outputs": unit["execution_outputs"],
        "allowed_writes": unit["allowed_writes"],
        "undeclared_writes": [],
        "authority_effect": "none",
        "successor": {
            "unit_id": unit["successor"],
            "eligible": True,
            "selected": False,
        },
        "experiment_harness": "not_applicable",
    }
    receipt_path = Path(unit["terminal_receipt"])
    write_json(receipt_path, terminal)
    schema_check(terminal, TERMINAL_SCHEMA)
    semantic = run(
        [
            "python3",
            str(TERMINAL_VALIDATOR),
            str(receipt_path),
            "--schema",
            str(TERMINAL_SCHEMA),
            "--unit",
            unit["unit_id"],
            "--step",
            unit["dispatch_step"],
            "--work-pack-sha256",
            exact_ref(WORK_PACK_PATH)["sha256"],
            "--successor",
            unit["successor"],
        ]
    )
    if semantic.returncode != 0:
        raise RuntimeError(f"closure receipt invalid: {semantic.stdout}")
    return {
        "result": "PASS",
        "terminal_receipt": str(receipt_path),
        "successor": unit["successor"],
    }


def run_readiness(unit: dict[str, Any]) -> dict[str, Any]:
    spec = unit["validation_commands"][0]
    result = run(
        spec["argv"],
        cwd=ARCANUM_ROOT / spec["cwd"],
        timeout=spec["timeout_seconds"],
    )
    if result.returncode != spec["expected_exit_code"]:
        raise RuntimeError(
            f"lifecycle decision command blocked: {result.stdout}{result.stderr}"
        )
    decision_path = Path(unit["terminal_receipt"])
    decision = load_json(decision_path)
    expected = {
        "unit_id": unit["unit_id"],
        "status": "pass",
        "owner": "spellcraft",
        "decision": "authorize-paired-real-workflow-experiment-proposal",
        "promotion": False,
        "publication": False,
        "authority_effect": "none",
        "successor": None,
    }
    mismatches = {
        key: {"expected": value, "actual": decision.get(key)}
        for key, value in expected.items()
        if decision.get(key) != value
    }
    if mismatches:
        raise RuntimeError(f"lifecycle decision mismatch: {mismatches}")
    return {
        "result": "PASS",
        "terminal_receipt": str(decision_path),
        "successor": None,
    }


def update_continuity(unit: dict[str, Any], result: dict[str, Any]) -> None:
    successor = result["successor"]
    cursor = {
        "schema_version": "task-session.continuity.v1",
        "session_id": "goal-dfe-series",
        "updated_at": FIXED_TIME,
        "scope_root": str(EXPERIMENT_ROOT),
        "work_pack": str(WORK_PACK_PATH),
        "source_swu": unit["unit_id"],
        "source_result": "PASS",
        "source_receipt": result["terminal_receipt"],
        "closeout_owner_receipt": result["terminal_receipt"],
        "next_swu": successor,
        "next_route": (
            {
                "capability": "spellcraft",
                "mode": "lifecycle-decision",
                "target": successor,
                "work_pack": str(WORK_PACK_PATH),
                "swu": successor,
            }
            if successor
            else None
        ),
        "blocker_fingerprint": None,
    }
    schema_check(cursor, CONTINUITY_SCHEMA)
    write_json(CONTROL_ROOT / "continuity.json", cursor)
    state = load_json(CONTROL_ROOT / "CHAIN-STATE.json")
    completed = list(state["completed"])
    if unit["unit_id"] not in completed:
        completed.append(unit["unit_id"])
    state.update(
        {
            "completed": completed,
            "last_unit": unit["unit_id"],
            "last_result": "PASS",
            "next_unit": successor,
            "selected_next": False,
            "stop_reason": "complete" if successor is None else None,
        }
    )
    write_json(CONTROL_ROOT / "CHAIN-STATE.json", state)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--unit", choices=["VERIFY-DFE-001", "READINESS-DFE-001"], required=True
    )
    args = parser.parse_args()
    matrix = load_json(MATRIX_PATH)
    unit = {item["unit_id"]: item for item in matrix["units"]}[args.unit]
    control_dir = CONTROL_ROOT / args.unit
    context_path = build_context(unit, control_dir)
    admission = admit(unit, context_path, control_dir)
    result = (
        run_verify(unit, control_dir)
        if args.unit == "VERIFY-DFE-001"
        else run_readiness(unit)
    )
    update_continuity(unit, result)
    print(
        json.dumps(
            {
                "unit_id": args.unit,
                "result": result["result"],
                "context_pack": str(context_path),
                "mutation_admission": str(admission),
                "terminal_receipt": result["terminal_receipt"],
                "successor": result["successor"],
                "successor_selected": False,
                "authority_effect": "none",
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
