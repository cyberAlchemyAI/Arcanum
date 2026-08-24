#!/usr/bin/env python3
"""Validate a sigil candidate as a virtual overlay at its canonical targets."""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import sys
import urllib.parse

import yaml


MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
PRE_APPLY_STATE = "repaired_candidate_awaiting_renewed_owner_acceptance"
LIVE_PENDING_STATE = (
    "repaired_candidate_present_in_canonical_awaiting_renewed_owner_acceptance"
)


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative_file_set(root: pathlib.Path) -> set[str]:
    return {
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file() and path.name != "__pycache__"
    }


def projected_link_target(
    raw_target: str,
    source_target: pathlib.Path,
    canonical_root: pathlib.Path,
) -> pathlib.Path | None:
    target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
    if not target or target.startswith("#"):
        return None
    parsed = urllib.parse.urlsplit(target)
    if parsed.scheme or parsed.netloc:
        return None
    path_text = urllib.parse.unquote(parsed.path)
    if not path_text:
        return None
    if path_text.startswith("/"):
        raise AssertionError(f"repository-absolute Markdown link is forbidden: {raw_target}")
    resolved = (source_target.parent / path_text).resolve()
    canonical = canonical_root.resolve()
    if resolved != canonical and canonical not in resolved.parents:
        raise AssertionError(
            f"projected Markdown link escapes canonical sigil root: {raw_target}"
        )
    return resolved


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=pathlib.Path)
    parser.add_argument("--canonical-root", type=pathlib.Path)
    args = parser.parse_args()

    candidate = (args.candidate or pathlib.Path(__file__).resolve().parent).resolve()
    canonical_root = (
        args.canonical_root.resolve()
        if args.canonical_root
        else candidate.parents[2].resolve()
    )
    manifest_path = candidate / "CANDIDATE-MANIFEST.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert manifest["schema_version"] == "arcanum.sigil-candidate-manifest.v1"
    assert manifest["target_sigil"] == canonical_root.name
    state = manifest["state"]
    assert state in {PRE_APPLY_STATE, LIVE_PENDING_STATE}, (
        f"unsupported candidate state: {state}"
    )

    target_rows = manifest["files"]
    sidecar_rows = manifest["sidecars"]
    targets = [row["target"] for row in target_rows]
    assert len(targets) == 7
    assert len(targets) == len(set(targets))

    expected_files = {"CANDIDATE-MANIFEST.json"}
    expected_files.update(targets)
    expected_files.update(row["path"] for row in sidecar_rows)
    actual_files = relative_file_set(candidate)
    assert actual_files == expected_files, {
        "missing": sorted(expected_files - actual_files),
        "unexpected": sorted(actual_files - expected_files),
    }

    overlay: dict[pathlib.Path, pathlib.Path] = {}
    for row in target_rows:
        candidate_path = candidate / row["target"]
        canonical_path = canonical_root / row["target"]
        assert candidate_path.is_file()
        assert canonical_path.is_file()
        assert sha256(candidate_path) == row["candidate_sha256"]
        assert candidate_path.stat().st_size == row["candidate_bytes"]
        canonical_sha256 = sha256(canonical_path)
        if state == PRE_APPLY_STATE:
            assert canonical_sha256 == row["input_sha256"], (
                f"canonical input drift: {row['target']}"
            )
        else:
            assert canonical_sha256 == row["candidate_sha256"], (
                f"live canonical bytes do not match candidate: {row['target']}"
            )
            assert canonical_path.stat().st_size == row["candidate_bytes"], (
                f"live canonical byte count does not match candidate: {row['target']}"
            )
        overlay[canonical_path.resolve()] = candidate_path

    for row in sidecar_rows:
        path = candidate / row["path"]
        assert path.is_file()
        assert sha256(path) == row["sha256"]
        assert path.stat().st_size == row["bytes"]

    json_count = 0
    yaml_count = 0
    for row in target_rows:
        path = candidate / row["target"]
        if path.suffix == ".json":
            json.loads(path.read_text(encoding="utf-8"))
            json_count += 1
        elif path.suffix in {".yml", ".yaml"}:
            yaml.safe_load(path.read_text(encoding="utf-8"))
            yaml_count += 1

    cards_path = candidate / "development/UX-EVIDENCE-REFERENCE-CARDS.yml"
    cards_doc = yaml.safe_load(cards_path.read_text(encoding="utf-8"))
    cards = cards_doc["cards"]
    card_ids = [card["id"] for card in cards]
    assert len(card_ids) == len(set(card_ids)) == manifest["validation"]["card_count"]
    external_count = sum(
        1 for card in cards if card.get("source_class") == "external_noncanonical"
    )
    assert external_count == manifest["validation"]["external_card_count"]

    checked_links: list[dict[str, str]] = []
    for row in target_rows:
        candidate_path = candidate / row["target"]
        if candidate_path.suffix != ".md":
            continue
        source_target = (canonical_root / row["target"]).resolve()
        text = candidate_path.read_text(encoding="utf-8")
        for raw_target in MARKDOWN_LINK.findall(text):
            resolved = projected_link_target(raw_target, source_target, canonical_root)
            if resolved is None:
                continue
            source_bytes = overlay.get(resolved, resolved)
            assert source_bytes.exists(), {
                "source": row["target"],
                "link": raw_target,
                "projected": str(resolved),
            }
            checked_links.append(
                {
                    "source": row["target"],
                    "link": raw_target,
                    "projected": resolved.relative_to(canonical_root).as_posix(),
                    "resolved_from": "candidate-overlay" if resolved in overlay else "canonical",
                }
            )

    for path in sorted(candidate.rglob("*")):
        if not path.is_file() or path.suffix not in {".md", ".json", ".yml", ".yaml", ".py"}:
            continue
        text = path.read_text(encoding="utf-8")
        for line_number, line in enumerate(text.splitlines(), 1):
            assert line == line.rstrip(" \t"), f"trailing whitespace: {path}:{line_number}"
        unresolved = r"\b(" + "|".join(("TO" + "DO", "T" + "BD", "FIX" + "ME", "PLACE" + "HOLDER")) + r")\b"
        assert not re.search(unresolved, text), path

    result = {
        "status": "pass",
        "candidate_id": manifest["candidate_id"],
        "candidate_state": state,
        "canonical_root": canonical_root.as_posix(),
        "target_count": len(target_rows),
        "sidecar_count": len(sidecar_rows),
        "json_targets_parsed": json_count,
        "yaml_targets_parsed": yaml_count,
        "card_count": len(card_ids),
        "external_card_count": external_count,
        "projected_markdown_links_checked": len(checked_links),
        "projected_markdown_links": checked_links,
        "canonical_inputs_unchanged": state == PRE_APPLY_STATE,
        "canonical_candidate_bytes_match": state == LIVE_PENDING_STATE,
        "candidate_inventory_exact": True,
        "owner_acceptance": "pending",
        "promotion_or_publication_authorized": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, KeyError, TypeError, ValueError, yaml.YAMLError) as error:
        print(f"TARGET_OVERLAY_VALIDATION_BLOCK: {error}", file=sys.stderr)
        raise SystemExit(1)
