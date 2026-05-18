#!/usr/bin/env bash
set -euo pipefail

usage() {
	cat <<'USAGE'
Usage:
  rebuild-observability-indexes.sh [--observability-dir <path>]

Rebuilds by-sigil/ and by-capability/ lookup indexes from the central
signals/sigil-invocations.jsonl ledger. The central ledger is the only source
of truth; index rows contain ledger references, not full telemetry copies.
USAGE
}

observability_dir=""
while [[ "$#" -gt 0 ]]; do
	case "$1" in
		--observability-dir) observability_dir="$2"; shift 2 ;;
		--help|-h) usage; exit 0 ;;
		*) printf 'ERROR: unknown argument: %s\n' "$1" >&2; usage >&2; exit 2 ;;
	esac
done

if ! command -v jq >/dev/null 2>&1; then
	printf 'ERROR: jq not found\n' >&2
	exit 1
fi

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if ! repo_root="$(git -C "$script_dir" rev-parse --show-toplevel 2>/dev/null)"; then
	repo_root="$(cd "$script_dir/../.." && pwd)"
fi
if [[ -z "$observability_dir" ]]; then
	observability_dir="$repo_root/.arcanum/observability"
fi

ledger="$observability_dir/signals/sigil-invocations.jsonl"
if [[ ! -f "$ledger" ]]; then
	printf 'ERROR: central ledger not found: %s\n' "$ledger" >&2
	exit 1
fi

mkdir -p "$observability_dir/by-sigil" "$observability_dir/by-capability"
find "$observability_dir/by-sigil" -type f -name '*.jsonl' -delete
find "$observability_dir/by-capability" -type f -name '*.jsonl' -delete
: > "$observability_dir/by-sigil/.gitkeep"
: > "$observability_dir/by-capability/.gitkeep"

indexed=0
skipped=0
line_no=0

while IFS= read -r event || [[ -n "$event" ]]; do
	line_no=$((line_no + 1))
	if ! printf '%s\n' "$event" | jq -e . >/dev/null 2>&1; then
		skipped=$((skipped + 1))
		continue
	fi

	capability_id="$(printf '%s\n' "$event" | jq -r '.capability.id // .sigil // empty')"
	capability_kind="$(printf '%s\n' "$event" | jq -r '.capability.kind // "sigil"')"
	legacy_sigil="$(printf '%s\n' "$event" | jq -r '.sigil // .capability.id // empty')"
	if [[ -z "$capability_id" || -z "$legacy_sigil" ]]; then
		skipped=$((skipped + 1))
		continue
	fi

	safe_capability_id="${capability_id//[^A-Za-z0-9._-]/-}"
	safe_capability_kind="${capability_kind//[^A-Za-z0-9._-]/-}"
	safe_sigil="${legacy_sigil//[^A-Za-z0-9._-]/-}"
	mkdir -p "$observability_dir/by-capability/$safe_capability_kind"

	index_event="$(
		printf '%s\n' "$event" | jq -c \
			--arg ledger "signals/sigil-invocations.jsonl" \
			--argjson line "$line_no" \
			'{
				timestamp,
				run_id: (.run_id // null),
				session_id: (.session_id // null),
				dedupe_key: (.dedupe_key // null),
				ledger: $ledger,
				line: $line,
				sigil: (.sigil // .capability.id),
				capability: {
					id: (.capability.id // .sigil),
					kind: (.capability.kind // "sigil"),
					tier: (.capability.tier // .tier // "unknown"),
					mode: (.capability.mode // .mode // "execute")
				},
				execution_status: (.execution.status // null),
				reflection_trigger: (.observer.reflection_trigger // null),
				recommendation: (.observer.recommendation // null),
				target_artifact: (.target_artifact // null)
			}'
	)"
	printf '%s\n' "$index_event" >> "$observability_dir/by-capability/$safe_capability_kind/$safe_capability_id.jsonl"
	printf '%s\n' "$index_event" >> "$observability_dir/by-sigil/$safe_sigil.jsonl"
	indexed=$((indexed + 1))
done < "$ledger"

printf 'INDEXED=%s\n' "$indexed"
printf 'SKIPPED=%s\n' "$skipped"
printf 'SOURCE=%s\n' "$ledger"
printf 'INDEX_MODEL=central-ledger-reference\n'
