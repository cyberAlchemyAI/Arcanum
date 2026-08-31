# Craft

Craft is an Arcana sigil for maintaining a project-local recursive ledger.

It gives a project a small durable memory for nested development contexts,
blockers, enablers, decisions, gaps, definitions, next moves, route evidence,
and recomposition. The ledger is machine-readable YAML; `CRAFT.md` is the
linked human view.

## Use When

- a project has several active contexts or workstreams;
- blockers, gaps, and decisions need to remain visible across sessions;
- a child context must recompose into a parent before closure;
- route evidence, receipts, and artifacts need row-level traceability;
- a human-readable project status page should be generated from structured
  state.

## Do Not Use When

- a single direct edit would solve the problem;
- there is no durable project state to preserve;
- the user needs global definition authority instead of project-local terms;
- the task is to execute an already bounded implementation slice without
  ledger mutation.

## Storage Model

```text
.craft/
  ledger.yml
  index.json
  artifacts/
CRAFT.md
```

`.craft/ledger.yml` is the source of truth. `CRAFT.md` is a linked human view.
`.craft/index.json`, when present, is a rebuildable machine index derived from
the ledger.

## Canonical Runtime Files

- [SKILL.md](SKILL.md) - executable Craft operating contract.
- [ARCHITECTURE.md](ARCHITECTURE.md) - current architecture baseline for
  comparing proposed Craft changes.
- [templates/ledger.schema.yml](templates/ledger.schema.yml) - first canonical
  ledger schema and compatibility entrypoint.
- [templates/schemas/ledger-core.schema.yml](templates/schemas/ledger-core.schema.yml)
  and [templates/schemas/index.schema.yml](templates/schemas/index.schema.yml)
  - first split schema-stack layer for source ledger rows and indexes.
- [examples/product-launch-ledger.yml](examples/product-launch-ledger.yml) and
  [examples/product-launch-CRAFT.md](examples/product-launch-CRAFT.md) - compact
  product readiness example.
- [examples/platform-governance-ledger.yml](examples/platform-governance-ledger.yml)
  and [examples/platform-governance-CRAFT.md](examples/platform-governance-CRAFT.md)
  - larger governance and adoption-readiness example.

The examples are synthetic public fixtures. They demonstrate Craft row shape,
linking, indexes, blocker refinement, lane-to-role hints, and recomposition
without copying private project state.

Historical promotion evidence remains in [development/craft/](../../development/craft/).

## Link And Index Rule

Craft rows should not be isolated prose islands. Every row has a stable ID, and
human views should render current decisions, blockers, gaps, recomposition, and
artifacts as links. Machine ledgers should include indexes for common access
patterns such as open decisions, active blockers, active gaps, next moves, and
artifacts by path.

## Blocker And Role Rule

Craft blockers are typed before closure. A blocker records its base condition
type, responsibility lane, optional local role fields, closure condition, and
evidence. Lanes name the kind of responsibility needed; roles name local
handlers. Role fields are advisory until backed by an owner policy, decision,
route contract, receipt, or explicit human evidence.

## Tier Fit

Craft belongs in Arcana because it coordinates recursive project state across
human decisions, evidence links, child contexts, blockers, gaps, validation, and
recomposition. It is not a deterministic formatter and not just a one-shot
artifact synthesis.
