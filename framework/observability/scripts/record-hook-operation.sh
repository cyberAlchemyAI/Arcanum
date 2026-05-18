#!/usr/bin/env bash
set -euo pipefail

usage() {
	cat <<'USAGE'
Usage:
  record-hook-operation.sh --observability-dir <path> --hook <name> --target-run-id <id> --action <action> --status <status> [options]

Options:
  --target-session-id <id>
  --hook-run-id <id>
  --input <path>              repeatable
  --output <path>             repeatable
  --emitted-signal true|false
  --reason <text>
  --duration-ms <number>
  --dedupe-key <key>
  --dedupe-mode check|commit|none
  --observer-version <version>

Statuses: started | completed | skipped | failed
USAGE
}

if ! command -v jq >/dev/null 2>&1; then
	printf 'ERROR: jq not found\n' >&2
	exit 1
fi

observability_dir=""
hook=""
target_run_id=""
target_session_id=""
hook_run_id=""
action=""
status=""
emitted_signal="false"
reason=""
duration_ms="0"
dedupe_key=""
observer_version="0.1.0"
dedupe_mode="commit"
inputs=()
outputs=()

while [[ "$#" -gt 0 ]]; do
	case "$1" in
		--observability-dir) observability_dir="$2"; shift 2 ;;
		--hook) hook="$2"; shift 2 ;;
		--target-run-id) target_run_id="$2"; shift 2 ;;
		--target-session-id) target_session_id="$2"; shift 2 ;;
		--hook-run-id) hook_run_id="$2"; shift 2 ;;
		--action) action="$2"; shift 2 ;;
		--status) status="$2"; shift 2 ;;
		--input) inputs+=("$2"); shift 2 ;;
		--output) outputs+=("$2"); shift 2 ;;
		--emitted-signal) emitted_signal="$2"; shift 2 ;;
		--reason) reason="$2"; shift 2 ;;
		--duration-ms) duration_ms="$2"; shift 2 ;;
		--dedupe-key) dedupe_key="$2"; shift 2 ;;
		--dedupe-mode) dedupe_mode="$2"; shift 2 ;;
		--observer-version) observer_version="$2"; shift 2 ;;
		--help|-h) usage; exit 0 ;;
		*)
			printf 'ERROR: unknown argument: %s\n' "$1" >&2
			usage >&2
			exit 2
			;;
	esac
done

if [[ -z "$observability_dir" || -z "$hook" || -z "$target_run_id" || -z "$action" || -z "$status" ]]; then
	usage >&2
	exit 2
fi

case "$status" in
	started|completed|skipped|failed) ;;
	*)
		printf 'ERROR: invalid status: %s\n' "$status" >&2
		exit 2
		;;
esac

case "$emitted_signal" in
	true|false) ;;
	*)
		printf 'ERROR: --emitted-signal must be true or false\n' >&2
		exit 2
		;;
esac
case "$dedupe_mode" in
	check|commit|none) ;;
	*)
		printf 'ERROR: --dedupe-mode must be check, commit, or none\n' >&2
		exit 2
		;;
esac

mkdir -p "$observability_dir/hooks/reflections"
operations="$observability_dir/hooks/hook-operations.jsonl"
failures="$observability_dir/hooks/failures.jsonl"
dedupe="$observability_dir/hooks/dedupe.jsonl"
touch "$operations" "$failures" "$dedupe"

timestamp="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
safe_timestamp="$(date -u +%Y%m%dT%H%M%SZ)"
if [[ -z "$hook_run_id" ]]; then
	hook_run_id="hook-$safe_timestamp-$hook"
fi
if [[ -z "$target_session_id" ]]; then
	target_session_id="unknown"
fi
if [[ -z "$dedupe_key" ]]; then
	dedupe_key="$target_run_id:$hook:$observer_version"
fi

if [[ "$status" == "completed" && "$dedupe_mode" != "none" && ( "$emitted_signal" == "true" || "$dedupe_mode" == "check" ) ]]; then
	if jq -e --arg key "$dedupe_key" 'select(.dedupe_key == $key)' "$dedupe" >/dev/null 2>&1; then
		status="skipped"
		emitted_signal="false"
		if [[ -z "$reason" ]]; then
			reason="duplicate observer emission"
		fi
	elif [[ "$dedupe_mode" == "commit" ]]; then
		jq -cn \
			--arg timestamp "$timestamp" \
			--arg dedupe_key "$dedupe_key" \
			--arg target_run_id "$target_run_id" \
			--arg hook "$hook" \
			'{timestamp: $timestamp, dedupe_key: $dedupe_key, target_run_id: $target_run_id, hook: $hook}' >> "$dedupe"
	fi
fi

inputs_json="$(printf '%s\n' "${inputs[@]}" | jq -Rsc 'split("\n")[:-1]')"
outputs_json="$(printf '%s\n' "${outputs[@]}" | jq -Rsc 'split("\n")[:-1]')"

event="$(
	jq -cn \
		--arg timestamp "$timestamp" \
		--arg hook "$hook" \
		--arg hook_run_id "$hook_run_id" \
		--arg target_run_id "$target_run_id" \
		--arg target_session_id "$target_session_id" \
		--arg action "$action" \
		--arg status "$status" \
		--arg reason "$reason" \
		--argjson inputs "$inputs_json" \
		--argjson outputs "$outputs_json" \
		--argjson emitted_signal "$emitted_signal" \
		--argjson duration_ms "$duration_ms" \
		--arg dedupe_key "$dedupe_key" \
		'{
			timestamp: $timestamp,
			hook: $hook,
			hook_run_id: $hook_run_id,
			target_run_id: $target_run_id,
			target_session_id: $target_session_id,
			action: $action,
			status: $status,
			inputs: $inputs,
			outputs: $outputs,
			emitted_signal: $emitted_signal,
			reason: $reason,
			duration_ms: $duration_ms,
			dedupe_key: $dedupe_key,
			observe: false
		}'
)"

printf '%s\n' "$event" >> "$operations"
if [[ "$status" == "failed" ]]; then
	printf '%s\n' "$event" >> "$failures"
fi

printf 'HOOK_OPERATION=%s\n' "$status"
printf 'HOOK_LEDGER=%s\n' "$operations"
printf 'DEDUPE_KEY=%s\n' "$dedupe_key"
