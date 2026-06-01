# Stage 3: Interrogation Refine Review

## Verdict

`flag`

## Critique

The define stage is directionally correct but needs sharper boundaries.

## Questions

1. Is this a refine-only runtime or an Arcanum-wide runtime?
2. Does the async handoff own execution status, or only execution intent?
3. How much adapter detail belongs in the generic handoff?
4. How are multiple loops represented without turning `RUN-MANIFEST.md` into an unstructured log?
5. Should `tools/arcanum --exec` be replaced or wrapped?

## Findings

- This must be Arcanum-wide infrastructure, not refine-only. Refine and task-session are first consumers.
- The async handoff should own intent and safety boundaries, not live execution state.
- Execution state belongs in `RUN.json`, `STATUS.json`, and `events.jsonl`.
- Adapter-specific data must be recorded under an adapter block, not in top-level generic fields.
- `tools/arcanum --exec` should become a compatibility wrapper over the runtime executor.

## Risks

- Renaming everything away from Codex Goal in one pass could break existing validation fixtures.
- A too-large generic schema could delay the immediate fix.
- If parent/child run identity is optional, nested refine loops will become hard to validate.

## Required Repair

The design must define a minimal v1 schema, a compatibility path for `tools/arcanum --exec`, and a clear multi-loop topology.
