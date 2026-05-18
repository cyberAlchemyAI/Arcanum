#!/usr/bin/env bash
set -euo pipefail

usage() {
	cat <<'USAGE'
Usage:
  reflect-invocation-signals.sh [--all|--capability <id>] [--kind skill|sigil|spell] [--since <iso-date>] [--min-signals <n>] [--dry-run] [--observability-dir <path>]

Reads invocation telemetry and writes a non-mutating reflection report when
threshold-backed signal evidence is present.
USAGE
}

if ! command -v jq >/dev/null 2>&1; then
	printf 'REFLECTION=failed\n'
	printf 'REASON=jq not found\n'
	exit 1
fi

scope="all"
capability=""
kind=""
since=""
min_signals="5"
dry_run="0"
observability_dir=""

while [[ "$#" -gt 0 ]]; do
	case "$1" in
		--all) scope="all"; capability=""; shift ;;
		--capability) scope="capability"; capability="$2"; shift 2 ;;
		--kind) kind="$2"; shift 2 ;;
		--since) since="$2"; shift 2 ;;
		--min-signals) min_signals="$2"; shift 2 ;;
		--dry-run) dry_run="1"; shift ;;
		--observability-dir) observability_dir="$2"; shift 2 ;;
		--help|-h) usage; exit 0 ;;
		*)
			printf 'REFLECTION=failed\n'
			printf 'REASON=unknown argument: %s\n' "$1"
			usage >&2
			exit 2
			;;
	esac
done

case "$min_signals" in
	''|*[!0-9]*) printf 'REFLECTION=failed\nREASON=min-signals must be numeric\n'; exit 2 ;;
esac
case "$kind" in
	""|skill|sigil|spell) ;;
	*) printf 'REFLECTION=failed\nREASON=invalid kind\n'; exit 2 ;;
esac

if [[ -z "$observability_dir" ]]; then
	repo_root="$(git -C "$PWD" rev-parse --show-toplevel 2>/dev/null || pwd)"
	observability_dir="$repo_root/.arcanum/observability"
fi

ledger="$observability_dir/signals/sigil-invocations.jsonl"
reflection_state="$observability_dir/reflection-state.json"
reports_dir="$observability_dir/reflections"

if [[ -z "$since" && -f "$reflection_state" ]]; then
	since="$(jq -r '.last_reflection_at // ""' "$reflection_state" 2>/dev/null || true)"
fi

if [[ ! -f "$ledger" ]]; then
	printf 'REFLECTION=failed\n'
	printf 'REASON=ledger not found\n'
	printf 'REPORT=n/a\n'
	printf 'STATE=unavailable\n'
	exit 1
fi

if ! jq -s . "$ledger" >/dev/null 2>&1; then
	printf 'REFLECTION=failed\n'
	printf 'REASON=invalid-ledger\n'
	printf 'REPORT=n/a\n'
	printf 'STATE=unavailable\n'
	exit 1
fi

analysis="$(
	jq -s \
		--arg scope "$scope" \
		--arg capability "$capability" \
		--arg kind "$kind" \
		--arg since "$since" \
		'
		[
			.[]?
			| select(($since == "") or ((.timestamp // "") >= $since))
			| select($scope == "all" or ((.capability.id // .sigil // "") == $capability))
			| select($kind == "" or ((.capability.kind // "sigil") == $kind))
		] as $signals
		| {
			count: ($signals | length),
			status_counts: ($signals | group_by(.execution.status // "unknown") | map({key: (.[0].execution.status // "unknown"), value: length}) | from_entries),
			quality_counts: ($signals | group_by(.observer.quality_bar_status // "unknown") | map({key: (.[0].observer.quality_bar_status // "unknown"), value: length}) | from_entries),
			recommendation_counts: ($signals | group_by(.observer.recommendation // "unknown") | map({key: (.[0].observer.recommendation // "unknown"), value: length}) | from_entries),
			thresholds: ([ $signals[]? | .observer.reflection_trigger // "none" | select(. != "none") ] | unique),
			severe_gaps: ([ $signals[]? | (.observer.workflow_gaps // [])[]? | select(.severity == "severe" or .severity == "high") ] | length),
			output_drift: ([ $signals[]? | select(.observer.output_contract_drift == true) ] | length),
			reflect_now: ([ $signals[]? | select(.observer.recommendation == "reflect-now") ] | length),
			capabilities: ([ $signals[]? | {id: (.capability.id // .sigil // "unknown"), kind: (.capability.kind // "sigil")} ] | unique)
		}
		' "$ledger"
)"

signals_analyzed="$(printf '%s\n' "$analysis" | jq -r '.count')"
thresholds_csv="$(printf '%s\n' "$analysis" | jq -r 'if (.thresholds | length) == 0 then "none" else (.thresholds | join(",")) end')"
reflect_now_count="$(printf '%s\n' "$analysis" | jq -r '.reflect_now')"

if [[ "$thresholds_csv" == "none" && "$reflect_now_count" -eq 0 ]]; then
	if [[ "$signals_analyzed" -lt "$min_signals" ]]; then
		printf 'REFLECTION=skipped\n'
		printf 'REASON=insufficient-signals\n'
		printf 'SIGNALS_ANALYZED=%s\n' "$signals_analyzed"
		printf 'THRESHOLDS_TRIGGERED=%s\n' "$thresholds_csv"
		printf 'REPORT=n/a\n'
		printf 'STATE=unchanged\n'
		exit 0
	fi
	printf 'REFLECTION=skipped\n'
	printf 'REASON=no-threshold\n'
	printf 'SIGNALS_ANALYZED=%s\n' "$signals_analyzed"
	printf 'THRESHOLDS_TRIGGERED=none\n'
	printf 'REPORT=n/a\n'
	printf 'STATE=unchanged\n'
	exit 0
fi

if [[ "$dry_run" == "1" ]]; then
	printf 'REFLECTION=skipped\n'
	printf 'REASON=dry-run\n'
	printf 'SIGNALS_ANALYZED=%s\n' "$signals_analyzed"
	printf 'THRESHOLDS_TRIGGERED=%s\n' "$thresholds_csv"
	printf 'REPORT=n/a\n'
	printf 'STATE=unchanged\n'
	exit 0
fi

mkdir -p "$reports_dir"
safe_timestamp="$(date -u +%Y%m%dT%H%M%SZ)"
safe_scope="$scope"
if [[ "$scope" == "capability" ]]; then
	safe_scope="${capability//[^A-Za-z0-9._-]/-}"
fi
report="$reports_dir/${safe_timestamp}-${safe_scope}-reflection.md"

{
	printf '# Invocation Signal Reflection\n\n'
	printf '## Scope\n\n'
	printf -- '- Scope: `%s`\n' "$scope"
	if [[ -n "$capability" ]]; then
		printf -- '- Capability: `%s`\n' "$capability"
	fi
	if [[ -n "$kind" ]]; then
		printf -- '- Kind: `%s`\n' "$kind"
	fi
	if [[ -n "$since" ]]; then
		printf -- '- Since: `%s`\n' "$since"
	fi
	printf -- '- Signals analyzed: `%s`\n' "$signals_analyzed"
	printf -- '- Thresholds triggered: `%s`\n' "$thresholds_csv"
	printf '\n## Signal Summary\n\n'
	printf '```json\n'
	printf '%s\n' "$analysis" | jq .
	printf '```\n\n'
	printf '## Proposed Iterations\n\n'
	printf -- '- Review threshold-backed gaps before mutating any capability.\n'
	printf -- '- Route approved capability changes through the appropriate lifecycle spell or sigil.\n'
	printf '\n## Contract Preservation\n\n'
	printf -- '- This reflection report did not edit observed capabilities.\n'
	printf -- '- Hook operation rows remain separate from capability telemetry.\n'
	printf '\n## Decision\n\n'
	printf -- '- Recommended next action: targeted update\n'
} > "$report"

state_status="unavailable"
if [[ -f "$reflection_state" ]]; then
	tmp_state="$(mktemp)"
	if jq --arg timestamp "$(date -u +%Y-%m-%dT%H:%M:%SZ)" '.last_reflection_at = $timestamp' "$reflection_state" > "$tmp_state"; then
		mv "$tmp_state" "$reflection_state"
		state_status="updated"
	else
		rm -f "$tmp_state"
		state_status="unchanged"
	fi
fi

printf 'REFLECTION=written\n'
printf 'REASON=threshold-hit\n'
printf 'SIGNALS_ANALYZED=%s\n' "$signals_analyzed"
printf 'THRESHOLDS_TRIGGERED=%s\n' "$thresholds_csv"
printf 'REPORT=%s\n' "$report"
printf 'STATE=%s\n' "$state_status"
