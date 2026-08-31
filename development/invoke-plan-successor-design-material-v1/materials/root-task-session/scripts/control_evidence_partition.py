#!/usr/bin/env python3
"""Validate the opt-in exact live Task Session control-evidence partition."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
from typing import Any

from jsonschema import Draft202012Validator


SCHEMA = Path(__file__).resolve().parent.parent / "schemas/live-control-evidence-partition-v1.schema.json"


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value


def normalized_path(raw: str) -> str:
    if "\\" in raw:
        raise ValueError(f"control output is not a POSIX locator: {raw}")
    path = PurePosixPath(raw)
    if path.is_absolute() or not path.parts or ".." in path.parts or "." in path.parts:
        raise ValueError(f"control output escapes the repository: {raw}")
    normalized = path.as_posix()
    if normalized != raw:
        raise ValueError(f"control output is not canonical: {raw}")
    return normalized


def overlap(left: str, right: str) -> bool:
    left_path = PurePosixPath(left)
    right_path = PurePosixPath(right)
    return left_path == right_path or left_path in right_path.parents or right_path in left_path.parents


def ensure_no_symlink_chain(repository_root: Path, raw: str) -> Path:
    relative = PurePosixPath(normalized_path(raw))
    current = repository_root.resolve()
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError(f"control output traverses symbolic link: {raw}")
    resolved = (repository_root / relative).resolve()
    resolved.relative_to(repository_root.resolve())
    return resolved


def file_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"state": "absent", "sha256": None, "size_bytes": None}
    if not path.is_file():
        raise ValueError(f"control output is not a regular file: {path}")
    data = path.read_bytes()
    return {"state": "present", "sha256": hashlib.sha256(data).hexdigest(), "size_bytes": len(data)}


def validate_partition(
    partition: dict[str, Any],
    *,
    repository_root: Path,
    attempt_id: str,
    forbidden_scopes: list[str] | None = None,
    run_dir: str | None = None,
    revalidate_runtime: bool = True,
) -> dict[str, Any]:
    errors = sorted(
        Draft202012Validator(load_object(SCHEMA)).iter_errors(partition),
        key=lambda item: list(item.absolute_path),
    )
    if errors:
        first = errors[0]
        location = "/".join(map(str, first.absolute_path)) or "<root>"
        raise ValueError(f"live control partition schema invalid at {location}: {first.message}")
    if partition["attempt_id"] != attempt_id:
        raise ValueError("live control partition attempt differs from execution attempt")
    outputs = partition["outputs"]
    paths = [normalized_path(item["path"]) for item in outputs]
    if len(paths) != len(set(paths)):
        raise ValueError("live control partition output paths are not unique")
    if sorted(paths) != sorted(partition["exact_union_scope"]):
        raise ValueError("live control output paths do not equal exact_union_scope")
    for index, item in enumerate(outputs):
        if item["attempt_id"] != attempt_id:
            raise ValueError(f"live control output attempt mismatch: {item['path']}")
        expected = item.get("expected_postimage_ref")
        if expected is not None and expected["path"] != item["path"]:
            raise ValueError(f"live control expected postimage locator mismatch: {item['path']}")
        path = ensure_no_symlink_chain(repository_root, item["path"])
        for other in paths[index + 1 :]:
            if overlap(item["path"], other):
                raise ValueError(f"live control output scopes overlap: {item['path']} and {other}")
        for forbidden in forbidden_scopes or []:
            normalized_forbidden = normalized_path(forbidden)
            if overlap(item["path"], normalized_forbidden):
                raise ValueError(f"live control output overlaps non-control scope: {item['path']} and {normalized_forbidden}")
        if run_dir is not None:
            normalized_run = normalized_path(run_dir)
            if item["path"] == normalized_run:
                raise ValueError("live control partition may not authorize the run directory as a wildcard")
            if item["write_class"] in {"governance-checkpoint", "execution-ticket", "reconciliation-evidence", "commit-evidence"} and PurePosixPath(normalized_run) not in PurePosixPath(item["path"]).parents:
                raise ValueError(f"runner-owned control output is outside the exact run directory: {item['path']}")
        if not revalidate_runtime:
            continue
        observed = file_state(path)
        if item["runtime_revalidation"] == "baseline-before-write":
            if observed != item["baseline"]:
                raise ValueError(f"live control baseline drift: {item['path']}")
        else:
            expected_state = {
                "state": "present",
                "sha256": expected["sha256"],
                "size_bytes": expected["size_bytes"],
            }
            if observed != expected_state:
                raise ValueError(f"live control postimage drift: {item['path']}")
    return {
        "schema_version": partition["schema_version"],
        "attempt_id": attempt_id,
        "partition_digest": canonical_digest(partition),
        "output_count": len(paths),
        "exact_union_scope": sorted(paths),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--partition", required=True)
    parser.add_argument("--attempt-id", required=True)
    parser.add_argument("--run-dir")
    parser.add_argument("--forbid", action="append", default=[])
    parser.add_argument("--no-runtime-revalidation", action="store_true")
    args = parser.parse_args()
    try:
        result = validate_partition(
            load_object(Path(args.partition)),
            repository_root=Path(args.repo_root).resolve(),
            attempt_id=args.attempt_id,
            forbidden_scopes=args.forbid,
            run_dir=args.run_dir,
            revalidate_runtime=not args.no_runtime_revalidation,
        )
    except (OSError, UnicodeError, ValueError) as error:
        print(json.dumps({"result": "block", "diagnostics": [str(error)]}, sort_keys=True))
        return 2
    print(json.dumps({"result": "pass", **result}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
