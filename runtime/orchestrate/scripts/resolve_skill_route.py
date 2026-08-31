#!/usr/bin/env python3
"""Resolve one skill route without allowing global aliases to shadow a repository."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


RUNTIME_ROOTS = {"codex": ".agents/skills", "claude": ".claude/skills"}
REPOSITORY_ALIASES = {"arcanum-orchestrate": "orchestrate"}


def normalized_capability(name: str) -> str:
    return REPOSITORY_ALIASES.get(name, name)


def safe_local_path(repository_root: Path, runtime: str, capability: str) -> Path:
    if not capability or capability in {".", ".."} or "/" in capability or "\\" in capability:
        raise ValueError("capability must be one normalized package name")
    return repository_root / RUNTIME_ROOTS[runtime] / capability / "SKILL.md"


def resolve(
    repository_root: Path,
    runtime: str,
    capability: str,
    *,
    explicit_repository_route: Path | None = None,
    user_named_skill: str | None = None,
    allow_global_fallback: bool = False,
    global_candidate: Path | None = None,
) -> dict[str, object]:
    repository_root = repository_root.resolve()
    requested = user_named_skill or capability
    normalized = normalized_capability(requested)

    if explicit_repository_route is not None:
        candidate = (repository_root / explicit_repository_route).resolve()
        try:
            candidate.relative_to(repository_root)
        except ValueError as error:
            raise ValueError("explicit repository route escapes repository root") from error
        if candidate.is_file():
            return _result(requested, normalized, candidate, "explicit-repository-route")
        raise ValueError("explicit repository route is missing")

    local = safe_local_path(repository_root, runtime, normalized)
    if local.is_file():
        source = "explicit-user-skill" if user_named_skill else "repository-capability-match"
        return _result(requested, normalized, local, source)

    if allow_global_fallback and global_candidate is not None and global_candidate.is_file():
        return _result(requested, normalized, global_candidate.resolve(), "permitted-global-fallback")

    reason = "repository package is absent and global fallback is not permitted"
    if allow_global_fallback and global_candidate is None:
        reason = "repository package is absent and no global candidate was supplied"
    raise ValueError(reason)


def _result(requested: str, normalized: str, path: Path, source: str) -> dict[str, object]:
    return {
        "status": "pass",
        "requested_skill": requested,
        "normalized_capability": normalized,
        "source": source,
        "path": str(path),
        "catalog_consulted": source == "permitted-global-fallback",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", required=True, type=Path)
    parser.add_argument("--runtime", required=True, choices=sorted(RUNTIME_ROOTS))
    parser.add_argument("--capability", required=True)
    parser.add_argument("--explicit-repository-route", type=Path)
    parser.add_argument("--user-named-skill")
    parser.add_argument("--allow-global-fallback", action="store_true")
    parser.add_argument("--global-candidate", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        result = resolve(
            args.repository_root,
            args.runtime,
            args.capability,
            explicit_repository_route=args.explicit_repository_route,
            user_named_skill=args.user_named_skill,
            allow_global_fallback=args.allow_global_fallback,
            global_candidate=args.global_candidate,
        )
    except ValueError as error:
        print(json.dumps({"status": "block", "reason": str(error)}, sort_keys=True))
        return 2
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
