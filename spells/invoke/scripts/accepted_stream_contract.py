#!/usr/bin/env python3
"""Canonical identities, paths, authority sets, and static bundle validation."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import unicodedata
from pathlib import Path, PurePosixPath
from typing import Any

STREAM_DOMAIN = b"invoke.accepted-stream.v1\0"
CHILD_DOMAIN = b"invoke.accepted-stream-child.v1\0"
WRITE_PARTITIONS = ("material", "control", "terminal", "lifecycle", "transient", "failure", "claim", "stream")


class ContractError(ValueError):
    pass


def canonical_bytes(value: Any) -> bytes:
    """RFC-8785-compatible encoding for the integer-only contract model."""
    def check(item: Any) -> None:
        if isinstance(item, float):
            raise ContractError("floating point values are not permitted")
        if isinstance(item, dict):
            if not all(isinstance(key, str) for key in item):
                raise ContractError("object keys must be strings")
            for key, child in item.items():
                if unicodedata.normalize("NFC", key) != key:
                    raise ContractError("object keys must be NFC")
                check(child)
        elif isinstance(item, list):
            for child in item:
                check(child)
        elif isinstance(item, str) and unicodedata.normalize("NFC", item) != item:
            raise ContractError("strings must be NFC")
        elif item is not None and not isinstance(item, (str, int, bool, list, dict)):
            raise ContractError(f"unsupported JSON type: {type(item).__name__}")
    check(value)
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest(domain: bytes, value: Any) -> str:
    return hashlib.sha256(domain + canonical_bytes(value)).hexdigest()


def stream_id(graph_digest: str, requested_effect: Any, authority: Any, frontier: list[Any], epoch: str) -> str:
    # Child identities contain the stream identity, so only the non-circular
    # frontier projection contributes to the stream identity.
    frontier_identity = [
        {"ordinal": unit["ordinal"], "swu_id": unit["swu_id"]}
        for unit in frontier
    ]
    return digest(STREAM_DOMAIN, {"authority": authority, "epoch": epoch, "frontier": frontier_identity, "graph_digest": graph_digest, "requested_effect": requested_effect})


def child_id(accepted_stream_id: str, ordinal: int, swu_id: str) -> str:
    if ordinal < 0:
        raise ContractError("ordinal must be non-negative")
    return digest(CHILD_DOMAIN, {"accepted_stream_id": accepted_stream_id, "ordinal": ordinal, "swu_id": swu_id})


def normalize_repo_path(repo_root: Path, raw: str, *, allow_missing: bool = True) -> str:
    if not raw or "\\" in raw or any(ch in raw for ch in "*?[]"):
        raise ContractError("path must be a non-glob POSIX repository-relative path")
    if unicodedata.normalize("NFC", raw) != raw:
        raise ContractError("path must be NFC")
    pure = PurePosixPath(raw)
    if pure.is_absolute() or ".." in pure.parts or "." in pure.parts:
        raise ContractError("path is not normalized repository-relative")
    root = repo_root.resolve(strict=True)
    candidate = root.joinpath(*pure.parts)
    probe = candidate
    while not probe.exists() and probe != root:
        probe = probe.parent
    if not allow_missing and not candidate.exists():
        raise ContractError("path does not exist")
    try:
        probe.resolve(strict=True).relative_to(root)
    except (FileNotFoundError, ValueError):
        raise ContractError("path escapes repository") from None
    return pure.as_posix()


def validate_authority(repo_root: Path, authority: dict[str, list[str]]) -> list[str]:
    if set(authority) != set(WRITE_PARTITIONS):
        raise ContractError("write partitions are not exact")
    normalized: list[str] = []
    for partition in WRITE_PARTITIONS:
        for path in authority[partition]:
            normalized.append(normalize_repo_path(repo_root, path))
    if len(normalized) != len(set(normalized)):
        raise ContractError("write partitions overlap")
    return sorted(normalized)


def validate_bundle(bundle: dict[str, Any], repo_root: Path) -> None:
    if bundle.get("schema_version") != "invoke.accepted-stream-static-bundle.v1":
        raise ContractError("wrong bundle schema")
    frontier = bundle.get("frontier")
    if not isinstance(frontier, list) or not frontier:
        raise ContractError("frontier must contain at least one unit")
    identities: list[str] = []
    ordinals: list[int] = []
    for unit in frontier:
        ordinal = unit.get("ordinal")
        swu_id = unit.get("swu_id")
        if not isinstance(ordinal, int) or isinstance(ordinal, bool) or ordinal < 0:
            raise ContractError("frontier ordinal must be a non-negative integer")
        if not isinstance(swu_id, str) or not swu_id.startswith("SWU-") or len(swu_id) <= 4:
            raise ContractError("frontier SWU identity is invalid")
        ordinals.append(ordinal); identities.append(swu_id)
    if ordinals != sorted(set(ordinals)) or len(identities) != len(set(identities)):
        raise ContractError("frontier is missing, duplicate, or reordered")
    accepted = validate_authority(repo_root, bundle.get("write_partitions", {}))
    declared = [normalize_repo_path(repo_root, item) for item in bundle.get("accepted_write_paths", [])]
    if declared != sorted(set(declared)) or declared != accepted:
        raise ContractError("accepted_write_paths must equal the disjoint partition union")
    expected = stream_id(bundle["graph_digest"], bundle["requested_effect"], bundle["write_partitions"], frontier, bundle["epoch"])
    if bundle.get("accepted_stream_id") != expected:
        raise ContractError("accepted stream identity mismatch")
    for unit in frontier:
        if unit.get("child_id") != child_id(expected, unit["ordinal"], unit["swu_id"]):
            raise ContractError("child identity mismatch")


def _fixture(root: Path) -> dict[str, Any]:
    frontier = [{"ordinal": i, "swu_id": f"SWU-GENERIC-{i + 1:03d}"} for i in (1, 4, 9)]
    authority = {name: [] for name in WRITE_PARTITIONS}
    authority["material"] = ["arcanum/spells/invoke/development/accepted-stream-runtime/output.json"]
    sid = stream_id("0" * 64, {"kind": "bounded-write", "external_effect": "none"}, authority, frontier, "epoch-001")
    for unit in frontier:
        unit["child_id"] = child_id(sid, unit["ordinal"], unit["swu_id"])
    return {"schema_version": "invoke.accepted-stream-static-bundle.v1", "graph_digest": "0" * 64, "epoch": "epoch-001", "requested_effect": {"kind": "bounded-write", "external_effect": "none"}, "frontier": frontier, "write_partitions": authority, "accepted_write_paths": authority["material"], "accepted_stream_id": sid}


def self_test(repo_root: Path) -> None:
    good = _fixture(repo_root)
    validate_bundle(good, repo_root)
    mutations = [
        lambda x: x["frontier"].pop(),
        lambda x: x["frontier"].reverse(),
        lambda x: x["write_partitions"]["control"].append(x["accepted_write_paths"][0]),
        lambda x: x.update(accepted_stream_id="f" * 64),
        lambda x: x["accepted_write_paths"].append("../escape"),
        lambda x: x["write_partitions"].update(extra=[]),
    ]
    for mutate in mutations:
        candidate = json.loads(json.dumps(good)); mutate(candidate)
        try: validate_bundle(candidate, repo_root)
        except ContractError: continue
        raise AssertionError("negative fixture passed")
    print("PASS SWU-MVLR-001 positive=1 negative=6")


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--validate-swu"); parser.add_argument("--bundle", type=Path)
    args = parser.parse_args(); root = Path.cwd()
    try:
        if args.validate_swu == "SWU-MVLR-001": self_test(root)
        elif args.bundle: validate_bundle(json.loads(args.bundle.read_text()), root); print("PASS")
        else: parser.error("provide --validate-swu SWU-MVLR-001 or --bundle")
    except (ContractError, KeyError, json.JSONDecodeError) as exc:
        print(f"BLOCK: {exc}"); return 2
    return 0


if __name__ == "__main__": raise SystemExit(main())
