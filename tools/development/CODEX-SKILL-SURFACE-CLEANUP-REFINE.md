---
module: codex-skill-surface-cleanup
version: current
status: refined-seed
updatedAt: 2026-06-01
docType: refine-seed
---

# Refine Seed: Codex Skill Surface Cleanup

## Target

Clean up Arcanum's Codex-facing command and skill surfaces so the user sees one practical suggestion per capability, using short alias names as the visible surface.

## Source Context

- Personal Codex home: `/mnt/c/Users/vlad_/.codex/skills`.
- Repository Codex skills: `.agents/skills`.
- Legacy Codex commands: `.codex/commands`.
- Installer: `tools/bootstrap_arcanum.sh`.
- Deterministic resolver: `tools/arcanum`.
- Current export plan: `tools/development/CODEX-GITHUB-EXPORT-WORK-PACK.md`.

## Current Evidence

Personal Codex skill home currently has 85 skill packages:

- 44 `arcanum-*` prefixed packages.
- 41 short alias packages.

Repository legacy commands currently has 85 command files:

- 42 `arcanum-*` prefixed command files.
- 43 bare command files.

The repository `.agents/skills` surface is already cleaner: it is symlink-based and short-name oriented in this checkout.

## Refined Objective

Make short aliases such as `refine`, `invoke`, `task-session`, `context-builder`, and `workflow-reflect` the visible Codex skill names, while preserving canonical source authority outside the discovery surface.

## Owner Boundaries

- Bootstrap owns generated install profiles and cleanup helpers.
- `tools/arcanum` owns deterministic resolution and legacy compatibility.
- Personal `$CODEX_HOME/skills` cleanup is machine-local state and must be executed only after explicit approval or with a dry-run preview.
- Repository `.codex/commands` cleanup is repo-local generated compatibility state and must remain recoverable through `--legacy-codex-commands`.

## Strategy Preview

Selected overlays:

- `baseline_sequence`: one governed cleanup route with validation gates.
- `memory_residue_for_context_recovery`: this continues the native profile/export cleanup already in progress.
- `route_menu_for_ambiguity`: personal cleanup can be alias-only, canonical-only, or mixed; the selected route is alias-only visible surface.

Subagent strategy: none. This is a local installer/runtime cleanup plan with shell-verifiable outputs.

## Decision

Use an alias-only visible surface:

- generated alias packages should carry the full usable `SKILL.md` content or otherwise be self-sufficient enough for Codex to execute;
- prefixed `arcanum-*` packages should not be installed into discovery roots by default;
- `.codex/commands` should be removable generated legacy state, regenerated only by explicit `--legacy-codex-commands`;
- canonical source remains in this repository under `formulae/`, `transmutations/`, `arcana/`, and `spells/`.

## Done Criteria

- A dry-run cleanup can show exactly which personal and repo files would be removed.
- Fresh `personal-codex` install produces short aliases only, unless an explicit compatibility flag asks for prefixed packages.
- Fresh `repo-codex` install produces short aliases only, unless an explicit compatibility flag asks for prefixed packages.
- `tools/arcanum --resolve refine` still works through `.agents/skills/refine/SKILL.md`.
- Legacy `.codex/commands` are absent after cleanup and reproducible with `--legacy-codex-commands`.
- The cleanup does not remove non-Arcanum skills such as `playwright`.

## Blocked Boundary

Do not delete personal Codex-home packages or repository `.codex/commands` in this step. This artifact only refines the plan.
