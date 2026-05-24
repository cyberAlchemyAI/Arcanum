#!/usr/bin/env bash
set -euo pipefail

root="/home/vrondelli/projects/domainspec-core/arcanum"
artifact="$root/arcana/refine"
validator="$root/arcana/experiment-harness/scripts/validate-harness.sh"
xray_output="$artifact/development/example-outputs/sigil-new-low.output.md"

generic_output="$("$validator" "$artifact" 2>&1 || true)"
printf '%s\n' "$generic_output"

generic_validation="$(printf '%s\n' "$generic_output" | sed -n 's/^VALIDATION=//p' | tail -n 1)"
profile_validation="$(printf '%s\n' "$generic_output" | sed -n 's/^PROFILE_VALIDATION=//p' | tail -n 1)"

case "${generic_validation:-pass}" in
	pass | flag | block) ;;
	*) generic_validation="flag" ;;
esac

case "${profile_validation:-pass}" in
	pass | flag | block) ;;
	*) profile_validation="flag" ;;
esac

refine_live_validation="pass"

if [[ -f "$xray_output" ]]; then
	if [[ ! -s "$xray_output" ]]; then
		printf 'BLOCK: sigil-new-low output exists but is empty\n'
		refine_live_validation="block"
	else
		has_task_session_route="0"
		has_final_refinement_evidence="0"
		has_explicit_preflight_status="0"

		rg -q -- 'Proposed Task Session route|/task-session ' "$xray_output" && has_task_session_route="1" || true
		rg -q -- 'Final refinement|final refinement|Task Session execution status|Executed stages|Task Session Result|## Final Refinement' "$xray_output" && has_final_refinement_evidence="1" || true
		rg -q -- 'Status: (flag|block)|preflight-only|proposal-only|not promotion evidence' "$xray_output" && has_explicit_preflight_status="1" || true

		if [[ "$has_task_session_route" == "1" && "$has_final_refinement_evidence" == "0" && "$has_explicit_preflight_status" == "0" ]]; then
			printf 'FLAG: sigil-new-low output is proposal-only; live promotion evidence requires final refinement evidence or explicit flag/block status\n'
			refine_live_validation="flag"
		fi
	fi
fi

printf 'REFINE_LIVE_VALIDATION=%s\n' "$refine_live_validation"

final_validation="$generic_validation"
if [[ "$generic_validation" == "block" || "$profile_validation" == "block" || "$refine_live_validation" == "block" ]]; then
	final_validation="block"
elif [[ "$generic_validation" == "flag" || "$profile_validation" == "flag" || "$refine_live_validation" == "flag" ]]; then
	final_validation="flag"
fi

printf 'VALIDATION=%s\n' "$final_validation"
printf 'PROFILE_VALIDATION=%s\n' "$profile_validation"

if [[ "$final_validation" == "block" ]]; then
	exit 1
fi
