# Native Dispatch Runner — Execution Pack

Status: prepared; execution authorization required

## Start Command

Use Task Session on one SWU at a time, beginning with:

```text
task-session work-pack/tasks/TASK-NDR-001.md SWU-NDR-001
```

The exact host invocation syntax may vary; the selected task file and SWU identifier must remain explicit.

## Preconditions

- canonical Dispatch Spec validator passes `execution.dispatch.json`;
- worktree changes outside the selected SWU write scope are preserved;
- the Task Session records baseline status before mutation;
- user execution authorization is present;
- implementation does not treat this Markdown file as a machine command source.

## Per-SWU Receipt

Every SWU returns:

```json
{
  "task_id": "TASK-NDR-...",
  "swu_id": "SWU-NDR-...",
  "status": "pass|fail|blocked",
  "changed_paths": [],
  "validation_commands": [],
  "validation_result": "pass|fail|not-run",
  "evidence": [],
  "residue": [],
  "next_swu": "SWU-NDR-...|none"
}
```

## Execution Gates

| Gate | Required evidence | On failure |
| --- | --- | --- |
| G0 route | Dispatch validator receipt | block all work |
| G1 L0 | deterministic action/reducer fixtures | do not build native driver |
| G2 L1 | host-bound spawn/join receipts | do not claim native integration |
| G3 L2 | withholding, recovery, and event-order fixtures | do not run success canary |
| G4 failure canary | zero dependent spawns after non-pass | block success canary |
| G5 success canary | dependent spawn exactly once after pass | block closeout |
| G6 closeout | validator pass + recomposition receipt | finish, without promotion claim |

## Evidence Standard

Accept concrete JSON/JSONL paths, deterministic command output, host action identifiers, and validator receipts. Do not accept a prose assertion that a native agent ran, or receipts synthesized after bespoke parent calls, as causal integration proof.

## Recovery

If a native wave partially spawns, the driver must stop new actions, join or interrupt every known host identifier, persist residue, and close blocked. If the driver loses its evidence store, the run is not replayed automatically; it is blocked for explicit recovery.

## Closeout

`TASK-NDR-VERIFY` checks the contract-to-evidence trace, runs deterministic validation, confirms failure-first order, and produces the final Task Session receipt. It may not add implementation behavior.
