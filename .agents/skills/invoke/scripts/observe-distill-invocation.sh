#!/usr/bin/env bash
set -euo pipefail

usage() {
	cat <<'USAGE'
Usage:
  observe-distill-invocation.sh --envelope <path> [--observability-dir <path>] [--observer-version <version>]

Validates one Invoke-owned Distill child invocation envelope and delegates the
exactly-once append to the canonical Signal Observer runtime.
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
def artifact_ref:
	type == "object"
	and (.path | non_empty_string)
	and (.sha256 | type == "string" and test("^[a-f0-9]{64}$"))
	and (.size_bytes | type == "number" and floor == . and . >= 0);

[
	(if ((.run_id // "") | non_empty_string) then empty else "missing child run_id" end),
	(if .run_id != (.lineage.parent_run_id // null) then empty else "child run_id must differ from parent run id" end),
	(if (.capability.id // .sigil) == "distill" then empty else "capability must be distill" end),
	(if (.capability.kind // "sigil") == "sigil" then empty else "Distill capability kind must be sigil" end),
	(if ((.mode // .capability.mode) | IN("compact", "standard", "tournament", "deep", "validate")) then empty else "invalid Distill mode" end),
	(if ((.lineage.parent_run_id // "") | non_empty_string) then empty else "missing lineage.parent_run_id" end),
	(if .lineage.relation == "invoked-by" then empty else "lineage.relation must be invoked-by" end),
	(if .lineage.caller.id == "invoke" then empty else "lineage caller must be invoke" end),
	(if .lineage.caller.kind == "spell" then empty else "lineage caller kind must be spell" end),
	(if ((.lineage.caller.mode // "") | non_empty_string) then empty else "missing Invoke caller mode" end),
	(if (.execution.status | IN("completed", "partial", "blocked", "failed")) then empty else "child execution must be completed, partial, blocked, or failed" end),
	(if (.evidence.status | IN("complete", "partial", "unavailable")) then empty else "invalid evidence status" end),
	(if (.evidence.distill_run_request_ref | artifact_ref) then empty else "invalid Distill run request reference" end),
	(if ((.evidence.runtime_event_refs // []) | type == "array") then empty else "runtime_event_refs must be an array" end),
	(if ((.evidence.runtime_event_refs // []) | all(.[]; artifact_ref)) then empty else "invalid runtime event reference" end),
	(if .evidence.status != "complete" or (.evidence.execution_receipt_ref | artifact_ref) then empty else "complete evidence requires an execution receipt reference" end),
	(if .evidence.status != "complete" or (.evidence.validation_result_ref | artifact_ref) then empty else "complete evidence requires a validation result reference" end)
]
'

validation_errors="$(jq -r "$validation_filter | .[]" "$envelope")"
if [[ -n "$validation_errors" ]]; then
	printf 'OBSERVATION=failed\n'
	printf 'REASON=invalid Invoke-to-Distill envelope\n'
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
