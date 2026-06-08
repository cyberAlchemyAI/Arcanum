---
profile: autobayes-research
name: Context Pack - TASK-AB-AFK-001
description: Strict context handoff pack for Codex goal execution of subagent closeout hardening.
type: context-pack
task_id: TASK-AB-AFK-001
swu_id: SWU-AB-AFK-001
strict_coverage: pass
last_updated: 2026-06-07
---

# Context Pack - TASK-AB-AFK-001

## Selected Unit

- Work-pack: [WORK-PACK.md](../WORK-PACK.md)
- Task: [TASK-AB-AFK-001-subagent-closeout-hardening.md](../tasks/TASK-AB-AFK-001-subagent-closeout-hardening.md)
- SWU: `SWU-AB-AFK-001`

## Objective

Harden subagent lifecycle closeout so mostly-AFK research goals can rely on Task Session and Dispatch Spec to prove every subagent lane was joined, closed, blocked, timed out, or safely handed off.

## Controlling Evidence

- [task-session-autobayes-full-mode-result.md](../../sessions/task-session-autobayes-full-mode-result.md): earlier fanout with thread-cap residue.
- [task-session-autobayes-all-possible-subagents-result.md](../../sessions/task-session-autobayes-all-possible-subagents-result.md): six spawned lanes completed; seventh blocked by thread cap.
- [full-mode-source-receipts.md](../../sessions/full-mode-source-receipts.md): completed receipt ledger.
- [REFINE-SEED-PROPOSAL.md](../../development/refinement-runs/20260607T044519Z-subagent-closeout-hardening/REFINE-SEED-PROPOSAL.md): refinement seed.
- [Invoke Plan](../../development/refinement-runs/20260607T044519Z-subagent-closeout-hardening/stages/09-invoke-plan.md): non-executed plan.

## Hard Constraints

- Pack-first execution: read this context and its JSON index before implementing.
- Keep local research artifacts separate from canonical Arcanum mutations unless the goal explicitly justifies owner-ready implementation.
- Every subagent lifecycle status must be explicit.
- Hidden open subagents must block success.
- Thread-cap failures may pass only as named residue with reroute.
- Canonical Dispatch Spec schema/validator changes require fixture validation.

## Write Boundaries

Safe first write scope:

- `research/autobayes/work-pack/`
- `research/autobayes/development/refinement-runs/20260607T044519Z-subagent-closeout-hardening/`

Conditional canonical write scope:

- `arcana/task-session/SKILL.md`
- `formulae/dispatch-spec/SKILL.md`
- `formulae/dispatch-spec/dispatch.schema.yml`
- `formulae/dispatch-spec/dispatch.schema.json`
- `formulae/dispatch-spec/scripts/validate-dispatch.py`
- `formulae/dispatch-spec/development/fixtures/`

## Validation

Required:

```bash
formulae/dispatch-spec/scripts/validate-dispatch.py research/autobayes/development/refinement-runs/20260607T044519Z-subagent-closeout-hardening/REFINE-DISPATCH.json --json
```

Conditional:

```bash
formulae/dispatch-spec/development/run-validation-fixtures.sh
```

## Fallback Exploration

Named gaps only:

- exact schema shape for adding subagent lifecycle fields;
- exact Task Session wording if output-contract edits are needed;
- fixture shape if validator changes are made.

Every extra source used must be reported with the gap that justified it.

