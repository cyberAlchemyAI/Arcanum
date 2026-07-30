#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: tools/sync-generated-skill-package.sh [options]

Generate one Arcanum skill package in an isolated temporary target, then preview
or apply only that package to an existing consuming repository.

Options:
  --target <path>       Consuming Git repository root. Default: current directory.
  --sigil <id>          Generate and sync one canonical sigil package.
  --spell <id>          Generate and sync one canonical spell package.
  --profiles <list>     repo-codex, claude, or repo-codex,claude.
                        Default: repo-codex.
  --apply               Apply the selective sync. Without this flag, preview only.
  -h, --help            Show this help.

Exactly one of --sigil or --spell is required.

Examples:
  tools/sync-generated-skill-package.sh --target .. --sigil task-session
  tools/sync-generated-skill-package.sh --target .. --spell invoke --apply
  tools/sync-generated-skill-package.sh --target .. --spell ontology-harness \
    --profiles repo-codex,claude --apply
USAGE
}

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
arcanum_root="$(cd "$script_dir/.." && pwd)"
bootstrap="$script_dir/bootstrap_arcanum.sh"
target_root="$PWD"
sigil_id=""
spell_id=""
profiles="repo-codex"
apply="false"
stage_root=""

fail() {
  echo "error: $*" >&2
  exit 1
}

cleanup() {
  if [[ -n "$stage_root" && -d "$stage_root" ]]; then
    rm -rf -- "$stage_root"
  fi
}
trap cleanup EXIT

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target) target_root="$2"; shift 2 ;;
    --sigil) sigil_id="$2"; shift 2 ;;
    --spell) spell_id="$2"; shift 2 ;;
    --profile|--profiles) profiles="$2"; shift 2 ;;
    --apply) apply="true"; shift ;;
    -h|--help) usage; exit 0 ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

[[ -x "$bootstrap" ]] || fail "bootstrap tool is not executable: $bootstrap"
command -v git >/dev/null 2>&1 || fail "git is required"
command -v rsync >/dev/null 2>&1 || fail "rsync is required"
[[ -d "$target_root" ]] || fail "target must be an existing directory: $target_root"
target_root="$(cd "$target_root" && pwd)"

git_root="$(git -C "$target_root" rev-parse --show-toplevel 2>/dev/null)" ||
  fail "target must be a Git repository root: $target_root"
git_root="$(cd "$git_root" && pwd)"
[[ "$target_root" == "$git_root" ]] ||
  fail "target must be the repository root: expected $git_root"

if [[ -n "$sigil_id" && -n "$spell_id" ]] || [[ -z "$sigil_id" && -z "$spell_id" ]]; then
  fail "exactly one of --sigil or --spell is required"
fi

capability_id="${sigil_id:-$spell_id}"
[[ "$capability_id" =~ ^[a-z0-9][a-z0-9-]*$ ]] ||
  fail "capability ID must contain only lowercase letters, digits, and hyphens"
if [[ "$sigil_id" == "structured-interview-kits" ]]; then
  fail "structured-interview-kits is an alias with a two-package closure; sync the canonical interrogation package instead"
fi

normalized_profiles=""
IFS=',' read -ra profile_items <<< "$profiles"
for item in "${profile_items[@]}"; do
  item="${item//[[:space:]]/}"
  case "$item" in
    repo-codex|claude) ;;
    *) fail "unsupported profile '$item'; use repo-codex, claude, or both" ;;
  esac
  if [[ ",$normalized_profiles," != *",$item,"* ]]; then
    normalized_profiles="${normalized_profiles:+$normalized_profiles,}$item"
  fi
done
[[ -n "$normalized_profiles" ]] || fail "at least one profile is required"
profiles="$normalized_profiles"

if [[ -n "$sigil_id" ]]; then
  canonical_source=""
  for tier in formulae transmutations arcana; do
    if [[ -f "$arcanum_root/$tier/$sigil_id/SKILL.md" ]]; then
      canonical_source="$arcanum_root/$tier/$sigil_id/SKILL.md"
      break
    fi
  done
  [[ -n "$canonical_source" ]] || fail "unknown sigil: $sigil_id"
  selection_args=(--sigils "$sigil_id" --spells none)
  capability_kind="sigil"
else
  canonical_source="$arcanum_root/spells/$spell_id/README.md"
  [[ -f "$canonical_source" ]] || fail "unknown spell: $spell_id"
  selection_args=(--sigils "" --spells "$spell_id")
  capability_kind="spell"
fi

stage_root="$(mktemp -d "${TMPDIR:-/tmp}/arcanum-skill-sync.XXXXXX")"
"$bootstrap" \
  --target "$stage_root" \
  "${selection_args[@]}" \
  --profiles "$profiles" \
  --force \
  --no-necronomicon

profile_roots=()
source_dirs=()
destination_dirs=()

preflight_package() {
  local profile="$1"
  local relative_root source_dir destination_dir destination_parent

  case "$profile" in
    repo-codex) relative_root=".agents/skills" ;;
    claude) relative_root=".claude/skills" ;;
    *) fail "internal profile routing error: $profile" ;;
  esac

  source_dir="$stage_root/$relative_root/$capability_id"
  destination_dir="$target_root/$relative_root/$capability_id"
  destination_parent="$(dirname "$destination_dir")"

  if [[ -L "$target_root/${relative_root%%/*}" || -L "$target_root/$relative_root" ]]; then
    fail "refusing a symbolic-link runtime surface: $target_root/$relative_root"
  fi
  [[ ! -L "$destination_dir" ]] ||
    fail "refusing a symbolic-link package destination: $destination_dir"
  [[ ! -e "$destination_dir" || -d "$destination_dir" ]] ||
    fail "package destination exists but is not a directory: $destination_dir"
  [[ -f "$source_dir/SKILL.md" ]] ||
    fail "staged package is missing SKILL.md: $source_dir"
  if find "$source_dir" -type l -print -quit | grep -q .; then
    fail "staged package contains a symbolic link: $source_dir"
  fi

  profile_roots+=("$profile")
  source_dirs+=("$source_dir")
  destination_dirs+=("$destination_dir")
}

show_package() {
  local index="$1"
  local profile="${profile_roots[$index]}"
  local source_dir="${source_dirs[$index]}"
  local destination_dir="${destination_dirs[$index]}"
  local destination_parent
  destination_parent="$(dirname "$destination_dir")"

  echo
  echo "$profile $capability_kind package:"
  echo "  source:      $canonical_source"
  echo "  destination: $destination_dir"
  if [[ "$apply" != "true" && -d "$destination_parent" ]]; then
    rsync -ainc --no-times --omit-dir-times --delete "$source_dir/" "$destination_dir/"
  elif [[ "$apply" != "true" ]]; then
    find "$source_dir" -type f -printf '  would create: %P\n' | sort
  fi
}

IFS=',' read -ra profile_items <<< "$profiles"
for item in "${profile_items[@]}"; do
  preflight_package "$item"
done
for index in "${!profile_roots[@]}"; do
  show_package "$index"
done

echo
if [[ "$apply" == "true" ]]; then
  backup_root="$stage_root/live-backups"
  mkdir -p "$backup_root"
  destination_existed=()
  for index in "${!destination_dirs[@]}"; do
    destination_dir="${destination_dirs[$index]}"
    if [[ -d "$destination_dir" ]]; then
      destination_existed+=("true")
      mkdir -p "$backup_root/$index"
      rsync -a "$destination_dir/" "$backup_root/$index/"
    else
      destination_existed+=("false")
    fi
  done

  apply_failed="false"
  for index in "${!destination_dirs[@]}"; do
    source_dir="${source_dirs[$index]}"
    destination_dir="${destination_dirs[$index]}"
    if ! mkdir -p "$(dirname "$destination_dir")" ||
      ! rsync -a --checksum --no-times --omit-dir-times --delete "$source_dir/" "$destination_dir/" ||
      [[ ! -f "$destination_dir/SKILL.md" ]]; then
      apply_failed="true"
      break
    fi
  done

  if [[ "$apply_failed" == "true" ]]; then
    for index in "${!destination_dirs[@]}"; do
      destination_dir="${destination_dirs[$index]}"
      if [[ "${destination_existed[$index]}" == "true" ]]; then
        mkdir -p "$destination_dir"
        rsync -a --delete "$backup_root/$index/" "$destination_dir/"
      elif [[ -e "$destination_dir" ]]; then
        rm -rf -- "$destination_dir"
      fi
    done
    fail "selective sync failed; previous package bytes were restored"
  fi

  for index in "${!profile_roots[@]}"; do
    echo "  ${profile_roots[$index]} result: applied"
  done
  echo "Selective skill sync complete. No other package directory was targeted."
else
  echo "  result: preview only; re-run with --apply"
  echo "Selective skill sync preview complete. The target was not changed."
fi
