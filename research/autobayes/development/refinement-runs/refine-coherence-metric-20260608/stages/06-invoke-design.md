---
stage: 6
name: Invoke Redefine / Design (metric tournament)
capability: invoke
mode: design
pattern: tournament
join: ranked
status: pass
dispatch_id: refine-coherence-metric-20260608
subagent_receipts:
  - role: residue-rate-metric-designer
    agent_id: a7016afdc4ad48f9f
  - role: composite-bundle-metric-designer
    agent_id: a7b55faf20d46bda1
  - role: recomposition-success-metric-designer
    agent_id: a38f7b0585c3bb7fc
---

# Invoke Design — DCI (metric tournament, ranked)

## Pareto comparison

| Candidate | Computability | Interpretability | Gaming-resistance | Verdict |
|---|---|---|---|---|
| A residue-rate | **5/5** (all fields emitted) | 4/5 (bimodal) | objective signals 0.75 weight + hard floor + clean-flag | **backbone** |
| B composite-bundle (E_energy/R_rel/A_att quad) | 2/5 (R_rel/A_att data-starved: 22 gap records) | **5/5** (named fix lane per dip) | hard 40-floor on fail | **presentation layer** |
| C recomposition-success (reopen) | 4/5 | 4/5 | **strongest** — reopen derived from future records, unsuppressable | **discriminator** |

## Ranked decision — a composition, not a single winner

> **DCI = residue-rate backbone (A), with C's same-target reopen term as the key objective
> discriminator, surfaced as B's typed {E_energy, R_rel, A_att} quad for interpretability.**

Rationale grounded in the real store: A is the only fully-computable scalar; B is the most
interpretable but its R_rel/A_att lanes are statistically empty today; C's **reopen detection**
(an earlier record whose `target_artifact` is re-touched in a rework mode within W=5 subsequent
same-target records) is the one signal that converts the dense invoke/task-session/context-builder
sequences into discrimination, and it cannot be gamed by suppressing self-reported gaps.

## The DCI definition (v0)

```
# normalize enum drift first
status_n  = completed|pass|completed_with_block→ok ; partial|flag→partial ; failed|blocked|block|None→fail
r_status  = {ok:0, partial:.5, fail:1}[status_n]
r_qbar    = {pass:0, partial:.4, not_checked:.25, fail:1}[quality_bar_status]
r_drift   = 1 if output_contract_drift else 0
r_reopen  = 1 if same target_artifact re-touched (rework mode) within next 5 same-target records else 0
r_gaps    = clamp(Σ sev_w, 0, 1)   # low .10 med .20 high .35 severe .50  (self-reported, capped)

residue   = min(0.30·r_status + 0.25·r_drift + 0.20·r_reopen + 0.10·r_qbar + 0.15·r_gaps, 1)
DCI(unit) = 100 × (1 − residue)          # objective signals carry 0.75; self-report ≤ 0.15
hard floor: if status_n=fail or qbar=fail → DCI = min(DCI, 40)
report quad: {DCI, E_energy(status+qbar), R_rel(drift+reopen+contract-gaps), A_att(process/approval gaps × files_changed overload)}
```

## Constraints honored (from refine-review + data)

- **Anti-gaming:** objective signals (status, drift, reopen) carry ≥0.75; reopen is unsuppressable; zero-variance sigils tagged `clean-unverified`.
- **Scope:** computed on the **execution-bearing subset** (mode∈new/update/execute or files_changed>0); zero-file observe units → `DCI=null`, not 100, so they don't inflate aggregates.
- **Read as per-sigil trend**, never absolute cross-sigil rank.
- **Honesty:** H_spread is NOT measured (no post-hoc access); DCI is the realized-residue trace.

## Recomposition into the workflow-reflect lens

Per-sigil baseline + N + clean-unverified flag; per-window trend with delta → reflection trigger;
DCI-vs-files_changed curve on the execution subset (rising residue at high file counts = units too
large to decompose coherently). Each flagged failure carries an evidence pointer (the reopening
record's timestamp+mode). Carried to the backtest for falsification on the real store.
