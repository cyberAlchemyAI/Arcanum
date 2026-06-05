---
module: skill-surface-dispatch-canonicalization
version: current
status: draft
updatedAt: 2026-06-03
docType: implementation-layering
---

# Implementation Layering: Skill Surface Dispatch Canonicalization

## Purpose

Make `dispatch-spec` the canonical route-shape authority for Arcanum orchestration while removing command-surface invocation requirements from active skill contracts.

## Source Contract

- Trigger evidence: installed `refine` reported that `.agents/formulae/dispatch-spec/dispatch.schema.yml` and `.agents/formulae/dispatch-spec/TECHNIQUE-CATALOG.md` were missing.
- Canonical dispatch package: `formulae/dispatch-spec/`.
- Refine contract: `arcana/refine/SKILL.md`.
- Invoke plan contract: `spells/invoke/plan.md`.
- Prior runtime migration plan: `formulae/dispatch-spec/development/ORCHESTRATION-RUNTIME-PLAN.md`.
- Prior surface inventory: `formulae/dispatch-spec/development/CODEX-EXEC-SURFACE-INVENTORY.md`.
- Cleanup work-pack: `tools/development/CODEX-SKILL-SURFACE-CLEANUP-WORK-PACK.md`.

## Target And Scope

- Target: active Arcanum skill contracts, generated Codex skill packages, and dispatch-spec install/validation surfaces.
- Scope: source contracts, generator behavior, installed package dependency layout, validation scripts, and live-surface refresh after approval.
- Current state: canonical dispatch-spec exists in the repo, but generated/installed runtime surfaces can look for copied dependencies under `.agents/formulae/dispatch-spec/`, and some active skill contracts still require command-surface stage execution language.

## Layer Decision Table

| Layer | Decision Question | Minimum Working Unit | Included Scope | Deferred Scope | Exit Evidence | Promotion Decision |
| --- | --- | --- | --- | --- | --- | --- |
| L0 (POC) | After this layer, we know whether current active failures are dependency-path drift or missing canonical source. | Reproduce the installed-package dispatch-spec lookup and compare it to `formulae/dispatch-spec/`. | inventory of failing path assumptions and canonical source files. | generator mutation and live `$CODEX_HOME` refresh. | report shows each missing installed file maps to a canonical source file or a generator bug. | continue if no canonical file is missing. |
| L1 | After this layer, we know whether skills can describe capability execution without invoking legacy command surfaces. | Update active skill/source contracts to use capability handles, dispatch documents, native skill/subagent receipts, and deterministic validators. | `arcana/refine/SKILL.md`, active orchestration skill docs, and validation guidance. | historical generated run evidence. | grep report shows active skill contracts do not require `.codex/commands`, `tools/arcanum --exec`, or command-backed stages except as explicit legacy compatibility. | promote if skill contracts remain executable through native skill usage. |
| L2 | After this layer, we know whether generated installed packages contain or resolve dispatch-spec dependencies correctly. | Change bootstrap/package generation so `dispatch-spec` is self-sufficient or dependency-resolving in generated runtime packages. | `tools/bootstrap_arcanum.sh`, generated `dispatch-spec` package shape, repo `.agents`/personal `$CODEX_HOME` staged installs. | live cleanup of unknown preserved packages. | staged install validates a dispatch JSON without falling back to `.agents/formulae/dispatch-spec/` unless that folder is intentionally installed. | promote if staged installs pass on personal and repo profiles. |
| L3 | After this layer, we know whether live installed surfaces are clean and current. | Regenerate or refresh installed aliases after source/generator fixes, preserving user-local non-Arcanum skills. | `/mnt/c/Users/vlad_/.codex/skills`, repo `.agents/skills`, generated reports. | deleting unknown packages without policy. | installed `refine` can validate dispatch-spec using the canonical package, and live grep has no active command-surface invocation requirements in skills. | ready for routine use after user-approved live refresh. |

## Non Regression Guardrails

- Do not copy all Arcanum internals into runtime packages.
- Do not make `.codex/commands/` a prerequisite for skill execution.
- Do not treat `.agents/` as canonical source.
- Do not rewrite historical refinement-run evidence by default.
- Preserve explicit legacy command adapters only as compatibility paths.
- `dispatch-spec` validates route shape and technique evidence; it does not own lifecycle execution.
- Generated aliases must either be self-sufficient for their own required deterministic validators or carry an explicit dependency-resolution rule to repo canonical files.

## Recommended Next Layer

- Next layer: L0.
- Key decision unlocked: whether the installed failure is solved by dependency packaging, canonical path resolution, or both.
- Major deferred scope: mutation of live personal Codex-home packages until staged generation proves the new package shape.
