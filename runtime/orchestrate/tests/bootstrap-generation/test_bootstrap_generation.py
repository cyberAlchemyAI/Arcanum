#!/usr/bin/env python3

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any

import yaml


ARCANUM_ROOT = Path(__file__).resolve().parents[4]
BOOTSTRAP = ARCANUM_ROOT / "tools/bootstrap_arcanum.sh"
CANONICAL = ARCANUM_ROOT / "runtime/orchestrate"
GENERATOR = CANONICAL / "scripts/generate_runtime_package.py"
MANIFEST = json.loads((CANONICAL / "generation-manifest.json").read_text(encoding="utf-8"))


def split_skill(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise AssertionError(f"missing frontmatter: {path}")
    _, raw, body = text.split("---", 2)
    frontmatter = yaml.safe_load(raw)
    if not isinstance(frontmatter, dict):
        raise AssertionError(f"frontmatter must be an object: {path}")
    return frontmatter, body


def file_snapshot(root: Path) -> dict[str, bytes]:
    return {
        str(path.relative_to(root)): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc"
    }


class BootstrapGenerationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temp = tempfile.TemporaryDirectory()
        cls.target = Path(cls.temp.name) / "consumer"
        cls.target.mkdir()
        cls.completed = subprocess.run(
            [
                sys.executable,
                str(GENERATOR),
                "--target",
                str(cls.target),
                "--profiles",
                "repo-codex,repo-local,claude",
                "--force",
            ],
            cwd=ARCANUM_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        cls.packages = {
            "codex": cls.target / ".agents/skills/orchestrate",
            "local": cls.target / ".arcanum/runtime/orchestrate",
            "claude": cls.target / ".claude/skills/orchestrate",
        }

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temp.cleanup()

    def test_bootstrap_completes_for_declared_surfaces(self) -> None:
        self.assertEqual(self.completed.returncode, 0, self.completed.stderr or self.completed.stdout)
        for package in self.packages.values():
            self.assertTrue((package / "SKILL.md").is_file())
            self.assertTrue((package / "generation-manifest.json").is_file())

    def test_generated_skill_preserves_canonical_contract_and_body(self) -> None:
        canonical_frontmatter, canonical_body = split_skill(CANONICAL / "SKILL.md")
        generated_only = {"surface_kind", "runtime", "canonical_source", "alias_of", "generated_by", "mutation_policy"}
        expected_contract = {key: value for key, value in canonical_frontmatter.items() if key not in generated_only}
        for runtime, package in self.packages.items():
            frontmatter, body = split_skill(package / "SKILL.md")
            provenance = frontmatter.pop("metadata")
            actual_contract = frontmatter
            self.assertEqual(actual_contract, expected_contract)
            self.assertEqual(body, canonical_body)
            self.assertEqual(provenance["surface_kind"], "generated-native-runtime-package")
            self.assertEqual(provenance["runtime"], runtime)
            self.assertEqual(provenance["canonical_source"], "runtime/orchestrate/SKILL.md")
            self.assertEqual(provenance["mutation_policy"], "regenerate-from-canonical-source")

    def test_manifest_selected_support_is_byte_equal(self) -> None:
        for package in self.packages.values():
            for relative in MANIFEST["support_paths"]:
                source = CANONICAL / relative
                generated = package / relative
                if source.is_dir():
                    self.assertEqual(file_snapshot(generated), file_snapshot(source))
                else:
                    self.assertEqual(generated.read_bytes(), source.read_bytes())

    def test_authoring_tests_and_caches_are_not_installed(self) -> None:
        for package in self.packages.values():
            self.assertFalse((package / "tests").exists())
            self.assertEqual(list(package.rglob("__pycache__")), [])
            self.assertEqual(list(package.rglob("*.pyc")), [])

    def test_bootstrap_no_longer_contains_hardcoded_orchestrate_body(self) -> None:
        source = BOOTSTRAP.read_text(encoding="utf-8")
        self.assertNotIn("<installed-capabilities>", source)
        self.assertNotIn("Classify the request as authoring, refinement", source)
        self.assertIn('source_file="$arcanum_root/runtime/orchestrate/SKILL.md"', source)


if __name__ == "__main__":
    unittest.main()
