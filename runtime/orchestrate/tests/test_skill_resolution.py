#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "resolve_skill_route.py"
SPEC = importlib.util.spec_from_file_location("resolve_skill_route", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class SkillResolutionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def skill(self, relative: str) -> Path:
        target = self.root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("---\nname: test\n---\n", encoding="utf-8")
        return target

    def test_explicit_repository_route_has_first_precedence(self) -> None:
        route = self.skill("policy/special/SKILL.md")
        self.skill(".agents/skills/orchestrate/SKILL.md")
        result = MODULE.resolve(self.root, "codex", "orchestrate", explicit_repository_route=route.relative_to(self.root))
        self.assertEqual(result["source"], "explicit-repository-route")
        self.assertEqual(Path(result["path"]), route.resolve())

    def test_legacy_alias_resolves_repository_orchestrate(self) -> None:
        local = self.skill(".agents/skills/orchestrate/SKILL.md")
        global_alias = self.skill("global/arcanum-orchestrate/SKILL.md")
        result = MODULE.resolve(self.root, "codex", "unused", user_named_skill="arcanum-orchestrate", allow_global_fallback=True, global_candidate=global_alias)
        self.assertEqual(result["normalized_capability"], "orchestrate")
        self.assertEqual(Path(result["path"]), local.resolve())
        self.assertFalse(result["catalog_consulted"])

    def test_runtime_specific_repository_paths(self) -> None:
        codex = self.skill(".agents/skills/invoke/SKILL.md")
        claude = self.skill(".claude/skills/invoke/SKILL.md")
        self.assertEqual(Path(MODULE.resolve(self.root, "codex", "invoke")["path"]), codex.resolve())
        self.assertEqual(Path(MODULE.resolve(self.root, "claude", "invoke")["path"]), claude.resolve())

    def test_missing_local_package_blocks_unpermitted_fallback(self) -> None:
        global_candidate = self.skill("global/invoke/SKILL.md")
        with self.assertRaisesRegex(ValueError, "not permitted"):
            MODULE.resolve(self.root, "codex", "invoke", global_candidate=global_candidate)

    def test_missing_local_package_allows_explicit_fallback(self) -> None:
        global_candidate = self.skill("global/invoke/SKILL.md")
        result = MODULE.resolve(self.root, "codex", "invoke", allow_global_fallback=True, global_candidate=global_candidate)
        self.assertEqual(result["source"], "permitted-global-fallback")
        self.assertTrue(result["catalog_consulted"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
