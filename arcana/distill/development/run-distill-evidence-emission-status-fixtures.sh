#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
wrapper="$script_dir/../scripts/observe-direct-invocation.sh"
skill="$script_dir/../SKILL.md"
base="$script_dir/fixtures/direct-telemetry/direct-not-required.json"
temporary_directory="$(mktemp -d)"
trap 'rm -rf "$temporary_directory"' EXIT
observability_dir="$temporary_directory/.arcanum/observability"

event_ref='{"path":"runs/direct/events.jsonl","sha256":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","size_bytes":512}'

for status in complete partial failed not-required not-configured; do
	case "$status" in
		complete)
			evidence_status="complete"
			execution_status="completed"
			runtime_refs="[$event_ref]"
			;;
		partial)
			evidence_status="partial"
			execution_status="partial"
			runtime_refs="[$event_ref]"
			;;
		failed)
			evidence_status="unavailable"
			execution_status="failed"
			runtime_refs="[]"
			;;
		not-required|not-configured)
			evidence_status="unavailable"
			execution_status="completed"
			runtime_refs="[]"
			;;
	esac

	jq \
		--arg run_id "distill-direct-status-$status" \
		--arg emission_status "$status" \
		--arg evidence_status "$evidence_status" \
		--arg execution_status "$execution_status" \
		--argjson runtime_refs "$runtime_refs" \
		'.run_id = $run_id
		| .evidence.emission_status = $emission_status
		| .evidence.status = $evidence_status
		| .evidence.runtime_event_refs = $runtime_refs
		| .execution.status = $execution_status' \
		"$base" > "$temporary_directory/$status.json"

	output="$("$wrapper" --envelope "$temporary_directory/$status.json" --observability-dir "$observability_dir")"
	printf '%s\n' "$output" | rg -q '^OBSERVATION=recorded$'
	echo "PASS DRE-005 evidence-emission status $status records"
done

ledger="$observability_dir/signals/sigil-invocations.jsonl"
jq -s -e '
  length == 5
  and ([.[].evidence.emission_status] | sort)
    == (["complete", "partial", "failed", "not-required", "not-configured"] | sort)
  and all(.[];
    .evidence.mutation_handoff_allowed == false
    and .evidence.verdict_authority == false)
' "$ledger" >/dev/null
echo "PASS DRE-005 all statuses remain non-authoritative"

jq '.run_id = "invalid-complete" | .evidence.emission_status = "complete"' \
  "$base" > "$temporary_directory/invalid-complete.json"
if "$wrapper" --envelope "$temporary_directory/invalid-complete.json" --observability-dir "$observability_dir" >/dev/null 2>&1; then
	echo "FAIL complete emission accepted unavailable evidence" >&2
	exit 1
fi
echo "PASS DRE-005 false complete emission blocks"

jq '.run_id = "invalid-not-required"
  | .evidence.emission_status = "not-required"
  | .evidence.status = "partial"
  | .evidence.runtime_event_refs = [{
      path: "runs/direct/events.jsonl",
      sha256: "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
      size_bytes: 512
    }]' "$base" > "$temporary_directory/invalid-not-required.json"
if "$wrapper" --envelope "$temporary_directory/invalid-not-required.json" --observability-dir "$observability_dir" >/dev/null 2>&1; then
	echo "FAIL not-required emission accepted runtime evidence" >&2
	exit 1
fi
echo "PASS DRE-005 contradictory non-emitting status blocks"

jq '.run_id = "invalid-authority" | .evidence.mutation_handoff_allowed = true' \
  "$base" > "$temporary_directory/invalid-authority.json"
if "$wrapper" --envelope "$temporary_directory/invalid-authority.json" --observability-dir "$observability_dir" >/dev/null 2>&1; then
	echo "FAIL telemetry accepted mutation authority" >&2
	exit 1
fi
echo "PASS DRE-005 telemetry mutation-authority claim blocks"

for mode in Compact Standard Tournament Deep Validate; do
	rg -F -q "| $mode |" "$skill"
done
echo "PASS DRE-005 Distill mode set remains unchanged"

rg -F -q "One proposal track, one recursive round" "$skill"
rg -F -q "two recursive rounds, one reconciliation pass" "$skill"
rg -F -q "Three proposal tracks by default" "$skill"
rg -F -q "three rounds by default" "$skill"
echo "PASS DRE-005 finite mode budgets remain unchanged"

rg -F -q "Use true subagents whenever the active runtime supports them" "$skill"
rg -F -q "If subagents are unavailable, run labeled Proposer and Balancer passes" "$skill"
echo "PASS DRE-005 role policy remains unchanged"

for field in \
	"Current smallest coherent unit:" \
	"Technique pack trace:" \
	"Closure and recomposition proof:" \
	"Navigation guide:" \
	"Next route:"; do
	rg -F -q -- "- $field" "$skill"
done
echo "PASS DRE-005 established output semantics remain present"

echo "SUMMARY: PASS (13 of 13 checks satisfied expectations)"
echo "AUTHORITY: evidence-emission status reports producer state only; it cannot change verdict or mutation readiness"
