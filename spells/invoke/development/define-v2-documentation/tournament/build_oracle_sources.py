#!/usr/bin/env python3
"""Materialize satisfiable oracle sources and fixed trial manifests."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[5]
ORACLE = ROOT / "oracle"
GOLDENS = ORACLE / "golden-sources"
RUNS = ROOT / "runs"
COMPILER = REPO / "arcanum/spells/invoke/scripts/compile_define_source_v2.py"


def exact_ref(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    return {
        "path": path.relative_to(REPO).as_posix(),
        "sha256": hashlib.sha256(data).hexdigest(),
        "size": len(data),
    }


def source_ref(path: Path, role: str, selector_type: str, selector: str) -> dict[str, object]:
    ref = exact_ref(path)
    return {
        "role": role,
        "path": ref["path"],
        "visibility": "public",
        "selector_type": selector_type,
        "selector": selector,
        "start_line": None,
        "end_line": None,
        "sha256": ref["sha256"],
        "size": ref["size"],
    }


def output_contract(layering: str) -> dict[str, str]:
    return {
        "spec": "SPEC.md",
        "definitions": "DEFINITIONS.json",
        "definitions_view": "DEFINITIONS.md",
        "glossary": "GLOSSARY.md",
        "layering": layering,
        "template_selection": "TEMPLATE-SELECTION-RECEIPT.json",
        "dispatch_trace": "DISPATCH-TRACE.json",
        "distill": "DISTILL-RECEIPT.json",
        "identity_denominator": "IDENTITY-DENOMINATOR-RECEIPT.json",
        "transport": "DEFINE-TRANSPORT-REPORT.json",
        "stage_receipt": "INVOKE-DEFINE-STAGE-RECEIPT.json",
    }


def common(
    source_id: str,
    target_id: str,
    objective: str,
    discovery: Path,
    declaration: dict[str, str],
    registry: dict[str, Any],
    layering: dict[str, str],
    techniques: list[str],
    distill: dict[str, str],
    identity: dict[str, Any],
    next_route: str,
) -> dict[str, Any]:
    return {
        "schema_version": "invoke.define-source.v2",
        "source_id": source_id,
        "target": {"id": target_id, "objective": objective},
        "discovery": {"kind": "artifact", "ref": exact_ref(discovery)},
        "template_selection": {
            "profile_id": "invoke.generic-definitions-baseline.v2",
            "selected": "invoke.generic-definitions-baseline.v2",
            "eligible": ["invoke.generic-definitions-baseline.v2"],
            "tie": False,
        },
        "spec_declarations": [declaration],
        "definition_registry": registry,
        "layering": layering,
        "dispatch_trace": {"techniques": techniques},
        "distill": distill,
        "identity_denominator": identity,
        "output_contracts": output_contract(
            "IMPLEMENTATION-LAYERING.md" if layering["kind"] == "seed" else "LAYERING-GAP.md"
        ),
        "transport_policy": {
            "append_existing_only": True,
            "upstream_mutation": False,
            "targets": [],
        },
        "next_route": next_route,
    }


def candidate_fields() -> dict[str, object]:
    return {
        "status": "candidate",
        "status_detail": None,
        "deferred_as": None,
        "supersedes": [],
        "superseded_by": None,
    }


def case_01() -> dict[str, Any]:
    case = ROOT / "cases/case-01-simple"
    evidence = case / "evidence.md"
    definition = {
        "id": "DOC-T1",
        "term": "reviewable definition draft",
        "aliases": ["definition draft"],
        **candidate_fields(),
        "source_kinds": ["domain-vocabulary"],
        "voices": {
            "normative": "A reviewable definition draft is proposed meaning bound to exact evidence and available for review without active authority.",
            "formal": "status = candidate",
            "operational": "Render and inspect the draft, but do not consume it as an active registry definition.",
            "plain_language": "A proposed meaning that can be reviewed but is not active.",
            "domain_context": "Used by the invoice-review feature while its vocabulary is still being evaluated.",
        },
        "notation": [],
        "boundary": {
            "includes": ["Exact-source-bound candidate meaning."],
            "excludes": ["Promotion, runtime, publication, or deployment authority."],
            "conditions": [],
        },
        "source_refs": [source_ref(evidence, "normative", "heading", "Definition Boundary")],
        "primary_consumers": ["DEFINITIONS.md", "GLOSSARY.md"],
        "relations": [],
        "use_carefully": None,
        "misuse_warning": None,
        "challenge_contract": None,
        "promotion_boundary": "Candidate only; definitions-governance owns promotion.",
        "drift_route": "definitions-governance",
        "definition_version": "1",
        "structural_schema": None,
    }
    registry = {
        "registry_id": "invoke.tournament.invoice-review",
        "title": "Invoice Review Candidate Definitions",
        "owner_route": "definitions-governance",
        "authority_scope": {"kind": "feature", "ref": "invoice-review"},
        "visibility": "public",
        "definitions": [definition],
    }
    return common(
        "DOC-TOURNAMENT-C01",
        "Invoice Review Vocabulary",
        "Define one reviewable candidate term for the invoice-review feature.",
        evidence,
        {
            "id": "C01-D1",
            "title": "Candidate Boundary",
            "statement": "The generated registry remains candidate-only and authority-free.",
        },
        registry,
        {"kind": "gap", "rationale": "Downstream design owns any implementation layering."},
        ["sequence", "owner_boundary_check", "concrete_path_evidence"],
        {"classification": "not-required", "rationale": "The case contains one bounded term."},
        {"classification": "not-applicable", "rationale": "No competing stable identity is asserted."},
        "deferred",
    )


def case_02() -> dict[str, Any]:
    case = ROOT / "cases/case-02-relations"
    evidence = case / "evidence.md"
    gate = {
        "id": "DOC-T2-GATE",
        "term": "definition validation gate",
        "aliases": ["validation gate"],
        **candidate_fields(),
        "source_kinds": ["method-vocabulary"],
        "voices": {
            "normative": "A definition validation gate is a bounded check that must pass before a candidate definition bundle can proceed.",
            "formal": "gate(source) = pass",
            "operational": "Run the declared source and artifact checks before handing the generated bundle forward.",
            "plain_language": "A required check before the bundle can move on.",
            "domain_context": "Used by Invoke Define before its candidate bundle is handed to another route.",
        },
        "notation": [],
        "boundary": {
            "includes": ["Source and generated-artifact validation."],
            "excludes": ["Acceptance or promotion decisions."],
            "conditions": ["The gate evaluates one exact source and its generated bundle."],
        },
        "source_refs": [source_ref(evidence, "normative", "heading", "Validation Gate")],
        "primary_consumers": ["invoke", "definitions-governance"],
        "relations": [],
        "use_carefully": None,
        "misuse_warning": None,
        "challenge_contract": None,
        "promotion_boundary": "Candidate only; definitions-governance owns promotion.",
        "drift_route": "invoke",
        "definition_version": "1",
        "structural_schema": None,
    }
    bundle = {
        "id": "DOC-T2-BUNDLE",
        "term": "candidate definition bundle",
        "aliases": ["definition bundle"],
        **candidate_fields(),
        "source_kinds": ["synthesis"],
        "voices": {
            "normative": "A candidate definition bundle is the complete atomic output generated from one valid Define source.",
            "formal": "bundle = compile(valid_source)",
            "operational": "Inspect DEFINITIONS.json first, derived views second, and the stage receipt last.",
            "plain_language": "All files produced together from one valid definition source.",
            "domain_context": "Used by Invoke Define as its candidate-only handoff package.",
        },
        "notation": [],
        "boundary": {
            "includes": ["The complete eleven-file atomic output directory."],
            "excludes": ["Active registry state or downstream execution authority."],
            "conditions": ["Every file comes from the same successful compiler run."],
        },
        "source_refs": [source_ref(evidence, "evidence", "heading", "Candidate Bundle")],
        "primary_consumers": ["invoke", "task-session"],
        "relations": [{"id": "DOC-T2-GATE", "type": "depends-on"}],
        "use_carefully": None,
        "misuse_warning": "Do not treat the stage receipt as the definition artifact.",
        "challenge_contract": None,
        "promotion_boundary": "Candidate only; definitions-governance owns promotion.",
        "drift_route": "invoke",
        "definition_version": "1",
        "structural_schema": None,
    }
    registry = {
        "registry_id": "invoke.tournament.bundle-validation",
        "title": "Bundle Validation Candidate Definitions",
        "owner_route": "invoke",
        "authority_scope": {"kind": "project", "ref": "invoke-documentation-tournament"},
        "visibility": "public",
        "definitions": [gate, bundle],
    }
    return common(
        "DOC-TOURNAMENT-C02",
        "Definition Bundle Validation",
        "Define the gate and bundle relationship for an atomic candidate output.",
        evidence,
        {
            "id": "C02-D1",
            "title": "Atomic Bundle",
            "statement": "The bundle is published only after every declared validation passes.",
        },
        registry,
        {
            "kind": "seed",
            "decision": "Preserve one atomic source-to-bundle producer boundary.",
            "minimum_unit": "One source, one compiler run, and one complete bundle.",
        },
        ["sequence", "validation_loop", "owner_boundary_check"],
        {
            "classification": "required",
            "verdict": "pass",
            "evidence": "Two related terms are retained as the smallest coherent semantic graph.",
        },
        {"classification": "not-applicable", "rationale": "Both requested ids are already stable and distinct."},
        "design",
    )


def case_03() -> dict[str, Any]:
    case = ROOT / "cases/case-03-structural"
    evidence = case / "evidence.json"
    schema = case / "concept.schema.json"
    definition = {
        "id": "DOC-T3",
        "term": "definition source binding",
        "aliases": ["source binding"],
        **candidate_fields(),
        "source_kinds": ["method-vocabulary", "local-inference"],
        "voices": {
            "normative": "A definition source binding is an exact link from a semantic claim to repository bytes and a selector that resolves within those bytes.",
            "formal": "binding = (path, sha256, size, selector_type, selector)",
            "operational": "Recompute the digest and size, then prove the selector resolves before accepting the source.",
            "plain_language": "A precise pointer from a definition to the evidence it relies on.",
            "domain_context": "Used by Invoke Define to make candidate definitions reproducible from public repository evidence.",
        },
        "notation": [{"symbol": "binding", "meaning": "The exact path, digest, size, and selector tuple."}],
        "boundary": {
            "includes": ["Repository-relative path, exact digest and size, and a resolving selector."],
            "excludes": ["Remote URLs, guessed evidence values, and promotion authority."],
            "conditions": ["The referenced bytes remain unchanged."],
        },
        "source_refs": [
            source_ref(evidence, "evidence", "json-pointer", "/concept/meaning"),
            source_ref(schema, "provenance", "json-pointer", "/title"),
        ],
        "primary_consumers": ["invoke", "validate_definitions_artifact"],
        "relations": [],
        "use_carefully": None,
        "misuse_warning": "A path without current byte evidence is not an exact source binding.",
        "challenge_contract": {
            "modes": ["evidence", "scope"],
            "claim_or_edge": "DOC-T3 source evidence",
            "owner_route": "invoke",
            "gate": "source_ref_validation",
            "blocking_question": "Do the recorded bytes and selector still resolve exactly?",
            "residue_route": "invoke:refresh",
        },
        "promotion_boundary": "Candidate only; validation does not promote the definition.",
        "drift_route": "invoke:refresh",
        "definition_version": "1",
        "structural_schema": {
            "handle": "DOC-T3-SCHEMA",
            "status": "machine-checkable",
            "ref": schema.relative_to(REPO).as_posix(),
        },
    }
    registry = {
        "registry_id": "invoke.tournament.source-binding",
        "title": "Source Binding Candidate Definition",
        "owner_route": "invoke",
        "authority_scope": {"kind": "artifact", "ref": "define-source-v2"},
        "visibility": "public",
        "definitions": [definition],
    }
    return common(
        "DOC-TOURNAMENT-C03",
        "Exact Definition Source Binding",
        "Define a machine-checkable source binding with an explicit identity denominator.",
        evidence,
        {
            "id": "C03-D1",
            "title": "Exact Evidence",
            "statement": "Every normative or evidence source is bound to current repository bytes.",
        },
        registry,
        {"kind": "gap", "rationale": "This case tests evidence structure rather than implementation layering."},
        ["concrete_path_evidence", "owner_boundary_check", "validation_loop"],
        {"classification": "not-required", "rationale": "One source-binding concept is already the smallest coherent unit."},
        {
            "classification": "required",
            "request_ref": exact_ref(case / "identity-request.json"),
            "result_ref": exact_ref(case / "identity-result.json"),
        },
        "sigil-development",
    )


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    cases = {"case-01": case_01(), "case-02": case_02(), "case-03": case_03()}
    if GOLDENS.exists():
        shutil.rmtree(GOLDENS)
    GOLDENS.mkdir(parents=True)

    case_manifest: dict[str, Any] = {
        "schema_version": "invoke.define-documentation-tournament-oracle.v1",
        "flexible_rationale_paths": {
            "case-01": ["/layering/rationale", "/distill/rationale", "/identity_denominator/rationale"],
            "case-02": ["/identity_denominator/rationale"],
            "case-03": ["/layering/rationale", "/distill/rationale"],
        },
        "golden_sources": {},
    }
    for case_id, source in cases.items():
        source_path = GOLDENS / f"{case_id}.json"
        write_json(source_path, source)
        with tempfile.TemporaryDirectory(prefix=f"invoke-{case_id}-") as temp:
            output = Path(temp) / "bundle"
            result = subprocess.run(
                [
                    "python3",
                    str(COMPILER),
                    str(source_path),
                    "--output-dir",
                    str(output),
                    "--repo-root",
                    str(REPO),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                raise SystemExit(f"oracle {case_id} does not compile: {result.stdout}{result.stderr}")
            if len(list(output.iterdir())) != 11:
                raise SystemExit(f"oracle {case_id} did not create eleven files")
        case_manifest["golden_sources"][case_id] = {
            "path": source_path.relative_to(ROOT).as_posix(),
            "sha256": hashlib.sha256(source_path.read_bytes()).hexdigest(),
        }

    write_json(ORACLE / "cases.json", case_manifest)
    write_json(
        ORACLE / "blind-map.json",
        {
            "schema_version": "invoke.define-documentation-tournament-blind-map.v1",
            "alpha": "schema-order-reference",
            "beta": "tutorial-first-walkthrough",
            "gamma": "ownership-first-progressive-reference",
            "hypothesis_candidate": "gamma",
        },
    )

    for candidate in ("alpha", "beta", "gamma"):
        for replicate in (1, 2):
            trial_id = f"trial-{candidate}-{replicate:02d}"
            trial_root = RUNS / trial_id
            (trial_root / "sources").mkdir(parents=True, exist_ok=True)
            write_json(
                trial_root / "TRIAL.json",
                {
                    "schema_version": "invoke.define-documentation-trial.v1",
                    "trial_id": trial_id,
                    "candidate": candidate,
                    "replicate": replicate,
                    "guide": f"guides/guide-{candidate}.md",
                    "cases": [
                        "cases/case-01-simple",
                        "cases/case-02-relations",
                        "cases/case-03-structural",
                    ],
                    "outputs": {
                        "case-01": f"runs/{trial_id}/sources/case-01.json",
                        "case-02": f"runs/{trial_id}/sources/case-02.json",
                        "case-03": f"runs/{trial_id}/sources/case-03.json",
                    },
                    "first_attempt_only": True,
                },
            )

    print("ORACLE_BUILD=pass")
    print(f"CASE_COUNT={len(cases)}")
    print("TRIAL_COUNT=6")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
