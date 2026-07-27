#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
fixture_dir="$script_dir/fixtures/distill-evidence"
wrapper="$script_dir/../scripts/observe-distill-invocation.sh"
temporary_directory="$(mktemp -d)"
trap 'rm -rf "$temporary_directory"' EXIT
observability_dir="$temporary_directory/.arcanum/observability"

complete="$fixture_dir/invoke-distill-telemetry-complete.json"
blocked="$fixture_dir/invoke-distill-telemetry-blocked.json"

complete_output="$("$wrapper" --envelope "$complete" --observability-dir "$observability_dir")"
printf '%s\n' "$complete_output" | rg -q '^OBSERVATION=recorded$'
printf '%s\n' "$complete_output" | rg -q '^PARENT_RUN_ID=invoke-parent-plan-001$'
echo "PASS completed Invoke-to-Distill child signal records"

duplicate_output="$("$wrapper" --envelope "$complete" --observability-dir "$observability_dir")"
printf '%s\n' "$duplicate_output" | rg -q '^OBSERVATION=skipped$'
echo "PASS repeated child run dedupes"

blocked_output="$("$wrapper" --envelope "$blocked" --observability-dir "$observability_dir")"
printf '%s\n' "$blocked_output" | rg -q '^OBSERVATION=recorded$'
echo "PASS blocked Invoke-to-Distill child signal records"

ledger="$observability_dir/signals/sigil-invocations.jsonl"
jq -s -e '
  length == 2
  and all(.[]; .capability.id == "distill")
  and all(.[]; .lineage.relation == "invoked-by")
  and any(.[]; .run_id == "distill-child-complete-001"
    and .lineage.parent_run_id == "invoke-parent-plan-001"
    and .lineage.caller.id == "invoke"
    and .evidence.status == "complete")
  and any(.[]; .run_id == "distill-child-blocked-001"
    and .execution.status == "blocked"
    and .evidence.status == "partial")
' "$ledger" >/dev/null
test "$(wc -l < "$observability_dir/by-sigil/distill.jsonl" | tr -d ' ')" = "2"
echo "PASS central ledger preserves two distinct linked Distill rows"

jq '.lineage.caller.id = "other"' "$complete" > "$temporary_directory/wrong-caller.json"
if "$wrapper" --envelope "$temporary_directory/wrong-caller.json" --observability-dir "$observability_dir" >/dev/null 2>&1; then
	echo "FAIL non-Invoke caller was accepted" >&2
	exit 1
fi
echo "PASS non-Invoke caller blocks"

jq 'del(.lineage.parent_run_id)' "$complete" > "$temporary_directory/missing-parent.json"
if "$wrapper" --envelope "$temporary_directory/missing-parent.json" --observability-dir "$observability_dir" >/dev/null 2>&1; then
	echo "FAIL missing parent run was accepted" >&2
	exit 1
fi
echo "PASS missing parent run blocks"

jq '.execution.status = "skipped"' "$complete" > "$temporary_directory/skipped-child.json"
if "$wrapper" --envelope "$temporary_directory/skipped-child.json" --observability-dir "$observability_dir" >/dev/null 2>&1; then
	echo "FAIL skipped Distill route emitted child telemetry" >&2
	exit 1
fi
echo "PASS skipped Distill route cannot emit child telemetry"

test "$(wc -l < "$ledger" | tr -d ' ')" = "2"
echo "SUMMARY: PASS (7 of 7 checks satisfied expectations)"
echo "AUTHORITY: telemetry is append-only non-authority evidence; child signals do not set Distill verdict or mutation readiness"
