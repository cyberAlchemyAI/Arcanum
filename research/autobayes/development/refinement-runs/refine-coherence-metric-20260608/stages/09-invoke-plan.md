---
stage: 9
name: Invoke Plan (DCI, non-executed)
capability: invoke
mode: plan
status: pass
dispatch_id: refine-coherence-metric-20260608
---

# Invoke Plan — DCI workflow-reflect integration (non-executed)

Running this is owned by `workflow-reflect` + `observability`, not this loop.

## Plan → Waves

### Wave 0 — fixes the backtest forced
- T0.1 Drop the inert reopen term from DCI v1; keep the objective backbone (status + drift + qbar + gaps), enum-normalized.
- T0.2 Replace reopen in v1 with a *real* recomposition signal: a later record touching the same `files_changed` paths, or a revert, within a window. Spec only — not built here.
- T0.3 Add a data-quality proposal to observability owners: **normalize the `execution.status` enum** (the store has `pass`/`flag`/`block`/`completed_with_block`/None drift) and emit a machine-readable obligation count so R_rel/A_att normalizers work.

### Wave 1 — workflow-reflect lens (proposal)
- T1.1 Compute DCI on the execution-bearing subset only; observe-mode → null.
- T1.2 Surface as **residue flag + per-sigil trend**, always beside `N` and residue-bearing count. Never a standalone "quality dial."
- T1.3 Typed quad {E_energy, R_rel, A_att} with `low-confidence (n<30)` labels on the sparse lanes; the named failing lane titles each workflow-reflect proposal.
- T1.4 `clean-unverified` flag for zero-variance sigils (anti-gaming).

### Wave 2 — readout
- T2.1 DCI trend per sigil over time; a negative window-delta fires the reflection trigger.
- T2.2 DCI-vs-size shown **with the confound warning** (size co-varies with sigil), not as an SCU-curve claim.

## Owner boundary

Proposal only. No edit to canonical `workflow-reflect`/`observability` packages; integration is
a separate owner task. Next route: `workflow-reflect` + `observability-setup`.
