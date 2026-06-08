---
profile: autobayes-research
name: TASK-AB-AFK-001 - Subagent Closeout Hardening
description: Selected SWU for hardening subagent lifecycle closeout in Task Session and Dispatch Spec.
type: work-pack-task
task_id: TASK-AB-AFK-001
swu_id: SWU-AB-AFK-001
status: completed
last_updated: 2026-06-07
---

# TASK-AB-AFK-001 - Subagent Closeout Hardening

## Objective

Implement or prototype the minimum hardening needed so future Task Session and Dispatch Spec research runs can prove every spawned subagent was properly joined, closed, blocked, timed out, or carried forward with a handoff.

## Write Scope

Primary implementation scope for the future goal:

- `research/autobayes/work-pack/`
- `research/autobayes/development/refinement-runs/20260607T044519Z-subagent-closeout-hardening/`

Candidate canonical scope only if the goal confirms owner-ready implementation:

- `arcana/task-session/SKILL.md`
- `formulae/dispatch-spec/SKILL.md`
- `formulae/dispatch-spec/dispatch.schema.yml`
- `formulae/dispatch-spec/dispatch.schema.json`
- `formulae/dispatch-spec/scripts/validate-dispatch.py`
- `formulae/dispatch-spec/development/fixtures/`

## Required Design

Create a subagent lifecycle ledger contract with fields:

```text
agent_id
role_id
lane_name
spawn_status
spawn_error
join_status
join_timeout_ms
receipt_artifact
close_status
close_error
residue
reroute
```

Create or propose closeout validation that rejects `PASS` when spawned agents remain open without closeout or continuation handoff.

## Done Criteria

- Lifecycle ledger contract is documented and implemented in Dispatch Spec schema/validator.
- Task Session final report shape includes subagent closeout status.
- Dispatch Spec route/receipt expectations include subagent lifecycle fields when `subagent_strategy` is recommended or required.
- Known closeout cases replay:
  - completed lane plus thread-cap blocked lane is `PASS` with residue and reroute;
  - open agent without handoff is `BLOCK`;
  - timed out or blocked lane is only acceptable with explicit residue and reroute.
- Dispatch validator passes existing fixtures plus newly scoped lifecycle fixtures.

## Validation Surface

At minimum:

```bash
formulae/dispatch-spec/scripts/validate-dispatch.py research/autobayes/development/refinement-runs/20260607T044519Z-subagent-closeout-hardening/REFINE-DISPATCH.json --json
```

If canonical Dispatch Spec files are changed, also run:

```bash
formulae/dispatch-spec/development/run-validation-fixtures.sh
```

If Task Session text is changed, inspect the output contract and anti-patterns for consistency.

## Blockers

Block if:

- write scope would mutate canonical Task Session or Dispatch Spec without explicit owner-ready rationale;
- no validation fixture or evidence replay can demonstrate the closeout gate;
- lifecycle evidence allows a hidden open subagent to pass;
- the goal cannot access both context pack Markdown and JSON index.

## Completion Evidence

- Task Session result: `TASK-AB-AFK-001-RESULT.md`.
- Dispatch Spec fixture suite: `formulae/dispatch-spec/development/run-validation-fixtures.sh` returned `VALIDATION=pass`.
- AutoBayes hardening dispatch: `formulae/dispatch-spec/scripts/validate-dispatch.py research/autobayes/development/refinement-runs/20260607T044519Z-subagent-closeout-hardening/REFINE-DISPATCH.json --json` returned `validation=pass`.
- JSON sanity checks passed for the schema, new lifecycle fixtures, Refine template, and AutoBayes dispatch.
