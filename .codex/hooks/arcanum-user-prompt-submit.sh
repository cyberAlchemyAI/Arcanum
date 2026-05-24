#!/usr/bin/env bash
set -euo pipefail

if ! command -v jq >/dev/null 2>&1; then
  printf '{}\n'
  exit 0
fi

input="$(cat)"
repo_root="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
commands_dir="$repo_root/.codex/commands"
skills_dir="$repo_root/.agents/skills"
observability_dir="$repo_root/.arcanum/observability"

prompt="$(printf '%s\n' "$input" | jq -r '.prompt // ""')"
turn_id="$(printf '%s\n' "$input" | jq -r '.turn_id // "unknown-turn"')"
session_id="$(printf '%s\n' "$input" | jq -r '.session_id // "codex-hook-session"')"

first_token="$(printf '%s\n' "$prompt" | sed -E 's/^[[:space:]]+//' | awk '{print $1}')"
route="none"
command_name=""
marked_command=""
command_file=""
skill_name=""
skill_file=""
skill_token=""
skill_detection_source=""
skill_domain=""
skill_description=""
capability_id=""
capability_kind=""
capability_tier=""
capability_alias=""

frontmatter_value() {
  local field="$1"
  local file="$2"
  sed -n -E "s/^${field}:[[:space:]]*//p" "$file" | head -n 1 | sed -E 's/^"//; s/"$//'
}

extract_skill_token() {
  local text="$1"
  local trimmed
  local first
  local second
  trimmed="$(printf '%s\n' "$text" | sed -E 's/^[[:space:]]+//')"
  first="$(printf '%s\n' "$trimmed" | awk '{print $1}')"
  second="$(printf '%s\n' "$trimmed" | awk '{print $2}')"

  if [[ "$first" =~ ^\$[A-Za-z0-9._-]+$ ]]; then
    printf 'explicit-dollar-token %s\n' "$first"
    return 0
  fi

  if [[ "${first,,}" == "use" && "$second" =~ ^\$[A-Za-z0-9._-]+$ ]]; then
    printf 'use-dollar-token %s\n' "$second"
    return 0
  fi

  local markdown_token
  markdown_token="$(printf '%s\n' "$trimmed" | sed -n -E 's/.*\[\$([A-Za-z0-9._-]+)\]\(.*/$\1/p' | head -n 1)"
  if [[ -n "$markdown_token" ]]; then
    printf 'markdown-skill-token %s\n' "$markdown_token"
    return 0
  fi

  return 1
}

if [[ "$first_token" == /* ]]; then
  command_name="${first_token#/}"
  if [[ -n "$command_name" && -f "$commands_dir/$command_name.md" ]]; then
    route="command"
    command_file="$commands_dir/$command_name.md"
    capability_id="$(sed -n 's/^<!-- arcanum:capability-id \(.*\) -->$/\1/p' "$command_file" | head -n 1)"
    capability_kind="$(sed -n 's/^<!-- arcanum:capability-kind \(.*\) -->$/\1/p' "$command_file" | head -n 1)"
    capability_tier="$(sed -n 's/^<!-- arcanum:capability-tier \(.*\) -->$/\1/p' "$command_file" | head -n 1)"
    capability_alias="$(sed -n 's/^<!-- arcanum:capability-alias \(.*\) -->$/\1/p' "$command_file" | head -n 1)"
    marked_command="$(sed -n 's/^<!-- arcanum:command \(.*\) -->$/\1/p' "$command_file" | head -n 1)"
  fi
fi

if [[ "$route" == "none" ]]; then
  skill_match="$(extract_skill_token "$prompt" || true)"
  if [[ -n "$skill_match" ]]; then
    skill_detection_source="${skill_match%% *}"
    skill_token="${skill_match#* }"
    skill_name="${skill_token#\$}"
    if [[ "$skill_name" =~ ^[A-Za-z0-9._-]+$ && -f "$skills_dir/$skill_name/SKILL.md" ]]; then
      route="skill"
      skill_file="$skills_dir/$skill_name/SKILL.md"
      capability_id="$(frontmatter_value "name" "$skill_file")"
      skill_description="$(frontmatter_value "description" "$skill_file")"
      capability_tier="$(frontmatter_value "tier" "$skill_file")"
      skill_domain="$(frontmatter_value "domain" "$skill_file")"
      resolved_skill_file="$(readlink -f "$skill_file" 2>/dev/null || printf '%s\n' "$skill_file")"

      if [[ -z "$capability_id" ]]; then capability_id="$skill_name"; fi
      if [[ "$capability_tier" == "arcana" || "$capability_tier" == "formulae" || "$capability_tier" == "transmutations" ]]; then
        capability_kind="sigil"
      elif [[ "$resolved_skill_file" == "$repo_root"/spells/* ]]; then
        capability_kind="spell"
        capability_tier="spell"
      else
        capability_kind="skill"
        capability_tier="runtime"
      fi
    fi
  fi
fi

if [[ "$route" == "none" ]]; then
  printf '{}\n'
  exit 0
fi

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
  --arg route "$route" \
  --arg command_name "$command_name" \
  --arg marked_command "$marked_command" \
  --arg command_file ".codex/commands/$command_name.md" \
  --arg skill_name "$skill_name" \
  --arg skill_file ".agents/skills/$skill_name/SKILL.md" \
  --arg skill_domain "$skill_domain" \
  --arg skill_description "$skill_description" \
  --arg skill_token "$skill_token" \
  --arg skill_detection_source "$skill_detection_source" \
  --arg prompt "$prompt" \
  '{
    timestamp: $timestamp,
    run_id: $run_id,
    session_id: $session_id,
    sigil: $capability_id,
    tier: $capability_tier,
    mode: $route,
    capability: {
      id: $capability_id,
      kind: $capability_kind,
      tier: $capability_tier,
      mode: $route,
      alias: (if $capability_alias == "" then null else $capability_alias end)
    },
    command: (if $route == "command" then {
      name: $marked_command,
      file: $command_file
    } else null end),
    skill: (if $route == "skill" then {
      name: $skill_name,
      file: $skill_file,
      domain: (if $skill_domain == "" then null else $skill_domain end),
      description: (if $skill_description == "" then null else $skill_description end)
    } else null end),
    skill_detection: (if $route == "skill" then {
      source: $skill_detection_source,
      token: $skill_token,
      confidence: "high"
    } else null end),
    request: {
      raw: $prompt,
      summary: (if $route == "command" then ("Arcanum command " + $command_name) else ("Codex skill " + $skill_name) end),
      intent: $prompt
    },
    execution: {
      status: "partial",
      outputs: [],
      files_changed: [],
      validation: [(if $route == "command" then "codex UserPromptSubmit hook opened observer envelope" else "codex UserPromptSubmit hook opened skill observer envelope" end)],
      notes: (if $route == "command" then "pending native slash command closeout" else "pending skill closeout" end)
    },
    observer: {
      quality_bar_status: "partial",
      anti_pattern_hits: [],
      workflow_gaps: [],
      output_contract_drift: false,
      reflection_trigger: "none",
      recommendation: "pending-closeout"
    },
    target_artifact: (if $route == "command" then $command_file else $skill_file end)
  }' > "$envelope"

printf '%s\n' "$input" > "$run_dir/user-prompt-submit.json"

jq -n --arg run_id "$run_id" '{
  hookSpecificOutput: {
    hookEventName: "UserPromptSubmit",
    additionalContext: ("Arcanum observer envelope opened with run_id " + $run_id + ". Preserve primary work and close telemetry on Stop.")
  }
}'
