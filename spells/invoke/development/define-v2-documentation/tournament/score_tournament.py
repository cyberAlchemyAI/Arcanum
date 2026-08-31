#!/usr/bin/env python3
"""Score frozen first-attempt Define v2 sources with the canonical compiler."""

from __future__ import annotations

import argparse
import copy
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[5]
ORACLE_PATH = ROOT / "oracle/cases.json"
GUIDE_MANIFEST = ROOT / "GUIDE-MANIFEST.json"
COMPILER = REPO / "arcanum/spells/invoke/scripts/compile_define_source_v2.py"
CASE_IDS = ("case-01", "case-02", "case-03")
CANDIDATES = ("alpha", "beta", "gamma")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def remove_pointer(document: dict[str, Any], pointer: str) -> None:
    current: Any = document
    tokens = [item.replace("~1", "/").replace("~0", "~") for item in pointer.split("/")[1:]]
    for token in tokens[:-1]:
        if not isinstance(current, dict) or token not in current:
            return
        current = current[token]
    if isinstance(current, dict) and tokens:
        current.pop(tokens[-1], None)


def order_insensitive(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: order_insensitive(value[key]) for key in sorted(value)}
    if isinstance(value, list):
        normalized = [order_insensitive(item) for item in value]
        return sorted(
            normalized,
            key=lambda item: json.dumps(item, sort_keys=True, separators=(",", ":"), ensure_ascii=False),
        )
    return value


def semantic_projection(document: dict[str, Any], flexible_paths: list[str]) -> Any:
    projection = copy.deepcopy(document)
    for pointer in flexible_paths:
        remove_pointer(projection, pointer)
    return order_insensitive(projection)


def category_errors(document: Any) -> list[str]:
    if not isinstance(document, dict):
        return ["source_root_is_not_object"]
    errors: list[str] = []
    if document.get("schema_version") != "invoke.define-source.v2":
        errors.append("wrong_or_derived_root_schema")
    forbidden_root = {
        "$schema",
        "registry_status",
        "authority_effect",
        "receipt_id",
        "producer",
        "outputs",
        "result",
        "receipt_digest",
    }
    for key in sorted(forbidden_root & set(document)):
        errors.append(f"authored_derived_root_field:{key}")
    contracts = document.get("output_contracts")
    if isinstance(contracts, dict) and contracts.get("definitions") != "DEFINITIONS.json":
        errors.append("definitions_output_not_DEFINITIONS.json")
    registry = document.get("definition_registry")
    if isinstance(registry, dict):
        for definition in registry.get("definitions", []) if isinstance(registry.get("definitions"), list) else []:
            if not isinstance(definition, dict):
                continue
            definition_id = definition.get("id", "<unknown>")
            if definition.get("status") != "candidate":
                errors.append(f"non_candidate_definition:{definition_id}")
            for key in ("authority_effect", "receipt_id", "receipt_digest", "producer", "registry_status"):
                if key in definition:
                    errors.append(f"authored_derived_definition_field:{definition_id}:{key}")
    return sorted(set(errors))


def compile_once(source_path: Path) -> tuple[bool, str, int | None]:
    with tempfile.TemporaryDirectory(prefix="invoke-doc-score-") as temp:
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
        detail = (result.stdout + result.stderr).strip()
        inventory = len(list(output.iterdir())) if output.is_dir() else None
        return result.returncode == 0 and inventory == 11, detail, inventory


def score_case(
    case_id: str,
    source_path: Path,
    golden_path: Path,
    flexible_paths: list[str],
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "case_id": case_id,
        "source": source_path.relative_to(ROOT).as_posix() if source_path.is_relative_to(ROOT) else str(source_path),
        "source_present": source_path.is_file(),
        "json_parse": False,
        "category_errors": [],
        "compile_pass": False,
        "compiled_file_count": None,
        "semantic_projection_pass": False,
        "score": 0,
        "compiler_detail": "not_run",
    }
    if not source_path.is_file():
        return result
    result["score"] += 2
    try:
        document = load_json(source_path)
    except (OSError, json.JSONDecodeError) as error:
        result["compiler_detail"] = f"JSON_PARSE_BLOCK: {error}"
        return result
    result["json_parse"] = True
    errors = category_errors(document)
    result["category_errors"] = errors
    if not errors:
        result["score"] += 3
    compiled, detail, inventory = compile_once(source_path)
    result["compile_pass"] = compiled
    result["compiler_detail"] = detail
    result["compiled_file_count"] = inventory
    if compiled:
        result["score"] += 10
    golden = load_json(golden_path)
    semantic_pass = semantic_projection(document, flexible_paths) == semantic_projection(
        golden, flexible_paths
    )
    result["semantic_projection_pass"] = semantic_pass
    if semantic_pass:
        result["score"] += 5
    return result


def validate_guide_control() -> tuple[bool, list[str]]:
    if not GUIDE_MANIFEST.is_file():
        return False, ["guide_manifest_missing"]
    manifest = load_json(GUIDE_MANIFEST)
    equivalence = manifest.get("equivalence", {})
    errors = []
    for key in ("same_section_inventory", "same_rendered_section_bytes"):
        if equivalence.get(key) is not True:
            errors.append(f"guide_equivalence_failed:{key}")
    if equivalence.get("candidate_specific_prose") is not False:
        errors.append("candidate_specific_prose_present")
    if set(manifest.get("guides", {})) != set(CANDIDATES):
        errors.append("guide_candidate_inventory_mismatch")
    return not errors, errors


def score_trial(trial_path: Path, oracle: dict[str, Any]) -> dict[str, Any]:
    trial = load_json(trial_path)
    trial_id = trial["trial_id"]
    candidate = trial["candidate"]
    outputs = trial.get("outputs", {})
    case_results = []
    for case_id in CASE_IDS:
        source_path = ROOT / outputs.get(case_id, "missing")
        golden_rel = oracle["golden_sources"][case_id]["path"]
        case_results.append(
            score_case(
                case_id,
                source_path,
                ROOT / golden_rel,
                oracle["flexible_rationale_paths"].get(case_id, []),
            )
        )
    return {
        "trial_id": trial_id,
        "candidate": candidate,
        "replicate": trial["replicate"],
        "complete": all(item["source_present"] for item in case_results),
        "compile_passes": sum(bool(item["compile_pass"]) for item in case_results),
        "semantic_projection_passes": sum(bool(item["semantic_projection_pass"]) for item in case_results),
        "category_error_count": sum(len(item["category_errors"]) for item in case_results),
        "score": sum(item["score"] for item in case_results),
        "cases": case_results,
    }


def aggregate(trials: list[dict[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for candidate in CANDIDATES:
        selected = [trial for trial in trials if trial["candidate"] == candidate]
        result[candidate] = {
            "trial_count": len(selected),
            "complete_trial_count": sum(bool(item["complete"]) for item in selected),
            "compile_passes": sum(item["compile_passes"] for item in selected),
            "semantic_projection_passes": sum(item["semantic_projection_passes"] for item in selected),
            "category_error_count": sum(item["category_error_count"] for item in selected),
            "score": sum(item["score"] for item in selected),
        }
    return result


def ranking_key(item: tuple[str, dict[str, Any]]) -> tuple[int, int, int, int]:
    _, metrics = item
    return (
        metrics["compile_passes"],
        metrics["semantic_projection_passes"],
        -metrics["category_error_count"],
        metrics["score"],
    )


def adjudicate(aggregates: dict[str, Any], complete: bool, protocol_errors: list[str]) -> dict[str, Any]:
    if protocol_errors:
        return {"status": "invalid", "verdict": "INVALID", "winner": None, "reason": protocol_errors}
    if not complete:
        return {"status": "not_evaluable", "verdict": None, "winner": None, "reason": ["six_complete_trials_required"]}
    ranked = sorted(aggregates.items(), key=ranking_key, reverse=True)
    first_key = ranking_key(ranked[0])
    winners = [candidate for candidate, metrics in ranked if ranking_key((candidate, metrics)) == first_key]
    if winners == ["gamma"]:
        return {"status": "evaluated", "verdict": "SURVIVED", "winner": "gamma", "reason": []}
    return {
        "status": "evaluated",
        "verdict": "FALSIFIED",
        "winner": winners[0] if len(winners) == 1 else None,
        "reason": ["ownership_first_not_unique_winner", f"top_candidates:{','.join(winners)}"],
    }


def self_test() -> int:
    oracle = load_json(ORACLE_PATH)
    for case_id in CASE_IDS:
        golden = ROOT / oracle["golden_sources"][case_id]["path"]
        result = score_case(
            case_id,
            golden,
            golden,
            oracle["flexible_rationale_paths"].get(case_id, []),
        )
        if result["score"] != 20 or not result["compile_pass"] or not result["semantic_projection_pass"]:
            raise SystemExit(f"golden self-test failed for {case_id}: {json.dumps(result, sort_keys=True)}")

    with tempfile.TemporaryDirectory(prefix="score-negative-", dir=ROOT / "oracle") as temp:
        source = load_json(ROOT / oracle["golden_sources"]["case-01"]["path"])
        source["definition_registry"]["definitions"][0]["status"] = "active"
        bad = Path(temp) / "bad.json"
        bad.write_text(json.dumps(source, indent=2) + "\n", encoding="utf-8")
        result = score_case(
            "case-01",
            bad,
            ROOT / oracle["golden_sources"]["case-01"]["path"],
            oracle["flexible_rationale_paths"]["case-01"],
        )
        if result["compile_pass"] or not result["category_errors"] or result["semantic_projection_pass"]:
            raise SystemExit("negative self-test failed")
    print("SCORER_SELF_TEST=pass")
    print("GOLDEN_CASES=3")
    print("NEGATIVE_CASES=1")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs", type=Path, default=ROOT / "runs")
    parser.add_argument("--output", type=Path, default=ROOT / "SCORECARD.json")
    parser.add_argument("--finalize", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()

    oracle = load_json(ORACLE_PATH)
    trial_paths = sorted(args.runs.glob("trial-*/TRIAL.json"))
    trials = [score_trial(path, oracle) for path in trial_paths]
    guide_pass, guide_errors = validate_guide_control()
    protocol_errors = list(guide_errors)
    if len(trials) != 6:
        protocol_errors.append(f"trial_manifest_count:{len(trials)}")
    if len({item["trial_id"] for item in trials}) != len(trials):
        protocol_errors.append("duplicate_trial_id")
    aggregates = aggregate(trials)
    complete = (
        len(trials) == 6
        and all(item["complete"] for item in trials)
        and all(aggregates[candidate]["trial_count"] == 2 for candidate in CANDIDATES)
    )
    adjudication_errors = protocol_errors if args.finalize else [
        item for item in protocol_errors if not item.startswith("trial_manifest_count:")
    ]
    adjudication = adjudicate(aggregates, complete, adjudication_errors)
    scorecard = {
        "schema_version": "invoke.define-documentation-tournament-scorecard.v1",
        "guide_control_pass": guide_pass,
        "trial_count": len(trials),
        "complete_trial_count": sum(bool(item["complete"]) for item in trials),
        "trials": trials,
        "candidates": aggregates,
        "adjudication": adjudication,
        "claim_ceiling": "Directional evidence for this model, compiler, case set, and six first attempts only.",
    }
    args.output.write_text(json.dumps(scorecard, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"TOURNAMENT_STATUS={adjudication['status']}")
    print(f"VERDICT={adjudication['verdict'] or 'not_evaluable'}")
    print(f"SCORECARD={args.output}")
    return 0 if adjudication["status"] != "invalid" else 2


if __name__ == "__main__":
    raise SystemExit(main())
