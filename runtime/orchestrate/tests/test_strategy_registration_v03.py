#!/usr/bin/env python3

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ARCANUM_ROOT = Path(__file__).resolve().parents[3]
COORDINATOR_PATH = ARCANUM_ROOT / "runtime/orchestrate/scripts/native_dispatch_coordinator.py"
VALIDATOR = ARCANUM_ROOT / "formulae/dispatch-spec/scripts/validate-dispatch.py"
FIXTURES = ARCANUM_ROOT / "runtime/orchestrate/tests/fixtures/compile"

SPEC = importlib.util.spec_from_file_location("native_dispatch_coordinator_v03", COORDINATOR_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot import coordinator: {COORDINATOR_PATH}")
coordinator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(coordinator)


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def exact_ref(root: Path, path: Path) -> dict[str, object]:
    payload = path.read_bytes()
    return {
        "path": path.relative_to(root).as_posix(),
        "sha256": hashlib.sha256(payload).hexdigest(),
        "size": len(payload),
    }


class StrategyRegistrationV03Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.dispatch_path = self.root / "canonical.dispatch.json"
        self.entry_path = self.root / "runtime/execution-entry.json"
        self.runtime_root = self.root / "runtime/subagents-strategy"
        self.runtime_root.mkdir(parents=True)
        self.envelope_path = self.runtime_root / "v03-example.tmp.json"
        self.close_path = self.runtime_root / "v03-example.close.tmp.json"
        self.source_sheet = self.root / "evidence/v03-example.sheet.json"
        self.material_path = self.root / "evidence/v03-example.material.json"
        self.closure_path = self.root / "evidence/v03-example.closure.json"
        self.profile_path = self.root / "profiles/material-test.json"
        self.ledger_path = self.root / "evidence/strategy-ledger.yaml"

        (self.root / "confirmed-briefings.json").write_bytes(
            (FIXTURES / "confirmed-briefings.json").read_bytes()
        )
        profile = {
            "schema_version": "arcanum.subagent-strategy-runtime-profile.v1",
            "profile_id": "arcanum.test.material-profile.v1",
            "profile_version": "1.0.0",
            "row_schemas": {"current": "9.9.9", "historical_validate_only": []},
            "confirmation": {
                "mode": "material_projection",
                "binding_digest": "material_projection",
                "equivalence_receipt_kind": "arcanum.test.equivalence.v1",
            },
            "source_lifecycle": "durable",
            "ledger": "evidence/strategy-ledger.yaml",
            "runtime_temp_root": "runtime/subagents-strategy",
            "adapter_module": "unused/test-adapter.cjs",
            "adapter_base": "project_root",
            "adapter_operations": {
                "readiness": "--check",
                "register": "--consume",
                "close": "--consume",
            },
            "required_admission_receipt_kind": "arcanum.test.closure.v1",
            "dispatch_types": {
                "review": {"status": "live", "owner_capability": "unused/review/SKILL.md"}
            },
        }
        write_json(self.profile_path, profile)
        profile_ref = exact_ref(self.root, self.profile_path)

        dispatch = json.loads((FIXTURES / "valid-two-wave.json").read_text(encoding="utf-8"))
        dispatch["dispatch_id"] = "v03-example"
        strategy = dispatch["subagent_strategy"]
        strategy["authorization"] = "requires_user_permission"
        strategy.pop("registration", None)
        strategy["registration_intent"] = {
            "schema_version": "arcanum.subagent-strategy-registration-intent.v0.1",
            "profile_id": profile["profile_id"],
            "profile_ref": profile_ref,
            "confirmation_mode": "material_projection",
            "source_lifecycle": "durable",
            "registration_schema_version": "arcanum.subagent-strategy-registration.v0.3",
        }
        write_json(self.dispatch_path, dispatch)

        approved = copy.deepcopy(dispatch)
        approved["subagent_strategy"]["authorization"] = "approved"
        projection_sha = coordinator.strategy_execution_projection_v03_sha256(approved)
        material_sha = "a" * 64
        write_json(
            self.source_sheet,
            {
                "dispatch_id": dispatch["dispatch_id"],
                "schema_version": "9.9.9",
                "material_sha256": material_sha,
            },
        )
        write_json(
            self.material_path,
            {
                "projection_schema": "domainspec.material-strategy.v3",
                "material_sha256": material_sha,
                "material": {"goal": "v0.3 executable binding fixture"},
            },
        )
        source_ref = exact_ref(self.root, self.source_sheet)
        material_ref = exact_ref(self.root, self.material_path)
        dispatch_ref = exact_ref(self.root, self.dispatch_path)
        briefings_ref = exact_ref(self.root, self.root / "confirmed-briefings.json")
        write_json(
            self.closure_path,
            {
                "schema_version": "arcanum.test.closure.v1",
                "status": "pass",
                "blockers": [],
                "material_strategy": {"material_sha256": material_sha, "status": "pass"},
                "inputs": {
                    "sheet_ref": source_ref,
                    "material_projection_ref": material_ref,
                    "execution_dispatch_ref": dispatch_ref,
                    "execution_briefings_ref": briefings_ref,
                },
            },
        )
        closure_ref = exact_ref(self.root, self.closure_path)
        self.closure_ref = closure_ref
        confirmation = {
            "mode": "material_projection",
            "handle": "CONFIRM V03 EXAMPLE",
            "binding_sha256": material_sha,
            "material_equivalence_ref": None,
        }
        write_json(
            self.envelope_path,
            {
                "schema_version": "arcanum.test.registration-envelope.v1",
                "source_sheet_ref": source_ref,
                "confirmation": confirmation,
                "admission_receipt_ref": closure_ref,
                "execution_projection_sha256": projection_sha,
            },
        )
        envelope_ref = exact_ref(self.root, self.envelope_path)

        groups = []
        connections = []
        role_counts = {
            role["role_id"]: role["agent_count"] for role in strategy["roles"]
        }
        for wave in strategy["execution_waves"]:
            count = sum(role_counts[role_id] for role_id in wave["role_ids"])
            groups.append(
                {
                    "group_id": wave["wave_id"],
                    "agents": [{"role": "explorer"} for _ in range(count)],
                }
            )
            for dependency in wave.get("depends_on_waves", []):
                connections.append(
                    {"from": dependency, "to": wave["wave_id"], "type": "sequential"}
                )
        ledger_row = [
            "dispatches:",
            f"  - dispatch_id: {json.dumps(dispatch['dispatch_id'])}",
            '    schema_version: "9.9.9"',
            f"    registration_envelope_sha256: {json.dumps(envelope_ref['sha256'])}",
            f"    profile_id: {json.dumps(profile['profile_id'])}",
            f"    source_sheet_ref: {json.dumps(source_ref, separators=(',', ':'))}",
            '    source_lifecycle: "durable"',
            f"    confirmation_binding_sha256: {json.dumps(material_sha)}",
            f"    admission_receipt_ref: {json.dumps(closure_ref, separators=(',', ':'))}",
            f"    execution_projection_sha256: {json.dumps(projection_sha)}",
            f"    temporary_close: {json.dumps(self.close_path.relative_to(self.root).as_posix())}",
            "    max_loops: 1",
            f"    groups: {json.dumps(groups, separators=(',', ':'))}",
            f"    connections: {json.dumps(connections, separators=(',', ':'))}",
            "",
        ]
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
        self.ledger_path.write_text("\n".join(ledger_row), encoding="utf-8")
        self.envelope_path.unlink()

        registration = {
            "schema_version": "arcanum.subagent-strategy-registration.v0.3",
            "profile_id": profile["profile_id"],
            "profile_ref": profile_ref,
            "ledger": profile["ledger"],
            "sheet_schema_version": "9.9.9",
            "source_sheet_ref": source_ref,
            "source_lifecycle": "durable",
            "registration_envelope_ref": envelope_ref,
            "confirmation": confirmation,
            "admission_receipt_ref": closure_ref,
            "execution_projection_sha256": projection_sha,
            "temporary_close": self.close_path.relative_to(self.root).as_posix(),
        }
        write_json(
            self.entry_path,
            {
                "schema_version": "arcanum.subagent-strategy-execution-entry.v0.1",
                "canonical_dispatch_ref": exact_ref(self.root, self.dispatch_path),
                "authorization": "approved",
                "confirmation_handle": confirmation["handle"],
                "registration": registration,
            },
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_execution_entry_compiles_without_mutating_canonical_dispatch(self) -> None:
        before = self.dispatch_path.read_bytes()
        output = self.root / "run"
        result = coordinator.compile_to_directory(
            self.dispatch_path,
            "v03-test",
            output,
            VALIDATOR,
            self.root,
            self.entry_path,
        )
        self.assertEqual(result["status"], "pass")
        self.assertEqual(self.dispatch_path.read_bytes(), before)
        self.assertEqual(result["state"]["authorization_status"], "approved")
        receipt = json.loads((output / "strategy-registration.json").read_text(encoding="utf-8"))
        self.assertEqual(receipt["schema_version"], "arcanum.subagent-strategy-registration.v0.3")
        self.assertTrue(receipt["registration_envelope_consumed"])
        self.assertTrue(receipt["source_sheet_preserved"])
        self.assertFalse(receipt["temporary_close_consumed"])
        self.assertIsNone(receipt["temporary_close_ref"])

    def test_canonical_dispatch_cannot_embed_postconfirmation_approval(self) -> None:
        dispatch = json.loads(self.dispatch_path.read_text(encoding="utf-8"))
        dispatch["subagent_strategy"]["authorization"] = "approved"
        write_json(self.dispatch_path, dispatch)
        entry = json.loads(self.entry_path.read_text(encoding="utf-8"))
        entry["canonical_dispatch_ref"] = exact_ref(self.root, self.dispatch_path)
        write_json(self.entry_path, entry)
        with self.assertRaises(coordinator.CompileBlocked) as raised:
            coordinator.verify_strategy_registration_v03(
                dispatch, self.dispatch_path, self.entry_path, self.root
            )
        self.assertIn(
            "v0.3 canonical dispatch must remain preconfirmation authorization",
            raised.exception.blockers,
        )

    def test_consumed_envelope_must_not_reappear(self) -> None:
        self.envelope_path.write_text("reappeared", encoding="utf-8")
        with self.assertRaises(coordinator.CompileBlocked) as raised:
            coordinator.verify_strategy_registration_v03(
                json.loads(self.dispatch_path.read_text(encoding="utf-8")),
                self.dispatch_path,
                self.entry_path,
                self.root,
            )
        self.assertIn(
            "registration_envelope_ref.path must be consumed before execution",
            raised.exception.blockers,
        )

    def test_close_verification_binds_consumed_record_and_registered_topology(self) -> None:
        with self.ledger_path.open("a", encoding="utf-8") as ledger:
            ledger.write(
                "\n".join(
                    [
                        f"  - close_of: {json.dumps('v03-example')}",
                        f"    close_sha256: {json.dumps('b' * 64)}",
                        f"    temporary_close: {json.dumps(self.close_path.relative_to(self.root).as_posix())}",
                        '    exit_reason: "resolved"',
                        '    agents_spawned: {"total":4,"tree":{"agents":4},"loops_used":1}',
                        "",
                    ]
                )
            )
        approved, receipt = coordinator.verify_strategy_registration_v03(
            json.loads(self.dispatch_path.read_text(encoding="utf-8")),
            self.dispatch_path,
            self.entry_path,
            self.root,
            require_close=True,
        )
        self.assertEqual(approved["subagent_strategy"]["authorization"], "approved")
        self.assertTrue(receipt["close_registered"])
        self.assertTrue(receipt["temporary_close_consumed"])
        self.assertEqual(
            receipt["temporary_close_ref"],
            {
                "path": self.close_path.relative_to(self.root).as_posix(),
                "sha256": "b" * 64,
            },
        )

    def test_close_verification_rejects_raw_normalized_topology_mismatch(self) -> None:
        with self.ledger_path.open("a", encoding="utf-8") as ledger:
            ledger.write(
                "\n".join(
                    [
                        f"  - close_of: {json.dumps('v03-example')}",
                        f"    close_sha256: {json.dumps('b' * 64)}",
                        f"    temporary_close: {json.dumps(self.close_path.relative_to(self.root).as_posix())}",
                        '    exit_reason: "resolved"',
                        '    agents_spawned: {"total":3,"tree":{"agents":3},"loops_used":1}',
                        "",
                    ]
                )
            )
        with self.assertRaises(coordinator.CompileBlocked) as raised:
            coordinator.verify_strategy_registration_v03(
                json.loads(self.dispatch_path.read_text(encoding="utf-8")),
                self.dispatch_path,
                self.entry_path,
                self.root,
                require_close=True,
            )
        self.assertIn(
            "strategy close agent total does not match the registered topology",
            raised.exception.blockers,
        )

    def test_full_v03_projection_rejects_every_execution_bearing_mutation(self) -> None:
        mutations = {
            "execution_contract_version": lambda value: value["subagent_strategy"].__setitem__(
                "execution_contract_version", "arcanum.capability-bound-execution.v9.9"
            ),
            "role_step": lambda value: value["subagent_strategy"]["roles"][0].__setitem__(
                "capability_ref", "mutated/capability/SKILL.md"
            ),
            "gate": lambda value: value["subagent_strategy"]["execution_waves"][0].__setitem__(
                "gate_after", "mutated-gate"
            ),
        }
        original_dispatch = self.dispatch_path.read_bytes()
        original_entry = self.entry_path.read_bytes()
        original_closure = self.closure_path.read_bytes()
        original_ledger = self.ledger_path.read_bytes()
        for label, mutate in mutations.items():
            with self.subTest(label=label):
                self.dispatch_path.write_bytes(original_dispatch)
                self.entry_path.write_bytes(original_entry)
                self.closure_path.write_bytes(original_closure)
                self.ledger_path.write_bytes(original_ledger)
                dispatch = json.loads(self.dispatch_path.read_text(encoding="utf-8"))
                mutate(dispatch)
                write_json(self.dispatch_path, dispatch)
                canonical_ref = exact_ref(self.root, self.dispatch_path)
                closure = json.loads(self.closure_path.read_text(encoding="utf-8"))
                closure["inputs"]["execution_dispatch_ref"] = canonical_ref
                write_json(self.closure_path, closure)
                refreshed_closure_ref = exact_ref(self.root, self.closure_path)
                entry = json.loads(self.entry_path.read_text(encoding="utf-8"))
                entry["canonical_dispatch_ref"] = canonical_ref
                entry["registration"]["admission_receipt_ref"] = refreshed_closure_ref
                write_json(self.entry_path, entry)
                ledger = self.ledger_path.read_text(encoding="utf-8").replace(
                    json.dumps(self.closure_ref, separators=(",", ":")),
                    json.dumps(refreshed_closure_ref, separators=(",", ":")),
                )
                self.ledger_path.write_text(ledger, encoding="utf-8")
                with self.assertRaises(coordinator.CompileBlocked) as raised:
                    coordinator.verify_strategy_registration_v03(
                        dispatch, self.dispatch_path, self.entry_path, self.root
                    )
                self.assertIn(
                    "strategy registration execution projection digest mismatch",
                    raised.exception.blockers,
                )
        self.dispatch_path.write_bytes(original_dispatch)
        self.entry_path.write_bytes(original_entry)
        self.closure_path.write_bytes(original_closure)
        self.ledger_path.write_bytes(original_ledger)

    def test_material_admission_binds_current_briefing_bytes(self) -> None:
        briefings = self.root / "confirmed-briefings.json"
        briefings.write_bytes(briefings.read_bytes() + b"\n")
        with self.assertRaises(coordinator.CompileBlocked) as raised:
            coordinator.verify_strategy_registration_v03(
                json.loads(self.dispatch_path.read_text(encoding="utf-8")),
                self.dispatch_path,
                self.entry_path,
                self.root,
            )
        self.assertIn(
            "strategy admission execution_briefings_ref does not match current file bytes",
            raised.exception.blockers,
        )

    def test_material_admission_binds_exact_canonical_dispatch_ref(self) -> None:
        closure = json.loads(self.closure_path.read_text(encoding="utf-8"))
        closure["inputs"]["execution_dispatch_ref"]["sha256"] = "f" * 64
        write_json(self.closure_path, closure)
        entry = json.loads(self.entry_path.read_text(encoding="utf-8"))
        registration = entry["registration"]
        registration["admission_receipt_ref"] = exact_ref(self.root, self.closure_path)
        write_json(self.entry_path, entry)
        with self.assertRaises(coordinator.CompileBlocked) as raised:
            coordinator.verify_strategy_registration_v03(
                json.loads(self.dispatch_path.read_text(encoding="utf-8")),
                self.dispatch_path,
                self.entry_path,
                self.root,
            )
        self.assertIn(
            "strategy admission execution dispatch binding mismatch",
            raised.exception.blockers,
        )


if __name__ == "__main__":
    unittest.main()
