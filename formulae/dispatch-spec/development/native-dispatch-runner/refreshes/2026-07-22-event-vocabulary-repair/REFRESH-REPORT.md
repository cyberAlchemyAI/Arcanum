# Invoke Refresh Result

- Mode: refresh
- Spell: invoke
- Canonical ID: invoke
- Scope: library
- Phase status: PASS
- Phase status basis: complete exact proposal; 0 refresh-authoring blockers
- Handoff readiness: READY for Task Session
- Mode contract: `arcanum/spells/invoke/refresh.md`
- Outputs: `REFRESH-REPORT.md`, `refresh-report.json`, `REFRESH-PATCH-PROPOSAL.md`, context pack, dispatch trace, validated refresh dispatch
- Mutation mode: apply-approved
- Source signals: 4 — blocker opened, artifact drift, route changed, evidence added
- Target artifacts: 9 work-pack/route artifacts
- Proposed changes: add SWU-NDR-010R, record blocked SWU-NDR-011 attempt, make retry append-only, update dependencies/gates/traceability
- Applied changes: 9/9 approved target artifacts, validated
- Skipped changes: historical receipt rewrite, blocked canary rewrite, runtime implementation, Inventory mutation
- Dispatch techniques: 9 selected; full dispatch validation PASS with zero blocks/flags
- Distill validation: skipped with rationale — one contract-completion behavior must cover both terminal branches together
- Inventory: lookup-only, machine-index-first, `no_inventory_match`; no authority contribution
- Decisions: preserve SWU-NDR-010 historical PASS; use a new repair SWU; preserve blocked canary root; retry under `failure/retry-001/`; keep success locked
- Blockers by scope: refresh-authoring 0, apply-authorization 0, target-lifecycle 3, audit 1
- Unresolved target gaps: complete lifecycle event model, failure retry, success canary, adjudication/recomposition
- Next route: Task Session `TASK-NDR-004 / SWU-NDR-010R`

## Applied route

The live work pack now contains one repair unit before the canary:

```text
SWU-NDR-010 PASS (historical original cases)
  -> SWU-NDR-010R (all five join lifecycle kinds and both branches)
  -> SWU-NDR-011 retry in failure/retry-001/
  -> SWU-NDR-012 success canary
  -> SWU-NDR-013 adjudication
  -> TASK-NDR-VERIFY
```

The blocked SWU-NDR-011 attempt remains immutable evidence. No success work becomes executable merely because this proposal passes.

## Handoff

Invoke Task Session on `TASK-NDR-004 / SWU-NDR-010R` only. Runtime implementation and canary execution remain unstarted by this refresh.
