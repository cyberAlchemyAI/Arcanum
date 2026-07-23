# Native Dispatch Runner — Work Pack

Status: implementation complete and closure verification passed; no lifecycle promotion granted

## Outcome

Implement the first trustworthy `orchestrate execute <dispatch.json>` path: deterministic coordination, one native host driver, fail-closed gates, generated installed surfaces, and causal failure/success evidence.

## Authority

- Behavioral source: `native-dispatch-runner.contract.json`
- Architecture source: `ARCHITECTURE.json`
- Route validation owner: Dispatch Spec
- Runtime owner: Orchestrate
- Execution method: one Task Session per selected SWU
- Promotion: outside this work pack

## Rules

1. Execute SWUs in dependency order, not by file order alone.
2. Do not combine independently acceptable SWUs in one task receipt.
3. Do not spawn native agents from a hand-written parent prompt for integration proof.
4. Preserve historical evidence; corrections are separate adjudication artifacts.
5. Generated installed skill files are not canonical source.
6. Every task closes with machine evidence and a Task Session receipt.

## Tasks

| Task | Purpose | SWUs | Layer | Depends on |
| --- | --- | --- | --- | --- |
| [TASK-NDR-001](work-pack/tasks/TASK-NDR-001.md) | Deterministic coordinator | 001–002 | L0 | none |
| [TASK-NDR-002](work-pack/tasks/TASK-NDR-002.md) | Native Orchestrate driver | 003–005 | L1 | TASK-NDR-001 |
| [TASK-NDR-003](work-pack/tasks/TASK-NDR-003.md) | Canonical source and generated surfaces | 006–007 | L1/L3 | TASK-NDR-002 |
| [TASK-NDR-004](work-pack/tasks/TASK-NDR-004.md) | Failure and evidence hardening | 008–010R | L2 | TASK-NDR-002 |
| [TASK-NDR-005](work-pack/tasks/TASK-NDR-005.md) | Causal canaries and adjudication | 011–013 | L3 | TASK-NDR-003, TASK-NDR-004 |
| [TASK-NDR-VERIFY](work-pack/tasks/TASK-NDR-VERIFY.md) | Closure-only recomposition check | exempt | closeout | TASK-NDR-005 |

## Waves

| Wave | Contents | Exit gate |
| --- | --- | --- |
| [W0](work-pack/waves/W0.md) | Coordinator compiler and reducer | deterministic fixture suite passes |
| [W1](work-pack/waves/W1.md) | Native driver and canonical source generation | installed native driver causally spawns a fixture role |
| [W2](work-pack/waves/W2.md) | Failure and evidence hardening | dependent withholding, event order, and complete native join lifecycle fixtures pass |
| [W3](work-pack/waves/W3.md) | Append-only failure retry, success canary, historical adjudication, closeout | repaired failure retry passes before success and recomposition proof |

## Acceptance

The work pack completes only when:

- `orchestrate execute` is the only manual action needed to start either canary;
- failure withholding is proven before the success route;
- the success route spawns its dependent role exactly once and only after a passing gate;
- events contain native host agent identifiers and precede dependent actions;
- the closeout dispatch passes the canonical validator;
- no artifact claims lifecycle promotion or cross-host parity.

## First Handoff

No implementation Task Session remains. Return the [closure receipt](../runtime-integration/native-dispatch-runner-canary/closeout/receipt.json) to the Orchestrate capability owner only if a separate lifecycle decision is requested.
