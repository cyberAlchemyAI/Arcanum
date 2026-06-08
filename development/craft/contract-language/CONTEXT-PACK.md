# Contract Language Context Pack

Context Builder mode: deep
Strict coverage: pass
Handoff type: new-lifecycle-thread
Target folder: `development/craft/contract-language/`

## Task

Create a new language for writing formal contracts that can be validated. The
language should be based on the Craft distinction between contract, schema, and
iteration.

## Obligations

| ID | Obligation | Coverage |
| --- | --- | --- |
| O1 | Explain contract vs schema as separate but linked artifact kinds. | covered |
| O2 | Preserve Craft rule that contracts express behavior, ownership, invariants, and boundaries. | covered |
| O3 | Preserve schema role as shape, enums, row families, references, and validation rules. | covered |
| O4 | Include iteration: examples, validation, residue, recomposition, and versioned changes. | covered |
| O5 | Seed a formal contract language that can itself be validated. | covered |
| O6 | Keep this as a new lifecycle thread, not an implementation. | covered |

## Selected Evidence

### `development/craft/CRAFT-INTERFACE.md`

Why selected: primary example of a behavioral contract.

Selectors:

- `## Purpose`
- `## Storage Contract`
- `## Method Contract`
- method sections such as `start_project`, `add_blocker`, `validate`,
  `recompose`, and `export_ledger`

Obligations: O1, O2, O4.

Key evidence:

- The contract says `.craft/ledger.yml` is source of truth and `CRAFT.md` is a
  human-readable view.
- Each method has inputs, writes, returns, and invariants.
- Contract-level rules include raw blockers cannot resolve directly,
  definitions remain local, and closure requires recomposition.

### `development/craft/CRAFT-INTERFACE-LEDGER-SCHEMA.yml`

Why selected: primary example of the schema representation beneath a contract.

Selectors:

- `source_of_truth_policy`
- `enums`
- `row_families`
- `interface_methods`
- `validation_rules`

Obligations: O1, O3, O5.

Key evidence:

- The schema names row families: `descriptions`, `definitions`, and `gaps`.
- It uses enums for statuses, severities, and treatments.
- It gives validation rule ids such as `CI-R001` through `CI-R007`.

### `development/craft/CRAFT-INTERACTION-CONTRACT.md`

Why selected: example of a contract that defines inter-artifact authority.

Selectors:

- `## Purpose`
- `## Interaction Methods`
- `## Capability Contracts`
- `## Closure Rule`

Obligations: O2, O4, O5.

Key evidence:

- Craft owns route memory and recursive ledger state.
- Called capabilities own native artifact contracts, validation, and verdicts.
- Methods such as `prepare_handoff`, `receive_receipt`, `apply_receipt`, and
  `open_residue` show how a contract can express lifecycle behavior.

### `development/craft/CRAFT-INTERACTION-LEDGER-SCHEMA.yml`

Why selected: example of validating interaction contracts structurally.

Selectors:

- `capability_ref`
- `route_handoffs`
- `receipts`
- `route_events`
- `validation_rules`

Obligations: O3, O5.

Key evidence:

- Handoffs, receipts, and route events become row families.
- Validation rules block owner-boundary violations, blocked receipts closing
  contexts, and dispatch evidence being treated as execution evidence.

### `development/craft/CRAFT-INTERFACE-EXAMPLE.yml`

Why selected: fixture showing contract and schema in use.

Selectors:

- `contexts`
- `definitions`
- `gaps`
- `typed_items`
- `decisions`
- `relations`
- `recomposition`

Obligations: O4, O5.

Key evidence:

- A root context and child context demonstrate recursive structure.
- The example shows a blocker, enabler, decision, gap, definition, next move,
  and recomposition evidence.

### `development/craft/CRAFT-INTERACTION-EXAMPLE.yml`

Why selected: fixture showing interaction contract validation concepts.

Selectors:

- `route_handoffs`
- `receipts`
- `route_events`
- `relations`
- `gaps`
- `recomposition`

Obligations: O4, O5.

Key evidence:

- It separates Invoke plan evidence, Dispatch Spec route-shape evidence, Task
  Session execution evidence, and Decision Gate decision evidence.
- It shows receipt application and recomposition as distinct events.

### `development/craft/CRAFT-INTERFACE-VALIDATION.md`

Why selected: validation style for a contract/schema pair.

Selectors:

- `## Method Coverage`
- `## Schema Review`
- `## Example Review`
- `## Hard Gate Review`

Obligations: O4, O5.

Key evidence:

- Validation checks methods, schema row families, examples, and hard gates.
- The validation result vocabulary is `pass`, `flag`, and `block`.

### `development/craft/CRAFT-INTERACTION-VALIDATION.md`

Why selected: validation style for interaction contracts.

Selectors:

- `## Method Coverage`
- `## Capability Contract Coverage`
- `## Schema Review`
- `## Fixture Review`
- `## Hard Gate Review`

Obligations: O2, O4, O5.

Key evidence:

- Capability contracts are validated separately from schema rows.
- Owner-boundary behavior is a first-class validation target.

### `formulae/dispatch-spec/dispatch.schema.yml`

Why selected: Arcanum example of a validateable route language.

Selectors:

- top-level `required`
- `properties.intent`
- `properties.mode`
- `properties.technique_overlays`
- `properties.subagent_strategy`

Obligations: O3, O5.

Key evidence:

- It shows how route documents become validateable through JSON Schema style
  required fields, enums, nested objects, and validation expectations.

### `spells/invoke/handoff.md`

Why selected: target handoff pattern.

Selectors:

- `## Purpose`
- `## Handoff Types`
- `## Context Builder Policy`
- `## Output Contract`

Obligations: O6.

Key evidence:

- New work should start as a `new-lifecycle-thread`.
- Context Builder should select obligation-linked context instead of copying a
  whole session.

## Inferences

- A formal contract language should likely have two layers:
  - a contract grammar for behavior, ownership, methods, invariants, gates, and
    lifecycle clauses;
  - a schema/validator model for checking contract completeness, references,
    and examples.
- The language should require examples or fixtures, because Craft validation
  relies on examples to prove contract/schema meaning.
- The first lifecycle should be `invoke define`, not parser implementation.

## Gaps For The New Project

- No grammar has been selected.
- No parser or validator runtime has been selected.
- No canonical contract schema exists yet.
- It is undecided whether the language should be YAML-native, Markdown-native
  with structured blocks, or its own DSL.

These are definition-stage decisions for the next lifecycle.

## Excluded Context

- Full Refine run internals: excluded because this handoff is about contract
  language design, not Refine execution.
- Runtime command-surface history: excluded because parser/runtime choices are
  not selected yet.
- Promotion readiness: excluded because the new language is only a project seed.
