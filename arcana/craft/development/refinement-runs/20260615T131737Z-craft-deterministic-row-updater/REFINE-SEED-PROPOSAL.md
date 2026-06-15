# Refine Seed Proposal: Craft Deterministic Row Updater

## Target

- Canonical target: `arcanum/arcana/craft`
- Historical evidence target: `arcanum/development/craft/`
- Prior planning baseline: `arcanum/arcana/craft/development/refinement-runs/20260615T121512Z-craft-ledger-csv-json-indexes/`

## Operator Intent

Determine whether Craft needs a deterministic row updater tool, rather than only
a broad CSV import dry-run, before implementing ledger projection writeback.

## Refinement Objective

Produce a non-executed design/plan decision for the smallest safe row update
surface:

- whether to create a dedicated deterministic row updater/reconciler;
- whether it should precede or live inside `import-csv --dry-run`;
- which row families and fields are editable in the first slice;
- which stale-source, ID-preservation, reference, and read-only nested-field
  checks are mandatory before YAML mutation.

## Source Context

- `arcana/craft/SKILL.md` keeps `.craft/ledger.yml` as source of truth and says
  generated indexes are rebuildable, not authoritative.
- `arcana/craft/templates/ledger.schema.yml` defines stable row families and
  validation rules for IDs, references, decisions, blockers, and indexes.
- `20260615T121512Z-craft-ledger-csv-json-indexes/RESULT.md` recommends JSON
  and CSV projections, with CSV writeback gated by dry-run reconcile proof.
- `TASK-CLP-004` and `SWU-CII-005` already name a CSV import dry-run, but the
  current acceptance text is broad and may hide the smaller deterministic row
  update primitive needed for safe writeback.

## Write Scope

Before confirmation, write only this refinement run folder.

After confirmation, runtime-backed stages may write stage artifacts inside this
run folder. Canonical Craft source files, scripts, generated runtime mirrors,
publication state, and parent gitlinks remain out of scope unless a later
approved route explicitly opens them.

## Done Criteria

- A dispatch route exists and validates before runtime-backed stages.
- The run decides between no new tool, a dedicated row updater/reconciler, or a
  broad import dry-run with row-update internals.
- The final plan names the first safe SWU and blocks direct YAML mutation until
  toy-fixture proof exists.
- The result preserves YAML authority and public-boundary rules.

## Validation Surface

- `python3 arcanum/formulae/dispatch-spec/scripts/validate-dispatch.py <run>/REFINE-DISPATCH.json`
- stage artifact existence checks after confirmation;
- fixture-shaped toy-game requirements for row ID preservation, stale-source
  detection, unresolved-reference blocking, and read-only nested-field reporting.

## Preset And Research

- Preset: `compact`
- Research: `no-research`

Local evidence is sufficient for the strategy proposal. External research is
blocked unless a confirmed Refine stage identifies a named gap.
