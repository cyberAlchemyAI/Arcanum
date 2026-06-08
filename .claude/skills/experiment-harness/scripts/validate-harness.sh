#!/usr/bin/env bash
set -euo pipefail

usage() {
	cat <<'USAGE'
Usage:
  validate-harness.sh <artifact-path>
USAGE
}

if [[ "$#" -ne 1 ]]; then
	usage >&2
	exit 2
fi

artifact="$1"
if [[ ! -d "$artifact" ]]; then
	printf 'ERROR: artifact path not found: %s\n' "$artifact" >&2
	exit 1
fi

artifact_abs="$(cd "$artifact" && pwd)"
dev_dir="$artifact_abs/development"
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
contract_checker="$script_dir/check-contract-output.sh"
repo_root="${EXPERIMENT_REPO_ROOT:-$(git -C "$PWD" rev-parse --show-toplevel 2>/dev/null || pwd)}"
profile_dir="$script_dir/../templates/profiles"
status="pass"
profile_validation="pass"
profile_id=""
lifecycle_owner=""
artifact_type=""
contract_path=""
prompt_set=""
regime_set=""
overall_quality_bar_status="not_checked"
overall_anti_pattern_hits_json='[]'
overall_workflow_gaps_json='[]'

merge_json_arrays() {
	local left="$1"
	local right="$2"
	jq -cn --argjson left "$left" --argjson right "$right" '$left + $right'
}

merge_quality_status() {
	local current="$1"
	local next="$2"
	case "$current:$next" in
		*fail*|fail:*) printf 'fail\n' ;;
		*partial*|partial:*) printf 'partial\n' ;;
		pass:*|*:pass) printf 'pass\n' ;;
		*) printf 'not_checked\n' ;;
	esac
}

flag() {
	if [[ "$status" != "block" ]]; then
		status="flag"
	fi
	printf 'FLAG: %s\n' "$1"
}

block() {
	status="block"
	if [[ "${2:-}" == "profile" ]]; then
		profile_validation="block"
	fi
	printf 'BLOCK: %s\n' "$1"
}

require_file() {
	if [[ ! -f "$1" ]]; then
		block "missing required file: ${1#$artifact_abs/}"
	fi
}

require_dir() {
	if [[ ! -d "$1" ]]; then
		block "missing required directory: ${1#$artifact_abs/}"
	fi
}

require_dir "$dev_dir"
require_file "$dev_dir/VALIDATION-EXPERIMENT.md"
require_file "$dev_dir/VALIDATION.md"
require_dir "$dev_dir/fixtures"
require_dir "$dev_dir/runs"

trim() {
	local value="$1"
	value="${value#"${value%%[![:space:]]*}"}"
	value="${value%"${value##*[![:space:]]}"}"
	printf '%s' "$value"
}

metadata_value() {
	local label="$1"
	local file="$2"
	sed -n "s/^- $label: //p" "$file" | head -n 1
}

resolve_profile_path() {
	local value="$1"
	if [[ "$value" = /* ]]; then
		printf '%s\n' "$value"
	else
		printf '%s\n' "$repo_root/$value"
	fi
}

validate_profile() {
	local profile_file="$dev_dir/EXPERIMENT-PROFILE.md"
	if [[ ! -f "$profile_file" ]]; then
		block "missing required profile metadata: development/EXPERIMENT-PROFILE.md" profile
		return
	fi

	profile_id="$(metadata_value "Profile ID" "$profile_file")"
	artifact_type="$(metadata_value "Artifact type" "$profile_file")"
	lifecycle_owner="$(metadata_value "Lifecycle owner" "$profile_file")"
	contract_path="$(metadata_value "Contract path" "$profile_file")"
	prompt_set="$(metadata_value "Prompt set" "$profile_file")"
	regime_set="$(metadata_value "Regime set" "$profile_file")"

	if [[ -z "$profile_id" ]]; then
		block "profile metadata is missing Profile ID" profile
		return
	fi

	local profile_template="$profile_dir/$profile_id.profile.sh"
	if [[ ! -f "$profile_template" ]]; then
		block "unknown experiment profile: $profile_id" profile
		return
	fi

	# shellcheck source=/dev/null
	source "$profile_template"

	if [[ "$artifact_type" != "$PROFILE_ARTIFACT_TYPE" ]]; then
		block "profile $profile_id expects artifact type $PROFILE_ARTIFACT_TYPE but found $artifact_type" profile
	fi
	if [[ -z "$lifecycle_owner" ]]; then
		block "profile metadata is missing Lifecycle owner" profile
	elif [[ "$lifecycle_owner" != "$PROFILE_LIFECYCLE_OWNER" ]]; then
		block "profile $profile_id expects lifecycle owner $PROFILE_LIFECYCLE_OWNER but found $lifecycle_owner" profile
	fi
	if [[ "$prompt_set" != "$PROFILE_PROMPT_SET" ]]; then
		block "profile prompt set does not match template for $profile_id" profile
	fi
	if [[ "$regime_set" != "$PROFILE_REGIME_SET" ]]; then
		block "profile regime set does not match template for $profile_id" profile
	fi
	if [[ -z "$contract_path" ]]; then
		block "profile metadata is missing Contract path" profile
	else
		resolved_contract="$(resolve_profile_path "$contract_path")"
		if [[ ! -f "$resolved_contract" ]]; then
			block "profile contract path is unreadable: $contract_path" profile
		fi
	fi
	if ! rg -q -- '^## Ownership Boundary' "$profile_file"; then
		block "profile metadata is missing ownership boundary" profile
	fi

	for prompt_id in "${PROFILE_PROMPT_IDS[@]}"; do
		prompt_file="$dev_dir/example-prompts/$prompt_id.md"
		if [[ ! -f "$prompt_file" ]]; then
			block "profile prompt missing: development/example-prompts/$prompt_id.md" profile
			continue
		fi
		if ! rg -q -- "$PROFILE_LIFECYCLE_OWNER" "$prompt_file"; then
			flag "profile prompt does not mention lifecycle owner $PROFILE_LIFECYCLE_OWNER: ${prompt_file#$artifact_abs/}"
		fi
	done

	for regime_id in "${PROFILE_REGIME_IDS[@]}"; do
		regime_file="$dev_dir/regimes/$regime_id.md"
		if [[ ! -f "$regime_file" ]]; then
			block "profile regime missing: development/regimes/$regime_id.md" profile
			continue
		fi
		regime_result="$("$script_dir/validate-regime.sh" "$artifact_abs" "$regime_id" || true)"
		printf '%s\n' "$regime_result"
		regime_validation="$(printf '%s\n' "$regime_result" | sed -n 's/^REGIME_VALIDATION=//p' | tail -n 1)"
		if [[ "$regime_validation" == "block" ]]; then
			block "profile regime validation failed: $regime_id" profile
		fi
	done
}

validate_profile

for optional_dir in example-prompts example-outputs example-runs; do
	if [[ ! -d "$dev_dir/$optional_dir" ]]; then
		flag "missing optional runtime evidence directory: development/$optional_dir"
	fi
done

if [[ -d "$dev_dir/fixtures" ]]; then
	fixture_count="$(find "$dev_dir/fixtures" -maxdepth 1 -type f -name '*.md' ! -name '*.expected.md' | wc -l | tr -d ' ')"
	expected_count="$(find "$dev_dir/fixtures" -maxdepth 1 -type f -name '*.expected.md' | wc -l | tr -d ' ')"
	if [[ "$fixture_count" -eq 0 ]]; then
		flag "no fixture inputs found"
	fi
	if [[ "$expected_count" -eq 0 ]]; then
		flag "no expected fixture outputs found"
	fi
	while IFS= read -r fixture; do
		name="$(basename "$fixture" .md)"
		if [[ "$name" == *.* ]]; then
			continue
		fi
		base="${fixture%.md}"
		if [[ ! -f "$base.expected.md" ]] && ! compgen -G "$base.*.expected.md" >/dev/null; then
			flag "fixture missing expected pair: ${fixture#$artifact_abs/}"
		fi
	done < <(find "$dev_dir/fixtures" -maxdepth 1 -type f -name '*.md' ! -name '*.expected.md' | sort)
fi

if [[ -d "$dev_dir/example-outputs" ]]; then
	while IFS= read -r output; do
		if [[ ! -s "$output" ]]; then
			block "example output is empty: ${output#$artifact_abs/}"
			continue
		fi
		if rg -q -- '^Saved the .*output to |^Saved .* to \[' "$output"; then
			block "example output is a save-summary, not a real artifact body: ${output#$artifact_abs/}"
		fi
		if ! rg -q -- '^## .+Result|^# .+Result|^## Gate Result|^## Spell Result|^## Sigil .*Result' "$output"; then
			flag "example output has no recognizable result heading: ${output#$artifact_abs/}"
		fi
		if [[ -x "$contract_checker" ]]; then
			contract_result="$("$contract_checker" "$artifact_abs" "$output" || true)"
			printf '%s\n' "$contract_result"
			contract_validation="$(printf '%s\n' "$contract_result" | sed -n 's/^VALIDATION=//p' | tail -n 1)"
			contract_quality="$(printf '%s\n' "$contract_result" | sed -n 's/^QUALITY_BAR_STATUS=//p' | tail -n 1)"
			contract_anti_hits="$(printf '%s\n' "$contract_result" | sed -n 's/^ANTI_PATTERN_HITS_JSON=//p' | tail -n 1)"
			contract_gaps="$(printf '%s\n' "$contract_result" | sed -n 's/^WORKFLOW_GAPS_JSON=//p' | tail -n 1)"
			if [[ -n "$contract_quality" ]]; then
				overall_quality_bar_status="$(merge_quality_status "$overall_quality_bar_status" "$contract_quality")"
			fi
			if [[ -n "$contract_anti_hits" ]] && printf '%s\n' "$contract_anti_hits" | jq -e . >/dev/null 2>&1; then
				overall_anti_pattern_hits_json="$(merge_json_arrays "$overall_anti_pattern_hits_json" "$contract_anti_hits")"
			fi
			if [[ -n "$contract_gaps" ]] && printf '%s\n' "$contract_gaps" | jq -e . >/dev/null 2>&1; then
				overall_workflow_gaps_json="$(merge_json_arrays "$overall_workflow_gaps_json" "$contract_gaps")"
			fi
			case "$contract_validation" in
				block) block "contract output check blocked: ${output#$artifact_abs/}" ;;
				flag) flag "contract output check flagged: ${output#$artifact_abs/}" ;;
			esac
		fi
	done < <(find "$dev_dir/example-outputs" -maxdepth 1 -type f -name '*.output.md' | sort)
fi

if [[ -d "$dev_dir/live-evidence" ]]; then
	while IFS= read -r output; do
		if [[ ! -s "$output" ]]; then
			block "live evidence output is empty: ${output#$artifact_abs/}"
			continue
		fi
		if [[ -x "$contract_checker" ]]; then
			contract_result="$("$contract_checker" "$artifact_abs" "$output" || true)"
			printf '%s\n' "$contract_result"
			contract_validation="$(printf '%s\n' "$contract_result" | sed -n 's/^VALIDATION=//p' | tail -n 1)"
			contract_quality="$(printf '%s\n' "$contract_result" | sed -n 's/^QUALITY_BAR_STATUS=//p' | tail -n 1)"
			contract_anti_hits="$(printf '%s\n' "$contract_result" | sed -n 's/^ANTI_PATTERN_HITS_JSON=//p' | tail -n 1)"
			contract_gaps="$(printf '%s\n' "$contract_result" | sed -n 's/^WORKFLOW_GAPS_JSON=//p' | tail -n 1)"
			if [[ -n "$contract_quality" ]]; then
				overall_quality_bar_status="$(merge_quality_status "$overall_quality_bar_status" "$contract_quality")"
			fi
			if [[ -n "$contract_anti_hits" ]] && printf '%s\n' "$contract_anti_hits" | jq -e . >/dev/null 2>&1; then
				overall_anti_pattern_hits_json="$(merge_json_arrays "$overall_anti_pattern_hits_json" "$contract_anti_hits")"
			fi
			if [[ -n "$contract_gaps" ]] && printf '%s\n' "$contract_gaps" | jq -e . >/dev/null 2>&1; then
				overall_workflow_gaps_json="$(merge_json_arrays "$overall_workflow_gaps_json" "$contract_gaps")"
			fi
			case "$contract_validation" in
				block) block "live evidence contract check blocked: ${output#$artifact_abs/}" ;;
				flag) flag "live evidence contract check flagged: ${output#$artifact_abs/}" ;;
			esac
		fi
	done < <(find "$dev_dir/live-evidence" -type f -name 'output.md' | sort)
fi

latest_report="$(find "$dev_dir/runs" -maxdepth 1 -type f -name '*.md' 2>/dev/null | sort | tail -n 1 || true)"
if [[ -z "$latest_report" ]]; then
	if ! find "$dev_dir/live-evidence" -type f -name 'loop-report.md' 2>/dev/null | read -r _; then
		flag "no timestamped validation report found under development/runs"
	fi
else
	if ! rg -q -- 'Validation: pass|Validation: flag|Validation: block|Status: pass|Status: flag|Status: block' "$latest_report"; then
		flag "latest report does not expose a validation status: ${latest_report#$artifact_abs/}"
	fi
	if [[ -n "$profile_id" ]] && ! rg -q -- "PROFILE_ID=$profile_id|- Profile ID: $profile_id" "$latest_report"; then
		flag "latest report does not expose profile id: ${latest_report#$artifact_abs/}"
	fi
	if [[ -n "$lifecycle_owner" ]] && ! rg -q -- "LIFECYCLE_OWNER=$lifecycle_owner|- Lifecycle owner: $lifecycle_owner" "$latest_report"; then
		flag "latest report does not expose lifecycle owner: ${latest_report#$artifact_abs/}"
	fi
fi

printf 'VALIDATION=%s\n' "$status"
printf 'PROFILE_VALIDATION=%s\n' "$profile_validation"
printf 'PROFILE_ID=%s\n' "$profile_id"
printf 'LIFECYCLE_OWNER=%s\n' "$lifecycle_owner"
printf 'ARTIFACT_TYPE=%s\n' "$artifact_type"
printf 'CONTRACT_PATH=%s\n' "$contract_path"
printf 'PROMPT_SET=%s\n' "$prompt_set"
printf 'REGIME_SET=%s\n' "$regime_set"
printf 'QUALITY_BAR_STATUS=%s\n' "$overall_quality_bar_status"
printf 'ANTI_PATTERN_HITS_JSON=%s\n' "$overall_anti_pattern_hits_json"
printf 'WORKFLOW_GAPS_JSON=%s\n' "$overall_workflow_gaps_json"

if [[ "$status" == "block" ]]; then
	exit 1
fi

exit 0
