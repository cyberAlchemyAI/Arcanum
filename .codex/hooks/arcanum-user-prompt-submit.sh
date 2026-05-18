#!/usr/bin/env bash
set -euo pipefail

if ! command -v jq >/dev/null 2>&1; then
  printf '{}\n'
  exit 0
fi

input="$(cat)"
repo_root="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
commands_dir="$repo_root/.codex/commands"
observability_dir="$repo_root/.arcanum/observability"

prompt="$(printf '%s\n' "$input" | jq -r '.prompt // ""')"
turn_id="$(printf '%s\n' "$input" | jq -r '.turn_id // "unknown-turn"')"
session_id="$(printf '%s\n' "$input" | jq -r '.session_id // "codex-hook-session"')"

first_token="$(printf '%s\n' "$prompt" | sed -E 's/^[[:space:]]+//' | awk '{print $1}')"
command_name="${first_token#/}"

if [[ -z "$command_name" || ! -f "$commands_dir/$command_name.md" ]]; then
  printf '{}\n'
  exit 0
fi

command_file="$commands_dir/$command_name.md"
capability_id="$(sed -n 's/^<!-- arcanum:capability-id \(.*\) -->$/\1/p' "$command_file" | head -n 1)"
capability_kind="$(sed -n 's/^<!-- arcanum:capability-kind \(.*\) -->$/\1/p' "$command_file" | head -n 1)"
capability_tier="$(sed -n 's/^<!-- arcanum:capability-tier \(.*\) -->$/\1/p' "$command_file" | head -n 1)"
capability_alias="$(sed -n 's/^<!-- arcanum:capability-alias \(.*\) -->$/\1/p' "$command_file" | head -n 1)"
marked_command="$(sed -n 's/^<!-- arcanum:command \(.*\) -->$/\1/p' "$command_file" | head -n 1)"

if [[ -z "$capability_id" ]]; then capability_id="$command_name"; fi
if [[ -z "$capability_kind" ]]; then capability_kind="skill"; fi
if [[ -z "$capability_tier" ]]; then capability_tier="runtime"; fi
if [[ -z "$marked_command" ]]; then marked_command="$command_name"; fi

safe_turn="${turn_id//[^A-Za-z0-9._-]/-}"
run_id="arcanum-hook-$safe_turn"
run_dir="$observability_dir/runs/arcanum-hooks/$run_id"
envelope="$run_dir/pending-envelope.json"
timestamp="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

mkdir -p "$run_dir" "$observability_dir/signals"

jq -n \
  --arg timestamp "$timestamp" \
  --arg run_id "$run_id" \
  --arg session_id "$session_id" \
  --arg capability_id "$capability_id" \
  --arg capability_kind "$capability_kind" \
  --arg capability_tier "$capability_tier" \
  --arg capability_alias "$capability_alias" \
  --arg command_name "$command_name" \
  --arg marked_command "$marked_command" \
  --arg command_file ".codex/commands/$command_name.md" \
  --arg prompt "$prompt" \
  '{
    timestamp: $timestamp,
    run_id: $run_id,
    session_id: $session_id,
    sigil: $capability_id,
    tier: $capability_tier,
    mode: "command",
    capability: {
      id: $capability_id,
      kind: $capability_kind,
      tier: $capability_tier,
      mode: "command",
      alias: (if $capability_alias == "" then null else $capability_alias end)
    },
    command: {
      name: $marked_command,
      file: $command_file
    },
    request: {
      raw: $prompt,
      summary: ("Arcanum command " + $command_name),
      intent: $prompt
    },
    execution: {
      status: "partial",
      outputs: [],
      files_changed: [],
      validation: ["codex UserPromptSubmit hook opened observer envelope"],
      notes: "pending native slash command closeout"
    },
    observer: {
      quality_bar_status: "partial",
      anti_pattern_hits: [],
      workflow_gaps: [],
      output_contract_drift: false,
      reflection_trigger: "none",
      recommendation: "pending-closeout"
    },
    target_artifact: $command_file
  }' > "$envelope"

printf '%s\n' "$input" > "$run_dir/user-prompt-submit.json"

jq -n --arg run_id "$run_id" '{
  hookSpecificOutput: {
    hookEventName: "UserPromptSubmit",
    additionalContext: ("Arcanum observer envelope opened with run_id " + $run_id + ". Preserve primary work and close telemetry on Stop.")
  }
}'
