#!/usr/bin/env python3
"""Resolve the nearest evidence-backed Task Session scope.

The resolver ranks selectors. It does not decide that an SWU is ready: Task
Session must re-read the selected live work pack and run its normal gates.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


CURSOR_SCHEMA_VERSION = "task-session.continuity.v1"
SESSION_ID_PATTERN = re.compile(r"^[A-Za-z0-9._-]+$")
RUNTIME_SESSION_ENV = (
    "ARCANUM_TASK_SESSION_ID",
    "CODEX_THREAD_ID",
    "CLAUDE_SESSION_ID",
)


@dataclass(frozen=True)
class Candidate:
    priority: int
    source: str
    evidence: str
    scope_root: str
    work_pack: str
    swu: str | None
    session_id: str | None
    requires_live_revalidation: bool = True


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError("top-level JSON value must be an object")
    return value


def is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def resolve_repo_path(repo_root: Path, raw_path: str) -> Path:
    candidate = Path(raw_path)
    if not candidate.is_absolute():
        candidate = repo_root / candidate
    resolved = candidate.resolve()
    if not is_within(resolved, repo_root):
        raise ValueError(f"path escapes repository root: {raw_path}")
    return resolved


def relative(repo_root: Path, path: Path) -> str:
    value = path.relative_to(repo_root).as_posix()
    return value or "."


def load_policy(script_path: Path) -> tuple[dict[str, int], int]:
    policy_path = script_path.parent.parent / "decision-validation-policy.json"
    policy = load_json(policy_path)["zero_argument_resolution"]
    priorities = {
        source: index
        for index, source in enumerate(policy["source_priority"])
    }
    return priorities, int(policy["execution_limit"])


def cursor_candidate(
    *,
    repo_root: Path,
    cwd: Path,
    cursor: dict[str, Any],
    evidence_path: Path,
    source: str,
    priority: int,
    require_scope_match: bool,
    expected_session_id: str | None = None,
) -> tuple[Candidate | None, dict[str, str] | None]:
    evidence = relative(repo_root, evidence_path)
    if cursor.get("schema_version") != CURSOR_SCHEMA_VERSION:
        return None, {"evidence": evidence, "reason": "unsupported-cursor-schema"}

    session_id = cursor.get("session_id")
    if not isinstance(session_id, str) or not session_id:
        return None, {"evidence": evidence, "reason": "missing-session-id"}
    if expected_session_id is not None and session_id != expected_session_id:
        return None, {"evidence": evidence, "reason": "session-id-mismatch"}

    try:
        scope_root = resolve_repo_path(repo_root, str(cursor["scope_root"]))
        work_pack = resolve_repo_path(repo_root, str(cursor["work_pack"]))
    except (KeyError, ValueError) as error:
        return None, {"evidence": evidence, "reason": str(error)}

    if require_scope_match and not is_within(cwd, scope_root):
        return None, {"evidence": evidence, "reason": "cursor-outside-cwd-scope"}
    if not work_pack.is_file():
        return None, {"evidence": evidence, "reason": "work-pack-missing"}
    if work_pack.name != "WORK-PACK.md":
        return None, {"evidence": evidence, "reason": "target-is-not-work-pack"}

    next_route = cursor.get("next_route")
    next_swu = cursor.get("next_swu")
    if isinstance(next_route, dict):
        capability = next_route.get("capability")
        if capability != "task-session":
            return None, {
                "evidence": evidence,
                "reason": f"next-route-owned-by-{capability or 'unknown'}",
            }
        route_work_pack = next_route.get("work_pack")
        if isinstance(route_work_pack, str) and route_work_pack:
            try:
                route_path = resolve_repo_path(repo_root, route_work_pack)
            except ValueError as error:
                return None, {"evidence": evidence, "reason": str(error)}
            if route_path != work_pack:
                return None, {
                    "evidence": evidence,
                    "reason": "cursor-route-work-pack-mismatch",
                }
        if not isinstance(next_swu, str) or not next_swu:
            route_swu = next_route.get("swu")
            next_swu = route_swu if isinstance(route_swu, str) and route_swu else None
    elif next_route is not None:
        return None, {"evidence": evidence, "reason": "invalid-next-route"}

    return (
        Candidate(
            priority=priority,
            source=source,
            evidence=evidence,
            scope_root=relative(repo_root, scope_root),
            work_pack=relative(repo_root, work_pack),
            swu=next_swu if isinstance(next_swu, str) and next_swu else None,
            session_id=session_id,
        ),
        None,
    )


def work_pack_candidate(
    *,
    repo_root: Path,
    work_pack: Path,
    source: str,
    priority: int,
    evidence: Path,
) -> tuple[Candidate | None, dict[str, str] | None]:
    evidence_name = relative(repo_root, evidence)
    if not work_pack.is_file():
        return None, {"evidence": evidence_name, "reason": "work-pack-missing"}
    if work_pack.name != "WORK-PACK.md":
        return None, {
            "evidence": evidence_name,
            "reason": "target-is-not-work-pack",
        }
    return (
        Candidate(
            priority=priority,
            source=source,
            evidence=evidence_name,
            scope_root=relative(repo_root, work_pack.parent),
            work_pack=relative(repo_root, work_pack),
            swu=None,
            session_id=None,
        ),
        None,
    )


def add_candidate(
    candidates: list[Candidate],
    rejected: list[dict[str, str]],
    result: tuple[Candidate | None, dict[str, str] | None],
) -> None:
    candidate, rejection = result
    if candidate is not None:
        candidates.append(candidate)
    if rejection is not None:
        rejected.append(rejection)


def nearest_ancestor_work_pack(cwd: Path, repo_root: Path) -> Path | None:
    current = cwd if cwd.is_dir() else cwd.parent
    while is_within(current, repo_root):
        candidate = current / "WORK-PACK.md"
        if candidate.is_file():
            return candidate.resolve()
        if current == repo_root:
            break
        current = current.parent
    return None


def runtime_session_id() -> tuple[str | None, str | None]:
    for variable in RUNTIME_SESSION_ENV:
        value = os.environ.get(variable)
        if value:
            return value, variable
    return None, None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--cwd", default=".")
    parser.add_argument("--session", dest="session_id")
    parser.add_argument("--visible-context", type=Path)
    parser.add_argument("--from", dest="from_path", type=Path)
    parser.add_argument("--list-nearest", action="store_true")
    args = parser.parse_args()
    detected_session_id, detected_session_source = runtime_session_id()
    current_session_id = args.session_id or detected_session_id
    session_id_source = (
        "explicit-flag"
        if args.session_id is not None
        else detected_session_source or "unavailable"
    )

    repo_root = Path(args.repo_root).resolve()
    cwd = Path(args.cwd).resolve()
    if not repo_root.is_dir() or not is_within(cwd, repo_root):
        print(
            json.dumps(
                {
                    "schema_version": "task-session.nearest-resolution.v1",
                    "status": "BLOCK",
                    "reason": "cwd-outside-repository-root",
                    "selected": None,
                    "candidates": [],
                    "rejected": [],
                },
                indent=2,
            )
        )
        return 2

    try:
        priorities, execution_limit = load_policy(Path(__file__).resolve())
    except (OSError, KeyError, ValueError, json.JSONDecodeError) as error:
        print(json.dumps({"status": "BLOCK", "reason": f"policy-error: {error}"}))
        return 2

    candidates: list[Candidate] = []
    rejected: list[dict[str, str]] = []

    if args.from_path is not None:
        try:
            source_path = resolve_repo_path(repo_root, str(args.from_path))
            if source_path.is_dir():
                source_path = source_path / "WORK-PACK.md"
            if source_path.suffix == ".json":
                cursor = load_json(source_path)
                add_candidate(
                    candidates,
                    rejected,
                    cursor_candidate(
                        repo_root=repo_root,
                        cwd=cwd,
                        cursor=cursor,
                        evidence_path=source_path,
                        source="explicit-source",
                        priority=priorities["explicit-source"],
                        require_scope_match=False,
                    ),
                )
            else:
                add_candidate(
                    candidates,
                    rejected,
                    work_pack_candidate(
                        repo_root=repo_root,
                        work_pack=source_path,
                        source="explicit-source",
                        priority=priorities["explicit-source"],
                        evidence=source_path,
                    ),
                )
        except (OSError, ValueError, json.JSONDecodeError) as error:
            rejected.append(
                {"evidence": str(args.from_path), "reason": f"invalid-source: {error}"}
            )
    else:
        if args.visible_context is not None:
            try:
                visible_path = resolve_repo_path(repo_root, str(args.visible_context))
                visible = load_json(visible_path)
                add_candidate(
                    candidates,
                    rejected,
                    cursor_candidate(
                        repo_root=repo_root,
                        cwd=cwd,
                        cursor=visible,
                        evidence_path=visible_path,
                        source="visible-session-context",
                        priority=priorities["visible-session-context"],
                        require_scope_match=False,
                    ),
                )
            except (OSError, ValueError, json.JSONDecodeError) as error:
                rejected.append(
                    {
                        "evidence": str(args.visible_context),
                        "reason": f"invalid-visible-context: {error}",
                    }
                )

        cursor_root = repo_root / ".arcanum/task-session/continuity"
        exact_cursor: Path | None = None
        if current_session_id is not None:
            if not SESSION_ID_PATTERN.fullmatch(current_session_id):
                rejected.append(
                    {
                        "evidence": current_session_id,
                        "reason": "invalid-session-id",
                    }
                )
            else:
                exact_cursor = cursor_root / f"{current_session_id}.json"
                if exact_cursor.is_file():
                    try:
                        exact = load_json(exact_cursor)
                        add_candidate(
                            candidates,
                            rejected,
                            cursor_candidate(
                                repo_root=repo_root,
                                cwd=cwd,
                                cursor=exact,
                                evidence_path=exact_cursor,
                                source="exact-session-cursor",
                                priority=priorities["exact-session-cursor"],
                                require_scope_match=False,
                                expected_session_id=current_session_id,
                            ),
                        )
                    except (OSError, ValueError, json.JSONDecodeError) as error:
                        rejected.append(
                            {
                                "evidence": relative(repo_root, exact_cursor),
                                "reason": f"invalid-cursor: {error}",
                            }
                        )
                else:
                    rejected.append(
                        {
                            "evidence": relative(repo_root, exact_cursor),
                            "reason": "exact-session-cursor-missing",
                        }
                    )

        ancestor = nearest_ancestor_work_pack(cwd, repo_root)
        if ancestor is not None:
            add_candidate(
                candidates,
                rejected,
                work_pack_candidate(
                    repo_root=repo_root,
                    work_pack=ancestor,
                    source="cwd-ancestor-work-pack",
                    priority=priorities["cwd-ancestor-work-pack"],
                    evidence=ancestor,
                ),
            )

        if cursor_root.is_dir():
            for cursor_path in sorted(cursor_root.glob("*.json")):
                if exact_cursor is not None and cursor_path == exact_cursor:
                    continue
                try:
                    cursor = load_json(cursor_path)
                    add_candidate(
                        candidates,
                        rejected,
                        cursor_candidate(
                            repo_root=repo_root,
                            cwd=cwd,
                            cursor=cursor,
                            evidence_path=cursor_path,
                            source="scope-matched-continuity",
                            priority=priorities["scope-matched-continuity"],
                            require_scope_match=True,
                        ),
                    )
                except (OSError, ValueError, json.JSONDecodeError) as error:
                    rejected.append(
                        {
                            "evidence": relative(repo_root, cursor_path),
                            "reason": f"invalid-cursor: {error}",
                        }
                    )

    unique: dict[tuple[str, str | None], Candidate] = {}
    for candidate in sorted(
        candidates,
        key=lambda item: (
            item.priority,
            item.work_pack,
            item.swu or "",
            item.evidence,
        ),
    ):
        unique.setdefault((candidate.work_pack, candidate.swu), candidate)
    ranked = list(unique.values())
    top_priority = ranked[0].priority if ranked else None
    nearest = (
        [candidate for candidate in ranked if candidate.priority == top_priority]
        if top_priority is not None
        else []
    )

    selected: Candidate | None = nearest[0] if len(nearest) == 1 else None
    if not ranked:
        status = "BLOCK"
        reason = "no-nearest-candidate"
    elif len(nearest) > 1:
        status = "BLOCK"
        reason = "ambiguous-nearest-candidates"
    elif args.list_nearest:
        status = "PREVIEW"
        reason = "nearest-candidate-preview"
    else:
        status = "RESOLVED"
        reason = "nearest-candidate-selected"

    output = {
        "schema_version": "task-session.nearest-resolution.v1",
        "mode": "list-nearest" if args.list_nearest else "resume-nearest",
        "status": status,
        "reason": reason,
        "execution_limit": execution_limit,
        "session_id_source": session_id_source,
        "requires_live_revalidation": True,
        "selected": asdict(selected) if selected is not None else None,
        "candidates": [asdict(candidate) for candidate in ranked],
        "rejected": rejected,
    }
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0 if status in {"RESOLVED", "PREVIEW"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
