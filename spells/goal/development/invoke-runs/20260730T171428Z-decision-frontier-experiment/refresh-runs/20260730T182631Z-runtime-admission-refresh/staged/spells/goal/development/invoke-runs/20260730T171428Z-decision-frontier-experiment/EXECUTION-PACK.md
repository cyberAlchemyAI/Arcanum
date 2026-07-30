---
artifact: goal-decision-frontier-experiment-execution-pack
status: blocked-until-selection
selected_swu: none
---

# Execution Pack

## Choreography

```text
Spellcraft accepts experiment boundary
  -> user selects exactly one eligible SWU
  -> Context Builder creates selection-bound pack
  -> Task Session captures exact baseline
  -> bounded mutation and validation
  -> terminal Task Session receipt
  -> Invoke Refresh closeout under the Spellcraft lifecycle boundary
  -> one successor may become eligible
```

## Serial Wave Graph

```text
W0 baseline
  -> W1 contract
  -> W2 reducer
  -> W3 claim
  -> W4 reconcile
  -> W5 HITL stop
  -> W6 Way Clear
  -> W7 execution non-collapse
  -> W8 closure
  -> W9 readiness
```

There is no parallel mutation wave because every implementation unit consumes
shared contract state.

## Admission

| Gate | Current state |
| --- | --- |
| Define | pass |
| Design denominator | pass |
| Design selection | pass, fixed point |
| Plan structure | pass |
| Spellcraft acceptance | pending |
| selected SWU | none |
| execution | blocked |

## Runtime Context Contract

After explicit selection, Context Builder must include:

- the selected task file and exact SWU subsection;
- shared context, decisions, gaps, traceability, and closeout contract;
- predecessor Invoke Refresh closeout receipts;
- exact source and target inventory;
- validation commands and evidence paths;
- unrelated worktree changes scoped away.

It must not include later SWUs as executable authority.

## Stop Conditions

Stop on ambiguous selection, missing predecessor receipt, digest drift,
undeclared target, non-L0 request while L0 is incomplete, canonical write,
private/public boundary risk, failed witness, or missing owner closeout.
