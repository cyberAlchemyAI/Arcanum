#!/usr/bin/env python3
"""Adversarial validation fixtures for work-pack-readiness-audit."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from jsonschema import Draft202012Validator


SPELL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = SPELL_ROOT / "scripts" / "audit_work_pack.py"
SPEC = importlib.util.spec_from_file_location("audit_work_pack", SCRIPT_PATH)
assert SPEC is not None and SPEC.loader is not None
AUDIT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUDIT)


def exact_ref(root: Path, relative_path: str) -> dict[str, object]:
    content = (root / relative_path).read_bytes()
    return {
        "path": relative_path,
        "sha256": hashlib.sha256(content).hexdigest(),
        "size_bytes": len(content),
    }


def command(cwd: str = "workspace") -> dict[str, object]:
    return {
        "cwd": cwd,
        "argv": ["python3", "-c", "pass"],
        "expected_exit_code": 0,
        "timeout_seconds": 30,
        "environment": {},
        "runtime_identity": {
            "executable": "python3",
            "version_policy": "Python 3.x captured at Task Session preflight",
            "hash_policy": "resolve and hash executable at Task Session preflight",
        },
        "risk_class": "read-only",
    }


def attempt(required: bool = False) -> dict[str, object]:
    teardown = [command()] if required else []
    return {
        "required": required,
        "id_algorithm": "UTC-basic + source digest prefix" if required else "",
        "collision_policy": "fail-if-exists",
        "retention_policy": "retain-receipt-only",
        "teardown_on_success": teardown,
        "teardown_on_failure": teardown,
    }


def strong_receipt_schema() -> dict[str, object]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "additionalProperties": False,
        "required": [
            "unit_id",
            "step_id",
            "status",
            "artifacts",
            "validation",
            "validation_result",
            "blockers",
        ],
        "properties": {
            "unit_id": {"type": "string"},
            "step_id": {"type": "string"},
            "status": {"enum": ["pass", "block"]},
            "artifacts": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["path", "sha256"],
                    "properties": {
                        "path": {"type": "string"},
                        "sha256": {
                            "type": "string",
                            "pattern": "^[a-f0-9]{64}$",
                        },
                    },
                },
            },
            "validation": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["argv", "exit_code"],
                    "properties": {
                        "argv": {"type": "array", "minItems": 1},
                        "exit_code": {"type": "integer"},
                    },
                },
            },
            "validation_result": {"enum": ["pass", "block", "not-run"]},
            "blockers": {"type": "array", "items": {"type": "string"}},
        },
        "allOf": [
            {
                "if": {
                    "properties": {"status": {"const": "pass"}},
                    "required": ["status"],
                },
                "then": {
                    "properties": {
                        "validation_result": {"const": "pass"},
                        "blockers": {"maxItems": 0},
                        "artifacts": {"minItems": 1},
                        "validation": {"minItems": 1},
                    }
                },
            }
        ],
    }


class FixtureRepository:
    def __init__(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / ".git").mkdir()
        (self.root / "workspace").mkdir()
        (self.root / "plans").mkdir()
        (self.root / "schemas").mkdir()
        (self.root / "validators").mkdir()
        (self.root / "plans" / "WORK-PACK.md").write_text(
            "# Synthetic Work Pack\n\nUNIT-A\n", encoding="utf-8"
        )
        (self.root / "plans" / "TASKS.md").write_text(
            "# Tasks\n\n## UNIT-A\n\nRead-only validation.\n", encoding="utf-8"
        )
        (self.root / "plans" / "CONTINUATION.json").write_text(
            json.dumps(
                {
                    "state": "audit-ready",
                    "selected_unit": None,
                    "selection_allowed": False,
                }
            ),
            encoding="utf-8",
        )
        request_schema = {
            "type": "object",
            "properties": {
                "executionMode": {
                    "enum": [
                        "routed-mutation",
                        "reusable-mutation",
                        "standalone-nonmutating",
                    ]
                }
            },
        }
        (self.root / "schemas" / "task-session-request.json").write_text(
            json.dumps(request_schema), encoding="utf-8"
        )
        (self.root / "schemas" / "terminal-receipt.json").write_text(
            json.dumps(strong_receipt_schema()), encoding="utf-8"
        )
        (self.root / "validators" / "validate-receipt.py").write_text(
            "# synthetic semantic validator\n", encoding="utf-8"
        )

    def close(self) -> None:
        self.temp.cleanup()

    def base_unit(self) -> dict[str, object]:
        return {
            "unit_id": "UNIT-A",
            "task_class": "read-only-validation",
            "state": "planned",
            "requested_execution_mode": "standalone-nonmutating",
            "contract_kind": "full-task",
            "contract_ref": exact_ref(self.root, "plans/TASKS.md"),
            "dependencies": [],
            "dependency_receipts": [],
            "successor": None,
            "dispatch_step": "s1",
            "material_writes": [],
            "execution_outputs": [],
            "allowed_writes": [],
            "validation_commands": [command()],
            "attempt": attempt(),
            "material_package": None,
            "terminal_receipt": "receipts/UNIT-A.terminal.json",
            "closeout_receipt": "closeout/UNIT-A.receipt.json",
        }

    def config(self, units: list[dict[str, object]] | None = None) -> dict[str, object]:
        return {
            "schema_version": "1.0.0",
            "audit_id": "synthetic-audit",
            "repository_root": ".",
            "authority_class": "public",
            "publication_class": "public",
            "work_pack": exact_ref(self.root, "plans/WORK-PACK.md"),
            "control_artifacts": [exact_ref(self.root, "plans/TASKS.md")],
            "task_session_request_schema": exact_ref(
                self.root, "schemas/task-session-request.json"
            ),
            "terminal_receipt_schema": exact_ref(
                self.root, "schemas/terminal-receipt.json"
            ),
            "terminal_receipt_semantic_validator": exact_ref(
                self.root, "validators/validate-receipt.py"
            ),
            "units": units or [self.base_unit()],
            "immutable_paths": ["plans/WORK-PACK.md"],
            "shared_write_owners": [],
            "source_selectors": ["plans/TASKS.md"],
            "closeout_directory": {
                "path": "closeout",
                "create_if_missing": True,
            },
            "handoff_state": {
                "artifact_ref": exact_ref(
                    self.root, "plans/CONTINUATION.json"
                ),
                "expected_fields": {
                    "state": "audit-ready",
                    "selected_unit": None,
                    "selection_allowed": False,
                },
            },
            "refresh_targets": ["plans/WORK-PACK.md", "plans/TASKS.md"],
            "next_owner": "invoke:refresh",
        }


class WorkPackReadinessAuditTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = FixtureRepository()

    def tearDown(self) -> None:
        self.fixture.close()

    def test_happy_read_only_frontier_passes_without_selecting(self) -> None:
        report = AUDIT.audit(self.fixture.config(), self.fixture.root)
        self.assertEqual(report["verdict"], "pass")
        self.assertEqual(report["ready_frontier"], ["UNIT-A"])
        self.assertIsNone(report["selected_unit"])
        self.assertFalse(report["mutation_ready"])
        output_dir = self.fixture.root / "audit-output"
        AUDIT.write_outputs(report, output_dir)
        written_report = json.loads(
            (output_dir / "work-pack-readiness-report.json").read_text(
                encoding="utf-8"
            )
        )
        signal_pack = json.loads(
            (output_dir / "REFRESH-SIGNAL-PACK.json").read_text(encoding="utf-8")
        )
        self.assertEqual(written_report["verdict"], "pass")
        self.assertEqual(signal_pack["mutation_mode"], "proposal-only")
        self.assertFalse(signal_pack["mutation_ready"])
        self.assertEqual(signal_pack["authority_effect"], "none")

    def test_mixed_frontier_exposes_runtime_class_gap(self) -> None:
        material = self.fixture.base_unit()
        material.update(
            {
                "unit_id": "UNIT-M",
                "task_class": "material-mutation",
                "requested_execution_mode": "routed-mutation",
                "material_writes": ["workspace/source.py"],
                "allowed_writes": ["workspace/source.py"],
                "successor": "UNIT-O",
            }
        )
        output = self.fixture.base_unit()
        output.update(
            {
                "unit_id": "UNIT-O",
                "task_class": "output-only",
                "requested_execution_mode": "routed-mutation",
                "dependencies": ["UNIT-M"],
                "execution_outputs": ["workspace/runs/{attempt_id}/receipt.json"],
                "allowed_writes": ["workspace/runs/{attempt_id}/receipt.json"],
                "attempt": attempt(required=True),
            }
        )
        (self.fixture.root / "plans" / "TASKS.md").write_text(
            "# Tasks\n\n## UNIT-M\n\nMutation.\n\n## UNIT-O\n\nOutput.\n",
            encoding="utf-8",
        )
        for unit in (material, output):
            unit["contract_ref"] = exact_ref(self.fixture.root, "plans/TASKS.md")
        config = self.fixture.config([material, output])
        config["control_artifacts"] = [
            exact_ref(self.fixture.root, "plans/TASKS.md")
        ]
        report = AUDIT.audit(config, self.fixture.root)
        self.assertEqual(report["plan_contract_status"], "pass")
        self.assertEqual(report["runtime_admission_status"], "block")
        claims = {item["claim"] for item in report["findings"]}
        self.assertIn(
            "material mutation lacks current material-package admission evidence",
            claims,
        )
        self.assertIn(
            "live routed mutation requires material writes for a non-material task",
            claims,
        )

    def test_live_output_profile_removes_only_non_material_runtime_gap(self) -> None:
        request_schema = {
            "type": "object",
            "properties": {
                "executionMode": {
                    "enum": [
                        "routed-mutation",
                        "reusable-mutation",
                        "standalone-nonmutating",
                    ]
                },
                "materialWrites": {"type": "array"},
            },
        }
        (
            self.fixture.root / "schemas" / "task-session-request.json"
        ).write_text(json.dumps(request_schema), encoding="utf-8")
        material = self.fixture.base_unit()
        material.update(
            {
                "unit_id": "UNIT-M",
                "task_class": "material-mutation",
                "requested_execution_mode": "routed-mutation",
                "material_writes": ["workspace/source.py"],
                "allowed_writes": ["workspace/source.py"],
                "successor": "UNIT-O",
            }
        )
        output = self.fixture.base_unit()
        output.update(
            {
                "unit_id": "UNIT-O",
                "task_class": "output-only",
                "requested_execution_mode": "routed-mutation",
                "dependencies": ["UNIT-M"],
                "execution_outputs": ["workspace/runs/{attempt_id}/receipt.json"],
                "allowed_writes": ["workspace/runs/{attempt_id}/receipt.json"],
                "attempt": attempt(required=True),
            }
        )
        (self.fixture.root / "plans" / "TASKS.md").write_text(
            "# Tasks\n\n## UNIT-M\n\nMutation.\n\n## UNIT-O\n\nOutput.\n",
            encoding="utf-8",
        )
        for unit in (material, output):
            unit["contract_ref"] = exact_ref(
                self.fixture.root, "plans/TASKS.md"
            )
        report = AUDIT.audit(
            self.fixture.config([material, output]), self.fixture.root
        )
        claims = {item["claim"] for item in report["findings"]}
        self.assertIn(
            "material mutation lacks current material-package admission evidence",
            claims,
        )
        self.assertNotIn(
            "live routed mutation requires material writes for a non-material task",
            claims,
        )

    def test_cycle_blocks_graph(self) -> None:
        first = self.fixture.base_unit()
        first.update({"unit_id": "UNIT-A", "dependencies": ["UNIT-B"], "successor": "UNIT-B"})
        second = self.fixture.base_unit()
        second.update({"unit_id": "UNIT-B", "dependencies": ["UNIT-A"], "successor": "UNIT-A"})
        (self.fixture.root / "plans" / "TASKS.md").write_text(
            "# Tasks\n\n## UNIT-A\n\nA.\n\n## UNIT-B\n\nB.\n", encoding="utf-8"
        )
        for unit in (first, second):
            unit["contract_ref"] = exact_ref(self.fixture.root, "plans/TASKS.md")
        report = AUDIT.audit(self.fixture.config([first, second]), self.fixture.root)
        self.assertEqual(report["plan_contract_status"], "block")
        self.assertTrue(
            any(item["claim"] == "dependency graph contains a cycle" for item in report["findings"])
        )

    def test_unsafe_path_and_write_union_block(self) -> None:
        unit = self.fixture.base_unit()
        unit["material_writes"] = ["../escape"]
        unit["allowed_writes"] = []
        report = AUDIT.audit(self.fixture.config([unit]), self.fixture.root)
        claims = {item["claim"] for item in report["findings"]}
        self.assertIn("material_writes contains an unsafe or noncanonical path", claims)
        self.assertIn("allowed writes are not an exact disjoint partition", claims)

    def test_incomplete_attempt_lifecycle_blocks(self) -> None:
        unit = self.fixture.base_unit()
        unit.update(
            {
                "task_class": "output-only",
                "requested_execution_mode": "routed-mutation",
                "execution_outputs": ["workspace/output.json"],
                "allowed_writes": ["workspace/output.json"],
                "attempt": {
                    "required": True,
                    "id_algorithm": "",
                    "collision_policy": "fail-if-exists",
                    "retention_policy": "retain-receipt-only",
                    "teardown_on_success": [],
                    "teardown_on_failure": [],
                },
            }
        )
        report = AUDIT.audit(self.fixture.config([unit]), self.fixture.root)
        self.assertTrue(
            any(item["claim"] == "attempt lifecycle is incomplete" for item in report["findings"])
        )

    def test_fail_open_receipt_schema_blocks(self) -> None:
        weak = {
            "type": "object",
            "properties": {
                "unit_id": {"pattern": "^UNIT-"},
                "artifacts": {"type": "array", "items": {"type": "object"}},
                "validation": {"type": "array", "items": {"type": "object"}},
            },
        }
        (self.fixture.root / "schemas" / "terminal-receipt.json").write_text(
            json.dumps(weak), encoding="utf-8"
        )
        config = self.fixture.config()
        config["terminal_receipt_schema"] = exact_ref(
            self.fixture.root, "schemas/terminal-receipt.json"
        )
        report = AUDIT.audit(config, self.fixture.root)
        self.assertEqual(report["receipt_semantics_status"], "block")

    def test_snapshot_drift_blocks(self) -> None:
        config = self.fixture.config()
        original = AUDIT.capture_snapshot
        calls = 0

        def drifting(root: Path, refs: list[dict[str, object]]):
            nonlocal calls
            calls += 1
            snapshot, errors = original(root, refs)
            if calls == 2:
                first = next(iter(snapshot))
                snapshot[first] = ("0" * 64, snapshot[first][1])
            return snapshot, errors

        with mock.patch.object(AUDIT, "capture_snapshot", side_effect=drifting):
            report = AUDIT.audit(config, self.fixture.root)
        self.assertTrue(report["snapshot"]["drift"])
        self.assertEqual(report["verdict"], "block")

    def test_refresh_schema_rejects_authority_escalation(self) -> None:
        schema = json.loads(
            (SPELL_ROOT / "schemas" / "refresh-signal-pack.schema.json").read_text(
                encoding="utf-8"
            )
        )
        invalid = {
            "schema_version": "1.0.0",
            "audit_id": "synthetic",
            "source_report": {
                "path": "work-pack-readiness-report.json",
                "sha256": "0" * 64,
                "size_bytes": 1,
            },
            "mutation_mode": "apply-approved",
            "mutation_ready": True,
            "authority_effect": "promote",
            "signals": [],
            "target_inventory": ["plans/WORK-PACK.md"],
            "next_owner": "invoke:refresh",
        }
        errors = list(Draft202012Validator(schema).iter_errors(invalid))
        self.assertGreaterEqual(len(errors), 3)

    def test_handoff_route_drift_blocks(self) -> None:
        config = self.fixture.config()
        config["handoff_state"]["expected_fields"]["selection_allowed"] = True
        report = AUDIT.audit(config, self.fixture.root)
        self.assertEqual(report["plan_contract_status"], "block")
        self.assertTrue(
            any(
                item["claim"]
                == "handoff state contradicts the captured work-pack route"
                for item in report["findings"]
            )
        )


if __name__ == "__main__":
    unittest.main()
