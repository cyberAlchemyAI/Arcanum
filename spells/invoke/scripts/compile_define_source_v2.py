#!/usr/bin/env python3
"""Compile one Define v2 source into an atomic candidate definitions bundle."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable

from jsonschema import Draft202012Validator, RefResolver


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from validate_definitions_artifact import (  # noqa: E402
    render_definitions_markdown,
    render_glossary_markdown,
    validate_artifact,
)


IDENTITY = "invoke.compile-define-source.v2"
PROFILE = "invoke.generic-definitions-baseline.v2"
KINDS = {
    "spec": "spec",
    "definitions": "definitions",
    "definitions_view": "definitions-view",
    "glossary": "glossary",
    "layering": "layering",
    "template_selection": "template-selection",
    "dispatch_trace": "dispatch-trace",
    "distill": "distill",
    "identity_denominator": "identity-denominator",
    "transport": "transport",
}


def canonical_digest(value: Any, omit: str | None = None) -> str:
    projection = copy.deepcopy(value)
    if omit:
        projection.pop(omit, None)
    encoded = json.dumps(
        projection,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def exact_ref(path: Path, label: str | None = None) -> dict[str, Any]:
    data = path.read_bytes()
    return {
        "path": label or path.as_posix(),
        "sha256": hashlib.sha256(data).hexdigest(),
        "size": len(data),
    }


def verify_ref(repo: Path, ref: dict[str, Any], label: str) -> None:
    path = (repo / ref["path"]).resolve()
    try:
        path.relative_to(repo.resolve())
    except ValueError as error:
        raise ValueError(f"{label} escapes repository") from error
    if not path.is_file():
        raise ValueError(f"{label} missing")
    if exact_ref(path, ref["path"]) != ref:
        raise ValueError(f"{label} exact ref is stale")


def schema_errors(
    document: Any,
    schema: dict[str, Any],
    store: dict[str, Any] | None = None,
) -> list[str]:
    resolver = RefResolver.from_schema(schema, store=store or {})
    return [
        f"{'/'.join(map(str, error.absolute_path)) or '<root>'}: {error.message}"
        for error in sorted(
            Draft202012Validator(schema, resolver=resolver).iter_errors(document),
            key=lambda item: list(item.absolute_path),
        )
    ]


def build_definitions_artifact(source: dict[str, Any], definitions_schema: dict[str, Any]) -> dict[str, Any]:
    registry = source["definition_registry"]
    return {
        "$schema": definitions_schema["$id"],
        "schema_version": "definitions/v1",
        "registry_id": registry["registry_id"],
        "title": registry["title"],
        "registry_status": "candidate",
        "owner_route": registry["owner_route"],
        "authority_kind": "kind.definition",
        "authority_scope": copy.deepcopy(registry["authority_scope"]),
        "visibility": registry["visibility"],
        "authority_effect": "none",
        "definitions": copy.deepcopy(registry["definitions"]),
    }


def compile_source(
    source_path: Path,
    output_dir: Path,
    repo_root: Path,
    schema_dir: Path,
    late_validator: Callable[[Path], None] | None = None,
) -> dict[str, Any]:
    if output_dir.exists():
        raise ValueError("output directory must be absent")
    source = json.loads(source_path.read_text(encoding="utf-8"))
    source_schema = json.loads((schema_dir / "define-source-v2.schema.json").read_text(encoding="utf-8"))
    result_schema = json.loads((schema_dir / "define-result-v2.schema.json").read_text(encoding="utf-8"))
    definitions_schema = json.loads((schema_dir / "definitions.schema.json").read_text(encoding="utf-8"))
    definitions_ref_uri = "https://arcanum.dev/schemas/invoke/definitions.schema.json"
    errors = schema_errors(
        source,
        source_schema,
        {
            definitions_schema["$id"]: definitions_schema,
            definitions_ref_uri: definitions_schema,
            "definitions.schema.json": definitions_schema,
        },
    )
    if errors:
        raise ValueError("source schema invalid: " + "; ".join(errors))
    if source["discovery"]["kind"] == "artifact":
        verify_ref(repo_root, source["discovery"]["ref"], "discovery")
    if source["template_selection"]["selected"] not in source["template_selection"]["eligible"]:
        raise ValueError("selected profile is not eligible")
    expected_layer = (
        "IMPLEMENTATION-LAYERING.md"
        if source["layering"]["kind"] == "seed"
        else "LAYERING-GAP.md"
    )
    if source["output_contracts"]["layering"] != expected_layer:
        raise ValueError("layering output contract mismatch")
    if source["identity_denominator"]["classification"] == "required":
        verify_ref(repo_root, source["identity_denominator"]["request_ref"], "identity request")
        verify_ref(repo_root, source["identity_denominator"]["result_ref"], "identity result")
        result = json.loads(
            (repo_root / source["identity_denominator"]["result_ref"]["path"]).read_text(encoding="utf-8")
        )
        if result.get("verdict") != "pass":
            raise ValueError("identity denominator result is not pass")

    artifact = build_definitions_artifact(source, definitions_schema)
    artifact_errors = validate_artifact(artifact, repo_root, definitions_schema)
    if artifact_errors:
        raise ValueError("definitions artifact invalid: " + "; ".join(artifact_errors))

    stage = Path(tempfile.mkdtemp(prefix=f".{output_dir.name}.", dir=output_dir.parent))
    try:
        declarations = "\n\n".join(
            f"## {item['title']}\n\n{item['statement']}"
            for item in source["spec_declarations"]
        )
        (stage / "SPEC.md").write_text(
            f"# {source['target']['id']}\n\n{source['target']['objective']}\n\n{declarations}\n",
            encoding="utf-8",
        )
        (stage / "DEFINITIONS.json").write_text(
            json.dumps(artifact, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        (stage / "DEFINITIONS.md").write_text(
            render_definitions_markdown(artifact),
            encoding="utf-8",
        )
        (stage / "GLOSSARY.md").write_text(
            render_glossary_markdown(artifact),
            encoding="utf-8",
        )
        if source["layering"]["kind"] == "seed":
            layering_text = (
                "# Implementation Layering Seed\n\n"
                f"- Decision: {source['layering']['decision']}\n"
                f"- Minimum unit: {source['layering']['minimum_unit']}\n"
            )
        else:
            layering_text = f"# Implementation Layering Gap\n\n{source['layering']['rationale']}\n"
        (stage / expected_layer).write_text(layering_text, encoding="utf-8")
        documents = {
            "TEMPLATE-SELECTION-RECEIPT.json": {
                "schema_version": "invoke.define-template-selection.v2",
                **source["template_selection"],
                "result": "pass",
            },
            "DISPATCH-TRACE.json": {
                "schema_version": "invoke.define-dispatch-trace.v2",
                **source["dispatch_trace"],
                "result": "pass",
            },
            "DISTILL-RECEIPT.json": {
                "schema_version": "invoke.define-distill-classification.v2",
                **source["distill"],
                "result": "pass",
            },
            "IDENTITY-DENOMINATOR-RECEIPT.json": {
                "schema_version": "invoke.define-identity-classification.v2",
                **source["identity_denominator"],
                "result": "pass",
            },
            "DEFINE-TRANSPORT-REPORT.json": {
                "schema_version": "invoke.define-transport.v2",
                "policy": source["transport_policy"],
                "result": "no-op",
                "authority_effect": "none",
            },
        }
        for name, document in documents.items():
            (stage / name).write_text(
                json.dumps(document, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )

        staged_artifact = json.loads((stage / "DEFINITIONS.json").read_text(encoding="utf-8"))
        staged_errors = validate_artifact(staged_artifact, repo_root, definitions_schema, stage)
        if staged_errors:
            raise ValueError("staged definitions invalid: " + "; ".join(staged_errors))
        if late_validator:
            late_validator(stage)
        staged_artifact = json.loads((stage / "DEFINITIONS.json").read_text(encoding="utf-8"))
        staged_errors = validate_artifact(staged_artifact, repo_root, definitions_schema, stage)
        if staged_errors:
            raise ValueError("late definitions validation failed: " + "; ".join(staged_errors))

        contracts = source["output_contracts"]
        outputs = [
            {"kind": kind, **exact_ref(stage / contracts[key], contracts[key])}
            for key, kind in KINDS.items()
        ]
        script = Path(__file__).resolve()
        receipt = {
            "schema_version": "invoke.define-stage-receipt.v2",
            "receipt_id": f"define-v2:{source['source_id']}:{canonical_digest(source)[:16]}",
            "owner_capability": "invoke",
            "mode": "define",
            "producer": {
                "identity": IDENTITY,
                "path": "arcanum/spells/invoke/scripts/compile_define_source_v2.py",
                "sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
            },
            "profile_id": PROFILE,
            "source_ref": exact_ref(
                source_path,
                source_path.relative_to(repo_root).as_posix(),
            ),
            "outputs": outputs,
            "result": "pass",
            "next_route": source["next_route"],
            "authority_effect": "none",
            "receipt_digest": "0" * 64,
        }
        receipt["receipt_digest"] = canonical_digest(receipt, "receipt_digest")
        receipt_errors = schema_errors(receipt, result_schema)
        if receipt_errors:
            raise ValueError("result schema invalid: " + "; ".join(receipt_errors))
        (stage / contracts["stage_receipt"]).write_text(
            json.dumps(receipt, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        os.replace(stage, output_dir)
        return receipt
    except Exception:
        shutil.rmtree(stage, ignore_errors=True)
        raise


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--repo-root", default=".", type=Path)
    parser.add_argument("--schema-dir", type=Path)
    args = parser.parse_args()
    root = args.repo_root.resolve()
    schemas = args.schema_dir or root / "arcanum/spells/invoke/schemas"
    try:
        receipt = compile_source(
            args.source.resolve(),
            args.output_dir.resolve(),
            root,
            schemas.resolve(),
        )
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"BLOCK: {error}")
        return 2
    print(json.dumps(receipt, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
