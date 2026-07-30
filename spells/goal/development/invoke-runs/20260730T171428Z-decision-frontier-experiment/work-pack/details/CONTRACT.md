# Implementation Detail: Contract And Graph Validation

## Purpose And Decision

Own the admission boundary for every experiment document. The validator
decides only whether bytes are structurally and graph-semantically valid; it
does not compute a frontier or mutate state.

## Inputs And Outputs

Inputs:

- UTF-8 JSON for decision map, frontier, claim, resolution, reconciliation, or
  Way Clear documents;
- the exact versioned schema for that document kind.

Output:

```text
validation_receipt {
  status: pass | block
  input_sha256
  schema_version
  diagnostics[code, selector]
}
```

No domain output is emitted on `block`.

## Data And State

- Node IDs are non-empty stable identifiers and unique within one map.
- Edges are directed `blocker_id -> blocked_id` pairs.
- Node states and route values are closed enums from the schema.
- The validator is pure; only its receipt file is written by the harness.

## Algorithm

```text
parse UTF-8 JSON
if parse fails: block JSON_INVALID
validate closed schema and schema_version
if schema fails: block SCHEMA_INVALID with stable selector

if document is a decision map:
  build node_by_id; reject duplicate IDs
  for each edge in lexical pair order:
    reject self-edge
    reject duplicate pair
    reject unknown blocker or blocked endpoint
  run Kahn topological sort with lexical ready queue
  if visited_count != node_count: block GRAPH_CYCLE

canonicalize accepted input
emit pass receipt bound to canonical input SHA-256
```

Diagnostic precedence is JSON, schema, duplicate identity, edge integrity,
then cycle. Multiple same-level diagnostics sort by code and selector.

## Edge Cases And Failure Modes

- Empty node set is valid only when a non-empty destination remains.
- Disconnected DAG components are valid.
- Duplicate edges block rather than deduplicate.
- A self-edge is both invalid and cyclic but reports `SELF_EDGE` first.
- Unknown states/routes block; they never downgrade to fog.
- A failed validation must leave no partial domain output or rewritten fixture.

## Acceptance

DFE-FIX-003 supplies cycle, duplicate-ID, unknown-endpoint, invalid-state, and
invalid-route mutants. Each must fail with stable diagnostics before a
frontier or claim file appears. Positive fixtures must yield byte-identical
receipts on replay.

