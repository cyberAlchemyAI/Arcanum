# Inventory Readiness Gate (G3)

Purpose: define the mandatory readiness checks before any experiment can proceed from sourcing to execution.

Gate owner: Inventorist
Pipeline stage: S6
Blocking behavior: if G3 fails, execution stops and returns remediation actions.

## Inputs

- Experiment protocol file in `experiments/<experiment-key>/protocol.md`
- Source selection file in `experiments/<experiment-key>/sources.md`
- Inventory index: `inventory/INVENTORY-INDEX.md`
- Source catalog: `sources/SOURCE-CATALOG.md`

## Gate Criteria

| Check | Pass Condition | Failure Action |
|---|---|---|
| Required entry types declared | Protocol declares required entry types for the experiment | Return BLOCKED with missing protocol fields |
| Source-to-inventory coverage | Every selected source has a corresponding inventory entry or approved waiver | Run `ingest` or request source replacement |
| Extraction completeness | Required fields for each entry type are populated | Run `ingest` re-extraction |
| Version pin consistency | Inventory entries reference the same pinned source version as source catalog | Re-pin source metadata and re-validate |
| Traceability links | Inventory entry references experiment ID and source ID | Patch inventory metadata |
| Inventory index freshness | INVENTORY-INDEX includes all entries used in the experiment | Rebuild index and re-run `validate` |

## Decision Outputs

- PASS: all checks pass.
- NEEDS-REVISION: non-blocking metadata inconsistencies only.
- BLOCKED: missing entry coverage, missing required fields, or stale/unpinned source references.

## Decision Flow

1. Parse experiment protocol and collect required entry types.
2. Run inventory lookup by experiment and entry type.
3. Build a coverage table: required source IDs vs available inventory entries.
4. If gaps exist:
   - If source exists and is accessible, run `ingest --source <source-id>`.
   - If source was used in prior completed runs, run `backfill --experiment <EX>`.
   - If source cannot be used, return to sourcer for substitution.
5. Run inventory validation for completeness and traceability.
6. Emit G3 decision with blocking reasons or pass confirmation.

## Recommended Command Patterns

- `lookup --experiment E4 --entry-type framework-architecture`
- `validate --experiment E4`
- `ingest --source GH-eShopOnContainers --entry-type domain-model`
- `backfill --experiment E6`

## Required Readiness Report Format

```
## Inventory Readiness Report

Experiment: <id>
Decision: PASS | NEEDS-REVISION | BLOCKED

Coverage:
- Required sources: <n>
- Inventoried sources: <n>
- Missing sources: <list>

Blocking Issues:
- <issue 1>
- <issue 2>

Remediation:
1. <action>
2. <action>
```
