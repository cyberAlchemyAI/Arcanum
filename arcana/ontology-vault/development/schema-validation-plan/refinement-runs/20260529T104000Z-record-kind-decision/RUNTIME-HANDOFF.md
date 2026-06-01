# Runtime Handoff: Record Kind Schema Gap

Status: local-dry-run
Run id: `20260529T104000Z-record-kind-decision`

## Objective

Refine the `record_kind` schema gap discovered by branch-aware ontology schema validation and recommend the next route before JSON Schema generation.

## Dispatch Reference

`REFINE-DISPATCH.json`

## Runtime Adapter

No model-backed runtime delegation is requested.

Stage command evidence uses:

```bash
tools/arcanum --exec --adapter dry-run --output <stage-output> <command> <request>
```

## Blocked Fields

- `dispatch-spec` command surface is not installed as an Arcanum command.

Mitigation:

- `REFINE-DISPATCH.json` is validated directly against `formulae/dispatch-spec/dispatch.schema.json` using `python3` and `jsonschema`.

## Boundary

No source schema mutation happens in this run.
