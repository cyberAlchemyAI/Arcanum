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
    "Research Questions (Can be refined)",
    "Confirmed Product Constraints",
    "Current Evidence Baseline",
    "Known Gaps",
]
VALID_QUESTIONS = """### Program question

**RQ-00.** What must be understood?

### Contract

1. **RQ-01.** Which contract applies?

### Compatibility

2. **RQ-02.** Which compatibility boundary applies?"""


def document(
    sections: list[str] | None = None,
    *,
    empty: str | None = None,
    questions: str = VALID_QUESTIONS,
) -> str:
    selected = sections or SECTIONS
    parts = ["# Research Initial Definitions — Fixture", ""]
    for heading in selected:
        if heading == empty:
            content = ""
        elif heading == "Research Questions (Can be refined)":
            content = questions
        else:
            content = f"Content for {heading}."
        parts.extend([f"## {heading}", content, ""])
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
            self.assertEqual(payload["question_ids"], ["RQ-00", "RQ-01", "RQ-02"])
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

    def test_legacy_singular_research_question_section_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo_root = Path(raw)
            folder = repo_root / "research" / "topic"
            folder.mkdir(parents=True)
            legacy = [
                *SECTIONS[:2],
                "Research Question (Can be refined)",
                *SECTIONS[3:],
            ]
            (folder / "research-initial-definitions.md").write_text(
                document(legacy), encoding="utf-8"
            )
            result = self.run_validator(folder, repo_root)
            self.assertNotEqual(result.returncode, 0)

    def test_research_questions_without_questions_block(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo_root = Path(raw)
            folder = repo_root / "research" / "topic"
            folder.mkdir(parents=True)
            (folder / "research-initial-definitions.md").write_text(
                document(questions="Content without any question."), encoding="utf-8"
            )
            result = self.run_validator(folder, repo_root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Program question", " ".join(json.loads(result.stdout)["errors"]))

    def test_research_questions_without_supporting_question_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo_root = Path(raw)
            folder = repo_root / "research" / "topic"
            folder.mkdir(parents=True)
            questions = """### Program question

**RQ-00.** What must be understood?

### Empty theme"""
            (folder / "research-initial-definitions.md").write_text(
                document(questions=questions), encoding="utf-8"
            )
            result = self.run_validator(folder, repo_root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("no supporting questions", " ".join(json.loads(result.stdout)["errors"]))

    def test_noncontinuous_question_identifiers_block(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo_root = Path(raw)
            folder = repo_root / "research" / "topic"
            folder.mkdir(parents=True)
            questions = VALID_QUESTIONS.replace("1. **RQ-01.**", "1. **RQ-02.**")
            (folder / "research-initial-definitions.md").write_text(
                document(questions=questions), encoding="utf-8"
            )
            result = self.run_validator(folder, repo_root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("continuous and matching", " ".join(json.loads(result.stdout)["errors"]))

    def test_headings_inside_fenced_code_do_not_satisfy_structure(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo_root = Path(raw)
            folder = repo_root / "research" / "topic"
            folder.mkdir(parents=True)
            fenced = f"```markdown\n{document()}\n```\n"
            (folder / "research-initial-definitions.md").write_text(fenced, encoding="utf-8")
            result = self.run_validator(folder, repo_root)
            self.assertNotEqual(result.returncode, 0)

    def test_fenced_fake_heading_does_not_invalidate_document(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            repo_root = Path(raw)
            folder = repo_root / "research" / "topic"
            folder.mkdir(parents=True)
            artifact = document().replace(
                "Content for Context.",
                "```markdown\n## Methods\n```\nContent for Context.",
            )
            (folder / "research-initial-definitions.md").write_text(
                artifact, encoding="utf-8"
            )
            result = self.run_validator(folder, repo_root)
            self.assertEqual(result.returncode, 0, result.stdout)

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
