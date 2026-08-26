#!/usr/bin/env python3
"""Validate lens_packet structure and cross-field semantics."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator
except ModuleNotFoundError as exc:
    if exc.name != "jsonschema":
        raise
    requirement = Path(__file__).resolve().parents[1] / "requirements.txt"
    print(
        "missing runtime dependency 'jsonschema'; install the declared requirement "
        f"with: python -m pip install -r {requirement}",
        file=sys.stderr,
    )
    raise SystemExit(3) from exc


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "references" / "lens-packet.schema.json"
SUPPORTED_WITHOUT_EVIDENCE = {"product-direction", "hypothesis", "open-question"}


def packet_digest(packet: dict[str, Any]) -> str:
    """Return the canonical digest binding every packet field except itself."""
    payload = copy.deepcopy(packet)
    payload.pop("packet_digest", None)
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(canonical).hexdigest()


def _valid_json_pointer(pointer: str) -> bool:
    if pointer == "":
        return True
    if not pointer.startswith("/"):
        return False
    index = 0
    while index < len(pointer):
        if pointer[index] == "~":
            if index + 1 >= len(pointer) or pointer[index + 1] not in "01":
                return False
            index += 2
        else:
            index += 1
    return True


def _inside_boundary(reference: str, boundary: dict[str, Any]) -> bool:
    locator = boundary["locator"]
    scope = boundary["scope"]
    kind = scope["kind"]
    if kind == "exact-locator":
        return reference == locator
    if kind == "line-range":
        prefix = locator + ":"
        if not reference.startswith(prefix):
            return False
        suffix = reference[len(prefix) :]
        if not suffix.isascii() or not suffix.isdigit() or suffix.startswith("0"):
            return False
        line = int(suffix)
        return scope["start_line"] <= line <= scope["end_line"]
    if kind == "json-pointer-prefix":
        prefix = locator + "#"
        if not reference.startswith(prefix):
            return False
        pointer = reference[len(prefix) :]
        if not _valid_json_pointer(pointer):
            return False
        allowed = scope["pointer"]
        return (
            pointer == allowed
            or (allowed == "" and pointer.startswith("/"))
            or pointer.startswith(allowed + "/")
        )
    if kind == "whole-resource":
        if reference == locator:
            return True
        line_prefix = locator + ":"
        if reference.startswith(line_prefix):
            suffix = reference[len(line_prefix) :]
            return suffix.isascii() and suffix.isdigit() and not suffix.startswith("0")
        pointer_prefix = locator + "#"
        return reference.startswith(pointer_prefix) and _valid_json_pointer(
            reference[len(pointer_prefix) :]
        )
    return False


def validate_packet(packet: Any) -> list[str]:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    errors = [
        "schema: " + error.message
        for error in sorted(
            Draft202012Validator(schema).iter_errors(packet),
            key=lambda item: list(item.absolute_path),
        )
    ]
    if errors or not isinstance(packet, dict):
        return errors

    expected_digest = packet_digest(packet)
    if packet["packet_digest"] != expected_digest:
        errors.append(
            "semantic: packet_digest does not match the canonical packet content"
        )

    selected = packet["selected_lenses"]
    selected_set = set(selected)
    rationale_lenses = [item["lens"] for item in packet["selection_rationale"]]
    if Counter(rationale_lenses) != Counter(selected):
        errors.append("semantic: require exactly one rationale for every selected lens")

    findings = packet["per_lens_findings"]
    finding_lenses: dict[str, str] = {}
    findings_by_lens: defaultdict[str, int] = defaultdict(int)
    all_ids: list[str] = []
    boundaries = packet["evidence_boundary"]
    for boundary in boundaries:
        scope = boundary["scope"]
        if (
            scope["kind"] == "line-range"
            and scope["start_line"] > scope["end_line"]
        ):
            errors.append(
                f"semantic: evidence boundary {boundary['locator']!r} has start_line after end_line"
            )

    for finding in findings:
        finding_id = finding["id"]
        all_ids.append(finding_id)
        finding_lenses[finding_id] = finding["lens"]
        findings_by_lens[finding["lens"]] += 1
        if finding["lens"] not in selected_set:
            errors.append(
                f"semantic: finding {finding_id} uses unselected lens {finding['lens']}"
            )
        for reference in finding["evidence_refs"]:
            if not any(_inside_boundary(reference, boundary) for boundary in boundaries):
                errors.append(
                    f"semantic: finding {finding_id} evidence {reference!r} is outside evidence_boundary"
                )
        if (
            finding["status"] in SUPPORTED_WITHOUT_EVIDENCE
            and not finding["evidence_refs"]
            and not finding["uncertainty"]
        ):
            errors.append(
                f"semantic: unsupported finding {finding_id} must preserve its limitation in uncertainty"
            )

    for lens in selected:
        if findings_by_lens[lens] == 0:
            errors.append(f"semantic: selected lens {lens} has no finding")

    composed = packet["composed_findings"]
    for relation in composed:
        relation_id = relation["id"]
        all_ids.append(relation_id)
        missing = [item for item in relation["finding_ids"] if item not in finding_lenses]
        if missing:
            errors.append(
                f"semantic: composition {relation_id} has unresolved finding IDs {missing}"
            )
        else:
            contributor_lenses = {finding_lenses[item] for item in relation["finding_ids"]}
            if len(contributor_lenses) < 2:
                errors.append(
                    f"semantic: composition {relation_id} must join findings from different lenses"
                )
        for reference in relation["evidence_refs"]:
            if not any(_inside_boundary(reference, boundary) for boundary in boundaries):
                errors.append(
                    f"semantic: composition {relation_id} evidence {reference!r} is outside evidence_boundary"
                )

    duplicates = sorted(item for item, count in Counter(all_ids).items() if count > 1)
    if duplicates:
        errors.append(f"semantic: IDs must be unique; duplicates: {duplicates}")

    if len(selected) == 1 and composed:
        errors.append("semantic: one-lens packet must have empty composed_findings")

    expected_checks = {
        "claim-status-language",
        "evidence-authority-permission",
        "lens-forbidden-jumps",
    }
    audits = packet["qualitative_audit"]
    audit_checks = [item["check"] for item in audits]
    if Counter(audit_checks) != Counter(expected_checks):
        errors.append("semantic: require exactly one record for every qualitative audit check")
    expected_reviewed_ids = set(all_ids)
    for audit in audits:
        if set(audit["reviewed_ids"]) != expected_reviewed_ids:
            errors.append(
                f"semantic: qualitative audit {audit['check']} must cover every finding ID"
            )

    return errors


def _valid_fixture() -> dict[str, Any]:
    packet = {
        "packet_version": "2.0",
        "packet_digest": "sha256:" + "0" * 64,
        "object": "candidate skill",
        "consumer": "maintainer",
        "purpose": "understand the routing contract",
        "evidence_boundary": [
            {
                "locator": "artifact.md",
                "scope": {"kind": "line-range", "start_line": 1, "end_line": 30},
            }
        ],
        "known_terms": ["skill"],
        "reserved_terms": ["evidence"],
        "selected_lenses": ["epistemic", "systemic"],
        "selection_rationale": [
            {
                "lens": "epistemic",
                "trigger": "claim support matters",
                "reason": "separate evidence from authority",
            },
            {
                "lens": "systemic",
                "trigger": "state transition matters",
                "reason": "trace downstream effects",
            },
        ],
        "per_lens_findings": [
            {
                "id": "E1",
                "lens": "epistemic",
                "statement": "The artifact states a route.",
                "status": "observed-implemented",
                "evidence_refs": ["artifact.md:10"],
                "materiality": "Changes whether the route is supported.",
                "uncertainty": None,
            },
            {
                "id": "S1",
                "lens": "systemic",
                "statement": "The route changes the next callable skill.",
                "status": "supported-interpretation",
                "evidence_refs": ["artifact.md:20"],
                "materiality": "Changes downstream execution.",
                "uncertainty": None,
            },
        ],
        "composed_findings": [
            {
                "id": "C1",
                "kind": "dependency",
                "finding_ids": ["E1", "S1"],
                "statement": "The supported route constrains the next transition.",
                "evidence_refs": [],
                "uncertainty": None,
            }
        ],
        "qualitative_audit": [
            {
                "check": "claim-status-language",
                "status": "pass",
                "reviewed_ids": ["E1", "S1", "C1"],
                "note": "Claim language matches recorded status.",
            },
            {
                "check": "evidence-authority-permission",
                "status": "pass",
                "reviewed_ids": ["E1", "S1", "C1"],
                "note": "No evidence was treated as authority or permission.",
            },
            {
                "check": "lens-forbidden-jumps",
                "status": "pass",
                "reviewed_ids": ["E1", "S1", "C1"],
                "note": "Selected lens forbidden jumps were reapplied.",
            },
        ],
        "open_questions": [],
    }
    packet["packet_digest"] = packet_digest(packet)
    return packet


def self_test() -> None:
    valid = _valid_fixture()
    assert valid["packet_digest"] == (
        "sha256:aabd9e2760030b715aefe3507e50d95f0cca9a9ebd77241dfe782a7937b741f3"
    )
    assert not validate_packet(valid), validate_packet(valid)

    def expect_invalid(case: dict[str, Any], expected: str, *, redigest: bool = True) -> None:
        if redigest:
            case["packet_digest"] = packet_digest(case)
        errors = validate_packet(case)
        assert any(expected in error for error in errors), errors

    case = copy.deepcopy(valid)
    case["selection_rationale"][1]["lens"] = "epistemic"
    expect_invalid(case, "exactly one rationale")
    case = copy.deepcopy(valid)
    case["per_lens_findings"] = case["per_lens_findings"][:1]
    case["composed_findings"] = []
    expect_invalid(case, "has no finding")
    case = copy.deepcopy(valid)
    case["per_lens_findings"][1]["id"] = "E1"
    expect_invalid(case, "IDs must be unique")
    case = copy.deepcopy(valid)
    case["composed_findings"][0]["finding_ids"][1] = "MISSING"
    expect_invalid(case, "unresolved finding IDs")
    case = copy.deepcopy(valid)
    case["per_lens_findings"][0]["evidence_refs"] = ["outside.md:1"]
    expect_invalid(case, "outside evidence_boundary")
    case = copy.deepcopy(valid)
    case["composed_findings"][0]["finding_ids"] = ["E1", "E1"]
    expect_invalid(case, "schema:")
    case = copy.deepcopy(valid)
    case["per_lens_findings"][0].update(
        status="hypothesis", evidence_refs=[], uncertainty=None
    )
    expect_invalid(case, "must preserve its limitation")
    case = copy.deepcopy(valid)
    case["qualitative_audit"][0]["reviewed_ids"] = ["E1"]
    expect_invalid(case, "must cover every finding ID")
    case = copy.deepcopy(valid)
    case["consumer"] = "different consumer"
    expect_invalid(case, "packet_digest", redigest=False)
    case = copy.deepcopy(valid)
    case["per_lens_findings"][0]["evidence_refs"] = ["artifact.md:999"]
    expect_invalid(case, "outside evidence_boundary")
    case = copy.deepcopy(valid)
    case["evidence_boundary"][0]["scope"]["start_line"] = 31
    expect_invalid(case, "start_line after end_line")

    for scope, references in [
        ({"kind": "whole-resource"}, ["artifact.md:10", "artifact.md:20"]),
        ({"kind": "exact-locator"}, ["artifact.md", "artifact.md"]),
        (
            {"kind": "json-pointer-prefix", "pointer": "/routes"},
            ["artifact.md#/routes/low", "artifact.md#/routes/high"],
        ),
    ]:
        case = copy.deepcopy(valid)
        case["evidence_boundary"][0]["scope"] = scope
        case["per_lens_findings"][0]["evidence_refs"] = [references[0]]
        case["per_lens_findings"][1]["evidence_refs"] = [references[1]]
        case["packet_digest"] = packet_digest(case)
        assert not validate_packet(case), validate_packet(case)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", nargs="?", help="JSON file or - for stdin")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--emit-valid-fixture", action="store_true")
    parser.add_argument(
        "--compute-digest",
        action="store_true",
        help="print the canonical digest for the supplied packet without validating it",
    )
    args = parser.parse_args()

    if args.self_test:
        self_test()
        print("lens packet validator self-test: PASS")
        return 0
    if args.emit_valid_fixture:
        print(json.dumps(_valid_fixture(), indent=2, ensure_ascii=False))
        return 0
    if not args.packet:
        parser.error("packet path or --self-test is required")

    try:
        raw = sys.stdin.read() if args.packet == "-" else Path(args.packet).read_text(encoding="utf-8")
        packet = json.loads(raw)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"input: {exc}", file=sys.stderr)
        return 2

    if args.compute_digest:
        if not isinstance(packet, dict):
            print("input: packet must be a JSON object", file=sys.stderr)
            return 2
        print(packet_digest(packet))
        return 0

    errors = validate_packet(packet)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("lens packet: VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
