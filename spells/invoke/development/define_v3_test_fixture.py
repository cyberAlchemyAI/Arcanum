"""Shared real-repository fixture for Define v3 compiler and replay tests."""

from __future__ import annotations

import copy
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

from test_validate_define_semantic_closure import (  # reuse the W1 repository substrate
    RepositoryFixture,
    canonical_bytes,
)


INVOKE_DIR = Path(__file__).resolve().parents[1]
COMPILER = INVOKE_DIR / "scripts" / "compile_define_source_v3.py"
VALIDATOR = INVOKE_DIR / "scripts" / "validate_define_semantic_closure.py"
CANONICAL_SCHEMA_DIR = INVOKE_DIR / "schemas"
POSITIVE_FAMILY = (
    INVOKE_DIR
    / "development"
    / "define-v3-semantic-closure"
    / "fixtures"
    / "schema-family"
    / "positive-family.json"
)
SCHEMA_FILES = (
    "define-semantic-context-v1.schema.json",
    "define-semantic-closure-receipt-v1.schema.json",
    "define-semantic-context-v2.schema.json",
    "define-semantic-closure-receipt-v2.schema.json",
    "define-bundle-admission-receipt-v2.schema.json",
    "define-source-v3.schema.json",
    "define-profile-v3.schema.json",
    "definitions.schema.json",
    "definitions-v2.schema.json",
    "define-result-v3.schema.json",
)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_bytes(value))


class DefineV3RepositoryFixture(RepositoryFixture):
    """Build exact context, closure, schemas, source, and canonical fixtures."""

    def __init__(self, root: Path, mode: str = "mixed") -> None:
        super().__init__(root)
        self.schema_dir = root / "arcanum/spells/invoke/schemas"
        self.script_dir = root / "arcanum/spells/invoke/scripts"
        self.schema_dir.mkdir(parents=True, exist_ok=True)
        self.script_dir.mkdir(parents=True, exist_ok=True)
        for filename in SCHEMA_FILES:
            (self.schema_dir / filename).write_bytes((CANONICAL_SCHEMA_DIR / filename).read_bytes())
        (self.script_dir / VALIDATOR.name).write_bytes(VALIDATOR.read_bytes())
        (self.script_dir / COMPILER.name).write_bytes(COMPILER.read_bytes())
        self.closure_path = root / "public/DEFINE-SEMANTIC-CLOSURE-RECEIPT.json"
        self.source_path = root / "public/DEFINE-SOURCE-v3.json"
        self.output_dir = root / "define-v3-output"
        self.mode = mode
        self.configure_mode(mode)

    def configure_mode(self, mode: str) -> None:
        if mode not in {"mixed", "reference-only", "candidate-only"}:
            raise ValueError(f"unsupported fixture mode: {mode}")
        if mode == "reference-only":
            self.context["concept_probes"] = [self.context["concept_probes"][0]]
        elif mode == "candidate-only":
            self.context["concept_probes"] = [self.context["concept_probes"][1]]
        self.write_context()
        self.closure_path.unlink(missing_ok=True)
        result = self.run("public/DEFINE-SEMANTIC-CLOSURE-RECEIPT.json")
        if result.returncode != 0:
            raise AssertionError(f"fixture closure failed: {result.stderr}")
        self.closure = json.loads(self.closure_path.read_text(encoding="utf-8"))
        self.source = self._source(mode)
        self.write_source()

    def upgrade_define_to_v2(self) -> None:
        """Rebind the fixture source to a passing v2 semantic closure."""

        self.upgrade_to_v2()
        self.closure_path.unlink(missing_ok=True)
        result = self.run("public/DEFINE-SEMANTIC-CLOSURE-RECEIPT.json")
        if result.returncode != 0:
            raise AssertionError(f"fixture v2 closure failed: {result.stderr}")
        self.closure = json.loads(self.closure_path.read_text(encoding="utf-8"))
        self.source = self._source(self.mode)
        self.write_source()

    def add_v2_relationship_obligation(self) -> None:
        """Require the existing FIX-D2 depends-on FIX-D1 relation."""

        if self.context.get("schema_version") != "invoke.define-semantic-context.v2":
            raise AssertionError("relationship obligation requires a v2 fixture")
        obligation_id = "obligation:feature-contract-depends-on-semantic-closure"
        probe_ids = ["probe:specialize-contract", "probe:new-semantic-closure"]
        self.context["intent_coverage"]["obligations"].append(
            {
                "obligation_id": obligation_id,
                "kind": "relationship",
                "statement": "Feature contract depends on semantic closure.",
                "status": "covered",
                "evidence_source_ids": ["intent-source:fixture-discovery"],
                "probe_ids": probe_ids,
                "relationship": {
                    "subject_probe_id": probe_ids[0],
                    "type": "depends-on",
                    "object_probe_id": probe_ids[1],
                },
                "boundary": None,
                "rationale": "The fixture requires this explicit dependency.",
            }
        )
        for probe in self.context["concept_probes"]:
            if probe["probe_id"] in probe_ids:
                probe["obligation_ids"].append(obligation_id)
        facet = next(
            item
            for item in self.context["intent_coverage"]["facets"]
            if item["facet_id"] == "relationships"
        )
        facet["status"] = "represented"
        facet["obligation_ids"] = [obligation_id]
        self.write_context()
        self.closure_path.unlink(missing_ok=True)
        result = self.run("public/DEFINE-SEMANTIC-CLOSURE-RECEIPT.json")
        if result.returncode != 0:
            raise AssertionError(f"fixture v2 relationship closure failed: {result.stderr}")
        self.closure = json.loads(self.closure_path.read_text(encoding="utf-8"))
        self.source = self._source(self.mode)
        self.write_source()

    def exact_ref(self, path: Path) -> dict[str, Any]:
        data = path.read_bytes()
        return {
            "path": path.relative_to(self.root).as_posix(),
            "sha256": hashlib.sha256(data).hexdigest(),
            "size": len(data),
        }

    @staticmethod
    def definition_ref(probe_ref: dict[str, Any]) -> dict[str, Any]:
        return {
            "role": "evidence",
            "path": probe_ref["path"],
            "visibility": probe_ref["visibility"],
            "selector_type": probe_ref["selector_type"],
            "selector": probe_ref["selector"],
            "start_line": None,
            "end_line": None,
            "sha256": probe_ref["sha256"],
            "size": probe_ref["size"],
        }

    @staticmethod
    def authority_ref(match_ref: dict[str, Any]) -> dict[str, Any]:
        return {
            "path": match_ref["path"],
            "sha256": match_ref["sha256"],
            "size": match_ref["size"],
            "selector": match_ref["selector"],
            "visibility": match_ref["visibility"],
        }

    def _source(self, mode: str) -> dict[str, Any]:
        family = json.loads(POSITIVE_FAMILY.read_text(encoding="utf-8"))
        source = copy.deepcopy(family["define_source"])
        source["source_id"] = f"fixture:define-v3:{mode}"
        source["upstream_bindings"] = {
            "semantic_context_ref": self.exact_ref(self.context_path),
            "semantic_closure_receipt_ref": self.exact_ref(self.closure_path),
        }
        registry = source["definition_registry"]
        registry["authority_scope"] = copy.deepcopy(self.context["target"]["authority_scope"])
        registry["visibility"] = self.context["target"]["visibility"]
        registry["owner_route"] = self.closure["authority_resolution"]["owner"]

        candidates = {item["id"]: item for item in registry["definitions"]}
        new_candidate = candidates["FIX-D1"]
        specialized_candidate = candidates["FIX-D2"]
        probes = {item["probe_id"]: item for item in self.context["concept_probes"]}
        results = {item["probe_id"]: item for item in self.closure["probe_results"]}

        if "probe:new-semantic-closure" in probes:
            probe = probes["probe:new-semantic-closure"]
            new_candidate["term"] = probe["term"]
            new_candidate["aliases"] = copy.deepcopy(probe["aliases"])
            new_candidate["source_refs"] = [self.definition_ref(item) for item in probe["evidence_refs"]]
        if "probe:specialize-contract" in probes:
            probe = probes["probe:specialize-contract"]
            specialized_candidate["term"] = probe["term"]
            specialized_candidate["aliases"] = copy.deepcopy(probe["aliases"])
            specialized_candidate["source_refs"] = [self.definition_ref(item) for item in probe["evidence_refs"]]

        definitions: list[dict[str, Any]] = []
        bindings: list[dict[str, Any]] = []
        applications: list[dict[str, Any]] = []
        for probe in self.context["concept_probes"]:
            probe_id = probe["probe_id"]
            result = results[probe_id]
            if result["disposition"] == "reuse-existing":
                match = result["matches"][0]
                binding = {
                    "binding_id": "binding:contract-reuse",
                    "probe_id": probe_id,
                    "role": "reuse",
                    "definition_id": match["definition_id"],
                    "term": match["term"],
                    "authority_scope": copy.deepcopy(match["authority_scope"]),
                    "authority_status": "active",
                    "authority_ref": self.authority_ref(match["source_ref"]),
                }
                bindings.append(binding)
                definition_ids: list[str] = []
                binding_ids = [binding["binding_id"]]
            elif result["disposition"] == "new-scoped-term":
                definitions.append(new_candidate)
                definition_ids = [new_candidate["id"]]
                binding_ids = []
            else:
                match = result["matches"][0]
                binding = {
                    "binding_id": "binding:contract-specialization",
                    "probe_id": probe_id,
                    "role": "specialization-basis",
                    "definition_id": match["definition_id"],
                    "term": match["term"],
                    "authority_scope": copy.deepcopy(match["authority_scope"]),
                    "authority_status": "active",
                    "authority_ref": self.authority_ref(match["source_ref"]),
                }
                bindings.append(binding)
                definitions.append(specialized_candidate)
                definition_ids = [specialized_candidate["id"]]
                binding_ids = [binding["binding_id"]]
            applications.append(
                {
                    "probe_id": probe_id,
                    "disposition": result["disposition"],
                    "definition_ids": definition_ids,
                    "authority_binding_ids": binding_ids,
                    "rationale": result["rationale"],
                }
            )
        # The fixture relation is useful only when both local candidates exist.
        if not {"FIX-D1", "FIX-D2"}.issubset({item["id"] for item in definitions}):
            specialized_candidate["relations"] = []
        registry["definitions"] = definitions
        registry["authority_bindings"] = bindings
        source["semantic_applications"] = applications
        return source

    def write_source(self) -> None:
        write_json(self.source_path, self.source)

    def refresh_source_ref(self, path: Path) -> None:
        relative = path.relative_to(self.root).as_posix()
        current = self.exact_ref(path)

        def visit(value: Any) -> None:
            if isinstance(value, dict):
                if value.get("path") == relative and "sha256" in value and "size" in value:
                    value["sha256"] = current["sha256"]
                    value["size"] = current["size"]
                for child in value.values():
                    visit(child)
            elif isinstance(value, list):
                for child in value:
                    visit(child)

        visit(self.source)
        self.write_source()

    def compiler_command(self, output_dir: Path | None = None) -> list[str]:
        command = [
            sys.executable,
            str(COMPILER),
            str(self.source_path),
            "--output-dir",
            str(output_dir or self.output_dir),
            "--repo-root",
            str(self.root),
            "--schema-dir",
            str(self.schema_dir),
            "--discovery-root",
            "public",
            "--public-root",
            "public",
        ]
        return command

    def compile(self, output_dir: Path | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            self.compiler_command(output_dir),
            text=True,
            capture_output=True,
            check=False,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
