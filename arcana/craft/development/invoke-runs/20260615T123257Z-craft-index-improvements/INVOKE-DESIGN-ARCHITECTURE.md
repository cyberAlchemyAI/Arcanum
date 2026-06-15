# Invoke Design And Architecture: Craft Index Improvements

## Design Identity

- Spell: `invoke`
- Modes: `design`, `plan`
- Target artifact: Craft ledger index improvements.
- Target owner: `arcana/craft`
- Phase status: `pass-with-gated-execution`
- Source refs:
  - `../refinement-runs/20260614T200439Z-craft-feature-readiness-indexes/RESULT.md`
  - `../refinement-runs/20260615T121512Z-craft-ledger-csv-json-indexes/RESULT.md`

## Context View

Craft already defines a YAML-ledger authority model: `.craft/ledger.yml` owns
structured state, `CRAFT.md` is a linked human view, and `.craft/index.json` is
rebuildable lookup data. Two refine runs exposed complementary improvements:

- readiness indexes: make work-pack/SWU readiness, approval scope, execution
  mode, and blocked mutation/publication scopes visible in Craft state;
- generated index/projection layer: make repeated reads fast and bulk review
  safer through `.craft/index.json` plus `.craft/projections/*.csv`.

The architecture must combine those without turning Craft into an executor and
without making generated files authoritative.

## High-Level Structure View

```text
ledger.yml
  owns canonical Craft rows, optional embedded compatibility indexes, and row links
      |
      v
craft-index build
  reads YAML, validates row families, emits generated lookup surfaces
      |
      +--> index.json
      |      metadata, by_id, by_family, pending_by_node, readiness, links, evidence
      |
      +--> projections/*.csv
             flat generated review/import staging surfaces

craft-index validate
  verifies freshness, references, supported row families, deterministic outputs

craft-index import-csv --dry-run
  compares edited projections against ledger hash and emits a patch plan only
```

## Low-Level Components View

| Component | Write Surface | Owner | Architecture Rule |
| --- | --- | --- | --- |
| Source contract | `arcana/craft/templates/ledger.schema.yml` | Craft | Add additive projection/readiness contracts; do not break existing ledgers. |
| Operating contract | `arcana/craft/SKILL.md` | Craft | Explain generated projections, all-status fast path, and non-execution boundary. |
| Human docs | `arcana/craft/README.md` | Craft | Summarize storage model and projection policy for users. |
| Public fixture | `arcana/craft/fixtures/craft-index-improvements/` | Craft | Synthetic fixture only; proves row-family coverage and public boundary. |
| Projection tool | `arcana/craft/scripts/craft-index.py` | Craft | Deterministic build/validate/dry-run import tool. |
| Generated mirrors | `.agents/skills/craft`, `.claude/skills/craft`, other generated runtime copies | Runtime generation | Refresh only after canonical source validation passes. |

## Workflow Process View

1. A Craft ledger records contexts, artifacts, blockers, decisions, gaps,
   relations, handoffs, receipts, and recomposition rows.
2. Optional readiness fields/indexes point to executable work-pack/SWU handles,
   approval records, execution modes, worktree scopes, and blocked mutation or
   publication scopes.
3. `craft-index build` derives `.craft/index.json` and
   `.craft/projections/*.csv`.
4. `craft-index validate` checks source hash freshness, row-family coverage,
   row references, links/evidence normalization, deterministic CSV headers, and
   readiness lookup integrity.
5. `craft-index import-csv --dry-run` can convert edited CSV fields into a patch
   plan, but does not mutate YAML until dry-run proof and approval exist.
6. `state all` can use `pending_by_node` and readiness summaries when the
   generated index is fresh; stale indexes trigger YAML fallback and a warning.

## Decision Flow View

| Decision | Selected | Reason |
| --- | --- | --- |
| Single combined architecture | Yes | Readiness and projection improvements share index authority, freshness, and status-rendering concerns. |
| One-go execution profile | Yes, with gates | One native goal may execute the ordered bundle, but each mutation/publication gate remains explicit. |
| YAML authority | Preserve | Generated JSON/CSV must never own canonical facts. |
| `.craft/projections/` | Selected | Names CSV as generated views, not authority tables. |
| Embedded indexes | Compatibility first | Existing ledgers can keep them while `.craft/index.json` becomes generator-owned fast path. |
| Import writeback | Dry-run first | Direct CSV mutation is unsafe until toy-game fixtures prove reversible mapping. |
| Fixture strategy | Synthetic public-safe fixture | Avoids leaking private workspace/project details into public `arcanum`. |

## Dependency Interface View

- Upstream: Refine results and Invoke work-packs provide readiness/projection
  requirements.
- Craft schema/docs: own canonical contract changes.
- Projection tool: owns deterministic generated output behavior.
- Task Session or native Codex Goal: owns later implementation execution.
- Submodule discipline: public `arcanum` changes must be committed and pushed
  before parent gitlink publication.

## Architecture Risks

| Risk | Mitigation |
| --- | --- |
| Generated projections become hidden authority. | Source-of-truth wording, metadata, stale checks, validator warnings. |
| CSV flattening loses nested links/evidence. | Keep complex fields read-only until import dry-run proof. |
| Live row families are skipped. | Fixture and validator must flag unsupported families. |
| Readiness index implies execution proof. | README/SKILL state Craft records readiness only; execution owners return receipts. |
| Public fixture leaks private context. | Synthetic fixture and generated-output public-boundary scan. |

## Handoff To Plan

Plan mode should produce a medium-complexity split work-pack with a selected
one-go orchestration task. Execution may proceed in one native Codex goal, but
the goal must stop on unresolved approval, unsafe public-boundary evidence,
failing validation, or publication requests.
