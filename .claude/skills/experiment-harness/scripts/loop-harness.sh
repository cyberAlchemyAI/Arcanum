#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FIND_CODEX="$SCRIPT_DIR/find-codex.sh"
VALIDATE_REGIME="$SCRIPT_DIR/validate-regime.sh"
VALIDATE_ATTEMPT="$SCRIPT_DIR/validate-loop-attempt.sh"
REFLECT_ATTEMPT="$SCRIPT_DIR/reflect-loop-attempt.sh"
APPLY_IMPROVEMENT="$SCRIPT_DIR/apply-loop-improvement.sh"
ROLLBACK_IMPROVEMENT="$SCRIPT_DIR/rollback-loop-improvement.sh"

usage() {
	cat <<'USAGE'
Usage:
  loop-harness.sh <artifact-path> <regime-id>

Environment:
  MAX_ATTEMPTS=5
  PASS_STREAK=2
  AUTO_IMPROVE=1
  EXPERIMENT_LOOP_MOCK_DIR=<dir>  # optional test fixture outputs
USAGE
}

if [[ "$#" -ne 2 ]]; then
	usage >&2
	exit 2
fi

if ! command -v jq >/dev/null 2>&1; then
	printf 'ERROR: jq not found\n' >&2
	exit 1
fi

artifact="$1"
regime_id="$2"
max_attempts="${MAX_ATTEMPTS:-5}"
required_streak="${PASS_STREAK:-2}"
auto_improve="${AUTO_IMPROVE:-1}"

case "$max_attempts" in
	''|*[!0-9]*) printf 'ERROR: MAX_ATTEMPTS must be numeric\n' >&2; exit 2 ;;
esac
case "$required_streak" in
	''|*[!0-9]*) printf 'ERROR: PASS_STREAK must be numeric\n' >&2; exit 2 ;;
esac

if [[ ! -d "$artifact" ]]; then
	printf 'ERROR: artifact path not found: %s\n' "$artifact" >&2
	exit 1
fi

artifact_abs="$(cd "$artifact" && pwd)"
repo_root="${EXPERIMENT_REPO_ROOT:-$(git -C "$PWD" rev-parse --show-toplevel 2>/dev/null || pwd)}"
dev_dir="$artifact_abs/development"
regime="$dev_dir/regimes/$regime_id.md"
loop_id="$(date -u +%Y%m%dT%H%M%SZ)"
loop_dir="$dev_dir/experiment-loops/$regime_id/$loop_id"
state="$loop_dir/loop-state.json"
report="$loop_dir/loop-report.md"

"$VALIDATE_REGIME" "$artifact_abs" "$regime_id" >/dev/null

prompt_rel="$(sed -n 's/^- Prompt: `\(.*\)`/\1/p' "$regime" | head -n 1)"
prompt_abs="$dev_dir/$prompt_rel"

mkdir -p "$loop_dir"

jq -n \
	--arg regime "$regime_id" \
	--arg loop_id "$loop_id" \
	--arg status "running" \
	--argjson max_attempts "$max_attempts" \
	--argjson required_streak "$required_streak" \
	'{
		regime: $regime,
		loop_id: $loop_id,
		status: $status,
		max_attempts: $max_attempts,
		required_streak: $required_streak,
		attempts: [],
		pass_streak: 0,
		best_status: "none",
		lessons: []
	}' > "$state"

status_rank() {
	case "$1" in
		pass) printf '4\n' ;;
		partial) printf '3\n' ;;
		fail) printf '2\n' ;;
		block) printf '1\n' ;;
		*) printf '0\n' ;;
	esac
}

write_attempt_report() {
	local attempt_dir="$1"
	local attempt="$2"
	local status="$3"
	{
		printf '# Attempt %03d Report\n\n' "$attempt"
		printf -- '- Regime: `%s`\n' "$regime_id"
		printf -- '- Status: `%s`\n' "$status"
		printf -- '- Prompt: `prompt.md`\n'
		printf -- '- Output: `output.md`\n'
		printf -- '- Validation: `validation.json`\n'
		if [[ -f "$attempt_dir/robot-talks.md" ]]; then
			printf -- '- Robot talks: `robot-talks.md`\n'
		fi
		if [[ -f "$attempt_dir/improvement-argument.md" ]]; then
			printf -- '- Improvement argument: `improvement-argument.md`\n'
		fi
	} > "$attempt_dir/attempt-report.md"
}

write_observer_event() {
	local attempt_dir="$1"
	local attempt="$2"
	local status="$3"
	local validation="$attempt_dir/validation.json"
	jq -n \
		--arg timestamp "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
		--arg regime "$regime_id" \
		--arg attempt "$attempt" \
		--arg status "$status" \
		--slurpfile validation "$validation" \
		'{
			timestamp: $timestamp,
			sigil: "experiment-harness",
			mode: "loop-attempt",
			regime: $regime,
			attempt: ($attempt | tonumber),
			execution: { status: $status },
			observer: {
				quality_bar_status: $validation[0].quality_bar_status,
				anti_pattern_hits: $validation[0].anti_pattern_hits,
				workflow_gaps: $validation[0].workflow_gaps,
				reflection_trigger: (if $status == "pass" then "none" else "severe-gap" end)
			}
		}' > "$attempt_dir/observer-event.json"
}

run_codex_or_mock() {
	local attempt="$1"
	local attempt_dir="$2"
	local output="$attempt_dir/output.md"
	local raw_log="$attempt_dir/raw.log"

	if [[ -n "${EXPERIMENT_LOOP_MOCK_DIR:-}" ]]; then
		local mock=""
		for candidate in \
			"$EXPERIMENT_LOOP_MOCK_DIR/$regime_id-attempt-$(printf '%03d' "$attempt").md" \
			"$EXPERIMENT_LOOP_MOCK_DIR/$regime_id-attempt-$attempt.md" \
			"$EXPERIMENT_LOOP_MOCK_DIR/$regime_id.md"; do
			if [[ -f "$candidate" ]]; then
				mock="$candidate"
				break
			fi
		done
		if [[ -z "$mock" ]]; then
			printf 'ERROR: mock output not found for %s attempt %s\n' "$regime_id" "$attempt" >&2
			return 1
		fi
		cp "$mock" "$output"
		printf 'MOCK_OUTPUT=%s\n' "$mock" > "$raw_log"
		return 0
	fi

	codex_bin="$("$FIND_CODEX" || true)"
	if [[ -z "$codex_bin" ]]; then
		printf 'ERROR: codex CLI not found\n' >&2
		return 1
	fi

	"$codex_bin" exec \
		-C "$repo_root" \
		--sandbox workspace-write \
		--output-last-message "$output" \
		"$(cat "$attempt_dir/prompt.md")" \
		> "$raw_log" 2>&1
}

pass_streak=0
best_status="none"
previous_status="none"
previous_patch_attempt=""
final_status="fail"

for ((attempt = 1; attempt <= max_attempts; attempt++)); do
	attempt_name="$(printf 'attempt-%03d' "$attempt")"
	attempt_dir="$loop_dir/$attempt_name"
	mkdir -p "$attempt_dir"
	cp "$prompt_abs" "$attempt_dir/prompt.md"

	if run_codex_or_mock "$attempt" "$attempt_dir"; then
		:
	else
		printf 'Codex execution failed\n' > "$attempt_dir/output.md"
	fi

	if "$VALIDATE_ATTEMPT" "$artifact_abs" "$regime_id" "$attempt_dir" >/dev/null 2>&1; then
		:
	else
		:
	fi

	attempt_status="$(jq -r '.status' "$attempt_dir/validation.json")"

	if [[ -n "$previous_patch_attempt" ]]; then
		if [[ "$(status_rank "$attempt_status")" -lt "$(status_rank "$previous_status")" ]]; then
			"$ROLLBACK_IMPROVEMENT" "$previous_patch_attempt" > "$attempt_dir/rollback-result.txt" || true
			jq --arg lesson "Attempt $attempt regressed after improvement; rollback requested." \
				'.lessons += [$lesson]' "$state" > "$state.tmp" && mv "$state.tmp" "$state"
		fi
		previous_patch_attempt=""
	fi

	write_observer_event "$attempt_dir" "$attempt" "$attempt_status"
	write_attempt_report "$attempt_dir" "$attempt" "$attempt_status"

	if [[ "$attempt_status" == "pass" ]]; then
		pass_streak=$((pass_streak + 1))
	else
		pass_streak=0
	fi

	if [[ "$(status_rank "$attempt_status")" -gt "$(status_rank "$best_status")" ]]; then
		best_status="$attempt_status"
	fi

	jq \
		--arg attempt "$attempt_name" \
		--arg status "$attempt_status" \
		--arg prompt "${attempt_dir#$repo_root/}/prompt.md" \
		--arg output "${attempt_dir#$repo_root/}/output.md" \
		--arg validation "${attempt_dir#$repo_root/}/validation.json" \
		--arg report "${attempt_dir#$repo_root/}/attempt-report.md" \
		--argjson pass_streak "$pass_streak" \
		--arg best_status "$best_status" \
		'.attempts += [{
			attempt: $attempt,
			status: $status,
			prompt: $prompt,
			output: $output,
			validation: $validation,
			report: $report
		}]
		| .pass_streak = $pass_streak
		| .best_status = $best_status' "$state" > "$state.tmp" && mv "$state.tmp" "$state"

	if [[ "$pass_streak" -ge "$required_streak" ]]; then
		final_status="pass"
		break
	fi

	if [[ "$attempt" -lt "$max_attempts" && "$auto_improve" == "1" && "$attempt_status" != "pass" ]]; then
		"$REFLECT_ATTEMPT" "$artifact_abs" "$regime_id" "$attempt_dir" >/dev/null
		if "$APPLY_IMPROVEMENT" "$attempt_dir" > "$attempt_dir/patch-result.txt" 2>&1; then
			if [[ -f "$attempt_dir/patch-applied.txt" && "$(cat "$attempt_dir/patch-applied.txt")" == "true" ]]; then
				previous_patch_attempt="$attempt_dir"
				previous_status="$attempt_status"
			fi
		fi
	fi
done

if [[ "$final_status" != "pass" ]]; then
	if [[ "$best_status" == "pass" ]]; then
		final_status="partial"
	elif [[ "$best_status" == "none" ]]; then
		final_status="block"
	else
		final_status="$best_status"
	fi
fi

jq --arg status "$final_status" '.status = $status' "$state" > "$state.tmp" && mv "$state.tmp" "$state"

{
	printf '# Experiment Loop Report\n\n'
	printf -- '- Regime: `%s`\n' "$regime_id"
	printf -- '- Loop ID: `%s`\n' "$loop_id"
	printf -- '- Status: `%s`\n' "$final_status"
	printf -- '- Required pass streak: `%s`\n' "$required_streak"
	printf -- '- Max attempts: `%s`\n' "$max_attempts"
	printf -- '- Final pass streak: `%s`\n' "$(jq -r '.pass_streak' "$state")"
	printf '\n## Attempts\n\n'
	jq -r '.attempts[] | "- `" + .attempt + "`: `" + .status + "` | output: `" + .output + "` | validation: `" + .validation + "`"' "$state"
	printf '\n## Lessons Learned\n\n'
	if [[ "$(jq '.lessons | length' "$state")" -eq 0 ]]; then
		printf -- '- No rollback or regression lessons recorded in this loop.\n'
	else
		jq -r '.lessons[] | "- " + .' "$state"
	fi
	printf '\n## Machine Summary\n\n'
	printf 'VALIDATION=%s\n' "$final_status"
	printf 'QUALITY_BAR_STATUS=%s\n' "$([[ "$final_status" == "pass" ]] && printf pass || printf partial)"
	printf 'ANTI_PATTERN_HITS_JSON=[]\n'
	printf 'WORKFLOW_GAPS_JSON=[]\n'
} > "$report"

printf 'LOOP_STATUS=%s\n' "$final_status"
printf 'LOOP_DIR=%s\n' "${loop_dir#$repo_root/}"
printf 'LOOP_REPORT=%s\n' "${report#$repo_root/}"

if [[ "$final_status" == "pass" ]]; then
	exit 0
fi
exit 1
