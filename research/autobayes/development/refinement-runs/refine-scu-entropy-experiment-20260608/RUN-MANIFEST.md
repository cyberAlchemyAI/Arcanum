---
profile: refine
run_id: refine-scu-entropy-experiment-20260608
type: run-manifest
status: pass
preset: full
research_mode: no-research
dispatch_validation: pass
subagent_authorization: approved
last_updated: 2026-06-08
---

# Run Manifest — refine-scu-entropy-experiment-20260608

## Target

Residue R3 from the Craft entropy search: instrument an entropy proxy so the SCU U-curve
becomes a measured, falsifiable claim.

## Owned artifacts

- [REFINE-SEED-PROPOSAL.md](REFINE-SEED-PROPOSAL.md)
- [REFINE-DISPATCH.json](REFINE-DISPATCH.json) — dispatch-spec validation `pass`
- [RUNTIME-HANDOFF.md](RUNTIME-HANDOFF.md)
- [RESULT.md](RESULT.md)
- [evidence-index.json](evidence-index.json)

## Stage receipts

| Stage | Capability | Handle | Receipt | Status |
|---|---|---|---|---|
| 1 Context baseline | context-builder | native (parent) | stages/01-context-baseline (frame in 02) | pass |
| 2 Invoke Define | invoke | native (parent) | [stages/02-invoke-define.md](stages/02-invoke-define.md) | pass |
| 3 Interrogation refine-review | interrogation | native (parent) | [stages/03-interrogation-refine-review.md](stages/03-interrogation-refine-review.md) | flag |
| 4 Research decision | refine | native (parent) | [stages/04-research-decision.md](stages/04-research-decision.md) | pass |
| 5 Distill select | distill | native (parent) | [stages/05-distill-select.md](stages/05-distill-select.md) | pass |
| 6 Invoke Design (tournament) | invoke | 3 subagents | [stages/06-invoke-design.md](stages/06-invoke-design.md) | pass |
| 7 Interrogation design-review | interrogation | native (parent) | [stages/07-interrogation-design-review.md](stages/07-interrogation-design-review.md) | flag |
| 8 Distill Repair (pilot) | distill | 1 subagent | [stages/08-distill-repair-pilot.md](stages/08-distill-repair-pilot.md) | pass |
| 9 Invoke Plan | invoke | native (parent) | [stages/09-invoke-plan.md](stages/09-invoke-plan.md) | pass |
| 10 Final synthesis | interrogation + refine | native (parent) | [RESULT.md](RESULT.md) | pass |

## Subagent receipts (delegated stages)

| Role | Agent ID | Stage | Join | Close |
|---|---|---|---|---|
| proxy-A-semantic-entropy-designer | a6a30a1d4da026afb | 6 | completed | closed |
| proxy-B-mdl-description-length-designer | a0b98eeab5d253d40 | 6 | completed | closed |
| proxy-C-residue-rate-designer | a974d9e386b43c115 | 6 | completed | closed |
| falsification-pilot-reviewer | a8166a0fc7630867c | 8 | completed | closed |

## Research

- Mode `research-if-gap-appears` → resolved to `no-research`; no external gap triggered.

## Final status

`pass` — falsifiable, pre-registered, pilot-scoped experiment design produced; handoff to
`experiment-harness` prepared; no Craft-definition edit. Next: `experiment-harness`, then
`decision-gate` on R1.
