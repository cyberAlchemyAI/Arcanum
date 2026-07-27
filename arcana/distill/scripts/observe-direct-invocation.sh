#!/usr/bin/env bash
set -euo pipefail

usage() {
	cat <<'USAGE'
Usage:
  observe-direct-invocation.sh --envelope <path> [--observability-dir <path>] [--observer-version <version>]

Validates one direct Distill invocation envelope and delegates the exactly-once
append to the canonical Signal Observer runtime.
USAGE
}

if ! command -v jq >/dev/null 2>&1; then
	printf 'ERROR: jq not found\n' >&2
	exit 1
fi

envelope=""
observability_dir=""
observer_version="0.1.0"

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

if [[ -z "$envelope" || ! -f "$envelope" ]]; then
	printf 'ERROR: a readable --envelope is required\n' >&2
	exit 2
fi

validation_filter='
def non_empty_string: type == "string" and length > 0;

(.evidence.runtime_event_refs // []) as $runtime_refs
| (.evidence.emission_status // "") as $emission_status
| [
	(if ((.run_id // "") | non_empty_string) then empty else "missing direct run_id" end),
	(if (.capability.id // .sigil) == "distill" then empty else "capability must be distill" end),
	(if (.capability.kind // "sigil") == "sigil" then empty else "Distill capability kind must be sigil" end),
	(if ((.mode // .capability.mode) | IN("compact", "standard", "tournament", "deep", "validate")) then empty else "invalid Distill mode" end),
	(if (.lineage // null) == null then empty else "direct Distill telemetry must not carry caller lineage" end),
	(if (.invocation_source // "direct") == "direct" then empty else "invocation_source must be direct" end),
	(if (.execution.status | IN("completed", "partial", "blocked", "failed")) then empty else "direct execution must be completed, partial, blocked, or failed" end),
	(if (.evidence.status | IN("complete", "partial", "unavailable")) then empty else "invalid evidence status" end),
	(if ($emission_status | IN("complete", "partial", "failed", "not-required", "not-configured")) then empty else "invalid evidence emission status" end),
	(if ($runtime_refs | type) == "array" then empty else "runtime_event_refs must be an array" end),
	(if $emission_status != "complete" or (.evidence.status == "complete" and ($runtime_refs | length) > 0) then empty else "complete emission requires complete evidence and runtime event references" end),
	(if $emission_status != "partial" or (.evidence.status == "partial" and ($runtime_refs | length) > 0) then empty else "partial emission requires partial evidence and runtime event references" end),
	(if (($emission_status == "not-required" or $emission_status == "not-configured") | not) or (.evidence.status == "unavailable" and ($runtime_refs | length) == 0) then empty else "non-emitting status requires unavailable evidence and no runtime event references" end),
	(if (.evidence.mutation_handoff_allowed // false) == false then empty else "telemetry cannot authorize mutation handoff" end),
	(if (.evidence.verdict_authority // false) == false then empty else "telemetry cannot claim verdict authority" end)
]
'

validation_errors="$(jq -r "$validation_filter | .[]" "$envelope")"
if [[ -n "$validation_errors" ]]; then
	printf 'OBSERVATION=failed\n'
	printf 'REASON=invalid direct Distill envelope\n'
	printf '%s\n' "$validation_errors" | sed 's/^/ERROR: /' >&2
	exit 1
fi

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
arcanum_root="$(cd "$script_dir/../../.." && pwd)"
observer="$arcanum_root/framework/observability/scripts/observe-invocation.sh"

if [[ ! -x "$observer" ]]; then
	printf 'ERROR: Signal Observer runtime is not executable: %s\n' "$observer" >&2
	exit 1
fi

command=(
	"$observer"
	--envelope "$envelope"
	--observer-version "$observer_version"
)
if [[ -n "$observability_dir" ]]; then
	command+=(--observability-dir "$observability_dir")
fi

exec "${command[@]}"
