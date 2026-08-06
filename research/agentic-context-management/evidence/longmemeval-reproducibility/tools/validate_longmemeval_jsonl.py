#!/usr/bin/env python3
"""Validate ACM OR1 LongMemEval JSONL evidence without third-party packages."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "0.1.0"
PROJECT_ID = "agentic-context-management"
EXPERIMENT_ID = "ACM-OR1-LME-REPRO"
SELECTED_UNIT = "OR1"
EVIDENCE_CLASSES = {"synthetic_fixture", "dry_run", "live_experiment"}
CATEGORY_ORDER = [
    "single-session-user",
    "single-session-preference",
    "knowledge-update",
    "temporal-reasoning",
    "single-session-assistant",
    "multi-session",
]
LIVE_CATEGORY_COUNTS = {
    "single-session-user": 70,
    "single-session-preference": 30,
    "knowledge-update": 78,
    "temporal-reasoning": 133,
    "single-session-assistant": 56,
    "multi-session": 133,
}
SHA256_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
GIT_RE = re.compile(r"^[0-9a-f]{40}$")
COMMON_FIELDS = {
    "schema_version",
    "project_id",
    "experiment_id",
    "selected_unit",
    "run_id",
    "record_index",
    "record_type",
    "timestamp",
    "evidence_class",
    "protocol_deviations",
    "claim_status_update_allowed",
    "notes",
}
RECORD_FIELDS = {
    "run_manifest": {
        "source_pins",
        "dataset",
        "models",
        "provider",
        "prompt_hashes",
        "judge_protocol",
        "isolation_mode",
    },
    "question_result": {"question", "retrieval", "answer", "judge", "correct"},
    "run_summary": {"question_count", "correct_count", "accuracy", "category_results"},
}


def is_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def require_object(value: Any, path: str, errors: list[str]) -> dict[str, Any] | None:
    if not isinstance(value, dict):
        errors.append(f"{path}: expected object")
        return None
    return value


def require_fields(row: dict[str, Any], fields: list[str], path: str, errors: list[str]) -> None:
    for field in fields:
        if field not in row:
            errors.append(f"{path}.{field}: missing required field")


def reject_unknown(value: dict[str, Any], allowed: set[str], path: str, errors: list[str]) -> None:
    for field in sorted(set(value) - allowed):
        errors.append(f"{path}.{field}: unknown field")


def validate_sha(value: Any, path: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not SHA256_RE.fullmatch(value):
        errors.append(f"{path}: expected sha256:<64 lowercase hex characters>")


def validate_git(value: Any, path: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not GIT_RE.fullmatch(value):
        errors.append(f"{path}: expected 40-character lowercase Git revision")


def parse_timestamp(value: Any, path: str, errors: list[str]) -> datetime | None:
    if not isinstance(value, str):
        errors.append(f"{path}: expected ISO 8601 string")
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        errors.append(f"{path}: expected ISO 8601 date-time")
        return None


def validate_artifact(value: Any, path: str, errors: list[str]) -> None:
    artifact = require_object(value, path, errors)
    if artifact is None:
        return
    reject_unknown(artifact, {"ref", "sha256"}, path, errors)
    require_fields(artifact, ["ref", "sha256"], path, errors)
    if "ref" in artifact and (not isinstance(artifact["ref"], str) or not artifact["ref"]):
        errors.append(f"{path}.ref: expected non-empty string")
    if "sha256" in artifact:
        validate_sha(artifact["sha256"], f"{path}.sha256", errors)


def validate_common(row: dict[str, Any], line_no: int, errors: list[str]) -> None:
    path = f"line {line_no}"
    require_fields(
        row,
        [
            "schema_version",
            "project_id",
            "experiment_id",
            "selected_unit",
            "run_id",
            "record_index",
            "record_type",
            "timestamp",
            "evidence_class",
            "protocol_deviations",
            "claim_status_update_allowed",
        ],
        path,
        errors,
    )
    constants = {
        "schema_version": SCHEMA_VERSION,
        "project_id": PROJECT_ID,
        "experiment_id": EXPERIMENT_ID,
        "selected_unit": SELECTED_UNIT,
    }
    for field, expected in constants.items():
        if field in row and row[field] != expected:
            errors.append(f"{path}.{field}: expected {expected}")
    if "run_id" in row and (not isinstance(row["run_id"], str) or not row["run_id"]):
        errors.append(f"{path}.run_id: expected non-empty string")
    if "record_index" in row and (not is_int(row["record_index"]) or row["record_index"] < 0):
        errors.append(f"{path}.record_index: expected non-negative integer")
    if row.get("record_type") not in {"run_manifest", "question_result", "run_summary"}:
        errors.append(f"{path}.record_type: expected run_manifest, question_result, or run_summary")
    else:
        reject_unknown(row, COMMON_FIELDS | RECORD_FIELDS[row["record_type"]], path, errors)
    if "timestamp" in row:
        parse_timestamp(row["timestamp"], f"{path}.timestamp", errors)
    if row.get("evidence_class") not in EVIDENCE_CLASSES:
        errors.append(f"{path}.evidence_class: expected one of {', '.join(sorted(EVIDENCE_CLASSES))}")
    if "protocol_deviations" in row:
        deviations = row["protocol_deviations"]
        if not isinstance(deviations, list) or any(not isinstance(item, str) or not item for item in deviations):
            errors.append(f"{path}.protocol_deviations: expected array of non-empty strings")
    if row.get("claim_status_update_allowed") is not False:
        errors.append(f"{path}.claim_status_update_allowed: must be false for raw or fixture evidence")


def validate_manifest(row: dict[str, Any], line_no: int, errors: list[str]) -> None:
    path = f"line {line_no}"
    require_fields(
        row,
        ["source_pins", "dataset", "models", "provider", "prompt_hashes", "judge_protocol", "isolation_mode"],
        path,
        errors,
    )
    pins = require_object(row.get("source_pins"), f"{path}.source_pins", errors)
    if pins is not None:
        reject_unknown(
            pins,
            {
                "paper_pdf_sha256",
                "companion_harness_revision",
                "companion_results_revision",
                "published_run_harness_revision",
            },
            f"{path}.source_pins",
            errors,
        )
        require_fields(
            pins,
            ["paper_pdf_sha256", "companion_harness_revision", "companion_results_revision", "published_run_harness_revision"],
            f"{path}.source_pins",
            errors,
        )
        if "paper_pdf_sha256" in pins:
            validate_sha(pins["paper_pdf_sha256"], f"{path}.source_pins.paper_pdf_sha256", errors)
        for field in ["companion_harness_revision", "companion_results_revision"]:
            if field in pins:
                validate_git(pins[field], f"{path}.source_pins.{field}", errors)
        published = pins.get("published_run_harness_revision")
        if published is not None:
            validate_git(published, f"{path}.source_pins.published_run_harness_revision", errors)

    dataset = require_object(row.get("dataset"), f"{path}.dataset", errors)
    if dataset is not None:
        reject_unknown(
            dataset,
            {
                "name",
                "revision",
                "distribution",
                "split",
                "expected_question_count",
                "expected_category_counts",
                "ordered_question_set_sha256",
            },
            f"{path}.dataset",
            errors,
        )
        require_fields(
            dataset,
            ["name", "revision", "distribution", "split", "expected_question_count", "expected_category_counts", "ordered_question_set_sha256"],
            f"{path}.dataset",
            errors,
        )
        for field in ["name", "revision", "distribution", "split"]:
            if field in dataset and (not isinstance(dataset[field], str) or not dataset[field]):
                errors.append(f"{path}.dataset.{field}: expected non-empty string")
        count = dataset.get("expected_question_count")
        if not is_int(count) or count < 1:
            errors.append(f"{path}.dataset.expected_question_count: expected positive integer")
        category_counts = require_object(dataset.get("expected_category_counts"), f"{path}.dataset.expected_category_counts", errors)
        if category_counts is not None:
            if not category_counts:
                errors.append(f"{path}.dataset.expected_category_counts: expected non-empty object")
            for category, value in category_counts.items():
                if category not in CATEGORY_ORDER:
                    errors.append(f"{path}.dataset.expected_category_counts.{category}: unknown category")
                if not is_int(value) or value < 0:
                    errors.append(f"{path}.dataset.expected_category_counts.{category}: expected non-negative integer")
            if is_int(count) and sum(v for v in category_counts.values() if is_int(v)) != count:
                errors.append(f"{path}.dataset.expected_category_counts: sum must equal expected_question_count")
        if "ordered_question_set_sha256" in dataset:
            validate_sha(dataset["ordered_question_set_sha256"], f"{path}.dataset.ordered_question_set_sha256", errors)

    models = require_object(row.get("models"), f"{path}.models", errors)
    if models is not None:
        reject_unknown(models, {"answer", "judge"}, f"{path}.models", errors)
        require_fields(models, ["answer", "judge"], f"{path}.models", errors)
        for role in ["answer", "judge"]:
            model = require_object(models.get(role), f"{path}.models.{role}", errors)
            if model is None:
                continue
            reject_unknown(model, {"identifier", "revision", "parameters_sha256"}, f"{path}.models.{role}", errors)
            require_fields(model, ["identifier", "revision", "parameters_sha256"], f"{path}.models.{role}", errors)
            for field in ["identifier", "revision"]:
                if field in model and (not isinstance(model[field], str) or not model[field]):
                    errors.append(f"{path}.models.{role}.{field}: expected non-empty string")
            if "parameters_sha256" in model:
                validate_sha(model["parameters_sha256"], f"{path}.models.{role}.parameters_sha256", errors)

    provider = require_object(row.get("provider"), f"{path}.provider", errors)
    if provider is not None:
        reject_unknown(provider, {"name", "adapter_revision", "configuration_sha256"}, f"{path}.provider", errors)
        require_fields(provider, ["name", "adapter_revision", "configuration_sha256"], f"{path}.provider", errors)
        for field in ["name", "adapter_revision"]:
            if field in provider and (not isinstance(provider[field], str) or not provider[field]):
                errors.append(f"{path}.provider.{field}: expected non-empty string")
        if "configuration_sha256" in provider:
            validate_sha(provider["configuration_sha256"], f"{path}.provider.configuration_sha256", errors)

    prompt_hashes = require_object(row.get("prompt_hashes"), f"{path}.prompt_hashes", errors)
    if prompt_hashes is not None:
        reject_unknown(prompt_hashes, {"retrieval", "answer", "judge"}, f"{path}.prompt_hashes", errors)
        require_fields(prompt_hashes, ["retrieval", "answer", "judge"], f"{path}.prompt_hashes", errors)
        for field in ["retrieval", "answer", "judge"]:
            if field in prompt_hashes:
                validate_sha(prompt_hashes[field], f"{path}.prompt_hashes.{field}", errors)

    if row.get("judge_protocol") != "binary_correct_wrong_against_gold":
        errors.append(f"{path}.judge_protocol: expected binary_correct_wrong_against_gold")
    if "isolation_mode" in row and (not isinstance(row["isolation_mode"], str) or not row["isolation_mode"]):
        errors.append(f"{path}.isolation_mode: expected non-empty string")

    evidence_class = row.get("evidence_class")
    if evidence_class == "live_experiment":
        if pins is not None and pins.get("published_run_harness_revision") is None:
            errors.append(f"{path}.source_pins.published_run_harness_revision: required for live experiment")
        if dataset is not None:
            if dataset.get("name") != "LongMemEval_S":
                errors.append(f"{path}.dataset.name: live experiment requires LongMemEval_S")
            if dataset.get("distribution") != "official" or dataset.get("split") != "full":
                errors.append(f"{path}.dataset: live experiment requires official full distribution")
            if dataset.get("expected_question_count") != 500:
                errors.append(f"{path}.dataset.expected_question_count: live experiment requires 500")
            if dataset.get("expected_category_counts") != LIVE_CATEGORY_COUNTS:
                errors.append(f"{path}.dataset.expected_category_counts: live experiment requires official category counts")
        if models is not None:
            for role in ["answer", "judge"]:
                model = models.get(role)
                if isinstance(model, dict) and model.get("identifier") != "gpt-5-mini":
                    errors.append(f"{path}.models.{role}.identifier: protocol-equivalent run requires gpt-5-mini")
    elif evidence_class == "synthetic_fixture":
        if pins is not None and pins.get("published_run_harness_revision") is not None:
            errors.append(f"{path}.source_pins.published_run_harness_revision: synthetic fixture must leave unresolved pin null")
        if models is not None:
            for role in ["answer", "judge"]:
                model = models.get(role)
                if isinstance(model, dict) and not str(model.get("identifier", "")).startswith("synthetic-"):
                    errors.append(f"{path}.models.{role}.identifier: synthetic fixture requires synthetic-* identifier")
        if provider is not None and not str(provider.get("name", "")).startswith("synthetic-"):
            errors.append(f"{path}.provider.name: synthetic fixture requires synthetic-* provider")


def validate_question(row: dict[str, Any], line_no: int, errors: list[str]) -> None:
    path = f"line {line_no}"
    require_fields(row, ["question", "retrieval", "answer", "judge", "correct"], path, errors)
    question = require_object(row.get("question"), f"{path}.question", errors)
    if question is not None:
        reject_unknown(question, {"id", "category", "query_sha256", "gold_answer_sha256"}, f"{path}.question", errors)
        require_fields(question, ["id", "category", "query_sha256", "gold_answer_sha256"], f"{path}.question", errors)
        if "id" in question and (not isinstance(question["id"], str) or not question["id"]):
            errors.append(f"{path}.question.id: expected non-empty string")
        if question.get("category") not in CATEGORY_ORDER:
            errors.append(f"{path}.question.category: unknown LongMemEval category")
        for field in ["query_sha256", "gold_answer_sha256"]:
            if field in question:
                validate_sha(question[field], f"{path}.question.{field}", errors)

    retrieval = require_object(row.get("retrieval"), f"{path}.retrieval", errors)
    if retrieval is not None:
        reject_unknown(retrieval, {"retrieved_item_count", "token_count", "latency_ms", "artifact"}, f"{path}.retrieval", errors)
        require_fields(retrieval, ["retrieved_item_count", "token_count", "latency_ms", "artifact"], f"{path}.retrieval", errors)
        for field in ["retrieved_item_count", "token_count"]:
            value = retrieval.get(field)
            if not is_int(value) or value < 0:
                errors.append(f"{path}.retrieval.{field}: expected non-negative integer")
        latency = retrieval.get("latency_ms")
        if not is_number(latency) or latency < 0:
            errors.append(f"{path}.retrieval.latency_ms: expected non-negative number")
        validate_artifact(retrieval.get("artifact"), f"{path}.retrieval.artifact", errors)

    for role in ["answer", "judge"]:
        value = require_object(row.get(role), f"{path}.{role}", errors)
        if value is None:
            continue
        allowed = {"model_identifier", "artifact", "token_count"} if role == "answer" else {"model_identifier", "artifact", "verdict"}
        reject_unknown(value, allowed, f"{path}.{role}", errors)
        required = ["model_identifier", "artifact"]
        if role == "answer":
            required.append("token_count")
        else:
            required.append("verdict")
        require_fields(value, required, f"{path}.{role}", errors)
        if "model_identifier" in value and (not isinstance(value["model_identifier"], str) or not value["model_identifier"]):
            errors.append(f"{path}.{role}.model_identifier: expected non-empty string")
        if role == "answer":
            if not is_int(value.get("token_count")) or value.get("token_count", -1) < 0:
                errors.append(f"{path}.answer.token_count: expected non-negative integer")
        elif value.get("verdict") not in {"CORRECT", "WRONG"}:
            errors.append(f"{path}.judge.verdict: expected CORRECT or WRONG")
        validate_artifact(value.get("artifact"), f"{path}.{role}.artifact", errors)

    if "correct" in row and not isinstance(row["correct"], bool):
        errors.append(f"{path}.correct: expected boolean")
    judge = row.get("judge")
    if isinstance(judge, dict) and isinstance(row.get("correct"), bool):
        expected = judge.get("verdict") == "CORRECT"
        if row["correct"] != expected:
            errors.append(f"{path}.correct: must agree with judge.verdict")


def validate_summary(row: dict[str, Any], line_no: int, errors: list[str]) -> None:
    path = f"line {line_no}"
    require_fields(row, ["question_count", "correct_count", "accuracy", "category_results"], path, errors)
    question_count = row.get("question_count")
    correct_count = row.get("correct_count")
    if not is_int(question_count) or question_count < 1:
        errors.append(f"{path}.question_count: expected positive integer")
    if not is_int(correct_count) or correct_count < 0:
        errors.append(f"{path}.correct_count: expected non-negative integer")
    if is_int(question_count) and is_int(correct_count) and correct_count > question_count:
        errors.append(f"{path}.correct_count: cannot exceed question_count")
    accuracy = row.get("accuracy")
    if not is_number(accuracy) or accuracy < 0 or accuracy > 1:
        errors.append(f"{path}.accuracy: expected number between 0 and 1")
    category_results = require_object(row.get("category_results"), f"{path}.category_results", errors)
    if category_results is not None:
        if not category_results:
            errors.append(f"{path}.category_results: expected non-empty object")
        for category, result in category_results.items():
            if category not in CATEGORY_ORDER:
                errors.append(f"{path}.category_results.{category}: unknown category")
            item = require_object(result, f"{path}.category_results.{category}", errors)
            if item is None:
                continue
            reject_unknown(item, {"question_count", "correct_count", "accuracy"}, f"{path}.category_results.{category}", errors)
            require_fields(item, ["question_count", "correct_count", "accuracy"], f"{path}.category_results.{category}", errors)
            q = item.get("question_count")
            c = item.get("correct_count")
            a = item.get("accuracy")
            if not is_int(q) or q < 1:
                errors.append(f"{path}.category_results.{category}.question_count: expected positive integer")
            if not is_int(c) or c < 0 or (is_int(q) and c > q):
                errors.append(f"{path}.category_results.{category}.correct_count: expected integer in range")
            if not is_number(a) or a < 0 or a > 1:
                errors.append(f"{path}.category_results.{category}.accuracy: expected number between 0 and 1")


def load_rows(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    rows: list[dict[str, Any]] = []
    errors: list[str] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, raw in enumerate(handle, start=1):
            if not raw.strip():
                errors.append(f"line {line_no}: blank lines are forbidden in append-only JSONL")
                continue
            try:
                value = json.loads(raw)
            except json.JSONDecodeError as exc:
                errors.append(f"line {line_no}: invalid JSON: {exc.msg}")
                continue
            if not isinstance(value, dict):
                errors.append(f"line {line_no}: expected JSON object")
                continue
            rows.append(value)
    if not rows:
        errors.append("file: expected at least one JSONL row")
    return rows, errors


def validate_rows(rows: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    for line_no, row in enumerate(rows, start=1):
        validate_common(row, line_no, errors)
        record_type = row.get("record_type")
        if record_type == "run_manifest":
            validate_manifest(row, line_no, errors)
        elif record_type == "question_result":
            validate_question(row, line_no, errors)
        elif record_type == "run_summary":
            validate_summary(row, line_no, errors)

    if not rows:
        return errors
    indices = [row.get("record_index") for row in rows]
    if indices != list(range(len(rows))):
        errors.append(f"file.record_index: expected contiguous sequence 0..{len(rows) - 1}; got {indices}")
    run_ids = {row.get("run_id") for row in rows}
    if len(run_ids) != 1:
        errors.append(f"file.run_id: expected one run_id; got {sorted(map(str, run_ids))}")
    evidence_classes = {row.get("evidence_class") for row in rows}
    if len(evidence_classes) != 1:
        errors.append(f"file.evidence_class: expected one evidence class; got {sorted(map(str, evidence_classes))}")
    record_types = [row.get("record_type") for row in rows]
    if record_types.count("run_manifest") != 1 or record_types[0] != "run_manifest":
        errors.append("file.record_type: expected exactly one run_manifest as first row")
    if record_types.count("run_summary") != 1 or record_types[-1] != "run_summary":
        errors.append("file.record_type: expected exactly one run_summary as final row")
    timestamps: list[datetime] = []
    for line_no, row in enumerate(rows, start=1):
        parsed = parse_timestamp(row.get("timestamp"), f"line {line_no}.timestamp", [])
        if parsed is not None:
            timestamps.append(parsed)
    if len(timestamps) == len(rows) and timestamps != sorted(timestamps):
        errors.append("file.timestamp: expected non-decreasing timestamps")

    manifests = [row for row in rows if row.get("record_type") == "run_manifest"]
    summaries = [row for row in rows if row.get("record_type") == "run_summary"]
    questions = [row for row in rows if row.get("record_type") == "question_result"]
    question_ids = [row.get("question", {}).get("id") for row in questions if isinstance(row.get("question"), dict)]
    duplicates = [item for item, count in Counter(question_ids).items() if count > 1]
    if duplicates:
        errors.append(f"file.question.id: duplicate question IDs {sorted(map(str, duplicates))}")

    if len(manifests) == 1:
        manifest = manifests[0]
        dataset = manifest.get("dataset") if isinstance(manifest.get("dataset"), dict) else {}
        expected_count = dataset.get("expected_question_count")
        expected_categories = dataset.get("expected_category_counts")
        if is_int(expected_count) and len(questions) != expected_count:
            errors.append(f"file.question_result: expected {expected_count} rows from manifest; got {len(questions)}")
        actual_categories = Counter(
            row.get("question", {}).get("category")
            for row in questions
            if isinstance(row.get("question"), dict)
        )
        if isinstance(expected_categories, dict) and dict(actual_categories) != expected_categories:
            errors.append(
                f"file.category_counts: expected {expected_categories}; got {dict(actual_categories)}"
            )
        models = manifest.get("models") if isinstance(manifest.get("models"), dict) else {}
        answer_id = models.get("answer", {}).get("identifier") if isinstance(models.get("answer"), dict) else None
        judge_id = models.get("judge", {}).get("identifier") if isinstance(models.get("judge"), dict) else None
        for idx, question in enumerate(questions, start=1):
            answer = question.get("answer") if isinstance(question.get("answer"), dict) else {}
            judge = question.get("judge") if isinstance(question.get("judge"), dict) else {}
            if answer_id is not None and answer.get("model_identifier") != answer_id:
                errors.append(f"question row {idx}.answer.model_identifier: must match manifest")
            if judge_id is not None and judge.get("model_identifier") != judge_id:
                errors.append(f"question row {idx}.judge.model_identifier: must match manifest")

    if len(summaries) == 1:
        summary = summaries[0]
        correct_count = sum(1 for row in questions if row.get("correct") is True)
        question_count = len(questions)
        accuracy = correct_count / question_count if question_count else 0
        if summary.get("question_count") != question_count:
            errors.append(f"file.summary.question_count: expected {question_count}; got {summary.get('question_count')}")
        if summary.get("correct_count") != correct_count:
            errors.append(f"file.summary.correct_count: expected {correct_count}; got {summary.get('correct_count')}")
        if not is_number(summary.get("accuracy")) or abs(summary.get("accuracy", -1) - accuracy) > 1e-12:
            errors.append(f"file.summary.accuracy: expected {accuracy:.12f}; got {summary.get('accuracy')}")
        category_totals: dict[str, int] = defaultdict(int)
        category_correct: dict[str, int] = defaultdict(int)
        for row in questions:
            question = row.get("question") if isinstance(row.get("question"), dict) else {}
            category = question.get("category")
            if category in CATEGORY_ORDER:
                category_totals[category] += 1
                if row.get("correct") is True:
                    category_correct[category] += 1
        computed = {
            category: {
                "question_count": category_totals[category],
                "correct_count": category_correct[category],
                "accuracy": category_correct[category] / category_totals[category],
            }
            for category in CATEGORY_ORDER
            if category_totals[category]
        }
        if summary.get("category_results") != computed:
            errors.append(f"file.summary.category_results: expected {computed}; got {summary.get('category_results')}")

    return errors


def validate_file(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    rows, errors = load_rows(path)
    errors.extend(validate_rows(rows))
    return rows, errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("jsonl", nargs="+", type=Path)
    args = parser.parse_args()
    total_errors = 0
    for path in args.jsonl:
        if not path.is_file():
            print(f"FAIL {path} (file not found)")
            total_errors += 1
            continue
        rows, errors = validate_file(path)
        if errors:
            print(f"FAIL {path} ({len(rows)} row(s), {len(errors)} error(s))")
            for error in errors:
                print(f"  - {error}")
            total_errors += len(errors)
        else:
            question_count = sum(row.get("record_type") == "question_result" for row in rows)
            print(f"PASS {path} ({len(rows)} row(s), {question_count} question result(s))")
    return 1 if total_errors else 0


if __name__ == "__main__":
    sys.exit(main())
