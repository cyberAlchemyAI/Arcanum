# Runtime Handoff

## Runtime Boundary

- Runtime: `arcanum-runtime`
- Adapter: `native-skill | codex-skill | claude-skill | copilot-instructions | dry-run | explicit legacy codex-exec | <adapter>`
- Owner: `refine`
- Status: `pass | flag | block | not_run`
- Runtime run folder: `.arcanum/runtime/runs/<run-id> | <blocked reason>`

## Runtime Objective

Run the canonical Refine loop for `<target>` using parent-owned native runtime dispatch and produce `RESULT.md`.

## Dispatch Route

- Dispatch route: `REFINE-DISPATCH.json`
- Dispatch schema: `formulae/dispatch-spec/dispatch.schema.yml`
- Dispatch validation: `pass | flag | block`
- Dispatch ID: `<dispatch_id>`
- Technique catalog: `formulae/dispatch-spec/TECHNIQUE-CATALOG.md`
- Technique overlays: `<selected overlay ids>`

## Stage Dispatch Contract

```bash
tools/arcanum --resolve <command>
tools/arcanum --exec --adapter native-skill --output <stage-output> <command> <stage-request>
```

Native adapters produce handoff/receipt contracts and must not spawn nested model-backed CLIs. Legacy model CLI adapters require explicit operator selection.

## Handoff Requirements

- Context Builder handoff pack: `<path or blocked reason>`
- Handoff index: `<path or blocked reason>`
- Strict coverage: `pass | block`
- Runtime adapter profile: `<path or blocked reason>`
- Runtime status: `pass | flag | block | not_run`
- Dispatch route validation: `pass | flag | block`
- Run manifest: `RUN-MANIFEST.md`
- Evidence index: `evidence-index.json`

## Blocked Fields

- `<field>`: `<reason>`
