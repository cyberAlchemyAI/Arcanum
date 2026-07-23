#!/usr/bin/env python3
"""Validate and consume one Decision Gate override under an exclusive lock."""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath, PureWindowsPath
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


def digest(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def parse_timestamp(value: str, label: str) -> tuple[datetime | None, str | None]:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None, f"{label} is not an ISO-8601 timestamp"
    if parsed.tzinfo is None:
        return None, f"{label} must include a timezone"
    return parsed.astimezone(timezone.utc), None


def normalize_scope(scope: list[str]) -> tuple[list[str], list[str]]:
    normalized: list[str] = []
    errors: list[str] = []
    for raw_path in scope:
        candidate = raw_path.replace("\\", "/")
        posix_path = PurePosixPath(candidate)
        if (
            not candidate
            or posix_path.is_absolute()
            or PureWindowsPath(raw_path).is_absolute()
            or ".." in posix_path.parts
        ):
            errors.append(f"scope path escape: {raw_path}")
            continue
        cleaned = str(posix_path)
        if cleaned in ("", "."):
            errors.append(f"scope path escape: {raw_path}")
            continue
        normalized.append(cleaned)
    if len(set(normalized)) != len(normalized):
        errors.append("normalized scope contains duplicate paths")
    return sorted(normalized), sorted(set(errors))


def blocked_receipt(
    override: dict[str, Any] | None,
    before_digest: str | None,
    reasons: list[str],
    owner_route_required: bool = False,
) -> dict[str, Any]:
    return {
        "schema_version": "1.0.0",
        "override_id": override.get("override_id") if override else None,
        "verdict": "block",
        "consumed_by": override.get("consumed_by") if override else None,
        "target": override.get("target") if override else None,
        "scope": sorted(
            {
                item
                for item in (override.get("scope", []) if override else [])
                if isinstance(item, str) and item
            }
        ),
        "hazard_class": override.get("hazard_class") if override else None,
        "owner_gate_receipt": (
            override.get("owner_gate_receipt") if override else None
        ),
        "owner_route_required": owner_route_required,
        "override_digest_before": before_digest,
        "override_digest_after": before_digest,
        "consumed_at": None,
        "reasons": sorted(set(reasons)),
    }


def consume_override(
    override_path: Path,
    request: dict[str, Any],
    request_schema: dict[str, Any],
    override_schema: dict[str, Any],
    now: datetime | None = None,
) -> dict[str, Any]:
    request_failures = schema_errors(
        request, request_schema, "override consumption request"
    )
    if request_failures:
        return blocked_receipt(None, None, request_failures)
    if not override_path.is_file():
        return blocked_receipt(
            None, None, [f"override artifact missing: {override_path}"]
        )

    observed_at = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    with override_path.open("r+", encoding="utf-8") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        handle.seek(0)
        before_content = handle.read().encode("utf-8")
        before_digest = digest(before_content)
        try:
            override = json.loads(before_content)
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            return blocked_receipt(
                None,
                before_digest,
                [f"override artifact is not valid JSON: {error}"],
            )
        if not isinstance(override, dict):
            return blocked_receipt(
                None, before_digest, ["override artifact must be a JSON object"]
            )

        failures = schema_errors(override, override_schema, "override")
        if failures:
            return blocked_receipt(override, before_digest, failures)

        override_scope, scope_errors = normalize_scope(override["scope"])
        request_scope, request_scope_errors = normalize_scope(request["scope"])
        failures.extend(scope_errors)
        failures.extend(request_scope_errors)
        if override["target"] != request["target"]:
            failures.append("override target mismatch")
        if override_scope != request_scope:
            failures.append("override scope mismatch")
        if override["hazard_class"] != request["hazard_class"]:
            failures.append("override hazard class mismatch")
        if override["consumed_by"] is not None:
            failures.append("override already consumed")

        issued_at, issued_error = parse_timestamp(
            override["issued_at"], "issued_at"
        )
        if issued_error:
            failures.append(issued_error)
        elif issued_at is not None and issued_at > observed_at:
            failures.append("override issued_at is in the future")
        expires_at: datetime | None = None
        if override["expires_at"] is not None:
            expires_at, expires_error = parse_timestamp(
                override["expires_at"], "expires_at"
            )
            if expires_error:
                failures.append(expires_error)
            elif expires_at is not None and observed_at >= expires_at:
                failures.append("override is stale")
        if (
            issued_at is not None
            and expires_at is not None
            and expires_at <= issued_at
        ):
            failures.append("override expiry does not follow issuance")

        protected = override["hazard_class"] in PROTECTED_HAZARDS
        if protected:
            if override["owner_gate_receipt"] is None:
                failures.append("protected hazard lacks owner gate receipt")
            failures.append(
                "protected hazard requires owner-specific gate admission"
            )

        failures = sorted(set(failures))
        if failures:
            return blocked_receipt(
                override,
                before_digest,
                failures,
                owner_route_required=protected,
            )

        override["consumed_by"] = request["run_id"]
        rendered = json.dumps(override, indent=2, sort_keys=True) + "\n"
        handle.seek(0)
        handle.write(rendered)
        handle.truncate()
        handle.flush()
        os.fsync(handle.fileno())
        after_digest = digest(rendered.encode("utf-8"))
        return {
            "schema_version": "1.0.0",
            "override_id": override["override_id"],
            "verdict": "consumed",
            "consumed_by": request["run_id"],
            "target": override["target"],
            "scope": override_scope,
            "hazard_class": override["hazard_class"],
            "owner_gate_receipt": override["owner_gate_receipt"],
            "owner_route_required": False,
            "override_digest_before": before_digest,
            "override_digest_after": after_digest,
            "consumed_at": observed_at.isoformat().replace("+00:00", "Z"),
            "reasons": [],
        }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("override")
    parser.add_argument("request")
    parser.add_argument("--override-schema", required=True)
    parser.add_argument("--request-schema", required=True)
    parser.add_argument("--receipt-schema", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()

    result = consume_override(
        Path(args.override),
        load_json(Path(args.request)),
        load_json(Path(args.request_schema)),
        load_json(Path(args.override_schema)),
    )
    receipt_failures = schema_errors(
        result,
        load_json(Path(args.receipt_schema)),
        "override consumption receipt",
    )
    if receipt_failures:
        raise ValueError("; ".join(receipt_failures))
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0 if result["verdict"] == "consumed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
