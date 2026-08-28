#!/usr/bin/env python3
"""Hostile fixtures for confirmed role-briefing fidelity."""

from __future__ import annotations

import copy
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable


ARCANUM = Path(__file__).resolve().parents[3]
VALIDATOR = ARCANUM / "formulae/dispatch-spec/scripts/validate-dispatch.py"
FIXTURE_DIR = ARCANUM / "runtime/orchestrate/tests/fixtures/compile"
BASE_DISPATCH = FIXTURE_DIR / "valid-two-wave.json"
BASE_SOURCE = FIXTURE_DIR / "confirmed-briefings.json"


def canonical_sha(value: Any) -> str:
    payload = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def portable_text_sha(raw: bytes) -> str:
    return hashlib.sha256(
        raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    ).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def refresh_exact_binding(dispatch: dict[str, Any], source: dict[str, Any], root: Path) -> None:
    source_path = root / "confirmed-briefings.json"
    write_json(source_path, source)
    artifact_sha = portable_text_sha(source_path.read_bytes())
    for role in dispatch["subagent_strategy"]["roles"]:
        for agent in role["agents"]:
            binding = agent["briefing_binding"]
            selector = binding["source_binding"]["selector"].removeprefix("/roles/")
            briefing = source["roles"][selector]
            digest = canonical_sha(briefing)
            binding["briefing"] = copy.deepcopy(briefing)
            binding["briefing_sha256"] = digest
            binding["source_binding"]["artifact_sha256"] = artifact_sha
            binding["source_binding"]["selected_payload_sha256"] = digest


def run_case(
    name: str,
    expected: str,
    mutate: Callable[[dict[str, Any], dict[str, Any], Path], None],
) -> bool:
    dispatch = json.loads(BASE_DISPATCH.read_text(encoding="utf-8"))
    source = json.loads(BASE_SOURCE.read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        shutil.copyfile(BASE_SOURCE, root / "confirmed-briefings.json")
        mutate(dispatch, source, root)
        dispatch_path = root / "dispatch.json"
        write_json(dispatch_path, dispatch)
        completed = subprocess.run(
            [sys.executable, str(VALIDATOR), str(dispatch_path), "--json"],
            check=False,
            capture_output=True,
            text=True,
        )
        result = json.loads(completed.stdout)
        actual = result["validation"]
        passed = actual == expected
        print(f"BRIEFING_FIXTURE={'pass' if passed else 'block'} CASE={name} EXPECTED={expected} ACTUAL={actual}")
        if not passed:
            print(json.dumps(result, indent=2))
        return passed


def role(dispatch: dict[str, Any], role_id: str) -> dict[str, Any]:
    return next(item for item in dispatch["subagent_strategy"]["roles"] if item["role_id"] == role_id)


def agent(dispatch: dict[str, Any], role_id: str, ordinal: int = 0) -> dict[str, Any]:
    return role(dispatch, role_id)["agents"][ordinal]


def no_change(dispatch: dict[str, Any], source: dict[str, Any], root: Path) -> None:
    del dispatch, source, root


def allowed_read_forbidden_write_overlap(dispatch: dict[str, Any], source: dict[str, Any], root: Path) -> None:
    target = role(dispatch, "beta-check")
    target["forbidden_write_scopes"].append("restricted-input/")
    for selector in ("beta-check-0", "beta-check-1"):
        briefing = source["roles"][selector]
        briefing["read_policy"]["allowed_read_scopes"].append("restricted-input/")
        briefing["write_policy"]["forbidden_write_scopes"].append("restricted-input/")
    refresh_exact_binding(dispatch, source, root)


def main() -> int:
    cases: list[tuple[str, str, Callable[[dict[str, Any], dict[str, Any], Path], None]]] = [
        ("exact binding", "pass", no_change),
        ("missing briefing", "block", lambda d, s, r: agent(d, "beta-check").pop("briefing_binding")),
        ("wrong artifact digest", "block", lambda d, s, r: agent(d, "beta-check")["briefing_binding"]["source_binding"].__setitem__("artifact_sha256", "0" * 64)),
        ("wrong selector", "block", lambda d, s, r: agent(d, "beta-check")["briefing_binding"]["source_binding"].__setitem__("selector", "/roles/alpha-check-0")),
        ("wrong selected payload digest", "block", lambda d, s, r: agent(d, "beta-check")["briefing_binding"]["source_binding"].__setitem__("selected_payload_sha256", "0" * 64)),
        ("changed instructions", "block", lambda d, s, r: agent(d, "beta-check")["briefing_binding"]["briefing"].__setitem__("instructions", "changed")),
        ("changed status semantics", "block", lambda d, s, r: agent(d, "beta-check")["briefing_binding"]["briefing"]["status_semantics"].__setitem__("task_complete_value", "done")),
        ("changed receipt shape", "block", lambda d, s, r: agent(d, "beta-check")["briefing_binding"]["briefing"]["receipt_shape"]["required_fields"].pop()),
        ("read write boundary mismatch", "block", lambda d, s, r: agent(d, "beta-check")["briefing_binding"]["briefing"]["write_policy"].__setitem__("forbidden_write_scopes", [])),
        ("allowed read and forbidden write overlap", "pass", allowed_read_forbidden_write_overlap),
    ]
    passed = all(run_case(*case) for case in cases)
    print(f"CONFIRMED_ROLE_BRIEFING_FIXTURES={'pass' if passed else 'block'}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
