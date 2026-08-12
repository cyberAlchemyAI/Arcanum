#!/usr/bin/env python3
"""Temporary-fixture regression coverage for the split-receipt controller."""

from __future__ import annotations

import importlib.util
import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path
from typing import Any


CONTROLLER_PATH = (
    Path(__file__).resolve().parents[1] / "scripts/plan-once-material-controller.py"
)
SPEC = importlib.util.spec_from_file_location("plan_once_material_controller", CONTROLLER_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("candidate controller cannot be imported")
controller = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(controller)
INVOKE_SCHEMA_ENV = "UEV_INVOKE_CANDIDATE_SCHEMA"
INVOKE_SCHEMA_RELATIVE = (
    "arcanum/spells/invoke/schemas/"
    "precloseout-refresh-closeout-receipt.schema.json"
)
PRE_SCHEMA_RELATIVE = (
    "arcanum/arcana/task-session/schemas/"
    "precloseout-execution-receipt.schema.json"
)
PRE_RECEIPT_RELATIVE = (
    "arcanum/arcana/ux-evidence-validator/development/work-packs/"
    "uev-deterministic-kernel/results/"
    "SWU-UEV-001-PRECLOSEOUT-EXECUTION-RECEIPT.json"
)
CLOSEOUT_RECEIPT_RELATIVE = (
    "arcanum/arcana/ux-evidence-validator/development/work-packs/"
    "uev-deterministic-kernel/closeout/SWU-UEV-001-REFRESH-RECEIPT.json"
)
TERMINAL_RECEIPT_RELATIVE = (
    "arcanum/arcana/ux-evidence-validator/development/work-packs/"
    "uev-deterministic-kernel/results/SWU-UEV-001-RESULT.json"
)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class PlanOnceMaterialControllerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="task-session-precloseout-fixture-")
        self.root = Path(self.temporary.name)
        (self.root / controller.MARKER).write_bytes(controller.MARKER_BYTES)
        self.run = self.root / "run"
        self.run.mkdir()
        self.run_rel = "run"
        self.token = "a" * 64
        self.attempt = "attempt-fixture-001"
        self.identity = {
            "run_id": "run-fixture-001",
            "task_id": "TASK-FIXTURE-001",
            "swu_id": "SWU-FIXTURE-001",
        }
        self.idempotency_key = "run-fixture-001:invoke-closeout"
        self._write_base()

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def ref(self, relative: str) -> dict[str, Any]:
        return controller.exact_ref(self.root, self.root / relative)

    def artifact(self, relative: str, value: Any) -> None:
        write_json(self.root / relative, value)

    def copy_artifact(self, relative: str, source: Path) -> None:
        target = self.root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)

    def _write_base(self) -> None:
        self.artifact("run/request.json", dict(self.identity))
        self.artifact("run/ticket.json", dict(self.identity))
        self.artifact("run/executor.json", dict(self.identity))
        self.artifact(
            "run/admission.json",
            {"admissionToken": self.token, "attemptId": self.attempt},
        )
        for relative in (
            "run/material-commit.json",
            "run/reconciliation.json",
            "run/validation.json",
            "run/target-inventory.json",
            "run/target-result-inventory.json",
            "run/output.json",
            "run/closeout-target-inventory.json",
            "run/evidence/source-precloseout.json",
            "run/evidence/material-reconciliation.json",
            "run/evidence/target-validation.json",
        ):
            self.artifact(relative, {"fixture": relative})
        task_session_root = Path(__file__).resolve().parents[1]
        self.copy_artifact(
            PRE_SCHEMA_RELATIVE,
            task_session_root / "schemas/precloseout-execution-receipt.schema.json",
        )
        self.copy_artifact(
            "arcanum/arcana/task-session/schemas/governance-terminal-receipt.schema.json",
            task_session_root / "schemas/governance-terminal-receipt.schema.json",
        )
        owner_schema = Path(os.environ.get(INVOKE_SCHEMA_ENV, ""))
        if not owner_schema.is_file():
            raise RuntimeError(
                f"{INVOKE_SCHEMA_ENV} must name the proposed Invoke owner schema"
            )
        self.copy_artifact(INVOKE_SCHEMA_RELATIVE, owner_schema)
        self.protocol = {
            "schema_version": "task-session.plan-once-material-controller-fixture.v1",
            "receipt_profile": controller.PROFILE,
            **self.identity,
            "attempt_id": self.attempt,
            "idempotency_key": self.idempotency_key,
            "admission_token": self.token,
            "admission_receipt_ref": self.ref("run/admission.json"),
            "ticket_ref": self.ref("run/ticket.json"),
            "executor_receipt_path": "run/executor.json",
            "precloseout_receipt_path": PRE_RECEIPT_RELATIVE,
            "invoke_receipt_path": CLOSEOUT_RECEIPT_RELATIVE,
            "terminal_receipt_path": TERMINAL_RECEIPT_RELATIVE,
            "validation_contract_digest": "b" * 64,
            "successor_policy": "emit-cursor-never-execute-successor",
        }
        self.artifact("run/protocol.json", self.protocol)

    def consume_once(self) -> dict[str, Any]:
        return controller.resume(self.root, self.run_rel)

    def ledger(self) -> Path:
        return controller.ledger_path(
            self.root, self.run, self.protocol["admission_receipt_ref"]
        )

    def write_precloseout(self) -> None:
        ledger = self.ledger()
        self.assertTrue(ledger.is_file(), "consume before creating the receipt")
        closeout = {
            "route": "invoke:refresh:apply-approved",
            "owner_capability": "invoke",
            "source_receipt_path": PRE_RECEIPT_RELATIVE,
            "source_schema_ref": self.ref(PRE_SCHEMA_RELATIVE),
            "target_inventory_ref": self.ref("run/closeout-target-inventory.json"),
            "expected_owner_receipt_path": CLOSEOUT_RECEIPT_RELATIVE,
            "expected_owner_receipt_schema_ref": self.ref(INVOKE_SCHEMA_RELATIVE),
            "final_terminal_receipt_path": TERMINAL_RECEIPT_RELATIVE,
            "final_terminal_schema_ref": self.ref(
                "arcanum/arcana/task-session/schemas/governance-terminal-receipt.schema.json"
            ),
            "allowed_delta_classes": ["evidence_added"],
            "continuation_policy": "emit-cursor-never-execute-successor",
        }
        self.precloseout = {
            "schema_version": "task-session.precloseout-execution-receipt.v1",
            "receipt_id": "precloseout-fixture-001",
            **self.identity,
            "request_ref": self.ref("run/request.json"),
            "ticket_ref": self.ref("run/ticket.json"),
            "executor_receipt_ref": self.ref("run/executor.json"),
            "consumed_admission": {
                "receipt_ref": self.protocol["admission_receipt_ref"],
                "admission_token": self.token,
                "attempt_id": self.attempt,
                "consumption_ledger_ref": controller.exact_ref(self.root, ledger),
            },
            "material_commit_ref": self.ref("run/material-commit.json"),
            "reconciliation_ref": self.ref("run/reconciliation.json"),
            "validation_receipt_ref": self.ref("run/validation.json"),
            "validation_contract_digest": self.protocol["validation_contract_digest"],
            "target_inventory_ref": self.ref("run/target-inventory.json"),
            "target_result_inventory_ref": self.ref("run/target-result-inventory.json"),
            "output_refs": [self.ref("run/output.json")],
            "closeout_contract": closeout,
            "claim_state": "execution-validated-closeout-pending",
            "owner_identity": {"capability": "task-session", "subject": "fixture-controller"},
            "idempotency_key": "run-fixture-001:precloseout",
            "result": "pass",
            "residue": [],
        }
        self.artifact(PRE_RECEIPT_RELATIVE, self.precloseout)

    def write_invoke(self, *, wrong_source: bool = False, wrong_owner: bool = False) -> None:
        source_ref = (
            self.ref("run/executor.json")
            if wrong_source
            else self.ref(PRE_RECEIPT_RELATIVE)
        )
        closeout_output = {
            "path": CLOSEOUT_RECEIPT_RELATIVE,
        }
        receipt = {
                "schema_version": "invoke.precloseout-refresh-closeout-receipt.v1",
                "receipt_id": "INVOKE-FIXTURE-001",
                "owner_identity": {
                    "capability": "continuation-router" if wrong_owner else "invoke",
                    "mode": "refresh",
                    "mutation_mode": "apply-approved",
                    "activation_source": "delegated",
                    "subject": "invoke:refresh:apply-approved",
                },
                "task_identity": {
                    "task_id": self.identity["task_id"],
                    "run_id": self.identity["run_id"],
                    "swu_id": self.identity["swu_id"],
                    "attempt_id": self.attempt,
                    "idempotency_key": self.idempotency_key,
                },
                "precloseout_source": {
                    "receipt_ref": source_ref,
                    "schema_ref": self.precloseout["closeout_contract"]["source_schema_ref"],
                    "task_identity": {
                        "task_id": self.identity["task_id"],
                        "run_id": self.identity["run_id"],
                        "swu_id": self.identity["swu_id"],
                        "attempt_id": self.attempt,
                        "idempotency_key": self.idempotency_key,
                    },
                },
                "closeout_output": closeout_output,
                "validation_inventory": [
                    {
                        "validation_id": "source-precloseout",
                        "kind": "source-precloseout",
                        "result": "pass",
                        "evidence_ref": self.ref("run/evidence/source-precloseout.json"),
                    },
                    {
                        "validation_id": "material-reconciliation",
                        "kind": "material-reconciliation",
                        "result": "pass",
                        "evidence_ref": self.ref("run/evidence/material-reconciliation.json"),
                    },
                    {
                        "validation_id": "target-validation",
                        "kind": "target-validation",
                        "result": "pass",
                        "evidence_ref": self.ref("run/evidence/target-validation.json"),
                    },
                ],
                "result": "pass",
                "final_owner_write": {
                    "write_class": "invoke-closeout-receipt",
                    "owner_capability": "invoke",
                    "completed": True,
                    "output_ref": closeout_output,
                },
                "receipt_digest": "0" * 64,
        }
        receipt["receipt_digest"] = controller.invoke_receipt_projection_digest(receipt)
        self.artifact(CLOSEOUT_RECEIPT_RELATIVE, receipt)

    def write_terminal(self, *, executor_substitution: bool = False) -> None:
        precloseout_ref = (
            self.ref("run/executor.json")
            if executor_substitution
            else self.ref(PRE_RECEIPT_RELATIVE)
        )
        self.artifact(
            TERMINAL_RECEIPT_RELATIVE,
            {
                **self.identity,
                "receipt_profile": controller.PROFILE,
                "precloseout_execution_receipt_ref": precloseout_ref,
                "precloseout_execution_schema_ref": self.precloseout["closeout_contract"]["source_schema_ref"],
                "closeout_join": {
                    "required_owner_capabilities": ["invoke"],
                    "joined_owner_receipts": [
                        {
                            "owner_capability": "invoke",
                            "receipt_ref": self.ref(CLOSEOUT_RECEIPT_RELATIVE),
                            "result": "pass",
                        }
                    ],
                    "continuation": {
                        "policy": "emit-cursor-never-execute-successor",
                        "cursor_ref": None,
                        "successor_executed": False,
                    },
                },
            },
        )

    def test_restart_is_byte_stable_and_never_executes_successor(self) -> None:
        first = self.consume_once()
        self.assertEqual(first["next_action"], "await-precloseout-receipt")
        self.write_precloseout()
        second = self.consume_once()
        self.assertEqual(second["next_action"], "await-invoke-closeout")
        self.write_invoke()
        third = self.consume_once()
        self.assertEqual(third["next_action"], "await-final-terminal")
        self.write_terminal()
        fourth = self.consume_once()
        self.assertEqual(fourth["next_action"], "terminal-validated-selection-eligible")
        self.assertFalse(fourth["successor_executed"])
        ledger_bytes = self.ledger().read_bytes()
        state_path = self.run / "controller-state.json"
        state_bytes = state_path.read_bytes()
        fifth = self.consume_once()
        self.assertEqual(fifth["consumption"], "already-consumed-same-contract")
        self.assertEqual(self.ledger().read_bytes(), ledger_bytes)
        self.assertEqual(state_path.read_bytes(), state_bytes)
        self.assertFalse((self.run / "successor-executed.json").exists())

    def test_executor_cannot_substitute_for_precloseout(self) -> None:
        self.consume_once()
        self.write_precloseout()
        self.write_invoke()
        self.write_terminal(executor_substitution=True)
        with self.assertRaisesRegex(controller.ControllerBlock, "precloseout identity drift"):
            self.consume_once()

    def test_wrong_invoke_source_blocks_before_terminal(self) -> None:
        self.consume_once()
        self.write_precloseout()
        self.write_invoke(wrong_source=True)
        with self.assertRaisesRegex(controller.ControllerBlock, "fails its exact owner schema|source is not"):
            self.consume_once()

    def test_wrong_invoke_owner_blocks(self) -> None:
        self.consume_once()
        self.write_precloseout()
        self.write_invoke(wrong_owner=True)
        with self.assertRaisesRegex(controller.ControllerBlock, "fails its exact owner schema"):
            self.consume_once()

    def test_missing_exact_invoke_schema_blocks(self) -> None:
        self.consume_once()
        self.write_precloseout()
        self.write_invoke()
        (self.root / INVOKE_SCHEMA_RELATIVE).unlink()
        with self.assertRaisesRegex(controller.ControllerBlock, "Invoke receipt schema is missing"):
            self.consume_once()

    def test_invoke_projection_digest_drift_blocks(self) -> None:
        self.consume_once()
        self.write_precloseout()
        self.write_invoke()
        receipt = json.loads(
            (self.root / CLOSEOUT_RECEIPT_RELATIVE).read_text(encoding="utf-8")
        )
        receipt["receipt_digest"] = "0" * 64
        self.artifact(CLOSEOUT_RECEIPT_RELATIVE, receipt)
        with self.assertRaisesRegex(controller.ControllerBlock, "digest does not match canonical projection"):
            self.consume_once()

    def test_forged_consumption_ledger_blocks(self) -> None:
        self.consume_once()
        self.artifact("run/.admission-consumption/%s.json" % self.protocol["admission_receipt_ref"]["sha256"], {"forged": True})
        with self.assertRaisesRegex(controller.ControllerBlock, "already consumed by a different contract"):
            self.consume_once()

    def test_reconciliation_drift_blocks(self) -> None:
        self.consume_once()
        self.write_precloseout()
        self.artifact("run/reconciliation.json", {"tampered": True})
        with self.assertRaisesRegex(controller.ControllerBlock, "reconciliation_ref exact identity drift"):
            self.consume_once()

    def test_marker_is_required(self) -> None:
        self.temporary.cleanup()
        with tempfile.TemporaryDirectory(prefix="task-session-precloseout-fixture-") as raw:
            root = Path(raw)
            with self.assertRaisesRegex(controller.ControllerBlock, "marker"):
                controller.resume(root, "run")


if __name__ == "__main__":
    unittest.main(verbosity=2)
