#!/usr/bin/env python3
"""Contract and deterministic-fault tests for the additive WPRA v2 projection."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SPELL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = SPELL_ROOT / "scripts" / "audit_work_pack.py"
SPEC = importlib.util.spec_from_file_location("audit_work_pack_v2", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot load {SCRIPT_PATH}")
AUDIT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUDIT)


def sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


class V2Fixture:
    def __init__(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / ".git").mkdir()
        evidence = {
            "objective": {"acceptance": ["projection", "finite frontier"]},
            "owner": "synthetic-owner",
            "material": {"digest": "a" * 64},
            "validation": {"argv": ["false"]},
            "receipt": {"semantic": "terminal-and-closeout"},
            "closeout": {"delta": "exact", "owner": "synthetic-owner"},
            "package": {"kind": "synthetic"},
            "producerReceipt": {"status": "pass"},
            "schema": {"type": "object"},
            "inventory": ["target.txt"],
            "terminalSchema": {"type": "object"},
            "validator": {"id": "synthetic-validator"},
            "admission": {"status": "candidate"},
            "status": {"value": "candidate"},
            "approval": {"status": "unapproved"},
            "risk": {"maximum": "bounded-write"},
            "decision": {"selection": "pending"},
            "successor": "U1",
            "equivalence": {"version": "1"},
            "continuation": "U1",
        }
        self.evidence_path = self.root / "evidence.json"
        self.evidence_path.write_text(
            json.dumps(evidence, sort_keys=True), encoding="utf-8"
        )
        self.target = self.root / "target.txt"
        self.target.write_text("baseline\n", encoding="utf-8")

    def close(self) -> None:
        self.temp.cleanup()

    def exact(self) -> dict[str, object]:
        content = self.evidence_path.read_bytes()
        return {
            "path": "evidence.json",
            "sha256": sha256(content),
            "size_bytes": len(content),
        }

    def binding(
        self, binding_id: str, selector: str, owner: str = "synthetic-owner"
    ) -> dict[str, object]:
        return {
            "binding_id": binding_id,
            "owner_ref": owner,
            "artifact_ref": self.exact(),
            "selector": selector,
        }

    def opaque_validator_binding(self, content: bytes) -> dict[str, object]:
        path = self.root / "validate-terminal-receipt.py"
        path.write_bytes(content)
        return {
            "binding_id": "terminal-validator",
            "owner_ref": "synthetic-owner",
            "binding_mode": "opaque-exact-artifact",
            "artifact_ref": {
                "path": path.name,
                "sha256": sha256(content),
                "size_bytes": len(content),
            },
        }

    def status(self, name: str, value: str) -> dict[str, object]:
        return {
            "value": value,
            "owner_ref": f"{name}-owner",
            "receipt_ref": self.binding(f"{name}-receipt", "/status"),
        }

    def config(self) -> dict[str, object]:
        package_digest = "a" * 64
        return {
            "schema_version": "2.0.0",
            "audit_id": "synthetic-v2",
            "repository_root": ".",
            "evidence_ceiling": "frozen-input-contractual-readiness",
            "classifier_version": "wpra-projection-v1",
            "objective_ref": self.binding("objective", "/objective"),
            "closure_receipt_refs": [
                self.binding("define-exit", "/status"),
                self.binding("plan-receipt", "/status"),
            ],
            "authority_bindings": {
                "canonical_authority_refs": [
                    self.binding("canonical-objective", "/objective")
                ],
                "semantic_bindings": {
                    "owner": self.binding("semantic-owner", "/owner"),
                    "material": self.binding("semantic-material", "/material"),
                    "validation": self.binding(
                        "semantic-validation", "/validation"
                    ),
                    "receipt": self.binding("semantic-receipt", "/receipt"),
                    "closeout": self.binding("semantic-closeout", "/closeout"),
                },
            },
            "execution_bindings": [
                {
                    "unit_id": "U1",
                    "dependencies": [],
                    "canonical_successors": ["__complete__"],
                    "command": {
                        "argv": ["false"],
                        "cwd": ".",
                        "risk_class": "bounded-write",
                    },
                    "material_writes": ["target.txt"],
                    "execution_outputs": ["receipts/U1.json"],
                    "allowed_writes": ["target.txt", "receipts/U1.json"],
                    "material_package": {
                        "package_ref": self.binding("package", "/package"),
                        "producer_owner_ref": "synthetic-producer",
                        "producer_receipt_ref": self.binding(
                            "producer-receipt", "/producerReceipt"
                        ),
                        "schema_ref": self.binding("package-schema", "/schema"),
                        "declared_sha256": package_digest,
                        "target_inventory_ref": self.binding(
                            "target-inventory", "/inventory"
                        ),
                    },
                    "byte_baselines": [
                        {
                            "path": "target.txt",
                            "sha256": sha256(self.target.read_bytes()),
                        }
                    ],
                }
            ],
            "receipt_bindings": {
                "terminal_schema_ref": self.binding(
                    "terminal-schema", "/terminalSchema"
                ),
                "semantic_validator_ref": self.binding(
                    "terminal-validator", "/validator"
                ),
                "expected_receipt_refs": [
                    self.binding("expected-terminal", "/status")
                ],
            },
            "closeout_bindings": [
                {
                    "unit_id": "U1",
                    "allowed_delta_policy_ref": self.binding(
                        "allowed-delta", "/closeout/delta"
                    ),
                    "owner_receipt_contract_ref": self.binding(
                        "closeout-owner", "/closeout"
                    ),
                    "compensation": {
                        "mode": "none",
                        "rationale": "Synthetic fixture has no reversible side effect.",
                    },
                }
            ],
            "runtime_binding": {
                "requested_task_session_execution_mode": "routed-mutation",
                "task_session_admission_receipt_ref": self.binding(
                    "task-session-admission", "/admission"
                ),
            },
            "status_receipt_refs": {
                "artifact_authored_status": self.status(
                    "artifact-authored", "authored"
                ),
                "registry_released_status": self.status(
                    "registry-released", "unreleased"
                ),
                "mutation_runtime_ready_status": self.status(
                    "mutation-runtime", "candidate"
                ),
                "audit_verdict": self.status("audit-verdict", "pending"),
            },
            "lifecycle_status_refs": {
                "plan_artifact_status": self.status("plan", "authored"),
                "audit_status": self.status("audit", "pending"),
                "approval_status": self.status("approval", "unapproved"),
                "chain_status": self.status("chain", "not-started"),
            },
            "approval_policy": {
                "approval_owner_ref": "decision-gate",
                "decision_gate_receipt_ref": self.binding(
                    "decision-gate", "/decision"
                ),
                "run_budget": {"max_task_session_requests": 1},
                "risk_policy_ref": self.binding("risk-policy", "/risk"),
                "allowed_audit_verdicts": ["pass", "flag"],
                "allowed_flag_classes": ["observability-residue"],
            },
            "continuity_projection": {
                "cursor": "U1",
                "completed_unit_receipt_refs": [],
                "joined_closeout_receipt_refs": [],
                "projected_next_successor": {
                    "unit_id": "U1",
                    "canonical_successor_ref": self.binding(
                        "canonical-successor", "/successor"
                    ),
                    "projection_owner_ref": "work-pack-readiness-audit",
                    "equivalence_validator_ref": self.binding(
                        "equivalence-validator", "/equivalence"
                    ),
                    "continuation_router_verification_receipt_ref": self.binding(
                        "continuation-verification", "/continuation"
                    ),
                    "authority_effect": "none",
                },
            },
            "expected_material_digests": {"U1": package_digest},
        }


class WorkPackReadinessAuditV2Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = V2Fixture()

    def tearDown(self) -> None:
        self.fixture.close()

    def audit(self, config: dict[str, object]) -> dict[str, object]:
        errors = AUDIT.schema_errors(
            config, AUDIT.load_json(AUDIT.CONFIG_SCHEMA_V2), "v2 config"
        )
        self.assertEqual(errors, [])
        return AUDIT.audit_v2(config, self.fixture.root)

    def test_projection_is_deterministic_and_executes_no_command(self) -> None:
        config = self.fixture.config()
        first = self.audit(config)
        self.assertEqual(first["verdict"], "pass")
        self.assertEqual(first["terminal_code"], "PROJECTION_READY")
        self.assertFalse(first["configured_commands_executed"])
        self.assertIsNone(first["selected_unit"])
        self.assertEqual(first["authority_effect"], "none")
        self.assertFalse(first["mutation_ready"])
        second_config = copy.deepcopy(config)
        second_config["audit_id"] = "synthetic-v2-regenerated"
        second = self.audit(second_config)
        self.assertEqual(
            first["audit_projection_digest"], second["audit_projection_digest"]
        )
        self.assertEqual(
            AUDIT.compare_manifests_v2(first["manifest"], second["manifest"]),
            "PROJECTION_EQUIVALENCE_PRESERVED",
        )
        output_dir = self.fixture.root / "outputs"
        AUDIT.write_outputs_v2(first, output_dir)
        self.assertTrue(
            (output_dir / "objective-execution-manifest.json").is_file()
        )

    def test_single_faults_return_stable_preroute_codes(self) -> None:
        cases = [
            (
                "MATERIAL_PACKAGE_REF_MISSING",
                lambda c: c["execution_bindings"][0]["material_package"].update(
                    package_ref=None
                ),
            ),
            (
                "MATERIAL_PRODUCER_OWNER_UNRESOLVED",
                lambda c: c["execution_bindings"][0]["material_package"].update(
                    producer_owner_ref=None
                ),
            ),
            (
                "MATERIAL_PRODUCER_RECEIPT_MISSING",
                lambda c: c["execution_bindings"][0]["material_package"].update(
                    producer_receipt_ref=None
                ),
            ),
            (
                "MATERIAL_RECEIPT_SCHEMA_MISSING",
                lambda c: c["execution_bindings"][0]["material_package"].update(
                    schema_ref=None
                ),
            ),
            (
                "TARGET_INVENTORY_MISSING",
                lambda c: c["execution_bindings"][0]["material_package"].update(
                    target_inventory_ref=None
                ),
            ),
            (
                "EXECUTION_BYTE_BASELINE_MISSING",
                lambda c: c["execution_bindings"][0].update(byte_baselines=[]),
            ),
            (
                "ALLOWED_DELTA_POLICY_MISSING",
                lambda c: c["closeout_bindings"][0].update(
                    allowed_delta_policy_ref=None
                ),
            ),
            (
                "CLOSEOUT_RECEIPT_CONTRACT_MISSING",
                lambda c: c["closeout_bindings"][0].update(
                    owner_receipt_contract_ref=None
                ),
            ),
            (
                "CANONICAL_SUCCESSOR_NON_UNIQUE",
                lambda c: c["execution_bindings"][0].update(
                    canonical_successors=["U2", "__complete__"]
                ),
            ),
            (
                "PREROUTE_MATERIAL_DIGEST_MISMATCH",
                lambda c: c["execution_bindings"][0]["material_package"].update(
                    declared_sha256="b" * 64
                ),
            ),
        ]
        for expected, mutate in cases:
            with self.subTest(expected=expected):
                config = copy.deepcopy(self.fixture.config())
                mutate(config)
                report = self.audit(config)
                self.assertEqual(report["verdict"], "block")
                self.assertEqual(report["terminal_code"], expected)
                self.assertIsNone(report["manifest"])
                self.assertIsNone(report["selected_unit"])

    def test_semantic_component_changes_invalidate_exact_owner(self) -> None:
        baseline = self.audit(self.fixture.config())["manifest"]
        cases = [
            ("owner", "EPOCH_INVALIDATED_OWNER_CHANGE"),
            ("material", "EPOCH_INVALIDATED_MATERIAL_CHANGE"),
            ("validation", "EPOCH_INVALIDATED_VALIDATION_CHANGE"),
            ("receipt", "EPOCH_INVALIDATED_RECEIPT_CHANGE"),
            ("closeout", "EPOCH_INVALIDATED_CLOSEOUT_CHANGE"),
        ]
        for component, expected in cases:
            with self.subTest(component=component):
                config = copy.deepcopy(self.fixture.config())
                config["authority_bindings"]["semantic_bindings"][component][
                    "owner_ref"
                ] = f"changed-{component}-owner"
                current = self.audit(config)["manifest"]
                self.assertEqual(
                    AUDIT.compare_manifests_v2(baseline, current), expected
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)
