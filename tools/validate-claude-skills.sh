#!/usr/bin/env bash
# Validate generated Claude Code skill packages.
#
# Checks every <root>/<name>/SKILL.md under each given root (default:
# .claude/skills) and fails if a generated package would be invalid or
# silently broken in Claude Code. This is the install-time and CI gate that
# guarantees Arcanum sigils/spells install as valid Claude skills.
#
# Usage:
#   validate-claude-skills.sh [--warn-only] [<skills-root> ...]
#
# Exit: 0 if all packages pass (or --warn-only); 1 if any hard failure.
set -euo pipefail

warn_only="false"
roots=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --warn-only) warn_only="true"; shift ;;
    -h|--help)
      grep '^#' "$0" | sed 's/^# \{0,1\}//'
      exit 0
      ;;
    *) roots+=("$1"); shift ;;
  esac
done
[[ ${#roots[@]} -gt 0 ]] || roots=(".claude/skills")

# Real Claude Code tool identifiers. Anything outside this set in an
# allowed-tools/tools list is a hard failure (e.g. the Codex-flavored
# Task / AskQuestions tokens).
claude_tools=" Read Write Edit Bash Glob Grep Agent AskUserQuestion WebFetch WebSearch NotebookEdit TodoWrite Skill "

failures=0
fail() { printf 'FAIL %s: %s\n' "$1" "$2" >&2; failures=$((failures + 1)); }

# Print the value of a top-level frontmatter scalar key (first match only).
fm_scalar() {
  awk -v key="$1" '
    NR==1 && $0!="---" { exit }
    NR==1 { in_fm=1; next }
    in_fm && $0=="---" { exit }
    in_fm && $0 ~ "^" key ":" {
      sub("^" key ":[[:space:]]*", "")
      gsub(/^"|"$/, "")
      print
      exit
    }
  ' "$2"
}

# Print tokens of an inline OR yaml-list frontmatter key, one per line.
fm_list_tokens() {
  awk -v key="$1" '
    NR==1 && $0!="---" { exit }
    NR==1 { in_fm=1; next }
    in_fm && $0=="---" { exit }
    !in_fm { next }
    collecting && /^[[:space:]]*-[[:space:]]*/ {
      line=$0; sub(/^[[:space:]]*-[[:space:]]*/, "", line)
      gsub(/[[:space:]]/, "", line); if (line!="") print line; next
    }
    collecting && /^[^[:space:]]/ { collecting=0 }
    $0 ~ "^" key ":" {
      rest=$0; sub("^" key ":[[:space:]]*", "", rest)
      if (rest=="") { collecting=1; next }
      n=split(rest, a, /,/)
      for (i=1;i<=n;i++){ gsub(/^[[:space:]]+|[[:space:]]+$/, "", a[i]); if(a[i]!="") print a[i] }
    }
  ' "$2"
}

validate_skill_dir() {
  local dir="$1" skills_root="$2"
  local name_expected file name desc tok
  name_expected="$(basename "$dir")"
  file="$dir/SKILL.md"

  if [[ ! -f "$file" ]]; then
    fail "$dir" "skill directory has no SKILL.md"
    return
  fi
  if [[ "$(head -n 1 "$file")" != "---" ]]; then
    fail "$file" "missing YAML frontmatter (no leading ---)"
    return
  fi
  if [[ "$(tail -n +2 "$file" | grep -c '^---$')" -lt 1 ]]; then
    fail "$file" "frontmatter is not closed (no second ---)"
  fi

  name="$(fm_scalar name "$file")"
  desc="$(fm_scalar description "$file")"

  if [[ -z "$name" ]]; then
    fail "$file" "missing 'name'"
  else
    [[ "$name" == "$name_expected" ]] || fail "$file" "name '$name' != directory '$name_expected'"
    [[ "$name" =~ ^[a-z0-9-]+$ ]] || fail "$file" "name '$name' is not kebab-case [a-z0-9-]"
    [[ "${#name}" -le 64 ]] || fail "$file" "name longer than 64 chars"
  fi

  if [[ -z "$desc" ]]; then
    fail "$file" "missing or empty 'description'"
  elif [[ "${#desc}" -gt 1024 ]]; then
    fail "$file" "description longer than 1024 chars"
  fi

  while IFS= read -r tok; do
    [[ -n "$tok" ]] || continue
    [[ "$claude_tools" == *" $tok "* ]] || fail "$file" "allowed-tools contains non-Claude tool '$tok'"
  done < <(fm_list_tokens allowed-tools "$file")

  while IFS= read -r tok; do
    [[ -n "$tok" ]] || continue
    [[ -f "$skills_root/$tok/SKILL.md" ]] || fail "$file" "skills: entry '$tok' does not resolve to a sibling package"
  done < <(fm_list_tokens skills "$file")
}

validate_agents() {
  local agents_dir="$1" skills_root="$2" f tok
  [[ -d "$agents_dir" ]] || return 0
  for f in "$agents_dir"/*.md; do
    [[ -f "$f" ]] || continue
    while IFS= read -r tok; do
      [[ -n "$tok" ]] || continue
      [[ -f "$skills_root/$tok/SKILL.md" ]] || fail "$f" "skills: entry '$tok' does not resolve to a skill package"
    done < <(fm_list_tokens skills "$f")
    while IFS= read -r tok; do
      [[ -n "$tok" ]] || continue
      [[ "$claude_tools" == *" $tok "* ]] || fail "$f" "tools contains non-Claude tool '$tok'"
    done < <(fm_list_tokens tools "$f")
  done
}

for root in "${roots[@]}"; do
  if [[ ! -d "$root" ]]; then
    fail "$root" "skills root does not exist"
    continue
  fi
  for dir in "$root"/*/; do
    [[ -d "$dir" ]] || continue
    validate_skill_dir "${dir%/}" "$root"
  done
  # Sibling .claude/agents (root is typically .../.claude/skills)
  validate_agents "$(dirname "$root")/agents" "$root"
done

if [[ "$failures" -gt 0 ]]; then
  echo "Claude skill validation: $failures failure(s)." >&2
  if [[ "$warn_only" == "true" ]]; then
    echo "(--warn-only: not failing the run)" >&2
    exit 0
  fi
  exit 1
fi
echo "Claude skill validation: pass (${roots[*]})"
