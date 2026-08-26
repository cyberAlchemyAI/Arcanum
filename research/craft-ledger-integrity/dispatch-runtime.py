#!/usr/bin/env python3
"""Local deterministic gates and append-only registrar for this research dispatch."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def resolve(repo_root: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else repo_root / path


def material_projection(sheet: dict) -> dict:
    return sheet.get("governance", {}).get("material_strategy", {})


def validate_agent_pool(pool_path: Path, agents: list[dict]) -> list[str]:
    errors: list[str] = []
    pool_text = pool_path.read_text(encoding="utf-8")
    identities = [agent.get("agent_name") for agent in agents]
    if len(identities) != len(set(identities)):
        errors.append("agent identities are not unique")
    for agent in agents:
        identity = agent.get("agent_name", "")
        role = agent.get("role", "")
        marker = f'name: "{identity}"'
        start = pool_text.find(marker)
        if start < 0:
            errors.append(f"agent is absent from pool: {identity}")
            continue
        next_start = pool_text.find("\n  - name:", start + len(marker))
        block = pool_text[start : next_start if next_start >= 0 else len(pool_text)]
        if f"role_fit: [{role}" not in block and f", {role}" not in block:
            errors.append(f"agent role is not admitted by pool: {identity} -> {role}")
    return errors


def validate_pair_coverage(material: dict) -> list[str]:
    errors: list[str] = []
    subject_groups = 0
    angle_by_id = {agent.get("agent_id"): agent.get("angle", "") for agent in material.get("agents", [])}
    for group in material.get("groups", []):
        members = group.get("agent_ids", [])
        if group.get("n") != len(members):
            errors.append(f"declared group size mismatch in {group.get('group_id')}")
        role = group.get("role")
        if role not in {"investigate", "evaluate", "synthesize", "meta-evaluate"}:
            errors.append(f"invalid group role in {group.get('group_id')}: {role}")
        if len(members) < 2:
            continue
        if role in {"investigate", "evaluate"}:
            subject_groups += 1
        anti_bias = group.get("anti_bias", "")
        if not any(axis in anti_bias for axis in ("methodology", "source-corpus", "attack-vector", "temporal-prior")):
            errors.append(f"noncanonical anti-bias axis in {group.get('group_id')}")
        for member in members:
            if not angle_by_id.get(member, "").strip():
                errors.append(f"missing agent angle for {member}")
        expected = {tuple(sorted(pair)) for pair in itertools.combinations(members, 2)}
        observed: set[tuple[str, str]] = set()
        for record in group.get("predicted_disagreements", []):
            pair = record.get("agents", [])
            sentence = record.get("sentence", "")
            if len(pair) != 2 or not sentence.strip():
                errors.append(f"invalid predicted disagreement in group {group.get('group_id')}")
                continue
            observed.add(tuple(sorted(pair)))
        if expected != observed:
            errors.append(
                f"pairwise tension coverage mismatch in {group.get('group_id')}: "
                f"expected={sorted(expected)} observed={sorted(observed)}"
            )
    if subject_groups >= 2 and not material.get("anti_bias_global", "").strip():
        errors.append("anti_bias_global is required for two or more subject groups")
    return errors


def readiness(profile_path: Path, sheet_path: Path) -> tuple[dict, int]:
    profile = load_json(profile_path)
    sheet = load_json(sheet_path)
    repo_root = Path(profile["repository_root"])
    errors: list[str] = []

    dispatch_type = sheet.get("mode")
    type_config = profile.get("dispatch_types", {}).get(dispatch_type)
    if not type_config or type_config.get("status") != "live":
        errors.append(f"dispatch type is not live: {dispatch_type}")
    elif not resolve(repo_root, type_config["owner_capability"]).is_file():
        errors.append("research owner capability is missing")

    baseline = sheet.get("governance", {}).get("preflight", {})
    baseline_path = resolve(repo_root, baseline.get("baseline_path", ""))
    if not baseline_path.is_file():
        errors.append("validated baseline is missing")
    elif sha256_file(baseline_path) != baseline.get("baseline_sha256"):
        errors.append("validated baseline digest does not match the sheet")

    material = material_projection(sheet)
    if not material:
        errors.append("material strategy projection is absent from sheet bytes")
    projection_path = resolve(repo_root, profile["material_confirmation"]["projection_artifact"])
    if not projection_path.is_file():
        errors.append("persisted material projection is missing")
    else:
        projection = load_json(projection_path)
        if canonical_bytes(projection) != canonical_bytes(material):
            errors.append("persisted material projection differs from exact sheet material")

    agents = material.get("agents", [])
    pool_path = resolve(repo_root, profile["agent_pool"]["source"])
    if not pool_path.is_file():
        errors.append("agent pool is missing")
    else:
        errors.extend(validate_agent_pool(pool_path, agents))
    errors.extend(validate_pair_coverage(material))

    if material.get("final_approver") != "parent":
        errors.append("this profile admits only parent as final approver")
    if sheet.get("subagent_strategy", {}).get("authorization") != "requires_user_permission":
        errors.append("pre-confirmation sheet must require user permission")

    publication = material.get("publication", {})
    working_folder = material.get("working_folder", "")
    if working_folder not in publication.get("public_paths", []):
        errors.append("working folder is absent from public publication paths")
    if publication.get("private_paths"):
        errors.append("private publication paths are not admitted for this dispatch")

    validator = resolve(repo_root, profile["form_owner"]["validator_script"])
    completed = subprocess.run(
        [sys.executable, str(validator), str(sheet_path), "--json"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    try:
        dispatch_validation = json.loads(completed.stdout)
    except json.JSONDecodeError:
        dispatch_validation = {"status": "block", "stdout": completed.stdout, "stderr": completed.stderr}
    if completed.returncode != 0 or dispatch_validation.get("status") == "block":
        errors.append("dispatch-spec validation blocked")

    sheet_digest = sha256_file(sheet_path)
    projection_digest = sha256_bytes(canonical_bytes(material)) if material else None
    result = {
        "status": "pass" if not errors else "block",
        "profile_id": profile.get("profile_id"),
        "profile_version": profile.get("version"),
        "schema_version": profile["form_owner"].get("schema_version"),
        "sheet_sha256": sheet_digest,
        "material_projection_sha256": projection_digest,
        "baseline_sha256": baseline.get("baseline_sha256"),
        "dispatch_validation": dispatch_validation,
        "errors": errors,
    }
    return result, 0 if not errors else 1


def append_event(profile_path: Path, sheet_path: Path, event_type: str, confirmation: str | None, result_ref: str | None) -> tuple[dict, int]:
    ready, ready_code = readiness(profile_path, sheet_path)
    if ready_code:
        return ready, ready_code
    profile = load_json(profile_path)
    sheet = load_json(sheet_path)
    repo_root = Path(profile["repository_root"])
    ledger_path = resolve(repo_root, profile["registration"]["ledger"])
    prior: list[dict] = []
    if ledger_path.exists():
        prior = [json.loads(line) for line in ledger_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    dispatch_id = sheet["dispatch_id"]
    dispatch_events = [e for e in prior if e.get("dispatch_id") == dispatch_id and e.get("event_type") == "dispatch"]
    close_events = [e for e in prior if e.get("dispatch_id") == dispatch_id and e.get("event_type") == "close"]
    if event_type == "dispatch":
        if not confirmation:
            return {"status": "block", "errors": ["explicit confirmation evidence is required"]}, 1
        if dispatch_events:
            return {"status": "block", "errors": ["dispatch event already exists"]}, 1
    elif event_type == "close":
        if len(dispatch_events) != 1 or close_events:
            return {"status": "block", "errors": ["close requires exactly one open dispatch event"]}, 1
        if not result_ref:
            return {"status": "block", "errors": ["close requires a result reference"]}, 1
    else:
        return {"status": "block", "errors": [f"unsupported event type: {event_type}"]}, 1

    event = {
        "event_type": event_type,
        "dispatch_id": dispatch_id,
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "profile_id": profile["profile_id"],
        "sheet_sha256": ready["sheet_sha256"],
        "material_projection_sha256": ready["material_projection_sha256"],
    }
    if confirmation:
        event["confirmation"] = confirmation
    if result_ref:
        event["result_ref"] = result_ref
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    with ledger_path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
    return {"status": "pass", "ledger": str(ledger_path), "event": event}, 0


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    ready_parser = subparsers.add_parser("readiness")
    ready_parser.add_argument("profile", type=Path)
    ready_parser.add_argument("sheet", type=Path)
    register_parser = subparsers.add_parser("register")
    register_parser.add_argument("profile", type=Path)
    register_parser.add_argument("sheet", type=Path)
    register_parser.add_argument("--confirmation", required=True)
    close_parser = subparsers.add_parser("close")
    close_parser.add_argument("profile", type=Path)
    close_parser.add_argument("sheet", type=Path)
    close_parser.add_argument("--result-ref", required=True)
    args = parser.parse_args()

    if args.command == "readiness":
        result, code = readiness(args.profile.resolve(), args.sheet.resolve())
    elif args.command == "register":
        result, code = append_event(args.profile.resolve(), args.sheet.resolve(), "dispatch", args.confirmation, None)
    else:
        result, code = append_event(args.profile.resolve(), args.sheet.resolve(), "close", None, args.result_ref)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
