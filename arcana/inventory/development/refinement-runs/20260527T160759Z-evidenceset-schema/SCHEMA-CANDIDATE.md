# EvidenceSet Schema Candidate

## Status

candidate-only

## Coherent Unit

An `EvidenceSet` is a stable, task-scoped grouping of evidence-card IDs with inclusion reasons, exclusion reasons, index terms, handoff intent, and residue.

It exists to make agent retrieval and downstream handoff assembly faster and more explainable. It does not own source evidence, duplicate card content, decide ontology authority, or replace Context Builder packs.

## Minimal JSON Shape

```json
{
  "schema_version": "inventory.evidence_set.v0",
  "set_id": "evidence-set.example",
  "purpose": "Short task-shaped reason this set exists.",
  "card_refs": [
    {
      "id": "inventory.card.example",
      "inclusion_reason": "Why this card belongs in the set."
    }
  ],
  "excluded_card_refs": [
    {
      "id": "inventory.card.excluded",
      "reason": "Why this nearby card is outside the set boundary."
    }
  ],
  "index_terms": [
    "retrieval-key"
  ],
  "handoff_target": "context-builder",
  "synthesis_note": "Short explanation of what the grouped cards preserve.",
  "residue": "What remains unresolved or intentionally out of scope.",
  "status": "candidate",
  "promotion_owner": "inventory"
}
```

## Required Fields

| Field | Purpose |
| --- | --- |
| `schema_version` | Lets agents distinguish candidate set shape from retrieval output shape. |
| `set_id` | Stable ID for repeated reference. |
| `purpose` | Task-shaped reason the group exists. |
| `card_refs[]` | Included evidence-card IDs plus inclusion rationale. |
| `excluded_card_refs[]` | Boundary evidence so the set does not silently absorb noise. |
| `index_terms[]` | Fast agent query surface. |
| `handoff_target` | Intended downstream consumer, without granting authority. |
| `synthesis_note` | One short explanation of why the group is useful. |
| `residue` | Open questions or limits that must not be hidden. |
| `status` | Candidate lifecycle state. |
| `promotion_owner` | Required when status implies promotion or terminal ownership. |

## Candidate Status Values

- `candidate`: useful enough to test, not canonical.
- `promote-pending`: candidate passed validation and awaits explicit promotion.
- `rejected`: candidate failed usefulness or boundary checks.
- `superseded`: replaced by a better set or schema.

## Validation Rules

- `set_id` must be unique within the evidence-set index.
- `card_refs` must be non-empty.
- Every `card_refs[].id` and `excluded_card_refs[].id` must resolve to an existing evidence card.
- Every included card must have an `inclusion_reason`.
- Every excluded card must have a `reason`.
- `index_terms` must be non-empty and short.
- `status` must use the controlled vocabulary.
- `promotion_owner` is required for `promote-pending`, `rejected`, and `superseded`.
- `synthesis_note` and `residue` must be short strings, not long-form synthesis.
- The set must not duplicate evidence-card source excerpts or summaries.

## Fit Against Current Candidates

| Candidate | Fit |
| --- | --- |
| `evidence-set.evidenceset-need` | Fits the minimal shape. Needs only `schema_version`, `status`, and `promotion_owner` added if promoted from retrieval output into a stored candidate artifact. |
| `evidence-set.craft-recursive-ledger` | Fits the minimal shape and validates the need for explicit exclusions, index terms, handoff target, synthesis note, and residue. |

## Non-Goals

- No source excerpt duplication.
- No ontology or definitions authority.
- No replacement for Context Builder handoff packs.
- No ledger, dependency graph, or lifecycle manager.
- No human UI fields.
- No ranking/scoring model in the first schema.
- No nested multi-artifact package.

## Recommended Storage

Keep the first implementation simple:

- add a production candidate template for one `EvidenceSet`;
- add one fixture file for stored candidate sets;
- add index references only after the fixture shape passes;
- keep retrieval output allowed to include an inline candidate set, but make stored sets use `schema_version`.
