#!/usr/bin/env python3
"""Compile and join the canonical accepted-stream driver without granting authority."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any
import argparse

from accepted_stream_contract import (
    ContractError,
    WRITE_PARTITIONS,
    canonical_bytes,
    child_id,
    stream_id,
    validate_authority,
)


DRIVER_PATH = "arcanum/spells/task-session-until-blocker/scripts/run_accepted_stream_driver.py"
DRIVER_REQUEST_SCHEMA = "task-session-until-blocker.accepted-stream-driver-request/v1"
DRIVER_RECEIPT_SCHEMA = "task-session-until-blocker.accepted-stream-driver-receipt/v1"
JOIN_SCHEMA = "invoke.accepted-stream-driver-join.v1"
HASH_KEYS = {"path", "sha256"}


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def canonical_digest(value: Any) -> str:
    return sha256_bytes(canonical_bytes(value))


def file_ref(repo_root: Path, relative_path: str) -> dict[str, str]:
    target = repo_root / relative_path
    if not target.is_file():
        raise ContractError(f"installed driver is missing: {relative_path}")
    return {"path": relative_path, "sha256": sha256_bytes(target.read_bytes())}


def _require_hash(value: Any, label: str) -> str:
    if not isinstance(value, str) or len(value) != 64:
        raise ContractError(f"{label} must be a SHA-256 digest")
    try:
        int(value, 16)
    except ValueError:
        raise ContractError(f"{label} must be a SHA-256 digest") from None
    return value


def _frontier_digest(frontier: list[dict[str, Any]]) -> str:
    return canonical_digest(frontier)


def _validate_exact_ref(value: Any, label: str) -> None:
    if not isinstance(value, dict) or set(value) != HASH_KEYS:
        raise ContractError(f"{label} must be an exact reference")
    if not isinstance(value["path"], str) or not value["path"]:
        raise ContractError(f"{label} path is missing")
    _require_hash(value["sha256"], f"{label} sha256")


def _validate_inputs(
    repo_root: Path,
    projection: dict[str, Any],
    accepted_response: dict[str, Any] | None,
    live_baseline: dict[str, Any],
    frozen_frontier: list[dict[str, Any]],
    *,
    no_effect: bool,
) -> tuple[str, list[str]]:
    required_projection = {
        "schema_version",
        "graph_digest",
        "accepted_stream_id",
        "requested_effect",
        "authority",
        "epoch",
        "frontier_digest",
        "acceptance_request_digest",
        "units",
    }
    if set(projection) != required_projection:
        raise ContractError("finalized projection fields are not exact")
    if projection["schema_version"] != "invoke.accepted-stream-finalized-projection.v1":
        raise ContractError("wrong finalized projection schema")
    if not frozen_frontier or len(frozen_frontier) != len(projection["units"]):
        raise ContractError("frozen frontier and units must contain the same nonzero entries")
    if projection["frontier_digest"] != _frontier_digest(frozen_frontier):
        raise ContractError("frozen frontier digest mismatch")
    validate_authority(repo_root, projection["authority"])
    expected_stream = stream_id(
        projection["graph_digest"],
        projection["requested_effect"],
        projection["authority"],
        frozen_frontier,
        projection["epoch"],
    )
    if projection["accepted_stream_id"] != expected_stream:
        raise ContractError("accepted stream identity mismatch")
    frontier_ids: list[str] = []
    prior_ordinal = -1
    for frontier_unit, runtime_unit in zip(frozen_frontier, projection["units"]):
        ordinal = frontier_unit.get("ordinal")
        swu_id = frontier_unit.get("swu_id")
        if not isinstance(ordinal, int) or isinstance(ordinal, bool) or ordinal <= prior_ordinal:
            raise ContractError("frozen frontier ordinals are invalid or reordered")
        if not isinstance(swu_id, str) or not swu_id.startswith("SWU-") or len(swu_id) <= 4:
            raise ContractError("frozen frontier SWU identity is invalid")
        expected_child = child_id(expected_stream, ordinal, swu_id)
        if frontier_unit != {
            "ordinal": ordinal,
            "swu_id": swu_id,
            "child_id": expected_child,
        }:
            raise ContractError("frozen frontier is missing, reordered, or has stale child identity")
        if set(runtime_unit) != {"unit_id", "ordinal", "status", "result_digest"}:
            raise ContractError("runtime unit fields are not exact")
        if runtime_unit["unit_id"] != swu_id or runtime_unit["ordinal"] != ordinal:
            raise ContractError("runtime unit differs from frozen frontier")
        if runtime_unit["status"] not in {"pass", "blocked"}:
            raise ContractError("runtime unit status is invalid")
        _require_hash(runtime_unit["result_digest"], "runtime unit result digest")
        frontier_ids.append(swu_id)
        prior_ordinal = ordinal
    if set(live_baseline) != {
        "schema_version",
        "accepted_stream_id",
        "epoch",
        "frontier_digest",
        "baseline_digest",
        "status",
    }:
        raise ContractError("live baseline fields are not exact")
    if live_baseline["schema_version"] != "invoke.accepted-stream-live-baseline.v1":
        raise ContractError("wrong live baseline schema")
    if live_baseline["status"] != "pass":
        raise ContractError("live baseline did not pass")
    _require_hash(live_baseline["baseline_digest"], "live baseline digest")
    for key in ("accepted_stream_id", "epoch", "frontier_digest"):
        if live_baseline[key] != projection[key]:
            raise ContractError(f"live baseline {key} mismatch")
    if no_effect:
        if accepted_response is not None:
            raise ContractError("no-effect rehearsal must not consume an acceptance response")
        if projection["requested_effect"].get("external_effect") != "none":
            raise ContractError("no-effect rehearsal cannot bind an external effect")
    else:
        if accepted_response is None:
            raise ContractError("effectful mode requires an accepted response")
        expected_response = {
            "schema_version",
            "request_id",
            "request_digest",
            "accepted_stream_id",
            "literal_token",
            "decision",
        }
        if set(accepted_response) != expected_response:
            raise ContractError("accepted response fields are not exact")
        if accepted_response["schema_version"] != "invoke.owner-acceptance-response.v2":
            raise ContractError("wrong accepted response schema")
        if accepted_response["decision"] != "accepted":
            raise ContractError("owner response is not accepted")
        if accepted_response["request_digest"] != projection["acceptance_request_digest"]:
            raise ContractError("accepted response request digest mismatch")
        if accepted_response["accepted_stream_id"] != expected_stream:
            raise ContractError("accepted response stream mismatch")
    return expected_stream, frontier_ids


def compile_request(
    repo_root: Path,
    projection: dict[str, Any],
    accepted_response: dict[str, Any] | None,
    live_baseline: dict[str, Any],
    frozen_frontier: list[dict[str, Any]],
    *,
    no_effect: bool,
) -> dict[str, Any]:
    """Compile the byte-stable public driver request after validating all bindings."""
    stream, frontier_ids = _validate_inputs(
        repo_root,
        projection,
        accepted_response,
        live_baseline,
        frozen_frontier,
        no_effect=no_effect,
    )
    return {
        "schema_version": DRIVER_REQUEST_SCHEMA,
        "stream_id": stream,
        "frontier": frontier_ids,
        "units": projection["units"],
        "no_effect": no_effect,
    }


def driver_identity(repo_root: Path) -> dict[str, Any]:
    return {
        "executable_ref": file_ref(repo_root, DRIVER_PATH),
        "invocation": ["python3", DRIVER_PATH, "--request", "<exact-request-path>"],
    }


def _load_driver(repo_root: Path, identity: dict[str, Any]):
    expected = driver_identity(repo_root)
    if identity != expected:
        raise ContractError("installed driver identity or invocation mismatch")
    spec = importlib.util.spec_from_file_location(
        "accepted_stream_driver_bridge_target", repo_root / DRIVER_PATH
    )
    if spec is None or spec.loader is None:
        raise ContractError("installed driver cannot be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def join_receipt(
    repo_root: Path,
    projection: dict[str, Any],
    live_baseline: dict[str, Any],
    request: dict[str, Any],
    receipts: list[dict[str, Any]],
    *,
    identity: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Join exactly one receipt after replaying the exact installed driver."""
    if len(receipts) != 1:
        raise ContractError("exactly one driver receipt is required")
    identity = driver_identity(repo_root) if identity is None else identity
    driver = _load_driver(repo_root, identity)
    expected_receipt = driver.run(json.loads(canonical_bytes(request)))
    receipt = receipts[0]
    if receipt != expected_receipt:
        raise ContractError("driver receipt is stale, cross-stream, or fabricated")
    if receipt.get("schema_version") != DRIVER_RECEIPT_SCHEMA:
        raise ContractError("wrong driver receipt schema")
    if receipt.get("stream_id") != projection["accepted_stream_id"]:
        raise ContractError("driver receipt stream mismatch")
    if request.get("stream_id") != projection["accepted_stream_id"]:
        raise ContractError("driver request stream mismatch")
    if request.get("frontier") != [unit["unit_id"] for unit in projection["units"]]:
        raise ContractError("driver request frontier mismatch")
    join = {
        "schema_version": JOIN_SCHEMA,
        "accepted_stream_id": projection["accepted_stream_id"],
        "graph_digest": projection["graph_digest"],
        "epoch": projection["epoch"],
        "requested_effect_digest": canonical_digest(projection["requested_effect"]),
        "authority_digest": canonical_digest(projection["authority"]),
        "frontier_digest": projection["frontier_digest"],
        "baseline_digest": live_baseline["baseline_digest"],
        "driver_identity": identity,
        "request_digest": canonical_digest(request),
        "receipt_digest": canonical_digest(receipt),
        "receipt_status": receipt["status"],
        "joined_receipt_count": 1,
        "no_effect": request["no_effect"],
    }
    join["join_digest"] = canonical_digest(join)
    return join


def rehearse_remaining_frontier(repo_root: Path, source: dict[str, Any]) -> dict[str, Any]:
    """Project an unchanged machine-view remaining frontier through the installed driver."""
    source_units = source.get("units")
    if not isinstance(source_units, list) or not source_units:
        raise ContractError("remaining-frontier source must contain nonempty units")
    frontier = []
    prior_ordinal = -1
    for unit in source_units:
        ordinal = unit.get("ordinal")
        swu_id = unit.get("swu_id")
        if not isinstance(ordinal, int) or isinstance(ordinal, bool) or ordinal <= prior_ordinal:
            raise ContractError("remaining-frontier source ordinals are invalid or reordered")
        if not isinstance(swu_id, str) or not swu_id.startswith("SWU-") or len(swu_id) <= 4:
            raise ContractError("remaining-frontier source SWU identity is invalid")
        frontier.append({"ordinal": ordinal, "swu_id": swu_id})
        prior_ordinal = ordinal
    authority = {name: [] for name in WRITE_PARTITIONS}
    requested_effect = {"kind": "no-effect", "external_effect": "none"}
    graph_digest = canonical_digest(source)
    epoch = "no-effect-frontier-" + graph_digest[:16]
    stream = stream_id(graph_digest, requested_effect, authority, frontier, epoch)
    for item in frontier:
        item["child_id"] = child_id(stream, item["ordinal"], item["swu_id"])
    projection = {
        "schema_version": "invoke.accepted-stream-finalized-projection.v1",
        "graph_digest": graph_digest,
        "accepted_stream_id": stream,
        "requested_effect": requested_effect,
        "authority": authority,
        "epoch": epoch,
        "frontier_digest": canonical_digest(frontier),
        "acceptance_request_digest": "0" * 64,
        "units": [
            {"unit_id": item["swu_id"], "ordinal": item["ordinal"], "status": "pass", "result_digest": canonical_digest(source_unit)}
            for item, source_unit in zip(frontier, source_units)
        ],
    }
    baseline = {
        "schema_version": "invoke.accepted-stream-live-baseline.v1",
        "accepted_stream_id": stream,
        "epoch": epoch,
        "frontier_digest": projection["frontier_digest"],
        "baseline_digest": canonical_digest({"source_digest": graph_digest, "frontier_digest": projection["frontier_digest"]}),
        "status": "pass",
    }
    request = compile_request(repo_root, projection, None, baseline, frontier, no_effect=True)
    driver = _load_driver(repo_root, driver_identity(repo_root))
    receipt = driver.run(request)
    joined = join_receipt(repo_root, projection, baseline, request, [receipt])
    return {
        "schema_version": "invoke.remaining-frontier-no-effect-rehearsal.v1",
        "source_digest": graph_digest,
        "frontier": [item["swu_id"] for item in frontier],
        "stable_ordinals": [item["ordinal"] for item in frontier],
        "driver_request_digest": canonical_digest(request),
        "driver_receipt_digest": canonical_digest(receipt),
        "driver_join_digest": joined["join_digest"],
        "completed_count": len(frontier),
        "retry_count": 0,
        "status": receipt["status"],
        "effects": {"selection": False, "admission": False, "execution": False, "external_effect": False},
        "authority_effect": "none",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--frontier-source", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = rehearse_remaining_frontier(Path.cwd(), json.loads(args.frontier_source.read_text(encoding="utf-8")))
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
