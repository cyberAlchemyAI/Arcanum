from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_initial_definitions.py"
SECTIONS = [
    "Context",
    "Purpose",
    "Research Question (Can be refined)",
    "Confirmed Product Constraints",
    "Current Evidence Baseline",
    "Known Gaps",
]


def document(sections: list[str] | None = None, *, empty: str | None = None) -> str:
    selected = sections or SECTIONS
    parts = ["# Research Initial Definitions — Fixture", ""]
    for heading in selected:
        parts.extend([f"## {heading}", "" if heading == empty else f"Content for {heading}.", ""])
    return "\n".join(parts)


class ValidatorTests(unittest.TestCase):
    def run_validator(self, folder: Path, repo_root: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(VALIDATOR),
                str(folder),
                "--repo-root",
                str(repo_root),
                "--json",
            ],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_valid_document_passes(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo_root = Path(raw)
            folder = repo_root / "research" / "topic"
            folder.mkdir(parents=True)
            (folder / "research-initial-definitions.md").write_text(document(), encoding="utf-8")
            result = self.run_validator(folder, repo_root)
            payload = json.loads(result.stdout)
            self.assertEqual(result.returncode, 0)
            self.assertEqual(payload["status"], "pass")
            self.assertEqual(payload["sections"], SECTIONS)
            self.assertEqual(len(payload["sha256"]), 64)
            self.assertEqual(Path(payload["research_root"]), repo_root / "research")

    def test_nested_research_container_passes(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo_root = Path(raw)
            folder = repo_root / "any-parent" / "deeply" / "nested" / "research" / "topic"
            folder.mkdir(parents=True)
            (folder / "research-initial-definitions.md").write_text(document(), encoding="utf-8")
            result = self.run_validator(folder, repo_root)
            payload = json.loads(result.stdout)
            self.assertEqual(result.returncode, 0)
            self.assertEqual(Path(payload["research_root"]), folder.parent)

    def test_missing_document_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo_root = Path(raw)
            folder = repo_root / "research" / "missing"
            folder.mkdir(parents=True)
            result = self.run_validator(folder, repo_root)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(json.loads(result.stdout)["status"], "block")

    def test_wrong_order_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo_root = Path(raw)
            folder = repo_root / "research" / "topic"
            folder.mkdir(parents=True)
            wrong = [SECTIONS[1], SECTIONS[0], *SECTIONS[2:]]
            (folder / "research-initial-definitions.md").write_text(document(wrong), encoding="utf-8")
            result = self.run_validator(folder, repo_root)
            self.assertNotEqual(result.returncode, 0)

    def test_extra_level_two_section_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo_root = Path(raw)
            folder = repo_root / "research" / "topic"
            folder.mkdir(parents=True)
            (folder / "research-initial-definitions.md").write_text(
                document([*SECTIONS, "Methods"]), encoding="utf-8"
            )
            result = self.run_validator(folder, repo_root)
            self.assertNotEqual(result.returncode, 0)

    def test_empty_section_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo_root = Path(raw)
            folder = repo_root / "research" / "topic"
            folder.mkdir(parents=True)
            (folder / "research-initial-definitions.md").write_text(
                document(empty="Purpose"), encoding="utf-8"
            )
            result = self.run_validator(folder, repo_root)
            self.assertNotEqual(result.returncode, 0)

    def test_folder_without_research_ancestor_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo_root = Path(raw)
            folder = repo_root / "feature" / "topic"
            folder.mkdir(parents=True)
            (folder / "research-initial-definitions.md").write_text(document(), encoding="utf-8")
            result = self.run_validator(folder, repo_root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("literally named 'research'", " ".join(json.loads(result.stdout)["errors"]))

    def test_shared_research_container_cannot_be_working_folder(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo_root = Path(raw)
            folder = repo_root / "research"
            folder.mkdir()
            (folder / "research-initial-definitions.md").write_text(document(), encoding="utf-8")
            result = self.run_validator(folder, repo_root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("identify one research", " ".join(json.loads(result.stdout)["errors"]))

    def test_folder_outside_repository_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as repo_raw, tempfile.TemporaryDirectory() as other_raw:
            repo_root = Path(repo_raw)
            folder = Path(other_raw) / "research" / "topic"
            folder.mkdir(parents=True)
            (folder / "research-initial-definitions.md").write_text(document(), encoding="utf-8")
            result = self.run_validator(folder, repo_root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("inside repository root", " ".join(json.loads(result.stdout)["errors"]))


if __name__ == "__main__":
    unittest.main()
