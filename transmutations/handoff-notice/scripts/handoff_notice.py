#!/usr/bin/env python3
"""Publish and resolve repository-local Handoff Notice artifacts.

Stdlib only. This tool persists communication evidence; it does not commit,
push, deliver, dispatch, authorize, or execute downstream work.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any

SCHEMA_VERSION = "0.1.0"
DEFAULT_STORE = ".arcanum/handoff-notices"
CODE_RE = re.compile(r"^HN-([0-9A-F]{12,64})$")
NOTICE_TYPES = {
    "incoming",
    "outgoing",
    "session-handoff",
    "discussion-draft",
    "resolution",
}
NOTICE_STATUSES = {
    "draft",
    "open",
    "flag",
    "blocked",
    "consumed",
    "resolved",
    "superseded",
}
PARTY_KINDS = {
    "person",
    "role",
    "future-session",
    "agent",
    "agent-lane",
    "team",
    "owner-route",
    "any",
}
PAYLOAD_KEYS = {
    "schema_version",
    "notice_type",
    "to",
    "from",
    "subject",
    "project_scope",
    "status",
    "created_at",
    "why_now",
    "key_points",
    "open_calls",
    "boundaries",
    "next_actions",
    "source_refs",
    "next_route",
    "terminal_receipt_ref",
    "supersedes",
    "resolution_ref",
}


class HandoffError(RuntimeError):
    """Fail-closed validation or integrity error."""


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def sha256_hex(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def require_string(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise HandoffError(f"{field} must be a non-empty string")
    if "\x00" in value:
        raise HandoffError(f"{field} contains a null byte")
    return value.strip()


def require_string_list(value: Any, field: str, *, nonempty: bool) -> list[str]:
    if not isinstance(value, list) or (nonempty and not value):
        qualifier = "a non-empty" if nonempty else "an"
        raise HandoffError(f"{field} must be {qualifier} array")
    return [require_string(item, f"{field}[{index}]") for index, item in enumerate(value)]


def validate_party(value: Any, field: str) -> dict[str, str]:
    if not isinstance(value, dict) or set(value) != {"kind", "label"}:
        raise HandoffError(f"{field} must contain exactly kind and label")
    kind = require_string(value["kind"], f"{field}.kind")
    if kind not in PARTY_KINDS:
        raise HandoffError(f"{field}.kind is not supported: {kind}")
    return {"kind": kind, "label": require_string(value["label"], f"{field}.label")}


def validate_relative_scope(value: Any) -> str:
    scope = require_string(value, "project_scope").replace("\\", "/")
    path = PurePosixPath(scope)
    if path.is_absolute() or ".." in path.parts:
        raise HandoffError("project_scope must be a repository-relative scope")
    normalized = path.as_posix().strip("/")
    if not normalized or normalized == ".":
        raise HandoffError("project_scope must name a bounded repository-relative scope")
    return normalized


def validate_timestamp(value: Any) -> str:
    timestamp = require_string(value, "created_at")
    try:
        parsed = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError as exc:
        raise HandoffError("created_at must be an RFC 3339 date-time") from exc
    if parsed.tzinfo is None:
        raise HandoffError("created_at must include a timezone")
    return parsed.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def validate_payload(raw: Any) -> dict[str, Any]:
    if not isinstance(raw, dict):
        raise HandoffError("publish input must be a JSON object")
    unknown = sorted(set(raw) - PAYLOAD_KEYS)
    if unknown:
        raise HandoffError(f"unsupported fields: {', '.join(unknown)}")

    required = {
        "schema_version",
        "notice_type",
        "to",
        "from",
        "subject",
        "project_scope",
        "status",
        "why_now",
        "key_points",
        "open_calls",
        "boundaries",
        "next_actions",
        "source_refs",
    }
    missing = sorted(required - set(raw))
    if missing:
        raise HandoffError(f"missing required fields: {', '.join(missing)}")
    if raw["schema_version"] != SCHEMA_VERSION:
        raise HandoffError(
            f"schema_version must be {SCHEMA_VERSION}, got {raw['schema_version']!r}"
        )

    notice_type = require_string(raw["notice_type"], "notice_type")
    if notice_type not in NOTICE_TYPES:
        raise HandoffError(f"unsupported notice_type: {notice_type}")
    status = require_string(raw["status"], "status")
    if status not in NOTICE_STATUSES:
        raise HandoffError(f"unsupported status: {status}")

    key_points = require_string_list(raw["key_points"], "key_points", nonempty=True)
    boundaries = require_string_list(raw["boundaries"], "boundaries", nonempty=True)

    open_calls_raw = raw["open_calls"]
    if not isinstance(open_calls_raw, list):
        raise HandoffError("open_calls must be an array")
    open_calls: list[dict[str, str]] = []
    for index, item in enumerate(open_calls_raw):
        if not isinstance(item, dict) or set(item) != {"owner", "question", "status"}:
            raise HandoffError(
                f"open_calls[{index}] must contain exactly owner, question, and status"
            )
        call_status = require_string(item["status"], f"open_calls[{index}].status")
        if call_status not in {"open", "blocked", "resolved"}:
            raise HandoffError(f"open_calls[{index}].status is not supported")
        open_calls.append(
            {
                "owner": require_string(item["owner"], f"open_calls[{index}].owner"),
                "question": require_string(
                    item["question"], f"open_calls[{index}].question"
                ),
                "status": call_status,
            }
        )

    next_actions_raw = raw["next_actions"]
    if not isinstance(next_actions_raw, list) or not next_actions_raw:
        raise HandoffError("next_actions must be a non-empty array")
    next_actions: list[dict[str, str]] = []
    for index, item in enumerate(next_actions_raw):
        if not isinstance(item, dict) or set(item) != {"owner", "action"}:
            raise HandoffError(
                f"next_actions[{index}] must contain exactly owner and action"
            )
        next_actions.append(
            {
                "owner": require_string(
                    item["owner"], f"next_actions[{index}].owner"
                ),
                "action": require_string(
                    item["action"], f"next_actions[{index}].action"
                ),
            }
        )

    source_refs_raw = raw["source_refs"]
    if not isinstance(source_refs_raw, list) or not source_refs_raw:
        raise HandoffError("source_refs must be a non-empty array")
    source_refs: list[dict[str, str]] = []
    for index, item in enumerate(source_refs_raw):
        if not isinstance(item, dict) or set(item) != {"ref", "label"}:
            raise HandoffError(
                f"source_refs[{index}] must contain exactly ref and label"
            )
        source_refs.append(
            {
                "ref": require_string(item["ref"], f"source_refs[{index}].ref"),
                "label": require_string(item["label"], f"source_refs[{index}].label"),
            }
        )

    payload: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "notice_type": notice_type,
        "to": validate_party(raw["to"], "to"),
        "from": validate_party(raw["from"], "from"),
        "subject": require_string(raw["subject"], "subject"),
        "project_scope": validate_relative_scope(raw["project_scope"]),
        "status": status,
        "created_at": validate_timestamp(
            raw.get(
                "created_at",
                datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            )
        ),
        "why_now": require_string(raw["why_now"], "why_now"),
        "key_points": key_points,
        "open_calls": open_calls,
        "boundaries": boundaries,
        "next_actions": next_actions,
        "source_refs": source_refs,
    }

    if "next_route" in raw:
        route = raw["next_route"]
        expected = {"capability", "mode", "target", "authorization"}
        if not isinstance(route, dict) or set(route) != expected:
            raise HandoffError(
                "next_route must contain exactly capability, mode, target, and authorization"
            )
        if route["authorization"] != "not-granted":
            raise HandoffError("next_route.authorization must be not-granted")
        payload["next_route"] = {
            "capability": require_string(route["capability"], "next_route.capability"),
            "mode": require_string(route["mode"], "next_route.mode"),
            "target": require_string(route["target"], "next_route.target"),
            "authorization": "not-granted",
        }

    for optional in ("terminal_receipt_ref", "resolution_ref"):
        if optional in raw:
            payload[optional] = require_string(raw[optional], optional)

    if "supersedes" in raw:
        payload["supersedes"] = normalize_code(raw["supersedes"])

    return payload


def normalize_code(value: Any) -> str:
    code = require_string(value, "notice code").upper()
    if not CODE_RE.fullmatch(code):
        raise HandoffError("notice code must match HN- followed by 12 to 64 hex digits")
    return code


def run_git(repo_root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo_root), *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
    )


def repository_fingerprint(repo_root: Path) -> str:
    origin = run_git(repo_root, "config", "--get", "remote.origin.url")
    if origin.returncode == 0 and origin.stdout.strip():
        identity = f"git-origin:{origin.stdout.strip().lower()}"
    else:
        identity = f"filesystem:{repo_root.as_posix()}"
    return hashlib.sha256(identity.encode("utf-8")).hexdigest()


def resolve_store(repo_root: Path, store: str) -> Path:
    requested = Path(store)
    store_root = requested if requested.is_absolute() else repo_root / requested
    resolved = store_root.resolve()
    try:
        resolved.relative_to(repo_root)
    except ValueError as exc:
        raise HandoffError("store must resolve inside the declared repository root") from exc
    return resolved


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def load_json(path: Path, description: str) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise HandoffError(f"{description} not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise HandoffError(f"{description} is invalid JSON: {path}: {exc}") from exc


def load_index(store_root: Path, fingerprint: str) -> dict[str, Any]:
    index_path = store_root / "index.json"
    if not index_path.exists():
        return {
            "schema_version": SCHEMA_VERSION,
            "repository_fingerprint": fingerprint,
            "entries": [],
        }
    index = load_json(index_path, "handoff notice index")
    if (
        not isinstance(index, dict)
        or index.get("schema_version") != SCHEMA_VERSION
        or not isinstance(index.get("entries"), list)
    ):
        raise HandoffError("handoff notice index has an unsupported shape")
    if index.get("repository_fingerprint") != fingerprint:
        raise HandoffError("handoff notice index belongs to a different repository")
    codes = [entry.get("code") for entry in index["entries"] if isinstance(entry, dict)]
    if len(codes) != len(set(codes)):
        raise HandoffError("handoff notice index contains ambiguous locator codes")
    return index


def select_code(digest: str, index: dict[str, Any], minimum: int) -> tuple[str, str]:
    if minimum < 12 or minimum > 64 or minimum % 4:
        raise HandoffError("code length must be a multiple of 4 between 12 and 64")
    entries = {
        entry.get("code"): entry
        for entry in index["entries"]
        if isinstance(entry, dict) and isinstance(entry.get("code"), str)
    }
    for length in range(minimum, 65, 4):
        code = f"HN-{digest[:length].upper()}"
        current = entries.get(code)
        if current is None:
            return code, "pass" if length == minimum else "extended"
        if current.get("digest") == digest:
            return code, "idempotent"
    raise HandoffError("unable to allocate a collision-free handoff locator")


def markdown_notice(record: dict[str, Any]) -> str:
    payload = record["payload"]
    lines = [
        f"# Handoff Notice: {payload['subject']}",
        "",
        f"- Code: `{record['notice_code']}`",
        f"- Status: `{payload['status']}`",
        f"- Type: `{payload['notice_type']}`",
        f"- To: {payload['to']['label']} (`{payload['to']['kind']}`)",
        f"- From: {payload['from']['label']} (`{payload['from']['kind']}`)",
        f"- Project scope: `{payload['project_scope']}`",
        f"- Created: `{payload['created_at']}`",
        f"- Digest: `{record['notice_digest']}`",
        "- Remote availability: `unverified`",
        "",
        "## Why Now",
        "",
        payload["why_now"],
        "",
        "## Key Points",
        "",
    ]
    lines.extend(f"- {item}" for item in payload["key_points"])
    lines.extend(["", "## Open Calls", ""])
    if payload["open_calls"]:
        lines.extend(
            f"- [{item['status']}] {item['owner']}: {item['question']}"
            for item in payload["open_calls"]
        )
    else:
        lines.append("- None.")
    lines.extend(["", "## Boundaries", ""])
    lines.extend(f"- {item}" for item in payload["boundaries"])
    lines.extend(["", "## Next Actions", ""])
    lines.extend(
        f"- {item['owner']}: {item['action']}" for item in payload["next_actions"]
    )
    lines.extend(["", "## Source References", ""])
    lines.extend(
        f"- `{item['ref']}` — {item['label']}" for item in payload["source_refs"]
    )
    if "next_route" in payload:
        route = payload["next_route"]
        lines.extend(
            [
                "",
                "## Suggested Next Route",
                "",
                f"- Capability: `{route['capability']}`",
                f"- Mode: `{route['mode']}`",
                f"- Target: `{route['target']}`",
                f"- Authorization: `{route['authorization']}`",
            ]
        )
    if "terminal_receipt_ref" in payload:
        lines.extend(
            [
                "",
                "## Terminal Receipt",
                "",
                f"- `{payload['terminal_receipt_ref']}`",
            ]
        )
    if "supersedes" in payload:
        lines.extend(["", "## Supersedes", "", f"- `{payload['supersedes']}`"])
    if "resolution_ref" in payload:
        lines.extend(["", "## Resolution Reference", "", f"- `{payload['resolution_ref']}`"])
    lines.extend(
        [
            "",
            "## Authority Boundary",
            "",
            "This notice is communication evidence only. The notice and locator grant no permission, authenticate no actor, resolve no open call, select no task, and authorize no mutation, dispatch, Git publication, or external delivery.",
            "",
        ]
    )
    return "\n".join(lines)


def relative_to_repo(path: Path, repo_root: Path) -> str:
    return path.relative_to(repo_root).as_posix()


def git_transport_status(repo_root: Path, paths: list[Path]) -> str:
    rels = [relative_to_repo(path, repo_root) for path in paths]
    tracked = run_git(repo_root, "ls-files", "--error-unmatch", "--", *rels)
    if tracked.returncode != 0:
        return "local-only"
    dirty = run_git(repo_root, "status", "--porcelain", "--", *rels)
    if dirty.returncode != 0:
        return "unavailable"
    return "git-tracked-uncommitted" if dirty.stdout.strip() else "committed-local"


def record_paths(store_root: Path, code: str) -> tuple[Path, Path]:
    notice_root = store_root / "notices"
    return notice_root / f"{code}.json", notice_root / f"{code}.md"


def entry_for(index: dict[str, Any], code: str) -> dict[str, Any] | None:
    matches = [
        entry
        for entry in index["entries"]
        if isinstance(entry, dict) and entry.get("code") == code
    ]
    if len(matches) > 1:
        raise HandoffError(f"ambiguous handoff locator: {code}")
    return matches[0] if matches else None


def expected_index_entry(
    record: dict[str, Any],
    json_path: Path,
    markdown_path: Path,
    repo_root: Path,
) -> dict[str, Any]:
    payload = record["payload"]
    return {
        "code": record["notice_code"],
        "digest": record["notice_digest"],
        "notice_id": record["notice_id"],
        "json_path": relative_to_repo(json_path, repo_root),
        "markdown_path": relative_to_repo(markdown_path, repo_root),
        "created_at": payload["created_at"],
        "notice_type": payload["notice_type"],
        "status": payload["status"],
        "project_scope": payload["project_scope"],
        "subject": payload["subject"],
        "supersedes": payload.get("supersedes"),
    }


def verify_indexed_json_record(
    repo_root: Path,
    store_root: Path,
    fingerprint: str,
    entry: dict[str, Any],
) -> tuple[dict[str, Any], Path, Path]:
    code = normalize_code(entry.get("code"))
    json_path, markdown_path = record_paths(store_root, code)
    expected_json = relative_to_repo(json_path, repo_root)
    expected_markdown = relative_to_repo(markdown_path, repo_root)
    if (
        entry.get("json_path") != expected_json
        or entry.get("markdown_path") != expected_markdown
    ):
        raise HandoffError(f"handoff locator path mismatch: {code}")
    record = load_json(json_path, "handoff notice record")
    if not isinstance(record, dict) or not isinstance(record.get("payload"), dict):
        raise HandoffError(f"handoff notice record has an unsupported shape: {code}")
    digest = sha256_hex(
        {
            "repository_fingerprint": fingerprint,
            "payload": record["payload"],
        }
    )
    if record.get("repository_fingerprint") != fingerprint:
        raise HandoffError(f"handoff notice belongs to a different repository: {code}")
    if record.get("notice_digest") != digest or entry.get("digest") != digest:
        raise HandoffError(f"handoff notice digest mismatch: {code}")
    if record.get("notice_code") != code or not digest.upper().startswith(code[3:]):
        raise HandoffError(f"handoff locator does not match notice content: {code}")
    if expected_index_entry(record, json_path, markdown_path, repo_root) != entry:
        raise HandoffError(f"handoff notice index metadata mismatch: {code}")
    return record, json_path, markdown_path


def verify_record(
    repo_root: Path, store_root: Path, fingerprint: str, code: str
) -> tuple[dict[str, Any], dict[str, Any], list[str], Path, Path]:
    index = load_index(store_root, fingerprint)
    entry = entry_for(index, code)
    if entry is None:
        raise HandoffError(f"handoff locator not found in this repository: {code}")
    record, json_path, markdown_path = verify_indexed_json_record(
        repo_root, store_root, fingerprint, entry
    )
    if not markdown_path.is_file():
        raise HandoffError(f"handoff notice Markdown representation is missing: {code}")
    expected_markdown_body = markdown_notice(record)
    if markdown_path.read_text(encoding="utf-8") != expected_markdown_body:
        raise HandoffError(f"handoff notice Markdown representation has drifted: {code}")
    superseded_by = []
    for item in index["entries"]:
        if not isinstance(item, dict) or item.get("supersedes") != code:
            continue
        candidate, _, _ = verify_indexed_json_record(
            repo_root, store_root, fingerprint, item
        )
        if candidate["payload"].get("supersedes") != code:
            raise HandoffError(
                f"handoff supersession metadata mismatch: {item.get('code')}"
            )
        superseded_by.append(item["code"])
    superseded_by.sort()
    return record, entry, superseded_by, json_path, markdown_path


def publish(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    if not repo_root.is_dir():
        raise HandoffError(f"repository root not found: {repo_root}")
    store_root = resolve_store(repo_root, args.store)
    fingerprint = repository_fingerprint(repo_root)
    raw = load_json(Path(args.input).resolve(), "handoff notice input")
    payload = validate_payload(raw)
    index = load_index(store_root, fingerprint)
    if "supersedes" in payload and entry_for(index, payload["supersedes"]) is None:
        raise HandoffError(
            f"superseded locator is not present in this repository: {payload['supersedes']}"
        )

    digest = sha256_hex(
        {"repository_fingerprint": fingerprint, "payload": payload}
    )
    code, collision = select_code(digest, index, args.code_length)
    json_path, markdown_path = record_paths(store_root, code)
    record = {
        "schema_version": SCHEMA_VERSION,
        "notice_id": f"hn:{digest}",
        "notice_code": code,
        "notice_digest": digest,
        "repository_fingerprint": fingerprint,
        "transport_claim": "local-artifact-only",
        "authority": {
            "kind": "communication-evidence",
            "grants": [],
            "statement": "The notice and locator grant no permission or authority.",
        },
        "payload": payload,
    }
    json_body = json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    markdown_body = markdown_notice(record)

    if json_path.exists() and json_path.read_text(encoding="utf-8") != json_body:
        raise HandoffError(f"refusing to overwrite a different notice at {json_path}")
    if markdown_path.exists() and markdown_path.read_text(encoding="utf-8") != markdown_body:
        raise HandoffError(f"refusing to overwrite a drifted notice at {markdown_path}")
    atomic_write(json_path, json_body)
    atomic_write(markdown_path, markdown_body)

    entry = expected_index_entry(record, json_path, markdown_path, repo_root)
    current = entry_for(index, code)
    registry_update = "idempotent" if current == entry else "created"
    if current is not None and current != entry:
        raise HandoffError(f"locator collision with a different index entry: {code}")
    if current is None:
        index["entries"].append(entry)
        index["entries"].sort(key=lambda item: item["code"])
    index_path = store_root / "index.json"
    atomic_write(
        index_path,
        json.dumps(index, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
    )

    paths = [json_path, markdown_path, index_path]
    return {
        "mode": "publish",
        "status": "pass",
        "code": code,
        "repository_fingerprint": fingerprint,
        "notice": relative_to_repo(json_path, repo_root),
        "message": relative_to_repo(markdown_path, repo_root),
        "index": relative_to_repo(index_path, repo_root),
        "digest": digest,
        "digest_verification": "pass",
        "notice_status": payload["status"],
        "superseded_by": [],
        "transport_status": git_transport_status(repo_root, paths),
        "remote_availability": "unverified",
        "authority": "communication evidence only; grants no permission",
        "open_calls": len(payload["open_calls"]),
        "next_owner": payload.get("next_route", {}).get("capability", "none"),
        "collision_check": collision,
        "registry_update": registry_update,
        "validation": [
            "schema",
            "repository-scope",
            "locator-collision",
            "artifact-index",
            "authority-boundary",
        ],
        "follow_up": "share through a separately authorized transport",
    }


def resolve_or_inspect(args: argparse.Namespace, mode: str) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    if not repo_root.is_dir():
        raise HandoffError(f"repository root not found: {repo_root}")
    store_root = resolve_store(repo_root, args.store)
    fingerprint = repository_fingerprint(repo_root)
    code = normalize_code(args.code)
    record, _, superseded_by, json_path, markdown_path = verify_record(
        repo_root, store_root, fingerprint, code
    )
    index_path = store_root / "index.json"
    payload = record["payload"]
    receipt: dict[str, Any] = {
        "mode": mode,
        "status": "pass",
        "code": code,
        "repository_fingerprint": fingerprint,
        "notice": relative_to_repo(json_path, repo_root),
        "message": relative_to_repo(markdown_path, repo_root),
        "index": relative_to_repo(index_path, repo_root),
        "digest": record["notice_digest"],
        "digest_verification": "pass",
        "notice_status": payload["status"],
        "superseded_by": superseded_by,
        "transport_status": git_transport_status(
            repo_root, [json_path, markdown_path, index_path]
        ),
        "remote_availability": "unverified",
        "authority": "communication evidence only; grants no permission",
        "open_calls": len(payload["open_calls"]),
        "next_owner": payload.get("next_route", {}).get("capability", "none"),
        "validation": [
            "repository-scope",
            "locator",
            "digest",
            "artifact-index",
            "markdown-parity",
            "authority-boundary",
        ],
        "follow_up": "route downstream work separately or none",
    }
    if mode == "resolve":
        receipt["record"] = record
    return receipt


def render_receipt(receipt: dict[str, Any], output_format: str) -> str:
    if output_format == "json":
        return json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True)
    superseded = ", ".join(receipt["superseded_by"]) or "none"
    validation = ", ".join(receipt["validation"])
    return "\n".join(
        [
            "## Handoff Notice Result",
            "",
            f"- Mode: {receipt['mode']}",
            f"- Status: {receipt['status']}",
            f"- Code: {receipt['code']}",
            f"- Repository scope: {receipt['repository_fingerprint']}",
            f"- Notice: {receipt['notice']}",
            f"- Message: {receipt['message']}",
            f"- Digest verification: {receipt['digest_verification']}",
            f"- Notice status: {receipt['notice_status']}",
            f"- Superseded by: {superseded}",
            f"- Transport status: {receipt['transport_status']}",
            f"- Remote availability: {receipt['remote_availability']}",
            f"- Authority: {receipt['authority']}",
            f"- Open calls: {receipt['open_calls']}",
            f"- Next owner: {receipt['next_owner']}",
            f"- Validation: {validation}",
            f"- Follow-up: {receipt['follow_up']}",
        ]
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Publish or resolve repository-local Handoff Notices."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    publish_parser = subparsers.add_parser("publish")
    publish_parser.add_argument("--repo-root", required=True)
    publish_parser.add_argument("--input", required=True)
    publish_parser.add_argument("--store", default=DEFAULT_STORE)
    publish_parser.add_argument(
        "--code-length",
        type=int,
        default=12,
        help="minimum hex locator length; 12 by default, extended on collision",
    )
    publish_parser.add_argument("--format", choices=("json", "markdown"), default="json")

    for command in ("resolve", "inspect"):
        command_parser = subparsers.add_parser(command)
        command_parser.add_argument("code")
        command_parser.add_argument("--repo-root", required=True)
        command_parser.add_argument("--store", default=DEFAULT_STORE)
        command_parser.add_argument(
            "--format", choices=("json", "markdown"), default="json"
        )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        if args.command == "publish":
            receipt = publish(args)
        else:
            receipt = resolve_or_inspect(args, args.command)
        print(render_receipt(receipt, args.format))
        return 0
    except HandoffError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
