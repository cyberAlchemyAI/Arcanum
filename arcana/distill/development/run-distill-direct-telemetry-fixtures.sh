#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
wrapper="$script_dir/../scripts/observe-direct-invocation.sh"
fixture="$script_dir/fixtures/direct-telemetry/direct-not-required.json"
temporary_directory="$(mktemp -d)"
trap 'rm -rf "$temporary_directory"' EXIT
observability_dir="$temporary_directory/.arcanum/observability"

first_output="$("$wrapper" --envelope "$fixture" --observability-dir "$observability_dir")"
printf '%s\n' "$first_output" | rg -q '^OBSERVATION=recorded$'
printf '%s\n' "$first_output" | rg -q '^PARENT_RUN_ID=none$'
echo "PASS DRE-004 direct Distill signal records without parent lineage"

duplicate_output="$("$wrapper" --envelope "$fixture" --observability-dir "$observability_dir")"
printf '%s\n' "$duplicate_output" | rg -q '^OBSERVATION=skipped$'
echo "PASS DRE-004 duplicate direct run dedupes"

ledger="$observability_dir/signals/sigil-invocations.jsonl"
jq -s -e '
  length == 1
  and .[0].run_id == "distill-direct-not-required-001"
  and .[0].capability.id == "distill"
  and .[0].lineage == null
  and .[0].evidence.emission_status == "not-required"
  and .[0].evidence.mutation_handoff_allowed == false
  and .[0].evidence.verdict_authority == false
' "$ledger" >/dev/null
echo "PASS DRE-004 central row preserves direct non-authority evidence"

jq '.lineage = {
  parent_run_id: "invoke-parent",
  relation: "invoked-by",
  caller: {id: "invoke", kind: "spell", mode: "plan"}
}' "$fixture" > "$temporary_directory/lineage.json"
if "$wrapper" --envelope "$temporary_directory/lineage.json" --observability-dir "$observability_dir" >/dev/null 2>&1; then
	echo "FAIL direct helper accepted caller lineage" >&2
	exit 1
fi
echo "PASS DRE-004 invoked lineage blocks on the direct helper"

jq '.capability.id = "other" | .sigil = "other" | .run_id = "other-run"' \
  "$fixture" > "$temporary_directory/other-capability.json"
if "$wrapper" --envelope "$temporary_directory/other-capability.json" --observability-dir "$observability_dir" >/dev/null 2>&1; then
	echo "FAIL direct helper accepted a non-Distill capability" >&2
	exit 1
fi
echo "PASS DRE-004 non-Distill capability blocks"

jq '.invocation_source = "invoked-by" | .run_id = "wrong-source"' \
  "$fixture" > "$temporary_directory/wrong-source.json"
if "$wrapper" --envelope "$temporary_directory/wrong-source.json" --observability-dir "$observability_dir" >/dev/null 2>&1; then
	echo "FAIL direct helper accepted invoked-by source" >&2
	exit 1
fi
echo "PASS DRE-004 invoked-by source blocks"

jq '.execution.status = "skipped" | .run_id = "skipped-run"' \
  "$fixture" > "$temporary_directory/skipped.json"
if "$wrapper" --envelope "$temporary_directory/skipped.json" --observability-dir "$observability_dir" >/dev/null 2>&1; then
	echo "FAIL direct helper emitted a skipped run" >&2
	exit 1
fi
echo "PASS DRE-004 skipped direct route cannot emit telemetry"

test "$(wc -l < "$ledger" | tr -d ' ')" = "1"
echo "SUMMARY: PASS (7 of 7 checks satisfied expectations)"
echo "AUTHORITY: direct usage telemetry is append-only maintenance evidence; it grants no verdict or mutation authority"
