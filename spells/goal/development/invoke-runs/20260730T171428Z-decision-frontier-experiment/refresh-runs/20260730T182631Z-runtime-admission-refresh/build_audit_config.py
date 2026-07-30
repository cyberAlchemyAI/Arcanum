#!/usr/bin/env python3
"""Build the exact DFE work-pack readiness frontier."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[7]
INVOKE_RUN = Path(
    "spells/goal/development/invoke-runs/"
    "20260730T171428Z-decision-frontier-experiment"
)
REFRESH_RUN = INVOKE_RUN / "refresh-runs/20260730T182631Z-runtime-admission-refresh"
MATERIAL_ROOT = REFRESH_RUN / "material-packages"
OUTPUT = INVOKE_RUN / "readiness-runs/post-execution/AUDIT-CONFIG.json"


def exact_ref(path: str | Path) -> dict[str, object]:
    relative = str(path)
    content = (REPOSITORY_ROOT / relative).read_bytes()
    return {
        "path": relative,
        "sha256": hashlib.sha256(content).hexdigest(),
        "size_bytes": len(content),
    }


def main() -> int:
    matrix_path = INVOKE_RUN / "work-pack/shared/COMMAND-MATRIX.json"
    matrix = json.loads(
        (REPOSITORY_ROOT / matrix_path).read_text(encoding="utf-8")
    )
    work_pack_ref = exact_ref(INVOKE_RUN / "WORK-PACK.md")
    work_pack_sha256 = work_pack_ref["sha256"]
    units = []
    all_mutation_units = [f"SWU-DFE-{index:03d}" for index in range(1, 8)]
    by_id = {unit["unit_id"]: unit for unit in matrix["units"]}
    for item in matrix["units"]:
        unit_id = item["unit_id"]
        dependencies = item["dependencies"]
        if unit_id == "VERIFY-DFE-001":
            dependencies = all_mutation_units
        dependency_receipts = [
            {
                "dependency_id": dependency,
                "receipt_ref": exact_ref(by_id[dependency]["terminal_receipt"]),
                "expected_unit_id": dependency,
                "expected_step_id": by_id[dependency]["dispatch_step"],
                "expected_status": "pass",
                "work_pack_sha256": work_pack_sha256,
            }
            for dependency in dependencies
        ]
        material = None
        if item["material_writes"]:
            material = {
                "package_ref": exact_ref(
                    MATERIAL_ROOT / unit_id / "material-package.json"
                ),
                "receipt_ref": exact_ref(
                    MATERIAL_ROOT / unit_id / "material-receipt.json"
                ),
            }
        units.append(
            {
                "unit_id": unit_id,
                "task_class": item["task_class"],
                "state": "complete",
                "requested_execution_mode": item["requested_execution_mode"],
                "contract_kind": "full-task",
                "contract_ref": exact_ref(item["task_path"]),
                "dependencies": dependencies,
                "dependency_receipts": dependency_receipts,
                "successor": item["successor"],
                "dispatch_step": item["dispatch_step"],
                "material_writes": item["material_writes"],
                "execution_outputs": item["execution_outputs"],
                "allowed_writes": item["allowed_writes"],
                "validation_commands": item["validation_commands"],
                "attempt": item["attempt"],
                "material_package": material,
                "terminal_receipt": item["terminal_receipt"],
                "closeout_receipt": item["closeout_receipt"],
            }
        )

    control_paths = [
        INVOKE_RUN / "WORK-PACK.md",
        INVOKE_RUN / "EXECUTION-PACK.md",
        INVOKE_RUN / "SPELL-HANDOFF.md",
        INVOKE_RUN / "SPELLCRAFT-ADMISSION-RECEIPT.json",
        INVOKE_RUN / "work-pack/shared/CONTEXT.md",
        INVOKE_RUN / "work-pack/shared/CLOSEOUT-CONTRACT.md",
        matrix_path,
        INVOKE_RUN / "TASK-SESSION-RECEIPT.schema.json",
        INVOKE_RUN / "CLOSEOUT-RECEIPT.schema.json",
        INVOKE_RUN / "work-pack/shared/validate-task-session-receipt.py",
        INVOKE_RUN / "work-pack/shared/closeout_sync.py",
        INVOKE_RUN / "work-pack/shared/run_closure.py",
        INVOKE_RUN / "work-pack/shared/record_lifecycle_decision.py",
        *[
            INVOKE_RUN / f"work-pack/details/{name}.md"
            for name in ("CONTRACT", "REDUCER", "CLAIM", "RECONCILE", "BOUNDARY")
        ],
    ]
    continuation_path = INVOKE_RUN / "CONTINUATION.json"
    config = {
        "schema_version": "1.0.0",
        "audit_id": "goal-dfe-post-execution-20260730",
        "repository_root": ".",
        "authority_class": "public",
        "publication_class": "public",
        "work_pack": work_pack_ref,
        "control_artifacts": [exact_ref(path) for path in control_paths],
        "task_session_request_schema": exact_ref(
            "arcana/task-session/schemas/mutation-admission-request.schema.json"
        ),
        "terminal_receipt_schema": exact_ref(
            INVOKE_RUN / "TASK-SESSION-RECEIPT.schema.json"
        ),
        "terminal_receipt_semantic_validator": exact_ref(
            INVOKE_RUN / "work-pack/shared/validate-task-session-receipt.py"
        ),
        "units": units,
        "immutable_paths": [
            "spells/goal/README.md",
            "spells/goal/runtime/goal_loop.py",
            "spells/goal/schemas/frontier-snapshot.schema.json",
            "spells/invoke/README.md",
            "arcana/craft/SKILL.md",
            "arcana/craft/templates/schemas/ledger-core.schema.yml",
        ],
        "shared_write_owners": [],
        "source_selectors": [
            str(INVOKE_RUN / "SPEC.md"),
            str(INVOKE_RUN / "ARCHITECTURE.md"),
            str(INVOKE_RUN / "SPELLCRAFT-ADMISSION-RECEIPT.json"),
        ],
        "closeout_directory": {
            "path": "spells/goal/development/decision-frontier-experiment/session-evidence",
            "create_if_missing": True,
        },
        "handoff_state": {
            "artifact_ref": exact_ref(continuation_path),
            "expected_fields": {
                "state": "complete",
                "first_selectable_swu": None,
                "selected_swu": None,
                "selection_allowed": False,
                "next_route": "spellcraft:paired-real-workflow-experiment-proposal",
            },
        },
        "refresh_targets": [str(path) for path in control_paths],
        "next_owner": "invoke:refresh",
    }
    output = REPOSITORY_ROOT / OUTPUT
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(config, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "config": str(OUTPUT),
                "units": len(units),
                "work_pack_sha256": work_pack_sha256,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
