---
profile: autobayes-research
name: AutoBayes Research Work Pack
description: Work pack for making AutoBayes research subagent fanout safe and closing the remaining learning research.
type: work-pack
status: active
last_updated: 2026-06-07
---

# AutoBayes Research Work Pack

## Objective

Harden AutoBayes research execution so broad subagent fanout can run mostly AFK while preserving Task Session and Dispatch Spec evidence quality, then close the remaining learning research into source-backed definitions, glossary, distilled knowledge, bridge decisions, and residue.

## SWU Manifest

| SWU | Status | Task | Objective | Dependencies | Validation |
| --- | --- | --- | --- | --- | --- |
| `SWU-AB-AFK-001` | completed | [TASK-AB-AFK-001](tasks/TASK-AB-AFK-001-subagent-closeout-hardening.md) | Add subagent lifecycle closeout hardening artifacts and validation expectations. | AutoBayes subagent task-session evidence exists. | Dispatch validation plus lifecycle ledger fixture/replay evidence. |
| `SWU-AB-LEARN-001` | completed | [TASK-AB-LEARN-001](tasks/TASK-AB-LEARN-001-research-closure.md) | Close the remaining AutoBayes learning research into a final source-backed operator pack. | `SWU-AB-AFK-001` completed; current research tower exists. | Dispatch validation, source/gate audit, and final artifact read-back. |

## Source Contracts

- [task-session-autobayes-full-mode-result.md](../sessions/task-session-autobayes-full-mode-result.md)
- [task-session-autobayes-all-possible-subagents-result.md](../sessions/task-session-autobayes-all-possible-subagents-result.md)
- [autobayes-research.dispatch.json](../autobayes-research.dispatch.json)
- [REFINE-DISPATCH.json](../development/refinement-runs/20260607T044519Z-subagent-closeout-hardening/REFINE-DISPATCH.json)
- [Invoke Plan](../development/refinement-runs/20260607T044519Z-subagent-closeout-hardening/stages/09-invoke-plan.md)
- [Closure Invoke Plan](../development/refinement-runs/20260607T070805Z-research-closure-plan/stages/09-invoke-plan.md)

## Completion Policy

The work-pack is complete when the selected SWU has:

- bounded canonical write scope;
- explicit subagent lifecycle receipt schema;
- Task Session closeout report language;
- Dispatch Spec receipt/gate expectations;
- validation evidence replaying the known AutoBayes fanout cases;
- no silent canonical promotion without owner review.
