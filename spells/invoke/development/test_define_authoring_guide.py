#!/usr/bin/env python3
"""Stable documentation and exact mixed-example checks for Define v3."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


INVOKE = Path(__file__).resolve().parents[1]
ARCANUM = INVOKE.parents[1]
REPO = ARCANUM.parent
GUIDE = INVOKE / "define-authoring-guide.md"
EXAMPLE = INVOKE / "examples/define-v3"
SOURCE = EXAMPLE / "DEFINE-SOURCE.json"
CONTEXT = EXAMPLE / "DEFINE-SEMANTIC-CONTEXT.json"
CLOSURE = EXAMPLE / "DEFINE-SEMANTIC-CLOSURE-RECEIPT.json"
SCHEMAS = INVOKE / "schemas"
W1 = INVOKE / "scripts/validate_define_semantic_closure.py"
COMPILER = INVOKE / "scripts/compile_define_source_v3.py"
ADMISSION = INVOKE / "scripts/validate_define_bundle_admission.py"


class DefineAuthoringGuideTests(unittest.TestCase):
    def test_guide_is_canonical_clear_and_not_evaluation_coupled(self) -> None:
        guide = GUIDE.read_text(encoding="utf-8")
        self.assertIn("./examples/define-v3/DEFINE-SOURCE.json", guide)
        self.assertIn("Retell-Chain Check", guide)
        self.assertIn("The Eight-Step Authoring Path", guide)
        self.assertIn("Inventory intent before probes", guide)
        self.assertIn("Apply a semantic quotient before selecting probes", guide)
        self.assertIn("Control-vocabulary test", guide)
        self.assertIn("Authority-reference test", guide)
        self.assertIn("Domain-role test", guide)
        self.assertIn("candidate obligation denominator", guide)
        self.assertIn("Materialize relation direction and boundary fields", guide)
        self.assertIn("semantic_disposition: retain-and-reassess", guide)
        self.assertIn("authority_disposition", guide)
        self.assertIn("enumerated semantic obligation", guide)
        self.assertNotIn("development/define-v3-documentation", guide)
        for forbidden in ("tournament", "benchmark", "trial"):
            self.assertNotIn(forbidden, guide.casefold())

        define_contract = (INVOKE / "define.md").read_text(encoding="utf-8")
        root_contract = (INVOKE / "README.md").read_text(encoding="utf-8")
        self.assertIn("./define-authoring-guide.md", define_contract)
        self.assertIn("./define-authoring-guide.md", root_contract)
        self.assertIn("./schemas/define-semantic-context-v2.schema.json", guide)
        self.assertIn("./schemas/define-semantic-closure-receipt-v2.schema.json", guide)
        self.assertIn("./schemas/define-bundle-admission-receipt-v2.schema.json", guide)
        self.assertIn("invoke.generic-definitions-baseline.v3", define_contract)
        self.assertIn("version: 0.6.0", root_contract)
        self.assertIn("tools/arcanum invoke define author semantic-context", guide)
        self.assertIn("tools/arcanum invoke define produce bundle", guide)
        self.assertIn("tools/arcanum invoke define admit admission", guide)

    def test_guide_names_every_required_context_source_definition_binding_and_application_field(self) -> None:
        guide = GUIDE.read_text(encoding="utf-8")
        context_schema = json.loads((SCHEMAS / "define-semantic-context-v1.schema.json").read_text())
        source_schema = json.loads((SCHEMAS / "define-source-v3.schema.json").read_text())
        definitions_v1 = json.loads((SCHEMAS / "definitions.schema.json").read_text())
        definitions_v2 = json.loads((SCHEMAS / "definitions-v2.schema.json").read_text())

        required_groups = (
            context_schema["required"],
            source_schema["required"],
            definitions_v1["$defs"]["definition"]["required"],
            definitions_v2["$defs"]["authorityBinding"]["required"],
            definitions_v2["$defs"]["semanticApplication"]["required"],
        )
        for fields in required_groups:
            for field in fields:
                self.assertIn(f"`{field}`", guide, field)

        required_values = {
            "reuse-existing",
            "new-scoped-term",
            "specialize-existing",
            "reuse",
            "specialization-basis",
            "design",
            "spellcraft",
            "sigil-development",
            "deferred",
            "operator-reading",
            "local-inference",
            "synthesis",
            "method-vocabulary",
            "domain-vocabulary",
            "historical",
            "references",
            "depends-on",
            "contrasts-with",
            "public",
            "private",
            "heading",
            "anchor",
            "line-span",
            "json-pointer",
            "yaml-path",
            "symbol",
            "contradiction",
            "scope",
            "evidence",
            "authority",
            "machine-checkable",
        }
        for value in sorted(required_values):
            self.assertIn(f"`{value}`", guide, value)

    def test_every_relative_markdown_link_resolves(self) -> None:
        guide = GUIDE.read_text(encoding="utf-8")
        targets = re.findall(r"\[[^]]+\]\((\./[^)#]+)(?:#[^)]+)?\)", guide)
        self.assertGreater(len(targets), 8)
        for target in targets:
            with self.subTest(target=target):
                self.assertTrue((INVOKE / target[2:]).exists(), target)

    def test_mixed_example_regenerates_closure_compiles_deterministically_and_admits(self) -> None:
        with tempfile.TemporaryDirectory(prefix=".define-v3-guide-", dir=INVOKE / "development") as temp:
            run = Path(temp)
            regenerated = run / "closure.json"
            closure_result = subprocess.run(
                [
                    sys.executable,
                    str(W1),
                    str(CONTEXT),
                    "--repository-root",
                    str(REPO),
                    "--context-schema",
                    str(SCHEMAS / "define-semantic-context-v1.schema.json"),
                    "--receipt-schema",
                    str(SCHEMAS / "define-semantic-closure-receipt-v1.schema.json"),
                    "--discovery-root",
                    "arcanum/spells/invoke/examples/define-v3",
                    "--public-root",
                    "arcanum",
                    "--output",
                    str(regenerated),
                ],
                cwd=REPO,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(0, closure_result.returncode, closure_result.stdout + closure_result.stderr)
            self.assertEqual(CLOSURE.read_bytes(), regenerated.read_bytes())
            closure = json.loads(regenerated.read_text())
            self.assertEqual("ready-for-define", closure["outcome"])
            self.assertEqual(
                ["reuse-existing", "new-scoped-term", "specialize-existing"],
                [item["disposition"] for item in closure["probe_results"]],
            )

            bundles = [run / "bundle-one", run / "bundle-two"]
            for bundle in bundles:
                completed = subprocess.run(
                    [
                        sys.executable,
                        str(COMPILER),
                        str(SOURCE),
                        "--output-dir",
                        str(bundle),
                        "--repo-root",
                        str(REPO),
                        "--schema-dir",
                        str(SCHEMAS),
                        "--discovery-root",
                        "arcanum/spells/invoke/examples/define-v3",
                        "--public-root",
                        "arcanum",
                    ],
                    cwd=REPO,
                    check=False,
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)
                self.assertEqual(13, len(list(bundle.iterdir())))

            self.assertEqual(
                {path.name: path.read_bytes() for path in bundles[0].iterdir()},
                {path.name: path.read_bytes() for path in bundles[1].iterdir()},
            )
            stage = json.loads((bundles[0] / "INVOKE-DEFINE-STAGE-RECEIPT.json").read_text())
            self.assertEqual("mixed", stage["semantic_outcome"])
            self.assertEqual(12, len(stage["outputs"]))

            admission_path = run / "admission.json"
            admitted = subprocess.run(
                [
                    sys.executable,
                    str(ADMISSION),
                    "--repo-root",
                    str(REPO),
                    "--bundle-root",
                    str(bundles[0]),
                    "--schema-dir",
                    str(SCHEMAS),
                    "--output",
                    str(admission_path),
                ],
                cwd=REPO,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(0, admitted.returncode, admitted.stdout + admitted.stderr)
            admission = json.loads(admission_path.read_text())
            self.assertEqual("pass", admission["result"])
            self.assertEqual("current", admission["drift_analysis"]["summary"]["overall"])
            self.assertEqual(13, len(admission["output_inventory"]))


if __name__ == "__main__":
    unittest.main()
