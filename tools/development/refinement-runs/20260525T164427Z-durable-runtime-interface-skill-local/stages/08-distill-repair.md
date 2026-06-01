# Stage 8: Distill Repair

## Verdict

`pass`

## Repair Focus

Clarify how `tools/arcanum --exec` should relate to the new runtime runner.

## Repaired Interface

`tools/arcanum` should keep:

- `--list`
- `--resolve`
- prompt generation
- command metadata detection
- observability envelope compatibility

`tools/arcanum` should stop owning:

- Codex home preparation,
- direct `codex exec`,
- process execution lifecycle,
- runtime state.

For `--exec`, it should:

1. resolve the command,
2. build the Arcanum command prompt as today,
3. write a generated runtime handoff,
4. call `tools/arcanum-runtime-run`,
5. link/copy runtime `RESULT.md` to `--output`,
6. emit the same command summary fields for compatibility.

## Repaired First Slice

Implement `tools/arcanum-runtime-run --adapter dry-run` first, then migrate `tools/arcanum --exec` behind a feature flag:

```bash
ARCANUM_RUNTIME_RUNNER=1 tools/arcanum --exec --output <path> <command> <request>
```

Once fixtures pass, make runtime runner the default path.
