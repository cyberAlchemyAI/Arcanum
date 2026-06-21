---
module: discipline-governance-promotion
version: current
status: draft
updatedAt: 2026-06-21
docType: implementation-layering
---

# Implementation Layering: discipline-governance → promotion threshold

Decision-first layering to move the sigil from v0.2.0 (3 executions, manual reflection) to the next promotion bar: ≥5 meaningful executions accrued through `experiment-harness`, the two reflection-named SKILL iterations applied, a **threshold-triggered** (not manual) reflection, and a validation surface for the routed constitutions.

## Source Contract

- Reflection report: [../reflection-report-20260621.md](../reflection-report-20260621.md) (names the two v0.2.x SKILL iterations)
- Harness report: [../EXPERIMENT-HARNESS-REPORT.md](../EXPERIMENT-HARNESS-REPORT.md) (3/3 regimes; gaps = telemetry auto-emit, execution count, constitution validators)
- Sigil contract: [../../SKILL.md](../../SKILL.md) (v0.2.0)

## Target And Scope

- Target: `discipline-governance` sigil promotion readiness
- Scope: sigil lifecycle (owned by sigil-development; harness mechanics owned by experiment-harness)
- Current state: v0.2.0, partially implemented (harness exists, telemetry manual, reflection manual)

## Layer Decision Table

| Layer | Decision Question | Minimum Working Unit | Included Scope | Deferred Scope | Exit Evidence | Promotion Decision |
| --- | --- | --- | --- | --- | --- | --- |
| **L0** | After this, do the two reflection-named SKILL iterations hold? | SKILL updated: (a) `scan`/`route` tag each candidate `public-safe \| private-parent` + target catalog; (b) `validate` requires `active-pattern` to cite evidence outside the owning sigil. | both SKILL edits + a fixture each | new executions; validators | SKILL diff + 1 fixture per rule passes | continue / revise |
| **L1** | After this, do executions auto-emit and reach ≥5? | `experiment-harness --profile sigil-development` initialized; post-run telemetry hook wired; 2+ new examples run (exec #4, #5) exercising the new rules. | harness scaffold, hook, examples #4-#5 | threshold reflection | telemetry jsonl ≥5 lines emitted automatically; harness `VALIDATION=pass` | continue / harden |
| **L2** | After this, does a threshold-triggered reflection confirm readiness? | reflection at the 5-execution threshold (trigger = `usage-threshold`, not manual) → patterns + promotion decision. | reflection report v2 | constitution validators | reflection trigger=`usage-threshold`; decision recorded | promote / iterate |
| **L3** | After this, can the routed disciplines reach canonical? | a deterministic validator for the receipt-id-legend constitution (and the gitignore ignore-policy check). | `tools/` validators; raise rules `review`→`deterministic` | further disciplines | validator runs in CI; constitutions cite it | canonical / hold |

## Non Regression Guardrails

- Later layers preserve the boundary the audit proved (sigil recommends routes, never promotes cross-owner knowledge).
- The 5-execution count must be genuine meaningful executions (real formalize/route/validate/deprecate runs), not padded reruns.
- Telemetry stays local + gitignored (observability discipline); only the harness/reflection summaries are tracked.

## Recommended Next Layer

- Next layer: **L0** (apply the two SKILL iterations — smallest change, unblocks honest harness runs).
- Key decision unlocked: are the reflection-named contract changes correct before accruing executions against them.
- Major deferred scope: constitution validators (L3).
