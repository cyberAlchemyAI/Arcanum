# MARS Inventory Library Contract

Purpose: define the required chain from authority reference to reusable inventory knowledge and, when possible, down to the raw source content that inventory claims are extracted from.

Scope: all new or refreshed library-grade inventory work in MARS projects.

## Required Knowledge Chain

Library-grade inventory should preserve a visible chain with these layers:

1. `sources/SOURCE-CATALOG.md`
   - discovery and selection layer
2. `sources/REFERENCE-LEDGER.md`
   - authority and pin layer
3. `inventory/INVENTORY-INDEX.md`
   - lookup and coverage layer
4. `inventory/library/<source-id>.md`
   - extracted knowledge layer
5. `inventory/raw/<source-id>/...`
   - raw source content or user-provided raw material layer

This chain is the default target for library-grade inventory.

## Contract Rules

| Rule ID | Rule                                                                                                                                                            |
| ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| IL0     | A primary or supporting reference is not library-grade if it only has a one-paragraph summary or thematic rollup mention.                                       |
| IL1     | Every library-grade source should have one dedicated extracted-content file at `inventory/library/<source-id>.md`.                                              |
| IL2     | The extracted-content file must cite the raw-content origin used to produce its claims.                                                                         |
| IL3     | If source content can be retrieved lawfully from the web, preserve the relevant raw material or pinned excerpt under `inventory/raw/<source-id>/`.              |
| IL4     | If source content cannot be retrieved from the web, the workflow must request user-provided raw files and store them under `inventory/raw/<source-id>/`.        |
| IL5     | The inventory index must show whether each source has both a library entry and a raw-content backing artifact.                                                  |
| IL6     | Thematic rollups such as `methodology-authorities.md` or `agentic-conversation-prior-art.md` are secondary views, not substitutes for per-source library files. |
| IL7     | Every extracted claim in a library file must point to either a raw-content anchor, a precise source location, or an explicit unresolved-anchor note.            |

## Required Fields For `inventory/library/<source-id>.md`

- source ID
- reference ID when available
- entry type
- canonical citation and pin
- acquisition mode (`web-retrieved` or `user-provided-raw`)
- raw content path(s)
- extraction date
- extracted constructs or findings
- cautions and limitations
- experiment relevance
- anchor notes describing where the content came from

## Required Fields For `inventory/raw/<source-id>/`

- one provenance note or README describing:
  - what raw files exist
  - how they were obtained
  - pin or version identifier when available
  - whether they are complete documents, excerpts, OCR, or user-supplied copies

## Library-Grade Interpretation

A library-grade inventory entry should let a later researcher answer both questions without re-discovery:

- what does this source actually contain that matters?
- where did that extracted knowledge come from?

If the second question cannot be answered, the entry is not yet fully library-grade.

## Usage Notes

1. Use `inventory/INVENTORY-INDEX.md` as the quick lookup view.
2. Use `inventory/library/<source-id>.md` as the reusable knowledge artifact.
3. Use `inventory/raw/<source-id>/` as the provenance base.
4. Keep thematic rollups as convenience views only.
