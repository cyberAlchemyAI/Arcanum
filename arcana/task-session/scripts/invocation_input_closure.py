#!/usr/bin/env python3
"""Build and validate deterministic exact input closure for one invocation."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
from typing import Any

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parent.parent
SCHEMA = ROOT / "schemas/invocation-input-closure-v1.schema.json"


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    ).hexdigest()


def load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value


def normalized_path(raw: str) -> str:
    relative = PurePosixPath(raw)
    if (
        not raw
        or "\\" in raw
        or relative.is_absolute()
        or ".." in relative.parts
        or "." in relative.parts
        or relative.as_posix() != raw
    ):
        raise ValueError(f"unsafe invocation input locator: {raw}")
    return raw


def resolve(root: Path, raw: str) -> Path:
    relative = PurePosixPath(normalized_path(raw))
    current = root.resolve()
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError(f"invocation input traverses symbolic link: {raw}")
    current.resolve().relative_to(root.resolve())
    return current


def exact_ref(root: Path, path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    return {
        "path": path.resolve().relative_to(root.resolve()).as_posix(),
        "sha256": hashlib.sha256(data).hexdigest(),
        "size_bytes": len(data),
    }


def derive_refs(
    root: Path,
    owner_package_roots: list[str],
    explicit_refs: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    by_path: dict[str, dict[str, Any]] = {}
    for raw_root in sorted(owner_package_roots):
        package = resolve(root, raw_root)
        if not package.is_dir():
            raise ValueError(f"invocation owner package root is not a directory: {raw_root}")
        for path in sorted(package.rglob("*")):
            if "__pycache__" in path.parts or path.suffix == ".pyc":
                continue
            if path.is_symlink():
                raise ValueError(f"invocation owner package contains symbolic link: {path}")
            if path.is_file():
                reference = exact_ref(root, path)
                by_path[reference["path"]] = reference
    for reference in explicit_refs:
        path = resolve(root, reference["path"])
        if not path.is_file() or exact_ref(root, path) != reference:
            raise ValueError(f"stale explicit invocation input: {reference['path']}")
        existing = by_path.get(reference["path"])
        if existing is not None and existing != reference:
            raise ValueError(f"conflicting invocation input reference: {reference['path']}")
        by_path[reference["path"]] = reference
    return [by_path[path] for path in sorted(by_path)]


def build(
    root: Path,
    closure_id: str,
    owner_package_roots: list[str],
    explicit_refs: list[dict[str, Any]],
) -> dict[str, Any]:
    document: dict[str, Any] = {
        "schema_version": "task-session.invocation-input-closure.v1",
        "closure_id": closure_id,
        "owner_package_roots": sorted(owner_package_roots),
        "explicit_refs": sorted(explicit_refs, key=lambda item: item["path"]),
        "input_refs": derive_refs(root, owner_package_roots, explicit_refs),
    }
    document["closure_digest"] = canonical_digest(document)
    validate(root, document)
    return document


def validate(root: Path, document: dict[str, Any]) -> dict[str, Any]:
    schema = load_object(SCHEMA)
    errors = sorted(
        Draft202012Validator(schema).iter_errors(document),
        key=lambda item: list(item.absolute_path),
    )
    if errors:
        first = errors[0]
        raise ValueError(
            "invocation input closure schema invalid at "
            f"{'/'.join(map(str, first.absolute_path)) or '<root>'}: {first.message}"
        )
    projected = dict(document)
    declared_digest = projected.pop("closure_digest")
    if canonical_digest(projected) != declared_digest:
        raise ValueError("invocation input closure digest is not canonical")
    derived = derive_refs(
        root, document["owner_package_roots"], document["explicit_refs"]
    )
    if derived != document["input_refs"]:
        raise ValueError("invocation input closure differs from deterministic package closure")
    return {
        "closure_id": document["closure_id"],
        "closure_digest": declared_digest,
        "input_count": len(derived),
    }


def write_exclusive(path: Path, value: dict[str, Any]) -> None:
    data = (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError:
        if path.read_bytes() != data:
            raise ValueError(f"input closure output already exists with different bytes: {path}")
        return
    with os.fdopen(descriptor, "wb") as handle:
        handle.write(data)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--closure-id", required=True)
    parser.add_argument("--owner-package-root", action="append", required=True)
    parser.add_argument("--explicit-ref", action="append", default=[])
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        root = Path(args.repo_root).resolve()
        explicit = [load_object(resolve(root, raw)) for raw in args.explicit_ref]
        document = build(root, args.closure_id, args.owner_package_root, explicit)
        write_exclusive(resolve(root, args.output), document)
    except (OSError, UnicodeError, ValueError) as error:
        print(json.dumps({"result": "block", "diagnostics": [str(error)]}, sort_keys=True))
        return 2
    print(json.dumps({"result": "pass", "closure_digest": document["closure_digest"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
