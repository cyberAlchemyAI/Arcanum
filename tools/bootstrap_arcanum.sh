#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: tools/bootstrap_arcanum.sh [options]

Install Arcanum into a consuming repository.

Options:
  --target <path>       Target repository root. Default: current directory.
  --prefix <path>       Install prefix inside target. Default: .arcanum.
  --sigils <list|all>   Comma-separated sigil IDs or all commands. Default: all.
  --spells <list|all|none>
                        Comma-separated spell command IDs, all, or none. Default: all.
  --runtime <target>    Runtime adapter: codex or none. Default: none.
  --command <name>      Runtime command name. Default: arcanum-orchestrate.
  --necronomicon
                        Initialize Necronomicon repository harness session state and command.
  --no-necronomicon
                        Skip Necronomicon harness generation.
  --force               Overwrite existing installed Arcanum files.
  --dry-run             Print planned actions without writing files.
  -h, --help            Show this help.

Examples:
  tools/bootstrap_arcanum.sh --target ../my-repo --sigils all --spells all --runtime codex
  tools/bootstrap_arcanum.sh --target ../my-repo --sigils ontology-vault,context-builder --spells ontology-harness --runtime codex
USAGE
}

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
arcanum_root="$(cd "$script_dir/.." && pwd)"
target_root="$PWD"
install_prefix=".arcanum"
sigil_selection="all"
spell_selection="all"
runtime="none"
command_name="arcanum-orchestrate"
necronomicon_harness="auto"
force="false"
dry_run="false"
installed_sigil_ids=()
installed_sigil_tiers=()
installed_spell_ids=()

titleize_id() {
  printf '%s' "$1" | tr '-' ' '
}

json_escape() {
  local value="$1"
  value="${value//\\/\\\\}"
  value="${value//\"/\\\"}"
  value="${value//$'\n'/\\n}"
  printf '%s' "$value"
}

run() {
  if [[ "$dry_run" == "true" ]]; then
    printf '[dry-run] %q' "$1"
    shift || true
    for arg in "$@"; do
      printf ' %q' "$arg"
    done
    printf '\n'
  else
    "$@"
  fi
}

ensure_clean_destination() {
  local path="$1"
  if [[ -e "$path" && "$force" != "true" ]]; then
    echo "Refusing to overwrite existing path without --force: $path" >&2
    exit 1
  fi
}

write_text_file() {
  local dst="$1"
  local content="$2"
  ensure_clean_destination "$dst"
  run mkdir -p "$(dirname "$dst")"
  if [[ "$dry_run" == "true" ]]; then
    echo "[dry-run] write $dst"
  else
    printf '%s\n' "$content" > "$dst"
  fi
}

write_file_if_missing() {
  local dst="$1"
  local content="$2"
  if [[ -e "$dst" ]]; then
    return 0
  fi
  run mkdir -p "$(dirname "$dst")"
  if [[ "$dry_run" == "true" ]]; then
    echo "[dry-run] write $dst"
  else
    printf '%s\n' "$content" > "$dst"
  fi
}

touch_file_if_missing() {
  local dst="$1"
  if [[ -e "$dst" ]]; then
    return 0
  fi
  run mkdir -p "$(dirname "$dst")"
  if [[ "$dry_run" == "true" ]]; then
    echo "[dry-run] touch $dst"
  else
    : > "$dst"
  fi
}

copy_file() {
  local src="$1"
  local dst="$2"
  ensure_clean_destination "$dst"
  run mkdir -p "$(dirname "$dst")"
  if [[ "$dry_run" == "true" ]]; then
    echo "[dry-run] copy $src -> $dst"
  else
    cp "$src" "$dst"
  fi
}

sigil_alias_slug() {
  local sigil="$1"
  case "$sigil" in
    structured-interview-kits) printf 'interrogation' ;;
    *) return 1 ;;
  esac
}

sigil_alias_display() {
  local sigil="$1"
  case "$sigil" in
    structured-interview-kits) printf 'Interrogation' ;;
    *) return 1 ;;
  esac
}

sigil_alias_command() {
  local sigil="$1"
  local alias_slug
  alias_slug="$(sigil_alias_slug "$sigil")" || return 1
  printf 'arcanum-sigil-%s' "$alias_slug"
}

selected_spell_installed() {
  local spell="$1"
  printf '%s\n' "${installed_spell_ids[@]}" | grep -qx "$spell"
}

necronomicon_should_install() {
  case "$necronomicon_harness" in
    true) return 0 ;;
    false) return 1 ;;
    auto) selected_spell_installed "ontology-harness" || selected_spell_installed "necronomicon" ;;
    *) return 1 ;;
  esac
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target) target_root="$2"; shift 2 ;;
    --prefix) install_prefix="$2"; shift 2 ;;
    --sigils) sigil_selection="$2"; shift 2 ;;
    --spells) spell_selection="$2"; shift 2 ;;
    --runtime) runtime="$2"; shift 2 ;;
    --command) command_name="$2"; shift 2 ;;
    --necronomicon) necronomicon_harness="true"; shift ;;
    --no-necronomicon) necronomicon_harness="false"; shift ;;
    --force) force="true"; shift ;;
    --dry-run) dry_run="true"; shift ;;
    -h|--help) usage; exit 0 ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

case "$runtime" in
  codex|none) ;;
  github-copilot|claude)
    echo "Unsupported runtime: $runtime. Arcanum now installs only codex or none." >&2
    exit 2
    ;;
  *)
    echo "Unsupported runtime: $runtime" >&2
    exit 2
    ;;
esac

target_root="$(mkdir -p "$target_root" && cd "$target_root" && pwd)"
dest_root="$target_root/$install_prefix"
arcanum_repo_url="https://github.com/cyberAlchemyAI/arcanum"

sigil_path_for() {
  local sigil="$1"
  local tier
  for tier in formulae transmutations arcana; do
    if [[ -d "$arcanum_root/$tier/$sigil" ]]; then
      printf '%s/%s' "$tier" "$sigil"
      return 0
    fi
  done
  return 1
}

collect_selected_sigils() {
  local selection="$1"
  local sigil tier_path tier sigil_name
  if [[ "$selection" == "all" ]]; then
    for tier in formulae transmutations arcana; do
      while IFS= read -r tier_path; do
        sigil_name="$(basename "$tier_path")"
        [[ -f "$tier_path/SKILL.md" ]] || continue
        installed_sigil_ids+=("$sigil_name")
        installed_sigil_tiers+=("$tier")
      done < <(find "$arcanum_root/$tier" -mindepth 1 -maxdepth 1 -type d | sort)
    done
    return 0
  fi

  IFS=',' read -ra sigils <<< "$selection"
  for sigil in "${sigils[@]}"; do
    sigil="${sigil//[[:space:]]/}"
    [[ -n "$sigil" ]] || continue
    if ! tier_path="$(sigil_path_for "$sigil")"; then
      echo "Unknown sigil: $sigil" >&2
      exit 1
    fi
    installed_sigil_ids+=("$sigil")
    installed_sigil_tiers+=("${tier_path%%/*}")
  done
}

spell_contract_file_for() {
  local spell="$1"
  if [[ -f "$arcanum_root/spells/$spell/README.md" ]]; then
    printf '%s\n' "$arcanum_root/spells/$spell/README.md"
    return 0
  fi
  return 1
}

spell_source_path_for() {
  local spell="$1"
  if [[ -f "$arcanum_root/spells/$spell/README.md" ]]; then
    printf 'spells/%s/README.md\n' "$spell"
    return 0
  fi
  return 1
}

spell_source_url_for() {
  local spell="$1"
  local source_path
  source_path="$(spell_source_path_for "$spell")" || return 1
  printf '%s/blob/main/%s\n' "$arcanum_repo_url" "$source_path"
}

collect_selected_spells() {
  local selection="$1"
  local spell spell_file spell_dir
  if [[ "$selection" == "none" ]]; then
    return 0
  fi
  if [[ "$selection" == "all" ]]; then
    while IFS= read -r spell_dir; do
      spell="$(basename "$spell_dir")"
      [[ "$spell" == "templates" ]] && continue
      [[ -f "$spell_dir/README.md" ]] || continue
      installed_spell_ids+=("$spell")
    done < <(find "$arcanum_root/spells" -mindepth 1 -maxdepth 1 -type d | sort)
    return 0
  fi

  IFS=',' read -ra spells <<< "$selection"
  for spell in "${spells[@]}"; do
    spell="${spell//[[:space:]]/}"
    [[ -n "$spell" ]] || continue
    if ! spell_file="$(spell_contract_file_for "$spell")"; then
      echo "Unknown spell: $spell" >&2
      exit 1
    fi
    installed_spell_ids+=("$spell")
  done
}

install_observability_package() {
  local observability_root="$dest_root/observability"

  run mkdir -p \
    "$observability_root/signals" \
    "$observability_root/by-sigil" \
    "$observability_root/by-capability" \
    "$observability_root/hooks" \
    "$observability_root/runs" \
    "$observability_root/reflections"

  write_file_if_missing "$observability_root/README.md" "# Arcanum Observability

This repository-local package stores Arcanum command, sigil, and spell telemetry plus reflection state.

- signals/sigil-invocations.jsonl is the central append-only invocation ledger.
- by-sigil/ and by-capability/ hold rebuildable ledger-reference indexes.
- hooks/ stores hook operation evidence.
- runs/ stores pending and completed observer envelopes.
- reflections/ can hold reflection reports."

  write_file_if_missing "$observability_root/config.json" '{
  "version": "0.2.0",
  "storage_model": "central-ledger-reference-indexes",
  "source_of_truth": "signals/sigil-invocations.jsonl",
  "per_sigil_index_path": "by-sigil/<sigil-name>.jsonl",
  "per_capability_index_path": "by-capability/<kind>/<capability-id>.jsonl",
  "reflection_path": "reflections/",
  "thresholds": {
    "meaningful_executions": 5,
    "generated_outputs": 10,
    "related_workflow_gaps": 3,
    "severe_workflow_gaps": 1
  }
}'

  write_file_if_missing "$observability_root/reflection-state.json" '{
  "version": "0.1.0",
  "last_reflection_at": null,
  "counters": {
    "meaningful_executions": 0,
    "generated_outputs": 0,
    "related_workflow_gaps": 0,
    "severe_workflow_gaps": 0,
    "quality_bar_failures": 0,
    "output_contract_drift_events": 0
  },
  "by_sigil": {},
  "by_capability": {}
}'

  touch_file_if_missing "$observability_root/signals/sigil-invocations.jsonl"
  touch_file_if_missing "$observability_root/by-sigil/.gitkeep"
  touch_file_if_missing "$observability_root/by-capability/.gitkeep"
  touch_file_if_missing "$observability_root/hooks/.gitkeep"
  touch_file_if_missing "$observability_root/runs/.gitkeep"
  touch_file_if_missing "$observability_root/reflections/.gitkeep"
}

remove_obsolete_runtime_layers() {
  if [[ "$force" != "true" ]]; then
    return 0
  fi
  run rm -rf "$dest_root/runtimes" "$target_root/.github/skills"
}

has_obsolete_necronomicon_runtime_book() {
  local necronomicon_root="$dest_root/necronomicon"
  [[ -e "$necronomicon_root" ]] || return 1
  [[ -e "$necronomicon_root/REGISTRY.md" ]] && return 0
  [[ -e "$necronomicon_root/ROUTES.md" ]] && return 0
  [[ -d "$necronomicon_root/formulae" ]] && return 0
  [[ -d "$necronomicon_root/transmutations" ]] && return 0
  [[ -d "$necronomicon_root/arcana" ]] && return 0
  [[ -d "$necronomicon_root/spells" ]] && return 0
  [[ -d "$necronomicon_root/framework" ]] && return 0
  [[ -d "$necronomicon_root/registry" ]] && return 0
  return 1
}

remove_obsolete_necronomicon_runtime_book() {
  local necronomicon_root="$dest_root/necronomicon"
  [[ -e "$necronomicon_root" ]] || return 0
  run rm -rf \
    "$necronomicon_root/REGISTRY.md" \
    "$necronomicon_root/ROUTES.md" \
    "$necronomicon_root/formulae" \
    "$necronomicon_root/transmutations" \
    "$necronomicon_root/arcana" \
    "$necronomicon_root/spells" \
    "$necronomicon_root/framework" \
    "$necronomicon_root/registry"
}

append_file_as_fenced_block() {
  local source_file="$1"
  local target_file="$2"
  local label="$3"
  local source_url="$4"

  {
    printf '\n## %s\n\n' "$label"
    printf 'Canonical source: %s\n\n' "$source_url"
    printf '````markdown\n'
    cat "$source_file"
    printf '\n````\n'
  } >> "$target_file"
}

append_sigil_snapshot() {
  local sigil="$1"
  local tier="$2"
  local target_file="$3"
  local sigil_root="$arcanum_root/$tier/$sigil"
  if [[ -f "$sigil_root/README.md" ]]; then
    append_file_as_fenced_block "$sigil_root/README.md" "$target_file" "Canonical README Snapshot" "$arcanum_repo_url/blob/main/$tier/$sigil/README.md"
  fi
  append_file_as_fenced_block "$sigil_root/SKILL.md" "$target_file" "Canonical SKILL Snapshot" "$arcanum_repo_url/blob/main/$tier/$sigil/SKILL.md"
}

append_spell_snapshot() {
  local spell="$1"
  local target_file="$2"
  local source_file source_url
  source_file="$(spell_contract_file_for "$spell")" || {
    echo "Unknown spell: $spell" >&2
    exit 1
  }
  source_url="$(spell_source_url_for "$spell")" || {
    echo "Unknown spell source path: $spell" >&2
    exit 1
  }
  append_file_as_fenced_block "$source_file" "$target_file" "Canonical Spell Snapshot" "$source_url"
}

observer_task_zero_block() {
  local capability_id="$1"
  local capability_kind="$2"
  local capability_tier="$3"
  local command="$4"
  cat <<EOF
## Observer Envelope: Task Zero

Before doing domain work, establish the observer envelope for this Arcanum invocation.

- \`run_id\`: use an existing hook-provided run id when present; otherwise use \`arcanum-$command-<UTC timestamp>\`.
- \`capability.id\`: \`$capability_id\`
- \`capability.kind\`: \`$capability_kind\`
- \`capability.tier\`: \`$capability_tier\`
- \`capability.mode\`: \`command\`
- \`target_artifact\`: this command file
- request summary: summarize the user request before execution.
- expected outputs: list intended artifacts before execution when known.

Closeout is mandatory but must not hide the primary result. At the end, report:

- \`OBSERVATION\`
- \`LEDGER\`
- \`REFLECTION_TRIGGER\`
- \`RECOMMENDATION\`
- \`DEDUPE_KEY\`

If deterministic hook or wrapper telemetry is unavailable, preserve the result and report the observability gap.
EOF
}

write_command_file() {
  local command="$1"
  local title="$2"
  local capability_id="$3"
  local capability_kind="$4"
  local capability_tier="$5"
  local body="$6"
  local dst="$target_root/.codex/commands/$command.md"

  ensure_clean_destination "$dst"
  run mkdir -p "$(dirname "$dst")"
  if [[ "$dry_run" == "true" ]]; then
    echo "[dry-run] write Codex command $dst"
    return 0
  fi

  {
    printf '# %s\n\n' "$title"
    printf '<!-- arcanum:capability-id %s -->\n' "$capability_id"
    printf '<!-- arcanum:capability-kind %s -->\n' "$capability_kind"
    printf '<!-- arcanum:capability-tier %s -->\n' "$capability_tier"
    printf '<!-- arcanum:command %s -->\n\n' "$command"
    if [[ "$runtime" == "codex" ]]; then
      printf '<!-- arcanum:runtime codex -->\n'
      if [[ "$capability_id" == "task-session" ]]; then
        printf '<!-- arcanum:runtime-goal-adapter codex-goal -->\n'
      fi
      printf '\n'
    fi
    observer_task_zero_block "$capability_id" "$capability_kind" "$capability_tier" "$command"
    printf '\n\n%s\n' "$body"
  } > "$dst"
}

write_orchestrate_command() {
  local command="$1"
  local body
  body="$(cat <<EOF
## Objective

Route a user request to the installed Arcanum command surface.

## Process

1. Classify the request as Necronomicon, Ontology Harness, sigil usage, spell usage, install/setup, authoring, validation, observability, or help.
2. Route Necronomicon start, create, resume, close, memory, route, fallback, or capability-update requests to \`arcanum-necronomicon\` when installed.
3. Route ontology, vault, premise, session distillation, business/system branch, or bridge-validation requests to \`arcanum-ontology-harness\` when installed.
4. Route lifecycle authoring requests through \`arcanum-spell-invoke\` when installed.
5. Route explicit sigil or spell requests to the matching installed command and resolve configured aliases to canonical commands.
6. If multiple routes are plausible, ask one focused clarification.
7. Preserve selected command contracts, quality bars, anti-pattern checks, validation gates, gaps, and next route.
8. Return selected route, command used, validation result, observability result, and next action.

## Installed Command Surface
EOF
)"
  local index sigil spell alias_command alias_display
  body+=$'\n\n'
  body+="- \`$command_name\`: general Arcanum router."$'\n'
  if selected_spell_installed "ontology-harness"; then
    body+="- \`arcanum-ontology-harness\`: alias for \`arcanum-spell-ontology-harness\`."$'\n'
  fi
  if necronomicon_should_install; then
    body+="- \`arcanum-necronomicon\`: persistent repository harness command."$'\n'
  fi
  for index in "${!installed_sigil_ids[@]}"; do
    sigil="${installed_sigil_ids[$index]}"
    body+="- \`arcanum-sigil-$sigil\`"$'\n'
    if alias_command="$(sigil_alias_command "$sigil")"; then
      alias_display="$(sigil_alias_display "$sigil")"
      body+="- \`$alias_command\`: alias ($alias_display) for \`arcanum-sigil-$sigil\`."$'\n'
    fi
  done
  for spell in "${installed_spell_ids[@]}"; do
    body+="- \`arcanum-spell-$spell\`"$'\n'
  done
  body="${body%$'\n'}"
  write_command_file "$command" "Arcanum Orchestrate" "$command" "skill" "runtime" "$body"
}

write_sigil_command() {
  local command="$1"
  local sigil="$2"
  local tier="$3"
  local display_title
  display_title="$(titleize_id "$sigil")"
  local dst="$target_root/.codex/commands/$command.md"
  local body
  body="$(cat <<EOF
## Objective

Run the installed Arcanum sigil \`$sigil\` using the canonical definition snapshot embedded below.

## Process

1. Use the embedded canonical README and SKILL snapshots as the execution contract.
2. Execute only this installed sigil unless the definition explicitly delegates or the user asks to route elsewhere.
3. Preserve the selected sigil's process, quality bar, anti-patterns, output contract, validation gates, gaps, and next route.
4. Return artifact used, command used, validation result, observability result, and next action.

## Guardrails

- Keep this command focused on \`$sigil\`.
- Do not silently add, remove, or refresh capabilities.
- Do not treat generated observer telemetry as a substitute for the primary result.
EOF
)"
  if [[ "$sigil" == "task-session" && "$runtime" == "codex" ]]; then
    body+=$'\n\n'
    body+="## Repository Runtime Interface"$'\n\n'
    body+="This installed command runs in the \`codex\` runtime."$'\n\n'
    body+="Task Session is the stable Arcanum coordinator. Runtime goal-like execution is delegated through adapters under \`arcana/task-session/runtime-adapters/\`."$'\n\n'
    body+="For this repository, the current goal-like adapter is:"$'\n\n'
    body+="- adapter: \`codex-goal\`"$'\n'
    body+="- contract: \`arcana/task-session/runtime-adapters/codex-goal.md\`"$'\n'
    body+="- profile transmutation: \`transmutations/codex-goal-profile/\`"$'\n'
    body+="- native runtime command: \`/goal\`"$'\n\n'
    body+="When the user asks Task Session to execute a work-pack through a goal-like runtime, resolve one task/SWU from the work-pack, check blockers, then use the \`codex-goal\` adapter to produce or hand off a native Codex \`/goal\`. Task Session still owns final evidence review and work-pack synchronization."
  fi
  write_command_file "$command" "Arcanum Sigil: $display_title" "$sigil" "sigil" "$tier" "$body"
  [[ "$dry_run" == "true" ]] || append_sigil_snapshot "$sigil" "$tier" "$dst"
}

write_experiment_harness_mode_command() {
  local command="$1"
  local mode="$2"
  local argument_hint="$3"
  local body
  body="$(cat <<EOF
## Objective

Run Experiment Harness in \`$mode\` mode.

## Command Shape

\`\`\`text
/$command <artifact-path> $argument_hint
\`\`\`

## Process

1. Resolve the target artifact path.
2. Use the installed \`experiment-harness\` command contract as the authoritative behavior source.
3. Run or explain the equivalent script operation for \`$mode\` mode.
4. Preserve profile metadata, validation fields, observability rules, and live-loop budget gates.
5. Return artifact used, mode, command or script path, validation result, observation result, and next action.

## Guardrails

- Keep this adapter focused on Experiment Harness \`$mode\` mode.
- Do not bypass \`development/EXPERIMENT-PROFILE.md\` validation.
- Do not run live Codex loops unless the user explicitly approved the live-loop budget.
EOF
)"
  write_command_file "$command" "Experiment Harness: $mode" "experiment-harness" "sigil" "arcana" "$body"
}

write_spell_command() {
  local command="$1"
  local spell="$2"
  local display_title
  display_title="$(titleize_id "$spell")"
  local dst="$target_root/.codex/commands/$command.md"
  local body
  body="$(cat <<EOF
## Objective

Run the installed Arcanum spell \`$spell\` using the canonical spell snapshot embedded below.

## Process

1. Use the embedded canonical spell snapshot as the execution contract.
2. Execute only this installed spell unless the definition explicitly delegates or the user asks to route elsewhere.
3. Preserve the selected spell's process, quality bar, output contract, validation gates, gaps, and next route.
4. Return artifact used, command used, validation result, observability result, and next action.

## Guardrails

- Keep this command focused on \`$spell\`.
- Do not silently add, remove, or refresh capabilities.
- Do not treat generated observer telemetry as a substitute for the primary result.
EOF
)"
  write_command_file "$command" "Arcanum Spell: $display_title" "$spell" "spell" "spell" "$body"
  [[ "$dry_run" == "true" ]] || append_spell_snapshot "$spell" "$dst"
}

write_necronomicon_command() {
  necronomicon_should_install || return 0
  local command="arcanum-necronomicon"
  local dst="$target_root/.codex/commands/$command.md"
  local body
  body="$(cat <<EOF
## Objective

Create, set up, resume, research, route, maintain, update, or close a repository-local Necronomicon harness.

## Process

1. Read \`$install_prefix/necronomicon/capabilities.json\` when it exists.
2. Resolve the mode as setup, start, resume, route, checkpoint, research, implementation-research, update-capabilities, fallback-discover, maintain, or close.
3. Load active session memory from \`$install_prefix/necronomicon/sessions/\` when resuming, routing, checkpointing, researching, or maintaining.
4. Prefer selected local capabilities from the manifest before considering fallback candidates.
5. Route ontology, vault, premise, branch, bridge, confidence, or session-distillation work to \`arcanum-ontology-harness\` or \`arcanum-spell-ontology-harness\` when installed.
6. Route lifecycle authoring requests and implementation-research handoffs to \`arcanum-spell-invoke\` when installed.
7. In research mode, use bounded source order: session, inventory, ontology, docs, code, then web when available and allowed.
8. In maintain mode, aggregate route telemetry plus selected sigil/spell signals and run \`arcanum-spell-sigil-maintenance-loop\` when installed.
9. If no selected capability matches, inspect installed commands and canonical registry references, then offer 2-5 fallback candidates before adding anything.
10. Record route attempts, decisions, memory changes, gap updates, and capability update recommendations under \`$install_prefix/necronomicon/\` when mutation is allowed.
11. Return session ID, selected route, confidence, fallback status, files updated, validation result, observability result, and next action.

## Guardrails

- Keep \`$install_prefix/necronomicon/\` as harness state only.
- Do not copy formulae, transmutations, arcana, spells, registries, or framework folders into it.
- Do not add fallback capabilities silently.
- Do not treat session memory as more authoritative than source documents, registries, or implementation evidence.
EOF
  )"
  write_command_file "$command" "Arcanum Necronomicon" "necronomicon" "spell" "spell" "$body"
  [[ "$dry_run" == "true" ]] || append_spell_snapshot "necronomicon" "$dst"
  if ! selected_spell_installed "necronomicon"; then
    write_spell_command "necronomicon" "necronomicon"
  fi
}

write_codex_commands() {
  [[ "$runtime" == "codex" ]] || return 0

  if [[ "$force" == "true" ]]; then
    run rm -rf "$target_root/.codex/commands"
  fi
  run mkdir -p "$target_root/.codex/commands"

  write_orchestrate_command "$command_name"

  local index sigil tier spell alias_command
  for index in "${!installed_sigil_ids[@]}"; do
    sigil="${installed_sigil_ids[$index]}"
    tier="${installed_sigil_tiers[$index]}"
    write_sigil_command "arcanum-sigil-$sigil" "$sigil" "$tier"
    write_sigil_command "$sigil" "$sigil" "$tier"
    if [[ "$sigil" == "experiment-harness" ]]; then
      write_experiment_harness_mode_command "experiment-next" "next" ""
      write_experiment_harness_mode_command "experiment-run" "run" "<example-id|next|--all>"
      write_experiment_harness_mode_command "experiment-validate" "validate" ""
      write_experiment_harness_mode_command "experiment-observe" "observe" "[report-path]"
      write_experiment_harness_mode_command "experiment-loop" "loop" "<regime-id>"
    fi
    if alias_command="$(sigil_alias_command "$sigil")"; then
      write_sigil_command "$alias_command" "$sigil" "$tier"
      write_sigil_command "${alias_command#arcanum-sigil-}" "$sigil" "$tier"
    fi
  done

  for spell in "${installed_spell_ids[@]}"; do
    write_spell_command "arcanum-spell-$spell" "$spell"
    write_spell_command "$spell" "$spell"
    if [[ "$spell" == "ontology-harness" ]]; then
      write_spell_command "arcanum-ontology-harness" "$spell"
    fi
  done

  write_necronomicon_command
}

write_necronomicon_harness_state() {
  necronomicon_should_install || return 0

  local necronomicon_root="$dest_root/necronomicon"
  local session_root="$necronomicon_root/sessions"
  local update_root="$necronomicon_root/capability-updates"
  run mkdir -p "$session_root" "$update_root"

  write_file_if_missing "$necronomicon_root/README.md" "# Necronomicon Repository Harness

This folder stores repository-local Necronomicon harness state: selected capabilities, session memory, route ledgers, decisions, handoffs, and capability update reports.

It is not a copied Arcanum definition store. Runtime command definitions live directly under .codex/commands/, and canonical Arcanum source remains upstream or embedded in generated command snapshots.

Expected contents:

- capabilities.json records selected local commands and fallback policy.
- sessions/ stores Necronomicon memory and route history.
- capability-updates/ stores explicit add, remove, or refresh reports.

Do not place copied formulae, transmutations, arcana, spells, registries, framework folders, or runtime command trees here."

  touch_file_if_missing "$session_root/.gitkeep"
  touch_file_if_missing "$update_root/.gitkeep"

  local capabilities_file="$necronomicon_root/capabilities.json"
  if [[ -e "$capabilities_file" && "$force" != "true" ]]; then
    return 0
  fi
  if [[ "$dry_run" == "true" ]]; then
    echo "[dry-run] write $capabilities_file"
    return 0
  fi

  local created_at
  created_at="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  {
    printf '{\n'
    printf '  "version": "0.2.0",\n'
    printf '  "created_at": "%s",\n' "$(json_escape "$created_at")"
    printf '  "install_prefix": "%s",\n' "$(json_escape "$install_prefix")"
    printf '  "runtime": "%s",\n' "$(json_escape "$runtime")"
    printf '  "command_surface": ".codex/commands",\n'
    printf '  "fallback_policy": "ask-before-add",\n'
    printf '  "selected_sigils": [\n'
    local index sigil tier spell alias_slug alias_display alias_command
    for index in "${!installed_sigil_ids[@]}"; do
      sigil="${installed_sigil_ids[$index]}"
      tier="${installed_sigil_tiers[$index]}"
      printf '    {"id": "%s", "tier": "%s", "command": "arcanum-sigil-%s"' "$(json_escape "$sigil")" "$(json_escape "$tier")" "$(json_escape "$sigil")"
      if alias_slug="$(sigil_alias_slug "$sigil")"; then
        alias_display="$(sigil_alias_display "$sigil")"
        alias_command="arcanum-sigil-$alias_slug"
        printf ', "aliases": [{"name": "%s", "slug": "%s", "command": "%s"}]' "$(json_escape "$alias_display")" "$(json_escape "$alias_slug")" "$(json_escape "$alias_command")"
      fi
      printf '}'
      if [[ "$index" != "$((${#installed_sigil_ids[@]} - 1))" ]]; then
        printf ','
      fi
      printf '\n'
    done
    printf '  ],\n'
    printf '  "selected_spells": [\n'
    for index in "${!installed_spell_ids[@]}"; do
      spell="${installed_spell_ids[$index]}"
      printf '    {"id": "%s", "command": "arcanum-spell-%s"}' "$(json_escape "$spell")" "$(json_escape "$spell")"
      if [[ "$index" != "$((${#installed_spell_ids[@]} - 1))" ]]; then
        printf ','
      fi
      printf '\n'
    done
    printf '  ],\n'
    printf '  "harness_commands": [\n'
    printf '    {"id": "necronomicon", "command": "arcanum-necronomicon", "source": "spells/necronomicon/README.md"}'
    if selected_spell_installed "ontology-harness"; then
      printf ',\n'
      printf '    {"id": "ontology-harness", "command": "arcanum-ontology-harness", "source": "spells/ontology-harness/README.md"}\n'
    else
      printf '\n'
    fi
    printf '  ],\n'
    printf '  "state_paths": {\n'
    printf '    "sessions": "%s/necronomicon/sessions",\n' "$(json_escape "$install_prefix")"
    printf '    "capability_updates": "%s/necronomicon/capability-updates",\n' "$(json_escape "$install_prefix")"
    printf '    "observability": "%s/observability"\n' "$(json_escape "$install_prefix")"
    printf '  }\n'
    printf '}\n'
  } > "$capabilities_file"
}

install_hook_support() {
  [[ "$runtime" == "codex" ]] || return 0

  local hooks_dir="$target_root/.codex/hooks"
  local hooks_json="$target_root/.codex/hooks.json"
  run mkdir -p "$hooks_dir"

  copy_file "$arcanum_root/framework/observability/scripts/arcanum-hook-user-prompt-submit.sh" "$hooks_dir/arcanum-user-prompt-submit.sh"
  copy_file "$arcanum_root/framework/observability/scripts/arcanum-hook-post-tool-use.sh" "$hooks_dir/arcanum-post-tool-use.sh"
  copy_file "$arcanum_root/framework/observability/scripts/arcanum-hook-stop.sh" "$hooks_dir/arcanum-stop.sh"
  if [[ "$dry_run" != "true" ]]; then
    chmod +x "$hooks_dir/arcanum-user-prompt-submit.sh" "$hooks_dir/arcanum-post-tool-use.sh" "$hooks_dir/arcanum-stop.sh"
  fi

  write_text_file "$hooks_json" '{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": ".codex/hooks/arcanum-user-prompt-submit.sh",
            "statusMessage": "Opening Arcanum observer envelope"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Bash|apply_patch|Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": ".codex/hooks/arcanum-post-tool-use.sh",
            "statusMessage": "Recording Arcanum tool evidence"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": ".codex/hooks/arcanum-stop.sh",
            "statusMessage": "Closing Arcanum observer envelope"
          }
        ]
      }
    ]
  }
}'
}

echo "Installing Arcanum"
echo "  source:  $arcanum_root"
echo "  target:  $target_root"
echo "  prefix:  $install_prefix"
echo "  sigils:  $sigil_selection"
echo "  spells:  $spell_selection"
echo "  runtime: $runtime"

run mkdir -p "$dest_root"
if [[ "$force" == "true" ]]; then
  run rm -rf "$dest_root/source"
  remove_obsolete_necronomicon_runtime_book
  remove_obsolete_runtime_layers
elif has_obsolete_necronomicon_runtime_book; then
  echo "Found obsolete $install_prefix/necronomicon runtime-book files. Re-run with --force to remove them after preserving any local outputs you still need." >&2
  exit 1
fi

install_observability_package
collect_selected_sigils "$sigil_selection"
collect_selected_spells "$spell_selection"
write_necronomicon_harness_state
write_codex_commands
install_hook_support

echo "Arcanum bootstrap complete."
echo "Observability package: $install_prefix/observability/"
if [[ "$runtime" == "codex" ]]; then
  echo "Command surface: .codex/commands/"
  echo "Codex hooks: .codex/hooks.json"
  if selected_spell_installed "ontology-harness"; then
    echo "Ontology Harness command alias: arcanum-ontology-harness"
  fi
  if necronomicon_should_install; then
    echo "Necronomicon command: arcanum-necronomicon"
  fi
  for sigil in "${installed_sigil_ids[@]}"; do
    if alias_command="$(sigil_alias_command "$sigil")"; then
      alias_display="$(sigil_alias_display "$sigil")"
      echo "Sigil command alias ($alias_display): $alias_command -> arcanum-sigil-$sigil"
    fi
  done
fi
