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
  --profile <list|all|none>
  --profiles <list|all|none>
                        Comma-separated install profiles:
                        personal-codex, repo-codex, repo-local,
                        github-copilot, claude, observability; or all/none.
                        Default: none.
                        all excludes personal-codex.
  --runtime <target>    Compatibility alias for --profile. Values: claude,
                        copilot, github-copilot, all, or none. Codex command
                        generation requires --legacy-codex-commands.
  --surfaces <list|all|none>
                        Compatibility alias for --profile.
  --default-adapter <id>
                        Default runtime adapter for tools/arcanum --exec.
                        Default: native-skill when repo-local is installed,
                        otherwise none.
  --command <name>      Runtime command name. Default: arcanum-orchestrate.
  --codex-home <path>   Personal Codex home for personal-codex. Default:
                        CODEX_HOME or ~/.codex.
  --legacy-codex-commands
                        Explicitly generate deprecated .codex/commands files.
  --clean-legacy-codex-commands
                        Remove generated deprecated .codex/commands files and
                        preserve unknown command files.
  --prefixed-skill-packages
                        Also generate compatibility arcanum-* native skill
                        packages. Default: aliases only for Codex skill roots.
  --necronomicon
                        Initialize Necronomicon repository harness session state and command.
  --no-necronomicon
                        Skip Necronomicon harness generation.
  --force               Overwrite existing installed Arcanum files.
  --dry-run             Print planned actions without writing files.
  -h, --help            Show this help.

Examples:
  tools/bootstrap_arcanum.sh --target ../my-repo --sigils all --spells all --profile all
  tools/bootstrap_arcanum.sh --target ../my-repo --sigils ontology-vault,context-builder --spells ontology-harness --profiles repo-codex,repo-local,github-copilot,claude
  tools/bootstrap_arcanum.sh --profile personal-codex --codex-home "$HOME/.codex"
USAGE
}

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
arcanum_root="$(cd "$script_dir/.." && pwd)"
target_root="$PWD"
install_prefix=".arcanum"
sigil_selection="all"
spell_selection="all"
runtime="none"
surface_selection=""
profile_selection=""
default_adapter=""
command_name="arcanum-orchestrate"
codex_home="${CODEX_HOME:-$HOME/.codex}"
legacy_codex_commands="false"
clean_legacy_codex_commands="false"
prefixed_skill_packages="false"
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
    --surfaces) surface_selection="$2"; shift 2 ;;
    --profile|--profiles) profile_selection="$2"; shift 2 ;;
    --default-adapter) default_adapter="$2"; shift 2 ;;
    --command) command_name="$2"; shift 2 ;;
    --codex-home) codex_home="$2"; shift 2 ;;
    --legacy-codex-commands) legacy_codex_commands="true"; shift ;;
    --clean-legacy-codex-commands) clean_legacy_codex_commands="true"; shift ;;
    --prefixed-skill-packages) prefixed_skill_packages="true"; shift ;;
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
  codex|claude|copilot|github-copilot|all|none) ;;
  *)
    echo "Unsupported runtime: $runtime" >&2
    exit 2
    ;;
esac

normalize_profile_item() {
  local item="$1"
  case "$item" in
    copilot) printf 'github-copilot' ;;
    codex)
      echo "The codex surface no longer generates .codex/commands by default." >&2
      echo "Use --profile personal-codex for native Codex skills, or --legacy-codex-commands for deprecated command files." >&2
      exit 2
      ;;
    *) printf '%s' "$item" ;;
  esac
}

profiles_from_compat_selection() {
  local selection="$1"
  local value item normalized
  local -a compat_items
  case "$selection" in
    ""|none) printf 'none'; return 0 ;;
    all) printf 'all'; return 0 ;;
  esac
  IFS=',' read -ra compat_items <<< "$selection"
  local out=()
  for value in "${compat_items[@]}"; do
    item="${value//[[:space:]]/}"
    [[ -n "$item" ]] || continue
    if ! normalized="$(normalize_profile_item "$item")"; then
      return 2
    fi
    out+=("$normalized")
  done
  (IFS=','; printf '%s' "${out[*]}")
}

if [[ -z "$profile_selection" ]]; then
  if [[ -n "$surface_selection" ]]; then
    if ! profile_selection="$(profiles_from_compat_selection "$surface_selection")"; then
      exit 2
    fi
  else
    if ! profile_selection="$(profiles_from_compat_selection "$runtime")"; then
      exit 2
    fi
  fi
fi

profile_enabled() {
  local profile="$1"
  local value item
  local -a profile_items
  case "$profile_selection" in
    all)
      [[ "$profile" == "personal-codex" ]] && return 1
      return 0
      ;;
    none|"") return 1 ;;
  esac
  IFS=',' read -ra profile_items <<< "$profile_selection"
  for value in "${profile_items[@]}"; do
    item="${value//[[:space:]]/}"
    [[ "$item" == "copilot" ]] && item="github-copilot"
    [[ "$item" == "$profile" ]] && return 0
  done
  return 1
}

surface_enabled() {
  local surface="$1"
  case "$surface" in
    codex) [[ "$legacy_codex_commands" == "true" ]] ;;
    claude) profile_enabled "claude" ;;
    copilot) profile_enabled "github-copilot" ;;
    *) return 1 ;;
  esac
}

case "$profile_selection" in
  all|none|"") ;;
  *)
    IFS=',' read -ra _profile_items <<< "$profile_selection"
    for _profile_item in "${_profile_items[@]}"; do
      _profile_item="${_profile_item//[[:space:]]/}"
      [[ "$_profile_item" == "copilot" ]] && _profile_item="github-copilot"
      case "$_profile_item" in
        personal-codex|repo-codex|repo-local|github-copilot|claude|observability) ;;
        *)
          echo "Unsupported install profile: $_profile_item" >&2
          echo "Supported profiles: personal-codex, repo-codex, repo-local, github-copilot, claude, observability, all, none" >&2
          exit 2
          ;;
      esac
    done
    ;;
esac

if [[ -z "$default_adapter" ]]; then
  if profile_enabled "repo-local"; then
    default_adapter="native-skill"
  else
    default_adapter="none"
  fi
fi

case "$default_adapter" in
  native-skill|codex-skill|claude-skill|copilot-instructions|local-skill|codex-exec|codex-bypass|dry-run|none|null) ;;
  *)
    echo "Unsupported default adapter: $default_adapter" >&2
    echo "Supported default adapters: native-skill, codex-skill, claude-skill, copilot-instructions, local-skill, codex-exec, codex-bypass, dry-run, none" >&2
    exit 2
    ;;
esac

target_profile_writes() {
  profile_enabled "repo-codex" && return 0
  profile_enabled "repo-local" && return 0
  profile_enabled "github-copilot" && return 0
  profile_enabled "claude" && return 0
  profile_enabled "observability" && return 0
  [[ "$legacy_codex_commands" == "true" ]] && return 0
  return 1
}

if [[ -d "$target_root" ]]; then
  target_root="$(cd "$target_root" && pwd)"
elif target_profile_writes; then
  target_root="$(mkdir -p "$target_root" && cd "$target_root" && pwd)"
elif command -v realpath >/dev/null 2>&1; then
  target_root="$(realpath -m "$target_root")"
else
  target_root="$(cd "$(dirname "$target_root")" && pwd)/$(basename "$target_root")"
fi
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

This repository-local package stores Arcanum observability configuration and structure markers.

- signals/sigil-invocations.jsonl is generated runtime evidence and is local by default unless explicitly promoted.
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

  touch_file_if_missing "$observability_root/by-sigil/.gitkeep"
  touch_file_if_missing "$observability_root/by-capability/.gitkeep"
  touch_file_if_missing "$observability_root/hooks/.gitkeep"
  touch_file_if_missing "$observability_root/runs/.gitkeep"
  touch_file_if_missing "$observability_root/reflections/.gitkeep"
}

adapter_profile_content() {
  local adapter="$1"
  case "$adapter" in
    native-skill|codex-skill|claude-skill|copilot-instructions|local-skill)
      local runtime_kind="native-agent-skill-surface"
      local package_shape="host-inferred native skill or instruction package"
      local alias_note="null"
      case "$adapter" in
        native-skill)
          runtime_kind="abstract-native-runtime-selector"
          package_shape="selected host-native package"
          ;;
        codex-skill)
          package_shape="\$CODEX_HOME/skills/<name>/SKILL.md"
          ;;
        claude-skill)
          package_shape=".claude/skills/<name>/SKILL.md plus optional .claude/agents/<name>.md"
          ;;
        copilot-instructions)
          package_shape=".github/skills/<name>/SKILL.md plus .github/instructions/*.instructions.md"
          ;;
        local-skill)
          runtime_kind="compatibility-alias"
          package_shape="\$CODEX_HOME/skills/<name>/SKILL.md"
          alias_note="\"Compatibility alias for codex-skill while older artifacts are migrated.\""
          ;;
      esac
      cat <<JSON
{
  "adapter_id": "$adapter",
  "runtime_kind": "$runtime_kind",
  "execution_mode": "parent-orchestrated-handoff",
  "state_model": "current-session-and-native-runtime",
  "isolation_model": "no-nested-model-cli",
  "input_shape": "command-prompt-plus-dispatch-step",
  "output_shape": "artifact-plus-stage-receipt",
  "failure_model": "passed|flagged|blocked|interrupted|timeout",
  "package_shape": "$package_shape",
  "alias_note": $alias_note,
  "capabilities": [
    "represent native runtime execution without spawning nested model CLI",
    "return handoff and receipt requirements for parent orchestration",
    "record canonical source and alias provenance for generated native packages"
  ],
  "limitations": [
    "not callable as an autonomous shell-only model runtime",
    "requires the parent runtime to own skill or agent execution and join"
  ],
  "validation_surface": [
    "adapter profile evidence",
    "dispatch-spec validation",
    "stage receipt validation",
    "observer or fallback telemetry receipt"
  ]
}
JSON
      ;;
    local-skill)
      cat <<'JSON'
{
  "adapter_id": "local-skill",
  "runtime_kind": "native-agent-skill-surface",
  "execution_mode": "parent-orchestrated-handoff",
  "state_model": "current-session-and-native-subagents",
  "isolation_model": "no-nested-model-cli",
  "input_shape": "command-prompt-plus-dispatch-step",
  "output_shape": "artifact-plus-stage-receipt",
  "failure_model": "passed|flagged|blocked|interrupted|timeout",
  "capabilities": [
    "represent native skill/subagent execution without spawning nested Codex CLI",
    "return handoff and receipt requirements for parent orchestration"
  ],
  "limitations": [
    "not callable as an autonomous shell-only model runtime",
    "requires the parent agent surface to own skill execution, subagent spawn, and join"
  ],
  "validation_surface": [
    "adapter profile evidence",
    "dispatch-spec validation",
    "stage receipt validation",
    "observer or fallback telemetry receipt"
  ]
}
JSON
      ;;
    dry-run)
      cat <<'JSON'
{
  "adapter_id": "dry-run",
  "runtime_kind": "dry-run",
  "execution_mode": "simulated",
  "state_model": "stateless",
  "isolation_model": "filesystem-output-only",
  "input_shape": "command-prompt",
  "output_shape": "requested-output",
  "failure_model": "passed|blocked|failed",
  "capabilities": [
    "validate command-surface adapter dispatch without external execution"
  ],
  "limitations": [
    "does not prove model-backed execution"
  ],
  "validation_surface": [
    "tools/arcanum --exec --adapter dry-run",
    "requested output exists"
  ]
}
JSON
      ;;
    codex-exec)
      cat <<'JSON'
{
  "adapter_id": "codex-exec",
  "runtime_kind": "model-backed-cli",
  "execution_mode": "synchronous-process",
  "state_model": "normal-codex-cli-state",
  "isolation_model": "no-run-local-codex-home-by-default",
  "input_shape": "command-prompt",
  "output_shape": "requested-output",
  "failure_model": "passed|flagged|blocked|failed",
  "capabilities": [
    "execute Codex CLI with an Arcanum command prompt",
    "capture final output in the requested output path"
  ],
  "limitations": [
    "does not use native /goal",
    "does not own orchestrator semantics",
    "does not create per-run private CLI state links by default"
  ],
  "validation_surface": [
    "adapter profile evidence",
    "Codex CLI exit classification",
    "STATUS.json validation_grade",
    "events.jsonl closeout"
  ]
}
JSON
      ;;
    codex-bypass)
      cat <<'JSON'
{
  "adapter_id": "codex-bypass",
  "runtime_kind": "model-backed-cli",
  "execution_mode": "synchronous-process",
  "state_model": "normal-codex-cli-state",
  "isolation_model": "codex-cli-danger-full-access",
  "input_shape": "command-prompt",
  "output_shape": "requested-output",
  "failure_model": "passed|flagged|blocked|failed",
  "capabilities": [
    "execute Codex CLI with an Arcanum command prompt when explicitly requested",
    "capture final output in the requested output path"
  ],
  "limitations": [
    "bypasses Codex CLI sandbox and approval prompts",
    "intended only for externally trusted automation environments"
  ],
  "validation_surface": [
    "adapter profile evidence",
    "Codex CLI exit classification",
    "timeout classification",
    "STATUS.json validation_grade",
    "events.jsonl closeout"
  ]
}
JSON
      ;;
    *)
      return 1
      ;;
  esac
}

runtime_config_content() {
  local command_surface="$1"
  local adapter="$2"
  local adapter_json
  if [[ "$adapter" == "none" || "$adapter" == "null" ]]; then
    adapter_json="null"
  else
    adapter_json="\"$(json_escape "$adapter")\""
  fi
  cat <<JSON
{
  "schema_version": "arcanum.runtime.config.v1",
  "command_surface": "$(json_escape "$command_surface")",
  "default_adapter": $adapter_json,
  "adapters": {
    "native-skill": {
      "enabled": true,
      "profile_path": "$install_prefix/runtime/adapters/native-skill.json"
    },
    "codex-skill": {
      "enabled": true,
      "profile_path": "$install_prefix/runtime/adapters/codex-skill.json"
    },
    "claude-skill": {
      "enabled": true,
      "profile_path": "$install_prefix/runtime/adapters/claude-skill.json"
    },
    "copilot-instructions": {
      "enabled": true,
      "profile_path": "$install_prefix/runtime/adapters/copilot-instructions.json"
    },
    "local-skill": {
      "enabled": true,
      "profile_path": "$install_prefix/runtime/adapters/local-skill.json"
    },
    "codex-exec": {
      "enabled": true,
      "profile_path": "$install_prefix/runtime/adapters/codex-exec.json"
    },
    "codex-bypass": {
      "enabled": true,
      "profile_path": "$install_prefix/runtime/adapters/codex-bypass.json"
    },
    "dry-run": {
      "enabled": true,
      "profile_path": "$install_prefix/runtime/adapters/dry-run.json"
    }
  }
}
JSON
}

install_runtime_config() {
  local runtime_root="$dest_root/runtime"
  local command_surface="$profile_selection"
  write_text_file "$runtime_root/config.json" "$(runtime_config_content "$command_surface" "$default_adapter")"
  write_text_file "$runtime_root/adapters/native-skill.json" "$(adapter_profile_content native-skill)"
  write_text_file "$runtime_root/adapters/codex-skill.json" "$(adapter_profile_content codex-skill)"
  write_text_file "$runtime_root/adapters/claude-skill.json" "$(adapter_profile_content claude-skill)"
  write_text_file "$runtime_root/adapters/copilot-instructions.json" "$(adapter_profile_content copilot-instructions)"
  write_text_file "$runtime_root/adapters/local-skill.json" "$(adapter_profile_content local-skill)"
  write_text_file "$runtime_root/adapters/dry-run.json" "$(adapter_profile_content dry-run)"
  write_text_file "$runtime_root/adapters/codex-exec.json" "$(adapter_profile_content codex-exec)"
  write_text_file "$runtime_root/adapters/codex-bypass.json" "$(adapter_profile_content codex-bypass)"
}

install_repo_local_tools() {
  profile_enabled "repo-local" || return 0

  copy_file "$arcanum_root/tools/arcanum" "$target_root/tools/arcanum"
  if [[ "$dry_run" != "true" ]]; then
    chmod +x "$target_root/tools/arcanum"
  fi
}

installed_capability_list_markdown() {
  local index sigil tier spell
  printf -- '- `arcanum-orchestrate`: route requests through installed Arcanum capabilities.\n'
  for index in "${!installed_sigil_ids[@]}"; do
    sigil="${installed_sigil_ids[$index]}"
    tier="${installed_sigil_tiers[$index]}"
    printf -- '- `%s` sigil (`%s` tier)\n' "$sigil" "$tier"
  done
  for spell in "${installed_spell_ids[@]}"; do
    printf -- '- `%s` spell\n' "$spell"
  done
}

derive_skill_description() {
  # Derive a Claude/Codex skill description for a source file that has no
  # frontmatter of its own (e.g. spell README.md). Uses the first paragraph of
  # the "## Purpose" section, collapsed to a single YAML-safe line.
  local source_file="$1"
  local fallback="$2"
  local desc
  desc="$(awk '
    /^##[[:space:]]+Purpose([[:space:]]|$)/ { grab=1; next }
    grab && /^##[[:space:]]/ { exit }
    grab {
      if ($0 ~ /^[[:space:]]*$/) { if (collected) exit; else next }
      line=$0
      gsub(/^[[:space:]]+|[[:space:]]+$/, "", line)
      out = (out=="" ? line : out " " line)
      collected=1
    }
    END { print out }
  ' "$source_file")"
  if [[ -z "$desc" ]]; then
    desc="$fallback"
  fi
  desc="${desc//\\/\\\\}"
  desc="${desc//\"/\\\"}"
  printf '%s' "$desc"
}

generated_skill_provenance_fields() {
  local runtime="$1"
  local canonical_source="$2"
  local alias_of="$3"
  cat <<EOF
surface_kind: generated-native-runtime-package
runtime: $runtime
canonical_source: $canonical_source
alias_of: $alias_of
generated_by: tools/bootstrap_arcanum.sh --profile
mutation_policy: regenerate-from-canonical-source
EOF
}

generated_skill_frontmatter() {
  local runtime="$1"
  local canonical_source="$2"
  local alias_of="$3"
  cat <<EOF
---
$(generated_skill_provenance_fields "$runtime" "$canonical_source" "$alias_of")
---

EOF
}

copy_generated_skill_support() {
  local source_file="$1"
  local package_dir="$2"
  local source_dir support_dir support_file src dst

  source_dir="$(dirname "$source_file")"

  # Copy every top-level support file the source ships, except SKILL.md (the
  # runtime SKILL.md is generated separately just above with rewritten
  # frontmatter). This is a denylist, not an allowlist: sigils/spells carry
  # mode-contract files (invoke's define/design/plan/handoff/refresh/full/
  # validate.md), loop docs (refine/REFINEMENT-LOOP.md), synthesis docs, etc.
  # that are required at runtime and must not be silently dropped. The `*`
  # glob skips dotfiles (.DS_Store and friends).
  for src in "$source_dir"/*; do
    [[ -f "$src" ]] || continue
    support_file="$(basename "$src")"
    [[ "$support_file" == "SKILL.md" ]] && continue
    dst="$package_dir/$support_file"

    ensure_clean_destination "$dst"
    run mkdir -p "$package_dir"
    copy_file "$src" "$dst"
  done

  # Copy every support directory except `development/`. `development/` holds
  # authoring/governance history (refresh packs, task sessions, evidence,
  # fixtures) that is not needed to run the skill and would bloat every
  # generated package, so it is the one directory intentionally excluded.
  # Everything else a sigil/spell ships (templates, examples, assets, scripts,
  # schemas, library, runtime-adapters, workflow-profiles, tools, ...) is
  # runtime-relevant and is copied.
  for src in "$source_dir"/*/; do
    [[ -d "$src" ]] || continue
    support_dir="$(basename "$src")"
    [[ "$support_dir" == "development" ]] && continue
    dst="$package_dir/$support_dir"

    if [[ -e "$dst" && "$force" == "true" ]]; then
      run rm -rf "$dst"
    fi
    ensure_clean_destination "$dst"
    run mkdir -p "$package_dir"

    if [[ "$dry_run" == "true" ]]; then
      echo "[dry-run] copy generated skill support $src -> $dst"
      continue
    fi

    tar \
      --exclude='*/__pycache__' \
      --exclude='*.pyc' \
      --exclude='.DS_Store' \
      -C "$source_dir" -cf - "$support_dir" | tar -C "$package_dir" -xf -
  done
}

# Emit a source SKILL.md frontmatter+body to stdout, skipping the leading `---`.
# Replaces the `name:` line when name_override is given, and for runtime=claude
# maps Codex-flavored tool tokens in `allowed-tools` to their real Claude names
# (Task -> Agent, AskQuestions -> AskUserQuestion). Other runtimes pass through
# unchanged. Sources are never edited; the rewrite happens only on the generated
# copy.
emit_generated_skill_stream() {
  local source_file="$1"
  local runtime="$2"
  local name_override="${3:-}"

  tail -n +2 "$source_file" | awk -v name="$name_override" -v runtime="$runtime" '
    BEGIN { in_fm=1; replaced=0 }
    in_fm && $0 == "---" {
      if (name != "" && !replaced) { print "name: " name; replaced=1 }
      print
      in_fm=0
      next
    }
    in_fm && $0 ~ /^name:/ {
      if (name != "") {
        if (!replaced) { print "name: " name; replaced=1 }
        next
      }
      print
      next
    }
    in_fm && runtime == "claude" && $0 ~ /^allowed-tools:/ {
      hdr = $0
      sub(/^allowed-tools:[[:space:]]*/, "", hdr)
      n = split(hdr, arr, /,/)
      out = ""
      delete seen
      for (i = 1; i <= n; i++) {
        t = arr[i]
        gsub(/^[[:space:]]+|[[:space:]]+$/, "", t)
        if (t == "") continue
        if (t == "Task") t = "Agent"
        else if (t == "AskQuestions") t = "AskUserQuestion"
        if (t in seen) continue
        seen[t] = 1
        out = (out == "" ? t : out ", " t)
      }
      print "allowed-tools: " out
      next
    }
    { print }
  '
}

write_generated_skill_file() {
  local runtime="$1"
  local package_dir="$2"
  local canonical_source="$3"
  local source_file="$4"
  local alias_of="${5:-null}"
  local name_override="${6:-}"
  local dst="$package_dir/SKILL.md"

  ensure_clean_destination "$dst"
  run mkdir -p "$package_dir"
  if [[ "$dry_run" == "true" ]]; then
    echo "[dry-run] write generated $runtime skill $dst from $canonical_source"
    return 0
  fi

  {
    if [[ "$(head -n 1 "$source_file")" == "---" ]]; then
      printf '%s\n' '---'
      generated_skill_provenance_fields "$runtime" "$canonical_source" "$alias_of"
      emit_generated_skill_stream "$source_file" "$runtime" "$name_override"
    else
      if [[ -n "$name_override" ]]; then
        cat <<EOF
---
name: $name_override
description: "$(derive_skill_description "$source_file" "Composed Arcanum spell: $name_override.")"
$(generated_skill_provenance_fields "$runtime" "$canonical_source" "$alias_of")
---

EOF
      else
        generated_skill_frontmatter "$runtime" "$canonical_source" "$alias_of"
      fi
      cat "$source_file"
    fi
  } > "$dst"
  copy_generated_skill_support "$source_file" "$package_dir"
}

write_generated_alias_skill() {
  local runtime="$1"
  local package_dir="$2"
  local canonical_source="$3"
  local alias_of="$4"
  local display_name="$5"
  local dst="$package_dir/SKILL.md"

  ensure_clean_destination "$dst"
  run mkdir -p "$package_dir"
  if [[ "$dry_run" == "true" ]]; then
    echo "[dry-run] write generated $runtime alias skill $dst -> $alias_of"
    return 0
  fi

  {
    cat <<EOF
---
name: $(basename "$package_dir")
description: "Alias package for $alias_of."
$(generated_skill_provenance_fields "$runtime" "$canonical_source" "$alias_of")
---

EOF
    cat <<EOF
# Skill: $display_name

Alias package for \`$alias_of\`.

Use the canonical generated package named \`$alias_of\`. This file exists only so the runtime can discover a familiar invocation name.
EOF
  } > "$dst"
}

write_orchestrate_skill_file() {
  local runtime="$1"
  local package_dir="$2"
  local dst="$package_dir/SKILL.md"

  ensure_clean_destination "$dst"
  run mkdir -p "$package_dir"
  if [[ "$dry_run" == "true" ]]; then
    echo "[dry-run] write generated $runtime orchestrate skill $dst"
    return 0
  fi

  {
    cat <<EOF
---
name: $(basename "$package_dir")
description: "Route repository work through installed Arcanum capabilities."
$(generated_skill_provenance_fields "$runtime" "arcanum/runtime/orchestrate" "null")
---

EOF
    cat <<EOF
# Skill: Arcanum Orchestrate

<objective>
Route repository work through installed Arcanum sigils and spells while preserving dispatch-spec, task-session, and observability boundaries.
</objective>

<installed-capabilities>
$(installed_capability_list_markdown)
</installed-capabilities>

<process>
1. Classify the request as authoring, refinement, task execution, observability, install/setup, validation, or help.
2. Prefer the host runtime's native skill, agent, or instruction execution for model-backed work.
3. Use native skills, subagents, and dispatch-spec validators for active execution evidence.
4. Treat \`tools/arcanum\` helpers as deterministic handoff preparation or explicit legacy compatibility only.
5. Do not spawn nested model-backed CLIs for the same stage.
6. Return capability, mode, receipt kind, execution surface, status, artifacts, validation, observer status, blockers, and handoff note.
</process>
EOF
  } > "$dst"
}

write_runtime_skill_packages() {
  local runtime="$1"
  local root="$2"
  local prefix_name="$3"
  local index sigil tier spell source_file canonical_source package_name alias_slug alias_display visible_name

  write_orchestrate_skill_file "$runtime" "$root/orchestrate"
  if [[ "$prefixed_skill_packages" == "true" && -n "$prefix_name" ]]; then
    write_generated_alias_skill "$runtime" "$root/arcanum-orchestrate" "arcanum/runtime/orchestrate" "orchestrate" "Arcanum Orchestrate"
  fi

  for index in "${!installed_sigil_ids[@]}"; do
    sigil="${installed_sigil_ids[$index]}"
    tier="${installed_sigil_tiers[$index]}"
    source_file="$arcanum_root/$tier/$sigil/SKILL.md"
    canonical_source="$tier/$sigil/SKILL.md"
    package_name="$prefix_name$sigil"
    visible_name="$sigil"
    if alias_slug="$(sigil_alias_slug "$sigil")"; then
      alias_display="$(sigil_alias_display "$sigil")"
      visible_name="$alias_slug"
    fi
    write_generated_skill_file "$runtime" "$root/$visible_name" "$canonical_source" "$source_file" "null" "$visible_name"
    if [[ "$visible_name" != "$sigil" ]]; then
      write_generated_alias_skill "$runtime" "$root/$sigil" "$canonical_source" "$visible_name" "$sigil"
    fi
    if [[ "$prefixed_skill_packages" == "true" && -n "$prefix_name" ]]; then
      write_generated_alias_skill "$runtime" "$root/$package_name" "$canonical_source" "$visible_name" "$sigil"
    fi
  done

  for spell in "${installed_spell_ids[@]}"; do
    source_file="$(spell_contract_file_for "$spell")" || continue
    canonical_source="$(spell_source_path_for "$spell")" || continue
    package_name="$prefix_name$spell"
    write_generated_skill_file "$runtime" "$root/$spell" "$canonical_source" "$source_file" "null" "$spell"
    if [[ "$prefixed_skill_packages" == "true" && -n "$prefix_name" ]]; then
      write_generated_alias_skill "$runtime" "$root/$package_name" "$canonical_source" "$spell" "$spell"
    fi
  done
}

write_copilot_skill_packages() {
  local root="$1"
  local runtime="github-copilot"
  local index sigil tier spell source_file canonical_source package_name alias_slug alias_display

  write_orchestrate_skill_file "$runtime" "$root/arcanum-orchestrate"

  for index in "${!installed_sigil_ids[@]}"; do
    sigil="${installed_sigil_ids[$index]}"
    tier="${installed_sigil_tiers[$index]}"
    source_file="$arcanum_root/$tier/$sigil/SKILL.md"
    canonical_source="$tier/$sigil/SKILL.md"
    package_name="arcanum-sigil-$sigil"
    write_generated_skill_file "$runtime" "$root/$package_name" "$canonical_source" "$source_file" "null"
    if alias_slug="$(sigil_alias_slug "$sigil")"; then
      alias_display="$(sigil_alias_display "$sigil")"
      write_generated_alias_skill "$runtime" "$root/arcanum-sigil-$alias_slug" "$canonical_source" "$package_name" "$alias_display"
    fi
  done

  for spell in "${installed_spell_ids[@]}"; do
    source_file="$(spell_contract_file_for "$spell")" || continue
    canonical_source="$(spell_source_path_for "$spell")" || continue
    package_name="arcanum-spell-$spell"
    write_generated_skill_file "$runtime" "$root/$package_name" "$canonical_source" "$source_file" "null"
  done

  if selected_spell_installed "ontology-harness"; then
    write_generated_alias_skill \
      "$runtime" \
      "$root/arcanum-necronomicon" \
      "spells/ontology-harness/README.md" \
      "arcanum-spell-ontology-harness" \
      "Necronomicon"
  fi

  if selected_spell_installed "necronomicon"; then
    write_generated_alias_skill \
      "$runtime" \
      "$root/arcanum-necronomicon-session" \
      "spells/necronomicon/README.md" \
      "arcanum-spell-necronomicon" \
      "Necronomicon Session"
    write_generated_alias_skill \
      "$runtime" \
      "$root/arcanum-spell-necronomicon-session" \
      "spells/necronomicon/README.md" \
      "arcanum-spell-necronomicon" \
      "Necronomicon Session"
  fi
}

write_personal_codex_surface() {
  profile_enabled "personal-codex" || return 0
  write_runtime_skill_packages "codex" "$codex_home/skills" "arcanum-"
}

write_repo_codex_surface() {
  profile_enabled "repo-codex" || return 0

  write_runtime_skill_packages "codex" "$target_root/.agents/skills" "arcanum-"
  write_file_if_missing "$target_root/AGENTS.md" "# Agent Instructions

This repository exposes Arcanum capabilities as repo-scoped Codex skills under \`.agents/skills/\`.

Core rules:

- Invoke skills explicitly with \`\$skill-name\` when the request names a capability.
- Use \`registry/SIGILS.md\` and \`registry/SPELLS.md\` for capability lookup when available.
- Use \`formulae/dispatch-spec/\` for route-shape validation when installed.
- Use \`spells/invoke/\` for lifecycle authoring artifacts.
- Use \`arcana/task-session/\` for bounded execution.
- Keep \`tools/arcanum\` deterministic: resolve, validate, handoff, and legacy adapter compatibility.
- Prefer native Codex skill execution over nested model-backed CLI execution.
"
}

write_claude_surface() {
  surface_enabled "claude" || return 0

  local claude_root="$target_root/.claude"
  write_runtime_skill_packages "claude" "$claude_root/skills" "arcanum-"
  run mkdir -p "$claude_root/agents"

  write_text_file "$claude_root/agents/arcanum-stage-worker.md" "---
description: Execute one bounded Arcanum stage and return a telemetry receipt.
tools:
  - Read
  - Glob
  - Grep
  - Bash
  - Edit
skills:
  - orchestrate
---

# Arcanum Stage Worker

Execute exactly one bounded stage from a parent Arcanum dispatch.

Rules:

- Read the parent dispatch step, source links, write scope, done criteria, and validation surface first.
- Keep edits inside the assigned write scope.
- Prefer local deterministic commands and native skill execution.
- Do not call nested model-backed CLIs such as \`codex exec\`, \`claude\`, or another autonomous agent runner.
- Return a receipt with status, artifacts, validation, observer status, blockers, and handoff note.
"

  write_file_if_missing "$target_root/CLAUDE.md" "# Claude Code Instructions

Use the project Arcanum skill at \`.claude/skills/orchestrate/SKILL.md\` for Arcanum work.

Use \`.claude/agents/arcanum-stage-worker.md\` for bounded sidecar stages when subagent delegation is helpful.

Preserve Arcanum boundaries:

- \`dispatch-spec\` validates route shape.
- \`invoke\` authors define/design/plan/handoff/refresh artifacts.
- \`task-session\` executes one bounded task or SWU.
- \`tools/arcanum\` is a deterministic resolver, validator, handoff, and legacy adapter surface.
- Native skills and subagents are preferred over nested model-backed CLI execution.
"

  # Blocking gate: a generated package with a non-Claude tool name, a name that
  # does not match its directory, a missing description, or a dangling skills:
  # reference must fail the install rather than ship a silently broken skill.
  if [[ "$dry_run" != "true" ]]; then
    if [[ -x "$script_dir/validate-claude-skills.sh" ]]; then
      if ! "$script_dir/validate-claude-skills.sh" "$claude_root/skills"; then
        echo "Claude skill surface failed validation; install blocked." >&2
        echo "Fix the canonical sources and regenerate (do not edit generated packages)." >&2
        exit 1
      fi
    else
      echo "Warning: validate-claude-skills.sh not found; skipping Claude surface validation." >&2
    fi
  fi
}

write_copilot_surface() {
  surface_enabled "copilot" || return 0

  write_copilot_skill_packages "$target_root/.github/skills"
  run mkdir -p "$target_root/.github/instructions"

  write_file_if_missing "$target_root/.github/copilot-instructions.md" "# Arcanum Copilot Instructions

This repository uses Arcanum governance for reusable agent capabilities.

For Arcanum work:

- Read \`AGENTS.md\` first when available.
- Treat \`dispatch-spec\` as the route-shape validator.
- Treat \`invoke\` as the define/design/plan/handoff authoring surface.
- Treat \`task-session\` as the execution owner for one bounded task or SWU.
- Prefer native Copilot agent execution with repository instructions over nested model-backed CLI calls.
- Keep \`tools/arcanum\` as a deterministic resolver, validator, handoff, and legacy adapter compatibility surface.
- Return artifact paths, validation result, observer status, blockers, and follow-up.
"

  write_text_file "$target_root/.github/instructions/arcanum.instructions.md" "---
applyTo: \"**\"
---

# Arcanum Path Instructions

When editing Arcanum files:

- Preserve owner boundaries between formulae, transmutations, arcana, spells, framework, registry, and generated evidence.
- Do not rewrite historical generated evidence unless the task explicitly owns cleanup.
- Use dispatch-spec for multi-stage route validation.
- Use Task Session for bounded implementation.
- Prefer native agent execution and returned receipts over nested \`codex exec\` style runtime calls.
"

  write_file_if_missing "$target_root/AGENTS.md" "# Agent Instructions

Arcanum agent surfaces should use native skill or agent execution with bounded receipts.

Core rules:

- Use \`registry/SIGILS.md\` and \`registry/SPELLS.md\` for capability lookup.
- Use \`formulae/dispatch-spec/\` for route-shape validation.
- Use \`spells/invoke/\` for lifecycle authoring artifacts.
- Use \`arcana/task-session/\` for bounded execution.
- Keep \`tools/arcanum\` deterministic: resolve, validate, handoff, and legacy adapter compatibility.
- Do not treat historical generated run evidence as active runtime policy.
"
}

remove_obsolete_runtime_layers() {
  if [[ "$force" != "true" ]]; then
    return 0
  fi
  if profile_enabled "repo-local"; then
    run rm -rf "$dest_root/runtimes"
  fi
  if profile_enabled "repo-codex"; then
    run rm -rf "$target_root/.agents/skills"
  fi
  if profile_enabled "github-copilot"; then
    run rm -rf "$target_root/.github/skills"
  fi
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
    if surface_enabled "codex"; then
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
  if [[ "$sigil" == "task-session" ]] && surface_enabled "codex"; then
    body+=$'\n\n'
    body+="## Repository Runtime Interface"$'\n\n'
    body+="This deprecated installed command is a compatibility entry point for repositories that explicitly request legacy Codex command files."$'\n\n'
    body+="Task Session is the stable Arcanum coordinator. Runtime-backed execution defaults to the local skill/subagent surface. \`tools/arcanum --exec\` remains a deterministic handoff and legacy adapter compatibility surface, not active native execution proof."$'\n\n'
    body+="For this repository, the installed default adapter is selected in \`$install_prefix/runtime/config.json\` and can be changed without editing command files:"$'\n\n'
    body+="- inspect: \`tools/arcanum --get-default-adapter\`"$'\n'
    body+="- change: \`tools/arcanum --set-default-adapter <adapter-id>\`"$'\n'
    body+="- override one legacy/handoff run: \`tools/arcanum --exec --adapter <adapter-id> ...\`"$'\n\n'
    body+="When the user asks Task Session to execute a work-pack through a runtime, resolve one task/SWU from the work-pack, check blockers, then delegate only the selected native capability or approved subagent work through the configured adapter. Task Session still owns final evidence review and work-pack synchronization."
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
  surface_enabled "codex" || return 0

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

clean_generated_codex_commands() {
  local commands_root="$target_root/.codex/commands"
  [[ -d "$commands_root" ]] || return 0

  local command_file
  while IFS= read -r command_file; do
    if grep -q '^<!-- arcanum:command ' "$command_file"; then
      run rm -f "$command_file"
    else
      echo "Preserving non-generated Codex command: ${command_file#$target_root/}" >&2
    fi
  done < <(find "$commands_root" -maxdepth 1 -type f -name '*.md' | sort)

  if [[ "$dry_run" != "true" ]] && find "$commands_root" -maxdepth 1 -type f -name '*.md' | read -r _; then
    return 0
  fi
  run rmdir "$commands_root" 2>/dev/null || true
  run rmdir "$target_root/.codex" 2>/dev/null || true
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
  surface_enabled "codex" || return 0

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
echo "  profiles: $profile_selection"
echo "  default adapter: $default_adapter"
echo "  clean legacy commands: $clean_legacy_codex_commands"

if target_profile_writes && [[ "$profile_selection" != "none" ]]; then
  run mkdir -p "$target_root"
fi
if profile_enabled "repo-local" || profile_enabled "observability"; then
  run mkdir -p "$dest_root"
fi
if [[ "$force" == "true" && ( "$profile_selection" != "none" || "$legacy_codex_commands" == "true" ) ]]; then
  run rm -rf "$dest_root/source"
  remove_obsolete_necronomicon_runtime_book
  remove_obsolete_runtime_layers
elif has_obsolete_necronomicon_runtime_book; then
  echo "Found obsolete $install_prefix/necronomicon runtime-book files. Re-run with --force to remove them after preserving any local outputs you still need." >&2
  exit 1
fi

if [[ "$clean_legacy_codex_commands" == "true" ]]; then
  clean_generated_codex_commands
fi

collect_selected_sigils "$sigil_selection"
collect_selected_spells "$spell_selection"
install_repo_local_tools
if profile_enabled "observability"; then
  install_observability_package
fi
if profile_enabled "repo-local"; then
  install_runtime_config
fi
if [[ "$legacy_codex_commands" == "true" ]]; then
  write_necronomicon_harness_state
fi
write_personal_codex_surface
write_repo_codex_surface
write_codex_commands
write_claude_surface
write_copilot_surface
if [[ "$legacy_codex_commands" == "true" ]]; then
  install_hook_support
fi

echo "Arcanum bootstrap complete."
if profile_enabled "observability"; then
  echo "Observability package: $install_prefix/observability/"
fi
if profile_enabled "repo-local"; then
  echo "Repository tool: tools/arcanum"
  echo "Runtime config: $install_prefix/runtime/config.json"
fi
echo "Default runtime adapter: $default_adapter"
echo "Install profiles: $profile_selection"
if profile_enabled "personal-codex"; then
  echo "Personal Codex skills: $codex_home/skills/"
fi
if profile_enabled "repo-codex"; then
  echo "Repository Codex skills: .agents/skills/"
fi
if surface_enabled "codex"; then
  echo "Legacy Codex command surface: .codex/commands/"
  echo "Legacy Codex hooks: .codex/hooks.json"
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
if surface_enabled "claude"; then
  echo "Claude Code skill surface: .claude/skills/"
  echo "Claude Code subagent surface: .claude/agents/arcanum-stage-worker.md"
fi
if surface_enabled "copilot"; then
  echo "GitHub/Copilot skills: .github/skills/"
  echo "Copilot instructions: .github/copilot-instructions.md"
  echo "Copilot path instructions: .github/instructions/arcanum.instructions.md"
fi
