# Task CRAFT-RUNTIME-001: Expose Dispatch Spec Command Route

## Objective

Add or repair the bare `dispatch-spec` command route so Refine can resolve it through `tools/arcanum`.

## Layer And Slice

| Field | Value |
| --- | --- |
| Layer | L0 |
| Slice | S-RUNTIME-001 |
| Wave | W0 |
| Complexity | medium |
| Status | completed |

## Source Contracts

- `formulae/dispatch-spec/SKILL.md`
- `formulae/dispatch-spec/scripts/validate-dispatch.py`
- `formulae/dispatch-spec/dispatch.schema.yml`
- `.codex/commands`
- `tools/arcanum`
- `development/craft/CRAFT-RUNTIME-DESIGN.md`

## Dependencies

None.

## Smallest Working Units

### SWU-CRAFT-RUNTIME-001

Goal: make `tools/arcanum --resolve dispatch-spec` pass.

Write scope:

- `.codex/commands/dispatch-spec.md` or the smallest equivalent command-route file.
- Task-session evidence folder.

Implementation detail:

1. Inspect existing command wrappers for source-owner comments and guardrail style.
2. Create a bare `dispatch-spec` command route that points to `formulae/dispatch-spec/SKILL.md` and the validator.
3. Preserve non-promotion wording.
4. Do not duplicate the full dispatch-spec skill body.

Done criteria:

- `tools/arcanum --resolve dispatch-spec` passes.
- Command file names the source owner and validation role.

Validation:

```text
tools/arcanum --resolve dispatch-spec
```

Execution owner: local-fallback.

## Completion Evidence

| Check | Result |
| --- | --- |
| `tools/arcanum --resolve dispatch-spec` | pass: `COMMAND_FILE=.codex/commands/dispatch-spec.md` |
| Source owner named | pass: `.codex/commands/dispatch-spec.md` cites `formulae/dispatch-spec/SKILL.md` and validator |
| Non-promotion guardrail | pass: command file states dispatch-spec validates route shape and does not promote owner artifacts |
| Craft dispatch validator smoke | pass: `python3 formulae/dispatch-spec/scripts/validate-dispatch.py development/craft/refinement-runs/20260529T164919Z-validate-craft/REFINE-DISPATCH.json` |
