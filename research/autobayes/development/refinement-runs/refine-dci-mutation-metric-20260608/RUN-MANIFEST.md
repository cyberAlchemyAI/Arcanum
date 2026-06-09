---
profile: refine
run_id: refine-dci-mutation-metric-20260608
type: run-manifest
status: flag
preset: full
research_mode: no-research
dispatch_validation: pass
subagent_authorization: approved
last_updated: 2026-06-08
---

# Run Manifest — refine-dci-mutation-metric-20260608

## Target

DCI as a skill-mutation regression differential — does it make sense, and is it detectable?

## Owned artifacts

- [REFINE-SEED-PROPOSAL.md](REFINE-SEED-PROPOSAL.md)
- [REFINE-DISPATCH.json](REFINE-DISPATCH.json) — validation `pass`
- [RUNTIME-HANDOFF.md](RUNTIME-HANDOFF.md)
- [RESULT.md](RESULT.md)
- [evidence-index.json](evidence-index.json)

## Stage receipts

| Stage | Capability | Receipt | Status |
|---|---|---|---|
| 1 Context baseline | context-builder | frame (in 02) | pass |
| 2 Invoke Define | invoke | [stages/02-invoke-define.md](stages/02-invoke-define.md) | pass |
| 3 Interrogation refine-review | interrogation | [stages/03-interrogation-refine-review.md](stages/03-interrogation-refine-review.md) | flag |
| 4 Research decision | refine | [stages/04-research-decision.md](stages/04-research-decision.md) | pass |
| 5 Distill select | distill | [stages/05-distill-select.md](stages/05-distill-select.md) | pass |
| 6 Invoke Design (tournament) | invoke + 3 subagents | [stages/06-invoke-design.md](stages/06-invoke-design.md) | pass |
| 7 Interrogation design-review | interrogation | [stages/07-interrogation-design-review.md](stages/07-interrogation-design-review.md) | flag |
| 8 Distill Repair (power analysis) | distill + 1 subagent | [stages/08-distill-repair-power-analysis.md](stages/08-distill-repair-power-analysis.md) | flag |
| 9 Invoke Plan | invoke | [stages/09-invoke-plan.md](stages/09-invoke-plan.md) | pass |
| 10 Final synthesis | interrogation + refine | [RESULT.md](RESULT.md) | flag |

## Subagent receipts

| Role | Agent ID | Stage | Join | Close |
|---|---|---|---|---|
| ground-truth-differential-designer | a54a80b356cb7e580 | 6 | completed | closed |
| harness-replay-designer | ac9826efa8fa68769 | 6 | completed | closed |
| live-version-slice-designer | a867a73e0b434f714 | 6 | completed | closed |
| power-analysis-reviewer | a0121922320a9c34e | 8 | completed | closed |

## Final status

`flag` — the differential makes sense conceptually (observer-independent rework anchor + paired test),
but is **underpowered on incidental telemetry** (gross-regression-only canary); a per-skill replay
corpus is the buyable fix. Next: `observability-setup`, `experiment-harness`, `sigil-development`.
