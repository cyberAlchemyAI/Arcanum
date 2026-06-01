# Runtime Adapter Design Transport

## Source Inputs

- `INVOKE-DEFINE.md`
- `INVOKE-DESIGN.md`
- `ARCHITECTURE-BUNDLE.md`
- `RUNTIME-SCHEMAS.md`
- `EXECUTION-PACK.md`
- `RUNTIME-ADAPTER-INTERROGATION-REVIEW.md`
- `RUNTIME-ADAPTER-DISTILL-REVIEW.md`
- `tools/arcanum`

## Produced Outputs

- `RUNTIME-ADAPTER-PATTERN.md`
- `CODEX-RUNTIME-ADAPTER-DESIGN.md`
- `ADAPTER-CONTRACT-DECISIONS.md`
- `RUNTIME-ADAPTER-DESIGN-TRANSPORT.md`

## Design Decision

New runtimes are added as adapters behind the durable runner. Each adapter must declare its properties, execution layers, state/isolation rules, translator behavior, result contract, and validation surface.

The refreshed contract adds adapter profile evidence, runner-owned event logs, adapter-owned status classification, and validation grades.

## Codex Explanation

Codex is used through `codex-exec`:

```text
RUNTIME-HANDOFF.md -> tools/arcanum-runtime-run --adapter codex-exec -> codex exec
```

Codex receives translated handoff prompts, runs with per-run `CODEX_HOME`, and returns normalized runtime evidence. It does not own Arcanum orchestration or native `/goal` state.

## Next Route

Refresh `WORK-PACK.md` and `IMPLEMENTATION-LAYERING.md` so `codex-exec` implementation depends on `ADAPTER-CONTRACT-DECISIONS.md`.
