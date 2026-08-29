#!/usr/bin/env python3
"""End-to-end and boundary fixtures for the governance-flow reference vertical."""

from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

import yaml
from jsonschema import Draft202012Validator


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_ROOT = PACKAGE_ROOT / "scripts"
sys.path.insert(0, str(SCRIPT_ROOT))

from compile_governance_flow import (  # noqa: E402
    GovernanceFlowError,
    canonical_bytes,
    compile_source,
    digest_document,
    load_json,
)
from render_governance_flow import render_graph, verify_human_view  # noqa: E402
from run_governance_flow import (  # noqa: E402
    accept_fixture,
    acceptance_is_exact,
    admit_fixture,
    blocker_timing_metric,
    can_auto_resume,
    classify_retry,
    collect_checks,
    descendant_is_current,
    emit_owner_request,
    execute_effects,
    freeze,
    graph_does_not_widen,
    is_bounded,
    make_owner_request,
    make_receipt,
    no_permissions,
    privacy_scan,
    receipt_edge_valid,
    rehearse,
    resume_governance_sidecar,
    review,
    run_environmental_retry,
    run_positive_fixture,
    select_fixture,
    terminal_complete,
)


POSITIVE = PACKAGE_ROOT / "development" / "fixtures" / "positive"
SOURCE_PATH = POSITIVE / "terminal-boundary-source.json"
EXECUTOR_PATH = POSITIVE / "terminal-boundary-executor.py"
EXPECTED_HUMAN = POSITIVE / "expected-human-view.md"
EXPECTED_TERMINAL = POSITIVE / "expected-terminal-receipt.json"
NEGATIVE_CASES = PACKAGE_ROOT / "development" / "fixtures" / "negative-cases.json"


class GovernanceFlowTests(unittest.TestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.source_bytes = SOURCE_PATH.read_bytes()
        self.source = json.loads(self.source_bytes.decode("utf-8"))

    def compile(self, source: dict | None = None) -> dict:
        value = copy.deepcopy(source if source is not None else self.source)
        exact_bytes = self.source_bytes if source is None else canonical_bytes(value)
        return compile_source(value, exact_bytes)

    def prepare_review(self, request_dir: Path | None = None) -> tuple[dict, str, dict, dict, dict]:
        graph = self.compile()
        human = render_graph(graph)
        rehearsal = rehearse(self.source, graph, human)
        frozen = freeze(graph, rehearsal)
        reviewed = review(graph, frozen, rehearsal, human)
        if request_dir is not None:
            emit_owner_request(graph, reviewed, human, request_dir)
        return graph, human, rehearsal, frozen, reviewed

    def test_schema_documents_are_draft_2020_12_valid(self) -> None:
        schema_root = PACKAGE_ROOT / "schemas"
        names = {
            "governance-flow-source-v1.schema.yml",
            "governance-flow-graph-v1.schema.yml",
            "governance-flow-stage-receipt-v1.schema.yml",
            "governance-flow-owner-request-v1.schema.yml",
        }
        self.assertEqual({path.name for path in schema_root.glob("*.schema.yml")}, names)
        for name in sorted(names):
            with self.subTest(schema=name):
                schema = yaml.safe_load((schema_root / name).read_text(encoding="utf-8"))
                Draft202012Validator.check_schema(schema)

    def test_p01_reaches_promised_terminal_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            result = run_positive_fixture(
                SOURCE_PATH,
                EXECUTOR_PATH,
                root / "isolated-root",
                root / "evidence",
            )
            self.assertEqual(result["human_view"], EXPECTED_HUMAN.read_text(encoding="utf-8"))
            self.assertEqual(result["terminal"], load_json(EXPECTED_TERMINAL))
            self.assertTrue(terminal_complete(result["graph"], result["terminal"]))
            self.assertEqual(
                (root / "isolated-root" / "outputs" / "result.txt").read_text(
                    encoding="utf-8"
                ),
                "governance-flow-terminal\n",
            )
            self.assertEqual(
                sorted(
                    str(path.relative_to(root / "isolated-root"))
                    for path in (root / "isolated-root").rglob("*")
                    if path.is_file()
                ),
                ["outputs/result.txt"],
            )
            chain = load_json(root / "evidence" / "chain.json")
            self.assertTrue(chain["strictly_bound"])
            self.assertTrue(chain["terminal_complete"])
            self.assertFalse(chain["successor_executed"])
            self.assertEqual(chain["external_calls"], 0)
            for metric in result["terminal"]["details"]["metrics"]:
                self.assertEqual(
                    metric["decision_graph_digest"],
                    result["graph"]["decision_graph_digest"],
                )
                self.assertTrue(metric["event_id"].startswith("gfr-metric-"))
                self.assertTrue(metric["evidence_edge"])
                self.assertEqual(metric["occurrence_count"], metric["value"])

    def case_n01_invalid_machine_source(self) -> str:
        invalid = copy.deepcopy(self.source)
        del invalid["owner"]
        with self.assertRaises(GovernanceFlowError):
            compile_source(invalid, canonical_bytes(invalid))
        return "source_schema"

    def case_n02_human_view_drift(self) -> str:
        graph = self.compile()
        with self.assertRaises(GovernanceFlowError):
            verify_human_view(graph, render_graph(graph) + "hand edit\n")
        return "human_renderer"

    def case_n03_multi_blocker_collect(self) -> str:
        definitions = [
            {"consumer_id": "one", "depends_on": []},
            {"consumer_id": "two", "depends_on": []},
            {"consumer_id": "three", "depends_on": []},
        ]
        visited: list[str] = []

        def failed(name: str, code: int):
            def check() -> tuple[bool, int, str]:
                visited.append(name)
                return False, code, name

            return check

        evaluated, blockers, first = collect_checks(
            definitions,
            {
                "one": failed("one", 7),
                "two": failed("two", 9),
                "three": failed("three", 11),
            },
        )
        self.assertEqual(visited, ["one", "three", "two"])
        self.assertEqual(len(evaluated), 3)
        self.assertEqual(len(blockers), 3)
        self.assertEqual(first, 7)
        return "preacceptance_collect_all"

    def case_n04_not_evaluable_causality(self) -> str:
        definitions = [
            {"consumer_id": "producer", "depends_on": []},
            {"consumer_id": "consumer", "depends_on": ["producer"]},
        ]
        evaluated, blockers, first = collect_checks(
            definitions,
            {
                "producer": lambda: (False, 8, "producer failed"),
                "consumer": lambda: (True, 0, "must not run"),
            },
        )
        self.assertEqual(len(blockers), 1)
        self.assertEqual(first, 8)
        self.assertEqual(evaluated[1]["status"], "not_evaluable")
        self.assertEqual(evaluated[1]["causal_blockers"], ["producer"])
        return "consumer_dependency"

    def case_n05_preparation_no_authority(self) -> str:
        with tempfile.TemporaryDirectory() as temporary:
            graph, human, rehearsal, frozen, reviewed = self.prepare_review()
            request = make_owner_request(graph, reviewed, human)
            self.assertFalse(any(graph["derived_permissions"].values()))
            for receipt in (rehearsal, frozen, reviewed):
                self.assertEqual(receipt["authority_effect"], "none")
                self.assertFalse(any(receipt["permissions"].values()))
            self.assertEqual(request["authority_effect"], "none")
            self.assertFalse(any(request["permissions"].values()))
        return "preparation_authority"

    def case_n06_stale_descendant(self) -> str:
        graph = self.compile()
        rehearsal = rehearse(self.source, graph, render_graph(graph))
        changed = copy.deepcopy(self.source)
        changed["risk"]["reasons"].append("changed semantic risk")
        new_graph = self.compile(changed)
        self.assertFalse(descendant_is_current(new_graph, rehearsal))
        with self.assertRaises(GovernanceFlowError):
            freeze(new_graph, rehearsal)
        return "digest_chain"

    def case_n07_duplicate_request(self) -> str:
        with tempfile.TemporaryDirectory() as temporary:
            graph, human, _, _, reviewed = self.prepare_review()
            request_dir = Path(temporary)
            first, first_created = emit_owner_request(graph, reviewed, human, request_dir)
            second, second_created = emit_owner_request(graph, reviewed, human, request_dir)
            self.assertTrue(first_created)
            self.assertFalse(second_created)
            self.assertEqual(canonical_bytes(first), canonical_bytes(second))
            self.assertEqual(len(list(request_dir.glob("*.json"))), 1)
            self.assertEqual(first["request_count"], 1)
            self.assertEqual(first["prompt_event_count"], 1)
        return "request_idempotency"

    def case_n08_missing_review(self) -> str:
        graph = self.compile()
        human = render_graph(graph)
        rehearsal = rehearse(self.source, graph, human)
        with self.assertRaises(GovernanceFlowError):
            make_owner_request(graph, rehearsal, human)
        return "independent_review"

    def case_n09_local_pass_no_terminal(self) -> str:
        graph = self.compile()
        self.assertFalse(terminal_complete(graph, None))
        return "terminal_dominance"

    def case_n10_wrong_terminal(self) -> str:
        graph = self.compile()
        wrong = make_receipt(
            stage="terminal",
            mode="effectful_execution",
            status="complete",
            graph_digest=graph["decision_graph_digest"],
            predecessor_digest="0" * 64,
            authority_effect="declared_local_effect",
            permissions=no_permissions(),
            details={
                "promised_boundary_id": "wrong-boundary",
                "required_terminal_receipt_schema": "governance-flow-stage-receipt-v1.schema.yml",
                "observed_effects": ["write:outputs/result.txt"],
                "observed_postimages": self.source["terminal_outcome"]["expected_postimages"],
                "prohibited_effects_observed": [],
                "successor_executed": False,
                "external_calls": 0,
                "authority_and_write_ceiling": ["outputs/result.txt"],
                "terminal_observer": self.source["terminal_outcome"]["terminal_observer"],
                "metrics": [],
                "completion_predicate": True,
                "aggregate_complete": True,
            },
        )
        self.assertFalse(terminal_complete(graph, wrong))
        return "terminal_predicate"

    def case_n11_effectful_fail_fast(self) -> str:
        observed: list[str] = []

        def first() -> None:
            observed.append("first")

        def fail() -> None:
            raise RuntimeError("effect failed")

        def later() -> None:
            observed.append("later")

        result = execute_effects([first, fail, later])
        self.assertEqual(result["status"], "block")
        self.assertEqual(result["failed_index"], 1)
        self.assertEqual(observed, ["first"])
        return "effect_fail_fast"

    def case_n12_environmental_retry(self) -> str:
        before = {
            "decision_graph_digest": "a",
            "target_byte_digest": "b",
            "semantic_digest": "c",
            "authority_digest": "d",
            "executable_digest": "e",
        }
        policy = next(
            item for item in self.source["retry_policy"] if item["classification"] == "environmental"
        )
        self.assertEqual(policy["maximum_attempts"], 1)
        self.assertEqual(policy["owner_prompt"], "none")
        attempts = 0

        def transient_then_pass() -> None:
            nonlocal attempts
            attempts += 1
            if attempts == 1:
                raise RuntimeError("transient")

        passed = run_environmental_retry(
            transient_then_pass, policy["maximum_attempts"], before, dict(before)
        )
        self.assertEqual(passed["status"], "pass")
        self.assertEqual(passed["attempts"], 2)
        self.assertEqual(passed["owner_prompt_count"], 0)
        exhausted = run_environmental_retry(
            lambda: (_ for _ in ()).throw(RuntimeError("still transient")),
            policy["maximum_attempts"],
            before,
            dict(before),
        )
        self.assertEqual(exhausted["status"], "block")
        self.assertEqual(exhausted["attempts"], 2)
        self.assertEqual(exhausted["owner_prompt_count"], 0)
        return "retry_environmental"

    def case_n13_mechanical_auto_resume(self) -> str:
        repair = {
            "classification": "mechanical_evidence_only",
            "independent_review": "pass",
            "decision_graph_unchanged": True,
            "target_bytes_unchanged": True,
            "executable_unchanged": True,
            "revalidation": "pass",
            "resume_count": 0,
        }
        observed: list[str] = []
        resumed = resume_governance_sidecar(
            repair, lambda: observed.append("continued") or "pass"
        )
        self.assertEqual(resumed["status"], "resumed")
        self.assertEqual(resumed["resume_count"], 1)
        self.assertEqual(observed, ["continued"])
        repair["resume_count"] += 1
        suspended = resume_governance_sidecar(
            repair, lambda: observed.append("must-not-run")
        )
        self.assertEqual(suspended["status"], "suspended")
        self.assertEqual(observed, ["continued"])
        return "sidecar_auto_resume"

    def case_n14_sidecar_no_resume(self) -> str:
        passing = {
            "classification": "mechanical_evidence_only",
            "independent_review": "pass",
            "decision_graph_unchanged": True,
            "target_bytes_unchanged": True,
            "executable_unchanged": True,
            "revalidation": "pass",
            "resume_count": 0,
        }
        mutations = {
            "classification": "semantic_or_authority",
            "independent_review": "block",
            "decision_graph_unchanged": False,
            "target_bytes_unchanged": False,
            "executable_unchanged": False,
            "revalidation": "block",
            "resume_count": 1,
        }
        for key, value in mutations.items():
            with self.subTest(predicate=key):
                candidate = dict(passing)
                candidate[key] = value
                self.assertFalse(can_auto_resume(candidate))
        return "sidecar_predicate"

    def case_n15_semantic_new_graph(self) -> str:
        before = {
            "decision_graph_digest": "a",
            "target_byte_digest": "b",
            "semantic_digest": "c",
            "authority_digest": "d",
            "executable_digest": "e",
        }
        after = dict(before)
        after["authority_digest"] = "changed"
        self.assertEqual(
            classify_retry(before, after, "mechanical_evidence_only"),
            "semantic_or_authority",
        )
        return "retry_semantic"

    def case_n16_exact_byte_acceptance(self) -> str:
        graph, human, _, _, reviewed = self.prepare_review()
        request = make_owner_request(graph, reviewed, human)
        acceptance = accept_fixture(graph, request)
        changed = copy.deepcopy(self.source)
        new_digest = "1" * 64
        changed["targets"][0]["postimage_sha256"] = new_digest
        changed["terminal_outcome"]["expected_postimages"]["outputs/result.txt"] = new_digest
        new_graph = self.compile(changed)
        self.assertFalse(acceptance_is_exact(new_graph, request, acceptance))
        with self.assertRaises(GovernanceFlowError):
            select_fixture(new_graph, acceptance)
        return "acceptance_binding"

    def case_n17_manual_receipt_transfer(self) -> str:
        valid, metric = receipt_edge_valid(
            {
                "producer_digest": "a",
                "consumer_input_digest": "a",
                "manual_transfer": True,
            }
        )
        self.assertFalse(valid)
        self.assertEqual(metric, 1)
        return "receipt_edge"

    def case_n18_late_discoverable_blocker(self) -> str:
        value = blocker_timing_metric(True, True)
        self.assertEqual(value, 1)
        self.assertNotEqual(value, 0)
        return "metric_blocker_timing"

    def case_n19_private_marker_public(self) -> str:
        self.assertFalse(privacy_scan("restricted-marker://fixture"))
        self.assertTrue(privacy_scan("project-agnostic public fixture"))
        return "public_privacy"

    def case_n20_graph_widening(self) -> str:
        graph = self.compile()
        widened = copy.deepcopy(graph)
        widened["decision_envelope"]["authority"]["publication"] = True
        widened["decision_graph_digest"] = digest_document(
            widened, omit="decision_graph_digest"
        )
        self.assertFalse(graph_does_not_widen(self.source, widened))
        malformed = copy.deepcopy(graph)
        del malformed["decision_envelope"]["owner"]["owner_id"]
        malformed["decision_graph_digest"] = digest_document(
            malformed, omit="decision_graph_digest"
        )
        self.assertFalse(graph_does_not_widen(self.source, malformed))
        return "graph_subset"

    def case_n21_boundless_slice(self) -> str:
        required = {item["consumer_id"] for item in self.source["consumers"]}
        self.assertFalse(is_bounded(required, required - {"terminal-contract"}, True))
        self.assertFalse(is_bounded(required, required, False))
        self.assertTrue(is_bounded(required, required, True))
        return "bounded_vertical"

    def test_negative_manifest_matches_executable_matrix(self) -> None:
        manifest = load_json(NEGATIVE_CASES)
        cases = manifest["cases"]
        expected_ids = {f"N{number:02d}" for number in range(1, 22)}
        observed_ids = {item["case_id"].split("-", 1)[0] for item in cases}
        self.assertEqual(observed_ids, expected_ids)
        self.assertEqual(len(cases), 21)
        methods = {
            item["case_id"]: getattr(
                self, "case_" + item["case_id"].lower().replace("-", "_")
            )
            for item in cases
        }
        for item in cases:
            with self.subTest(case_id=item["case_id"]):
                self.assertEqual(methods[item["case_id"]](), item["expected_boundary"])


if __name__ == "__main__":
    result = unittest.main(verbosity=2, exit=False).result
    print(
        f"governance-flow fixtures positive=1 negative=21 "
        f"tests_run={result.testsRun} failures={len(result.failures)} errors={len(result.errors)}"
    )
    raise SystemExit(0 if result.wasSuccessful() else 1)
