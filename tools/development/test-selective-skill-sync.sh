#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
tools_dir="$(cd "$script_dir/.." && pwd)"
bootstrap="$tools_dir/bootstrap_arcanum.sh"
sync_tool="$tools_dir/sync-generated-skill-package.sh"
test_root=""

cleanup() {
  if [[ -n "$test_root" && -d "$test_root" ]]; then
    rm -rf -- "$test_root"
  fi
}
trap cleanup EXIT

fail() {
  echo "FAIL: $*" >&2
  exit 1
}

test_root="$(mktemp -d "${TMPDIR:-/tmp}/arcanum-selective-sync-test.XXXXXX")"
target="$test_root/consumer"
mkdir -p "$target/.agents/skills/sentinel"
git init -q "$target"
printf '%s\n' "sentinel package" > "$target/.agents/skills/sentinel/SKILL.md"
sentinel_before="$(sha256sum "$target/.agents/skills/sentinel/SKILL.md")"

if "$bootstrap" \
  --target "$target" \
  --sigils task-session \
  --spells none \
  --profile repo-codex \
  --force \
  --no-necronomicon >"$test_root/direct.out" 2>"$test_root/direct.err"; then
  fail "partial --force bootstrap unexpectedly succeeded"
fi
grep -q "Refusing a partial --force repo-codex install" "$test_root/direct.err" ||
  fail "partial --force bootstrap did not return the expected guard message"
[[ "$(sha256sum "$target/.agents/skills/sentinel/SKILL.md")" == "$sentinel_before" ]] ||
  fail "partial --force bootstrap changed the sentinel package"

if "$bootstrap" \
  --target "$target" \
  --sigils not-a-real-sigil \
  --spells none \
  --profile repo-codex \
  --force \
  --no-necronomicon >"$test_root/unknown.out" 2>"$test_root/unknown.err"; then
  fail "unknown sigil unexpectedly succeeded"
fi
grep -q "Unknown sigil" "$test_root/unknown.err" ||
  fail "unknown sigil did not return the expected error"
[[ "$(sha256sum "$target/.agents/skills/sentinel/SKILL.md")" == "$sentinel_before" ]] ||
  fail "unknown sigil cleanup changed the sentinel package"

"$sync_tool" \
  --target "$target" \
  --spell work-pack-readiness-audit >"$test_root/preview.out"
grep -q "preview only" "$test_root/preview.out" ||
  fail "selective sync preview did not report preview mode"
[[ ! -e "$target/.agents/skills/work-pack-readiness-audit" ]] ||
  fail "selective sync preview mutated the target"
[[ "$(sha256sum "$target/.agents/skills/sentinel/SKILL.md")" == "$sentinel_before" ]] ||
  fail "selective sync preview changed the sentinel package"

"$sync_tool" \
  --target "$target" \
  --spell work-pack-readiness-audit \
  --apply >"$test_root/apply.out"
[[ -f "$target/.agents/skills/work-pack-readiness-audit/SKILL.md" ]] ||
  fail "selective sync did not install the selected package"
[[ "$(sha256sum "$target/.agents/skills/sentinel/SKILL.md")" == "$sentinel_before" ]] ||
  fail "selective sync changed the sentinel package"
[[ "$(find "$target/.agents/skills" -mindepth 1 -maxdepth 1 -type d | wc -l)" -eq 2 ]] ||
  fail "selective sync created or removed an unexpected package"

"$sync_tool" \
  --target "$target" \
  --spell work-pack-readiness-audit \
  --profiles repo-codex,claude \
  --apply >"$test_root/both-profiles.out"
[[ -f "$target/.claude/skills/work-pack-readiness-audit/SKILL.md" ]] ||
  fail "two-profile sync did not install the selected Claude package"
[[ ! -e "$target/.claude/skills/orchestrate" ]] ||
  fail "two-profile sync copied an unselected staged package"
[[ "$(sha256sum "$target/.agents/skills/sentinel/SKILL.md")" == "$sentinel_before" ]] ||
  fail "two-profile sync changed the sentinel package"

alias_target="$test_root/alias-consumer"
mkdir -p "$alias_target"
git init -q "$alias_target"
if "$sync_tool" \
  --target "$alias_target" \
  --sigil structured-interview-kits >"$test_root/alias.out" 2>"$test_root/alias.err"; then
  fail "multi-package alias unexpectedly succeeded"
fi
grep -q "two-package closure" "$test_root/alias.err" ||
  fail "multi-package alias did not return the expected error"

symlink_target="$test_root/symlink-consumer"
linked_surface="$test_root/linked-skills"
mkdir -p "$symlink_target/.agents" "$linked_surface/sentinel"
git init -q "$symlink_target"
printf '%s\n' "linked sentinel" > "$linked_surface/sentinel/SKILL.md"
ln -s "$linked_surface" "$symlink_target/.agents/skills"
if "$bootstrap" \
  --target "$symlink_target" \
  --sigils task-session \
  --spells none \
  --profile repo-codex \
  --force \
  --no-necronomicon >"$test_root/symlink.out" 2>"$test_root/symlink.err"; then
  fail "symbolic-link skill surface unexpectedly succeeded"
fi
grep -q "symbolic-link skill surface" "$test_root/symlink.err" ||
  fail "symbolic-link skill surface did not return the expected error"
[[ -f "$linked_surface/sentinel/SKILL.md" ]] ||
  fail "symbolic-link skill surface changed its target"

echo "PASS: partial bootstrap is fail-closed and selective sync preserves unrelated packages"
