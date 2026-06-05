---
module: inventory-whole-arcanum
status: active
updatedAt: 2026-06-01
docType: operational-command-contract
---

# Operational Commands: Whole Arcanum Inventory

## Purpose

This contract defines the agent-fast shell plus `jq` surface for refreshing,
linting, validating, and querying the whole-Arcanum inventory without a human UI.

## Primary Validation

Run the full validation suite from the repository root:

```bash
bash arcana/inventory/development/whole-arcanum/scripts/validate-whole-arcanum-inventory.sh
```

The suite checks:

- every current slice under `cards/*/`,
- slice indexes and retrieval fixtures,
- source reference paths and line spans,
- candidate EvidenceSet references against known card IDs,
- pilot evidence-card fixtures,
- Artifact Constitution self-test,
- current Artifact Constitution validation.

Known pre-existing benchmark generated-artifact warnings from the Artifact
Constitution validator are not this inventory task's blocker when the validator
still returns `result: pass`.

## Slice Validation

Run one slice:

```bash
bash arcana/inventory/scripts/validate-evidence-card-slice.sh arcana/inventory/development/whole-arcanum/cards/runtime
```

Replace `runtime` with `inventory`, `governance`, `lifecycle`, `arcana`, or
`composition`.

## Query Examples

List all cards by ID and title:

```bash
jq -r '.cards[] | [.id, .title] | @tsv' arcana/inventory/development/whole-arcanum/cards/*/cards.json
```

Find cards tagged for runtime support:

```bash
jq -r '.cards[] | select(.tags | index("runtime")) | [.id, .title] | @tsv' arcana/inventory/development/whole-arcanum/cards/*/cards.json
```

Find selected cards in a retrieval fixture:

```bash
jq -r '.selected_cards[] | [.id, .reason] | @tsv' arcana/inventory/development/whole-arcanum/cards/composition/retrieval.json
```

Check EvidenceSet references:

```bash
jq -r '.evidence_sets[] | .set_id as $set | .card_refs[] | [$set, .id, .inclusion_reason] | @tsv' arcana/inventory/development/whole-arcanum/evidence-sets/evidence-sets.json
```

## Refresh Rule

A refresh is valid when it:

1. starts from `source-manifest.json` and `SOURCE-POLICY.md`,
2. updates only the affected slice folder and synchronized task evidence,
3. records intentional omissions and duplicate/ownership risks in `COVERAGE.md`,
4. runs the slice validator,
5. runs the whole validation suite before handoff.

Do not add broad full-file ingestion just because a family has more source files.
Record selector gaps instead.

