---
module: inventory-whole-arcanum
version: 0.1.0
status: draft
updatedAt: 2026-05-29
docType: source-policy
---

# Source Policy: Whole Arcanum Inventory

## Purpose

This policy decides what the whole-Arcanum inventory may ingest after
`source-manifest.json` identifies the initial source families.

## Default Rule

Inventory may summarize and index tracked source artifacts from these families:

- `arcana/`
- `spells/`
- `transmutations/`
- `formulae/`
- `framework/`
- `registry/`
- `tools/`
- `.codex/commands/`

The source boundary starts from `git ls-files`, not untracked filesystem state.

## Generated And Local Runtime Exclusions

Exclude generated and local runtime paths by default:

- `.arcanum/codex-home/**`
- `.arcanum/codex-home-smoke/**`
- `.arcanum/runtime/**`
- `.arcanum/observability/runs/**`
- `.arcanum/observability/reflections/**`
- `.arcanum/observability/by-sigil/*.jsonl`
- `.arcanum/observability/by-capability/**/*.jsonl`
- `.arcanum/observability/hooks/*.jsonl`
- `.arcanum/observability/signals/*.jsonl`
- `.arcanum/observability/reflection-state.json`
- `**/development/runs/**`
- `**/development/example-runs/**`
- `**/development/example-outputs/**`
- `benchmark/artifacts/**`
- `benchmark/logs/**`
- `output/**`
- `tmp/**`

These paths may not become source inventory scope just because they exist or are
tracked.

## Durable Evidence Promotion

Durable evidence can be included only when a nearby source artifact explains why
the evidence matters.

Acceptable promotion anchors:

- a current work-pack row,
- a readiness report,
- a validation report,
- a package README,
- a task-session result that is explicitly cited by one of the above.

If no promotion anchor exists, keep the artifact out of the source inventory and
record a selector gap.

## Development Artifact Treatment

Development docs are not automatically generated state. The inventory may include
development contracts when they govern current behavior, such as:

- `SPEC.md`
- `ARCHITECTURE.md`
- `WORK-PACK.md`
- `IMPLEMENTATION-LAYERING.md`
- `EXECUTION-PACK.md`
- `READINESS.md`
- validator or migration plans referenced by those files.

Unpromoted run folders and loose experiment output remain excluded.

## Schema Rule

Inventory must not create or promote new machine-readable schemas outside the
Schema Constitution rule. Canonical machine-readable schemas use `.schema.yml`.
Markdown schema explainers are allowed only when paired with a `.schema.yml`
counterpart or marked non-canonical.

## Query Rule

The inventory is optimized for agents. Cards should preserve source selectors,
brief captured claims, and enough trace for shell plus `jq` queries. Human UI
work remains deferred.

## Stop Conditions

Stop and route to a decision gate when:

- a path looks both generated and source-owned,
- a durable evidence candidate lacks a promotion anchor but is needed for an
  implementation decision,
- a source family would require broad full-file ingestion to be useful,
- two artifacts claim authority over the same definition or lifecycle rule.
