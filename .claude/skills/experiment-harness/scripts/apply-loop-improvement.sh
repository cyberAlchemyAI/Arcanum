#!/usr/bin/env bash
set -euo pipefail

usage() {
	cat <<'USAGE'
Usage:
  apply-loop-improvement.sh <attempt-dir>

Applies attempt-dir/patch.diff when present. Empty or missing patches are a no-op.
USAGE
}

if [[ "$#" -ne 1 ]]; then
	usage >&2
	exit 2
fi

attempt_dir="$1"
patch="$attempt_dir/patch.diff"
applied="$attempt_dir/patch-applied.txt"

if [[ ! -s "$patch" ]]; then
	printf 'PATCH_APPLIED=false\n'
	printf 'REASON=no patch.diff present\n'
	printf 'false\n' > "$applied"
	exit 0
fi

if ! git apply --check "$patch"; then
	printf 'PATCH_APPLIED=false\n'
	printf 'REASON=patch does not apply cleanly\n'
	printf 'false\n' > "$applied"
	exit 1
fi

git apply "$patch"
printf 'PATCH_APPLIED=true\n'
printf 'PATCH=%s\n' "$patch"
printf 'true\n' > "$applied"
