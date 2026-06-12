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
- [templates/ledger.schema.yml](templates/ledger.schema.yml) - first canonical
  ledger schema.
- [examples/body-war-ledger.yml](examples/body-war-ledger.yml) and
  [examples/body-war-CRAFT.md](examples/body-war-CRAFT.md) - small product MVP
  readiness example.
- [examples/goldenquill-ledger.yml](examples/goldenquill-ledger.yml) and
  [examples/goldenquill-CRAFT.md](examples/goldenquill-CRAFT.md) - larger
  governance and architecture-readiness example.

Historical promotion evidence remains in [development/craft/](../../development/craft/).

## Link And Index Rule

Craft rows should not be isolated prose islands. Every row has a stable ID, and
human views should render current decisions, blockers, gaps, recomposition, and
artifacts as links. Machine ledgers should include indexes for common access
patterns such as open decisions, active blockers, active gaps, next moves, and
artifacts by path.

## Tier Fit

Craft belongs in Arcana because it coordinates recursive project state across
human decisions, evidence links, child contexts, blockers, gaps, validation, and
recomposition. It is not a deterministic formatter and not just a one-shot
artifact synthesis.
