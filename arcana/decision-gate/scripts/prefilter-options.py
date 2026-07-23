#!/usr/bin/env python3
"""Prefilter structurally inadmissible options before Decision Gate."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


PROTECTED_HAZARDS = {
    "destructive",
    "authority",
    "promotion",
    "publication",
    "spend",
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value


def canonical_digest(document: Any) -> str:
    payload = json.dumps(
        document, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def schema_errors(
    document: dict[str, Any], schema: dict[str, Any], label: str
) -> list[str]:
    return [
        f"{label} schema invalid at "
        f"{'/'.join(map(str, error.path)) or '<root>'}: {error.message}"
        for error in sorted(
            Draft202012Validator(schema).iter_errors(document),
            key=lambda item: list(item.path),
        )
    ]


def blocked_receipt(
    request: dict[str, Any], reasons: list[str]
) -> dict[str, Any]:
    return {
        "schemaVersion": "1.0.0",
        "decisionId": request.get("decisionId"),
        "requestDigest": canonical_digest(request),
        "routeOutcome": "block",
        "decisionGateRequired": False,
        "admissibleOptionIds": [],
        "presentedOptionIds": [],
        "directOptionId": None,
        "ownerGate": None,
        "rejectedOptions": [],
        "reasons": sorted(set(reasons)),
    }


def resolve_option_admissibility(
    request: dict[str, Any], request_schema: dict[str, Any]
) -> dict[str, Any]:
    failures = schema_errors(request, request_schema, "admissibility request")
    if failures:
        return blocked_receipt(request, failures)

    option_ids = [item["optionId"] for item in request["candidates"]]
    duplicate_ids = sorted(
        {option_id for option_id in option_ids if option_ids.count(option_id) > 1}
    )
    if duplicate_ids:
        return blocked_receipt(
            request,
            [f"duplicate option id: {option_id}" for option_id in duplicate_ids],
        )

    admissible: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    for candidate in request["candidates"]:
        reasons = list(candidate["rejectionReasons"])
        if candidate["structuralStatus"] == "inadmissible":
            rejected.append(
                {
                    "optionId": candidate["optionId"],
                    "reasons": sorted(set(reasons)),
                }
            )
            continue

        owner_gate_required = (
            candidate["hazardClass"] in PROTECTED_HAZARDS
            or candidate["reversibility"] == "irreversible"
        )
        if owner_gate_required and candidate["ownerGate"] is None:
            rejected.append(
                {
                    "optionId": candidate["optionId"],
                    "reasons": ["protected or irreversible option lacks owner gate"],
                }
            )
            continue
        admissible.append(candidate)

    admissible_ids = sorted(item["optionId"] for item in admissible)
    result = {
        "schemaVersion": "1.0.0",
        "decisionId": request["decisionId"],
        "requestDigest": canonical_digest(request),
        "routeOutcome": "block",
        "decisionGateRequired": False,
        "admissibleOptionIds": admissible_ids,
        "presentedOptionIds": [],
        "directOptionId": None,
        "ownerGate": None,
        "rejectedOptions": sorted(
            rejected, key=lambda item: item["optionId"]
        ),
        "reasons": [],
    }
    if len(admissible) == 0:
        result["reasons"] = ["no structurally admissible option remains"]
    elif len(admissible) == 1:
        result["routeOutcome"] = "direct"
        result["directOptionId"] = admissible[0]["optionId"]
        result["ownerGate"] = admissible[0]["ownerGate"]
    else:
        result["routeOutcome"] = "gate"
        result["decisionGateRequired"] = True
        result["presentedOptionIds"] = admissible_ids
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("request")
    parser.add_argument("--request-schema", required=True)
    parser.add_argument("--receipt-schema", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()

    request = load_json(Path(args.request))
    request_schema = load_json(Path(args.request_schema))
    receipt_schema = load_json(Path(args.receipt_schema))
    result = resolve_option_admissibility(request, request_schema)
    receipt_failures = schema_errors(
        result, receipt_schema, "admissibility receipt"
    )
    if receipt_failures:
        raise ValueError("; ".join(receipt_failures))
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0 if result["routeOutcome"] in ("direct", "gate") else 1


if __name__ == "__main__":
    raise SystemExit(main())
