#!/usr/bin/env python3
"""Resolve capability dependencies in canonical and generated skill layouts."""

from __future__ import annotations

from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
SKILL_COLLECTION_ROOT = PACKAGE_ROOT.parent
CANONICAL_ARCANUM_ROOT = Path(__file__).resolve().parents[3]


def capability_root(capability_id: str, canonical_tier: str) -> Path:
    """Return one installed capability root without assuming source layout."""

    candidates = (
        CANONICAL_ARCANUM_ROOT / canonical_tier / capability_id,
        SKILL_COLLECTION_ROOT / capability_id,
    )
    for candidate in candidates:
        if candidate.is_dir():
            return candidate
    rendered = ", ".join(str(candidate) for candidate in candidates)
    raise RuntimeError(
        f"required capability '{capability_id}' is not installed; checked {rendered}"
    )
