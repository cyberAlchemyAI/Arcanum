---
module: skill-surface-dispatch-canonicalization
version: current
status: live-refresh-complete
updatedAt: 2026-06-05
docType: work-pack
---

# Work Pack: Skill Surface Dispatch Canonicalization

## Invoke Plan Result

- Mode: `plan`
- Spell: `invoke`
- Canonical ID: `invoke`
- Scope: library
- Phase status: `pass`
- Mode contract: `spells/invoke/plan.md`
- Outputs: this work-pack and `formulae/dispatch-spec/development/SKILL-SURFACE-DISPATCH-CANONICALIZATION-IMPLEMENTATION-LAYERING.md`
- Design views: reused prior orchestration runtime architecture and surface cleanup artifacts
- Glossary consistency: n/a
- Implementation layering: `formulae/dispatch-spec/development/SKILL-SURFACE-DISPATCH-CANONICALIZATION-IMPLEMENTATION-LAYERING.md`
- Work-pack: split-ready single-file coordinator
- Complexity: medium
- Per-layer planning: L0, L1, L2, L3
- Implementation detail: inline task specs complete
- Smallest working units: complete
- Refresh: n/a
- Target artifact: Arcanum skill/runtime surface and dispatch-spec canonical package
- Template or recipe selection: standalone `implementation-layering` plus standalone `work-pack`
- Decisions: use canonical `formulae/dispatch-spec/` as source of truth; remove command-surface invocation requirements from active skills; fix installed dependency resolution by generator/staged install before live refresh
- Unresolved gaps: live personal package mutation requires explicit execution approval; unknown preserved local packages keep separate policy
- Next route: `task-session`

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | pass | Ready for bounded execution through Task Session, one SWU at a time. |
| complexity | medium | Crosses source contracts, generator output, and live install surfaces. |
| outputMode | single-file | Split files can be added if execution expands. |
| executionPackRef | n/a | Current scope is ordered and narrow enough for this coordinator file. |
| layeringArtifactRef | `formulae/dispatch-spec/development/SKILL-SURFACE-DISPATCH-CANONICALIZATION-IMPLEMENTATION-LAYERING.md` | Layer model. |
| activeLayerWindow | L3-verify | Live refresh completed; final report-only audit is ready. |
| lastUpdatedAt | 2026-06-05 | `SWU-DISP-SURF-005` completed approved live Codex skill refresh. |
| readinessProfile | pilot | Source and staged install proof before live refresh. |

## Objective Summary

- Objective: eliminate active skill-contract dependence on command surfaces, make dispatch-spec canonical for route validation, and fix installed-package dependency gaps such as missing `.agents/formulae/dispatch-spec/dispatch.schema.yml` and `TECHNIQUE-CATALOG.md`.
- Primary inputs: `arcana/refine/SKILL.md`, `formulae/dispatch-spec/`, `tools/bootstrap_arcanum.sh`, prior codex-exec surface inventory, and current installed alias behavior.
- Success condition: active skills route through native skill/capability handles plus dispatch-spec validation and receipts; staged and live generated installs can validate dispatch-spec without missing dependency paths.

## Current Evidence

| Evidence | Status | Implication |
| --- | --- | --- |
| `formulae/dispatch-spec/dispatch.schema.yml` exists | pass | canonical schema source is present. |
| `formulae/dispatch-spec/TECHNIQUE-CATALOG.md` exists | pass | canonical technique catalog is present. |
| installed `refine` reported missing `.agents/formulae/dispatch-spec/*` | flag | generated/runtime dependency path is wrong or incomplete. |
| `arcana/refine/SKILL.md` still names command resolution and `tools/arcanum --exec` in stage execution policy | flag | active skill contract still carries command-surface invocation language. |
| `formulae/dispatch-spec/development/CODEX-EXEC-SURFACE-INVENTORY.md` classifies prior codex-exec surfaces | pass | reuse existing inventory rather than reclassifying from scratch. |
| `tools/development/CODEX-SKILL-SURFACE-CLEANUP-WORK-PACK.md` completed duplicate cleanup | pass | do not reopen alias duplication; this plan focuses on self-sufficiency and dependency resolution. |

## Delivery Slices

| Slice ID | Outcome | Layer | Dependencies | Validation |
| --- | --- | --- | --- | --- |
| S-001 | Installed failure is reproduced and traced to source/generator path assumptions. | L0 | none | pass: `formulae/dispatch-spec/development/SKILL-SURFACE-DISPATCH-CANONICALIZATION-L0-RESULT.md` maps the failure to stale thin live aliases pointing at absent `arcanum-*` packages. |
| S-002 | Active skill contracts no longer invoke command surfaces for stage execution. | L1 | S-001 | pass: `formulae/dispatch-spec/development/SKILL-SURFACE-DISPATCH-CANONICALIZATION-SWU-002-RESULT.md` classifies remaining hits as deterministic handoff metadata, legacy installer ownership, compatibility validation, or bootstrap adapter documentation. |
| S-003 | Dispatch-spec generated package is canonical or self-sufficient. | L2 | S-001 | pass: `formulae/dispatch-spec/development/SKILL-SURFACE-DISPATCH-CANONICALIZATION-SWU-004-RESULT.md` proves staged personal and repo installs validate `pass-refine-dispatch.json` with generated package guidance. |
| S-004 | Live installed surfaces are refreshed after staged proof and approval. | L3 | S-002, S-003, explicit approval | pass: `formulae/dispatch-spec/development/SKILL-SURFACE-DISPATCH-CANONICALIZATION-SWU-005-RESULT.md` proves backed-up live refresh and installed dispatch-spec validation. |

## Task Status Board

| Task ID | Goal | Layer | Complexity | Source | Gate Status | Status |
| --- | --- | --- | --- | --- | --- | --- |
| TASK-DISP-SURF-001 | Reproduce and classify dispatch-spec installed dependency gap. | L0 | low | `formulae/dispatch-spec/`, installed `$CODEX_HOME/skills`, repo `.agents` | pass | completed |
| TASK-DISP-SURF-002 | Rewrite active skill contracts away from command-surface invocation. | L1 | medium | `arcana/refine/SKILL.md`, active orchestration `SKILL.md` files | pass | completed |
| TASK-DISP-SURF-003 | Fix generated dispatch-spec package dependency resolution. | L2 | medium | `tools/bootstrap_arcanum.sh`, generated package templates | pass | completed |
| TASK-DISP-SURF-004 | Validate staged installs and dispatch fixtures. | L2 | medium | `/tmp` staged installs, dispatch-spec fixture runner | pass | completed |
| TASK-DISP-SURF-005 | Refresh live installed Codex packages after approval. | L3 | medium | `/mnt/c/Users/vlad_/.codex/skills`, repo `.agents/skills` | pass | completed |
| TASK-DISP-SURF-VERIFY | Verify no active skill command-surface invocations remain. | L3 | low | repository grep and installed smoke | ready | not-started |

## Implementation Detail

### TASK-DISP-SURF-001: Reproduce And Classify Dependency Gap

- Owner route: `task-session`
- Write scope:
  - `formulae/dispatch-spec/development/`
  - read-only inspection of `/mnt/c/Users/vlad_/.codex/skills`
  - read-only inspection of `.agents/skills` when present
- Steps:
  1. Inspect installed `refine`, `invoke`, and `dispatch-spec` packages.
  2. Search generated packages for `.agents/formulae/dispatch-spec`, `dispatch.schema.yml`, and `TECHNIQUE-CATALOG.md`.
  3. Confirm whether the package expects copied dependencies or should resolve to repo canonical paths.
  4. Record one recommended fix: self-sufficient package, canonical path resolver, or profile-installed formulae package.
- Validation:
  - `rg -n "\\.agents/formulae|dispatch\\.schema\\.yml|TECHNIQUE-CATALOG" /mnt/c/Users/vlad_/.codex/skills .agents tools formulae arcana spells`
  - `test -f formulae/dispatch-spec/dispatch.schema.yml`
  - `test -f formulae/dispatch-spec/TECHNIQUE-CATALOG.md`

### TASK-DISP-SURF-002: Remove Command-Surface Invocation From Active Skills

- Owner route: `task-session`
- Write scope:
  - `arcana/refine/SKILL.md`
  - active `arcana/*/SKILL.md`, `spells/*/README.md`, and generated package source text only when they require command-surface invocation
  - exclude historical `development/refinement-runs/` evidence unless a current contract imports it
- Implementation rule:
  - Replace "command", "command file", and `tools/arcanum --exec` stage requirements with "capability handle", "native skill/subagent receipt", "dispatch step", and deterministic validator language.
  - Keep `tools/arcanum` references only when they are deterministic local validation, adapter metadata, or explicit legacy compatibility.
  - Keep `sigil-runtime-installer` language about `.codex/commands/` because that sigil explicitly owns legacy adapter installation, but clarify that it is not the default skill execution route if needed.
- Validation:
  - `rg -n "tools/arcanum --exec|\\.codex/commands|command-backed|command file|resolved command|command used" arcana spells transmutations formulae --glob 'SKILL.md' --glob 'README.md'`
  - Remaining active hits are classified as `deterministic-validator`, `legacy-installer`, `migration-note`, or `historical-preserved`.

### TASK-DISP-SURF-003: Fix Dispatch-Spec Generated Package Shape

- Owner route: `task-session`
- Write scope:
  - `tools/bootstrap_arcanum.sh`
  - generated package helper logic
  - optional package metadata for `dispatch-spec`
- Implementation rule:
  - Treat `dispatch-spec` as a canonical Formulae package, not a thin alias that assumes hidden `.agents/formulae` dependencies.
  - Generated `dispatch-spec/SKILL.md` must either include enough deterministic validation instructions to find canonical repo files or install/copy the minimal package assets it directly requires.
  - Minimal self-sufficient assets, if copied, are limited to `SKILL.md`, `README.md`, `dispatch.schema.yml`, `TECHNIQUE-CATALOG.md`, and `scripts/validate-dispatch.py`; do not copy unrelated Arcanum internals.
  - The package must state `canonical_source: formulae/dispatch-spec/SKILL.md` and `mutation_policy: regenerate-from-canonical-source`.
- Validation:
  - staged install contains a usable `dispatch-spec` package.
  - staged install does not require `.codex/commands`.
  - generated metadata points back to canonical `formulae/dispatch-spec/`.

### TASK-DISP-SURF-004: Staged Install And Fixture Validation

- Owner route: `task-session`
- Write scope:
  - `/tmp/arcanum-dispatch-surface-*`
  - validation report under `formulae/dispatch-spec/development/`
- Steps:
  1. Generate a personal Codex staged install.
  2. Generate a repo Codex staged install.
  3. Verify `dispatch-spec` package assets or canonical resolver guidance.
  4. Run dispatch fixture validation from the repo canonical package.
  5. If generated package includes a local validator script, run it against `formulae/dispatch-spec/development/fixtures/pass-refine-dispatch.json` from the staged context.
- Validation:
  - `bash tools/bootstrap_arcanum.sh --profile personal-codex --codex-home /tmp/arcanum-dispatch-surface-personal/.codex --sigils dispatch-spec,refine --spells invoke --force`
  - `bash tools/bootstrap_arcanum.sh --target /tmp/arcanum-dispatch-surface-repo --profile repo-codex,repo-local --sigils dispatch-spec,refine --spells invoke --force`
  - `formulae/dispatch-spec/development/run-validation-fixtures.sh`

### TASK-DISP-SURF-005: Approved Live Refresh

- Owner route: `task-session`
- Write scope:
  - `/mnt/c/Users/vlad_/.codex/skills`
  - repo `.agents/skills` if selected
  - generated backup report under `tools/development/` or `formulae/dispatch-spec/development/`
- Blocker:
  - Requires explicit user approval because it mutates machine-global Codex skill discovery.
- Steps:
  1. Create a timestamped backup of generated Arcanum packages being replaced.
  2. Regenerate installed packages with the fixed generator.
  3. Preserve non-Arcanum skills and unknown packages.
  4. Re-run the installed-package smoke that previously produced the missing `.agents/formulae/dispatch-spec` message.
- Validation:
  - installed package inventory shows no duplicate prefixed package drift.
  - installed `refine` and `dispatch-spec` package guidance can locate schema and catalog.

### TASK-DISP-SURF-VERIFY: Final Active Surface Audit

- Owner route: `task-session`
- Write scope:
  - validation report only
- Validation:
  - active skill grep has no unclassified command-surface invocation requirements.
  - dispatch-spec fixtures pass.
  - installed surface smoke passes or records an exact environmental blocker.

## SWU Execution Handoff

| SWU ID | Parent Task | Source Anchors | Dependencies | Write Scope | Done Criteria | Acceptance Evidence | Validation Surface | Execution Owner | Handoff Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-DISP-SURF-001 | TASK-DISP-SURF-001 | installed `refine` message; `formulae/dispatch-spec/SKILL.md`; `tools/bootstrap_arcanum.sh` package generation | none | report only | missing dependency path is classified | pass: `formulae/dispatch-spec/development/SKILL-SURFACE-DISPATCH-CANONICALIZATION-L0-RESULT.md` | `rg` plus file existence checks; dispatch fixture validation | local-fallback | completed |
| SWU-DISP-SURF-002 | TASK-DISP-SURF-002 | `arcana/refine/SKILL.md` stage-dispatch contract; codex-exec inventory active rows | SWU-DISP-SURF-001 | active skill/source contracts | skills no longer require command-surface invocation | pass: `formulae/dispatch-spec/development/SKILL-SURFACE-DISPATCH-CANONICALIZATION-SWU-002-RESULT.md` | active `SKILL.md` grep plus dispatch fixture suite | local-fallback | completed |
| SWU-DISP-SURF-003 | TASK-DISP-SURF-003 | `tools/bootstrap_arcanum.sh`; cleanup work-pack alias-only generation | SWU-DISP-SURF-001 | generator/package source | dispatch-spec generated package is canonical/self-sufficient | pass: `formulae/dispatch-spec/development/SKILL-SURFACE-DISPATCH-CANONICALIZATION-SWU-003-RESULT.md` | staged install checks | local-fallback | completed |
| SWU-DISP-SURF-004 | TASK-DISP-SURF-004 | dispatch-spec fixtures; staged install roots | SWU-DISP-SURF-003 | `/tmp` staged roots and validation report | staged installs validate without missing `.agents/formulae` files | pass: `formulae/dispatch-spec/development/SKILL-SURFACE-DISPATCH-CANONICALIZATION-SWU-004-RESULT.md` | fixture runner plus package smoke | local-fallback | completed |
| SWU-DISP-SURF-005 | TASK-DISP-SURF-005 | approved staged report; cleanup backup pattern | SWU-DISP-SURF-004, explicit approval | live generated skill surfaces | live installed aliases refreshed safely | pass: `formulae/dispatch-spec/development/SKILL-SURFACE-DISPATCH-CANONICALIZATION-SWU-005-RESULT.md` | installed package smoke | manual | completed |
| SWU-DISP-SURF-006 | TASK-DISP-SURF-VERIFY | all prior reports | SWU-DISP-SURF-005 | report only | final active surface audit passes | no unclassified active command-surface invocation; dispatch fixtures pass | grep, fixture runner, installed smoke | local-fallback | ready |

## Blockers

| Blocker ID | Scope | Description | Owner | Next Action |
| --- | --- | --- | --- | --- |
| B-DISP-SURF-001 | live install refresh | Mutating `/mnt/c/Users/vlad_/.codex/skills` changes machine-global skill discovery. | user | resolved: Option A approved; backup-first live refresh completed. |
| B-DISP-SURF-002 | unknown local packages | Prior cleanup preserved unknown `arcanum-orchestrate`; this plan should not delete or reinterpret it. | user/installer policy | Keep preserved unless a separate policy task resolves it. |
| B-DISP-SURF-003 | historical evidence | Prior refinement runs mention command surfaces and should not be rewritten as active policy. | task-session | Exclude historical evidence from active contract grep or classify it explicitly. |

## Gate Checks

| Gate | Condition | On Fail |
| --- | --- | --- |
| G-DISP-SURF-001 | canonical dispatch-spec schema and catalog exist before generator changes. | block |
| G-DISP-SURF-002 | active skill contracts use capability handles/receipts, not command-surface invocation, except legacy installer docs. | block |
| G-DISP-SURF-003 | staged generated packages can resolve dispatch-spec dependencies. | block |
| G-DISP-SURF-004 | live refresh has explicit approval and backup manifest. | block |
| G-DISP-SURF-005 | final grep has no unclassified active command-surface requirements. | flag or block depending on active owner. |

## Recommended Next Route

Next ready route is `SWU-DISP-SURF-006`, a report-only final active surface audit using the live installed smoke, command-surface classification, and dispatch fixture evidence from `SWU-DISP-SURF-005`.
