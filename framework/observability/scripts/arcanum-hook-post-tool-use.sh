#!/usr/bin/env bash
set -euo pipefail

if ! command -v jq >/dev/null 2>&1; then
  printf '{}\n'
  exit 0
fi

input="$(cat)"
repo_root="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
observability_dir="$repo_root/.arcanum/observability"
artifact_validator="$repo_root/tools/validate-artifact-constitution.sh"
turn_id="$(printf '%s\n' "$input" | jq -r '.turn_id // "unknown-turn"')"
safe_turn="${turn_id//[^A-Za-z0-9._-]/-}"
run_id="arcanum-hook-$safe_turn"
run_dir="$observability_dir/runs/arcanum-hooks/$run_id"
envelope="$run_dir/pending-envelope.json"

if [[ ! -f "$envelope" ]]; then
  printf '{}\n'
  exit 0
fi

mkdir -p "$run_dir"
printf '%s\n' "$input" | jq -c '{
  timestamp: (now | todateiso8601),
  turn_id: (.turn_id // null),
  tool_name: (.tool_name // null),
  tool_use_id: (.tool_use_id // null),
  tool_input: (.tool_input // null),
  tool_response: (.tool_response // null)
}' >> "$run_dir/tool-events.jsonl"

artifact_validation="skipped"
if [[ -x "$artifact_validator" ]]; then
  set +e
  validation_output="$("$artifact_validator" 2>&1)"
  validation_status=$?
  set -e
  printf '%s\n' "$validation_output" > "$run_dir/artifact-constitution-validation.txt"
  if [[ "$validation_status" -eq 0 ]]; then
    artifact_validation="passed"
  else
    artifact_validation="failed"
  fi
fi

tmp="$(mktemp)"
jq --arg artifact_validation "$artifact_validation" \
  '.execution.validation += [
    "codex PostToolUse hook recorded tool evidence",
    ("artifact constitution validation " + $artifact_validation)
  ]' "$envelope" > "$tmp" && mv "$tmp" "$envelope"

printf '{}\n'
