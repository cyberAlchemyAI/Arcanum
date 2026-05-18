#!/usr/bin/env bash
set -euo pipefail

usage() {
	cat <<'USAGE'
Usage:
  observe-invocation.sh --envelope <path> [--observability-dir <path>] [--observer-version <version>]

Validates one invocation envelope, normalizes legacy sigil-shaped and
capability-shaped envelopes, records hook operations, dedupes repeated
observer emissions, and appends one telemetry row to the central observability
ledger.

This script intentionally does not perform reflection report generation or
reflection routing. Those belong to later observed-invocation-loop SWUs.
USAGE
}

if ! command -v jq >/dev/null 2>&1; then
	printf 'ERROR: jq not found\n' >&2
	exit 1
fi

envelope=""
observability_dir=""
observer_version="0.1.0"
strict_mode="${OBSERVED_INVOCATION_STRICT:-0}"

while [[ "$#" -gt 0 ]]; do
	case "$1" in
		--envelope) envelope="$2"; shift 2 ;;
		--observability-dir) observability_dir="$2"; shift 2 ;;
		--observer-version) observer_version="$2"; shift 2 ;;
		--help|-h) usage; exit 0 ;;
		*)
			printf 'ERROR: unknown argument: %s\n' "$1" >&2
			usage >&2
			exit 2
			;;
	esac
done

if [[ -z "$envelope" ]]; then
	usage >&2
	exit 2
fi
if [[ ! -f "$envelope" ]]; then
	printf 'ERROR: envelope not found: %s\n' "$envelope" >&2
	exit 1
fi

envelope_abs="$(cd "$(dirname "$envelope")" && pwd)/$(basename "$envelope")"
if [[ -z "$observability_dir" ]]; then
	repo_root="$(git -C "$(dirname "$envelope_abs")" rev-parse --show-toplevel 2>/dev/null || pwd)"
	observability_dir="$repo_root/.arcanum/observability"
fi

mkdir -p \
	"$observability_dir/signals" \
	"$observability_dir/by-sigil" \
	"$observability_dir/by-capability" \
	"$observability_dir/hooks"

ledger="$observability_dir/signals/sigil-invocations.jsonl"
reflection_state="$observability_dir/reflection-state.json"
observability_config="$observability_dir/config.json"
touch "$ledger"
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
hook_recorder="$script_dir/record-hook-operation.sh"
hook_started_at_ms="$(date +%s%3N)"

record_hook() {
	local action="$1"
	local status="$2"
	local emitted_signal="$3"
	local reason="$4"
	local duration_ms="${5:-0}"
	local dedupe_mode="${6:-commit}"

	if [[ -x "$hook_recorder" ]]; then
		if "$hook_recorder" \
			--observability-dir "$observability_dir" \
			--hook signal-observer \
			--target-run-id "$target_run_id" \
			--target-session-id "$target_session_id" \
			--action "$action" \
			--status "$status" \
			--input "$envelope_abs" \
			--output "$ledger" \
			--emitted-signal "$emitted_signal" \
			--reason "$reason" \
			--duration-ms "$duration_ms" \
			--dedupe-key "$dedupe_key" \
			--dedupe-mode "$dedupe_mode" \
			--observer-version "$observer_version" 2>/dev/null; then
			return 0
		fi
		if [[ "$strict_mode" == "1" ]]; then
			return 1
		fi
	fi
	return 0
}

validate_filter='
def non_empty_string: type == "string" and length > 0;
def array_field: type == "array";

(. as $e
| ($e.capability.id // $e.sigil // "") as $capability_id
| ($e.capability.kind // "sigil") as $capability_kind
| [
	(if ($e.timestamp | non_empty_string) then empty else "missing timestamp" end),
	(if ($capability_id | non_empty_string) then empty else "missing capability.id or sigil" end),
	(if ($capability_kind | non_empty_string) then empty else "missing capability.kind" end),
	(if (($e.mode // $e.capability.mode // "") | non_empty_string) then empty else "missing mode" end),
	(if (($e.request.summary // $e.request.intent // "") | non_empty_string) then empty else "missing request summary or intent" end),
	(if (($e.execution.status // "") | non_empty_string) then empty else "missing execution.status" end),
	(if (($e.execution.outputs // []) | array_field) then empty else "execution.outputs must be an array" end),
	(if (($e.execution.files_changed // []) | array_field) then empty else "execution.files_changed must be an array" end),
	(if (($e.execution.validation // []) | array_field) then empty else "execution.validation must be an array" end),
	(if (($e.observer.quality_bar_status // "") | non_empty_string) then empty else "missing observer.quality_bar_status" end),
	(if (($e.observer.anti_pattern_hits // []) | array_field) then empty else "observer.anti_pattern_hits must be an array" end),
	(if (($e.observer.workflow_gaps // []) | array_field) then empty else "observer.workflow_gaps must be an array" end),
	(if (($e.observer.reflection_trigger // "") | non_empty_string) then empty else "missing observer.reflection_trigger" end),
	(if (($e.observer.recommendation // "") | non_empty_string) then empty else "missing observer.recommendation" end)
])
'

validation_errors="$(jq -r "$validate_filter | .[]" "$envelope_abs")"
if [[ -n "$validation_errors" ]]; then
	printf 'OBSERVATION=failed\n'
	printf 'REASON=invalid envelope\n'
	printf '%s\n' "$validation_errors" | sed 's/^/ERROR: /' >&2
	exit 1
fi

target_run_id="$(
	jq -r \
		--arg envelope "$envelope_abs" \
		'(.run_id // .id // .target_run_id // empty) as $direct
		| (.session_id // "unknown") as $session
		| (.capability.id // .sigil // "unknown") as $capability
		| (.timestamp // "unknown") as $timestamp
		| if ($direct | length) > 0 then $direct
		  else "invocation-\($session)-\($capability)-\($timestamp)-\($envelope)"
		  end
		| gsub("[^A-Za-z0-9._-]"; "-")' "$envelope_abs"
)"
target_session_id="$(jq -r '.session_id // "unknown"' "$envelope_abs")"
dedupe_key="$target_run_id:signal-observer:$observer_version"
record_hook observe started false "observer started" 0

event="$(
	jq -c \
		--arg observer_version "$observer_version" \
		'
		(.capability.id // .sigil) as $capability_id
		| (.capability.kind // "sigil") as $capability_kind
		| (.capability.tier // .tier // "unknown") as $capability_tier
		| (.capability.mode // .mode // "execute") as $capability_mode
		| {
			timestamp: .timestamp,
			run_id: (.run_id // .id // .target_run_id // null),
			session_id: (.session_id // null),
			sigil: (.sigil // $capability_id),
			tier: $capability_tier,
			mode: $capability_mode,
			capability: {
				id: $capability_id,
				kind: $capability_kind,
				tier: $capability_tier,
				mode: $capability_mode,
				alias: (.capability.alias // null)
			},
			command: (.command // null),
			request: {
				raw: (.request.raw // null),
				summary: (.request.summary // .request.intent),
				intent: (.request.intent // .request.summary)
			},
			execution: {
				status: .execution.status,
				outputs: (.execution.outputs // []),
				files_changed: (.execution.files_changed // []),
				validation: (.execution.validation // []),
				notes: (.execution.notes // "")
			},
			observer: {
				quality_bar_status: .observer.quality_bar_status,
				anti_pattern_hits: (.observer.anti_pattern_hits // []),
				workflow_gaps: (.observer.workflow_gaps // []),
				output_contract_drift: (.observer.output_contract_drift // false),
				reflection_trigger: .observer.reflection_trigger,
				recommendation: .observer.recommendation
			},
			target_artifact: (.target_artifact // .artifact // null),
			dedupe_key: null,
			observer_version: $observer_version
		}
		' "$envelope_abs"
)"
event="$(printf '%s\n' "$event" | jq -c --arg run_id "$target_run_id" --arg session_id "$target_session_id" --arg dedupe_key "$dedupe_key" '.run_id = $run_id | .session_id = $session_id | .dedupe_key = $dedupe_key')"

dedupe_probe="$(
	record_hook append completed false "capability telemetry duplicate check" "$(( $(date +%s%3N) - hook_started_at_ms ))" check
)"
hook_status="$(printf '%s\n' "$dedupe_probe" | sed -n 's/^HOOK_OPERATION=//p' | tail -n 1)"
if [[ "$hook_status" == "skipped" ]]; then
	printf 'OBSERVATION=skipped\n'
	printf 'REASON=duplicate observer emission\n'
	printf 'LEDGER=%s\n' "$ledger"
	printf 'DEDUPE_KEY=%s\n' "$dedupe_key"
	printf 'CAPABILITY=%s\n' "$(printf '%s\n' "$event" | jq -r '.capability.id')"
	printf 'CAPABILITY_KIND=%s\n' "$(printf '%s\n' "$event" | jq -r '.capability.kind')"
	printf 'REFLECTION_TRIGGER=%s\n' "$(printf '%s\n' "$event" | jq -r '.observer.reflection_trigger')"
	printf 'RECOMMENDATION=%s\n' "$(printf '%s\n' "$event" | jq -r '.observer.recommendation')"
	exit 0
fi

if jq -e --arg dedupe_key "$dedupe_key" 'select(.dedupe_key == $dedupe_key)' "$ledger" >/dev/null 2>&1; then
	record_hook append completed false "central ledger duplicate check" "$(( $(date +%s%3N) - hook_started_at_ms ))" none >/dev/null
	printf 'OBSERVATION=skipped\n'
	printf 'REASON=duplicate observer emission in central ledger\n'
	printf 'LEDGER=%s\n' "$ledger"
	printf 'DEDUPE_KEY=%s\n' "$dedupe_key"
	printf 'CAPABILITY=%s\n' "$(printf '%s\n' "$event" | jq -r '.capability.id')"
	printf 'CAPABILITY_KIND=%s\n' "$(printf '%s\n' "$event" | jq -r '.capability.kind')"
	printf 'REFLECTION_TRIGGER=%s\n' "$(printf '%s\n' "$event" | jq -r '.observer.reflection_trigger')"
	printf 'RECOMMENDATION=%s\n' "$(printf '%s\n' "$event" | jq -r '.observer.recommendation')"
	exit 0
fi

reflection_trigger="$(printf '%s\n' "$event" | jq -r '.observer.reflection_trigger')"
if [[ -f "$reflection_state" && -f "$observability_config" && "$reflection_trigger" == "none" ]]; then
	threshold_trigger="$(
		printf '%s\n' "$event" | jq -r \
			--slurpfile state "$reflection_state" \
			--slurpfile config "$observability_config" \
			--slurpfile signals "$ledger" \
			'
			. as $event
			| ($state[0].last_reflection_at // "") as $last_reflection_at
			| ($config[0].thresholds // {}) as $t
			| [$signals[]? | select(($last_reflection_at == "") or ((.timestamp // "") > $last_reflection_at))] as $recent
			| (($recent | length) + 1) as $meaningful
			| (([$recent[]? | (.execution.outputs // []) | length] | add // 0) + (($event.execution.outputs // []) | length)) as $outputs
			| (([$recent[]? | if (.observer.quality_bar_status // "") == "partial" then 1 else 0 end] | add // 0) + (if $event.observer.quality_bar_status == "partial" then 1 else 0 end)) as $related
			| ([ ($event.observer.workflow_gaps // [])[]? | select(.severity == "severe" or .severity == "high") ] | length) as $severe
			| if (($t.severe_workflow_gaps // 1) > 0 and $severe >= ($t.severe_workflow_gaps // 1)) then "severe-gap"
			  elif (($t.related_workflow_gaps // 3) > 0 and $related >= ($t.related_workflow_gaps // 3)) then "gap-threshold"
			  elif (($t.generated_outputs // 10) > 0 and $outputs >= ($t.generated_outputs // 10)) then "output-threshold"
			  elif (($t.meaningful_executions // 5) > 0 and $meaningful >= ($t.meaningful_executions // 5)) then "usage-threshold"
			  else "none" end
			'
	)"
	if [[ "$threshold_trigger" != "none" ]]; then
		event="$(printf '%s\n' "$event" | jq -c --arg trigger "$threshold_trigger" '.observer.reflection_trigger = $trigger | .observer.recommendation = "reflect-now"')"
	fi
fi

printf '%s\n' "$event" >> "$ledger"
ledger_line="$(wc -l < "$ledger" | tr -d ' ')"

capability_id="$(printf '%s\n' "$event" | jq -r '.capability.id')"
capability_kind="$(printf '%s\n' "$event" | jq -r '.capability.kind')"
legacy_sigil="$(printf '%s\n' "$event" | jq -r '.sigil')"

safe_capability_id="${capability_id//[^A-Za-z0-9._-]/-}"
safe_capability_kind="${capability_kind//[^A-Za-z0-9._-]/-}"
safe_sigil="${legacy_sigil//[^A-Za-z0-9._-]/-}"

mkdir -p "$observability_dir/by-capability/$safe_capability_kind"
index_event="$(
	printf '%s\n' "$event" | jq -c \
		--arg ledger "signals/sigil-invocations.jsonl" \
		--argjson line "$ledger_line" \
		'{
			timestamp,
			run_id,
			session_id,
			dedupe_key,
			ledger: $ledger,
			line: $line,
			sigil,
			capability,
			execution_status: .execution.status,
			reflection_trigger: .observer.reflection_trigger,
			recommendation: .observer.recommendation,
			target_artifact
		}'
)"
printf '%s\n' "$index_event" >> "$observability_dir/by-capability/$safe_capability_kind/$safe_capability_id.jsonl"
printf '%s\n' "$index_event" >> "$observability_dir/by-sigil/$safe_sigil.jsonl"

reflection_state_status="unavailable"
if [[ -f "$reflection_state" ]]; then
	tmp_state="$(mktemp)"
	if printf '%s\n' "$event" | jq \
		--slurpfile state "$reflection_state" \
		'
		. as $event
		| ($state[0] // {}) as $s
		| (($event.execution.outputs // []) | length) as $generated_outputs
		| ([ ($event.observer.workflow_gaps // [])[]? | select(.severity == "severe" or .severity == "high") ] | length) as $severe_gaps
		| ($event.capability.id // $event.sigil) as $capability_id
		| ($event.capability.kind // "sigil") as $capability_kind
		| ($event.sigil // $capability_id) as $sigil
		| $s
		| .version = (.version // "0.1.0")
		| .last_reflection_at = (.last_reflection_at // null)
		| .counters.meaningful_executions = ((.counters.meaningful_executions // 0) + 1)
		| .counters.generated_outputs = ((.counters.generated_outputs // 0) + $generated_outputs)
		| .counters.related_workflow_gaps = ((.counters.related_workflow_gaps // 0) + (if $event.observer.quality_bar_status == "partial" then 1 else 0 end))
		| .counters.severe_workflow_gaps = ((.counters.severe_workflow_gaps // 0) + $severe_gaps)
		| .counters.quality_bar_failures = ((.counters.quality_bar_failures // 0) + (if $event.observer.quality_bar_status == "fail" then 1 else 0 end))
		| .counters.output_contract_drift_events = ((.counters.output_contract_drift_events // 0) + (if $event.observer.output_contract_drift == true then 1 else 0 end))
		| .by_sigil[$sigil].meaningful_executions = ((.by_sigil[$sigil].meaningful_executions // 0) + 1)
		| .by_sigil[$sigil].generated_outputs = ((.by_sigil[$sigil].generated_outputs // 0) + $generated_outputs)
		| .by_sigil[$sigil].last_observed_at = $event.timestamp
		| .by_capability[$capability_kind][$capability_id].meaningful_executions = ((.by_capability[$capability_kind][$capability_id].meaningful_executions // 0) + 1)
		| .by_capability[$capability_kind][$capability_id].generated_outputs = ((.by_capability[$capability_kind][$capability_id].generated_outputs // 0) + $generated_outputs)
		| .by_capability[$capability_kind][$capability_id].last_observed_at = $event.timestamp
		' > "$tmp_state"; then
		mv "$tmp_state" "$reflection_state"
		reflection_state_status="updated"
		record_hook update-counters completed false "reflection counters updated" "$(( $(date +%s%3N) - hook_started_at_ms ))" >/dev/null
	else
		rm -f "$tmp_state"
		reflection_state_status="failed"
		record_hook update-counters failed false "reflection counter update failed" "$(( $(date +%s%3N) - hook_started_at_ms ))" >/dev/null
	fi
fi

if ! commit_output="$(record_hook append completed true "capability telemetry append committed" "$(( $(date +%s%3N) - hook_started_at_ms ))" commit)"; then
	printf 'OBSERVATION=failed\n'
	printf 'REASON=dedupe commit failed\n'
	printf 'LEDGER=%s\n' "$ledger"
	printf 'LEDGER_LINE=%s\n' "$ledger_line"
	printf 'DEDUPE_KEY=%s\n' "$dedupe_key"
	exit 1
fi

printf 'OBSERVATION=recorded\n'
printf 'LEDGER=%s\n' "$ledger"
printf 'LEDGER_LINE=%s\n' "$ledger_line"
printf 'BY_CAPABILITY=%s\n' "$observability_dir/by-capability/$safe_capability_kind/$safe_capability_id.jsonl"
printf 'BY_SIGIL=%s\n' "$observability_dir/by-sigil/$safe_sigil.jsonl"
printf 'INDEX_MODEL=central-ledger-reference\n'
printf 'CAPABILITY=%s\n' "$capability_id"
printf 'CAPABILITY_KIND=%s\n' "$capability_kind"
printf 'DEDUPE_KEY=%s\n' "$dedupe_key"
printf 'REFLECTION_TRIGGER=%s\n' "$(printf '%s\n' "$event" | jq -r '.observer.reflection_trigger')"
printf 'RECOMMENDATION=%s\n' "$(printf '%s\n' "$event" | jq -r '.observer.recommendation')"
printf 'REFLECTION_STATE=%s\n' "$reflection_state_status"
