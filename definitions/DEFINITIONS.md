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

## DomainSpec Definitions (wedge)

> Canonical, machine-checkable definitions of the **DomainSpec** domain-modeling
> vocabulary — the open-core methodology surface. The formal `DS-*` IDs below are
> the source of truth; `TAXONOMY.md` and `RELATIONSHIPS.md` are the prose example
> layer that points here.
>
> **Term boundary:** the DomainSpec meta-type and edge vocabulary (Entity, Mapping,
> Adapter, `contracts` edge, …) is domain-modeling vocabulary and is distinct from the
> Arcanum-native governance terms `DEF-ARC-CONTRACT` / `DEF-ARC-SCHEMA` above. Where a
> word coincides (e.g. the `contracts` relationship verb), the DomainSpec meaning is the
> typed graph-edge, not the Arcanum authority agreement.

### DS-D1: Meta-Type System

Let:

$$
\mathcal{M} = \mathcal{M}_B \cup \mathcal{M}_U
$$

Canonical composition-extension profile (25 backend types):

$$
\mathcal{M}_B = \{Entity, ValueObject, Enum, Operation, Query, Calculation, Rule, Policy, Workflow, Interface, Event, Mapping, StateMachine, Saga\}
$$

$$
\mathcal{M}_U = \{Page, Layout, Component, ViewModel, Hook, Form, Action, Guard, Binding, Adapter, StateIndicator\}
$$

(A 24-type pre-composition baseline — `\mathcal{M}_B` without `Saga` — exists historically; the canonical profile is the 25-type set above. Report profile-specific counts explicitly in evidence.)

Intuition: this defines the allowed concept-type vocabulary; profile-specific counts avoid mixing baseline and extended semantics in evidence reports.

### DS-D2: Typed Relationship System

Let:

$$
\mathcal{R} = \mathcal{R}_B \cup \mathcal{R}_U \cup \mathcal{R}_X
$$

$$
\mathcal{R}_B = \{performs, produces, enforces, calculates, transitions, exposes, orchestrates, applies, maps, contains, queries, emits\}
$$

$$
\mathcal{R}_U = \{renders, wraps, composes, consumes, submits, shapes, protects, displays\}
$$

$$
\mathcal{R}_X = \{fetches, mutates, reflects, derives, contracts, mirrors\}
$$

Canonical composition-extension profile (29 edges) adds cross-feature relations:

$$
\mathcal{R}_{CF} = \{produces\text{-}for, triggers\text{-}cross, enforces\text{-}cross\}
$$

$$
\mathcal{R}^{29} = \mathcal{R}_B \cup \mathcal{R}_U \cup \mathcal{R}_X \cup \mathcal{R}_{CF}
$$

Intuition: this defines the allowed relationship verbs, partitioned by layer role, with optional cross-feature relations for composition-heavy analyses.

**Canon boundary.** The canonical vocabulary is exactly the 25-type / 29-edge composition-extension profile above, as shipped in `TAXONOMY.md` and `RELATIONSHIPS.md`. No larger edge or category extension is adopted; any such proposal is deferred design rationale, not canonical vocabulary.

### DS-D3: Concept Graph

A feature-level concept graph is:

$$
G = (V, E, \tau, \lambda)
$$

where $V$ is concept vertices, $E \subseteq V \times V$ is directed edges, $\tau: V \rightarrow \mathcal{M}$ is meta-type assignment, and $\lambda: E \rightarrow \mathcal{R}$ is edge-type assignment.

Intuition: every feature is modeled as a typed graph where both nodes and edges carry explicit semantics.

### DS-D7: Edge-Family Partition

Relationship families are disjoint:

$$
\mathcal{R} = \mathcal{R}_B \uplus \mathcal{R}_U \uplus \mathcal{R}_X
$$

and in composition-enabled analyses may extend to $\mathcal{R}^{+} = \mathcal{R} \uplus \mathcal{R}_{CF}$.

Intuition: each edge family has a unique semantic home; optional cross-feature edges are explicit extensions, not implicit overloads.

### DS-D8: Edge-Signature Operator

Let $\sigma: \mathcal{R} \rightarrow \mathcal{P}(\mathcal{M}) \times \mathcal{P}(\mathcal{M})$. A typed edge instance $e=(u,r,v)$ is valid iff:

$$
\tau(u) \in \pi_1(\sigma(r)) \land \tau(v) \in \pi_2(\sigma(r))
$$

Intuition: relation typing behaves like a graph type-checker: source and target types must satisfy the edge signature contract.

### DS-D10: Coverage-Status Taxonomy

Concept mapping status: `covered`, `strained`, `uncovered`. Edge modeling status: `works`, `strained`, `broken`. Cross-experiment synthesis must preserve these vocabularies without relabeling.

Intuition: fixed status vocabularies keep evidence comparable across experiments and reruns.

### DS-P1: Type Safety Property

All edge instances satisfy signature constraints (no relation may connect concept types that violate the declared signature).

### DS-P2: Backend/UI Partition Property

$\mathcal{M}_B \cap \mathcal{M}_U = \emptyset$ for the selected profile. Backend and UI type sets are intentionally non-overlapping to reduce ambiguity.

### DS-P3: Cross-Layer Direction Property

Edges in $\mathcal{R}_X$ are directed UI → backend. Cross-layer interactions use a single directional semantics for consistency.
