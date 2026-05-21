#!/usr/bin/env bash
set -euo pipefail

usage() {
	cat <<'USAGE'
Usage:
  report-harness.sh <artifact-path>

Writes a timestamped report. If .arcanum/observability exists, also appends
one signal-observer-compatible telemetry event unless EXPERIMENT_OBSERVE=0.
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
run_dir="$dev_dir/runs"
mkdir -p "$run_dir"

repo_root="${EXPERIMENT_REPO_ROOT:-$(git -C "$PWD" rev-parse --show-toplevel 2>/dev/null || pwd)}"

prompt_count="$(find "$dev_dir/example-prompts" -maxdepth 1 -type f -name '*.md' 2>/dev/null | wc -l | tr -d ' ')"
output_count="$(find "$dev_dir/example-outputs" -maxdepth 1 -type f -name '*.output.md' 2>/dev/null | wc -l | tr -d ' ')"
fixture_count="$(find "$dev_dir/fixtures" -maxdepth 1 -type f -name '*.md' ! -name '*.expected.md' 2>/dev/null | wc -l | tr -d ' ')"

validation_output="$("$dev_dir/run-validation-fixtures.sh" 2>&1 || true)"
validation="$(printf '%s\n' "$validation_output" | sed -n 's/^VALIDATION=//p' | tail -n 1)"
profile_validation="$(printf '%s\n' "$validation_output" | sed -n 's/^PROFILE_VALIDATION=//p' | tail -n 1)"
profile_id="$(printf '%s\n' "$validation_output" | sed -n 's/^PROFILE_ID=//p' | tail -n 1)"
lifecycle_owner="$(printf '%s\n' "$validation_output" | sed -n 's/^LIFECYCLE_OWNER=//p' | tail -n 1)"
artifact_type="$(printf '%s\n' "$validation_output" | sed -n 's/^ARTIFACT_TYPE=//p' | tail -n 1)"
contract_path="$(printf '%s\n' "$validation_output" | sed -n 's/^CONTRACT_PATH=//p' | tail -n 1)"
prompt_set="$(printf '%s\n' "$validation_output" | sed -n 's/^PROMPT_SET=//p' | tail -n 1)"
regime_set="$(printf '%s\n' "$validation_output" | sed -n 's/^REGIME_SET=//p' | tail -n 1)"
profile_file="$dev_dir/EXPERIMENT-PROFILE.md"
metadata_value() {
	local label="$1"
	local file="$2"
	sed -n "s/^- $label: //p" "$file" | head -n 1
}
if [[ -z "$validation" ]]; then
	validation="$(printf '%s\n' "$validation_output" | sed -n 's/^RESULT: //p' | sed 's/ .*//' | tail -n 1)"
fi
if [[ -z "$validation" ]]; then
	validation="block"
fi
if [[ -f "$profile_file" ]]; then
	if [[ -z "$profile_id" ]]; then
		profile_id="$(metadata_value "Profile ID" "$profile_file")"
	fi
	if [[ -z "$lifecycle_owner" ]]; then
		lifecycle_owner="$(metadata_value "Lifecycle owner" "$profile_file")"
	fi
	if [[ -z "$artifact_type" ]]; then
		artifact_type="$(metadata_value "Artifact type" "$profile_file")"
	fi
	if [[ -z "$contract_path" ]]; then
		contract_path="$(metadata_value "Contract path" "$profile_file")"
	fi
	if [[ -z "$prompt_set" ]]; then
		prompt_set="$(metadata_value "Prompt set" "$profile_file")"
	fi
	if [[ -z "$regime_set" ]]; then
		regime_set="$(metadata_value "Regime set" "$profile_file")"
	fi
fi
if [[ -z "$profile_validation" ]]; then
	if [[ -n "$profile_id" && -n "$lifecycle_owner" && -n "$artifact_type" && -n "$contract_path" && -n "$prompt_set" && -n "$regime_set" ]]; then
		profile_validation="pass"
	else
		profile_validation="block"
	fi
fi

timestamp="$(date -u +%Y%m%dT%H%M%SZ)"
report="$run_dir/$timestamp.md"
if [[ -e "$report" ]]; then
	report="$run_dir/$timestamp-experiment-harness.md"
fi

{
	printf '# Experiment Harness Run %s\n\n' "$timestamp"
	printf '%s\n' "- Artifact: ${artifact_abs#$repo_root/}"
	printf '%s\n' "- Profile ID: ${profile_id:-unknown}"
	printf '%s\n' "- Lifecycle owner: ${lifecycle_owner:-unknown}"
	printf '%s\n' "- Artifact type: ${artifact_type:-unknown}"
	printf '%s\n' "- Contract path: ${contract_path:-unknown}"
	printf '%s\n' "- Fixture inputs: $fixture_count"
	printf '%s\n' "- Example prompts: $prompt_count"
	printf '%s\n' "- Example outputs: $output_count"
	printf '%s\n\n' "- Validation: $validation"
	printf '## Profile Fields\n\n'
	printf '```text\n'
	printf 'PROFILE_ID=%s\n' "${profile_id:-unknown}"
	printf 'LIFECYCLE_OWNER=%s\n' "${lifecycle_owner:-unknown}"
	printf 'ARTIFACT_TYPE=%s\n' "${artifact_type:-unknown}"
	printf 'CONTRACT_PATH=%s\n' "${contract_path:-unknown}"
	printf 'PROMPT_SET=%s\n' "${prompt_set:-unknown}"
	printf 'REGIME_SET=%s\n' "${regime_set:-unknown}"
	printf 'PROFILE_VALIDATION=%s\n' "$profile_validation"
	printf '```\n\n'
	printf '## Validation Output\n\n'
	printf '```text\n%s\n```\n' "$validation_output"
} > "$report"

printf 'REPORT=%s\n' "${report#$repo_root/}"
printf 'VALIDATION=%s\n' "$validation"
printf 'PROFILE_VALIDATION=%s\n' "$profile_validation"

if [[ "${EXPERIMENT_OBSERVE:-1}" != "0" ]]; then
	observer_script="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/observe-harness.sh"
	"$observer_script" "$artifact_abs" "$report" || true
fi
