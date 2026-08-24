#!/usr/bin/env python3
"""Validate and reduce one synthetic App Server fixture without live execution."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Any


PROFILE_SCHEMA = "app-server.fixture-profile.v0"
EVENT_SCHEMA = "app-server.fixture-event.v0"
HOST_RESULT_SCHEMA = "app-server.host-result.v0"
ADAPTER_STATE_SCHEMA = "app-server.fixture-adapter-state.v0"
STATUS_SCHEMA = "arcanum.runtime.status.v1"
PINNED_PROTOCOL_COMMIT = "9946da9af1829410271f6b76f9159961f7281e0a"
EVENT_TYPES = (
    "runtime.created",
    "app_server.initialized",
    "thread.started",
    "turn.started",
    "item.started",
    "item.completed",
    "turn.completed",
)
IDENTITY_KEYS = (
    "process_instance_id",
    "listener_id",
    "connection_id",
    "thread_id",
    "turn_id",
    "item_id",
)
SHA256_RE = re.compile(r"^sha256:[0-9a-f]{64}$")


class FixtureError(ValueError):
    """Fail-closed fixture contract violation."""


def canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
        + "\n"
    ).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return "sha256:" + hashlib.sha256(value).hexdigest()


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise FixtureError(f"invalid JSON input {path}: {exc}") from exc


def load_events(path: Path) -> tuple[list[dict[str, Any]], bytes]:
    try:
        raw = path.read_bytes()
        text = raw.decode("utf-8")
    except (OSError, UnicodeError) as exc:
        raise FixtureError(f"unreadable JSONL input {path}: {exc}") from exc

    events: list[dict[str, Any]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            raise FixtureError(f"blank JSONL record at line {line_number}")
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise FixtureError(f"invalid JSONL record at line {line_number}: {exc}") from exc
        if not isinstance(value, dict):
            raise FixtureError(f"JSONL record {line_number} is not an object")
        events.append(value)
    return events, raw


def require_equal(actual: Any, expected: Any, label: str) -> None:
    if actual != expected:
        raise FixtureError(f"{label} mismatch: expected {expected!r}, got {actual!r}")


def require_sha256(value: Any, label: str) -> str:
    if not isinstance(value, str) or not SHA256_RE.fullmatch(value):
        raise FixtureError(f"{label} must be a lowercase sha256 digest")
    return value


def expected_identity(sequence: int, identity: dict[str, str]) -> dict[str, str | None]:
    visible = 0
    if sequence >= 2:
        visible = 3
    if sequence >= 3:
        visible = 4
    if sequence >= 4:
        visible = 5
    if sequence in (5, 6):
        visible = 6
    return {
        key: identity[key] if index < visible else None
        for index, key in enumerate(IDENTITY_KEYS)
    }


def expected_payloads(profile: dict[str, Any]) -> tuple[dict[str, Any], ...]:
    runtime = profile["runtime"]
    refine = profile["refine"]
    protocol = profile["protocol"]
    output = profile["expected_output"]
    return (
        {
            "orchestrator_id": "refine",
            "refine_run_id": refine["run_id"],
            "runtime_run_id": runtime["run_id"],
            "stage": refine["stage"],
        },
        {
            "protocol_commit": protocol["source_commit"],
            "transport": "stdio",
        },
        {
            "input_digest": profile["input_digest"],
            "purpose": refine["stage"],
        },
        {"turn_limit": 1},
        {"item_type": "agentMessage"},
        {
            "item_type": "agentMessage",
            "output": {"path": output["path"], "sha256": output["sha256"]},
        },
        {"status": "completed"},
    )


def validate_profile(profile: Any, handoff_raw: bytes) -> dict[str, Any]:
    if not isinstance(profile, dict):
        raise FixtureError("profile must be an object")

    require_equal(profile.get("schema_version"), PROFILE_SCHEMA, "profile schema")
    require_equal(profile.get("fixture_id"), "F-01", "fixture id")
    require_equal(profile.get("adapter_id"), "app-server-fixture", "adapter id")
    require_equal(profile.get("profile_mode"), "synthetic-replay-only", "profile mode")
    require_equal(profile.get("live_app_server"), False, "live App Server policy")
    require_equal(profile.get("proof_status"), "fixture-observed", "proof status")
    require_equal(
        profile.get("protocol"),
        {
            "installed_binary_parity": "unverified",
            "source_commit": PINNED_PROTOCOL_COMMIT,
        },
        "protocol pin",
    )
    require_equal(
        profile.get("runtime"),
        {"run_id": "rt-refine-001", "target_kind": "refine-stage"},
        "runtime binding",
    )
    require_equal(
        profile.get("refine"),
        {
            "first_stop": "owner-local-stage-verdict",
            "run_id": "refine-candidate-001",
            "stage": "invoke-design",
        },
        "Refine binding",
    )
    require_equal(
        profile.get("input_digest"), "sha256:" + "1" * 64, "input digest"
    )
    require_equal(
        profile.get("skill"),
        {
            "digest": "sha256:" + "2" * 64,
            "digest_pinned": True,
            "id": "invoke",
        },
        "skill pin",
    )
    require_equal(
        profile.get("policy"),
        {
            "allowed_write_paths": ["/fixture/out/design.md"],
            "filesystem": "read-only-except-allowlist",
            "forbidden_effects": [
                "automatic-next-stage",
                "craft-mutation",
                "goal-control",
                "lifecycle-promotion",
                "orchestrate-dispatch",
                "task-session-admission",
            ],
            "network": "denied",
            "outbound_connector": "denied",
            "realtime": "denied",
            "shell": "denied",
            "transport": "stdio",
            "turn_limit": 1,
            "unsandboxed_process": "denied",
        },
        "fixture policy",
    )
    expected_output = profile.get("expected_output")
    if not isinstance(expected_output, dict):
        raise FixtureError("expected output must be an object")
    require_equal(expected_output.get("path"), "/fixture/out/design.md", "output path")
    require_equal(
        expected_output.get("sha256"), "sha256:" + "3" * 64, "output digest"
    )
    require_equal(profile.get("expected_event_types"), list(EVENT_TYPES), "event types")
    require_equal(
        profile.get("handoff_sha256"), sha256_bytes(handoff_raw), "handoff digest"
    )

    identity = profile.get("identity")
    if not isinstance(identity, dict):
        raise FixtureError("identity must be an object")
    require_equal(tuple(identity.keys()), IDENTITY_KEYS, "identity key order")
    values = list(identity.values())
    if any(not isinstance(value, str) or not value for value in values):
        raise FixtureError("provider-local identities must be non-empty strings")
    if len(set(values)) != len(values):
        raise FixtureError("provider-local identities must be distinct")
    native_ids = {profile["runtime"]["run_id"], profile["refine"]["run_id"]}
    if native_ids.intersection(values):
        raise FixtureError("provider-local identity substitutes an Arcanum identity")
    return profile


def validate_handoff(handoff_raw: bytes) -> None:
    try:
        text = handoff_raw.decode("utf-8")
    except UnicodeError as exc:
        raise FixtureError(f"handoff must be UTF-8: {exc}") from exc
    required = (
        "`adapter_id`: app-server-fixture",
        "`runtime_run_id`: rt-refine-001",
        "`refine_run_id`: refine-candidate-001",
        "`stage`: invoke-design",
        "`network`: denied",
        "`allowed_write_path`: /fixture/out/design.md",
        "owner-local stage verdict",
    )
    missing = [marker for marker in required if marker not in text]
    if missing:
        raise FixtureError(f"handoff is missing contract markers: {missing}")


def validate_events(
    events: list[dict[str, Any]], profile: dict[str, Any]
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    require_equal(len(events), len(EVENT_TYPES), "event count")
    identity = profile["identity"]
    payloads = expected_payloads(profile)
    seen_event_ids: dict[str, str] = {}
    payload_hashes: list[dict[str, str]] = []
    event_hashes: list[dict[str, str]] = []

    for sequence, (event, event_type, payload) in enumerate(
        zip(events, EVENT_TYPES, payloads), start=1
    ):
        require_equal(
            tuple(event.keys()),
            ("schema_version", "sequence", "event_id", "type", "identity", "payload"),
            f"event {sequence} field order",
        )
        require_equal(event["schema_version"], EVENT_SCHEMA, f"event {sequence} schema")
        require_equal(event["sequence"], sequence, f"event {sequence} sequence")
        require_equal(event["type"], event_type, f"event {sequence} type")
        require_equal(
            event["identity"], expected_identity(sequence, identity), f"event {sequence} identity"
        )
        require_equal(event["payload"], payload, f"event {sequence} payload")

        event_id = event["event_id"]
        if not isinstance(event_id, str) or not event_id:
            raise FixtureError(f"event {sequence} has an invalid event id")
        payload_digest = sha256_bytes(canonical_bytes(event["payload"]))
        if event_id in seen_event_ids:
            disposition = (
                "duplicate_replay" if seen_event_ids[event_id] == payload_digest else "replay_mismatch"
            )
            raise FixtureError(f"event {sequence} violates replay policy: {disposition}")
        seen_event_ids[event_id] = payload_digest
        payload_hashes.append({"event_id": event_id, "sha256": payload_digest})
        event_hashes.append(
            {"event_id": event_id, "sha256": sha256_bytes(canonical_bytes(event))}
        )
    return payload_hashes, event_hashes


def build_outputs(
    profile: dict[str, Any],
    handoff_raw: bytes,
    profile_raw: bytes,
    events_raw: bytes,
    events: list[dict[str, Any]],
    payload_hashes: list[dict[str, str]],
    event_hashes: list[dict[str, str]],
) -> dict[str, dict[str, Any]]:
    identity = profile["identity"]
    cursor = {
        "event_count": len(events),
        "last_event_id": events[-1]["event_id"],
        "last_payload_sha256": payload_hashes[-1]["sha256"],
        "last_sequence": events[-1]["sequence"],
    }
    identity_map = {key: identity[key] for key in IDENTITY_KEYS}
    adapter_state = {
        "adapter_id": "app-server-fixture",
        "cursor": cursor,
        "event_hashes": event_hashes,
        "fixture_id": profile["fixture_id"],
        "identity_map": identity_map,
        "input_hashes": {
            "events_sha256": sha256_bytes(events_raw),
            "handoff_sha256": sha256_bytes(handoff_raw),
            "profile_sha256": sha256_bytes(profile_raw),
        },
        "payload_hashes": payload_hashes,
        "proof_status": "fixture-observed",
        "replay_policy": {
            "duplicate_identity_same_payload": "reject-for-exact-f01-trace",
            "duplicate_identity_changed_payload": "reject-replay-mismatch",
        },
        "schema_version": ADAPTER_STATE_SCHEMA,
    }
    host_result = {
        "adapter_id": "app-server-fixture",
        "authority": {
            "capability_owner_verdict": None,
            "craft_state": None,
            "decision_gate": None,
            "goal_control": None,
            "lifecycle_promotion": None,
            "semantic_verdict": None,
            "task_session_admission": None,
        },
        "cursor": cursor,
        "declared_outputs": [profile["expected_output"]],
        "fixture_id": profile["fixture_id"],
        "identity": identity_map,
        "input_digest": profile["input_digest"],
        "next_required_owner": "owner-local-stage-verdict",
        "proof_status": "fixture-observed",
        "provider_status": "completed",
        "receipts": {"executor": None, "owner": None, "terminal": None},
        "runtime_run_id": profile["runtime"]["run_id"],
        "schema_version": HOST_RESULT_SCHEMA,
        "terminal_state": "completed",
        "validation": {"grade": "contract", "status": "passed"},
    }
    status = {
        "adapter_status": "fixture-replay-completed",
        "blocked_reason": None,
        "completed_at": None,
        "error_summary": None,
        "output_paths": ["adapter-state.json", "host-result.json"],
        "run_id": profile["runtime"]["run_id"],
        "schema_version": STATUS_SCHEMA,
        "started_at": None,
        "status": "passed",
        "validation_grade": "contract",
    }
    return {
        "adapter-state.json": adapter_state,
        "host-result.json": host_result,
        "STATUS.json": status,
    }


def prepare_output_dir(path: Path) -> None:
    if path.exists():
        if not path.is_dir():
            raise FixtureError("output path exists and is not a directory")
        try:
            if any(path.iterdir()):
                raise FixtureError("output directory must be empty")
        except OSError as exc:
            raise FixtureError(f"cannot inspect output directory: {exc}") from exc
        return
    try:
        path.mkdir()
    except OSError as exc:
        raise FixtureError(f"cannot create output directory: {exc}") from exc


def write_outputs(path: Path, outputs: dict[str, dict[str, Any]]) -> None:
    created: list[Path] = []
    try:
        for filename, value in outputs.items():
            target = path / filename
            descriptor = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
            created.append(target)
            with os.fdopen(descriptor, "wb") as stream:
                stream.write(canonical_bytes(value))
    except OSError as exc:
        for target in created:
            try:
                target.unlink()
            except OSError:
                pass
        raise FixtureError(f"collision-safe output write failed: {exc}") from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture-dir", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    fixture_dir = args.fixture_dir.resolve()
    output_dir = args.output_dir.resolve()
    if fixture_dir == output_dir or fixture_dir in output_dir.parents:
        raise FixtureError("output directory must be outside the immutable fixture directory")

    handoff_path = fixture_dir / "RUNTIME-HANDOFF.md"
    profile_path = fixture_dir / "profile.json"
    events_path = fixture_dir / "events.jsonl"
    try:
        handoff_raw = handoff_path.read_bytes()
        profile_raw = profile_path.read_bytes()
    except OSError as exc:
        raise FixtureError(f"missing or unreadable fixture input: {exc}") from exc

    validate_handoff(handoff_raw)
    profile = validate_profile(load_json(profile_path), handoff_raw)
    events, events_raw = load_events(events_path)
    payload_hashes, event_hashes = validate_events(events, profile)
    outputs = build_outputs(
        profile,
        handoff_raw,
        profile_raw,
        events_raw,
        events,
        payload_hashes,
        event_hashes,
    )
    prepare_output_dir(output_dir)
    write_outputs(output_dir, outputs)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except FixtureError as exc:
        print(f"app-server fixture validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
