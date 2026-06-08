#!/usr/bin/env bash
set -euo pipefail

usage() {
	cat <<'USAGE'
Usage:
  select-prompt.sh <artifact-path> <task-id>
  select-prompt.sh <artifact-path> <template> <low|medium|complex>
  select-prompt.sh <artifact-path> next
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
output_dir="$dev_dir/example-outputs"

resolve_task_id() {
	if [[ "$#" -eq 1 ]]; then
		if [[ "$1" == "next" ]]; then
			local prompt task_id
			while IFS= read -r prompt; do
				task_id="$(basename "$prompt" .md)"
				if [[ ! -f "$output_dir/$task_id.output.md" ]]; then
					printf '%s\n' "$task_id"
					return 0
				fi
			done < <(find "$prompt_dir" -maxdepth 1 -type f -name '*.md' 2>/dev/null | sort)
			printf 'none\n'
			return 0
		fi
		printf '%s\n' "$1"
		return 0
	fi

	if [[ "$#" -eq 2 ]]; then
		printf '%s-%s\n' "$1" "$2"
		return 0
	fi

	usage >&2
	exit 2
}

task_id="$(resolve_task_id "$@")"

if [[ "$task_id" == "none" ]]; then
	printf 'TASK_ID=none\n'
	printf 'PROMPT=none\n'
	printf 'OUTPUT=none\n'
	exit 0
fi

prompt="$prompt_dir/$task_id.md"
output="$output_dir/$task_id.output.md"

if [[ ! -f "$prompt" ]]; then
	printf 'ERROR: prompt not found for task %s\n' "$task_id" >&2
	printf 'Expected: %s\n' "$prompt" >&2
	exit 1
fi

repo_root="${EXPERIMENT_REPO_ROOT:-$(git -C "$PWD" rev-parse --show-toplevel 2>/dev/null || pwd)}"

printf 'TASK_ID=%s\n' "$task_id"
printf 'PROMPT=%s\n' "${prompt#$repo_root/}"
printf 'OUTPUT=%s\n' "${output#$repo_root/}"
