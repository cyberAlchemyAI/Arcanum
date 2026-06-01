# Refined Synthesis: Native Skill Package Completeness

Date: 2026-05-31
Status: pass

## Smallest Coherent Fix

The fix belongs in `arcanum/tools/bootstrap_arcanum.sh`, in the native skill package writer.

Current behavior:

- `write_generated_skill_file` writes only `SKILL.md`.
- `write_generated_alias_skill` correctly writes thin aliases.

Target behavior:

- Canonical generated packages copy runtime-useful support directories from the canonical capability folder.
- Alias packages remain thin and do not copy support directories.
- Generated/noisy evidence is excluded from copied `development/` trees.

## Implementation Shape

Add a helper around generated canonical package creation:

```text
copy_generated_skill_support(source_file, package_dir)
```

The helper should:

1. Resolve `source_dir="$(dirname "$source_file")"`.
2. Copy support directories when present:
   - `templates`
   - `examples`
   - `assets`
   - `scripts`
   - `development`
3. Exclude generated/noisy development paths:
   - `development/runs`
   - `development/refinement-runs`
   - `development/task-sessions`
   - `development/example-runs`
   - `development/live-evidence`
4. Preserve file modes where practical.
5. Respect `--dry-run`.
6. Respect `--force` through the existing destination cleanup behavior.

`write_generated_skill_file` should call this helper after writing `SKILL.md`.

`write_generated_alias_skill` should not call it.

## Validation Surface

After implementation:

```bash
bash -n arcanum/tools/bootstrap_arcanum.sh
rm -rf /tmp/arcanum-personal-codex-stage-package-completeness
arcanum/tools/bootstrap_arcanum.sh --profile personal-codex --codex-home /tmp/arcanum-personal-codex-stage-package-completeness/.codex --force
test -d /tmp/arcanum-personal-codex-stage-package-completeness/.codex/skills/arcanum-refine/templates
test -d /tmp/arcanum-personal-codex-stage-package-completeness/.codex/skills/arcanum-invoke/templates
test -d /tmp/arcanum-personal-codex-stage-package-completeness/.codex/skills/arcanum-context-builder/templates
test ! -d /tmp/arcanum-personal-codex-stage-package-completeness/.codex/skills/refine/templates
find /tmp/arcanum-personal-codex-stage-package-completeness/.codex/skills -path '*/development/refinement-runs/*' -print -quit | test "$(wc -l)" -eq 0
```

## Recommended Next Route

`task-session` for `TASK-PKG-001 / SWU-PKG-001`, then resume `TASK-SURFACE-002`.
