Blocked by the execution environment before I could start task zero.

Every local command invocation fails with:

```text
bubblewrap is unavailable: no system bwrap was found on PATH and no bundled codex-resources/bwrap binary was found next to the Codex executable
```

Because sandbox approval is disabled for this session, I can’t bypass that runner failure. That prevents me from reading `.codex/commands/refine.md`, running `tools/arcanum` stage dispatch, inspecting the existing refinement folder, or updating `RUN-MANIFEST.md`, `evidence-index.json`, `GOAL-HANDOFF.md`, `RESULT.md`, and `stages/` artifacts.

Once the runner has `bwrap` available or the session is started with a working command sandbox, I can continue from the first required step.