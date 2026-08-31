# WORK-PACK: Lifecycle Source Laboratory

Machine source: `lifecycle-source-laboratory-plan-v1` (`invoke.plan-execution-source.v1`).

## Objective

Implement canonical fixture contracts, a disposable lifecycle runner, and an adversarial integration matrix that continuously prove the installed schema-first planning workflow.

## Execution frontier

| Unit | Dependencies | Producer | Writes |
| --- | --- | --- | --- |
| `SWU-LSL-001` | none | `task-session:swu-lsl-001` | development/lifecycle-source-laboratory/FIXTURE-CONTRACT.json, development/lifecycle-source-laboratory/VALIDATE-FIXTURE.py, development/lifecycle-source-laboratory/RECEIPT-SWU-LSL-001.json |
| `SWU-LSL-002` | SWU-LSL-001 | `task-session:swu-lsl-002` | development/lifecycle-source-laboratory/DISPOSABLE-RUNNER.py, development/lifecycle-source-laboratory/VALIDATE-RUNNER.py, development/lifecycle-source-laboratory/RECEIPT-SWU-LSL-002.json |
| `SWU-LSL-003` | SWU-LSL-002 | `task-session:swu-lsl-003` | development/lifecycle-source-laboratory/ADVERSARIAL-MATRIX.json, development/lifecycle-source-laboratory/TEST-INTEGRATION.py, development/lifecycle-source-laboratory/RECEIPT-SWU-LSL-003.json |

## Boundary

This derived view grants no selection, admission, execution, publication, deployment, or external-effect authority.
