#!/usr/bin/env python3
"""Validate evidence-grounded-diagrams package closure and canonical schemas."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "README.md",
    "SKILL.md",
    "requirements.txt",
    "agents/openai.yaml",
    "references/claim-model.md",
    "references/runbooks.md",
    "references/artifact-lifecycle.md",
    "references/schema-guide.md",
    "schemas/diagram-request.schema.yml",
    "schemas/diagram-semantic-model.schema.yml",
    "schemas/diagram-bundle-manifest.schema.yml",
    "schemas/diagram-commit-marker.schema.yml",
    "schemas/diagram-review-receipt.schema.yml",
    "schemas/diagram-manual-attestation.schema.yml",
    "schemas/usage-event.schema.yml",
    "schemas/diagram-validation-receipt.schema.yml",
    "templates/diagram-request.yml",
    "templates/diagram.request.yml",
    "templates/diagram.model.yml",
    "templates/diagram.meta.yml",
    "templates/review.receipt.yml",
    "templates/manual-attestation.yml",
    "templates/textual-equivalent.md",
    "templates/validation.receipt.yml",
    "templates/usage-event.json",
    "scripts/persist_diagram_bundle.py",
    "scripts/preflight_runtime.py",
    "scripts/validate_review_receipt.py",
    "scripts/validate_diagram_bundle.py",
    "scripts/list_diagram_bundles.py",
    "scripts/record_usage_event.py",
    "scripts/detect_renderer_capabilities.py",
]


def load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def main() -> int:
    errors: list[str] = []
    for relative in REQUIRED:
        if not (ROOT / relative).is_file():
            errors.append(f"missing required package file: {relative}")

    skill = ROOT / "SKILL.md"
    text = skill.read_text(encoding="utf-8") if skill.is_file() else ""
    tick = chr(96)
    pattern = tick + r"((?:references|schemas|templates|scripts)/[^" + tick + r"]+)" + tick
    for relative in sorted(set(re.findall(pattern, text))):
        if not (ROOT / relative).is_file():
            errors.append(f"SKILL.md references missing resource: {relative}")

    if list(ROOT.rglob("*.schema.json")):
        errors.append("new canonical schemas must not use .schema.json")
    for schema_path in sorted((ROOT / "schemas").glob("*.schema.yml")):
        try:
            schema = load_yaml(schema_path)
            if not isinstance(schema, dict):
                raise TypeError("top level is not a mapping")
            Draft202012Validator.check_schema(schema)
        except Exception as exc:
            errors.append(f"invalid schema {schema_path.name}: {exc}")

    template_pairs = [
        ("templates/diagram-request.yml", "schemas/diagram-request.schema.yml"),
        ("templates/diagram.request.yml", "schemas/diagram-request.schema.yml"),
        ("templates/diagram.model.yml", "schemas/diagram-semantic-model.schema.yml"),
        ("templates/diagram.meta.yml", "schemas/diagram-bundle-manifest.schema.yml"),
        ("templates/review.receipt.yml", "schemas/diagram-review-receipt.schema.yml"),
        ("templates/manual-attestation.yml", "schemas/diagram-manual-attestation.schema.yml"),
        ("templates/validation.receipt.yml", "schemas/diagram-validation-receipt.schema.yml"),
    ]
    for template_name, schema_name in template_pairs:
        try:
            instance = load_yaml(ROOT / template_name)
            schema = load_yaml(ROOT / schema_name)
            validation_errors = list(Draft202012Validator(schema).iter_errors(instance))
            for error in validation_errors:
                locator = ".".join(str(item) for item in error.absolute_path) or "<root>"
                errors.append(f"{template_name}:{locator}: {error.message}")
        except Exception as exc:
            errors.append(f"cannot validate {template_name}: {exc}")

    try:
        json.loads((ROOT / "templates/usage-event.json").read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        errors.append(f"invalid templates/usage-event.json: {exc}")

    try:
        agent = load_yaml(ROOT / "agents/openai.yaml")
        prompt = agent["interface"]["default_prompt"]
        if "$evidence-grounded-diagrams" not in prompt:
            errors.append("agents/openai.yaml default_prompt must mention the skill")
    except (OSError, UnicodeError, yaml.YAMLError, KeyError, TypeError) as exc:
        errors.append(f"invalid agents/openai.yaml: {exc}")

    requirement_lines = {
        line.strip()
        for line in (ROOT / "requirements.txt").read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }
    if not any(line.startswith("PyYAML") for line in requirement_lines):
        errors.append("requirements.txt must declare PyYAML")
    if not any(line.startswith("jsonschema") for line in requirement_lines):
        errors.append("requirements.txt must declare jsonschema")

    try:
        event = __import__("json").loads(
            (ROOT / "templates/usage-event.json").read_text(encoding="utf-8")
        )
        schema = load_yaml(ROOT / "schemas/usage-event.schema.yml")
        for error in Draft202012Validator(schema).iter_errors(event):
            locator = ".".join(str(item) for item in error.absolute_path) or "<root>"
            errors.append(f"templates/usage-event.json:{locator}: {error.message}")
    except Exception as exc:
        errors.append(f"cannot validate templates/usage-event.json: {exc}")

    if errors:
        print("SKILL_PACKAGE_VALIDATION=block")
        for error in errors:
            print(f"BLOCK: {error}")
        return 1
    print("SKILL_PACKAGE_VALIDATION=pass")
    print(f"PACKAGE={ROOT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
