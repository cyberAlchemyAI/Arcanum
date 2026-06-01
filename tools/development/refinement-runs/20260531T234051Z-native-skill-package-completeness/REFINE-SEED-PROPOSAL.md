# Refine Seed Proposal: Native Skill Package Completeness

Date: 2026-05-31
Preset: compact
Research: no-research
Target: `arcanum/tools/bootstrap_arcanum.sh` native runtime package generation

## Objective

Repair the `personal-codex` staging blocker by making generated native skill packages complete enough to use without relying on stale package-local assets from older personal installs.

## Source Context

- `ops/development/TASK-SESSION-SURFACE-002.md`
- `ops/ARCANUM-SURFACE-MAP-AND-PLAN.md`
- `docs/decisions/personal-codex-skill-refresh.md`
- `docs/decisions/surface-cleanup-blocker-decisions.md`
- `docs/decisions/native-runtime-skill-surface.md`
- `docs/decisions/install-profile-contract.md`
- `arcanum/tools/bootstrap_arcanum.sh`

## Refined Problem

The generated native package currently writes only `SKILL.md`.

That proves provenance, but it is not package-complete for skills that reference package-local support folders such as:

- `templates/`
- `examples/`
- `assets/`
- `scripts/`
- curated `development/` references

Directly replacing active personal Codex package directories with `SKILL.md`-only output could remove useful runtime support assets. Promoting only `SKILL.md` files could preserve old stale support folders.

## Design Direction

The generator should produce complete native packages from canonical source:

1. Write generated `SKILL.md` with provenance.
2. Copy canonical support directories into canonical generated packages.
3. Keep alias packages thin and support-free.
4. Exclude generated/noisy run evidence from copied `development/`.
5. Validate package completeness before personal Codex promotion.

## Write Scope For Next Task

- `arcanum/tools/bootstrap_arcanum.sh`
- `arcanum/tools/development/*` evidence for this fix
- generated staging directories under `/tmp` during validation

No mutation to `/mnt/c/Users/vlad_/.codex/skills` belongs to this fix task itself. Personal Codex promotion resumes only after this generator fix passes.

## Done Criteria

- Generated canonical packages include support directories when the canonical source has them.
- Alias packages remain thin and include `alias_of`.
- Generated packages exclude noisy generated run evidence by default.
- Staged `personal-codex` output proves `arcanum-refine`, `arcanum-invoke`, `arcanum-context-builder`, `arcanum-distill`, and `arcanum-experiment-harness` have required package support where applicable.
- Existing syntax checks still pass.

## Research Decision

No external research. The source contract and blocker evidence are local.
