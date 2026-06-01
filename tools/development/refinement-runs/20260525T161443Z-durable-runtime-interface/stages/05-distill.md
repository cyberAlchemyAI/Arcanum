# Stage 5: Distill

## Verdict

`pass`

## Selected Coherent Unit

Design and implement a **Durable Runtime Run Contract** as shared Arcanum infrastructure.

## Rejected Alternatives

- **Keep Codex Goal as canonical runtime**: rejected because the user explicitly removed `/goal` from the model and because current command execution already shows adapter-level fragility.
- **Patch refine only**: rejected because task-session has the same delegation problem.
- **Make context-builder own runtime handoff**: rejected because context-builder owns evidence baseline, not execution.
- **Build a scheduler first**: rejected because durable handoff/status folders are enough for v1 async semantics.

## Distilled Architecture

V1 should include:

- `RUNTIME-HANDOFF.md` as the generic handoff artifact.
- `.arcanum/runtime/runs/<run-id>/` as the durable executor run folder.
- `tools/arcanum-runtime-run` as the shared runtime executor.
- `codex-exec` as the first adapter.
- `tools/arcanum --exec` as a compatibility wrapper that delegates into the runtime executor.

## Distilled Validation Rule

Every non-blocked runtime-backed stage must have:

- parent run id when applicable,
- run id,
- adapter id,
- command or skill target,
- resolved command file when command-backed,
- input handoff path,
- output artifact path,
- status,
- verdict.
