#!/usr/bin/env python3
"""Compile a schema-valid governance-flow source into one normalized graph."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_ROOT = PACKAGE_ROOT / "schemas"
SOURCE_SCHEMA = SCHEMA_ROOT / "governance-flow-source-v1.schema.yml"
GRAPH_SCHEMA = SCHEMA_ROOT / "governance-flow-graph-v1.schema.yml"

METRIC_CONTRACTS = {
    "postacceptance_consumer_defects": ("governance_flow.consumer_defect.v1", 0),
    "prompts_per_immutable_graph": ("governance_flow.owner_prompt.v1", 1),
    "unchanged_byte_approval_retries": ("governance_flow.request_retry.v1", 0),
    "blockers_discovered_after_request": ("governance_flow.late_blocker.v1", 0),
    "manual_receipt_transfers": ("governance_flow.receipt_transfer.v1", 0),
}


class GovernanceFlowError(ValueError):
    """A deterministic contract violation."""


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def digest_document(value: Any, *, omit: str | None = None) -> str:
    candidate = copy.deepcopy(value)
    if omit is not None:
        candidate.pop(omit, None)
    return sha256_bytes(canonical_bytes(candidate))


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise GovernanceFlowError(f"{path}: expected a mapping")
    return value


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise GovernanceFlowError(f"{path}: expected an object")
    return value


def validate_with_schema(value: Any, schema_path: Path) -> None:
    schema = load_yaml(schema_path)
    errors = sorted(
        Draft202012Validator(schema).iter_errors(value),
        key=lambda error: (list(error.absolute_path), error.message),
    )
    if errors:
        rendered = []
        for error in errors:
            location = "/".join(str(part) for part in error.absolute_path) or "<root>"
            rendered.append(f"{location}: {error.message}")
        raise GovernanceFlowError("schema validation failed: " + "; ".join(rendered))


def _assert_unique(values: list[str], label: str) -> None:
    if len(values) != len(set(values)):
        raise GovernanceFlowError(f"{label} must be unique")


def _assert_acyclic(consumers: list[dict[str, Any]]) -> None:
    dependencies = {
        item["consumer_id"]: set(item["depends_on"]) for item in consumers
    }
    known = set(dependencies)
    for consumer_id, depends_on in dependencies.items():
        unknown = sorted(depends_on - known)
        if unknown:
            raise GovernanceFlowError(
                f"consumer {consumer_id} has unknown dependencies: {', '.join(unknown)}"
            )

    pending = {key: set(value) for key, value in dependencies.items()}
    resolved: set[str] = set()
    while pending:
        ready = sorted(key for key, value in pending.items() if value <= resolved)
        if not ready:
            raise GovernanceFlowError("consumer dependency graph contains a cycle")
        for key in ready:
            resolved.add(key)
            del pending[key]


def validate_source_semantics(source: dict[str, Any]) -> None:
    target_paths = [item["path"] for item in source["targets"]]
    _assert_unique(target_paths, "target paths")
    if sorted(target_paths) != sorted(source["authority"]["write_paths"]):
        raise GovernanceFlowError("target paths must equal the declared write ceiling")

    expected = source["terminal_outcome"]["expected_postimages"]
    target_postimages = {
        item["path"]: item["postimage_sha256"] for item in source["targets"]
    }
    if expected != target_postimages:
        raise GovernanceFlowError("terminal expected postimages must equal target postimages")

    owner = source["owner"]["owner_id"]
    reviewer = source["independent_review"]["reviewer_id"]
    if owner == reviewer:
        raise GovernanceFlowError("independent reviewer must differ from owner")

    consumer_ids = [item["consumer_id"] for item in source["consumers"]]
    _assert_unique(consumer_ids, "consumer identifiers")
    _assert_acyclic(source["consumers"])

    retries = {item["classification"]: item for item in source["retry_policy"]}
    if set(retries) != {
        "environmental",
        "mechanical_evidence_only",
        "semantic_or_authority",
    }:
        raise GovernanceFlowError("retry policy must define each classification exactly once")
    if retries["semantic_or_authority"]["owner_prompt"] != "new_graph_only":
        raise GovernanceFlowError("semantic or authority changes require a new graph request")
    if any(
        retries[name]["owner_prompt"] != "none"
        for name in ("environmental", "mechanical_evidence_only")
    ):
        raise GovernanceFlowError("nonsemantic retries cannot request owner approval")

    metrics = {
        item["metric_id"]: (item["event"], item["target"])
        for item in source["metrics"]
    }
    if metrics != METRIC_CONTRACTS:
        raise GovernanceFlowError("metric event contracts or targets do not match v1")

    terminal = source["terminal_outcome"]
    prohibited = set(terminal["prohibited_effects"])
    if not {"external_call", "successor_execution"} <= prohibited:
        raise GovernanceFlowError(
            "terminal contract must prohibit external calls and successor execution"
        )


def validate_source(source: dict[str, Any]) -> None:
    validate_with_schema(source, SOURCE_SCHEMA)
    validate_source_semantics(source)


def normalize_source(source: dict[str, Any]) -> dict[str, Any]:
    envelope = copy.deepcopy(
        {
            key: source[key]
            for key in (
                "owner",
                "targets",
                "authority",
                "risk",
                "executable",
                "independent_review",
                "consumers",
                "protected_inputs",
                "request_budget",
                "terminal_outcome",
                "retry_policy",
                "sidecar_resume",
                "metrics",
            )
        }
    )
    envelope["targets"] = sorted(envelope["targets"], key=lambda item: item["path"])
    envelope["authority"]["write_paths"] = sorted(
        envelope["authority"]["write_paths"]
    )
    envelope["risk"]["reasons"] = sorted(envelope["risk"]["reasons"])
    envelope["executable"]["environment_allowlist"] = sorted(
        envelope["executable"]["environment_allowlist"]
    )
    envelope["consumers"] = sorted(
        envelope["consumers"], key=lambda item: item["consumer_id"]
    )
    for consumer in envelope["consumers"]:
        consumer["depends_on"] = sorted(consumer["depends_on"])
    envelope["protected_inputs"] = sorted(envelope["protected_inputs"])
    envelope["terminal_outcome"]["required_effects"] = sorted(
        envelope["terminal_outcome"]["required_effects"]
    )
    envelope["terminal_outcome"]["prohibited_effects"] = sorted(
        envelope["terminal_outcome"]["prohibited_effects"]
    )
    retry_order = {
        "environmental": 0,
        "mechanical_evidence_only": 1,
        "semantic_or_authority": 2,
    }
    envelope["retry_policy"] = sorted(
        envelope["retry_policy"], key=lambda item: retry_order[item["classification"]]
    )
    envelope["sidecar_resume"]["unchanged_fields"] = sorted(
        envelope["sidecar_resume"]["unchanged_fields"]
    )
    envelope["metrics"] = sorted(
        envelope["metrics"], key=lambda item: item["metric_id"]
    )
    return envelope


def compile_source(source: dict[str, Any], source_bytes: bytes) -> dict[str, Any]:
    validate_source(source)
    graph: dict[str, Any] = {
        "schema_version": "arcanum.governance-flow.graph.v1",
        "flow_id": source["flow_id"],
        "source_digest": sha256_bytes(source_bytes),
        "digest_algorithm": "sha256-canonical-json-without-self-digest",
        "authority_effect": "none",
        "decision_envelope": normalize_source(source),
        "derived_permissions": {
            "selection": False,
            "admission": False,
            "execution": False,
            "publication": False,
            "git": False,
            "deployment": False,
            "credentials": False,
            "destructive_actions": False,
            "external_effects": False,
            "successor_execution": False,
        },
    }
    graph["decision_graph_digest"] = digest_document(graph)
    validate_with_schema(graph, GRAPH_SCHEMA)
    return graph


def compile_path(source_path: Path) -> dict[str, Any]:
    source_bytes = source_path.read_bytes()
    source = json.loads(source_bytes.decode("utf-8"))
    if not isinstance(source, dict):
        raise GovernanceFlowError("machine source must be a JSON object")
    return compile_source(source, source_bytes)


def verify_graph(graph: dict[str, Any]) -> None:
    validate_with_schema(graph, GRAPH_SCHEMA)
    expected = digest_document(graph, omit="decision_graph_digest")
    if graph["decision_graph_digest"] != expected:
        raise GovernanceFlowError("decision graph digest is stale or invalid")
    reconstructed_source = {
        "schema_version": "arcanum.governance-flow.source.v1",
        "flow_id": graph["flow_id"],
        **copy.deepcopy(graph["decision_envelope"]),
    }
    validate_source(reconstructed_source)
    if normalize_source(reconstructed_source) != graph["decision_envelope"]:
        raise GovernanceFlowError("decision graph envelope is not fully normalized")


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    graph = compile_path(args.source)
    rendered = json.dumps(graph, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if args.check:
        if not args.output.is_file() or args.output.read_text(encoding="utf-8") != rendered:
            raise GovernanceFlowError("compiled graph differs from the expected bytes")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
