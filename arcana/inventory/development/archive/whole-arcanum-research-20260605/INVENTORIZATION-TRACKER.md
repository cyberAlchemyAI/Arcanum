---
module: inventory-whole-arcanum
version: 0.1.0
status: active
updatedAt: 2026-06-05
docType: tracker
---

# Tracker: Arcanum Inventorization

## Purpose

This tracker records how Arcanum has been inventorized, what remains missing,
and which gaps should drive the next slices.

It is the working ledger for `INVENTORIZATION-METHOD.md`.

## Current Inventory State

| Slice | Status | Cards | Retrieval Fixture | Coverage Report | Notes |
| --- | --- | ---: | --- | --- | --- |
| `inventory` | pass | 4 | yes | not separate | First proof slice for Inventory itself. |
| `governance` | pass | 2 | yes | not separate | Artifact and schema constitution proof cards. |
| `lifecycle` | pass | 3 | yes | not separate | Invoke, Refine, and Task Session lifecycle boundary cards. |
| `arcana` | pass | 5 | yes | yes | Clustered high-value arcana capability families. |
| `composition` | pass | 5 | yes | yes | Spells, transmutations, and formulae composition surfaces. |
| `runtime` | pass | 5 | yes | yes | Framework, registry, tools, and native runtime boundary. |

Total current cards: 24.

## Current EvidenceSets

| EvidenceSet | Status | Cards | Use |
| --- | --- | ---: | --- |
| `evidence-set.whole-arcanum.inventory-self.next-slice-context` | candidate | 4 | Choose source context before adding another Inventory card slice. |
| `evidence-set.whole-arcanum.can-implement-next-swu` | candidate | 5 | Decide whether a planned Inventory SWU is executable or needs a gate. |

EvidenceSets remain candidate-level until repeated task-session reuse proves
stable value.

## Inventorization Method Status

| Method Step | Status | Evidence | Gap |
| --- | --- | --- | --- |
| Source boundary | pass | `source-manifest.json`, `SOURCE-POLICY.md` | none |
| Slice-aware validation | pass | `validate-evidence-card-slice.sh`, whole validator | none |
| Card authoring shape | pass | existing slice `cards.json` files | none |
| Retrieval fixture shape | pass | existing `retrieval.json` files | none |
| Coverage report shape | partial | `arcana`, `composition`, `runtime` coverage reports | `inventory`, `governance`, and `lifecycle` lack separate coverage reports because they were proof slices. |
| Reuse evidence template | pass | `INVENTORIZATION-METHOD.md` | not yet used in a real task |
| Live task proof | blocked | `DECISION-LIVE-ARCANUM-TEST.md` | first lane not selected |

## Known Missing Coverage

| Gap ID | Missing Area | Why It Matters | Current Handling | Next Trigger |
| --- | --- | --- | --- | --- |
| INV-GAP-001 | Fine-grained per-sigil cards | Current cards cluster families; a task may need specific sigil behavior. | Deferred to concrete task demand. | A live task falls back to broad search for one sigil. |
| INV-GAP-002 | Per-spell operational cards | Composition slice covers families, not every spell. | Deferred. | A task needs a specific spell beyond `invoke`. |
| INV-GAP-003 | Coverage reports for proof slices | Inventory/governance/lifecycle slices validate but do not each have `COVERAGE.md`. | Non-blocking. | A maintenance task touches those slices. |
| INV-GAP-004 | Reuse ledger from real task | Promotion needs evidence that Inventory reduces search cost. | Blocked by live task lane decision. | User selects A, B, C, or D in `DECISION-LIVE-ARCANUM-TEST.md`. |
| INV-GAP-005 | Native wrapper for whole validation | Current validation is shell script plus `jq`. | Deferred. | Agents repeatedly struggle to run the shell command. |
| INV-GAP-006 | EvidenceSet promotion evidence | Candidate sets exist but need repeated task-session reuse. | Deferred. | At least three task-session runs consume EvidenceSets successfully. |

## Current Blocker

| Blocker | Status | Artifact | Recommendation |
| --- | --- | --- | --- |
| `B-LAT-001` first live task lane | open | `decisions/DECISION-LIVE-ARCANUM-TEST.md` | Choose `C. EvidenceSet reuse lane`. |

## Next Slice Queue

| Priority | Candidate Slice | Trigger | Suggested Retrieval Question |
| --- | --- | --- | --- |
| 1 | EvidenceSet reuse result | `B-LAT-001` resolved to C | What evidence tells an agent whether the next Inventory SWU can execute directly? |
| 2 | Missing sigil-specific slice | live task fallback search finds missing sigil context | What source context does an agent need before changing `<sigil>`? |
| 3 | Proof-slice coverage reports | maintenance pass touches inventory/governance/lifecycle cards | What was intentionally omitted from the proof slices? |
| 4 | Native validation wrapper | shell plus `jq` becomes annoying or error-prone | How should agents run whole-inventory validation without remembering paths? |

## Update Rules

Update this tracker whenever:

- a slice is added or materially changed,
- a task uses Inventory before source search,
- a fallback search reveals missing cards,
- an EvidenceSet is used, split, rejected, or proposed for later promotion,
- validation fails or starts warning about Inventory-owned artifacts,
- a coverage report records a new omission or duplicate-risk area.

## Validation Commands

```bash
bash arcana/inventory/scripts/validate-evidence-card-slice.sh arcana/inventory/development/whole-arcanum/cards/<slice>
bash arcana/inventory/development/whole-arcanum/scripts/validate-whole-arcanum-inventory.sh
```

## Latest Tracker Update

2026-06-05: Added explicit inventorization method and tracker because the prior
package proved Inventory structure but did not clearly explain or track how to
continue inventorizing Arcanum.
