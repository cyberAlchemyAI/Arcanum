#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() {
	cat <<'USAGE'
Usage:
  init-harness.sh <artifact-path> --type spell|sigil [--profile generic-spell|spellcraft|invoke-live|generic-sigil|sigil-development]
USAGE
}

if [[ "$#" -ne 3 && "$#" -ne 5 ]]; then
	usage >&2
	exit 2
fi

artifact="$1"
shift
artifact_type=""
profile_id=""

while [[ "$#" -gt 0 ]]; do
	case "$1" in
		--type)
			if [[ "$#" -lt 2 ]]; then
				usage >&2
				exit 2
			fi
			artifact_type="$2"
			shift 2
			;;
		--profile)
			if [[ "$#" -lt 2 ]]; then
				usage >&2
				exit 2
			fi
			profile_id="$2"
			shift 2
			;;
		*)
			usage >&2
			exit 2
			;;
	esac
done

if [[ -z "$artifact_type" ]]; then
	usage >&2
	exit 2
fi

case "$artifact_type" in
	spell|sigil) ;;
	*)
		printf 'ERROR: artifact type must be spell or sigil\n' >&2
		exit 2
		;;
esac

if [[ -z "$profile_id" ]]; then
	case "$artifact_type" in
		spell) profile_id="generic-spell" ;;
		sigil) profile_id="generic-sigil" ;;
	esac
fi

profile_dir="$SCRIPT_DIR/../templates/profiles"
profile_file="$profile_dir/$profile_id.profile.sh"
if [[ ! -f "$profile_file" ]]; then
	printf 'ERROR: unknown experiment profile: %s\n' "$profile_id" >&2
	exit 2
fi

# shellcheck source=/dev/null
source "$profile_file"

if [[ "${PROFILE_ARTIFACT_TYPE:-}" != "$artifact_type" ]]; then
	printf 'ERROR: profile %s requires --type %s\n' "$profile_id" "${PROFILE_ARTIFACT_TYPE:-unknown}" >&2
	exit 2
fi

if [[ ! -d "$artifact" ]]; then
	printf 'ERROR: artifact path not found: %s\n' "$artifact" >&2
	exit 1
fi

artifact_abs="$(cd "$artifact" && pwd)"
dev_dir="$artifact_abs/development"
repo_root="${EXPERIMENT_REPO_ROOT:-$(git -C "$PWD" rev-parse --show-toplevel 2>/dev/null || pwd)}"

contract_path=""
if [[ -f "$artifact_abs/SKILL.md" ]]; then
	contract_path="$artifact_abs/SKILL.md"
elif [[ -f "$artifact_abs/README.md" ]]; then
	contract_path="$artifact_abs/README.md"
else
	printf 'ERROR: profile-aware harness requires %s/SKILL.md or %s/README.md\n' "$artifact" "$artifact" >&2
	exit 1
fi

mkdir -p \
	"$dev_dir/fixtures" \
	"$dev_dir/regimes" \
	"$dev_dir/example-prompts" \
	"$dev_dir/example-outputs" \
	"$dev_dir/example-runs" \
	"$dev_dir/experiment-loops" \
	"$dev_dir/runs"

write_if_missing() {
	local path="$1"
	shift
	if [[ -e "$path" ]]; then
		printf 'KEEP: %s\n' "${path#$repo_root/}"
		return 0
	fi
	printf '%s\n' "$@" > "$path"
	printf 'CREATE: %s\n' "${path#$repo_root/}"
}

display_path() {
	local path="$1"
	if [[ "$path" == "$repo_root/"* ]]; then
		printf '%s\n' "${path#$repo_root/}"
	else
		printf '%s\n' "$path"
	fi
}

write_if_missing "$dev_dir/VALIDATION-EXPERIMENT.md" \
	"# Validation Experiment" \
	"" \
	"- Artifact: ${artifact_abs#$repo_root/}" \
	"- Artifact type: $artifact_type" \
	"- Runtime: Codex CLI" \
	"- Harness owner: experiment-harness" \
	"" \
	"## Goal" \
	"" \
	"Validate that this $artifact_type works against realistic low, medium, and complex tasks and produces user-facing outputs that satisfy its contract." \
	"" \
	"## Evidence Required" \
	"" \
	"- Fixture inputs and expected outputs." \
	"- Real example prompts." \
	"- Real Codex CLI example outputs when runtime execution is enabled." \
	"- Timestamped validation reports under \`development/runs/\`." \
	"" \
	"## Promotion Gate" \
	"" \
	"This artifact is not promotion-ready until validation passes, expected outputs are inspectable, and at least one real runtime output exists when a runtime adapter is available."

write_if_missing "$dev_dir/VALIDATION.md" \
	"# Validation" \
	"" \
	"- Latest report: pending" \
	"- Status: flag" \
	"- Reason: harness initialized, but fixtures and example outputs still need to be added." \
	"" \
	"## Checks" \
	"" \
	"- Harness layout exists." \
	"- Fixture pairs exist." \
	"- Example prompts cover low, medium, and complex cases when applicable." \
	"- Real outputs are not save summaries." \
	"- Latest run report is linked after validation."

write_if_missing "$dev_dir/TASK-MATRIX.md" \
	"# Task Matrix" \
	"" \
	"| ID | Complexity | Scenario | Expected Output | Status |" \
	"| --- | --- | --- | --- | --- |" \
	"| ${artifact_type}-low | low | Small focused request. | Contract-shaped result. | pending |" \
	"| ${artifact_type}-medium | medium | Multi-part realistic request. | Contract-shaped result with gates. | pending |" \
	"| ${artifact_type}-complex | complex | Cross-boundary or lifecycle request. | Contract-shaped result with risks and next steps. | pending |"

write_if_missing "$dev_dir/.gitignore" \
	"# Generated experiment evidence." \
	"example-outputs/*" \
	"example-runs/*" \
	"experiment-loops/*" \
	"runs/*" \
	"" \
	"# Keep evidence directories present." \
	"!example-outputs/.gitkeep" \
	"!example-runs/.gitkeep" \
	"!experiment-loops/.gitkeep" \
	"!runs/.gitkeep"

write_if_missing "$dev_dir/example-outputs/.gitkeep" ""
write_if_missing "$dev_dir/example-runs/.gitkeep" ""
write_if_missing "$dev_dir/experiment-loops/.gitkeep" ""
write_if_missing "$dev_dir/runs/.gitkeep" ""

write_if_missing "$dev_dir/EXPERIMENT-PROFILE.md" \
	"# Experiment Profile" \
	"" \
	"- Profile ID: $PROFILE_ID" \
	"- Artifact type: $artifact_type" \
	"- Lifecycle owner: $PROFILE_LIFECYCLE_OWNER" \
	"- Artifact path: $(display_path "$artifact_abs")" \
	"- Contract path: $(display_path "$contract_path")" \
	"- Scenario pack: $PROFILE_SCENARIO_PACK" \
	"- Required modes: $PROFILE_REQUIRED_MODES" \
	"- Prompt set: $PROFILE_PROMPT_SET" \
	"- Regime set: $PROFILE_REGIME_SET" \
	"- Validation focus: $PROFILE_VALIDATION_FOCUS" \
	"- Observability focus: $PROFILE_OBSERVABILITY_FOCUS" \
	"- Promotion gate: $PROFILE_PROMOTION_GATE" \
	"" \
	"## Ownership Boundary" \
	"" \
	"Experiment Harness owns experiment mechanics. The lifecycle owner owns artifact meaning and promotion judgment."

for i in "${!PROFILE_PROMPT_IDS[@]}"; do
	prompt_id="${PROFILE_PROMPT_IDS[$i]}"
	regime_id="${PROFILE_REGIME_IDS[$i]}"
	prompt_request="${PROFILE_PROMPT_REQUESTS[$i]}"
	regime_goal="${PROFILE_REGIME_GOALS[$i]}"

	write_if_missing "$dev_dir/fixtures/$prompt_id.md" \
		"# Fixture: $prompt_id" \
		"" \
		"## Request" \
		"" \
		"$prompt_request" \
		"" \
		"## Inputs" \
		"" \
		"- Target artifact: $(display_path "$artifact_abs")" \
		"- Contract path: $(display_path "$contract_path")" \
		"- Lifecycle owner: $PROFILE_LIFECYCLE_OWNER"

	write_if_missing "$dev_dir/fixtures/$prompt_id.expected.md" \
		"# Expected Output: $prompt_id" \
		"" \
		"## Result" \
		"" \
		"- Status: flag" \
		"- Profile ID: $PROFILE_ID" \
		"- Lifecycle owner: $PROFILE_LIFECYCLE_OWNER" \
		"- Reason: starter expected output must be replaced with artifact-specific contract evidence."

	write_if_missing "$dev_dir/example-prompts/$prompt_id.md" \
		"# Experiment Prompt: $prompt_id" \
		"" \
		"Run the target $artifact_type through the $PROFILE_ID experiment profile." \
		"" \
		"## Target Artifact" \
		"" \
		"$(display_path "$artifact_abs")" \
		"" \
		"## Contract" \
		"" \
		"$(display_path "$contract_path")" \
		"" \
		"## Lifecycle Owner" \
		"" \
		"$PROFILE_LIFECYCLE_OWNER" \
		"" \
		"## User Request" \
		"" \
		"$prompt_request Return the full user-facing result body. Do not summarize that you saved an output file." \
		"" \
		"## Required Capture" \
		"" \
		"Save only the final artifact result body to \`development/example-outputs/$prompt_id.output.md\`."

	write_if_missing "$dev_dir/regimes/$regime_id.md" \
		"# Regime: $regime_id" \
		"" \
		"## Goal" \
		"" \
		"$regime_goal" \
		"" \
		"## Prompt" \
		"" \
		"- Prompt: \`example-prompts/$prompt_id.md\`" \
		"" \
		"## Required Output Patterns" \
		"" \
		"- \`## .+Result|# .+Result\`" \
		"- \`Status:|Validation:|Phase status:\`" \
		"" \
		"## Quality Bar" \
		"" \
		"- Output must satisfy the target contract at \`$(display_path "$contract_path")\`." \
		"- Output must preserve lifecycle owner boundary: $PROFILE_LIFECYCLE_OWNER." \
		"- Output must be a real artifact body, not a save-summary." \
		"" \
		"## Anti-Patterns" \
		"" \
		"- Avoid accepting empty output or a summary that only says a file was saved." \
		"- Avoid replacing $PROFILE_LIFECYCLE_OWNER judgment with Experiment Harness mechanics." \
		"" \
		"## Observability" \
		"" \
		"- Attempt telemetry should record profile id $PROFILE_ID, lifecycle owner $PROFILE_LIFECYCLE_OWNER, quality, anti-patterns, workflow gaps, and reflection trigger." \
		"" \
		"## Lessons To Capture" \
		"" \
		"- Missing output sections." \
		"- Prompt ambiguity." \
		"- Observer gaps." \
		"- Profile drift from the target contract."
done

write_if_missing "$dev_dir/select-example-prompt.sh" \
	"#!/usr/bin/env bash" \
	"set -euo pipefail" \
	"\"$SCRIPT_DIR/select-prompt.sh\" \"$artifact_abs\" \"\$@\""

write_if_missing "$dev_dir/run-example-with-codex.sh" \
	"#!/usr/bin/env bash" \
	"set -euo pipefail" \
	"\"$SCRIPT_DIR/run-with-codex.sh\" \"$artifact_abs\" \"\$@\""

write_if_missing "$dev_dir/run-experiment-loop.sh" \
	"#!/usr/bin/env bash" \
	"set -euo pipefail" \
	"\"$SCRIPT_DIR/loop-harness.sh\" \"$artifact_abs\" \"\$@\""

write_if_missing "$dev_dir/run-validation-fixtures.sh" \
	"#!/usr/bin/env bash" \
	"set -euo pipefail" \
	"\"$SCRIPT_DIR/validate-harness.sh\" \"$artifact_abs\""

write_if_missing "$dev_dir/write-experiment-report.sh" \
	"#!/usr/bin/env bash" \
	"set -euo pipefail" \
	"\"$SCRIPT_DIR/report-harness.sh\" \"$artifact_abs\""

write_if_missing "$dev_dir/observe-experiment-report.sh" \
	"#!/usr/bin/env bash" \
	"set -euo pipefail" \
	"\"$SCRIPT_DIR/observe-harness.sh\" \"$artifact_abs\" \"\$@\""

chmod +x \
	"$dev_dir/select-example-prompt.sh" \
	"$dev_dir/run-example-with-codex.sh" \
	"$dev_dir/run-experiment-loop.sh" \
	"$dev_dir/run-validation-fixtures.sh" \
	"$dev_dir/write-experiment-report.sh" \
	"$dev_dir/observe-experiment-report.sh"

printf 'HARNESS=%s\n' "${dev_dir#$repo_root/}"
printf 'TYPE=%s\n' "$artifact_type"
printf 'PROFILE_ID=%s\n' "$PROFILE_ID"
printf 'LIFECYCLE_OWNER=%s\n' "$PROFILE_LIFECYCLE_OWNER"
