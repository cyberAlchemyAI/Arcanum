---
module: codex-skill-surface-cleanup
version: current
status: draft
updatedAt: 2026-06-01
docType: work-pack
---

# Work Pack: Codex Skill Surface Cleanup

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | pass | Planning is execution-ready, but destructive cleanup requires explicit approval. |
| complexity | medium | Touches personal machine state plus repo generated surfaces. |
| outputMode | single-file | Initial cleanup can run as a controlled sequence. |
| executionPackRef | n/a | Not needed for first cleanup slice. |
| layeringArtifactRef | `tools/development/CODEX-SKILL-SURFACE-CLEANUP-IMPLEMENTATION-LAYERING.md` | Layer model. |
| activeLayerWindow | L0-L1 | Classification and alias-only install behavior. |
| lastUpdatedAt | 2026-06-01 | Initial invoke plan. |
| readinessProfile | pilot | Dry-run first, then explicit approved cleanup. |
| latestDryRunRef | `tools/development/CODEX-SKILL-SURFACE-CLEANUP-DRY-RUN-20260601T115842Z.md` | Refreshed after user selected decision option 2. |
| latestCleanupRef | `tools/development/CODEX-SKILL-SURFACE-CLEANUP-POST-CLEANUP-20260601T120907Z.md` | Generated duplicate cleanup completed after user selected option 1. |

## Objective Summary

- Objective: remove duplicate Arcanum command/skill suggestions and make short aliases the default visible Codex surface.
- Primary inputs: current personal skill inventory, repo `.agents/skills`, repo `.codex/commands`, bootstrap profiles.
- Success condition: only short Arcanum aliases appear in Codex discovery surfaces by default, with legacy commands and prefixed packages available only through explicit compatibility options.

## Selected Surface Policy

| Surface | Keep By Default | Remove/Clean By Default | Regeneration Path |
| --- | --- | --- | --- |
| Personal Codex `$CODEX_HOME/skills` | short aliases: `refine`, `invoke`, `task-session`, etc. | generated `arcanum-*` packages that duplicate aliases | `tools/bootstrap_arcanum.sh --profile personal-codex --codex-home ...` after alias-only generator update |
| Repo Codex `.agents/skills` | short aliases only | generated `arcanum-*` packages in discovery root | `--profile repo-codex` after alias-only generator update |
| Repo legacy `.codex/commands` | none for normal use | all generated Arcanum command files | `--legacy-codex-commands` |
| Canonical source | `formulae/`, `transmutations/`, `arcana/`, `spells/` | nothing | normal repo source control |
| Non-Arcanum personal skills | keep, for example `playwright` | none | not owned by this work-pack |

## Delivery Slices

| Slice ID | Outcome | Layer | Dependencies | Validation |
| --- | --- | --- | --- | --- |
| S-001 | Dry-run cleanup inventory reports personal and repo duplicate sets. | L0 | none | pass: `tools/development/CODEX-SKILL-SURFACE-CLEANUP-DRY-RUN.md` |
| S-002 | Alias-only generation writes self-sufficient short skill packages. | L1 | S-001 | pass: staged personal/repo install has no `arcanum-*` discovery packages |
| S-003 | Legacy command cleanup removes generated `.codex/commands` safely. | L2 | S-001 | pass: staged cleanup removes generated commands and explicit legacy reinstall restores them |
| S-004 | Approved personal cleanup removes duplicate prefixed packages. | L3 | S-002, user approval | pass: `$CODEX_HOME/skills` keeps short aliases and non-Arcanum skills; remove candidates are zero |

## Task Status Board

| Task ID | Goal | Layer | Complexity | Source | Gate Status | Status |
| --- | --- | --- | --- | --- | --- | --- |
| TASK-CLEAN-001 | Add cleanup inventory/dry-run support. | L0 | medium | `tools/arcanum-skill-surface-cleanup-report` | ready | completed |
| TASK-CLEAN-002 | Change generated Codex skill installs to alias-only visible packages. | L1 | medium | `tools/bootstrap_arcanum.sh` | ready-after-TASK-CLEAN-001 | completed |
| TASK-CLEAN-003 | Add repo legacy command cleanup path. | L2 | medium | `tools/bootstrap_arcanum.sh`, `.codex/commands` | ready-after-TASK-CLEAN-001 | completed |
| TASK-CLEAN-004 | Execute approved personal/repo cleanup. | L3 | medium | `/mnt/c/Users/vlad_/.codex/skills`, `.codex/commands`, `.agents/skills` | approved-option-1 | completed |
| TASK-CLEAN-VERIFY | Validate no duplicate Arcanum suggestions remain. | L3 | low | generated inventory reports | ready-after-cleanup | completed |

## SWU Execution Handoff

| SWU ID | Parent Task | Source Anchors | Dependencies | Write Scope | Done Criteria | Acceptance Evidence | Validation Surface | Execution Owner | Handoff Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-CLEAN-001 | TASK-CLEAN-001 | current `find` inventory commands; generated provenance frontmatter | none | `tools/development/` plus optional helper under `tools/` | dry-run report classifies keep/remove/unknown paths | report shows personal and legacy command keep/remove/unknown sets, and keeps `playwright` | `tools/arcanum-skill-surface-cleanup-report` exits zero | local-fallback | completed |
| SWU-CLEAN-002 | TASK-CLEAN-002 | `write_runtime_skill_packages`, `write_generated_skill_file`, `write_generated_alias_skill` | SWU-CLEAN-001 | `tools/bootstrap_arcanum.sh` | alias packages are self-sufficient and no prefixed packages are installed by default | staged installs contain `refine/SKILL.md`, not `arcanum-refine`; compatibility flag restores prefixed packages | `/tmp` staged `personal-codex`, `repo-codex`, and `--prefixed-skill-packages` installs | local-fallback | completed |
| SWU-CLEAN-003 | TASK-CLEAN-003 | `write_codex_commands`, `--legacy-codex-commands` | SWU-CLEAN-001 | `tools/bootstrap_arcanum.sh`, `.codex/commands` generated output | cleanup removes generated commands while preserving regeneration | staged cleanup removed generated commands, preserved unknown local command, and legacy reinstall restored `refine.md` | staged repo cleanup and reinstall smoke | local-fallback | completed |
| SWU-CLEAN-004 | TASK-CLEAN-004 | approved dry-run report | SWU-CLEAN-002, SWU-CLEAN-003, explicit user approval | `/mnt/c/Users/vlad_/.codex/skills`, repo generated surfaces | duplicate prefixed packages removed; aliases remain | post-cleanup report shows remove candidates are zero; backup manifest records moved files | shell inventory comparison | manual | completed |

## Latest SWU-CLEAN-004 Decision Refresh

- User selected decision option 2: rerun dry-run before live cleanup.
- Refreshed report: `tools/development/CODEX-SKILL-SURFACE-CLEANUP-DRY-RUN-20260601T115842Z.md`.
- Result: counts match the earlier dry-run.
- Current candidates:
  - Personal Codex skills: keep 44, remove candidates 40, unknown 1.
  - Repository Codex skills: keep 0, remove candidates 0, unknown 0.
  - Legacy Codex commands: keep 0, remove candidates 84, unknown 1.
- Gate: still blocked before live cleanup. The refreshed evidence supports a final choice between backed-up full cleanup, repository-only legacy command cleanup, or deferral.

## SWU-CLEAN-004 Cleanup Result

- User selected final option 1 through `invoke refresh 1`.
- Personal duplicate generated packages moved to `/mnt/c/Users/vlad_/.codex/skills/.cleanup-backups/20260601T120907Z/personal-skills/`.
- Generated legacy command files moved to `tools/development/cleanup-backups/20260601T120907Z/codex-commands/`.
- Manifest: `tools/development/cleanup-backups/20260601T120907Z/manifest.txt`.
- Unknown entries preserved:
  - `/mnt/c/Users/vlad_/.codex/skills/arcanum-orchestrate/SKILL.md`
  - `.codex/commands/arcanum-runtime-smoke.md`
- Post-cleanup report: `tools/development/CODEX-SKILL-SURFACE-CLEANUP-POST-CLEANUP-20260601T120907Z.md`.
- Post-cleanup counts:
  - Personal Codex skills: keep 44, remove candidates 0, unknown 1.
  - Repository Codex skills: keep 0, remove candidates 0, unknown 0.
  - Legacy Codex commands: keep 0, remove candidates 0, unknown 1.

## Implementation Detail

### Alias-only Generation

Current generated alias packages are thin and point at canonical `arcanum-*` packages. That creates duplicate suggestions because both package names live in discovery roots.

Change the model:

1. For Codex discovery roots, write the full generated package to the short alias path.
2. Do not write `arcanum-*` packages by default.
3. Add an explicit compatibility flag such as `--prefixed-skill-packages` only if prefixed packages are still needed.
4. Preserve provenance frontmatter with `canonical_source` and `mutation_policy`.
5. Keep alias names as the visible surface:
   - `refine`
   - `invoke`
   - `task-session`
   - `context-builder`
   - `distill`
   - `interrogation`
   - etc.

### Cleanup Classification

Classify generated packages by frontmatter:

- `surface_kind: generated-native-runtime-package`
- `generated_by: tools/bootstrap_arcanum.sh --profile`
- `canonical_source:` under Arcanum source folders

Safe remove candidates:

- personal `arcanum-*` packages with generated provenance and a matching short alias package;
- repo `.agents/skills/arcanum-*` packages with generated provenance and a matching short alias package;
- repo `.codex/commands/*.md` generated by legacy Arcanum command install.

Keep candidates:

- short alias packages;
- non-Arcanum skills such as `playwright`;
- canonical repo source;
- generated reports until the user chooses cleanup.

Unknown candidates:

- any package without generated provenance;
- any package whose short alias is missing;
- any hand-authored local skill.

### Personal Cleanup Gate

Before touching `/mnt/c/Users/vlad_/.codex/skills`, produce a dry-run report and ask for approval. The approved cleanup should move removed packages to a timestamped backup directory first, not hard-delete them immediately.

Suggested backup:

```text
/mnt/c/Users/vlad_/.codex/skills/.cleanup-backups/<timestamp>/
```

## Validation Strategy

Dry-run validation:

```bash
find /mnt/c/Users/vlad_/.codex/skills -maxdepth 2 -name SKILL.md -print
find .agents/skills -maxdepth 2 -name SKILL.md -print
find .codex/commands -maxdepth 1 -type f -name '*.md' -print
```

Staged alias-only install validation:

```bash
rm -rf /tmp/arcanum-alias-only-personal /tmp/arcanum-alias-only-repo
bash tools/bootstrap_arcanum.sh --profile personal-codex --codex-home /tmp/arcanum-alias-only-personal/.codex --sigils refine,invoke-example-runner --spells invoke --force
test -f /tmp/arcanum-alias-only-personal/.codex/skills/refine/SKILL.md
test ! -e /tmp/arcanum-alias-only-personal/.codex/skills/arcanum-refine
bash tools/bootstrap_arcanum.sh --target /tmp/arcanum-alias-only-repo --profile repo-codex,repo-local --sigils refine,context-builder --spells none --force
test -f /tmp/arcanum-alias-only-repo/.agents/skills/refine/SKILL.md
test ! -e /tmp/arcanum-alias-only-repo/.agents/skills/arcanum-refine
/tmp/arcanum-alias-only-repo/tools/arcanum --resolve refine
```

Legacy regeneration validation:

```bash
rm -rf /tmp/arcanum-legacy-proof
bash tools/bootstrap_arcanum.sh --target /tmp/arcanum-legacy-proof --profile repo-local --sigils refine --spells none --force
test ! -d /tmp/arcanum-legacy-proof/.codex/commands
bash tools/bootstrap_arcanum.sh --target /tmp/arcanum-legacy-proof --profile repo-local --legacy-codex-commands --sigils refine --spells none --force
test -f /tmp/arcanum-legacy-proof/.codex/commands/refine.md
bash tools/bootstrap_arcanum.sh --target /tmp/arcanum-legacy-proof --profile none --clean-legacy-codex-commands --sigils refine --spells none
test ! -d /tmp/arcanum-legacy-proof/.codex/commands
bash tools/bootstrap_arcanum.sh --target /tmp/arcanum-legacy-proof --profile repo-local --legacy-codex-commands --sigils refine --spells none --force
test -f /tmp/arcanum-legacy-proof/.codex/commands/refine.md
```

## Blockers

| Blocker ID | Scope | Description | Owner | Next Action |
| --- | --- | --- | --- | --- |
| B-CLEAN-001 | personal cleanup | Removing `/mnt/c/Users/vlad_/.codex/skills/arcanum-*` changes machine-global Codex suggestions. | user | Approve after dry-run report. |
| B-CLEAN-002 | alias-only install | Existing alias packages are thin, so alias-only install must first make aliases self-sufficient. | implementation | Complete SWU-CLEAN-002 before cleanup. |
| B-CLEAN-003 | unknown entries | `arcanum-orchestrate` and `arcanum-runtime-smoke.md` require manual policy before cleanup. | implementation | Decide whether to keep, alias, or mark generated before cleanup execution. |

## Recommended Next Route

`SWU-CLEAN-001` through `SWU-CLEAN-004` are complete. Remaining optional follow-up is policy cleanup for the two preserved unknown entries.
