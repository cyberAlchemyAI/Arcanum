#!/usr/bin/env python3
"""Regression tests for machine-first criterion and read-only guide controls."""

from __future__ import annotations

import copy
import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from render_criterion import render_criterion
from validate_criterion import validate as validate_criterion
from verify_guide_equivalence import verify as verify_guides



class TournamentControlTests(unittest.TestCase):
    def copy_package(self) -> Path:
        temp = Path(tempfile.mkdtemp(prefix="criterion-controls-"))
        self.addCleanup(shutil.rmtree, temp, True)
        target = temp / "tournament"
        target.mkdir()
        for name in ("CRITERION.json", "criterion.schema.json", "CRITERION.md", "GUIDE-MANIFEST.json"):
            shutil.copy2(ROOT / name, target / name)
        for name in ("content", "guides", "shared"):
            shutil.copytree(ROOT / name, target / name)
        return target

    def write_json(self, root: Path, value: dict) -> None:
        (root / "CRITERION.json").write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")

    def test_current_machine_source_and_generated_view_pass(self) -> None:
        result = validate_criterion(ROOT)
        self.assertEqual(result["status"], "pass", result["blockers"])
        criterion = json.loads((ROOT / "CRITERION.json").read_text(encoding="utf-8"))
        self.assertEqual((ROOT / "CRITERION.md").read_text(encoding="utf-8"), render_criterion(criterion))

    def test_every_arithmetic_invariant_fails_closed(self) -> None:
        mutations = {
            "candidate_count": lambda value: value["design"]["candidate_structures"].pop(),
            "case_count": lambda value: value["design"].update({"case_count": 4}),
            "trials_per_candidate": lambda value: value["design"].update({"trials_per_candidate": 3}),
            "sources_per_trial": lambda value: value["design"].update({"sources_per_trial": 4}),
            "total_trials": lambda value: value["design"].update({"total_trials": 7}),
            "total_source_records": lambda value: value["design"].update({"total_source_records": 19}),
            "candidate_aggregate_count": lambda value: value["design"].update({"candidate_aggregate_count": 4}),
            "metric_count": lambda value: value["observable"]["metrics"].pop(),
        }
        baseline = json.loads((ROOT / "CRITERION.json").read_text(encoding="utf-8"))
        for invariant, mutate in mutations.items():
            with self.subTest(invariant=invariant):
                root = self.copy_package()
                candidate = copy.deepcopy(baseline)
                mutate(candidate)
                self.write_json(root, candidate)
                result = validate_criterion(root)
                self.assertEqual(result["status"], "block")
                self.assertTrue(any(f"invariant:{invariant}" in blocker for blocker in result["blockers"]), result["blockers"])

    def test_schema_error_and_metric_order_mismatch_fail(self) -> None:
        root = self.copy_package()
        criterion = json.loads((root / "CRITERION.json").read_text(encoding="utf-8"))
        criterion["state"]["status"] = "accepted"
        criterion["outcome_rule"]["metric_order"] = list(reversed(criterion["outcome_rule"]["metric_order"]))
        self.write_json(root, criterion)
        result = validate_criterion(root)
        self.assertEqual(result["status"], "block")
        self.assertTrue(any(blocker.startswith("schema:state.status") for blocker in result["blockers"]))
        self.assertTrue(any("outcome metric_order" in blocker for blocker in result["blockers"]))

    def test_generated_view_drift_and_four_candidate_regression_fail(self) -> None:
        root = self.copy_package()
        text = (root / "CRITERION.md").read_text(encoding="utf-8")
        (root / "CRITERION.md").write_text(text.replace("three candidate aggregate tuples", "four candidate aggregate tuples"), encoding="utf-8")
        result = validate_criterion(root)
        self.assertEqual(result["status"], "block")
        self.assertTrue(any("clean in-memory render" in blocker for blocker in result["blockers"]))
        self.assertTrue(any("four-candidate" in blocker for blocker in result["blockers"]))

    def test_guide_manifest_and_guide_tampering_fail(self) -> None:
        for target in ("GUIDE-MANIFEST.json", "guides/guide-alpha.md"):
            with self.subTest(target=target):
                root = self.copy_package()
                path = root / target
                path.write_bytes(path.read_bytes() + b"\nTAMPER\n")
                result = verify_guides(root)
                self.assertEqual(result["status"], "block")

    def test_missing_extra_or_changed_shared_sections_fail(self) -> None:
        mutations = {
            "missing": lambda root: (root / "content/09-validation.md").unlink(),
            "extra": lambda root: (root / "content/10-extra.md").write_text("## Extra\n", encoding="utf-8"),
            "changed": lambda root: (root / "content/01-artifact-boundary.md").write_text("## Changed\n", encoding="utf-8"),
        }
        for name, mutate in mutations.items():
            with self.subTest(name=name):
                root = self.copy_package()
                mutate(root)
                result = verify_guides(root)
                self.assertEqual(result["status"], "block")

    def test_forbidden_reviewer_scope_mutations_fail(self) -> None:
        repo = next(parent for parent in ROOT.parents if (parent / "ops/development/2026-08-27-invoke-define-v2-documentation-tournament").is_dir())
        validator_path = repo / "ops/development/2026-08-27-invoke-define-v2-documentation-tournament/validate_criterion_successor.py"
        spec = importlib.util.spec_from_file_location("criterion_successor_validator_tests", validator_path)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader if spec else None)
        module = importlib.util.module_from_spec(spec)
        assert spec is not None and spec.loader is not None
        spec.loader.exec_module(module)
        dispatch = json.loads(module.DISPATCH.read_text(encoding="utf-8"))
        mutations = {
            "guide_reads_oracle": lambda roles: roles["guide-equivalence-auditor"]["briefing_binding"]["briefing"]["read_policy"]["allowed_read_scopes"].append(
                "arcanum/spells/invoke/development/define-v2-documentation/tournament/oracle/"
            ),
            "guide_omits_scorer_forbidden": lambda roles: roles["guide-equivalence-auditor"]["briefing_binding"]["briefing"]["read_policy"]["forbidden_read_scopes"].remove(
                "arcanum/spells/invoke/development/define-v2-documentation/tournament/score_tournament.py"
            ),
            "skeptic_reads_raw_guides": lambda roles: roles["validity-skeptic"]["briefing_binding"]["briefing"]["read_policy"]["allowed_read_scopes"].append(
                "arcanum/spells/invoke/development/define-v2-documentation/tournament/guides/"
            ),
            "skeptic_omits_manifest_forbidden": lambda roles: roles["validity-skeptic"]["briefing_binding"]["briefing"]["read_policy"]["forbidden_read_scopes"].remove(
                "arcanum/spells/invoke/development/define-v2-documentation/tournament/GUIDE-MANIFEST.json"
            ),
        }
        for name, mutate in mutations.items():
            with self.subTest(name=name):
                candidate = copy.deepcopy(dispatch)
                candidate_roles = {
                    role["role_id"]: role
                    for role in candidate["subagent_strategy"]["roles"]
                }
                mutate(candidate_roles)
                self.assertTrue(module.topology_blockers(candidate))


if __name__ == "__main__":
    unittest.main()
