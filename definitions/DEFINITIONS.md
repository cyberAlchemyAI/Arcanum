# Arcanum Canonical Definitions

Status: active
Owner: definitions-governance
Canonical source: `definitions/DEFINITIONS.md`
Lookup index: `definitions/DEFINITIONS-INDEX.md`

## Authority Rule

Only this file defines normative semantics for Arcanum-wide terms it contains.
Downstream artifacts may explain, apply, or reference these terms, but should
not redefine them as global authority.

Feature glossaries, refinement-run glossaries, work-pack glossaries, and
capability-local vocabulary may define local terms. Promote those terms here
only when they are intended to become Arcanum-wide vocabulary.

## DEF-ARC-CONTRACT: Contract

Status: active
Term: contract
Aliases: output contract, mode contract, handoff contract, execution contract,
artifact contract, source contract

### Normative Definition

A contract is an explicit behavioral and authority agreement for an Arcanum
artifact, capability, route, stage, or handoff. It states what the thing
promises, who owns the result, what inputs, outputs, evidence, and boundaries
are required, and what conditions cause pass, flag, block, handoff, deferral,
or rejection.

### Operational Interpretation

Use a contract to decide whether behavior is allowed, whether an artifact
satisfies its obligation, which owner has authority, and when work must stop,
route elsewhere, or produce more evidence.

### Plain-Language Intuition

A contract is the promise around the work: what it is allowed to mean, do,
require, and prove.

### Boundary

A contract may reference a schema, but it is not only field shape. A route,
stage, or artifact does not satisfy its contract merely because a schema
validates; it must also meet the behavioral, ownership, evidence, and boundary
conditions named by the contract.

### Primary Consumers

- `README.md`
- `registry/`
- `framework/`
- `formulae/dispatch-spec/`
- `spells/`
- `arcana/task-session/`
- `arcana/refine/`
- `transmutations/context-builder/`
- `development/craft/`

### Related Definitions

- `DEF-ARC-SCHEMA`

## DEF-ARC-SCHEMA: Schema

Status: active
Term: schema
Aliases: dispatch schema, ledger schema, artifact schema, row-family schema,
YAML schema, JSON Schema

### Normative Definition

A schema is an explicit structural representation of valid artifact, data,
route, ledger, or runtime state. It defines fields, row families, types,
enums, references, cardinality, shape constraints, and parse or validation
rules used to store, exchange, inspect, or validate instances.

### Operational Interpretation

Use a schema to check whether an instance has the required structure. Pair it
with a contract to decide what that structure means, who owns it, and whether
it proves the required behavior.

### Plain-Language Intuition

A schema is the form the evidence must fit.

### Boundary

Schema validation is shape evidence, not execution evidence, promotion
evidence, or authority transfer by itself. A schema can support a contract, but
it does not replace the contract's behavioral and ownership claims.

### Primary Consumers

- `framework/SCHEMA-CONSTITUTION.md`
- `formulae/dispatch-spec/`
- `development/craft/`
- `benchmark/`
- validation scripts and fixtures

### Related Definitions

- `DEF-ARC-CONTRACT`
