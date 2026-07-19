#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/../../../../" && pwd)"

python3 - "$repo_root" <<'PY'
import hashlib
import json
import pathlib
import re
import subprocess
import sys

repo_root = pathlib.Path(sys.argv[1])
plan_root = repo_root / "projects/ide-extension/development/manual-session-bridge-plan"
work_pack = plan_root / "WORK-PACK.md"
evidence_root = plan_root / "work-pack/evidence"
required_artifacts = [
    "WORK-PACK.md",
    "DISTILL-VALIDATION.md",
    "IMPLEMENTATION-LAYERING.md",
    "EXECUTION-PACK.md",
    "INVOKE-RESULT.md",
    "PLAN-TRANSPORT.md",
    "manual-session-bridge-plan.dispatch.json",
]
historical_root = evidence_root / "SWU-MSB-011-assets/runtime-artifacts"
historical_execution = historical_root / (
    "artifact-run-61e2f724-fd9a-49a9-ad70-3c0a00fbe947-"
    "receipt-816aacd8-4619-472c-b963-bf9920dbe1ed-execution-receipt.json"
)
historical_result = historical_root / (
    "artifact-run-61e2f724-fd9a-49a9-ad70-3c0a00fbe947-"
    "receipt-816aacd8-4619-472c-b963-bf9920dbe1ed-result.json"
)
historical_after = historical_root / (
    "artifact-run-61e2f724-fd9a-49a9-ad70-3c0a00fbe947-"
    "receipt-816aacd8-4619-472c-b963-bf9920dbe1ed-after.json"
)
failures = []

for relative_path in required_artifacts:
    if not (plan_root / relative_path).is_file():
        failures.append(f"missing Workbench artifact: {relative_path}")

rows = re.findall(
    r"^\| (SWU-MSB-\d{3}) \|.*?\| \[PASS[^\]]*\]\(([^)]+)\) \|",
    work_pack.read_text(encoding="utf-8"),
    flags=re.MULTILINE,
)
swu_ids = [row[0] for row in rows]
expected_ids = [f"SWU-MSB-{index:03d}" for index in range(1, 12)]
if swu_ids != expected_ids or len(set(swu_ids)) != 11:
    failures.append(f"expected eleven ordered unique SWUs, got {swu_ids}")
else:
    print("PASS current Workbench manifest resolves eleven ordered SWUs")

for swu_id, result_ref in rows:
    if not (plan_root / result_ref).is_file():
        failures.append(f"{swu_id}: missing result {result_ref}")
if not failures:
    print("PASS every SWU result reference resolves")

distill_text = (plan_root / "DISTILL-VALIDATION.md").read_text(encoding="utf-8")
for marker in ("## Role Conversation Trace", "## Recomposition Proof", "| Verdict | pass |"):
    if marker not in distill_text:
        failures.append(f"missing Distill process evidence: {marker}")
if not failures:
    print("PASS Distill role/process and recomposition evidence resolves")

parsed_count = 0
for path in sorted(evidence_root.rglob("*")):
    if path.suffix not in {".json", ".jsonl"}:
        continue
    try:
        if path.suffix == ".json":
            json.loads(path.read_text(encoding="utf-8"))
        else:
            for line in path.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    json.loads(line)
        parsed_count += 1
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        failures.append(f"invalid evidence JSON: {path}: {error}")
if not failures:
    print(f"PASS checked-in JSON/JSONL evidence parses ({parsed_count} files)")

historical_documents = [
    json.loads(path.read_text(encoding="utf-8"))
    for path in (historical_execution, historical_result, historical_after)
]
if not all(path.is_file() for path in (historical_execution, historical_result, historical_after)):
    failures.append("historical MSB-011 predecessor artifacts are incomplete")
else:
    execution, result, after = historical_documents
    identities = {
        execution["run_id"], result["run_id"], after["run_id"],
        execution["envelope_id"], result["envelope_id"], after["envelope_id"],
        execution["claim_id"], result["claim_id"], after["claim_id"],
    }
    if len(identities) != 3:
        failures.append("historical approval/claim/result identity disagreement")
    if execution["kind"] != "bridge.execution.receipt" or result["kind"] != "bridge.result":
        failures.append("historical terminal artifact kinds are not bridge execution/result")
    if after["state"] != result["result"]["status"]:
        failures.append("historical after state disagrees with result status")
    else:
        print("PASS historical approval/claim/execution/result identity agrees")

predecessor_bytes = historical_execution.read_bytes()
predecessor_sha256 = hashlib.sha256(predecessor_bytes).hexdigest()
predecessor_size = len(predecessor_bytes)
print(f"PASS historical predecessor preserved: sha256={predecessor_sha256} size_bytes={predecessor_size}")

test = subprocess.run(
    ["npm", "--prefix", str(repo_root / "projects/ide-extension"), "run", "test:bridge-replay"],
    cwd=repo_root,
    text=True,
    capture_output=True,
)
if test.returncode != 0:
    failures.append(f"focused Workbench replay test failed: {test.stdout}\n{test.stderr}")
else:
    print("PASS focused Workbench replay Node test")

if failures:
    print("SUMMARY: FAIL")
    for failure in failures:
        print(f"- {failure}")
    raise SystemExit(1)

print("SUMMARY: PASS (6 checks satisfied expectations)")
print(json.dumps({
    "status": "pass",
    "authority": "replay_evidence_only",
    "swu_count": 11,
    "evidence_files_parsed": parsed_count,
    "predecessor": {
        "path": str(historical_execution.relative_to(repo_root)),
        "sha256": predecessor_sha256,
        "size_bytes": predecessor_size,
    },
    "mutation_handoff_allowed": False,
    "next_route": "task-session",
}, sort_keys=True))
PY
