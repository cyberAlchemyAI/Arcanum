# TASK-004: Create Handoff Examples

## Objective

Create downstream handoff examples for Ontology Vault and Definitions Governance.

## Source Contracts

- `../../INTERFACES.md`
- `../../FLOWS-POLICIES.md`

## Smallest Working Units

### SWU-INV-KS-007

- Goal: Add ontology and definitions handoff JSON examples.
- Dependencies: SWU-INV-KS-005.
- Write scope: `arcana/inventory/development/pilot/evidence-card/pilot-handoff-ontology.json`, `arcana/inventory/development/pilot/evidence-card/pilot-handoff-definitions.json`.
- Done criteria: both packets include source refs and non-authority notices.
- Validation: `jq empty arcana/inventory/development/pilot/evidence-card/pilot-handoff-ontology.json arcana/inventory/development/pilot/evidence-card/pilot-handoff-definitions.json`
- Execution owner: subagent.
- Status: completed on 2026-05-27.
- Evidence: `../../task-session/SWU-INV-KS-007-CONTEXT.md`, `../../task-session/SWU-INV-KS-007-RESULT.md`.

## Synchronization

After completion, readiness review can check handoff clarity.

## Completion Evidence

| SWU | Status | Evidence | Validation |
| --- | --- | --- | --- |
| SWU-INV-KS-007 | completed | `pilot-handoff-ontology.json`, `pilot-handoff-definitions.json` | `jq empty`; both packets include `non_authority_notice` and `source_refs` |
