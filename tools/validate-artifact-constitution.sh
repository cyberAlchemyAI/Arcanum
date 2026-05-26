#!/usr/bin/env bash
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$repo_root"

constitution="framework/ARTIFACT-CONSTITUTION.md"

failures=()
warnings=()

add_failure() {
	failures+=("$1")
}

add_warning() {
	warnings+=("$1")
}

is_local_runtime_path() {
	local path="$1"
	case "$path" in
		.arcanum/codex-home/*|.arcanum/codex-home-smoke/*|.arcanum/runtime/*|tmp/*) return 0 ;;
		*.sqlite|*.sqlite-shm|*.sqlite-wal|*/auth.json|auth.json|*/installation_id|installation_id) return 0 ;;
		*) return 1 ;;
	esac
}

is_generated_path() {
	local path="$1"
	case "$path" in
		*/development/runs/*|*/development/example-runs/*|*/development/example-outputs/*) return 0 ;;
		.arcanum/observability/runs/*|.arcanum/observability/reflections/*) return 0 ;;
		.arcanum/observability/by-sigil/*.jsonl|.arcanum/observability/hooks/*.jsonl) return 0 ;;
		.arcanum/observability/by-capability/*.jsonl|.arcanum/observability/by-capability/*/*.jsonl) return 0 ;;
		.arcanum/observability/signals/*.jsonl|.arcanum/observability/reflection-state.json) return 0 ;;
		benchmark/artifacts/*|benchmark/logs/*|benchmark/code_analysis.log|benchmark/*.swebench-lite-official-smoke.json) return 0 ;;
		*) return 1 ;;
	esac
}

is_keep_file() {
	local path="$1"
	case "$path" in
		*/.gitkeep) return 0 ;;
		*) return 1 ;;
	esac
}

is_ignored() {
	local path="$1"
	git check-ignore -q -- "$path"
}

validate_path_visibility() {
	local path="$1"
	[[ -e "$path" || -L "$path" ]] || return 0

	if is_keep_file "$path"; then
		return 0
	fi

	if is_local_runtime_path "$path"; then
		if ! is_ignored "$path"; then
			add_failure "local runtime artifact is not ignored: $path"
		fi
		return 0
	fi

	if is_generated_path "$path"; then
		if ! is_ignored "$path"; then
			add_failure "generated artifact is not ignored or explicitly promoted: $path"
		fi
	fi
}

if [[ ! -f "$constitution" ]]; then
	add_failure "missing artifact constitution: $constitution"
fi

while IFS= read -r path; do
	[[ -n "$path" ]] || continue
	validate_path_visibility "$path"
done < <(git ls-files --others --exclude-standard)

while IFS= read -r path; do
	[[ -n "$path" ]] || continue
	if is_keep_file "$path"; then
		continue
	fi
	if is_local_runtime_path "$path"; then
		add_failure "tracked local runtime artifact must be removed from the index: $path"
	elif is_generated_path "$path"; then
		add_warning "tracked generated artifact should remain only if promoted as durable evidence: $path"
	fi
done < <(git ls-files)

printf 'Artifact Constitution validation\n'
printf 'constitution: %s\n' "$constitution"

if ((${#warnings[@]} > 0)); then
	printf '\nwarnings:\n'
	warning_limit=25
	for warning in "${warnings[@]:0:$warning_limit}"; do
		printf -- '- %s\n' "$warning"
	done
	if ((${#warnings[@]} > warning_limit)); then
		printf -- '- ... %s more tracked generated artifacts omitted from this report\n' "$((${#warnings[@]} - warning_limit))"
	fi
fi

if ((${#failures[@]} > 0)); then
	printf '\nfailures:\n'
	for failure in "${failures[@]}"; do
		printf -- '- %s\n' "$failure"
	done
	exit 1
fi

printf '\nresult: pass\n'
