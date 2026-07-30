"""Digest-bound single-process claim compare-and-set."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def claim_decision(request: dict[str, Any], frontier: dict[str, Any], store_path: Path) -> dict[str, Any]:
    store = json.loads(store_path.read_text(encoding="utf-8"))
    before_digest = canonical_digest(store)
    eligible = {item["id"]: item["eligible"] for item in frontier["nodes"]}
    reason = None
    if request["source_digest"] != frontier["source_digest"]:
        reason = "STALE_SOURCE"
    elif request["expected_store_digest"] != before_digest:
        reason = "CAS_MISMATCH"
    elif request["decision_id"] not in eligible:
        reason = "UNKNOWN_DECISION"
    elif not eligible[request["decision_id"]]:
        reason = "NOT_ELIGIBLE"
    elif any(
        item["decision_id"] == request["decision_id"]
        and item["source_digest"] == request["source_digest"]
        and item["status"] == "active"
        for item in store["claims"]
    ):
        reason = "ACTIVE_CLAIM"
    if reason:
        return {"status": "rejected", "code": reason, "store_digest": before_digest}

    claim = {
        "schema_version": "1.0.0",
        "kind": "claim",
        "claim_id": request["claim_id"],
        "decision_id": request["decision_id"],
        "source_digest": request["source_digest"],
        "owner": request["owner"],
        "claimed_at": request["claimed_at"],
        "status": "active",
        "previous_store_digest": before_digest,
    }
    updated = {"schema_version": "1.0.0", "claims": [*store["claims"], claim]}
    temporary = store_path.with_name(store_path.name + ".tmp")
    with temporary.open("wb") as handle:
        handle.write(canonical_bytes(updated) + b"\n")
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, store_path)
    return {
        "status": "accepted",
        "code": "CLAIM_ACCEPTED",
        "claim": claim,
        "before_store_digest": before_digest,
        "after_store_digest": canonical_digest(updated),
    }
