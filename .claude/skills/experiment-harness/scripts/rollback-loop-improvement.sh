#!/usr/bin/env bash
set -euo pipefail

usage() {
	cat <<'USAGE'
Usage:
  rollback-loop-improvement.sh <attempt-dir>

Reverts attempt-dir/patch.diff when it was applied.
USAGE
}

if [[ "$#" -ne 1 ]]; then
	usage >&2
	exit 2
fi

attempt_dir="$1"
patch="$attempt_dir/patch.diff"
applied="$attempt_dir/patch-applied.txt"

if [[ ! -s "$patch" || ! -f "$applied" || "$(cat "$applied")" != "true" ]]; then
	printf 'ROLLBACK=false\n'
	printf 'REASON=no applied patch\n'
	exit 0
fi

if ! git apply -R --check "$patch"; then
	printf 'ROLLBACK=false\n'
	printf 'REASON=reverse patch does not apply cleanly\n'
	exit 1
fi

git apply -R "$patch"
printf 'ROLLBACK=true\n'
printf 'PATCH=%s\n' "$patch"
printf 'false\n' > "$applied"
