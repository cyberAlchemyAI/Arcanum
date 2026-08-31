#!/usr/bin/env python3
"""Render three order-only documentation candidates from shared section bytes."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
GUIDES = ROOT / "guides"
EXAMPLE = ROOT / "shared/example-evidence.md"

ORDERS = {
    "alpha": [
        "04-source-fields.md",
        "05-definition-fields.md",
        "01-artifact-boundary.md",
        "02-ownership.md",
        "06-evidence-cookbook.md",
        "07-complete-example.md",
        "03-workflow.md",
        "08-diagnostics.md",
        "09-validation.md",
    ],
    "beta": [
        "01-artifact-boundary.md",
        "03-workflow.md",
        "07-complete-example.md",
        "04-source-fields.md",
        "05-definition-fields.md",
        "06-evidence-cookbook.md",
        "02-ownership.md",
        "08-diagnostics.md",
        "09-validation.md",
    ],
    "gamma": [
        "01-artifact-boundary.md",
        "02-ownership.md",
        "03-workflow.md",
        "04-source-fields.md",
        "05-definition-fields.md",
        "06-evidence-cookbook.md",
        "07-complete-example.md",
        "08-diagnostics.md",
        "09-validation.md",
    ],
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def build_expected(root: Path = ROOT) -> tuple[dict[str, bytes], dict[str, object]]:
    """Build guide bytes and their manifest in memory without writing files."""

    content = root / "content"
    example = root / "shared/example-evidence.md"
    example_bytes = example.read_bytes()
    replacements = {
        "{{EXAMPLE_SHA256}}": sha256(example_bytes),
        "{{EXAMPLE_SIZE}}": str(len(example_bytes)),
    }
    section_names = sorted(path.name for path in content.glob("*.md"))
    if set(section_names) != set(ORDERS["alpha"]):
        raise SystemExit("section inventory does not match the fixed candidate order")
    for order in ORDERS.values():
        if len(order) != len(set(order)) or set(order) != set(section_names):
            raise SystemExit("candidate order is not a permutation of the section inventory")

    rendered_sections: dict[str, str] = {}
    for name in section_names:
        text = (content / name).read_text(encoding="utf-8").strip()
        for old, new in replacements.items():
            text = text.replace(old, new)
        if "{{" in text or "}}" in text:
            raise SystemExit(f"unresolved template marker in {name}")
        rendered_sections[name] = text

    guide_bytes: dict[str, bytes] = {}
    guides: dict[str, dict[str, object]] = {}
    for candidate, order in ORDERS.items():
        body = "# Invoke Define v2 Authoring Guide\n\n" + "\n\n".join(
            rendered_sections[name] for name in order
        ) + "\n"
        relative_path = f"guides/guide-{candidate}.md"
        encoded = body.encode("utf-8")
        guide_bytes[relative_path] = encoded
        guides[candidate] = {
            "path": relative_path,
            "sha256": sha256(encoded),
            "size": len(encoded),
            "section_order": order,
        }

    section_manifest = {
        name: {
            "sha256": sha256(rendered_sections[name].encode("utf-8")),
            "size": len(rendered_sections[name].encode("utf-8")),
        }
        for name in section_names
    }
    manifest = {
        "schema_version": "invoke.define-documentation-tournament-guides.v1",
        "controlled_variable": "section-order-only",
        "shared_sections": section_manifest,
        "guides": guides,
        "equivalence": {
            "same_section_inventory": True,
            "same_rendered_section_bytes": True,
            "candidate_specific_prose": False,
        },
    }
    return guide_bytes, manifest


def main() -> int:
    guide_bytes, manifest = build_expected(ROOT)
    GUIDES.mkdir(parents=True, exist_ok=True)
    for relative_path, body in guide_bytes.items():
        (ROOT / relative_path).write_bytes(body)
    (ROOT / "GUIDE-MANIFEST.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print("GUIDE_RENDER=pass")
    print("CONTROLLED_VARIABLE=section-order-only")
    print(f"GUIDE_COUNT={len(guide_bytes)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
