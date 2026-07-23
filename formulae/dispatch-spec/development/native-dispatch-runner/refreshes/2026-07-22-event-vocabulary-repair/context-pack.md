# Refresh Context Pack — Native Lifecycle Event Vocabulary Repair

Mode: Invoke Refresh, proposal-only

## Refresh objective

Convert the blocked SWU-NDR-011 native canary into an exact work-pack repair route that Task Session can execute without weakening the causal evidence requirement or overwriting the failed run.

## Covered obligations

1. Preserve the live blocked canary as evidence.
2. Name all five join-lifecycle events absent from the canonical schema.
3. Add one smallest repair SWU before the failure-canary retry.
4. Define successful-close and timeout/interrupt ordering acceptance in the same repair.
5. Make the SWU-NDR-011 blocked attempt visible in the manifest.
6. Keep SWU-NDR-012 locked until the retry passes.
7. Make the retry append-only below the existing failure boundary.
8. Update NDR-R7/NDR-R8 traceability and the cross-task blocker ledger.
9. Update the execution route so its L2 receipt includes the repair.
10. Preserve validator/executor and lifecycle/promotion authority boundaries.
11. Provide exact apply validation checks.
12. Return a Task Session route only after apply authorization.

## Selected source evidence

- Blocked result and Task Session receipt: the real helper returned non-pass, the gate blocked, zero dependent spawns occurred, and causal validation blocked.
- Evidence validator receipt: live sequences 3, 4, and 6 fail as unsupported kinds.
- Canonical Orchestrate skill: requires registration, wait, terminal, close, timeout, and interrupt lifecycle events.
- Canonical event schema and validator: admit only `agent_terminal` from that join lifecycle.
- Current TASK-NDR-004/005, manifest, traceability, gap ledger, execution dispatch, WORK-PACK, and W2/W3 files: target inventory for the refresh.

## Inventory lookup

`.arcanum/inventory/index.json` was parsed first. No entry matched Native Dispatch Runner, causal run evidence, lifecycle event vocabulary, or the failure canary. Status: `no_inventory_match`. Inventory contributes no authority and no proposed delta; the source artifacts above remain authoritative.

## Distill decision

Distill is skipped with rationale: the remediation already has one primary behavior—make the causal evidence model cover the complete declared native join lifecycle. Splitting terminal-close and timeout-interrupt support would knowingly leave the same contract/schema contradiction open and force another canary loop. The unit remains independently reviewable through one fixture matrix and one live failure rerun.

## Mutation boundary

This refresh is proposal-only. It writes only this refresh package and does not edit the target work-pack or runtime files. Apply requires explicit approval.
