#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SELECTOR="$SCRIPT_DIR/select-prompt.sh"
FIND_CODEX="$SCRIPT_DIR/find-codex.sh"

usage() {
	cat <<'USAGE'
Usage:
  run-with-codex.sh <artifact-path> <task-id>
  run-with-codex.sh <artifact-path> <template> <low|medium|complex>
  run-with-codex.sh <artifact-path> next
  run-with-codex.sh <artifact-path> --all

Set RERUN=1 to overwrite an existing example output.
Set CODEX_BIN=/path/to/codex when codex is not on PATH.
USAGE
}

if [[ "$#" -lt 2 ]]; then
	usage >&2
	exit 2
fi

artifact="$1"
shift

if [[ ! -d "$artifact" ]]; then
	printf 'ERROR: artifact path not found: %s\n' "$artifact" >&2
	exit 1
fi

artifact_abs="$(cd "$artifact" && pwd)"
dev_dir="$artifact_abs/development"
prompt_dir="$dev_dir/example-prompts"
run_dir="$dev_dir/example-runs"
repo_root="${EXPERIMENT_REPO_ROOT:-$(git -C "$PWD" rev-parse --show-toplevel 2>/dev/null || pwd)}"

mkdir -p "$dev_dir/example-outputs" "$run_dir"

codex_bin="$("$FIND_CODEX" || true)"
if [[ -z "$codex_bin" ]]; then
	printf 'ERROR: codex CLI not found on PATH\n' >&2
	printf 'Set CODEX_BIN to the codex executable path, for example:\n' >&2
	printf '  CODEX_BIN=/path/to/codex %s %s next\n' "$0" "$artifact" >&2
	exit 1
fi

validate_output() {
	local output_abs="$1"
	if [[ ! -s "$output_abs" ]]; then
		printf 'ERROR: output file missing or empty: %s\n' "$output_abs" >&2
		return 1
	fi
	if rg -q -- '^Saved the .*output to |^Saved .* to \[' "$output_abs"; then
		printf 'ERROR: output is a save-summary, not the artifact result body\n' >&2
		return 1
	fi
	if ! rg -q -- '^## .+Result|^# .+Result|^## Gate Result|^## Spell Result|^## Sigil .*Result' "$output_abs"; then
		printf 'ERROR: output missing recognizable result heading\n' >&2
		return 1
	fi
}

run_one() {
	local task_id="$1"
	local selector_output prompt_rel output_rel prompt_abs output_abs run_id run_log last_message_abs

	selector_output="$("$SELECTOR" "$artifact_abs" "$task_id")"
	if [[ "$selector_output" == *'TASK_ID=none'* ]]; then
		printf 'No unrun prompts remain.\n'
		return 0
	fi

	task_id="$(printf '%s\n' "$selector_output" | sed -n 's/^TASK_ID=//p')"
	prompt_rel="$(printf '%s\n' "$selector_output" | sed -n 's/^PROMPT=//p')"
	output_rel="$(printf '%s\n' "$selector_output" | sed -n 's/^OUTPUT=//p')"
	prompt_abs="$repo_root/$prompt_rel"
	output_abs="$repo_root/$output_rel"
	run_id="$(date -u +%Y%m%dT%H%M%SZ)-$task_id"
	run_log="$run_dir/$run_id.log"
	last_message_abs="$run_dir/$run_id.last-message.md"

	if [[ -f "$output_abs" && "${RERUN:-0}" != "1" ]]; then
		printf 'SKIP: %s already has output %s\n' "$task_id" "$output_rel"
		printf 'Set RERUN=1 to overwrite.\n'
		return 0
	fi
	if [[ -f "$output_abs" && "${RERUN:-0}" == "1" ]]; then
		mv "$output_abs" "$run_dir/$run_id.previous-output.md"
	fi

	printf 'RUN: %s\n' "$task_id"
	printf 'PROMPT: %s\n' "$prompt_rel"
	printf 'OUTPUT: %s\n' "$output_rel"

	if ! "$codex_bin" exec \
		-C "$repo_root" \
		--sandbox workspace-write \
		--output-last-message "$last_message_abs" \
		"$(cat "$prompt_abs")" \
		> "$run_log" 2>&1; then
		printf 'FAIL: %s\n' "$task_id" >&2
		printf 'LOG: %s\n' "${run_log#$repo_root/}" >&2
		return 1
	fi

	if validate_output "$output_abs"; then
		printf 'CAPTURE: artifact-written\n'
	elif validate_output "$last_message_abs"; then
		cp "$last_message_abs" "$output_abs"
		printf 'CAPTURE: last-message\n'
	else
		printf 'ERROR: neither artifact output nor last message contained a valid artifact result body\n' >&2
		printf 'OUTPUT: %s\n' "$output_rel" >&2
		printf 'LAST_MESSAGE: %s\n' "${last_message_abs#$repo_root/}" >&2
		return 1
	fi

	printf 'DONE: %s\n' "$task_id"
	printf 'LOG: %s\n' "${run_log#$repo_root/}"
}

if [[ "$1" == "--help" || "$1" == "-h" ]]; then
	usage
	exit 0
fi

if [[ "$1" == "--all" ]]; then
	while IFS= read -r prompt; do
		run_one "$(basename "$prompt" .md)"
	done < <(find "$prompt_dir" -maxdepth 1 -type f -name '*.md' | sort)
	exit 0
fi

if [[ "$#" -eq 2 ]]; then
	run_one "$1-$2"
	exit 0
fi

if [[ "$#" -eq 1 ]]; then
	if [[ "$1" == "next" ]]; then
		selector_output="$("$SELECTOR" "$artifact_abs" next)"
		task_id="$(printf '%s\n' "$selector_output" | sed -n 's/^TASK_ID=//p')"
		if [[ "$task_id" == "none" ]]; then
			printf 'No unrun prompts remain.\n'
			exit 0
		fi
		run_one "$task_id"
	else
		run_one "$1"
	fi
	exit 0
fi

usage >&2
exit 2
