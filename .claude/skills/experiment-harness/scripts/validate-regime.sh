#!/usr/bin/env bash
set -euo pipefail

usage() {
	cat <<'USAGE'
Usage:
  validate-regime.sh <artifact-path> <regime-id>

Validates one loop regime definition without running Codex.
USAGE
}

if [[ "$#" -ne 2 ]]; then
	usage >&2
	exit 2
fi

artifact="$1"
regime_id="$2"

if [[ ! -d "$artifact" ]]; then
	printf 'ERROR: artifact path not found: %s\n' "$artifact" >&2
	exit 1
fi

artifact_abs="$(cd "$artifact" && pwd)"
repo_root="${EXPERIMENT_REPO_ROOT:-$(git -C "$PWD" rev-parse --show-toplevel 2>/dev/null || pwd)}"
dev_dir="$artifact_abs/development"
regime="$dev_dir/regimes/$regime_id.md"

failures=0

fail() {
	printf 'FAIL: %s\n' "$1"
	failures=$((failures + 1))
}

require_file() {
	if [[ ! -f "$1" ]]; then
		fail "missing file: ${1#$repo_root/}"
	fi
}

require_pattern() {
	local file="$1"
	local pattern="$2"
	local label="$3"
	if [[ ! -f "$file" ]] || ! rg -q -- "$pattern" "$file"; then
		fail "$label missing pattern: $pattern"
	fi
}

require_file "$regime"

if [[ -f "$regime" ]]; then
	require_pattern "$regime" "^# Regime: $regime_id" "regime heading"
	require_pattern "$regime" '^## Goal' "goal section"
	require_pattern "$regime" '^## Prompt' "prompt section"
	require_pattern "$regime" '^## Required Output Patterns' "required output patterns section"
	require_pattern "$regime" '^## Quality Bar' "quality bar section"
	require_pattern "$regime" '^## Anti-Patterns' "anti-patterns section"
	require_pattern "$regime" '^## Observability' "observability section"
	require_pattern "$regime" '^## Lessons To Capture' "lessons section"

	prompt_rel="$(sed -n 's/^- Prompt: `\(.*\)`/\1/p' "$regime" | head -n 1)"
	if [[ -z "$prompt_rel" ]]; then
		fail "regime does not declare a prompt path"
	else
		require_file "$dev_dir/$prompt_rel"
	fi

	pattern_count="$(awk '
		/^## Required Output Patterns/ {inside=1; next}
		/^## / {inside=0}
		inside && /^- `/ {count++}
		END {print count+0}
	' "$regime")"
	if [[ "$pattern_count" -eq 0 ]]; then
		fail "regime declares no required output patterns"
	fi
fi

if [[ "$failures" -gt 0 ]]; then
	printf 'REGIME_VALIDATION=block\n'
	exit 1
fi

printf 'REGIME_VALIDATION=pass\n'
printf 'REGIME=%s\n' "$regime_id"
printf 'REGIME_FILE=%s\n' "${regime#$repo_root/}"
