#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/../../../../" && pwd)"

python3 - "$repo_root" <<'PY'
import hashlib
import json
import pathlib
import sys

repo_root = pathlib.Path(sys.argv[1])
status_path = repo_root / "projects/ide-extension/development/manual-session-bridge-plan/work-pack/evidence/SWU-DEE-013-SUPERSEDING-STATUS.json"
craft_path = repo_root / "projects/ide-extension/.craft/ledger.yml"
target_path = repo_root / "projects/ide-extension/development/workbench-ui-v1/work-pack/tasks/TASK-WUI-001-SHELL.md"
history_path = repo_root / (
    "projects/ide-extension/development/manual-session-bridge-plan/work-pack/evidence/"
    "SWU-MSB-011-assets/runtime-artifacts/artifact-run-61e2f724-fd9a-49a9-ad70-3c0a00fbe947-"
    "receipt-816aacd8-4619-472c-b963-bf9920dbe1ed-execution-receipt.json"
)
observability_path = repo_root / ".arcanum/observability/by-sigil/invoke.jsonl"
status = json.loads(status_path.read_text(encoding="utf-8"))
history_bytes = history_path.read_bytes()
history_sha256 = hashlib.sha256(history_bytes).hexdigest()
failures = []

if status["predecessor"]["replay_result"].endswith("SWU-DEE-012-RESULT.md") and status["workbench"]["replay_status"] == "pass":
    print("PASS superseding record binds the passing DEE-012 replay")
else:
    failures.append("superseding record does not bind a passing DEE-012 replay")

if (
    history_sha256 == status["predecessor"]["historical_sha256"]
    and len(history_bytes) == status["predecessor"]["historical_size_bytes"]
    and status["history_mutation"] == "none"
):
    print("PASS historical predecessor digest and no-rewrite policy agree")
else:
    failures.append("historical predecessor changed or no-rewrite policy missing")

craft_text = craft_path.read_text(encoding="utf-8")
target_text = target_path.read_text(encoding="utf-8")
if "SWU-WUI-001" in craft_text and "next_move:" in craft_text and target_path.is_file():
    print("PASS Craft ledger and WUI-001 target exist")
else:
    failures.append("Craft continuation target is not available")

continuation = status["continuation"]
if (
    continuation["status"] == "ready"
    and continuation["capability"] == "task-session"
    and continuation["target"].endswith("TASK-WUI-001-SHELL.md")
    and continuation["mutation_handoff_allowed"] is False
    and "SWU-WUI-001" in target_text
):
    print("PASS continuation route derives task-session WUI-001 without mutation authority")
else:
    failures.append("continuation route is missing, stale, or overclaims authority")

observability_rows = []
for line in observability_path.read_text(encoding="utf-8").splitlines():
    if line.strip():
        observability_rows.append(json.loads(line))
matching_rows = [row for row in observability_rows if row.get("run_id") == status["observability_run_id"]]
if len(matching_rows) == 1:
    print("PASS one append-only Invoke observability row records the closeout")
else:
    failures.append(f"expected one closeout observability row, found {len(matching_rows)}")

continuation_path = repo_root / "projects/ide-extension/development/manual-session-bridge-plan/work-pack/evidence/SWU-DEE-013-CRAFT-CONTINUATION.md"
if status["workbench"]["swu_count"] == 11 and "eleven" in continuation_path.read_text(encoding="utf-8"):
    print("PASS superseding continuation has explicit eleven-SWU status")
else:
    failures.append("superseding continuation does not state the complete eleven-SWU result")

if failures:
    print("SUMMARY: FAIL")
    for failure in failures:
        print(f"- {failure}")
    raise SystemExit(1)

print("SUMMARY: PASS (6 checks satisfied expectations)")
print("AUTHORITY: route synchronization is append-only and does not authorize code mutation")
PY
