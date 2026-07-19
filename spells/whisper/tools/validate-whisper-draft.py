#!/usr/bin/env python3
"""Validate a Whisper draft against its text-intent substrate."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - environment guard
    yaml = None


DEFAULT_FORBIDDEN_STARTS = [
    r"(?i)^\s*(yuval|harari|sapiens|in\s+sapiens|as\s+harari)",
]

REQUIRED_PARETO_OBJECTIVES = {"resonance", "relevance", "trajectory"}
REQUIRED_PARETO_GATES = {"opening_contract_compliance", "citation_integrity", "audience_legibility"}
REQUIRED_CANDIDATE_FIELDS = {
    "technique_stack",
    "target_reader_effect",
    "expected_strengths",
    "known_tradeoffs",
    "failure_modes",
    "part_sequence",
    "objective_scores",
    "hard_gate_results",
}
REQUIRED_PART_TRIGGERS = {"delegated", "revised", "validation_failed"}


def load_schema(path: Path) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML is required. Run with the repository python3 environment.")

    with path.open("r", encoding="utf-8") as handle:
        loaded = yaml.safe_load(handle)

    if not isinstance(loaded, dict):
        raise RuntimeError(f"Schema did not parse as a mapping: {path}")

    return loaded.get("text_intent_substrate", loaded)


def prose_paragraphs(markdown: str) -> list[str]:
    paragraphs: list[str] = []
    current: list[str] = []
    in_code = False

    def flush() -> None:
        nonlocal current
        if current:
            paragraphs.append(" ".join(current).strip())
            current = []

    for raw_line in markdown.splitlines():
        line = raw_line.strip()

        if line.startswith("```"):
            flush()
            in_code = not in_code
            continue

        if in_code:
            continue

        if not line:
            flush()
            continue

        if line.startswith("#"):
            flush()
            continue

        if (line.startswith("_") and line.endswith("_")) or (
            line.startswith("*") and line.endswith("*") and len(line) < 160
        ):
            flush()
            continue

        if line.startswith(("- ", "* ", "> ")) or re.match(r"^\d+\.\s+", line):
            flush()
            continue

        current.append(line)

    flush()
    return paragraphs


def markdown_word_count(markdown: str) -> int:
    body = re.sub(r"`([^`]*)`", r"\1", markdown)
    body = re.sub(r"https?://\S+", "", body)
    return len(re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)?", body))


def normalize_prose_block(text: str) -> str:
    words = re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)?", text.lower())
    return " ".join(words)


def contains_any(text: str, terms: list[str]) -> bool:
    lowered = text.lower()
    for term in terms:
        term = str(term).strip().lower()
        if term and term in lowered:
            return True
    return False


def first_external_reference(paragraphs: list[str], terms: list[str]) -> int | None:
    for index, paragraph in enumerate(paragraphs, start=1):
        if contains_any(paragraph, terms):
            return index
    return None


def sentence_count(text: str) -> int:
    return len([part for part in re.split(r"[.!?]+", text) if part.strip()])


def terms_from(*values: object) -> list[str]:
    terms: list[str] = []
    for value in values:
        if isinstance(value, str):
            if value.strip():
                terms.append(value.strip())
        elif isinstance(value, list):
            for item in value:
                term = str(item).strip()
                if term:
                    terms.append(term)

    return terms


def optional_positive_int(value: object) -> int | None:
    if value is None:
        return None

    try:
        number = int(value)
    except (TypeError, ValueError):
        return None

    if number <= 0:
        return None
    return number


def readability_rule_severity(config: dict, rule_id: str, default: str) -> str:
    rules = config.get("validation_rules", {})
    severity = default
    if isinstance(rules, dict):
        severity = str(rules.get(rule_id, default))

    return "block" if severity.strip().lower() == "block" else "flag"


def record_readability_finding(
    config: dict,
    rule_id: str,
    default_severity: str,
    message: str,
    errors: list[str],
    flags: list[str],
) -> None:
    finding = f"readability {rule_id}: {message}"
    if readability_rule_severity(config, rule_id, default_severity) == "block":
        errors.append(finding)
    else:
        flags.append(finding)


def ids_from(items: list[dict], key: str = "id") -> set[str]:
    return {str(item.get(key, "")).strip() for item in items if isinstance(item, dict) and item.get(key)}


def validate_pareto_tournament(schema: dict) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    checks: list[str] = []

    tournament = schema.get("pareto_tournament")
    if not tournament:
        if schema.get("scu_candidate_set", {}).get("tournament_mode") == "pareto_aware":
            errors.append("schema names pareto_aware but lacks pareto_tournament")
        return errors, checks

    if tournament.get("tiering") != "two_tier":
        errors.append("pareto_tournament.tiering must be two_tier")
    else:
        checks.append("pareto tournament tiering is two_tier")

    objective_ids = ids_from(tournament.get("objectives", []))
    missing_objectives = REQUIRED_PARETO_OBJECTIVES - objective_ids
    if missing_objectives:
        errors.append(f"pareto_tournament missing objectives: {', '.join(sorted(missing_objectives))}")
    else:
        checks.append("pareto tournament includes resonance, relevance, and trajectory objectives")

    gate_ids = ids_from(tournament.get("hard_gates", []))
    missing_gates = REQUIRED_PARETO_GATES - gate_ids
    if missing_gates:
        errors.append(f"pareto_tournament missing hard gates: {', '.join(sorted(missing_gates))}")
    else:
        checks.append("pareto tournament declares required hard gates")

    protocol = tournament.get("candidate_protocol", {})
    protocol_fields = set(protocol.get("each_candidate_must_define", []))
    missing_protocol = REQUIRED_CANDIDATE_FIELDS - protocol_fields
    if missing_protocol:
        errors.append(f"pareto candidate protocol missing fields: {', '.join(sorted(missing_protocol))}")
    else:
        checks.append("pareto candidate protocol declares complete candidate fields")

    policy = protocol.get("part_level_policy", {})
    policy_triggers = set(policy.get("mini_tournament_triggers", []))
    missing_triggers = REQUIRED_PART_TRIGGERS - policy_triggers
    if missing_triggers:
        errors.append(f"pareto part-level policy missing triggers: {', '.join(sorted(missing_triggers))}")
    else:
        checks.append("pareto part-level policy limits mini-tournaments to delegated, revised, or failed parts")

    if not protocol.get("dominance_rule"):
        errors.append("pareto candidate protocol missing dominance_rule")
    if not protocol.get("consensus_rule"):
        errors.append("pareto candidate protocol missing consensus_rule")

    candidates = tournament.get("candidates", [])
    if len(candidates) < 2:
        errors.append("pareto_tournament must compare at least two candidates")

    candidate_ids = ids_from(candidates, "candidate_set_id")
    consensus = tournament.get("consensus", {})
    selected = str(consensus.get("selected_candidate_set", "")).strip()
    if not selected:
        errors.append("pareto consensus missing selected_candidate_set")
    elif selected not in candidate_ids:
        errors.append(f"pareto selected candidate `{selected}` is not present in candidates")
    elif not consensus.get("selected_because"):
        errors.append("pareto selected candidate lacks selected_because rationale")
    else:
        checks.append(f"pareto consensus selects `{selected}` with rationale")

    plan_selected = str(schema.get("composition_plan", {}).get("source_candidate_set", "")).strip()
    if selected and plan_selected and selected != plan_selected:
        errors.append(
            "composition_plan.source_candidate_set does not match pareto selected candidate: "
            f"{plan_selected} != {selected}"
        )
    elif selected and plan_selected:
        checks.append("composition plan source matches pareto selected candidate")

    rejected_ids = ids_from(consensus.get("rejected_alternatives", []), "candidate_set_id")
    missing_rejections = candidate_ids - {selected} - rejected_ids
    if missing_rejections:
        errors.append(f"pareto consensus missing rejected alternatives: {', '.join(sorted(missing_rejections))}")
    elif candidate_ids and selected:
        checks.append("pareto consensus preserves rejected alternatives")

    for candidate in candidates:
        if not isinstance(candidate, dict):
            errors.append("pareto candidate entry is not a mapping")
            continue

        candidate_id = str(candidate.get("candidate_set_id", "")).strip() or "<missing>"
        missing_fields = [field for field in REQUIRED_CANDIDATE_FIELDS if field not in candidate]
        if missing_fields:
            errors.append(f"pareto candidate `{candidate_id}` missing fields: {', '.join(sorted(missing_fields))}")
            continue

        scores = candidate.get("objective_scores", {})
        missing_scores = REQUIRED_PARETO_OBJECTIVES - set(scores)
        if missing_scores:
            errors.append(f"pareto candidate `{candidate_id}` missing objective scores: {', '.join(sorted(missing_scores))}")

        gates = candidate.get("hard_gate_results", {})
        missing_gate_results = REQUIRED_PARETO_GATES - set(gates)
        if missing_gate_results:
            errors.append(f"pareto candidate `{candidate_id}` missing hard gate results: {', '.join(sorted(missing_gate_results))}")

        if candidate_id == selected:
            failed_selected_gates = [gate for gate in REQUIRED_PARETO_GATES if gates.get(gate) != "pass"]
            if failed_selected_gates:
                errors.append(
                    f"selected pareto candidate `{candidate_id}` fails gates: "
                    f"{', '.join(sorted(failed_selected_gates))}"
                )

    if not errors:
        checks.append("pareto candidates include scores, gates, tradeoffs, and failure modes")

    part_errors, part_checks = validate_composition_parts(schema, selected)
    errors.extend(part_errors)
    checks.extend(part_checks)

    return errors, checks


def validate_composition_parts(schema: dict, selected_candidate: str) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    checks: list[str] = []

    parts_block = schema.get("composition_parts", {})
    if not parts_block:
        errors.append("two-tier pareto schema requires composition_parts")
        return errors, checks

    policy = parts_block.get("part_level_tournament_policy", {})
    policy_triggers = set(policy.get("mini_tournament_triggers", []))
    missing_policy_triggers = REQUIRED_PART_TRIGGERS - policy_triggers
    if missing_policy_triggers:
        errors.append(
            "composition_parts policy missing mini-tournament triggers: "
            f"{', '.join(sorted(missing_policy_triggers))}"
        )

    parts = parts_block.get("parts", [])
    part_ids = [str(part.get("part_id", "")).strip() for part in parts if isinstance(part, dict)]
    plan_sequence = [str(part_id).strip() for part_id in schema.get("composition_plan", {}).get("construction_sequence", [])]

    if not parts:
        errors.append("composition_parts.parts is empty")
        return errors, checks

    missing_parts = [part_id for part_id in plan_sequence if part_id not in part_ids]
    if missing_parts:
        errors.append(f"composition_parts missing plan parts: {', '.join(missing_parts)}")
    else:
        checks.append("composition parts cover the construction sequence")

    for part in parts:
        if not isinstance(part, dict):
            errors.append("composition part entry is not a mapping")
            continue

        part_id = str(part.get("part_id", "")).strip() or "<missing>"
        if not part.get("global_candidate_binding"):
            errors.append(f"composition part `{part_id}` missing global_candidate_binding")
        elif selected_candidate and part.get("global_candidate_binding") != selected_candidate:
            errors.append(f"composition part `{part_id}` is not bound to selected candidate `{selected_candidate}`")

        triggers = set(part.get("mini_tournament_triggers", []))
        if not triggers:
            errors.append(f"composition part `{part_id}` missing mini_tournament_triggers")
        elif not triggers <= REQUIRED_PART_TRIGGERS:
            errors.append(
                f"composition part `{part_id}` has unsupported triggers: "
                f"{', '.join(sorted(triggers - REQUIRED_PART_TRIGGERS))}"
            )

        for field in ("inputs", "output", "must_do", "must_not_do", "validation"):
            if not part.get(field):
                errors.append(f"composition part `{part_id}` missing {field}")

    if not errors:
        checks.append("composition parts define two-tier mini-tournament hooks")

    return errors, checks


def validate_readability_dynamics(schema: dict, paragraphs: list[str]) -> tuple[list[str], list[str], list[str]]:
    errors: list[str] = []
    checks: list[str] = []
    flags: list[str] = []

    config = schema.get("readability_dynamics")
    if config is None:
        return errors, checks, flags

    if not isinstance(config, dict):
        errors.append("readability_dynamics must be a mapping when present")
        return errors, checks, flags

    defaults = config.get("defaults", {})
    density_profile = config.get("density_profile", {})
    scan_anchors = config.get("scan_anchors", {})
    delivery_flow = config.get("delivery_flow", {})

    if defaults is None:
        defaults = {}
    if density_profile is None:
        density_profile = {}
    if scan_anchors is None:
        scan_anchors = {}
    if delivery_flow is None:
        delivery_flow = {}

    if not isinstance(defaults, dict):
        errors.append("readability_dynamics.defaults must be a mapping when present")
        return errors, checks, flags
    if not isinstance(density_profile, dict):
        errors.append("readability_dynamics.density_profile must be a mapping when present")
        return errors, checks, flags
    if not isinstance(scan_anchors, dict):
        errors.append("readability_dynamics.scan_anchors must be a mapping when present")
        return errors, checks, flags
    if not isinstance(delivery_flow, dict):
        errors.append("readability_dynamics.delivery_flow must be a mapping when present")
        return errors, checks, flags

    default_severity = str(defaults.get("severity_default", "flag"))
    max_words = optional_positive_int(defaults.get("max_words_per_paragraph"))
    max_sentences = optional_positive_int(defaults.get("max_sentences_per_paragraph"))
    max_consecutive_dense = optional_positive_int(defaults.get("max_consecutive_dense_paragraphs"))
    scan_anchor_interval = optional_positive_int(defaults.get("require_scan_anchor_every_n_blocks"))
    scan_terms = terms_from(scan_anchors.get("terms"))
    abstraction_terms = terms_from(
        config.get("abstraction_terms"),
        config.get("abstract_internal_terms"),
        density_profile.get("abstraction_terms"),
        density_profile.get("abstract_terms"),
        density_profile.get("internal_terms"),
    )
    example_terms = terms_from(
        config.get("example_markers"),
        config.get("example_terms"),
        density_profile.get("example_markers"),
        density_profile.get("example_terms"),
        scan_anchors.get("example_markers"),
    )
    if not example_terms:
        example_terms = ["for example", "for instance", "imagine", "consider", "in practice", "try this"]

    dense_paragraphs: list[int] = []
    for index, paragraph in enumerate(paragraphs, start=1):
        paragraph_words = markdown_word_count(paragraph)
        paragraph_sentences = sentence_count(paragraph)
        dense = False

        if max_words and paragraph_words > max_words:
            dense = True
            record_readability_finding(
                config,
                "density_limit_violation",
                default_severity,
                f"paragraph {index} has {paragraph_words} words, limit {max_words}",
                errors,
                flags,
            )

        if max_sentences and paragraph_sentences > max_sentences:
            dense = True
            record_readability_finding(
                config,
                "sentence_density_violation",
                default_severity,
                f"paragraph {index} has {paragraph_sentences} sentences, limit {max_sentences}",
                errors,
                flags,
            )

        if dense:
            dense_paragraphs.append(index)

        if abstraction_terms and contains_any(paragraph, abstraction_terms):
            grounding_terms = scan_terms + example_terms
            if grounding_terms and not contains_any(paragraph, grounding_terms):
                record_readability_finding(
                    config,
                    "abstraction_without_example",
                    default_severity,
                    f"paragraph {index} uses configured abstraction terms without a configured example or scan anchor",
                    errors,
                    flags,
                )

    if max_consecutive_dense and dense_paragraphs:
        streak: list[int] = []
        for index in range(1, len(paragraphs) + 1):
            if index in dense_paragraphs:
                streak.append(index)
                continue

            if len(streak) > max_consecutive_dense:
                record_readability_finding(
                    config,
                    "density_limit_violation",
                    default_severity,
                    f"paragraphs {streak[0]}-{streak[-1]} are consecutive dense paragraphs, limit {max_consecutive_dense}",
                    errors,
                    flags,
                )
            streak = []

        if len(streak) > max_consecutive_dense:
            record_readability_finding(
                config,
                "density_limit_violation",
                default_severity,
                f"paragraphs {streak[0]}-{streak[-1]} are consecutive dense paragraphs, limit {max_consecutive_dense}",
                errors,
                flags,
            )

    if scan_anchor_interval and scan_terms:
        for start in range(0, len(paragraphs), scan_anchor_interval):
            chunk = paragraphs[start : start + scan_anchor_interval]
            if chunk and not any(contains_any(paragraph, scan_terms) for paragraph in chunk):
                end = start + len(chunk)
                record_readability_finding(
                    config,
                    "scan_anchor_gap",
                    default_severity,
                    f"paragraphs {start + 1}-{end} lack a configured scan anchor",
                    errors,
                    flags,
                )

    if delivery_flow:
        intent_patterns = terms_from(delivery_flow.get("intent_narration_patterns"))
        for index, paragraph in enumerate(paragraphs, start=1):
            for pattern in intent_patterns:
                try:
                    matched = re.search(pattern, paragraph)
                except re.error as exc:
                    errors.append(f"readability delivery_flow has invalid intent pattern `{pattern}`: {exc}")
                    continue

                if matched:
                    record_readability_finding(
                        config,
                        "intent_narration_detected",
                        default_severity,
                        f"paragraph {index} matches configured author-intent narration pattern `{pattern}`",
                        errors,
                        flags,
                    )
                    break

        if delivery_flow.get("detect_exact_duplicate_prose_blocks", False):
            minimum_words = optional_positive_int(delivery_flow.get("duplicate_block_min_words")) or 8
            seen_blocks: dict[str, int] = {}
            for index, paragraph in enumerate(paragraphs, start=1):
                normalized = normalize_prose_block(paragraph)
                if len(normalized.split()) < minimum_words:
                    continue

                first_index = seen_blocks.get(normalized)
                if first_index is not None:
                    record_readability_finding(
                        config,
                        "duplicate_prose_block",
                        default_severity,
                        f"paragraph {index} duplicates paragraph {first_index} after conservative normalization",
                        errors,
                        flags,
                    )
                    continue

                seen_blocks[normalized] = index

        human_checks = terms_from(delivery_flow.get("human_review_checks"))
        checks.append(f"delivery flow evaluated {len(paragraphs)} prose paragraphs")
        if human_checks:
            checks.append(
                "delivery flow reserves human-only checks without claiming mechanical proof: "
                + ", ".join(human_checks)
            )

    checks.append(f"readability dynamics evaluated {len(paragraphs)} prose paragraphs")
    if config.get("layer_id"):
        checks.append(f"readability dynamics layer `{config.get('layer_id')}` is configured")
    if not errors and not flags:
        checks.append("readability dynamics emitted no findings")

    return errors, checks, flags


def validate(schema: dict, draft: str) -> tuple[list[str], list[str], list[str]]:
    errors: list[str] = []
    checks: list[str] = []
    flags: list[str] = []

    pareto_errors, pareto_checks = validate_pareto_tournament(schema)
    errors.extend(pareto_errors)
    checks.extend(pareto_checks)

    transport = schema.get("transport_schema", {})
    contract = transport.get("opening_contract", {})
    validation_rules = contract.get("validation_rules", {})
    external_policy = contract.get("external_reference_policy", {})

    paragraphs = prose_paragraphs(draft)
    if not paragraphs:
        return ["no prose paragraphs found"], checks

    first = paragraphs[0]
    forbidden_patterns = list(validation_rules.get("first_paragraph_cannot_match", []))
    forbidden_patterns.extend(DEFAULT_FORBIDDEN_STARTS)
    for pattern in forbidden_patterns:
        if re.search(str(pattern), first):
            errors.append(
                "first paragraph violates opening_contract: starts with external authority "
                f"or forbidden opening pattern `{pattern}`"
            )
            break
    else:
        checks.append("first paragraph does not start from a forbidden authority pattern")

    grounding_terms = list(validation_rules.get("first_paragraph_must_include_any", []))
    if grounding_terms:
        if contains_any(first, grounding_terms):
            checks.append("first paragraph contains a reader-grounding term")
        else:
            errors.append(
                "first paragraph lacks a reader-grounding term "
                f"from {', '.join(map(str, grounding_terms))}"
            )

    external_terms = list(external_policy.get("external_reference_terms", []))
    allowed_after = int(external_policy.get("allowed_after_paragraph", 1))
    if external_terms:
        first_external = first_external_reference(paragraphs, external_terms)
        if first_external is not None and first_external < allowed_after:
            errors.append(
                "external reference appears too early: "
                f"paragraph {first_external}, allowed from paragraph {allowed_after}"
            )
        elif first_external is None:
            checks.append("external reference placement not applicable; no configured external reference found")
        else:
            checks.append(f"external reference appears at paragraph {first_external}, after the opening hook")

    required_anywhere = list(validation_rules.get("draft_must_include_anywhere", []))
    missing = [term for term in required_anywhere if not contains_any(draft, [str(term)])]
    if missing:
        errors.append(f"draft missing required substrate terms: {', '.join(map(str, missing))}")
    elif required_anywhere:
        checks.append("draft includes required substrate terms")

    length_words = transport.get("length_words", {})
    word_count = markdown_word_count(draft)
    min_words = int(length_words.get("min", 0))
    max_words = int(length_words.get("max", 10**9))
    if word_count < min_words or word_count > max_words:
        errors.append(f"word count {word_count} outside target range {min_words}-{max_words}")
    else:
        checks.append(f"word count {word_count} within target range {min_words}-{max_words}")

    max_characters = int(transport.get("max_characters", 10**9))
    char_count = len(draft)
    if char_count > max_characters:
        errors.append(f"character count {char_count} exceeds max {max_characters}")
    else:
        checks.append(f"character count {char_count} within max {max_characters}")

    readability_errors, readability_checks, readability_flags = validate_readability_dynamics(schema, paragraphs)
    errors.extend(readability_errors)
    checks.extend(readability_checks)
    flags.extend(readability_flags)

    return errors, checks, flags


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--schema", required=True, type=Path, help="Path to text-intent-substrate.yaml")
    parser.add_argument("--draft", required=True, type=Path, help="Path to the draft Markdown file")
    args = parser.parse_args()

    try:
        schema = load_schema(args.schema)
        draft = args.draft.read_text(encoding="utf-8")
        errors, checks, flags = validate(schema, draft)
    except Exception as exc:  # pragma: no cover - command-line guard
        print(f"BLOCK whisper draft validation\n- error: {exc}")
        return 2

    if errors:
        print("BLOCK whisper draft validation")
        for error in errors:
            print(f"- {error}")
        for flag in flags:
            print(f"- flag: {flag}")
        for check in checks:
            print(f"- ok: {check}")
        return 1

    if flags:
        print("FLAG whisper draft validation")
        for flag in flags:
            print(f"- flag: {flag}")
        for check in checks:
            print(f"- ok: {check}")
        return 0

    print("PASS whisper draft validation")
    for check in checks:
        print(f"- ok: {check}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
