#!/usr/bin/env bash
set -euo pipefail

usage() {
	cat <<'USAGE'
Usage:
  validate-loop-attempt.sh <artifact-path> <regime-id> <attempt-dir>
USAGE
}

if [[ "$#" -ne 3 ]]; then
	usage >&2
	exit 2
fi

artifact="$1"
regime_id="$2"
attempt_dir="$3"

if ! command -v jq >/dev/null 2>&1; then
	printf 'ERROR: jq not found\n' >&2
	exit 1
fi

artifact_abs="$(cd "$artifact" && pwd)"
repo_root="${EXPERIMENT_REPO_ROOT:-$(git -C "$PWD" rev-parse --show-toplevel 2>/dev/null || pwd)}"
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
regime="$artifact_abs/development/regimes/$regime_id.md"
output="$attempt_dir/output.md"
contract_checker="$script_dir/check-contract-output.sh"
contract_result="$attempt_dir/contract-output.txt"
validation_json="$attempt_dir/validation.json"
missing_patterns=()

status="pass"

set_status() {
	local next="$1"
	case "$status:$next" in
		block:*|*:block) status="block" ;;
		fail:*|*:fail) status="fail" ;;
		partial:*|*:partial) status="partial" ;;
		*) status="pass" ;;
	esac
}

json_array() {
	if [[ "$#" -eq 0 ]]; then
		printf '[]\n'
		return 0
	fi
	printf '%s\n' "$@" | jq -Rsc 'split("\n")[:-1]'
}

if [[ ! -f "$regime" ]]; then
	printf 'ERROR: regime not found: %s\n' "$regime" >&2
	exit 1
fi

if [[ ! -s "$output" ]]; then
	set_status block
	missing_patterns+=("output missing or empty")
else
	if "$contract_checker" "$artifact_abs" "$output" > "$contract_result" 2>&1; then
		:
	else
		:
	fi
	contract_validation="$(sed -n 's/^VALIDATION=//p' "$contract_result" | tail -n 1)"
	case "$contract_validation" in
		block) set_status block ;;
		flag) set_status partial ;;
	esac

	while IFS= read -r pattern; do
		if ! rg -q -- "$pattern" "$output"; then
			missing_patterns+=("$pattern")
			set_status partial
		fi
	done < <(awk '
		/^## Required Output Patterns/ {inside=1; next}
		/^## / {inside=0}
		inside && /^- `/ {
			line=$0
			sub(/^- `/, "", line)
			sub(/`[[:space:]]*$/, "", line)
			print line
		}
	' "$regime")
fi

quality="not_checked"
anti_hits='[]'
gaps='[]'
if [[ -f "$contract_result" ]]; then
	quality="$(sed -n 's/^QUALITY_BAR_STATUS=//p' "$contract_result" | tail -n 1)"
	anti_hits="$(sed -n 's/^ANTI_PATTERN_HITS_JSON=//p' "$contract_result" | tail -n 1)"
	gaps="$(sed -n 's/^WORKFLOW_GAPS_JSON=//p' "$contract_result" | tail -n 1)"
fi
if [[ -z "$quality" ]]; then
	quality="not_checked"
fi
if [[ -z "$anti_hits" ]] || ! printf '%s\n' "$anti_hits" | jq -e . >/dev/null 2>&1; then
	anti_hits='[]'
fi
if [[ -z "$gaps" ]] || ! printf '%s\n' "$gaps" | jq -e . >/dev/null 2>&1; then
	gaps='[]'
fi

missing_json="$(json_array "${missing_patterns[@]}")"

jq -n \
	--arg regime "$regime_id" \
	--arg status "$status" \
	--arg quality "$quality" \
	--argjson anti_hits "$anti_hits" \
	--argjson gaps "$gaps" \
	--argjson missing "$missing_json" \
	'{
		regime: $regime,
		status: $status,
		quality_bar_status: $quality,
		anti_pattern_hits: $anti_hits,
		workflow_gaps: $gaps,
		missing_patterns: $missing
	}' > "$validation_json"

printf 'ATTEMPT_VALIDATION=%s\n' "$status"
printf 'VALIDATION_JSON=%s\n' "${validation_json#$repo_root/}"

case "$status" in
	block|fail) exit 1 ;;
	*) exit 0 ;;
esac
