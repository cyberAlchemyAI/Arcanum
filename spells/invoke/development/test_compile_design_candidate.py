#!/usr/bin/env python3
"""Producer acceptance tests for the W2 Design candidate boundary."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path


INVOKE = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


W1_TESTS = load_module("w2_w1_fixture", Path(__file__).with_name("test_compile_design_input_bundle.py"))
W2 = load_module("w2_candidate_compiler", INVOKE / "scripts/compile_design_candidate.py")
PROJECTOR = load_module("w2_candidate_projector", INVOKE / "scripts/project_design_artifact.py")
VALIDATOR = load_module("w2_candidate_validator", INVOKE / "scripts/validate_design_coherence.py")


def digest_without(document: dict, field: str) -> str:
    return hashlib.sha256(json.dumps({key: value for key, value in document.items() if key != field}, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


class DesignCandidateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = W1_TESTS.DesignInputBundleTests(methodName="runTest")
        self.fixture.setUp()
        self.repo = self.fixture.repo
        target = self.repo / "arcanum/spells/invoke"
        (target / "development/whole-invoke-repair-plan/design-process").mkdir(parents=True)
        shutil.copytree(INVOKE / "schemas", target / "schemas")
        shutil.copytree(INVOKE / "scripts", target / "scripts")
        for name in ["DESIGN-PRODUCTION-PROCESS.json", "DESIGN-PROFILE.json", "DESIGN-COHERENCE-POLICY.json"]:
            shutil.copy2(INVOKE / "development/whole-invoke-repair-plan/design-process" / name, target / "development/whole-invoke-repair-plan/design-process" / name)
        self.schemas = target / "schemas"
        input_id = "input:define"
        self.fixture.closure["scope_signals"] = {
            "human_actors": [{"signal_id": "signal:actor", "source_input_id": input_id, "actor_id": "actor:owner", "natural_person": True, "reads": True, "decides": True, "acts": True, "recovers": True, "navigates": True, "assistive_operation": True, "surfaces": ["console"]}],
            "rendered_surfaces": [{"signal_id": "signal:surface", "source_input_id": input_id, "surface_id": "surface:console", "modality": "text", "semantic_contract_ref": "contract:w1-input", "semantic_change": "new"}],
            "interfaces": [{"signal_id": "signal:interface", "source_input_id": input_id, "interface_id": "interface:compiler", "kind": "CLI", "peer": "design-author", "direction": "inbound", "contract_ref": "contract:w1-input"}],
            "stores": [{"signal_id": "signal:store", "source_input_id": input_id, "store_id": "store:evidence", "authority": "candidate-only", "data_classes": ["design-evidence"], "writers": ["invoke-design-candidate-producer"]}],
            "queues": [{"signal_id": "signal:queue", "source_input_id": input_id, "queue_id": "queue:none", "producers": ["invoke-design-candidate-producer"], "consumers": ["design-bundle-producer"], "ordering": "single atomic candidate"}],
            "writers": [{"signal_id": "signal:writer", "source_input_id": input_id, "writer_id": "writer:candidate", "targets": ["W2 candidate directory"], "concurrency": "single writer"}],
            "normative_rules": [{"signal_id": "signal:validate-inputs", "source_input_id": input_id, "rule_id": "rule:validate-inputs", "verb": "validate", "subject": "Design input producer", "object": "approved input closure", "enforcement_hint": "Require an exact passing W1 receipt."}],
            "effects": [{"signal_id": "signal:effect", "source_input_id": input_id, "effect_id": "effect:publish-candidate", "reversible": True, "external": False, "privileged": False}],
            "data_and_log_sinks": [{"signal_id": "signal:sink", "source_input_id": input_id, "sink_id": "sink:candidate", "data_classes": ["design-evidence"], "retention_hint": "repository-local candidate"}],
            "deployment_targets": [{"signal_id": "signal:deployment", "source_input_id": input_id, "deployment_id": "deployment:none", "environment": "none", "release_mode": "not-deployed"}],
            "compatibility_boundaries": [{"signal_id": "signal:compatibility", "source_input_id": input_id, "boundary_id": "compatibility:w1-w2", "old_contract": "W1 producer v1", "new_contract": "W2 candidate v1"}],
            "quality_claims": [{"signal_id": "signal:quality", "source_input_id": input_id, "claim_id": "claim:determinism", "source_kind": "quality-constraint", "threshold_or_tradeoff": "byte-identical for exact inputs and destination", "required": True}],
            "acceptance_and_readiness_claims": [{"signal_id": "signal:readiness", "source_input_id": input_id, "claim_id": "claim:source-complete", "selector": "DESIGN-SOURCE.json", "evidence_state": "authored-complete"}],
        }
        selector = self.fixture.closure["input_catalog"][0]["selector"]
        ownership = {"accountable_owner": "design-input-owner", "contributing_owners": ["design-input-owner"], "artifact_owner": "plan-work-pack-owner", "validator_owner": "invoke-design-selection-validator"}
        self.fixture.closure["constraints"] = [{"obligation_id": "constraint:atomic", "class": "constraint", "statement": "Candidate publication is atomic.", "source_input_ids": [input_id], "owner": "design-input-owner"}]
        self.fixture.closure["invariants"] = [{"obligation_id": "invariant:no-authority", "class": "invariant", "statement": "W2 grants no later lifecycle authority.", "source_input_ids": [input_id], "owner": "design-input-owner"}]
        self.fixture.closure["prior_decisions"] = [{"decision_id": "decision:preserve-w1", "status": "preserved", "owner": "design-input-owner", "decision_ref": self.fixture.file_ref(self.fixture.no_prior_path)}]
        self.fixture.closure["input_conflicts"] = [{"conflict_id": "conflict:resolved", "input_ids": [input_id], "resolution_status": "resolved", "decision_ref": self.fixture.file_ref(self.fixture.no_prior_path)}]
        self.fixture.closure["selection_inputs"]["authored_concerns"].extend([
            {"concern_id": "authored:reliability", "primary_class": "reliability", "disposition": "recommended", "required_predicate": False, "evidence_selectors": [selector], "ownership": copy.deepcopy(ownership), "selected": False, "rationale": "Retain a reviewable reliability recommendation.", "revisit_condition": "Revisit when runtime SLO evidence exists."},
            {"concern_id": "authored:migration", "primary_class": "migration", "disposition": "not-applicable-with-rationale", "required_predicate": False, "evidence_selectors": [selector], "ownership": copy.deepcopy(ownership), "selected": False, "rationale": "The greenfield fixture has no migration predecessor.", "revisit_condition": None},
        ])
        self.fixture.closure["selection_inputs"]["predicate_inputs"].extend([
            {"predicate_id": "predicate:reliability", "concern_id": "authored:reliability", "source_input_ids": [input_id], "expected": False},
            {"predicate_id": "predicate:migration", "concern_id": "authored:migration", "source_input_ids": [input_id], "expected": False},
        ])
        self.fixture.closure["selection_inputs"]["planned_witness_requirements"] = [{"witness_id": "witness:atomic", "claim_id": "claim:source-complete", "concern_id": "authored:validation", "evidence_state": "planned-contract"}]
        self.fixture.write_closure(self.fixture.closure)
        self.w1_receipt = self.fixture.compile_at("w1-bundle")
        self.w1_dir = self.repo / "w1-bundle"
        self.source_path = self.repo / "DESIGN-SOURCE.json"
        self.source = self.make_source()
        self.write_source(self.source)

    def tearDown(self) -> None:
        self.fixture.tearDown()

    def exact(self, path: Path) -> dict:
        data = path.read_bytes()
        return {"path": path.relative_to(self.repo).as_posix(), "sha256": hashlib.sha256(data).hexdigest(), "size": len(data)}

    @staticmethod
    def write_json(path: Path, document: dict) -> None:
        path.write_text(json.dumps(document, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")

    def write_source(self, source: dict) -> None:
        source["source_digest"] = digest_without(source, "source_digest")
        self.write_json(self.source_path, source)

    def make_source(self) -> dict:
        closure = json.loads(self.fixture.closure_path.read_text())
        selection = json.loads((self.w1_dir / "DESIGN-SELECTION-RESULT.json").read_text())
        pairs = sorted(VALIDATOR.expected_application_pairs(closure, selection))
        closure_ref = self.exact(self.fixture.closure_path)
        concern_by_id = {item["concern_id"]: item for item in selection["concerns"]}
        na_pairs = {("selection-concern", item["concern_id"]) for item in selection["concerns"] if item["disposition"] == "not-applicable-with-rationale"}
        signal_pairs = {("scope-signal", item["signal_id"]) for values in closure["scope_signals"].values() for item in values}
        signal_fact_ids = {("scope-signal", item["signal_id"]): item[identity_key] for signal_class, values in closure["scope_signals"].items() for item in values for _, identity_key, _ in [VALIDATOR.SIGNAL_MAP[signal_class]]}
        main_pairs = [item for item in pairs if item not in signal_pairs and item not in na_pairs]
        main_fact_ids = ["system:w1-target", "component:w1-producer", "contract:w1-input"]
        all_fact_ids = [*main_fact_ids, *sorted(signal_fact_ids.values())]
        applications = []
        for subject_kind, subject_id in pairs:
            is_na = (subject_kind, subject_id) in na_pairs
            application_fact_ids = [] if is_na else [signal_fact_ids[(subject_kind, subject_id)]] if (subject_kind, subject_id) in signal_pairs else copy.deepcopy(all_fact_ids) if (subject_kind, subject_id) == ("selected-output", "architecture") else copy.deepcopy(main_fact_ids)
            applications.append({
                "subject_kind": subject_kind, "subject_id": subject_id, "disposition": "not-applicable-with-evidence" if is_na else "satisfied",
                "fact_ids": application_fact_ids,
                "evidence_refs": [closure_ref] if is_na else [], "decision_ref": None,
                "rationale": "The candidate fact registry preserves this exact W1 obligation.",
            })
        main_refs = [{"subject_kind": kind, "subject_id": identifier} for kind, identifier in main_pairs]
        facts = [
            {"fact_id": "system:w1-target", "fact_kind": "system", "name": "W1 target system", "owner": "design-input-owner", "requirement_refs": copy.deepcopy(main_refs), "attributes": {"responsibility": "Own the approved-boundary Design candidate."}},
            {"fact_id": "component:w1-producer", "fact_kind": "component", "name": "W1-bound candidate producer", "owner": "invoke-design-candidate-producer", "requirement_refs": copy.deepcopy(main_refs), "attributes": {"level": "high-level", "parent_component_id": None, "responsibility": "Project and validate one W2 candidate atomically.", "contract_ids": ["contract:w1-input"]}},
            {"fact_id": "contract:w1-input", "fact_kind": "contract", "name": "Normal W1 input contract", "owner": "design-input-owner", "requirement_refs": copy.deepcopy(main_refs), "attributes": {"contract_kind": "evidence-binding", "statement": "Accept exactly one normal W1 PASS bundle.", "versioning": "v1 exact digest", "failure_boundary": "Governed BLOCK before publication.", "preservation": "preserved"}},
        ]
        for signal_class, values in closure["scope_signals"].items():
            fact_kind, identity_key, fields = VALIDATOR.SIGNAL_MAP[signal_class]
            for signal in values:
                facts.append({"fact_id": signal[identity_key], "fact_kind": fact_kind, "name": f"W1 {signal_class} {signal[identity_key]}", "owner": "design-input-owner", "requirement_refs": [{"subject_kind": "scope-signal", "subject_id": signal["signal_id"]}, {"subject_kind": "selected-output", "subject_id": "architecture"}], "attributes": {field: copy.deepcopy(signal[field]) for field in fields}})
        no_prior = self.exact(self.fixture.no_prior_path)
        profile_path = self.repo / PROJECTOR.PROFILE_PATH
        input_ref = {key: closure["input_catalog"][0]["source_ref"][key] for key in ["path", "sha256", "size"]}
        selected_outputs = sorted(selection["selected_outputs"])
        companions = [{"output_id": output_id, "fact_ids": copy.deepcopy(main_fact_ids), "requirement_refs": [{"subject_kind": "selected-output", "subject_id": output_id}]} for output_id in selected_outputs if output_id != "architecture"]
        profile = json.loads(profile_path.read_text())
        fact_by_id = {item["fact_id"]: item for item in facts}
        projected_views = {}
        view_keys = ["context", "high_level_structure", "low_level_components", "workflow_process", "decision_flow", "dependency_interface"]
        for key, rule in zip(view_keys, profile["view_rules"]):
            ids = sorted(item["fact_id"] for item in facts if item["fact_kind"] in rule["allowed_fact_kinds"])
            projected_views[key] = {"view_id": rule["view_id"], "applicability": "applicable", "fact_ids": ids, "na_evidence_refs": []}
        return {
            "$schema": "https://arcanum.dev/schemas/invoke/design-source/v1", "schema_version": "invoke.design-source.v1",
            "source_id": "design-source:w2-fixture", "target_id": self.fixture.target_id, "activation_kind": "normal",
            "profile_binding": {"profile_id": "invoke.generic-design-baseline.v1", "profile_ref": self.exact(profile_path)},
            "upstream_bindings": {
                "design_input_production_receipt_ref": self.exact(self.w1_dir / "DESIGN-INPUT-PRODUCTION-RECEIPT.json"),
                "design_input_closure_ref": closure_ref,
                "design_input_closure_receipt_ref": self.exact(self.w1_dir / "DESIGN-INPUT-CLOSURE-RECEIPT.json"),
                "scope_manifest_ref": self.exact(self.w1_dir / "DESIGN-SCOPE-MANIFEST.json"),
                "denominator_receipt_ref": self.exact(self.w1_dir / "DESIGN-DENOMINATOR-RECEIPT.json"),
                "selection_result_ref": self.exact(self.w1_dir / "DESIGN-SELECTION-RESULT.json"),
            },
            "design_kind": {"kind": "greenfield", "determination_ref": no_prior},
            "applications": applications, "facts": facts,
            "views": projected_views,
            "selected_outputs": selected_outputs, "selected_companions": companions,
            "glossary_application": {"source_glossary_ref": input_ref, "mappings": [{"term": "approved design input boundary", "fact_ids": ["contract:w1-input"]}], "unmapped_terms": []},
            "planned_witnesses": [{"witness_id": "witness:atomic", "claim_id": "claim:source-complete", "concern_id": "authored:validation", "polarity": "positive", "target_fact_ids": copy.deepcopy(main_fact_ids), "input_or_violation": "Compile the exact source.", "expected_result": "The three-file W2 candidate publishes atomically.", "execution_owner": "plan-work-pack-owner", "execution_phase": "validation", "evidence_state": "planned-contract"}], "unresolved_gaps": [],
            "layering": {"kind": "seed", "decision": "Keep W2 as one source-to-coherence producer slice.", "minimum_unit": "Normal W1 bundle through atomic candidate receipt."},
            "template_selection": {"selected_profile_id": "invoke.generic-design-baseline.v1", "evidence_ref": closure_ref},
            "dispatch_trace": {"techniques": ["exact-binding", "deterministic-projection"], "evidence_ref": closure_ref},
            "distill_contract": {"classification": "required", "validator_owner": "distill", "coherent_unit_candidate": "One W2 candidate producer", "split_pressure_question": "Would any split break exact W1-to-fact trace closure?", "expected_receipt": "DISTILL-RECEIPT.json"},
            "transport_policy": {"append_existing_only": True, "upstream_mutation": False, "targets": []},
            "next_route": "design-bundle-production", "authority_effect": "none", "source_digest": "0" * 64,
        }

    def compile(self, name: str, source: dict | None = None, late=None) -> int:
        if source is not None:
            self.write_source(source)
        return W2.compile_candidate(self.source_path, self.repo, self.repo / name, self.repo / f"{name}.attempt.json", self.schemas, late)

    def assert_block(self, name: str) -> dict:
        self.assertFalse((self.repo / name).exists())
        attempt = self.repo / f"{name}.attempt.json"
        self.assertTrue(attempt.is_file())
        receipt = json.loads(attempt.read_text())
        self.assertEqual("block", receipt["result"])
        self.assertTrue(receipt["blockers"])
        store = VALIDATOR.schema_store(self.schemas)
        self.assertEqual(
            [],
            VALIDATOR.schema_errors(
                receipt,
                store["https://arcanum.dev/schemas/invoke/design-candidate-production-receipt/v1"],
                store,
            ),
        )
        return receipt

    def test_normal_w1_to_atomic_w2_is_deterministic(self) -> None:
        self.assertEqual(0, self.compile("w2-repeat"))
        first = {item.name: item.read_bytes() for item in (self.repo / "w2-repeat").iterdir()}
        self.assertEqual({"DESIGN.json", "DESIGN-COHERENCE-RECEIPT.json", "DESIGN-CANDIDATE-PRODUCTION-RECEIPT.json"}, set(first))
        shutil.rmtree(self.repo / "w2-repeat")
        self.assertEqual(0, self.compile("w2-repeat"))
        second = {item.name: item.read_bytes() for item in (self.repo / "w2-repeat").iterdir()}
        self.assertEqual(first, second)
        receipt = json.loads((self.repo / "w2-repeat/DESIGN-CANDIDATE-PRODUCTION-RECEIPT.json").read_text())
        self.assertEqual("pass", receipt["result"])
        self.assertEqual("design-bundle-production", receipt["next_route"])
        self.assertFalse(receipt["evidence_ceiling"]["design_stage_pass"])

    def test_cli_exit_codes_are_zero_one_and_two(self) -> None:
        cli = self.repo / "arcanum/spells/invoke/scripts/compile_design_candidate.py"

        def run(source: Path, output: str, attempt: str) -> subprocess.CompletedProcess[str]:
            return subprocess.run(
                [
                    sys.executable, str(cli), str(source), "--repo-root", str(self.repo),
                    "--output-dir", str(self.repo / output),
                    "--attempt-receipt", str(self.repo / attempt),
                ],
                text=True, capture_output=True, check=False,
            )

        passed = run(self.source_path, "cli-pass", "cli-pass.attempt.json")
        self.assertEqual(0, passed.returncode, passed.stderr)
        self.assertTrue((self.repo / "cli-pass/DESIGN-CANDIDATE-PRODUCTION-RECEIPT.json").is_file())
        self.assertFalse((self.repo / "cli-pass.attempt.json").exists())

        blocked_source = copy.deepcopy(self.source)
        blocked_source["applications"] = blocked_source["applications"][:-1]
        self.write_source(blocked_source)
        blocked = run(self.source_path, "cli-block", "cli-block.attempt.json")
        self.assertEqual(1, blocked.returncode, blocked.stderr)
        self.assertFalse((self.repo / "cli-block").exists())
        self.assertTrue((self.repo / "cli-block.attempt.json").is_file())

        malformed = self.repo / "MALFORMED-DESIGN-SOURCE.json"
        malformed.write_text("{}\n", encoding="utf-8")
        failed = run(malformed, "cli-malformed", "cli-malformed.attempt.json")
        self.assertEqual(2, failed.returncode)
        self.assertFalse((self.repo / "cli-malformed").exists())
        self.assertFalse((self.repo / "cli-malformed.attempt.json").exists())

    def test_missing_ledger_pair_blocks_with_embedded_coherence_receipt(self) -> None:
        source = copy.deepcopy(self.source)
        source["applications"] = [item for item in source["applications"] if not (item["subject_kind"] == "input" and item["subject_id"] == "input:define")]
        self.assertEqual(1, self.compile("missing-ledger", source))
        receipt = self.assert_block("missing-ledger")
        self.assertIsNotNone(receipt["coherence_block_receipt"])
        self.assertEqual("block", receipt["coherence_block_receipt"]["verdict"])

    def test_lossy_signal_projection_blocks(self) -> None:
        source = copy.deepcopy(self.source)
        signal_fact = next(item for item in source["facts"] if item["fact_id"] == "rule:validate-inputs")
        signal_fact["attributes"]["object"] = "different object"
        self.assertEqual(1, self.compile("lossy-signal", source))
        receipt = self.assert_block("lossy-signal")
        self.assertIn("DESIGN_FACT_REGISTRY_INVALID", {item["code"] for item in receipt["coherence_block_receipt"]["diagnostics"]})

    def test_wrong_kind_workflow_operator_blocks(self) -> None:
        source = copy.deepcopy(self.source)
        workflow = {
            "fact_id": "workflow:compile", "fact_kind": "workflow-step", "name": "Compile candidate",
            "owner": "invoke-design-candidate-producer",
            "requirement_refs": [{"subject_kind": "selected-output", "subject_id": "architecture"}],
            "attributes": {"actor_or_component_id": "contract:w1-input", "action": "Compile the candidate.", "next_step_ids": []},
        }
        source["facts"].append(workflow)
        architecture = next(item for item in source["applications"] if item["subject_kind"] == "selected-output" and item["subject_id"] == "architecture")
        architecture["fact_ids"].append(workflow["fact_id"])
        source["views"]["workflow_process"]["fact_ids"].append(workflow["fact_id"])
        self.assertEqual(1, self.compile("wrong-workflow-operator", source))
        receipt = self.assert_block("wrong-workflow-operator")
        self.assertIn("DESIGN_FACT_REGISTRY_INVALID", {item["code"] for item in receipt["coherence_block_receipt"]["diagnostics"]})

    def test_evolution_is_explicitly_fail_closed_in_w2(self) -> None:
        closure = copy.deepcopy(self.fixture.closure)
        closure["design_kind"] = {
            "kind": "evolution",
            "prior_design_candidates": [{
                "artifact_ref": self.fixture.file_ref(self.fixture.no_prior_path),
                "stage_receipt_ref": self.fixture.file_ref(self.fixture.no_prior_path),
            }],
            "declared_delta_ids": ["delta:one"],
        }
        selection = json.loads((self.w1_dir / "DESIGN-SELECTION-RESULT.json").read_text())
        source = copy.deepcopy(self.source)
        source["design_kind"] = {
            "kind": "evolution",
            "predecessor_artifact_ref": self.fixture.file_ref(self.fixture.no_prior_path),
            "predecessor_stage_receipt_ref": self.fixture.file_ref(self.fixture.no_prior_path),
            "deltas": [{
                "delta_id": "delta:one", "change": "added", "prior_fact_id": None,
                "current_fact_id": "system:w1-target", "decision_ref": None,
                "rationale": "Represent the authored delta without admitting an unvalidated predecessor.",
            }],
        }
        source["applications"].append({
            "subject_kind": "evolution-delta", "subject_id": "delta:one", "disposition": "satisfied",
            "fact_ids": ["system:w1-target"], "evidence_refs": [], "decision_ref": None,
            "rationale": "Bind the declared delta to the current fact.",
        })
        for fact in source["facts"]:
            if fact["fact_id"] == "system:w1-target":
                fact["requirement_refs"].append({"subject_kind": "evolution-delta", "subject_id": "delta:one"})
        closure_receipt = json.loads((self.w1_dir / "DESIGN-INPUT-CLOSURE-RECEIPT.json").read_text())
        closure_receipt["prior_design_determination"] = {
            "kind": "evolution", "applicable_candidates": [{
                "artifact_ref": self.fixture.file_ref(self.fixture.no_prior_path),
                "stage_receipt_ref": self.fixture.file_ref(self.fixture.no_prior_path),
            }],
            "selected_candidate_ref": self.fixture.file_ref(self.fixture.no_prior_path),
        }
        artifact = PROJECTOR.project_design_artifact(
            source,
            self.exact(self.source_path),
            self.exact(self.repo / PROJECTOR.PROCESS_PATH),
            self.exact(self.repo / PROJECTOR.PROFILE_PATH),
            self.exact(self.repo / PROJECTOR.POLICY_PATH),
            selection,
        )
        issues = VALIDATOR.validate_semantics(
            source,
            artifact,
            closure,
            closure_receipt,
            json.loads((self.w1_dir / "DESIGN-SCOPE-MANIFEST.json").read_text()),
            selection,
            json.loads((self.repo / PROJECTOR.PROFILE_PATH).read_text()),
            artifact,
        )
        diagnostics = [item for values in issues.values() for item in values]
        self.assertTrue(any(
            item["code"] == "DESIGN_EVOLUTION_DELTA_INCOMPLETE"
            for item in diagnostics
        ))

    def test_discovery_w1_is_rejected_before_projection(self) -> None:
        w1_path = self.w1_dir / "DESIGN-INPUT-PRODUCTION-RECEIPT.json"
        w1 = json.loads(w1_path.read_text())
        w1["activation_kind"] = "discovery"
        w1["next_route"] = "input-review"
        w1["receipt_digest"] = digest_without(w1, "receipt_digest")
        self.write_json(w1_path, w1)
        source = copy.deepcopy(self.source)
        source["upstream_bindings"]["design_input_production_receipt_ref"] = self.exact(w1_path)
        self.assertEqual(1, self.compile("discovery-w1", source))
        receipt = self.assert_block("discovery-w1")
        self.assertEqual("block", receipt["stage_results"][0]["status"])
        self.assertFalse(receipt["evidence_ceiling"]["normal_w1_bound"])

    def test_invalid_w1_producer_identity_is_rejected(self) -> None:
        w1_path = self.w1_dir / "DESIGN-INPUT-PRODUCTION-RECEIPT.json"
        w1 = json.loads(w1_path.read_text())
        w1["producer"]["identity"] = "invoke.uninstalled-design-input-producer.v1"
        w1["receipt_digest"] = digest_without(w1, "receipt_digest")
        self.write_json(w1_path, w1)
        source = copy.deepcopy(self.source)
        source["upstream_bindings"]["design_input_production_receipt_ref"] = self.exact(w1_path)
        self.assertEqual(1, self.compile("invalid-w1-producer", source))
        receipt = self.assert_block("invalid-w1-producer")
        self.assertEqual("repair-w1-input", receipt["next_route"])
        self.assertFalse(receipt["evidence_ceiling"]["normal_w1_bound"])

    def test_core_semantic_drifts_block_without_publication(self) -> None:
        cases: list[tuple[str, object]] = []

        duplicate_pair = copy.deepcopy(self.source)
        duplicate_pair["applications"].append(copy.deepcopy(duplicate_pair["applications"][0]))
        cases.append(("duplicate-application", duplicate_pair))

        illegal_view = copy.deepcopy(self.source)
        illegal_view["views"]["context"]["fact_ids"].append("contract:w1-input")
        cases.append(("illegal-view", illegal_view))

        glossary_drift = copy.deepcopy(self.source)
        glossary_drift["glossary_application"]["unmapped_terms"] = ["unmapped-term"]
        cases.append(("glossary-drift", glossary_drift))

        witness_drift = copy.deepcopy(self.source)
        witness_app = next(item for item in witness_drift["applications"] if item["subject_kind"] == "planned-witness")
        witness_app["fact_ids"] = witness_app["fact_ids"][:-1]
        cases.append(("witness-drift", witness_drift))

        contract_drift = copy.deepcopy(self.source)
        constraint_app = next(item for item in contract_drift["applications"] if item["subject_kind"] == "constraint")
        constraint_app["disposition"] = "changed-by-exact-decision"
        constraint_app["decision_ref"] = self.exact(self.fixture.closure_path)
        cases.append(("contract-drift", contract_drift))

        orphan_fact = copy.deepcopy(self.source)
        orphan_fact["facts"].append({
            "fact_id": "risk:orphan", "fact_kind": "risk", "name": "Orphan risk",
            "owner": "design-input-owner",
            "requirement_refs": [{"subject_kind": "selected-output", "subject_id": "architecture"}],
            "attributes": {"risk": "This fact is intentionally absent from every view.", "mitigation": "Reject it."},
        })
        architecture_app = next(item for item in orphan_fact["applications"] if item["subject_kind"] == "selected-output" and item["subject_id"] == "architecture")
        architecture_app["fact_ids"].append("risk:orphan")
        cases.append(("orphan-fact", orphan_fact))

        self.assertTrue(self.source["selected_companions"])
        companion_drift = copy.deepcopy(self.source)
        companion_drift["selected_companions"][0]["fact_ids"] = companion_drift["selected_companions"][0]["fact_ids"][:1]
        cases.append(("companion-drift", companion_drift))

        target_drift = copy.deepcopy(self.source)
        target_drift["target_id"] = "target:different"
        cases.append(("target-drift", target_drift))

        for name, source in cases:
            with self.subTest(case=name):
                self.assertEqual(1, self.compile(name, source))
                receipt = self.assert_block(name)
                if name in {"duplicate-application", "target-drift"}:
                    self.assertEqual(
                        "ARTIFACT_PROJECTION_FAILED" if name == "duplicate-application" else "TARGET_BINDING_MISMATCH",
                        receipt["blockers"][0]["code"],
                    )
                    self.assertIsNone(receipt["coherence_block_receipt"])
                else:
                    self.assertIsNotNone(receipt["coherence_block_receipt"])

    def test_installed_profile_and_policy_drift_block(self) -> None:
        profile_drift = copy.deepcopy(self.source)
        profile_drift["profile_binding"]["profile_ref"]["sha256"] = "f" * 64
        self.assertEqual(1, self.compile("profile-drift", profile_drift))
        self.assert_block("profile-drift")

        policy_path = self.repo / PROJECTOR.POLICY_PATH
        policy = json.loads(policy_path.read_text())
        policy["policy_digest"] = "f" * 64
        self.write_json(policy_path, policy)
        self.assertEqual(1, self.compile("policy-drift", self.source))
        receipt = self.assert_block("policy-drift")
        self.assertEqual("repair-installed-contract", receipt["next_route"])

    def test_late_byte_mutation_blocks_without_publication(self) -> None:
        def mutate(staging: Path) -> None:
            with (staging / "DESIGN.json").open("ab") as handle:
                handle.write(b" ")
        self.assertEqual(1, self.compile("late-mutation", late=mutate))
        receipt = self.assert_block("late-mutation")
        self.assertEqual("OUTPUT_INVENTORY_MISMATCH", receipt["blockers"][0]["code"])

    def test_coherent_late_rewrite_is_revalidated_and_blocks(self) -> None:
        output_name = "late-coherent-rewrite"

        def rewrite_every_binding(staging: Path) -> None:
            source = json.loads(self.source_path.read_text())
            source["layering"]["decision"] = "A late hook must not replace the validated source epoch."
            self.write_source(source)
            source_ref = self.exact(self.source_path)
            selection = json.loads((self.w1_dir / "DESIGN-SELECTION-RESULT.json").read_text())
            process_ref = self.exact(self.repo / PROJECTOR.PROCESS_PATH)
            profile_ref = self.exact(self.repo / PROJECTOR.PROFILE_PATH)
            policy_ref = self.exact(self.repo / PROJECTOR.POLICY_PATH)
            artifact = PROJECTOR.project_design_artifact(
                source, source_ref, process_ref, profile_ref, policy_ref, selection,
            )
            artifact_path = staging / W2.ARTIFACT_NAME
            W2.write_json(artifact_path, artifact)
            artifact_data = artifact_path.read_bytes()
            artifact_ref = {
                "path": f"{output_name}/{W2.ARTIFACT_NAME}",
                "sha256": hashlib.sha256(artifact_data).hexdigest(),
                "size": len(artifact_data),
            }
            coherence = VALIDATOR.validate_design_coherence(
                self.source_path, artifact_path, artifact_ref, self.repo, self.schemas,
            )
            W2.write_json(staging / W2.COHERENCE_NAME, coherence)
            outputs = [
                W2.output_ref(artifact_path, "design-artifact"),
                W2.output_ref(staging / W2.COHERENCE_NAME, "coherence-receipt"),
            ]
            receipt = W2.make_receipt(
                source_ref,
                source["upstream_bindings"]["design_input_production_receipt_ref"],
                {"process": process_ref, "profile": profile_ref, "policy": policy_ref},
                self.exact(self.repo / W2.PRODUCER_PATH)["sha256"],
                "pass",
                outputs,
            )
            W2.write_json(staging / W2.RECEIPT_NAME, receipt)

        self.assertEqual(1, self.compile(output_name, late=rewrite_every_binding))
        receipt = self.assert_block(output_name)
        self.assertEqual("LATE_VALIDATION_FAILED", receipt["blockers"][0]["code"])
        self.assertFalse((self.repo / output_name).exists())

    def test_unsafe_or_preexisting_destinations_and_source_symlink_exit_without_receipt(self) -> None:
        preexisting = self.repo / "preexisting-output"
        preexisting.mkdir()
        with self.assertRaises(ValueError):
            W2.compile_candidate(
                self.source_path, self.repo, preexisting,
                self.repo / "preexisting-output.attempt.json", self.schemas,
            )
        self.assertFalse((self.repo / "preexisting-output.attempt.json").exists())

        source_link = self.repo / "DESIGN-SOURCE-LINK.json"
        source_link.symlink_to(self.source_path.name)
        with self.assertRaises(ValueError):
            W2.compile_candidate(
                source_link, self.repo, self.repo / "symlink-output",
                self.repo / "symlink-output.attempt.json", self.schemas,
            )
        self.assertFalse((self.repo / "symlink-output").exists())
        self.assertFalse((self.repo / "symlink-output.attempt.json").exists())

        def replace_validated_source_with_symlink(_: Path) -> None:
            preserved = self.repo / "DESIGN-SOURCE-PRESERVED.json"
            shutil.copy2(self.source_path, preserved)
            self.source_path.unlink()
            self.source_path.symlink_to(preserved.name)

        self.assertEqual(1, self.compile("late-source-symlink", late=replace_validated_source_with_symlink))
        receipt = self.assert_block("late-source-symlink")
        self.assertEqual("LATE_VALIDATION_FAILED", receipt["blockers"][0]["code"])

    def test_projector_rejects_duplicate_pairs_and_normalizes_nested_sets(self) -> None:
        selection = json.loads((self.w1_dir / "DESIGN-SELECTION-RESULT.json").read_text())
        refs = [self.exact(self.repo / PROJECTOR.PROCESS_PATH), self.exact(self.repo / PROJECTOR.PROFILE_PATH), self.exact(self.repo / PROJECTOR.POLICY_PATH)]
        source_ref = self.exact(self.source_path)
        first = PROJECTOR.project_design_artifact(self.source, source_ref, *refs, selection)
        shuffled = copy.deepcopy(self.source)
        shuffled["applications"].reverse()
        shuffled["facts"].reverse()
        for fact in shuffled["facts"]:
            fact["requirement_refs"].reverse()
        second = PROJECTOR.project_design_artifact(shuffled, source_ref, *refs, selection)
        self.assertEqual(first, second)
        duplicate = copy.deepcopy(self.source)
        duplicate["applications"].append(copy.deepcopy(duplicate["applications"][0]))
        with self.assertRaises(ValueError):
            PROJECTOR.project_design_artifact(duplicate, source_ref, *refs, selection)

    def test_all_thirteen_signal_adapters_reject_each_field_drift(self) -> None:
        selection = json.loads((self.w1_dir / "DESIGN-SELECTION-RESULT.json").read_text())
        contract_refs = [self.exact(self.repo / PROJECTOR.PROCESS_PATH), self.exact(self.repo / PROJECTOR.PROFILE_PATH), self.exact(self.repo / PROJECTOR.POLICY_PATH)]
        closure = json.loads(self.fixture.closure_path.read_text())
        cases = []
        for signal_class, values in closure["scope_signals"].items():
            fact_kind, identity_key, fields = VALIDATOR.SIGNAL_MAP[signal_class]
            for signal in values:
                for field in [identity_key, *fields]:
                    cases.append((signal_class, signal, fact_kind, identity_key, field))
        self.assertGreaterEqual(len(cases), 50)
        for index, (signal_class, signal, fact_kind, identity_key, field) in enumerate(cases):
            with self.subTest(signal_class=signal_class, field=field):
                source = copy.deepcopy(self.source)
                fact = next(item for item in source["facts"] if item["fact_id"] == signal[identity_key] and item["fact_kind"] == fact_kind)
                if field == identity_key:
                    fact["fact_id"] = f"{fact['fact_id']}:drift"
                else:
                    value = fact["attributes"][field]
                    if isinstance(value, bool):
                        fact["attributes"][field] = not value
                    elif isinstance(value, list):
                        fact["attributes"][field] = [*value, "drift"]
                    elif field == "semantic_change":
                        fact["attributes"][field] = "changed" if value != "changed" else "none"
                    elif field == "direction":
                        fact["attributes"][field] = "outbound" if value != "outbound" else "inbound"
                    elif field == "evidence_state":
                        fact["attributes"][field] = "design-validator-pass"
                    else:
                        fact["attributes"][field] = f"{value}-drift"
                self.write_source(source)
                artifact_path = self.repo / f"signal-mutation-{index}.json"
                try:
                    artifact = PROJECTOR.project_design_artifact(source, self.exact(self.source_path), *contract_refs, selection)
                    self.write_json(artifact_path, artifact)
                    try:
                        receipt = VALIDATOR.validate_design_coherence(self.source_path, artifact_path, self.exact(artifact_path), self.repo, self.schemas)
                    except VALIDATOR.ContractFailure:
                        continue
                    self.assertEqual("block", receipt["verdict"])
                    self.assertIn("DESIGN_FACT_REGISTRY_INVALID", {item["code"] for item in receipt["diagnostics"]})
                finally:
                    artifact_path.unlink(missing_ok=True)
        self.write_source(self.source)

    def test_selection_trace_preserves_required_recommended_and_na(self) -> None:
        self.assertEqual(0, self.compile("selection-trace"))
        artifact = json.loads((self.repo / "selection-trace/DESIGN.json").read_text())
        dispositions = {item["disposition"] for item in artifact["concern_trace"]}
        self.assertTrue({"required", "recommended", "not-applicable-with-rationale"} <= dispositions)
        na = next(item for item in artifact["concern_trace"] if item["disposition"] == "not-applicable-with-rationale")
        self.assertEqual([], na["fact_ids"])

    def test_total_catalog_denominator_includes_excluded_and_conditional_excluded(self) -> None:
        closure = copy.deepcopy(self.fixture.closure)
        evidence = self.fixture.file_ref(self.fixture.no_prior_path)
        closure["input_catalog"].extend([
            {**copy.deepcopy(closure["input_catalog"][0]), "input_id": "input:excluded", "classification": "excluded", "exclusion_evidence_ref": evidence},
            {**copy.deepcopy(closure["input_catalog"][0]), "input_id": "input:conditional-excluded", "classification": "conditional", "exclusion_evidence_ref": None},
        ])
        closure["conditional_input_resolutions"] = [{"input_id": "input:conditional-excluded", "outcome": "excluded", "evidence_ref": evidence, "owner": "design-input-owner"}]
        selection = json.loads((self.w1_dir / "DESIGN-SELECTION-RESULT.json").read_text())
        pairs = VALIDATOR.expected_application_pairs(closure, selection)
        self.assertIn(("input", "input:excluded"), pairs)
        self.assertIn(("input", "input:conditional-excluded"), pairs)
        self.assertIn(("conditional-resolution", "input:conditional-excluded"), pairs)

    def test_excluded_inputs_require_exact_upstream_evidence(self) -> None:
        closure = copy.deepcopy(self.fixture.closure)
        evidence = self.fixture.file_ref(self.fixture.no_prior_path)
        closure["input_catalog"].extend([
            {**copy.deepcopy(closure["input_catalog"][0]), "input_id": "input:excluded", "classification": "excluded", "exclusion_evidence_ref": evidence},
            {**copy.deepcopy(closure["input_catalog"][0]), "input_id": "input:conditional-excluded", "classification": "conditional", "exclusion_evidence_ref": None},
        ])
        closure["conditional_input_resolutions"] = [{"input_id": "input:conditional-excluded", "outcome": "excluded", "evidence_ref": evidence, "owner": "design-input-owner"}]
        source = copy.deepcopy(self.source)
        for subject_kind, subject_id in [
            ("input", "input:excluded"),
            ("input", "input:conditional-excluded"),
            ("conditional-resolution", "input:conditional-excluded"),
        ]:
            source["applications"].append({
                "subject_kind": subject_kind, "subject_id": subject_id,
                "disposition": "not-applicable-with-evidence", "fact_ids": [],
                "evidence_refs": [copy.deepcopy(evidence)], "decision_ref": None,
                "rationale": "Preserve the exact approved W1 exclusion.",
            })
        selection = json.loads((self.w1_dir / "DESIGN-SELECTION-RESULT.json").read_text())
        artifact = PROJECTOR.project_design_artifact(
            source, self.exact(self.source_path),
            self.exact(self.repo / PROJECTOR.PROCESS_PATH),
            self.exact(self.repo / PROJECTOR.PROFILE_PATH),
            self.exact(self.repo / PROJECTOR.POLICY_PATH), selection,
        )
        arguments = [
            source, artifact, closure,
            json.loads((self.w1_dir / "DESIGN-INPUT-CLOSURE-RECEIPT.json").read_text()),
            json.loads((self.w1_dir / "DESIGN-SCOPE-MANIFEST.json").read_text()),
            selection, json.loads((self.repo / PROJECTOR.PROFILE_PATH).read_text()), artifact,
        ]
        issues = VALIDATOR.validate_semantics(*arguments)
        self.assertEqual([], issues["rule:application-denominator"])

        drifted = copy.deepcopy(source)
        excluded = next(item for item in drifted["applications"] if item["subject_id"] == "input:excluded")
        excluded["evidence_refs"][0]["sha256"] = "f" * 64
        drifted_artifact = PROJECTOR.project_design_artifact(
            drifted, self.exact(self.source_path),
            self.exact(self.repo / PROJECTOR.PROCESS_PATH),
            self.exact(self.repo / PROJECTOR.PROFILE_PATH),
            self.exact(self.repo / PROJECTOR.POLICY_PATH), selection,
        )
        arguments[0], arguments[1], arguments[-1] = drifted, drifted_artifact, drifted_artifact
        issues = VALIDATOR.validate_semantics(*arguments)
        self.assertIn("DESIGN_APPLICATION_DENOMINATOR_INVALID", {item["code"] for item in issues["rule:application-denominator"]})


if __name__ == "__main__":
    unittest.main()
