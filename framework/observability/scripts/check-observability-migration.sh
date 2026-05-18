#!/usr/bin/env bash
set -euo pipefail

usage() {
	cat <<'USAGE'
Usage:
  check-observability-migration.sh [--observability-dir <path>]

Checks whether the central invocation ledger can be summarized through the
generic capability shape without anonymous capability groups. Legacy rows may
omit capability.id/kind as long as sigil and tier fields can be used as a
compatibility fallback.
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
	printf 'MIGRATION_CHECK=failed\n'
	printf 'REASON=jq not found\n'
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
	printf 'MIGRATION_CHECK=failed\n'
	printf 'REASON=ledger not found\n'
	printf 'LEDGER=%s\n' "$ledger"
	exit 1
fi

if ! jq -s . "$ledger" >/dev/null 2>&1; then
	printf 'MIGRATION_CHECK=failed\n'
	printf 'REASON=invalid-ledger\n'
	printf 'LEDGER=%s\n' "$ledger"
	exit 1
fi

summary="$(
	jq -s '
		[
			.[]?
			| {
				id: (.capability.id // .sigil // ""),
				kind: (.capability.kind // (if (.capability.id? or .sigil?) then "sigil" else "" end)),
				legacy: ((.capability.id? | not) or (.capability.kind? | not))
			}
		] as $rows
		| {
			total: ($rows | length),
			anonymous: ([$rows[] | select(.id == "" or .kind == "")] | length),
			legacy_fallback: ([$rows[] | select(.legacy == true and .id != "" and .kind != "")] | length),
			groups: ($rows
				| map(select(.id != "" and .kind != ""))
				| group_by(.kind + ":" + .id)
				| map({key: (.[0].kind + ":" + .[0].id), value: length})
				| from_entries)
		}
	' "$ledger"
)"

anonymous="$(printf '%s\n' "$summary" | jq -r '.anonymous')"
if [[ "$anonymous" != "0" ]]; then
	printf 'MIGRATION_CHECK=failed\n'
	printf 'REASON=anonymous-capability-groups\n'
	printf 'ANONYMOUS=%s\n' "$anonymous"
	printf 'SUMMARY=%s\n' "$summary"
	exit 1
fi

printf 'MIGRATION_CHECK=pass\n'
printf 'ANONYMOUS=0\n'
printf 'LEGACY_FALLBACK=%s\n' "$(printf '%s\n' "$summary" | jq -r '.legacy_fallback')"
printf 'SUMMARY=%s\n' "$summary"
