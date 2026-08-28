#!/usr/bin/env python3
"""Focused documentation checks for the current Design successor CLI."""

from __future__ import annotations

import re
import unittest
from pathlib import Path


INVOKE = Path(__file__).resolve().parents[1]
HUMAN = INVOKE / "design/README.md"
GUIDE = INVOKE / "design-authoring-guide.md"
STAGE_GUIDES = (
    "design-input-authoring-guide.md",
    "design-source-authoring-guide.md",
    "design-bundle-authoring-guide.md",
)


class DesignAuthoringGuideV2Tests(unittest.TestCase):
    def test_guides_name_the_current_chain_and_public_commands(self) -> None:
        input_guide = (INVOKE / "design-input-authoring-guide.md").read_text(
            encoding="utf-8"
        )
        source_guide = (INVOKE / "design-source-authoring-guide.md").read_text(
            encoding="utf-8"
        )
        bundle_guide = (INVOKE / "design-bundle-authoring-guide.md").read_text(
            encoding="utf-8"
        )
        contract = (INVOKE / "design.md").read_text(encoding="utf-8")

        for required in (
            "tools/arcanum invoke design author boundary",
            "tools/arcanum invoke design author input-closure",
            "tools/arcanum invoke design produce input-bundle",
        ):
            self.assertIn(required, input_guide)
        self.assertIn("Define v3 stage receipt", input_guide)
        self.assertIn("Define admission v1", input_guide)

        self.assertIn("# Invoke Design Source v2 Authoring Guide", source_guide)
        self.assertIn("tools/arcanum invoke design author source", source_guide)
        self.assertIn("tools/arcanum invoke design produce candidate", source_guide)
        self.assertIn("Design v3 stage receipt", source_guide)
        self.assertIn("admission v2", source_guide)

        self.assertIn("tools/arcanum invoke design author bundle-closure", bundle_guide)
        self.assertIn("tools/arcanum invoke design produce final-bundle", bundle_guide)
        self.assertIn("tools/arcanum invoke design admit admission", bundle_guide)
        self.assertIn("v3 stage receipt", bundle_guide)

        self.assertIn("W1 v2, W2 v2, and W3 v3", contract)
        self.assertNotIn("W4 generated-package synchronization unreleased", contract)

        guide = GUIDE.read_text(encoding="utf-8")
        for required in (
            "tools/arcanum invoke modes",
            "tools/arcanum invoke design describe",
            "tools/arcanum invoke design check boundary",
            "tools/arcanum invoke design author boundary",
            "tools/arcanum invoke design check input-closure",
            "tools/arcanum invoke design author input-closure",
            "tools/arcanum invoke design produce input-bundle",
            "tools/arcanum invoke design check source",
            "tools/arcanum invoke design author source",
            "tools/arcanum invoke design produce candidate",
            "tools/arcanum invoke design check bundle-closure",
            "tools/arcanum invoke design author bundle-closure",
            "tools/arcanum invoke design produce final-bundle",
            "tools/arcanum invoke design admit admission",
            "tools/arcanum invoke design status",
        ):
            self.assertIn(required, guide)

        for required in (
            "current Define v3 stage + admission v1",
            "W1 v2 input bundle",
            "W2 v2 candidate",
            "W3 v3 final bundle",
            "independent admission v2",
            "external Distill",
            "Greenfield And Evolution",
            "absent",
            "atomic",
            "Exit `0`",
            "Exit `1`",
            "Exit `2`",
            "Retell-Chain Check",
            "Claim Ceiling",
        ):
            self.assertIn(required, guide)

    def test_human_overview_uses_concrete_returns_language_and_claims_only_checked_design(
        self,
    ) -> None:
        human = HUMAN.read_text(encoding="utf-8")
        folded = human.casefold()
        for required in (
            "returns service",
            "inspection component",
            "returninspected",
            "refund service",
            "inspection window",
            "payment provider",
            "responsibility",
            "interface",
            "event",
            "state",
            "decision",
            "dependency",
            "design.json",
        ):
            self.assertIn(required, folded)

        for required_heading in (
            "## Why Design follows Define",
            "## Why Design comes before Plan",
            "## Questions Design answers",
            "## From checked definitions to a checked design",
            "## A returns example",
            "## When Design must check again",
            "## What Design does not approve",
            "## Continue from here",
        ):
            self.assertIn(required_heading, human)

        for forbidden_claim in ("correct architecture", "optimal architecture"):
            self.assertNotIn(forbidden_claim, folded)

        self.assertRegex(human, r"(?s)does not automatically:.*change application code")
        self.assertRegex(human, r"(?s)does not automatically:.*approve an implementation plan")
        self.assertRegex(human, r"(?s)does not automatically:.*authorize execution")
        self.assertNotRegex(
            human,
            r"(?im)^\s*(?:preserve meaning|architectural drift|ensure coherence)\.?\s*$",
        )

    def test_unified_guide_assigns_decisions_and_results_to_their_real_owners(
        self,
    ) -> None:
        guide = GUIDE.read_text(encoding="utf-8")
        for owner_statement in (
            "Target owner. The CLI can record this approval but cannot grant it.",
            "Design author, backed by admitted inputs and explicit owner decisions.",
            "CLI and installed producers.",
            "Their independent validators.",
            "External Distill owners.",
        ):
            self.assertIn(owner_statement, guide)
        for concrete_view in (
            "Context",
            "High-level structure",
            "Low-level components",
            "Workflow process",
            "Decision flow",
            "Dependency interface",
        ):
            self.assertIn(f"**{concrete_view}**", guide)
        self.assertIn("The CLI records those supplied decisions", guide)
        self.assertIn("it does not choose them", guide)

    def test_root_contract_and_stage_guides_link_both_entrypoints(self) -> None:
        root = (INVOKE / "README.md").read_text(encoding="utf-8")
        contract = (INVOKE / "design.md").read_text(encoding="utf-8")
        self.assertIn("[Human overview](./design/README.md)", root)
        self.assertIn("[Agent authoring guide](./design-authoring-guide.md)", root)
        self.assertIn("[Design overview](./design/README.md)", contract)
        self.assertIn("[Design authoring guide](./design-authoring-guide.md)", contract)
        for name in STAGE_GUIDES:
            content = (INVOKE / name).read_text(encoding="utf-8")
            self.assertIn("[Design authoring guide](design-authoring-guide.md)", content)

    def test_relative_markdown_links_resolve(self) -> None:
        paths = [HUMAN, GUIDE, *(INVOKE / name for name in STAGE_GUIDES)]
        for path in paths:
            content = path.read_text(encoding="utf-8")
            for target in re.findall(r"\[[^]]+\]\(([^)#]+)(?:#[^)]+)?\)", content):
                if "://" not in target:
                    self.assertTrue((path.parent / target).exists(), f"{path.name}: {target}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
