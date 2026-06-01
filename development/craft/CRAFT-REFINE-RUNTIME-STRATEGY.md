# Craft Refine Runtime Strategy

## Status

Candidate strategy, based on failed command-backed refine attempts during Craft recursive-ledger development.

## Problem

The current command-backed refine strategy is not working for this local development shape.

Observed evidence:

| Run | Command Path | Result |
| --- | --- | --- |
| `CRAFT-REFINE-001` | `tools/arcanum --exec refine development/craft/WORK-PACK.md --task CRAFT-REFINE-001` | timed out after 600 seconds, no output artifact |
| `CRAFT-REFINE-002` | `tools/arcanum --exec refine development/craft/WORK-PACK.md --task CRAFT-REFINE-002` | timed out after 300 seconds, no output artifact |

Both tasks were completed successfully only after Codex treated them as bounded local skill work from the work-pack contract.

The failure is not in the target artifacts. The failure is in the runtime topology:

```text
model-backed refine command
  -> tries to orchestrate more model-backed command stages
  -> stalls or times out before useful artifacts are produced
```

## Strategy Shift

Use an orchestrator-first runtime.

The orchestrator owns:

- target resolution,
- run folder creation,
- stage plan,
- evidence index,
- task state,
- artifact collection,
- final synthesis,
- timeout and blocked-stage accounting.

Each refine step runs as a bounded worker:

- a subagent when the runtime supports subagents,
- a direct skill invocation in Codex or CI when subagents are not available,
- a local fallback worker when the stage is small and deterministic enough.

The orchestrator should not ask a model-backed refine process to recursively spawn another model-backed refine process.

## Runtime Shape

Recommended topology:

```text
Refine Orchestrator
  -> Context Builder worker
  -> Invoke Define worker
  -> Interrogation worker
  -> Distill worker
  -> Invoke Design worker
  -> Interrogation worker
  -> Distill Repair worker
  -> Invoke Plan worker
  -> Final Synthesis worker
```

Each worker receives:

- the selected stage objective,
- source artifact paths,
- write scope,
- expected output path,
- acceptance criteria,
- timeout,
- blocked return contract.

Each worker returns:

```yaml
stage_id: <stage>
result: pass | flag | block | timeout
artifact_path: <path-or-null>
files_touched:
  - <path>
validation:
  - <check>
blockers:
  - <blocker-or-none>
handoff_note: <summary for orchestrator>
```

## CI Skill-Direct Mode

For CI, prefer skill-direct execution over recursive command-backed execution.

CI should call the relevant skill or deterministic local script for each stage directly, with the orchestrator providing the stage contract and collecting artifacts.

Example:

```text
ci-refine-orchestrator
  stage invoke-define -> run invoke skill contract
  stage interrogation -> run interrogation skill contract
  stage distill -> run distill skill contract
```

This avoids:

- Codex-inside-Codex recursion,
- long opaque command timeouts,
- missing intermediate artifacts,
- unclear ownership between refine and stage capabilities.

## Policy

1. Refine is an orchestrator, not a monolithic model-backed command.
2. The orchestrator may use subagents, skill-direct calls, or local fallback workers.
3. Every stage must have an output artifact or blocked reason.
4. A stage timeout must be recorded as a stage result, not allowed to consume the whole run invisibly.
5. CI should prefer skill-direct stage execution.
6. `tools/arcanum --exec refine ...` should be reserved for a root orchestrator that dispatches stages itself, not for nested model orchestration.
7. For small work-pack tasks, direct skill execution is valid when the canonical command path is unavailable or repeatedly timing out, as long as the blocked runtime evidence is recorded.

## Implication For Craft

Craft's recursive ledger should model this runtime shape explicitly:

- the orchestrator is a context,
- each stage is a child context or typed item,
- stage blockers must pass through `blocker_refiner`,
- stage workers can be assigned by `type + lane -> role`,
- CI can consume the same ledger as a stage contract.

## Proposed Next Work

Create a follow-up work-pack or patch plan for `arcana/refine`:

| Task | Outcome |
| --- | --- |
| REFINE-RUNTIME-001 | Define orchestrator/worker stage contract in refine docs. |
| REFINE-RUNTIME-002 | Add CI skill-direct mode to refine runtime strategy. |
| REFINE-RUNTIME-003 | Add timeout handling and blocked-stage artifact requirements. |
| REFINE-RUNTIME-004 | Validate against Craft refinement runs as regression examples. |

## Gate

- Status: `flag`
- Reason: The strategy is supported by local failure evidence, but canonical `arcana/refine` mutation should happen through a dedicated refine runtime work-pack or explicit approval.
