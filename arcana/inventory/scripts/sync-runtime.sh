#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  sync-runtime.sh (--check | --apply) --target <inventory-root> [--json]
USAGE
}

mode=""
target=""
json_output="0"
while [[ "$#" -gt 0 ]]; do
  case "$1" in
    --check) mode="check"; shift ;;
    --apply) mode="apply"; shift ;;
    --target) target="$2"; shift 2 ;;
    --json) json_output="1"; shift ;;
    --help|-h) usage; exit 0 ;;
    *) printf 'ERROR: unknown argument: %s\n' "$1" >&2; usage >&2; exit 2 ;;
  esac
done

if [[ -z "$mode" || -z "$target" ]]; then
  usage >&2
  exit 2
fi

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source_root="$(cd "$script_dir/.." && pwd)"

python3 - "$mode" "$source_root" "$target" "$json_output" <<'PY'
from __future__ import annotations

import hashlib
import json
import os
import shutil
import sys
from pathlib import Path, PurePosixPath


mode, source_value, target_value, json_output = sys.argv[1:]
source_root = Path(source_value).resolve()
target_root = Path(target_value).resolve()
manifest_path = source_root / "runtime-manifest.json"
manifest_bytes = manifest_path.read_bytes()
manifest = json.loads(manifest_bytes)
forbidden = {
    "entries", "queries", "raw", "receipts",
    "index.json", "index.md", "schema.md", "tags.md", "log.md",
}


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def safe_relative(value: str) -> str:
    pure = PurePosixPath(value)
    if (
        not value
        or pure.is_absolute()
        or ".." in pure.parts
        or "\\" in value
    ):
        raise ValueError(f"unsafe manifest path: {value}")
    if pure.parts[0] in forbidden:
        raise ValueError(f"consumer-owned path in runtime manifest: {value}")
    return pure.as_posix()


if target_root == Path("/") or target_root == source_root:
    raise SystemExit("refusing unsafe runtime sync target")
if manifest.get("schema_version") != "inventory.runtime-manifest.v1":
    raise SystemExit("unsupported runtime manifest")

members = manifest.get("members", [])
expected: dict[str, str] = {}
for member in members:
    relative = safe_relative(member["path"])
    if relative in expected:
        raise SystemExit(f"duplicate runtime manifest path: {relative}")
    source_path = source_root.joinpath(*PurePosixPath(relative).parts)
    observed = sha256_bytes(source_path.read_bytes())
    if observed != member["sha256"]:
        raise SystemExit(f"canonical runtime member digest mismatch: {relative}")
    expected[relative] = member["sha256"]

canonical_members = json.dumps(
    members, sort_keys=True, separators=(",", ":")
) + "\n"
if sha256_bytes(canonical_members.encode()) != manifest.get("bundle_sha256"):
    raise SystemExit("canonical runtime bundle digest mismatch")

expected["runtime-manifest.json"] = sha256_bytes(manifest_bytes)
managed_roots = tuple(manifest.get("managed_roots", []))
managed_files = set(manifest.get("managed_files", []))
for value in [*managed_roots, *managed_files]:
    safe_relative(value)


def target_digest(relative: str) -> str | None:
    candidate = target_root.joinpath(*PurePosixPath(relative).parts)
    if not candidate.is_file():
        return None
    return sha256_bytes(candidate.read_bytes())


def actual_managed_files() -> set[str]:
    paths: set[str] = set()
    for root_name in managed_roots:
        root = target_root / root_name
        if not root.exists():
            continue
        for candidate in root.rglob("*"):
            if candidate.is_file() or candidate.is_symlink():
                paths.add(candidate.relative_to(target_root).as_posix())
    for relative in managed_files:
        candidate = target_root.joinpath(*PurePosixPath(relative).parts)
        if candidate.is_file() or candidate.is_symlink():
            paths.add(relative)
    return paths


def inspect() -> dict[str, list[str]]:
    missing: list[str] = []
    drifted: list[str] = []
    for relative, digest in expected.items():
        observed = target_digest(relative)
        if observed is None:
            missing.append(relative)
        elif observed != digest:
            drifted.append(relative)
    extra = sorted(actual_managed_files() - set(expected))
    return {
        "missing": sorted(missing),
        "drifted": sorted(drifted),
        "extra_managed": extra,
    }


before = inspect()
changed: list[str] = []
if mode == "apply":
    target_root.mkdir(parents=True, exist_ok=True)
    for relative in sorted(expected):
        target = target_root.joinpath(*PurePosixPath(relative).parts)
        target.parent.mkdir(parents=True, exist_ok=True)
        source = manifest_path if relative == "runtime-manifest.json" else (
            source_root.joinpath(*PurePosixPath(relative).parts)
        )
        if target_digest(relative) != expected[relative]:
            shutil.copy2(source, target)
            changed.append(relative)
    for relative in before["extra_managed"]:
        target = target_root.joinpath(*PurePosixPath(relative).parts)
        if target.is_symlink() or target.is_file():
            target.unlink()
            changed.append(relative)
    for root_name in managed_roots:
        root = target_root / root_name
        if root.is_dir():
            for directory, _, _ in os.walk(root, topdown=False):
                candidate = Path(directory)
                if candidate != root and not any(candidate.iterdir()):
                    candidate.rmdir()

after = inspect()
clean_after = not any(after.values())
report = {
    "schema_version": "inventory.runtime-sync-result.v1",
    "mode": mode,
    "status": (
        "clean" if mode == "check" and clean_after
        else "drift" if mode == "check"
        else "applied" if clean_after
        else "apply-failed"
    ),
    "before": before,
    "after": after,
    "changed_paths": sorted(set(changed)),
    "managed_paths": sorted(expected),
    "authority_boundary": "generated-runtime-only",
}
if json_output == "1":
    print(json.dumps(report, indent=2))
else:
    print(json.dumps(report, separators=(",", ":")))
raise SystemExit(0 if clean_after else 1)
PY
