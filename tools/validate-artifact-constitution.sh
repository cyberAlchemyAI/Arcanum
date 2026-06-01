#!/usr/bin/env bash
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$repo_root"

constitution="framework/ARTIFACT-CONSTITUTION.md"
schema_constitution="framework/SCHEMA-CONSTITUTION.md"
metadata_constitution="framework/ARTIFACT-METADATA-CONSTITUTION.md"
metadata_validator="tools/validate-artifact-metadata.py"

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

is_visual_artifact_path() {
	local path="$1"
	case "$path" in
		*.html|*.svg|*.js|*.jsx|*.ts|*.tsx|*.json) ;;
		*) return 1 ;;
	esac
	case "$path" in
		*chart*|*Chart*|*dashboard*|*Dashboard*|*presentation*|*Presentation*|*visual*|*Visual*|*plot*|*Plot*|*.svg) return 0 ;;
		*) return 1 ;;
	esac
}

is_schema_artifact_path() {
	local path="$1"
	case "$path" in
		*.schema.yml) return 1 ;;
		*.schema.yaml|*.schema.json) return 0 ;;
		*) return 1 ;;
	esac
}

is_schema_markdown_path() {
	local path="$1"
	case "$path" in
		*/templates/*schema*.md|*/templates/schema.md) return 0 ;;
		*) return 1 ;;
	esac
}

schema_markdown_declares_noncanonical() {
	local path="$1"
	grep -qiE 'Schema Artifact Role:[[:space:]]*(non-canonical|prose-only|explanatory-template|schema-template|package-conventions)' "$path"
}

schema_markdown_has_yml_counterpart() {
	local path="$1"
	local dir
	local base
	local stem

	dir="$(dirname "$path")"
	base="$(basename "$path")"

	case "$base" in
		*-schema.md)
			stem="${base%-schema.md}"
			[[ -f "$dir/$stem.schema.yml" ]]
			return
			;;
		schema.md)
			[[ -f "$dir/schema.schema.yml" ]]
			return
			;;
		*)
			return 1
			;;
	esac
}

line_looks_like_chart_text() {
	local line="$1"
	case "$line" in
		*label*|*Label*|*legend*|*Legend*|*title*|*Title*|*annotation*|*Annotation*|*tooltip*|*Tooltip*|*axis*|*Axis*|*tick*|*Tick*|*text*|*Text*|*name*|*Name*) return 0 ;;
		*) return 1 ;;
	esac
}

is_ignored() {
	local path="$1"
	git check-ignore -q -- "$path"
}

validate_chart_line_breaks() {
	local path="$1"
	local line
	local lineno
	local text

	[[ -f "$path" ]] || return 0
	is_visual_artifact_path "$path" || return 0
	is_generated_path "$path" && return 0
	is_local_runtime_path "$path" && return 0

	while IFS= read -r line; do
		lineno="${line%%:*}"
		text="${line#*:}"
		if line_looks_like_chart_text "$text"; then
			add_failure "chart/visual artifact uses literal \\n for text line break; use <br> or renderer rich text: $path:$lineno"
		fi
	done < <(grep -nF '\n' "$path" 2>/dev/null || true)
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

validate_schema_format() {
	local path="$1"

	[[ -f "$path" ]] || return 0
	is_schema_artifact_path "$path" || return 0
	is_generated_path "$path" && return 0
	is_local_runtime_path "$path" && return 0

	if git ls-files --error-unmatch -- "$path" >/dev/null 2>&1; then
		add_warning "legacy tracked schema artifact is not .schema.yml and needs migration planning: $path"
	else
		add_failure "new schema artifact must use .schema.yml format: $path"
	fi
}

validate_schema_markdown_boundary() {
	local path="$1"

	[[ -f "$path" ]] || return 0
	is_schema_markdown_path "$path" || return 0
	is_generated_path "$path" && return 0
	is_local_runtime_path "$path" && return 0

	if schema_markdown_declares_noncanonical "$path"; then
		return 0
	fi

	if schema_markdown_has_yml_counterpart "$path"; then
		return 0
	fi

	if git ls-files --error-unmatch -- "$path" >/dev/null 2>&1; then
		add_warning "legacy tracked schema markdown lacks .schema.yml counterpart or non-canonical marker: $path"
	else
		add_failure "new schema markdown must be non-canonical or paired with .schema.yml: $path"
	fi
}

run_self_test() {
	local tmp_dir
	local bad_chart
	local good_chart
	local non_visual
	local bad_schema
	local good_schema
	local bad_schema_md
	local good_schema_md
	local paired_schema_md

	tmp_dir="$(mktemp -d)"

	bad_chart="$tmp_dir/chart-bad.html"
	good_chart="$tmp_dir/chart-good.html"
	non_visual="$tmp_dir/plain-note.md"
	bad_schema="$tmp_dir/example.schema.json"
	good_schema="$tmp_dir/example.schema.yml"
	mkdir -p "$tmp_dir/templates"
	bad_schema_md="$tmp_dir/templates/example-schema.md"
	good_schema_md="$tmp_dir/templates/prose-schema.md"
	paired_schema_md="$tmp_dir/templates/paired-schema.md"

	printf '<script>const option = { title: { text: "Bad\\nTitle" } };</script>\n' > "$bad_chart"
	printf '<script>const option = { title: { text: "Good<br>Title" } };</script>\n' > "$good_chart"
	printf 'This literal \\n is documentation, not chart text.\n' > "$non_visual"
	printf '{"type":"object"}\n' > "$bad_schema"
	printf 'type: object\n' > "$good_schema"
	printf '# Example Schema\n\nCanonical contract.\n' > "$bad_schema_md"
	printf '# Prose Schema Notes\n\nSchema Artifact Role: non-canonical\n' > "$good_schema_md"
	printf '# Paired Schema\n\nCanonical schema companion exists.\n' > "$paired_schema_md"
	printf 'type: object\n' > "$tmp_dir/templates/paired.schema.yml"

	failures=()
	validate_chart_line_breaks "$bad_chart"
	if ((${#failures[@]} != 1)); then
		printf 'self-test failed: bad chart fixture produced %s failures, expected 1\n' "${#failures[@]}" >&2
		exit 1
	fi

	failures=()
	validate_chart_line_breaks "$good_chart"
	if ((${#failures[@]} != 0)); then
		printf 'self-test failed: good chart fixture produced %s failures, expected 0\n' "${#failures[@]}" >&2
		exit 1
	fi

	failures=()
	validate_chart_line_breaks "$non_visual"
	if ((${#failures[@]} != 0)); then
		printf 'self-test failed: non-visual fixture produced %s failures, expected 0\n' "${#failures[@]}" >&2
		exit 1
	fi

	failures=()
	warnings=()
	validate_schema_format "$bad_schema"
	if ((${#failures[@]} != 1)); then
		printf 'self-test failed: bad schema fixture produced %s failures, expected 1\n' "${#failures[@]}" >&2
		exit 1
	fi

	failures=()
	warnings=()
	validate_schema_format "$good_schema"
	if ((${#failures[@]} != 0 || ${#warnings[@]} != 0)); then
		printf 'self-test failed: good schema fixture produced %s failures and %s warnings, expected 0/0\n' "${#failures[@]}" "${#warnings[@]}" >&2
		exit 1
	fi

	failures=()
	warnings=()
	validate_schema_markdown_boundary "$bad_schema_md"
	if ((${#failures[@]} != 1)); then
		printf 'self-test failed: bad schema markdown fixture produced %s failures, expected 1\n' "${#failures[@]}" >&2
		exit 1
	fi

	failures=()
	warnings=()
	validate_schema_markdown_boundary "$good_schema_md"
	if ((${#failures[@]} != 0 || ${#warnings[@]} != 0)); then
		printf 'self-test failed: non-canonical schema markdown fixture produced %s failures and %s warnings, expected 0/0\n' "${#failures[@]}" "${#warnings[@]}" >&2
		exit 1
	fi

	failures=()
	warnings=()
	validate_schema_markdown_boundary "$paired_schema_md"
	if ((${#failures[@]} != 0 || ${#warnings[@]} != 0)); then
		printf 'self-test failed: paired schema markdown fixture produced %s failures and %s warnings, expected 0/0\n' "${#failures[@]}" "${#warnings[@]}" >&2
		exit 1
	fi

	printf 'Artifact Constitution validator self-test\n'
	printf 'chart line-break fixtures: pass\n'
	printf 'schema format fixtures: pass\n'
	printf 'schema markdown boundary fixtures: pass\n'
	rm -rf "$tmp_dir"
}

if [[ "${1:-}" == "--self-test" ]]; then
	run_self_test
	exit 0
fi

if [[ ! -f "$constitution" ]]; then
	add_failure "missing artifact constitution: $constitution"
fi

if [[ ! -f "$schema_constitution" ]]; then
	add_failure "missing schema constitution: $schema_constitution"
fi

if [[ ! -f "$metadata_constitution" ]]; then
	add_failure "missing artifact metadata constitution: $metadata_constitution"
fi

if [[ ! -f "$metadata_validator" ]]; then
	add_failure "missing artifact metadata validator: $metadata_validator"
fi

while IFS= read -r path; do
	[[ -n "$path" ]] || continue
	validate_path_visibility "$path"
	validate_chart_line_breaks "$path"
	validate_schema_format "$path"
	validate_schema_markdown_boundary "$path"
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
	validate_chart_line_breaks "$path"
	validate_schema_format "$path"
	validate_schema_markdown_boundary "$path"
done < <(git ls-files)

printf 'Artifact Constitution validation\n'
printf 'constitution: %s\n' "$constitution"

if [[ -f "$metadata_validator" ]]; then
	metadata_output="$(python3 "$metadata_validator" --changed --advisory 2>&1 || true)"
	if [[ -n "$metadata_output" ]]; then
		while IFS= read -r line; do
			[[ -n "$line" ]] || continue
			case "$line" in
				"Artifact metadata validation"|"result: pass"|"warnings:"|"failures:") ;;
				-*) add_warning "artifact metadata advisory ${line#- }" ;;
				*) ;;
			esac
		done <<< "$metadata_output"
	fi
fi

if ((${#warnings[@]} > 0)); then
	printf '\nwarnings:\n'
	warning_limit=25
	for warning in "${warnings[@]:0:$warning_limit}"; do
		printf -- '- %s\n' "$warning"
	done
	if ((${#warnings[@]} > warning_limit)); then
		printf -- '- ... %s more warnings omitted from this report\n' "$((${#warnings[@]} - warning_limit))"
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
