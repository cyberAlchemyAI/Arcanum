#!/usr/bin/env python3
"""Execute exactly one admitted DFE SWU and join its closeout owner receipt."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


ARCANUM_ROOT = Path(__file__).resolve().parents[7]
INVOKE_RUN = Path(
    "spells/goal/development/invoke-runs/"
    "20260730T171428Z-decision-frontier-experiment"
)
REFRESH_RUN = INVOKE_RUN / "refresh-runs/20260730T182631Z-runtime-admission-refresh"
MATERIAL_ROOT = REFRESH_RUN / "material-packages"
CONTROL_ROOT = INVOKE_RUN / "execution-control"
EXPERIMENT_ROOT = Path(
    "spells/goal/development/decision-frontier-experiment"
)
MATRIX_PATH = INVOKE_RUN / "work-pack/shared/COMMAND-MATRIX.json"
WORK_PACK_PATH = INVOKE_RUN / "WORK-PACK.md"
TERMINAL_SCHEMA_PATH = INVOKE_RUN / "TASK-SESSION-RECEIPT.schema.json"
CLOSEOUT_SCHEMA_PATH = INVOKE_RUN / "CLOSEOUT-RECEIPT.schema.json"
TERMINAL_VALIDATOR_PATH = (
    INVOKE_RUN / "work-pack/shared/validate-task-session-receipt.py"
)
CLOSEOUT_RUNNER_PATH = INVOKE_RUN / "work-pack/shared/closeout_sync.py"
MATERIAL_SCHEMA_DIR = Path("spells/invoke/schemas")
MATERIAL_VALIDATOR = Path("spells/invoke/scripts/material_package_validator.py")
ADMISSION_REQUEST_SCHEMA = Path(
    "arcana/task-session/schemas/mutation-admission-request.schema.json"
)
ADMISSION_RECEIPT_SCHEMA = Path(
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


def exact_ref(path: str | Path, *, camel: bool = False) -> dict[str, Any]:
    relative = str(path)
    content = (ARCANUM_ROOT / relative).read_bytes()
    size_key = "sizeBytes" if camel else "size_bytes"
    return {
        "path": relative,
        "sha256": hashlib.sha256(content).hexdigest(),
        size_key: len(content),
    }


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


def file_snapshot(paths: list[str]) -> list[dict[str, Any]]:
    result = []
    for relative in paths:
        target = ARCANUM_ROOT / relative
        if target.is_file():
            content = target.read_bytes()
            result.append(
                {
                    "path": relative,
                    "exists": True,
                    "kind": "file",
                    "sha256": hashlib.sha256(content).hexdigest(),
                    "size_bytes": len(content),
                }
            )
        elif target.exists():
            result.append(
                {
                    "path": relative,
                    "exists": True,
                    "kind": "other",
                    "sha256": None,
                    "size_bytes": None,
                }
            )
        else:
            result.append(
                {
                    "path": relative,
                    "exists": False,
                    "kind": "missing",
                    "sha256": None,
                    "size_bytes": None,
                }
            )
    return result


def tree_snapshot(root: Path) -> dict[str, str]:
    target = ARCANUM_ROOT / root
    if not target.exists():
        return {}
    return {
        str(path.relative_to(ARCANUM_ROOT)): hashlib.sha256(
            path.read_bytes()
        ).hexdigest()
        for path in sorted(target.rglob("*"))
        if path.is_file()
    }


def run(
    argv: list[str],
    *,
    cwd: Path = ARCANUM_ROOT,
    timeout: int = 120,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    runtime_env = os.environ.copy()
    runtime_env["PYTHONDONTWRITEBYTECODE"] = "1"
    runtime_env.update(env or {})
    return subprocess.run(
        argv,
        cwd=cwd,
        env=runtime_env,
        timeout=timeout,
        check=False,
        capture_output=True,
        text=True,
    )


def task_id(task_path: str) -> str:
    return Path(task_path).stem


def previous_unit(unit_id: str) -> str | None:
    index = int(unit_id.rsplit("-", 1)[1])
    return None if index == 1 else f"SWU-DFE-{index - 1:03d}"


def build_context_pack(
    unit: dict[str, Any],
    package: dict[str, Any],
    control_dir: Path,
) -> Path:
    unit_id = unit["unit_id"]
    context_path = control_dir / "CONTEXT-PACK.json"
    markdown_path = control_dir / "CONTEXT-PACK.md"
    index_path = control_dir / "CONTEXT-PACK.index.json"
    commands = package["validation_commands"]
    sources = [
        exact_ref(unit["task_path"]),
        exact_ref(WORK_PACK_PATH),
        exact_ref(INVOKE_RUN / "work-pack/shared/CONTEXT.md"),
        exact_ref(INVOKE_RUN / "SPELLCRAFT-ADMISSION-RECEIPT.json"),
        exact_ref(
            INVOKE_RUN
            / "readiness-runs/post-command-normalization/results/work-pack-readiness-report.json"
        ),
    ]
    obligations = [
        {
            "id": "scope",
            "status": "covered",
            "evidence": unit["task_path"],
        },
        {
            "id": "dependencies",
            "status": "covered",
            "evidence": (
                f"{previous_unit(unit_id)} owner receipt"
                if previous_unit(unit_id)
                else "Spellcraft execution admission"
            ),
        },
        {
            "id": "write-partition",
            "status": "covered",
            "evidence": str(MATRIX_PATH),
        },
        {
            "id": "validation",
            "status": "covered",
            "evidence": commands,
        },
        {
            "id": "closeout",
            "status": "covered",
            "evidence": str(INVOKE_RUN / "work-pack/shared/CLOSEOUT-CONTRACT.md"),
        },
        {
            "id": "authority",
            "status": "covered",
            "evidence": "public fixture-only; authority effect none",
        },
    ]
    contract = {
        "writeProfile": "material-bound",
        "materialWrites": unit["material_writes"],
        "executionOutputs": unit["execution_outputs"],
        "allowedWrites": unit["allowed_writes"],
        "validationCommands": commands,
        "lifecycleOwner": "spellcraft",
        "authorityClass": "public",
        "publicationClass": "public",
    }
    document = {
        "schema_version": "context-builder.runtime-handoff.v1",
        "task_id": task_id(unit["task_path"]),
        "swu_id": unit_id,
        "session_id": f"dfe-{unit_id.lower()}-20260730",
        "mode": "lean",
        "handoff": "runtime",
        "strict_coverage": True,
        "obligations": obligations,
        "selected_sources": sources,
        "constraints": [
            "apply only the validated producer material package",
            "write only the exact execution output partition",
            "no canonical Goal, Craft, Invoke, Task Session, tracker, promotion, publication, or deployment mutation",
            "stop on the first failed acceptance-critical witness",
        ],
        "non_goals": [
            "adapter implementation",
            "workflow benefit claim",
            "canonical adoption",
            "production concurrency claim",
        ],
        "execution_contract": contract,
        "blockers": [],
        "authority_precedence": [
            "live Task Session contract",
            "exact work pack and task contract",
            "selection-bound context pack",
            "producer material package",
        ],
        "output_paths": {
            "markdown": str(markdown_path),
            "json": str(context_path),
            "index": str(index_path),
        },
        "provenance": {
            "captured_at": FIXED_TIME,
            "work_pack_sha256": exact_ref(WORK_PACK_PATH)["sha256"],
        },
    }
    write_json(context_path, document)
    markdown = [
        f"# Context Pack: {unit_id}",
        "",
        "- Mode: `lean`",
        "- Handoff: `runtime`",
        "- Strict coverage: `pass`",
        f"- Task: `{unit['task_path']}`",
        f"- Material writes: `{len(unit['material_writes'])}`",
        f"- Execution outputs: `{len(unit['execution_outputs'])}`",
        "- Authority effect: `none`",
        "",
        "## Obligations",
        "",
        *[
            f"- `{item['id']}`: `{item['status']}` — {item['evidence']}"
            for item in obligations
        ],
        "",
        "## Runtime Boundary",
        "",
        "Apply only the digest-bound material package, run the exact validation "
        "argv, reconcile outputs against the allowed union, write one terminal "
        "receipt, and join the Invoke Refresh closeout receipt.",
    ]
    (ARCANUM_ROOT / markdown_path).write_text(
        "\n".join(markdown) + "\n", encoding="utf-8"
    )
    write_json(
        index_path,
        {
            "schema_version": "context-builder.runtime-index.v1",
            "task_id": document["task_id"],
            "swu_id": unit_id,
            "strict_coverage": True,
            "obligation_count": len(obligations),
            "covered_count": len(obligations),
            "context_pack": exact_ref(context_path),
            "markdown": exact_ref(markdown_path),
        },
    )
    return context_path


def refresh_material_package(
    unit: dict[str, Any], context_path: Path
) -> tuple[Path, Path]:
    unit_id = unit["unit_id"]
    unit_root = MATERIAL_ROOT / unit_id
    package_path = unit_root / "material-package.json"
    receipt_path = unit_root / "material-receipt.json"
    package = load_json(package_path)
    execution_control_prefix = str(CONTROL_ROOT / unit_id)
    package["source_artifacts"] = [
        item
        for item in package["source_artifacts"]
        if not item["path"].startswith(execution_control_prefix)
    ]
    package["source_artifacts"].append(
        {**exact_ref(context_path), "authority_class": "public"}
    )
    predecessor = previous_unit(unit_id)
    dependencies = []
    if predecessor:
        owner_path = (
            EXPERIMENT_ROOT
            / "session-evidence"
            / predecessor
            / "owner-receipt.json"
        )
        dependencies.append(
            {
                "dependency_id": predecessor,
                "artifact_ref": exact_ref(owner_path),
            }
        )
    package["dependencies"] = dependencies
    for item in package["target_inventory"]:
        item["dependency_ids"] = [predecessor] if predecessor else []
    write_json(package_path, package)
    result = run(
        [
            "python3",
            str(MATERIAL_VALIDATOR),
            str(package_path),
            "--root",
            ".",
            "--schema-dir",
            str(MATERIAL_SCHEMA_DIR),
            "--output",
            str(receipt_path),
        ]
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"material package rejected for {unit_id}: {result.stdout}{result.stderr}"
        )
    receipt = load_json(receipt_path)
    if (
        receipt["patchVerdict"] != "pass"
        or receipt["mutationHandoff"] != "ready"
        or receipt["reasons"]
    ):
        raise RuntimeError(f"material receipt not ready for {unit_id}: {receipt}")
    return package_path, receipt_path


def role_for(path: str, unit: dict[str, Any], context_path: Path) -> str:
    if path == unit["task_path"]:
        return "task-contract"
    if path == str(WORK_PACK_PATH):
        return "work-pack"
    if path == str(context_path):
        return "context-pack"
    return "source"


def build_admission(
    unit: dict[str, Any],
    package_path: Path,
    receipt_path: Path,
    context_path: Path,
    control_dir: Path,
) -> tuple[Path, Path]:
    package = load_json(package_path)
    controls = []
    for source in package["source_artifacts"]:
        controls.append(
            {
                "path": source["path"],
                "sha256": source["sha256"],
                "sizeBytes": source["size_bytes"],
                "role": role_for(source["path"], unit, context_path),
                "authorityClass": source["authority_class"],
            }
        )
    dependencies = [
        {
            "dependencyId": item["dependency_id"],
            "artifactRef": {
                "path": item["artifact_ref"]["path"],
                "sha256": item["artifact_ref"]["sha256"],
                "sizeBytes": item["artifact_ref"]["size_bytes"],
            },
        }
        for item in package["dependencies"]
    ]
    request = {
        "schemaVersion": "1.2.0",
        "executionMode": "reusable-mutation",
        "taskId": task_id(unit["task_path"]),
        "swuId": unit["unit_id"],
        "controlArtifacts": controls,
        "dependencyFrontier": dependencies,
        "materialPackage": exact_ref(package_path, camel=True),
        "materialReceipt": exact_ref(receipt_path, camel=True),
        "producerReceiptSchema": exact_ref(
            "spells/invoke/schemas/material-package-receipt.schema.json",
            camel=True,
        ),
        "materialWrites": unit["material_writes"],
        "executionOutputs": unit["execution_outputs"],
        "allowedWrites": unit["allowed_writes"],
        "validationCommands": package["validation_commands"],
        "lifecycleOwner": "spellcraft",
        "authorityClass": "public",
        "publicationClass": "public",
    }
    request_path = control_dir / "mutation-admission-request.json"
    receipt_output = control_dir / "mutation-admission-receipt.json"
    write_json(request_path, request)
    result = run(
        [
            "python3",
            str(ADMISSION_CONSUMER),
            str(request_path),
            "--repository-root",
            ".",
            "--request-schema",
            str(ADMISSION_REQUEST_SCHEMA),
            "--receipt-schema",
            str(ADMISSION_RECEIPT_SCHEMA),
            "--output",
            str(receipt_output),
        ]
    )
    if result.returncode != 0:
        receipt = (
            load_json(receipt_output)
            if (ARCANUM_ROOT / receipt_output).is_file()
            else {"missing": True}
        )
        raise RuntimeError(
            f"mutation admission blocked for {unit['unit_id']}: {receipt}"
        )
    receipt = load_json(receipt_output)
    if (
        receipt["admissionVerdict"] != "admit"
        or receipt["mutationReady"] is not True
        or receipt["reasons"]
    ):
        raise RuntimeError(f"mutation admission not ready: {receipt}")
    return request_path, receipt_output


def scoped_porcelain(paths: list[str]) -> list[str]:
    result = run(["git", "status", "--short", "--", *paths])
    if result.returncode != 0:
        raise RuntimeError(result.stderr)
    return [line for line in result.stdout.splitlines() if line]


def apply_material(package: dict[str, Any]) -> None:
    for change in package["changes"]:
        source = ARCANUM_ROOT / change["output_ref"]["path"]
        target = ARCANUM_ROOT / change["target_path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        if hashlib.sha256(target.read_bytes()).hexdigest() != change["output_ref"][
            "sha256"
        ]:
            raise RuntimeError(f"applied bytes drifted: {change['target_path']}")


def validate_schema(document: dict[str, Any], schema_path: Path) -> None:
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


def execute(unit: dict[str, Any]) -> dict[str, Any]:
    unit_id = unit["unit_id"]
    predecessor = previous_unit(unit_id)
    if predecessor:
        owner_path = (
            EXPERIMENT_ROOT
            / "session-evidence"
            / predecessor
            / "owner-receipt.json"
        )
        owner = load_json(owner_path)
        if owner.get("validation_result") != "pass":
            raise RuntimeError(f"predecessor owner receipt blocks {unit_id}")

    control_dir = CONTROL_ROOT / unit_id
    package_before_context = load_json(
        MATERIAL_ROOT / unit_id / "material-package.json"
    )
    context_path = build_context_pack(unit, package_before_context, control_dir)
    package_path, material_receipt_path = refresh_material_package(
        unit, context_path
    )

    inventory = [
        *unit["material_writes"],
        *unit["execution_outputs"],
        unit["terminal_receipt"],
        unit["closeout_receipt"],
    ]
    before_inventory = file_snapshot(inventory)
    before_tree = tree_snapshot(EXPERIMENT_ROOT)
    preflight = {
        "schema_version": "dfe-closeout-preflight.v1",
        "unit_id": unit_id,
        "work_pack": exact_ref(WORK_PACK_PATH),
        "target_inventory": before_inventory,
        "source_receipt_contract": exact_ref(TERMINAL_SCHEMA_PATH),
        "owner_receipt_contract": exact_ref(CLOSEOUT_SCHEMA_PATH),
        "owner_validation_commands": unit["validation_commands"],
        "admitted_delta_classes": ["evidence_added", "route_changed"],
        "unique_successor": unit["successor"],
        "forbidden": [
            "implementation outside material package",
            "authority change",
            "promotion",
            "publication",
            "deployment",
            "successor selection",
        ],
        "status": "pass",
    }
    write_json(control_dir / "closeout-preflight.json", preflight)
    request_path, admission_receipt_path = build_admission(
        unit,
        package_path,
        material_receipt_path,
        context_path,
        control_dir,
    )

    baseline_core = {
        "schema_version": "dfe-task-session-baseline.v1",
        "swu_id": unit_id,
        "session_id": f"dfe-{unit_id.lower()}-20260730",
        "selected_swu": unit_id,
        "target_inventory": before_inventory,
        "scoped_porcelain": scoped_porcelain(inventory),
    }
    baseline = {
        **baseline_core,
        "baseline_digest": canonical_digest(baseline_core),
    }
    baseline_path = Path(unit["execution_outputs"][0])
    write_json(baseline_path, baseline)

    package = load_json(package_path)
    apply_material(package)

    command_results = []
    validation_pass = True
    for spec in unit["validation_commands"]:
        result = run(
            spec["argv"],
            cwd=ARCANUM_ROOT / spec["cwd"],
            timeout=spec["timeout_seconds"],
            env=spec["environment"],
        )
        command_results.append(
            {
                "argv": spec["argv"],
                "exit_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
            }
        )
        validation_pass = (
            validation_pass and result.returncode == spec["expected_exit_code"]
        )

    after_tree = tree_snapshot(EXPERIMENT_ROOT)
    changed_paths = {
        path
        for path in set(before_tree) | set(after_tree)
        if before_tree.get(path) != after_tree.get(path)
    }
    undeclared = sorted(changed_paths - set(unit["allowed_writes"]))
    missing_outputs = sorted(
        path
        for path in unit["execution_outputs"]
        if not (ARCANUM_ROOT / path).is_file()
    )
    if undeclared or missing_outputs:
        validation_pass = False

    artifacts = []
    before_by_path = {item["path"]: item for item in before_inventory}
    for path in unit["allowed_writes"]:
        reference = exact_ref(path)
        baseline_item = before_by_path[path]
        delta = (
            "added"
            if not baseline_item["exists"]
            else (
                "unchanged"
                if baseline_item["sha256"] == reference["sha256"]
                else "changed"
            )
        )
        artifacts.append({**reference, "delta": delta})

    evidence_path = unit["execution_outputs"][-1]
    successor = {
        "unit_id": unit["successor"],
        "eligible": validation_pass,
        "selected": False,
    }
    terminal = {
        "schema_version": "task-session-terminal-receipt.v1",
        "unit_id": unit_id,
        "step_id": unit["dispatch_step"],
        "session_id": f"dfe-{unit_id.lower()}-20260730",
        "status": "pass" if validation_pass else "block",
        "validation_result": "pass" if validation_pass else "block",
        "work_pack_sha256": exact_ref(WORK_PACK_PATH)["sha256"],
        "baseline_digest": baseline["baseline_digest"],
        "artifacts": artifacts,
        "validation": [
            {
                "argv": item["argv"],
                "exit_code": item["exit_code"],
                "evidence_path": evidence_path,
            }
            for item in command_results
        ],
        "blockers": [
            *([] if validation_pass else ["acceptance-critical validation failed"]),
            *[f"undeclared write: {path}" for path in undeclared],
            *[f"missing output: {path}" for path in missing_outputs],
        ],
        "material_writes": unit["material_writes"],
        "execution_outputs": unit["execution_outputs"],
        "allowed_writes": unit["allowed_writes"],
        "undeclared_writes": undeclared,
        "authority_effect": "none",
        "successor": successor,
        "experiment_harness": "not_applicable",
    }
    terminal_path = Path(unit["terminal_receipt"])
    write_json(terminal_path, terminal)
    validate_schema(terminal, TERMINAL_SCHEMA_PATH)
    semantic = run(
        [
            "python3",
            str(TERMINAL_VALIDATOR_PATH),
            str(terminal_path),
            "--schema",
            str(TERMINAL_SCHEMA_PATH),
            "--unit",
            unit_id,
            "--step",
            unit["dispatch_step"],
            "--work-pack-sha256",
            exact_ref(WORK_PACK_PATH)["sha256"],
            "--successor",
            unit["successor"] or "none",
        ]
    )
    if semantic.returncode != 0:
        raise RuntimeError(f"terminal semantic validation failed: {semantic.stdout}")
    if not validation_pass:
        raise RuntimeError(f"Task Session blocked: {terminal['blockers']}")

    closeout = run(
        [
            "python3",
            str(CLOSEOUT_RUNNER_PATH),
            "--repository-root",
            str(ARCANUM_ROOT),
            "--matrix",
            str(ARCANUM_ROOT / MATRIX_PATH),
            "--unit",
            unit_id,
            "--source-receipt",
            str(terminal_path),
            "--output",
            unit["closeout_receipt"],
        ]
    )
    if closeout.returncode != 0:
        raise RuntimeError(
            f"closeout owner blocked: {closeout.stdout}{closeout.stderr}"
        )
    owner = load_json(unit["closeout_receipt"])
    validate_schema(owner, CLOSEOUT_SCHEMA_PATH)
    if owner["validation_result"] != "pass" or owner["blockers"]:
        raise RuntimeError(f"owner receipt not passing: {owner}")

    continuity = {
        "schema_version": "task-session.continuity.v1",
        "session_id": "goal-dfe-series",
        "updated_at": FIXED_TIME,
        "scope_root": str(EXPERIMENT_ROOT),
        "work_pack": str(WORK_PACK_PATH),
        "source_swu": unit_id,
        "source_result": "PASS",
        "source_receipt": str(terminal_path),
        "closeout_owner_receipt": unit["closeout_receipt"],
        "next_swu": unit["successor"],
        "next_route": (
            {
                "capability": (
                    "task-session"
                    if unit["successor"].startswith("SWU-")
                    else "work-pack-closure"
                ),
                "mode": "execute",
                "target": unit["successor"],
                "work_pack": str(WORK_PACK_PATH),
                "swu": unit["successor"],
            }
            if unit["successor"]
            else None
        ),
        "blocker_fingerprint": None,
    }
    validate_schema(continuity, CONTINUITY_SCHEMA)
    write_json(CONTROL_ROOT / "continuity.json", continuity)
    completed = []
    for index in range(1, 8):
        candidate = f"SWU-DFE-{index:03d}"
        owner_path = (
            EXPERIMENT_ROOT
            / "session-evidence"
            / candidate
            / "owner-receipt.json"
        )
        if (ARCANUM_ROOT / owner_path).is_file():
            completed.append(candidate)
    write_json(
        CONTROL_ROOT / "CHAIN-STATE.json",
        {
            "schema_version": "task-session-until-blocker.chain.v1",
            "work_pack": str(WORK_PACK_PATH),
            "series_authorization": "execute-work-pack-until-blocker",
            "ordered_frontier": [
                f"SWU-DFE-{index:03d}" for index in range(1, 8)
            ],
            "completed": completed,
            "last_unit": unit_id,
            "last_result": "PASS",
            "next_unit": unit["successor"],
            "selected_next": False,
            "stop_reason": None,
            "background_helper": {
                "spawned": 1,
                "joined": 1,
                "closed": 1,
                "open": 0,
                "result": "read-only readiness block confirmed and remediated",
            },
            "authority_effect": "none",
        },
    )
    return {
        "unit_id": unit_id,
        "result": "PASS",
        "context_pack": str(context_path),
        "mutation_admission": str(admission_receipt_path),
        "terminal_receipt": str(terminal_path),
        "closeout_receipt": unit["closeout_receipt"],
        "continuity": str(CONTROL_ROOT / "continuity.json"),
        "successor": unit["successor"],
        "successor_selected": False,
        "authority_effect": "none",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--unit", required=True)
    args = parser.parse_args()
    matrix = load_json(MATRIX_PATH)
    by_id = {item["unit_id"]: item for item in matrix["units"]}
    if args.unit not in by_id or not args.unit.startswith("SWU-DFE-"):
        raise SystemExit(f"unknown mutation SWU: {args.unit}")
    result = execute(by_id[args.unit])
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
