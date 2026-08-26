#!/usr/bin/env python3
"""Validate Arcanum artifact metadata for governed source artifacts."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = [
    "artifact_id",
    "artifact_type",
    "intent",
    "owner",
    "lifecycle_status",
    "constitution_selectors",
    "validation_profile",
]

LIST_FIELDS = {"constitution_selectors", "validation_profile"}
METADATA_FIELDS = set(REQUIRED_FIELDS) | {
    "evidence_role",
    "canonical_format",
    "companion_to",
    "supersedes",
    "expires_when",
}
VALID_STATUSES = {
    "candidate",
    "reviewed",
    "canonical",
    "deprecated",
    "generated",
    "local-runtime",
}


class MetadataParseError(ValueError):
    """Raised when governed metadata is not in the supported strict YAML subset."""

GENERATED_PREFIXES = (
    ".arcanum/observability/",
    ".arcanum/runtime/",
    ".arcanum/codex-home/",
    ".arcanum/codex-home-smoke/",
    "benchmark/artifacts/",
    "benchmark/logs/",
    "tmp/",
)


def run_git(args: list[str]) -> list[str]:
    try:
        result = subprocess.run(
            ["git", *args],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []
    return [line for line in result.stdout.splitlines() if line]


def repo_root() -> Path:
    lines = run_git(["rev-parse", "--show-toplevel"])
    if lines:
        return Path(lines[0])
    return Path.cwd()


def rel_path(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def is_generated_or_runtime(rel: str) -> bool:
    return rel.startswith(GENERATED_PREFIXES)


def is_candidate_governed_path(rel: str) -> bool:
    if is_generated_or_runtime(rel):
        return False
    if rel.startswith((".codex/commands/", "arcana/", "spells/", "transmutations/", "framework/", "disciplines/", "registry/", "tools/")):
        return Path(rel).suffix.lower() in {".md", ".yml", ".yaml", ".json", ".sh", ".py"}
    return False


def parse_scalar(value: str, *, line_number: int) -> Any:
    value = value.strip()
    if not value:
        return ""
    if value in {"[]", "null", "~"}:
        return [] if value == "[]" else None
    if value.startswith('"'):
        if not value.endswith('"') or len(value) == 1:
            raise MetadataParseError(f"line {line_number}: unterminated double-quoted scalar")
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError as exc:
            raise MetadataParseError(f"line {line_number}: invalid double-quoted scalar: {exc.msg}") from exc
        if not isinstance(parsed, str):
            raise MetadataParseError(f"line {line_number}: quoted metadata scalar must be a string")
        return parsed
    if value.startswith("'"):
        if not value.endswith("'") or len(value) == 1:
            raise MetadataParseError(f"line {line_number}: unterminated single-quoted scalar")
        return value[1:-1].replace("''", "'")
    if value.endswith(('"', "'")):
        raise MetadataParseError(f"line {line_number}: closing quote has no matching opening quote")
    return value


def parse_simple_yaml_mapping(lines: list[str], *, context: str = "metadata") -> dict[str, Any]:
    data: dict[str, Any] = {}
    current_key: str | None = None
    for line_number, raw in enumerate(lines, 1):
        if "\t" in raw:
            raise MetadataParseError(f"{context} line {line_number}: tabs are forbidden in indentation or content")
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.startswith(" "):
            if current_key is None:
                raise MetadataParseError(f"{context} line {line_number}: unexpected indentation")
            if not raw.startswith("  - ") or raw.startswith("   "):
                raise MetadataParseError(
                    f"{context} line {line_number}: list items must use exactly two spaces followed by `- `"
                )
            item = raw[4:]
            if not item.strip():
                raise MetadataParseError(f"{context} line {line_number}: empty list item")
            data[current_key].append(parse_scalar(item, line_number=line_number))
            continue
        match = re.match(r"^([A-Za-z0-9_-]+):(?:\s*(.*))?$", raw)
        if not match:
            raise MetadataParseError(f"{context} line {line_number}: unconsumed or invalid YAML line: {raw!r}")
        key, value = match.group(1), match.group(2) or ""
        if key in data:
            raise MetadataParseError(f"{context} line {line_number}: duplicate key `{key}`")
        if value.strip() == "":
            data[key] = []
            current_key = key
        else:
            data[key] = parse_scalar(value, line_number=line_number)
            current_key = None
    return data


def extract_markdown_frontmatter(text: str) -> dict[str, Any] | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    block = text[4:end].strip("\n")
    top_level_keys = {
        match.group(1)
        for raw in block.splitlines()
        if not raw.startswith((" ", "\t"))
        if (match := re.match(r"^([A-Za-z0-9_-]+):", raw))
    }
    if not METADATA_FIELDS.intersection(top_level_keys):
        return None
    return parse_simple_yaml_mapping(block.splitlines(), context="Markdown frontmatter")


def is_artifact_metadata_block(metadata: dict[str, Any] | None) -> bool:
    return bool(metadata and METADATA_FIELDS.intersection(metadata.keys()))


def extract_yaml_artifact_block(text: str) -> dict[str, Any] | None:
    if "\t" in text:
        raise MetadataParseError("YAML document: tabs are forbidden in indentation or content")
    lines = text.splitlines()
    start: int | None = None
    for index, line in enumerate(lines):
        if line.strip() == "artifact:":
            start = index + 1
            break
    if start is None:
        return None
    block: list[str] = []
    for line in lines[start:]:
        if line and not line.startswith((" ", "\t")):
            break
        block.append(line[2:] if line.startswith("  ") else line.lstrip())
    return parse_simple_yaml_mapping(block, context="YAML artifact block")


def extract_json_artifact(text: str) -> dict[str, Any] | None:
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return None
    artifact = data.get("artifact") if isinstance(data, dict) else None
    return artifact if isinstance(artifact, dict) else None


def extract_script_metadata(text: str) -> dict[str, Any] | None:
    lines: list[str] = []
    for raw in text.splitlines()[:40]:
        stripped = raw.strip()
        if stripped.startswith("# artifact_") or stripped.startswith("# constitution_selectors") or stripped.startswith("# validation_profile"):
            lines.append(stripped[2:])
        elif lines and stripped.startswith("#"):
            lines.append(stripped[2:])
        elif lines:
            break
    return parse_simple_yaml_mapping(lines, context="script metadata comment block") if lines else None


def load_sidecar(path: Path) -> dict[str, Any] | None:
    sidecar = path.with_name(path.name + ".artifact.yml")
    if not sidecar.exists():
        return None
    text = sidecar.read_text(encoding="utf-8")
    artifact = extract_yaml_artifact_block(text)
    if artifact is not None:
        significant = [line for line in text.splitlines() if line.strip() and not line.lstrip().startswith("#")]
        if not significant or significant[0] != "artifact:":
            raise MetadataParseError("sidecar: `artifact` must be the first top-level key")
        trailing_top_level = [line for line in significant[1:] if not line.startswith("  ")]
        if trailing_top_level:
            raise MetadataParseError(f"sidecar: unconsumed top-level YAML line: {trailing_top_level[0]!r}")
        return artifact
    return parse_simple_yaml_mapping(text.splitlines(), context="sidecar")


def extract_metadata(path: Path) -> tuple[dict[str, Any] | None, str]:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        sidecar = load_sidecar(path)
        return (sidecar, "sidecar") if sidecar else (None, "none")

    suffix = path.suffix.lower()
    metadata: dict[str, Any] | None = None
    source = "none"
    if suffix == ".md":
        metadata = extract_markdown_frontmatter(text)
        if not is_artifact_metadata_block(metadata):
            metadata = None
        source = "markdown-frontmatter" if metadata is not None else "none"
    elif suffix in {".yml", ".yaml"}:
        metadata = extract_yaml_artifact_block(text)
        source = "yaml-artifact-block" if metadata is not None else "none"
    elif suffix == ".json":
        metadata = extract_json_artifact(text)
        source = "json-artifact-object" if metadata is not None else "none"
    elif suffix in {".sh", ".py"}:
        metadata = extract_script_metadata(text)
        source = "script-comment-block" if metadata is not None else "none"

    if metadata is None:
        sidecar = load_sidecar(path)
        if sidecar is not None:
            return sidecar, "sidecar"
    return metadata, source


def validate_metadata(path: Path, root: Path, require_missing: bool) -> tuple[list[str], list[str]]:
    rel = rel_path(path, root)
    errors: list[str] = []
    warnings: list[str] = []
    try:
        metadata, source = extract_metadata(path)
    except MetadataParseError as exc:
        errors.append(f"{rel}: invalid artifact metadata YAML: {exc}")
        return errors, warnings

    if metadata is None:
        if require_missing and is_candidate_governed_path(rel):
            errors.append(f"{rel}: missing artifact metadata")
        return errors, warnings

    for field in REQUIRED_FIELDS:
        value = metadata.get(field)
        if value in (None, "", []):
            errors.append(f"{rel}: missing required artifact metadata field `{field}`")

    for field in LIST_FIELDS:
        value = metadata.get(field)
        if value in (None, ""):
            continue
        if not isinstance(value, list):
            errors.append(f"{rel}: `{field}` must be a YAML/JSON list")

    status = metadata.get("lifecycle_status")
    if status and status not in VALID_STATUSES:
        errors.append(f"{rel}: lifecycle_status `{status}` is not recognized")

    artifact_type = metadata.get("artifact_type")
    companion_to = metadata.get("companion_to")
    if artifact_type in {"companion-doc", "companion"} and not companion_to:
        errors.append(f"{rel}: companion artifact metadata requires `companion_to`")

    selectors = metadata.get("constitution_selectors")
    profiles = metadata.get("validation_profile")
    if isinstance(selectors, list) and len(selectors) == 0:
        errors.append(f"{rel}: `constitution_selectors` must not be empty")
    if isinstance(profiles, list) and len(profiles) == 0:
        errors.append(f"{rel}: `validation_profile` must not be empty")

    if source == "none":
        warnings.append(f"{rel}: artifact metadata source could not be identified")
    return errors, warnings


def changed_paths(root: Path) -> list[Path]:
    seen: set[str] = set()
    paths: list[Path] = []
    for rel in run_git(["diff", "--name-only", "--diff-filter=ACMRTUXB"]):
        seen.add(rel)
        paths.append(root / rel)
    for rel in run_git(["ls-files", "--others", "--exclude-standard"]):
        if rel not in seen:
            paths.append(root / rel)
    return [path for path in paths if path.exists() and path.is_file()]


def expand_requested_paths(raw_paths: list[str], root: Path) -> tuple[list[Path], list[str]]:
    """Expand explicit directories into governed files and reject empty inputs."""
    seen: set[Path] = set()
    paths: list[Path] = []
    errors: list[str] = []

    for raw in raw_paths:
        requested = Path(raw)
        if not requested.exists():
            errors.append(f"requested path does not exist: {raw}")
            continue

        candidates = [requested] if requested.is_file() else sorted(
            path
            for path in requested.rglob("*")
            if path.is_file() and is_candidate_governed_path(rel_path(path, root))
        )
        if not candidates:
            errors.append(f"requested path contains no governed files: {raw}")
            continue

        for candidate in candidates:
            resolved = candidate.resolve()
            if resolved not in seen:
                seen.add(resolved)
                paths.append(candidate)

    return paths, errors


def run_self_test() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        md_good = root / "good.md"
        md_bad = root / "bad.md"
        yml_good = root / "good.yml"
        yml_bad = root / "bad.yml"
        json_good = root / "good.json"
        json_bad = root / "bad.json"
        companion_bad = root / "companion.md"
        runtime_frontmatter = root / "runtime-skill.md"
        yaml_adversarial: list[Path] = []

        md_good.write_text(
            """---
artifact_id: test.good
artifact_type: constitution
intent: Test complete Markdown metadata.
owner: test
lifecycle_status: candidate
constitution_selectors:
  - framework.artifact-metadata
validation_profile:
  - artifact-metadata
---
# Good
""",
            encoding="utf-8",
        )
        md_bad.write_text("---\nartifact_id: test.bad\n---\n# Bad\n", encoding="utf-8")
        yml_good.write_text(
            """artifact:
  artifact_id: test.yml
  artifact_type: library-data
  intent: Test YAML metadata.
  owner: test
  lifecycle_status: candidate
  constitution_selectors:
    - framework.artifact-metadata
  validation_profile:
    - artifact-metadata
items: []
""",
            encoding="utf-8",
        )
        yml_bad.write_text("artifact:\n  artifact_id: test.bad-yml\n", encoding="utf-8")
        json_good.write_text(
            json.dumps(
                {
                    "artifact": {
                        "artifact_id": "test.json",
                        "artifact_type": "durable-evidence",
                        "intent": "Test JSON metadata.",
                        "owner": "test",
                        "lifecycle_status": "candidate",
                        "constitution_selectors": ["framework.artifact-metadata"],
                        "validation_profile": ["artifact-metadata"],
                    },
                    "data": [],
                }
            ),
            encoding="utf-8",
        )
        json_bad.write_text('{"artifact":{"artifact_id":"test.bad-json"}}', encoding="utf-8")
        companion_bad.write_text(
            """---
artifact_id: test.companion
artifact_type: companion-doc
intent: Test companion metadata.
owner: test
lifecycle_status: candidate
constitution_selectors:
  - framework.artifact-metadata
validation_profile:
  - artifact-metadata
---
# Companion
""",
            encoding="utf-8",
        )
        runtime_frontmatter.write_text(
            """---
metadata:
  surface_kind: generated-native-runtime-package
name: runtime-skill
description: Runtime frontmatter is not artifact metadata.
required_operations:
  - collaboration.spawn_agent
---
# Runtime skill
""",
            encoding="utf-8",
        )

        adversarial_documents = {
            "unterminated-quote.md": """---
artifact_id: "test.unterminated
artifact_type: constitution
---
""",
            "tab-indent.md": """---
artifact_id: test.tab
constitution_selectors:
\t- framework.artifact-metadata
---
""",
            "bad-indent.md": """---
artifact_id: test.indent
constitution_selectors:
   - framework.artifact-metadata
---
""",
            "duplicate-key.md": """---
artifact_id: test.first
artifact_id: test.second
---
""",
            "unconsumed-line.md": """---
artifact_id: test.line
this is not yaml
---
""",
        }
        for name, document in adversarial_documents.items():
            path = root / name
            path.write_text(document, encoding="utf-8")
            yaml_adversarial.append(path)

        expectations = [
            (md_good, 0),
            (md_bad, 6),
            (yml_good, 0),
            (yml_bad, 6),
            (json_good, 0),
            (json_bad, 6),
            (companion_bad, 1),
            (runtime_frontmatter, 0),
        ]
        for path, minimum_errors in expectations:
            errors, warnings = validate_metadata(path, root, require_missing=False)
            if minimum_errors == 0 and (errors or warnings):
                print(f"self-test failed: {path.name} expected pass, got errors={errors} warnings={warnings}", file=sys.stderr)
                return 1
            if minimum_errors > 0 and len(errors) < minimum_errors:
                print(f"self-test failed: {path.name} expected at least {minimum_errors} errors, got {len(errors)}", file=sys.stderr)
                return 1

        for path in yaml_adversarial:
            errors, _ = validate_metadata(path, root, require_missing=False)
            if len(errors) != 1 or "invalid artifact metadata YAML" not in errors[0]:
                print(f"self-test failed: {path.name} did not fail strictly: {errors}", file=sys.stderr)
                return 1

        nested = root / "transmutations" / "nested"
        nested.mkdir(parents=True)
        nested_file = nested / "artifact.md"
        nested_file.write_text(md_good.read_text(encoding="utf-8"), encoding="utf-8")
        expanded, expansion_errors = expand_requested_paths([str(nested)], root)
        if expansion_errors or expanded != [nested_file]:
            print(
                f"self-test failed: directory expansion got paths={expanded} errors={expansion_errors}",
                file=sys.stderr,
            )
            return 1

        expanded, expansion_errors = expand_requested_paths([str(root / "missing")], root)
        if expanded or len(expansion_errors) != 1:
            print("self-test failed: missing requested path did not fail closed", file=sys.stderr)
            return 1

    print("Artifact metadata validator self-test")
    print("metadata fixtures: pass")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Arcanum artifact metadata.")
    parser.add_argument("paths", nargs="*", help="Specific paths to validate.")
    parser.add_argument("--changed", action="store_true", help="Validate changed and untracked files.")
    parser.add_argument("--self-test", action="store_true", help="Run built-in fixtures.")
    parser.add_argument("--require-metadata", action="store_true", help="Fail when governed paths omit metadata.")
    parser.add_argument("--advisory", action="store_true", help="Downgrade validation errors to warnings.")
    args = parser.parse_args()

    if args.self_test:
        return run_self_test()

    root = repo_root()
    input_errors: list[str] = []
    if args.changed:
        paths = changed_paths(root)
    elif args.paths:
        paths, input_errors = expand_requested_paths(args.paths, root)
    else:
        paths = []

    errors: list[str] = list(input_errors)
    warnings: list[str] = []
    checked = 0
    for path in paths:
        rel = rel_path(path, root)
        if is_generated_or_runtime(rel):
            continue
        checked += 1
        item_errors, item_warnings = validate_metadata(path, root, require_missing=args.require_metadata)
        errors.extend(item_errors)
        warnings.extend(item_warnings)

    if args.advisory and errors:
        warnings.extend(errors)
        errors = []

    print("Artifact metadata validation")
    print(f"checked: {checked}")
    if warnings:
        print("\nwarnings:")
        for warning in warnings:
            print(f"- {warning}")
    if errors:
        print("\nfailures:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("\nresult: pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
