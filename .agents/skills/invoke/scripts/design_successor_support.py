#!/usr/bin/env python3
"""Internal helpers for additive Design successor executable identities."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
from types import ModuleType
from typing import Any


SCHEMA_ALIASES = {
    "https://arcanum.dev/schemas/invoke/design-input-closure/v1": "https://arcanum.dev/schemas/invoke/design-input-closure/v2",
    "https://arcanum.dev/schemas/invoke/design-input-closure-receipt/v1": "https://arcanum.dev/schemas/invoke/design-input-closure-receipt/v2",
    "https://arcanum.dev/schemas/invoke/design-input-production-receipt/v1": "https://arcanum.dev/schemas/invoke/design-input-production-receipt/v2",
    "https://arcanum.dev/schemas/invoke/design-source/v1": "https://arcanum.dev/schemas/invoke/design-source/v2",
    "https://arcanum.dev/schemas/invoke/design-artifact/v1": "https://arcanum.dev/schemas/invoke/design-artifact/v2",
    "https://arcanum.dev/schemas/invoke/design-coherence-receipt/v1": "https://arcanum.dev/schemas/invoke/design-coherence-receipt/v2",
    "https://arcanum.dev/schemas/invoke/design-candidate-production-receipt/v1": "https://arcanum.dev/schemas/invoke/design-candidate-production-receipt/v2",
    "https://arcanum.dev/schemas/invoke/design-bundle-closure/v1": "https://arcanum.dev/schemas/invoke/design-bundle-closure/v2",
    "https://arcanum.dev/schemas/invoke/design-bundle-attempt-receipt/v1": "https://arcanum.dev/schemas/invoke/design-bundle-attempt-receipt/v2",
    "https://arcanum.dev/schemas/invoke/design-result/v2": "https://arcanum.dev/schemas/invoke/design-result/v3",
    "https://arcanum.dev/schemas/invoke/design-bundle-admission-receipt/v1": "https://arcanum.dev/schemas/invoke/design-bundle-admission-receipt/v2",
}


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load Design predecessor implementation: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_store(schema_dir: Path) -> dict[str, dict[str, Any]]:
    store: dict[str, dict[str, Any]] = {}
    for path in schema_dir.glob("*.schema.json"):
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(value, dict) and isinstance(value.get("$id"), str):
            store[value["$id"]] = value
    return store


def aliased_store(schema_dir: Path) -> dict[str, dict[str, Any]]:
    # Preserve historical URI bindings: successor schemas intentionally refer back
    # to unchanged v1 definitions, so overwriting a v1 URI would break local $refs.
    return load_store(schema_dir)


def schema_for_document(
    document: dict[str, Any],
    fallback: dict[str, Any],
    store: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    schema_uri = document.get("$schema")
    if isinstance(schema_uri, str) and schema_uri in store:
        return store[schema_uri]
    return fallback


def canonical_digest(document: dict[str, Any], field: str) -> str:
    value = {key: item for key, item in document.items() if key != field}
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def translate_identity(
    document: dict[str, Any],
    *,
    schema_uri: str,
    schema_version: str,
    digest_field: str,
    identity: str | None = None,
    path: str | None = None,
    executable: Path | None = None,
) -> dict[str, Any]:
    result = json.loads(json.dumps(document))
    result["$schema"] = schema_uri
    result["schema_version"] = schema_version
    if identity is not None:
        owner = "producer" if "producer" in result else "validator"
        result[owner]["identity"] = identity
        if path is not None:
            result[owner]["path"] = path
        if executable is not None:
            result[owner]["sha256"] = hashlib.sha256(executable.read_bytes()).hexdigest()
    result[digest_field] = "0" * 64
    result[digest_field] = canonical_digest(result, digest_field)
    return result
