# Work Pack: Native Skill Package Completeness

Date: 2026-05-31
Owner: Arcanum tools/runtime installer
Status: pass
Invoke mode: plan

## Objective

Make generated native runtime skill packages complete by copying canonical package support assets into generated canonical packages while keeping alias packages thin.

## Source Contracts

- `arcanum/tools/bootstrap_arcanum.sh`
- `ops/development/TASK-SESSION-SURFACE-002.md`
- `docs/decisions/native-runtime-skill-surface.md`
- `docs/decisions/install-profile-contract.md`
- `docs/decisions/surface-cleanup-blocker-decisions.md`

## Implementation Layering

| Layer | Question | Included Scope | Promotion Evidence |
| --- | --- | --- | --- |
| L0 | Can the generator copy support directories for canonical packages without touching aliases? | helper + `write_generated_skill_file` call | staged package has support dirs; alias package stays thin |
| L1 | Can noisy generated evidence be excluded consistently? | exclusion rules for development run evidence | generated staging has no `development/refinement-runs`, `task-sessions`, `runs`, `example-runs`, or `live-evidence` |
| L2 | Can validation prove the package is safe for personal Codex promotion? | staging checks and provenance checks | validation commands pass |
| L3 | Can the personal Codex refresh resume safely? | handoff to `TASK-SURFACE-002` | task-session resumes with complete staging output |

## Task Board

| Task | Status | Goal | Write Scope | Validation |
| --- | --- | --- | --- | --- |
| `TASK-PKG-001` | pass | Add package support copying to generated canonical native skill packages. | `arcanum/tools/bootstrap_arcanum.sh` | `bash -n`, staged `personal-codex` package checks |
| `TASK-PKG-002` | pass | Resume personal Codex refresh after package completeness is proven. | `/mnt/c/Users/vlad_/.codex/skills` via `TASK-SURFACE-002` | active personal skill validation |

## Smallest Working Units

| SWU | Parent | Goal | Write Scope | Done Criteria | Verification |
| --- | --- | --- | --- | --- | --- |
| `SWU-PKG-001` | `TASK-PKG-001` | Add support-directory copy helper and call it for canonical packages only. | `arcanum/tools/bootstrap_arcanum.sh` | helper copies support dirs; aliases stay thin; dry-run/force behavior respected | pass |
| `SWU-PKG-002` | `TASK-PKG-001` | Validate staged `personal-codex` output for package completeness and exclusions. | `/tmp/arcanum-personal-codex-stage-package-completeness*` only | staged canonical packages include support assets; generated run evidence excluded | pass |

## Implementation Detail: `TASK-PKG-001`

Add a helper in `bootstrap_arcanum.sh` near the generated skill writer functions.

Pseudo-flow:

```bash
copy_generated_skill_support() {
  local source_file="$1"
  local package_dir="$2"
  local source_dir
  source_dir="$(dirname "$source_file")"

  for support_dir in templates examples assets scripts development; do
    [[ -d "$source_dir/$support_dir" ]] || continue
    copy support_dir into package_dir with exclusions
  done
}
```

Use `rsync` if available for exclusions; otherwise use a portable `find`/`cp` fallback or repository-standard shell copy approach.

Exclusions:

- `development/runs/**`
- `development/refinement-runs/**`
- `development/task-sessions/**`
- `development/example-runs/**`
- `development/live-evidence/**`

Call this helper only from `write_generated_skill_file` after `SKILL.md` is written.

Do not call it from `write_generated_alias_skill`.

## Validation Strategy

Required commands:

```bash
bash -n arcanum/tools/bootstrap_arcanum.sh
rm -rf /tmp/arcanum-personal-codex-stage-package-completeness
arcanum/tools/bootstrap_arcanum.sh --profile personal-codex --codex-home /tmp/arcanum-personal-codex-stage-package-completeness/.codex --force
test -d /tmp/arcanum-personal-codex-stage-package-completeness/.codex/skills/arcanum-refine/templates
test -d /tmp/arcanum-personal-codex-stage-package-completeness/.codex/skills/arcanum-invoke/templates
test -d /tmp/arcanum-personal-codex-stage-package-completeness/.codex/skills/arcanum-context-builder/templates
test ! -d /tmp/arcanum-personal-codex-stage-package-completeness/.codex/skills/refine/templates
test ! -d /tmp/arcanum-personal-codex-stage-package-completeness/.codex/skills/invoke/templates
find /tmp/arcanum-personal-codex-stage-package-completeness/.codex/skills -path '*/development/refinement-runs/*' -print -quit | wc -l
```

The final count must be `0`.

## Blockers

None.

## Next Route

Proceed to `TASK-SURFACE-003` for root GitHub/Copilot Arcanum package regeneration.
