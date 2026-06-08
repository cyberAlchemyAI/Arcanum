#!/usr/bin/env bash
set -euo pipefail

usage() {
	cat <<'USAGE'
Usage:
  check-contract-output.sh <artifact-path> <output-path>

Extracts <quality-bar> and <anti-patterns> from SKILL.md when present and
checks one saved experiment output for observable quality and anti-pattern hits.
USAGE
}

if [[ "$#" -ne 2 ]]; then
	usage >&2
	exit 2
fi

artifact="$1"
output="$2"

if [[ ! -d "$artifact" ]]; then
	printf 'ERROR: artifact path not found: %s\n' "$artifact" >&2
	exit 1
fi

if [[ ! -f "$output" ]]; then
	printf 'ERROR: output not found: %s\n' "$output" >&2
	exit 1
fi

artifact_abs="$(cd "$artifact" && pwd)"
repo_root="${EXPERIMENT_REPO_ROOT:-$(git -C "$PWD" rev-parse --show-toplevel 2>/dev/null || pwd)}"
skill="$artifact_abs/SKILL.md"
output_rel="${output#$repo_root/}"

quality_bar_status="not_checked"
validation="pass"
anti_hits=()
workflow_gaps=()

json_array() {
	if [[ "$#" -eq 0 ]]; then
		printf '[]\n'
		return 0
	fi
	printf '%s\n' "$@" | jq -Rsc 'split("\n")[:-1]'
}

add_gap() {
	local category="$1"
	local severity="$2"
	local summary="$3"
	local evidence="$4"
	workflow_gaps+=("$(
		jq -cn \
			--arg category "$category" \
			--arg severity "$severity" \
			--arg summary "$summary" \
			--arg evidence "$evidence" \
			'{
				category: $category,
				severity: $severity,
				summary: $summary,
				evidence: $evidence
			}'
	)")
}

add_hit() {
	local summary="$1"
	anti_hits+=("$summary")
}

extract_section() {
	local file="$1"
	local start="$2"
	local end="$3"
	awk -v start="$start" -v end="$end" '
		$0 ~ start {inside=1; next}
		$0 ~ end {inside=0}
		inside {print}
	' "$file"
}

quality_criteria_count=0
anti_pattern_count=0

if [[ -f "$skill" ]]; then
	quality_criteria_count="$(extract_section "$skill" '<quality-bar>' '</quality-bar>' | rg -c '^[[:space:]]*-' || true)"
	anti_pattern_count="$(extract_section "$skill" '<anti-patterns>' '</anti-patterns>' | rg -c '^[[:space:]]*-' || true)"

	if [[ "$quality_criteria_count" -eq 0 ]]; then
		quality_bar_status="partial"
		add_gap "quality-bar" "medium" "SKILL.md has no concrete quality-bar criteria" "${skill#$repo_root/}"
		validation="flag"
	else
		quality_bar_status="pass"
	fi

	if [[ "$anti_pattern_count" -eq 0 ]]; then
		add_gap "anti-pattern" "medium" "SKILL.md has no concrete anti-pattern criteria" "${skill#$repo_root/}"
		if [[ "$validation" != "block" ]]; then
			validation="flag"
		fi
	fi
fi

if [[ ! -s "$output" ]]; then
	quality_bar_status="fail"
	add_gap "output-contract" "severe" "output is empty" "$output_rel"
	validation="block"
fi

if rg -q -- '^Saved the .*output to |^Saved .* to \[' "$output"; then
	quality_bar_status="fail"
	add_hit "save-summary output instead of artifact body"
	add_gap "output-contract" "severe" "output is a save-summary, not a real artifact body" "$output_rel"
	validation="block"
fi

if ! rg -q -- '^## .+Result|^# .+Result|^## Gate Result|^## Spell Result|^## Sigil .*Result' "$output"; then
	if [[ "$quality_bar_status" == "pass" ]]; then
		quality_bar_status="partial"
	fi
	add_gap "output-contract" "medium" "output has no recognizable result heading" "$output_rel"
	if [[ "$validation" == "pass" ]]; then
		validation="flag"
	fi
fi

if rg -q -- 'TODO|TBD|\{\{[^}]+\}\}|<[^>[:space:]]+>' "$output"; then
	add_hit "placeholder or unresolved template marker left in output"
	add_gap "template" "medium" "output contains TODO/TBD or template placeholder markers" "$output_rel"
	if [[ "$quality_bar_status" == "pass" ]]; then
		quality_bar_status="partial"
	fi
	if [[ "$validation" == "pass" ]]; then
		validation="flag"
	fi
fi

if rg -q -- 'Phase status:[[:space:]]*pass' "$output" && rg -qi -- 'missing required (evidence|input|source|contract)|blocked by|cannot proceed|no approved (source|contract|input|define|glossary)|not provided' "$output"; then
	add_hit "pass status with blocker or missing-required language"
	add_gap "quality-bar" "high" "output claims pass while naming blocker or missing required evidence" "$output_rel"
	quality_bar_status="fail"
	validation="block"
fi

anti_json="$(json_array "${anti_hits[@]}")"
if [[ "${#workflow_gaps[@]}" -eq 0 ]]; then
	gaps_json='[]'
else
	gaps_json="$(printf '%s\n' "${workflow_gaps[@]}" | jq -sc '.')"
fi

printf 'CONTRACT_OUTPUT=%s\n' "$output_rel"
printf 'QUALITY_BAR_STATUS=%s\n' "$quality_bar_status"
printf 'QUALITY_BAR_CRITERIA=%s\n' "$quality_criteria_count"
printf 'ANTI_PATTERN_CRITERIA=%s\n' "$anti_pattern_count"
printf 'ANTI_PATTERN_HITS_JSON=%s\n' "$anti_json"
printf 'WORKFLOW_GAPS_JSON=%s\n' "$gaps_json"
printf 'VALIDATION=%s\n' "$validation"
