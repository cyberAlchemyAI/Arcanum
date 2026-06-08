#!/usr/bin/env bash
set -euo pipefail

usage() {
	cat <<'USAGE'
Usage:
  observe-harness.sh <artifact-path> [report-path]

Appends one signal-observer-compatible invocation envelope to the repository
observability ledger when .arcanum/observability exists.
USAGE
}

if [[ "$#" -lt 1 || "$#" -gt 2 ]]; then
	usage >&2
	exit 2
fi

if ! command -v jq >/dev/null 2>&1; then
	printf 'OBSERVATION=skipped\n'
	printf 'REASON=jq not found\n'
	exit 0
fi

artifact="$1"
if [[ ! -d "$artifact" ]]; then
	printf 'ERROR: artifact path not found: %s\n' "$artifact" >&2
	exit 1
fi

artifact_abs="$(cd "$artifact" && pwd)"
dev_dir="$artifact_abs/development"
repo_root="${EXPERIMENT_REPO_ROOT:-$(git -C "$artifact_abs" rev-parse --show-toplevel 2>/dev/null || pwd)}"
observability_dir="${EXPERIMENT_OBSERVABILITY_DIR:-$repo_root/.arcanum/observability}"

if [[ ! -d "$observability_dir" ]]; then
	printf 'OBSERVATION=skipped\n'
	printf 'REASON=observability package not found: %s\n' "${observability_dir#$repo_root/}"
	exit 0
fi

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
default_framework_observability_dir="$(cd "$script_dir/../../../framework/observability" && pwd)"
framework_observability_dir="${EXPERIMENT_FRAMEWORK_OBSERVABILITY_DIR:-$default_framework_observability_dir}"
hook_recorder="$framework_observability_dir/scripts/record-hook-operation.sh"
run_starter="$framework_observability_dir/scripts/start-observed-run.sh"
run_checkpointer="$framework_observability_dir/scripts/checkpoint-observed-run.sh"
run_finisher="$framework_observability_dir/scripts/finish-observed-run.sh"

mkdir -p "$observability_dir/signals" "$observability_dir/by-sigil" "$observability_dir/by-capability" "$observability_dir/hooks/reflections" "$observability_dir/runs"
ledger="$observability_dir/signals/sigil-invocations.jsonl"
reflection_state="$observability_dir/reflection-state.json"
touch "$ledger" "$observability_dir/hooks/hook-operations.jsonl" "$observability_dir/hooks/failures.jsonl" "$observability_dir/hooks/dedupe.jsonl"

report="${2:-}"
if [[ -z "$report" ]]; then
	report="$(find "$dev_dir/runs" -maxdepth 1 -type f -name '*.md' 2>/dev/null | sort | tail -n 1 || true)"
fi

if [[ -z "$report" || ! -f "$report" ]]; then
	printf 'OBSERVATION=skipped\n'
	printf 'REASON=report not found\n'
	exit 0
fi

report_abs="$(cd "$(dirname "$report")" && pwd)/$(basename "$report")"
report_rel="${report_abs#$repo_root/}"
artifact_rel="${artifact_abs#$repo_root/}"
timestamp="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
safe_timestamp="$(date -u +%Y%m%dT%H%M%SZ)"
target_run_id="experiment-${report_rel//[^A-Za-z0-9._-]/-}"
target_session_id="${EXPERIMENT_SESSION_ID:-experiment-harness}"
observer_version="${EXPERIMENT_OBSERVER_VERSION:-0.1.0}"
dedupe_key="$target_run_id:signal-observer:$observer_version"
hook_started_at_ms="$(date +%s%3N)"

record_hook() {
	if [[ -x "$hook_recorder" ]]; then
		"$hook_recorder" \
			--observability-dir "$observability_dir" \
			--hook signal-observer \
			--target-run-id "$target_run_id" \
			--target-session-id "$target_session_id" \
			--action observe \
			--status "$1" \
			--input "$report_rel" \
			--output "${ledger#$repo_root/}" \
			--emitted-signal "${2:-false}" \
			--reason "${3:-}" \
			--duration-ms "${4:-0}" \
			--dedupe-key "$dedupe_key" \
			--observer-version "$observer_version" >/dev/null || true
	fi
}

if [[ -x "$run_starter" ]]; then
	run_output="$("$run_starter" \
		--observability-dir "$observability_dir" \
		--session-id "$target_session_id" \
		--run-id "$target_run_id" \
		--capability experiment-harness \
		--kind sigil \
		--tier arcana \
		--mode observe \
		--summary "Observe experiment harness report for $artifact_rel" \
		--intent "Record experiment validation evidence as telemetry." 2>/dev/null || true)"
	run_dir="$(printf '%s\n' "$run_output" | sed -n 's/^RUN_DIR=//p' | tail -n 1)"
else
	run_dir=""
fi

record_hook started false "observer started" 0

validation="$(sed -n 's/^- Validation: //p' "$report_abs" | head -n 1)"
if [[ -z "$validation" ]]; then
	validation="$(sed -n 's/^VALIDATION=//p' "$report_abs" | tail -n 1)"
fi
if [[ -z "$validation" ]]; then
	validation="$(sed -n 's/^RESULT: //p' "$report_abs" | sed 's/ .*//' | tail -n 1)"
fi
if [[ -z "$validation" ]]; then
	validation="not_checked"
fi
reported_quality_bar_status="$(sed -n 's/^QUALITY_BAR_STATUS=//p' "$report_abs" | tail -n 1)"
reported_anti_pattern_hits_json="$(sed -n 's/^ANTI_PATTERN_HITS_JSON=//p' "$report_abs" | tail -n 1)"
reported_workflow_gaps_json="$(sed -n 's/^WORKFLOW_GAPS_JSON=//p' "$report_abs" | tail -n 1)"

case "$validation" in
	pass)
		execution_status="completed"
		quality_bar_status="pass"
		reflection_trigger="none"
		recommendation="none"
		;;
	flag)
		execution_status="partial"
		quality_bar_status="partial"
		reflection_trigger="none"
		recommendation="targeted-update"
		;;
	block|fail|failed)
		execution_status="blocked"
		quality_bar_status="fail"
		reflection_trigger="severe-gap"
		recommendation="reflect-now"
		;;
	*)
		execution_status="partial"
		quality_bar_status="not_checked"
		reflection_trigger="none"
		recommendation="targeted-update"
		;;
esac

if [[ -n "$reported_quality_bar_status" ]]; then
	quality_bar_status="$reported_quality_bar_status"
	case "$quality_bar_status" in
		pass)
			if [[ "$validation" == "pass" ]]; then
				execution_status="completed"
				recommendation="none"
			fi
			;;
		partial)
			execution_status="partial"
			recommendation="targeted-update"
			;;
		fail)
			execution_status="blocked"
			reflection_trigger="severe-gap"
			recommendation="reflect-now"
			;;
	esac
fi

prompt_count="$(find "$dev_dir/example-prompts" -maxdepth 1 -type f -name '*.md' 2>/dev/null | wc -l | tr -d ' ')"
output_count="$(find "$dev_dir/example-outputs" -maxdepth 1 -type f -name '*.output.md' 2>/dev/null | wc -l | tr -d ' ')"
fixture_count="$(find "$dev_dir/fixtures" -maxdepth 1 -type f -name '*.md' ! -name '*.expected.md' 2>/dev/null | wc -l | tr -d ' ')"

if [[ -n "$run_dir" && -x "$run_checkpointer" ]]; then
	"$run_checkpointer" "$run_dir" \
		--phase "report-summary" \
		--summary "fixtures=$fixture_count prompts=$prompt_count outputs=$output_count validation=$validation" \
		--file "$report_rel" \
		--validation "experiment harness validation: $validation" \
		--next "append signal-observer telemetry" >/dev/null || true
fi

workflow_gaps_json='[]'
if [[ "$validation" != "pass" ]]; then
	workflow_gaps_json="$(
		jq -n \
			--arg severity "$([[ "$validation" == "block" || "$validation" == "fail" || "$validation" == "failed" ]] && printf 'severe' || printf 'medium')" \
			--arg summary "Experiment harness validation returned $validation" \
			--arg evidence "$report_rel" \
			'[{
				category: "validation",
				severity: $severity,
				summary: $summary,
				evidence: $evidence
			}]'
	)"
fi
if [[ -n "$reported_workflow_gaps_json" ]] && printf '%s\n' "$reported_workflow_gaps_json" | jq -e . >/dev/null 2>&1; then
	workflow_gaps_json="$reported_workflow_gaps_json"
fi
anti_pattern_hits_json='[]'
if [[ -n "$reported_anti_pattern_hits_json" ]] && printf '%s\n' "$reported_anti_pattern_hits_json" | jq -e . >/dev/null 2>&1; then
	anti_pattern_hits_json="$reported_anti_pattern_hits_json"
fi

event="$(
	jq -cn \
		--arg timestamp "$timestamp" \
		--arg sigil "experiment-harness" \
		--arg tier "arcana" \
		--arg mode "observe" \
		--arg run_id "$target_run_id" \
		--arg session_id "$target_session_id" \
		--arg summary "Observed experiment harness report for $artifact_rel" \
		--arg intent "Close the experiment cycle by recording harness validation evidence as observability telemetry." \
		--arg status "$execution_status" \
		--arg artifact "$artifact_rel" \
		--arg report "$report_rel" \
		--arg notes "fixtures=$fixture_count prompts=$prompt_count outputs=$output_count validation=$validation" \
		--arg validation_entry "experiment harness validation: $validation" \
		--arg quality "$quality_bar_status" \
		--arg trigger "$reflection_trigger" \
		--arg recommendation "$recommendation" \
		--argjson anti_pattern_hits "$anti_pattern_hits_json" \
		--argjson workflow_gaps "$workflow_gaps_json" \
		'{
			timestamp: $timestamp,
			run_id: $run_id,
			session_id: $session_id,
			sigil: $sigil,
			tier: $tier,
			mode: $mode,
			capability: {
				id: $sigil,
				kind: "sigil",
				tier: $tier,
				mode: $mode
			},
			request: {
				raw: null,
				summary: $summary,
				intent: $intent
			},
			execution: {
				status: $status,
				outputs: [$report],
				files_changed: [$report],
				validation: [$validation_entry],
				notes: $notes
			},
			observer: {
				quality_bar_status: $quality,
				anti_pattern_hits: $anti_pattern_hits,
				workflow_gaps: $workflow_gaps,
				output_contract_drift: false,
				reflection_trigger: $trigger,
				recommendation: $recommendation
			},
			target_artifact: $artifact
	}'
)"

if [[ -n "$run_dir" ]]; then
	observer_envelope="$run_dir/invocation-envelope.json"
else
	observer_envelope="$(mktemp)"
fi
printf '%s\n' "$event" > "$observer_envelope"

observer_script="$framework_observability_dir/scripts/observe-invocation.sh"
if [[ ! -x "$observer_script" ]]; then
	printf 'OBSERVATION=failed\n'
	printf 'REASON=generic observer not found: %s\n' "$observer_script"
	exit 1
fi

observer_output="$("$observer_script" \
	--envelope "$observer_envelope" \
	--observability-dir "$observability_dir" \
	--observer-version "$observer_version" 2>&1)" || {
	if [[ -n "$run_dir" && -x "$run_finisher" ]]; then
		"$run_finisher" "$run_dir" \
			--status failed \
			--output "$report_rel" \
			--file "$report_rel" \
			--validation "generic observer failed" \
			--notes "$observer_output" >/dev/null || true
	fi
	printf '%s\n' "$observer_output"
	exit 1
}

observer_status="$(printf '%s\n' "$observer_output" | sed -n 's/^OBSERVATION=//p' | tail -n 1)"
reflection_trigger="$(printf '%s\n' "$observer_output" | sed -n 's/^REFLECTION_TRIGGER=//p' | tail -n 1)"
recommendation="$(printf '%s\n' "$observer_output" | sed -n 's/^RECOMMENDATION=//p' | tail -n 1)"
dedupe_key="$(printf '%s\n' "$observer_output" | sed -n 's/^DEDUPE_KEY=//p' | tail -n 1)"
ledger_out="$(printf '%s\n' "$observer_output" | sed -n 's/^LEDGER=//p' | tail -n 1)"
per_sigil_out="$(printf '%s\n' "$observer_output" | sed -n 's/^BY_SIGIL=//p' | tail -n 1)"

if [[ "$observer_status" == "skipped" ]]; then
	if [[ -n "$run_dir" && -x "$run_finisher" ]]; then
		"$run_finisher" "$run_dir" \
			--status partial \
			--output "$report_rel" \
			--file "$report_rel" \
			--validation "duplicate observer emission skipped" \
			--notes "dedupe_key=$dedupe_key" >/dev/null || true
	fi
	printf '%s\n' "$observer_output"
	exit 0
fi

if [[ -n "$run_dir" && -x "$run_finisher" ]]; then
	"$run_finisher" "$run_dir" \
		--status "$execution_status" \
		--output "$report_rel" \
		--file "$report_rel" \
		--validation "experiment harness validation: $validation" \
		--notes "observer_version=$observer_version dedupe_key=$dedupe_key" >/dev/null || true
fi

printf 'OBSERVATION=%s\n' "$observer_status"
printf 'LEDGER=%s\n' "${ledger_out#$repo_root/}"
printf 'PER_SIGIL_INDEX=%s\n' "${per_sigil_out#$repo_root/}"
printf 'REFLECTION_TRIGGER=%s\n' "${reflection_trigger:-none}"
printf 'RECOMMENDATION=%s\n' "${recommendation:-none}"
printf 'RUN_ID=%s\n' "$target_run_id"
printf 'DEDUPE_KEY=%s\n' "$dedupe_key"
