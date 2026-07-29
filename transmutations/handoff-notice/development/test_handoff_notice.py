#!/usr/bin/env python3
"""Deterministic contract tests for the Handoff Notice runtime."""

from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ARTIFACT_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ARTIFACT_ROOT / "scripts" / "handoff_notice.py"
SPEC = importlib.util.spec_from_file_location("handoff_notice_runtime", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"unable to load {SCRIPT}")
RUNTIME = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNTIME)


def git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def payload(
    *,
    created_at: str = "2026-07-29T12:00:00Z",
    subject: str = "Review the prototype handoff",
) -> dict:
    return {
        "schema_version": "0.1.0",
        "notice_type": "session-handoff",
        "to": {"kind": "person", "label": "Review partner"},
        "from": {"kind": "agent", "label": "Working agent"},
        "subject": subject,
        "project_scope": "projects/example",
        "status": "open",
        "created_at": created_at,
        "why_now": "A bounded prototype is ready for review.",
        "key_points": [
            "The local round-trip is implemented.",
            "Remote availability has not been verified.",
        ],
        "open_calls": [
            {
                "owner": "Review partner",
                "question": "Is the message sufficient to continue the work?",
                "status": "open",
            }
        ],
        "boundaries": [
            "Do not treat this notice as permission to mutate or publish."
        ],
        "next_actions": [
            {
                "owner": "Review partner",
                "action": "Resolve the locator and inspect the source evidence.",
            }
        ],
        "source_refs": [
            {
                "ref": "projects/example/PROTOTYPE.md",
                "label": "Prototype evidence",
            }
        ],
        "next_route": {
            "capability": "task-session",
            "mode": "execute",
            "target": "EXAMPLE-001",
            "authorization": "not-granted",
        },
    }


class HandoffNoticeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp.name) / "repo"
        self.repo.mkdir()
        self.assertEqual(git(self.repo, "init", "-q").returncode, 0)
        self.assertEqual(
            git(self.repo, "config", "user.email", "test@example.invalid").returncode,
            0,
        )
        self.assertEqual(
            git(self.repo, "config", "user.name", "Handoff Test").returncode,
            0,
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def run_cli(
        self, *args: str, expect: int = 0
    ) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            ["python3", str(SCRIPT), *args],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(
            result.returncode,
            expect,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        return result

    def write_payload(self, value: dict, name: str = "input.json") -> Path:
        path = self.repo / name
        path.write_text(
            json.dumps(value, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        return path

    def publish(self, value: dict) -> dict:
        input_path = self.write_payload(value)
        result = self.run_cli(
            "publish",
            "--repo-root",
            str(self.repo),
            "--input",
            str(input_path),
        )
        return json.loads(result.stdout)

    def test_publish_resolve_round_trip_and_authority_boundary(self) -> None:
        published = self.publish(payload())
        self.assertRegex(published["code"], r"^HN-[0-9A-F]{12}$")
        self.assertEqual(published["digest_verification"], "pass")
        self.assertEqual(published["transport_status"], "local-only")
        self.assertEqual(published["remote_availability"], "unverified")
        self.assertIn("grants no permission", published["authority"])

        resolved = json.loads(
            self.run_cli(
                "resolve",
                published["code"],
                "--repo-root",
                str(self.repo),
            ).stdout
        )
        self.assertEqual(resolved["digest"], published["digest"])
        self.assertEqual(
            resolved["record"]["payload"]["open_calls"][0]["status"], "open"
        )
        self.assertEqual(
            resolved["record"]["payload"]["next_route"]["authorization"],
            "not-granted",
        )

    def test_missing_boundary_fails_before_locator_allocation(self) -> None:
        invalid = payload()
        invalid["boundaries"] = []
        input_path = self.write_payload(invalid)
        result = self.run_cli(
            "publish",
            "--repo-root",
            str(self.repo),
            "--input",
            str(input_path),
            expect=1,
        )
        self.assertIn("boundaries must be a non-empty array", result.stderr)
        self.assertFalse((self.repo / ".arcanum/handoff-notices/index.json").exists())

    def test_digest_drift_fails_closed(self) -> None:
        published = self.publish(payload())
        record_path = self.repo / published["notice"]
        record = json.loads(record_path.read_text(encoding="utf-8"))
        record["payload"]["subject"] = "Drifted subject"
        record_path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
        result = self.run_cli(
            "resolve",
            published["code"],
            "--repo-root",
            str(self.repo),
            expect=1,
        )
        self.assertIn("digest mismatch", result.stderr)

    def test_index_metadata_drift_fails_closed(self) -> None:
        published = self.publish(payload())
        index_path = self.repo / ".arcanum/handoff-notices/index.json"
        index = json.loads(index_path.read_text(encoding="utf-8"))
        index["entries"][0]["subject"] = "Drifted index subject"
        index_path.write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")
        result = self.run_cli(
            "inspect",
            published["code"],
            "--repo-root",
            str(self.repo),
            expect=1,
        )
        self.assertIn("index metadata mismatch", result.stderr)

    def test_copied_store_is_rejected_in_a_different_repository(self) -> None:
        self.publish(payload())
        other = Path(self.temp.name) / "other"
        other.mkdir()
        self.assertEqual(git(other, "init", "-q").returncode, 0)
        shutil.copytree(self.repo / ".arcanum", other / ".arcanum")
        index = json.loads(
            (self.repo / ".arcanum/handoff-notices/index.json").read_text(
                encoding="utf-8"
            )
        )
        code = index["entries"][0]["code"]
        result = self.run_cli(
            "resolve", code, "--repo-root", str(other), expect=1
        )
        self.assertIn("different repository", result.stderr)

    def test_supersession_is_visible_without_mutating_old_notice(self) -> None:
        first = self.publish(payload())
        next_payload = payload(
            created_at="2026-07-29T12:01:00Z",
            subject="Resolution of the prototype handoff",
        )
        next_payload["notice_type"] = "resolution"
        next_payload["status"] = "resolved"
        next_payload["supersedes"] = first["code"]
        second = self.publish(next_payload)
        old = json.loads(
            self.run_cli(
                "inspect", first["code"], "--repo-root", str(self.repo)
            ).stdout
        )
        self.assertEqual(old["notice_status"], "open")
        self.assertEqual(old["superseded_by"], [second["code"]])

    def test_collision_extends_locator_without_overwrite(self) -> None:
        digest = ("a" * 12) + ("b" * 52)
        index = {
            "entries": [
                {
                    "code": "HN-" + ("A" * 12),
                    "digest": ("a" * 12) + ("c" * 52),
                }
            ]
        }
        code, collision = RUNTIME.select_code(digest, index, 12)
        self.assertEqual(code, "HN-" + ("A" * 12) + ("B" * 4))
        self.assertEqual(collision, "extended")

    def test_malformed_and_unknown_codes_fail_distinctly(self) -> None:
        malformed = self.run_cli(
            "inspect", "HN-NOT-A-CODE", "--repo-root", str(self.repo), expect=1
        )
        self.assertIn("must match", malformed.stderr)
        unknown = self.run_cli(
            "inspect",
            "HN-0123456789AB",
            "--repo-root",
            str(self.repo),
            expect=1,
        )
        self.assertIn("not found in this repository", unknown.stderr)

    def test_git_transport_never_claims_remote_availability(self) -> None:
        published = self.publish(payload())
        self.assertEqual(git(self.repo, "add", ".arcanum").returncode, 0)
        self.assertEqual(
            git(self.repo, "commit", "-qm", "Add handoff notice").returncode, 0
        )
        inspected = json.loads(
            self.run_cli(
                "inspect", published["code"], "--repo-root", str(self.repo)
            ).stdout
        )
        self.assertEqual(inspected["transport_status"], "committed-local")
        self.assertEqual(inspected["remote_availability"], "unverified")


if __name__ == "__main__":
    unittest.main(verbosity=2)
