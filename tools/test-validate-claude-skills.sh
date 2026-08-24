#!/usr/bin/env bash
# Regression checks for the Claude skill package/container boundary.
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
fixture_root="$(mktemp -d)"
trap 'rm -rf -- "$fixture_root"' EXIT

skills_root="$fixture_root/.claude/skills"
mkdir -p "$skills_root/valid-skill" "$skills_root/custom"

printf '%s\n' \
  '---' \
  'name: valid-skill' \
  'description: A valid fixture skill.' \
  '---' \
  '# Valid fixture' > "$skills_root/valid-skill/SKILL.md"
printf '%s\n' '# Repository-owned writing guide' > "$skills_root/custom/writing-guide.md"

bash "$script_dir/validate-claude-skills.sh" "$skills_root" >/dev/null

mkdir -p "$skills_root/unexpected"
printf '%s\n' '# Not a skill package' > "$skills_root/unexpected/notes.md"
if bash "$script_dir/validate-claude-skills.sh" "$skills_root" >"$fixture_root/unexpected.out" 2>&1; then
  echo "FAIL unexpected directory without SKILL.md was accepted" >&2
  exit 1
fi
grep -Fq "skill directory has no SKILL.md" "$fixture_root/unexpected.out"
rm -rf -- "$skills_root/unexpected"

printf '%s\n' 'not a Markdown guide' > "$skills_root/custom/not-a-guide.txt"
if bash "$script_dir/validate-claude-skills.sh" "$skills_root" >"$fixture_root/custom.out" 2>&1; then
  echo "FAIL malformed custom container was accepted" >&2
  exit 1
fi
grep -Fq "custom guide container accepts only regular Markdown files" "$fixture_root/custom.out"

echo "Claude skill validator regression: pass"
