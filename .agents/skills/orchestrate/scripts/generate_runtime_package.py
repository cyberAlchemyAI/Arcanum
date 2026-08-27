#!/usr/bin/env python3
"""Generate portable Orchestrate runtime packages from the canonical source."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any

import yaml


CANONICAL_ROOT = Path(__file__).resolve().parents[1]
MANIFEST = json.loads(
    (CANONICAL_ROOT / "generation-manifest.json").read_text(encoding="utf-8")
)
PROVENANCE_KEYS = {
    "surface_kind",
    "runtime",
    "canonical_source",
    "alias_of",
    "generated_by",
    "mutation_policy",
}
PROFILE_TARGETS = {
    "repo-codex": ("codex", Path(".agents/skills/orchestrate")),
    "repo-local": ("local", Path(".arcanum/runtime/orchestrate")),
    "claude": ("claude", Path(".claude/skills/orchestrate")),
}


def split_skill(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        raise ValueError(f"invalid canonical skill frontmatter: {path}")
    _, raw, body = text.split("---", 2)
    frontmatter = yaml.safe_load(raw)
    if not isinstance(frontmatter, dict):
        raise ValueError(f"canonical skill frontmatter must be an object: {path}")
    return frontmatter, body


def generated_skill(runtime: str) -> str:
    frontmatter, body = split_skill(CANONICAL_ROOT / "SKILL.md")
    contract = {
        key: value for key, value in frontmatter.items() if key not in PROVENANCE_KEYS
    }
    generated = {
        "metadata": {
            "surface_kind": "generated-native-runtime-package",
            "runtime": runtime,
            "canonical_source": "runtime/orchestrate/SKILL.md",
            "alias_of": None,
            "generated_by": "tools/bootstrap_arcanum.sh --profile",
            "mutation_policy": "regenerate-from-canonical-source",
        },
        **contract,
    }
    yaml_text = yaml.safe_dump(
        generated,
        allow_unicode=True,
        sort_keys=False,
        width=1000,
    )
    return f"---\n{yaml_text}---{body}"


def copy_support(destination: Path) -> None:
    for relative_value in MANIFEST["support_paths"]:
        relative = Path(relative_value)
        source = CANONICAL_ROOT / relative
        target = destination / relative
        if source.is_dir():
            shutil.copytree(
                source,
                target,
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"),
            )
        elif source.is_file():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
        else:
            raise FileNotFoundError(f"missing canonical support path: {source}")


def generate(target_root: Path, profile: str, force: bool) -> Path:
    runtime, relative = PROFILE_TARGETS[profile]
    root = target_root.resolve()
    destination = (root / relative).resolve()
    destination.relative_to(root)
    if destination.exists():
        if not force:
            raise FileExistsError(f"destination already exists: {destination}")
        if not destination.is_dir() or destination.is_symlink():
            raise ValueError(f"refusing unsafe generated destination: {destination}")
        shutil.rmtree(destination)
    destination.mkdir(parents=True)
    (destination / "SKILL.md").write_text(
        generated_skill(runtime), encoding="utf-8", newline="\n"
    )
    copy_support(destination)
    return destination


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate Orchestrate packages without shell-specific tooling."
    )
    parser.add_argument("--target", required=True, type=Path)
    parser.add_argument(
        "--profiles",
        default="repo-codex",
        help="Comma-separated: repo-codex, repo-local, claude",
    )
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    if not args.target.is_dir():
        parser.error("--target must be an existing directory")
    profiles = [item.strip() for item in args.profiles.split(",") if item.strip()]
    if not profiles or any(item not in PROFILE_TARGETS for item in profiles):
        parser.error("--profiles must contain repo-codex, repo-local, or claude")
    if len(set(profiles)) != len(profiles):
        parser.error("--profiles contains duplicates")
    for profile in profiles:
        destination = generate(args.target, profile, args.force)
        print(f"generated {profile}: {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
