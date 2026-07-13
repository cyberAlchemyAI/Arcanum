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

### Scientific/Formal Voice

A contract is an explicit behavioral and authority agreement for an Arcanum
artifact, capability, route, stage, or handoff. It states what the thing
promises, who owns the result, what inputs, outputs, evidence, and boundaries
are required, and what conditions cause pass, flag, block, handoff, deferral,
or rejection.

### Operational Interpretation

Use a contract to decide whether behavior is allowed, whether an artifact
satisfies its obligation, which owner has authority, and when work must stop,
route elsewhere, or produce more evidence.

### Plain-Language Voice

A contract is the promise around the work: what it is allowed to mean, do,
require, and prove.

### Domain Context

In this workspace, contracts appear in sigil `SKILL.md` files, spell mode
contracts, dispatch routes, work-packs, task-session reports, and handoff
artifacts. They are the operating boundary used by Arcanum agents to decide
whether a route may proceed, must block, should defer, or should hand off to a
different owner. The reader-facing `development/user-guide/` material may
explain contracts as part of the Arcanum development loop, but this definition
remains the authority for the Arcanum-wide term.

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

### Scientific/Formal Voice

A schema is an explicit declaration of admissible structure: what kinds of
thing may occur, what relations they may stand in, and what constraints a
well-formed configuration must satisfy. It is stated independently of any
particular occupant, so that conformance can be decided by inspection alone,
without executing the thing, populating it, or interpreting what it means.

### Operational Interpretation

Use a schema to check whether an instance has the required structure. Pair it
with a contract to decide what that structure means, who owns it, and whether
it proves the required behavior.

### Plain-Language Voice

A schema is the form the evidence must fit.

### Domain Context

In this workspace, the things that carry a schema include dispatch routes,
Craft ledgers, artifact frontmatter and metadata, definition indexes, and
generated or runtime-facing structured files. Depending on the carrier, the
declared structure is notated as fields, types, enums, references,
cardinality, row families, or shape constraints; these are notations for
structure, not the definition of it. Schemas give agents a parseable shape to
inspect before a contract decides what that shape means. The Arcanum
user-guide can use schemas as examples of governed structure, but schema
validity is not by itself execution proof, promotion proof, or authority
transfer.

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

## DEF-ARC-GOAL-SPELL: Goal Spell

Status: active
Term: goal spell
Aliases: autonomous goal loop, goal loop, DAG goal loop

### Scientific/Formal Voice

A goal spell is an Arcanum spell that routes a bounded goal over a governed work
graph through frontier reading, risk classification, owner and technique
selection, delegated execution, audit, staged-delta proposal, and
approval-gated promotion.

### Operational Interpretation

Use a goal spell when a goal should advance through existing Arcanum
capabilities while preserving owner boundaries, stop conditions, reviewable
evidence, staged source changes, and explicit approval before protected
mutation.

### Plain-Language Voice

A goal spell is the conductor for a goal: it decides what can run, who should
do it, when to stop, and what must be approved before source truth changes.

### Domain Context

In this workspace, `spells/goal/` is the draft reusable goal spell. Its local
source contract, spec, and package glossary explain goal-specific phases and
handoff artifacts, while this definition provides the Arcanum-wide meaning for
the term.

### Boundary

A goal spell is not a replacement for delegated sigils or spells. It routes to
owners and records evidence; it does not redefine the internal contracts of
`craft`, `dispatch-spec`, `decision-gate`, `task-session`, observability
capabilities, or other delegated owners.

### Primary Consumers

- `spells/goal/`
- `arcana/task-session/`
- `arcana/craft/`
- `formulae/dispatch-spec/`
- `spells/observed-invocation-loop/`
- `arcana/decision-gate/`
- `formulae/observability-setup/`

### Related Definitions

- `DEF-ARC-CONTRACT`
- `DEF-ARC-STAGED-DELTA`
- `DEF-ARC-APPROVAL-TOKEN`

## DEF-ARC-STAGED-DELTA: Staged Delta

Status: active
Term: staged delta
Aliases: proposed delta, staged proposal, proposed ledger delta

### Scientific/Formal Voice

A staged delta is a proposed change to an authoritative source that records the
target, operation, framed diff or equivalent review surface, validation
expectation, and promotion state before any active source-of-truth mutation is
applied.

### Operational Interpretation

Use a staged delta when a capability has evidence for a source change but the
change requires review, approval, validation, or batching before it can mutate
the authoritative artifact.

### Plain-Language Voice

A staged delta is a held change: visible, reviewable, and not yet applied.

### Domain Context

In this workspace, staged deltas are used by the draft `spells/goal/` contract
to keep Craft ledger changes proposal-only until approval. Other Arcanum
capabilities may use the same term when they separate proposal evidence from
active mutation.

### Boundary

A staged delta is not proof that the change is correct or approved. It is review
state. Application still depends on the relevant contract, validation surface,
and approval policy.

### Primary Consumers

- `spells/goal/`
- `arcana/craft/`
- `arcana/task-session/`
- `arcana/decision-gate/`

### Related Definitions

- `DEF-ARC-CONTRACT`
- `DEF-ARC-APPROVAL-TOKEN`

## DEF-ARC-APPROVAL-TOKEN: Approval Token

Status: active
Term: approval token
Aliases: apply token, batch approval token, promotion token

### Scientific/Formal Voice

An approval token is an explicit authorization artifact that binds an approver,
a reviewed batch or operation, a decision record or equivalent durable approval
reference, and an approval state before a protected mutation may execute.

### Operational Interpretation

Use an approval token to decide whether a protected operation may move from
proposal to application. The token should identify exactly what is approved and
which durable record or evidence supports that approval.

### Plain-Language Voice

An approval token is the clear yes for this exact batch that lets a protected
change move from proposal to apply.

### Domain Context

In this workspace, the draft `spells/goal/` contract uses approval tokens for
batch promotion of staged deltas. Decision Gate supplies durable decision
evidence; Craft or another owner applies the approved change according to its
own contract.

### Boundary

An approval token should not be ambient authority. It applies to the named
batch or operation only, and it does not authorize unrelated source mutation,
publication, commits, pushes, parent gitlink movement, or promotion unless those
operations are explicitly included.

### Primary Consumers

- `spells/goal/`
- `arcana/decision-gate/`
- `arcana/craft/`
- `arcana/task-session/`

### Related Definitions

- `DEF-ARC-CONTRACT`
- `DEF-ARC-STAGED-DELTA`

## DEF-ARC-DEVELOPMENT-ARTIFACT: Development Artifact

Status: active
Term: development artifact
Aliases: run artifact, candidate artifact, development package, refinement
artifact, invoke artifact, task-session artifact

### Scientific/Formal Voice

A development artifact is a non-authoritative artifact produced during
exploration, refinement, design, planning, validation, task execution, runtime
observation, or maintenance. It may carry evidence, candidate wording, proposed
structure, validation results, or promotion recommendations, but it does not
define canonical Arcanum behavior, terminology, architecture, registry state, or
artifact policy until an owning promotion route applies a reviewed change to the
target canonical artifact.

### Operational Interpretation

Use a development artifact as source evidence or a proposal input. Before using
its content to change a canonical artifact, resolve the target owner, extract
the smallest durable claim, frame the change as a staged delta or promotion
patch, and run the target artifact's validation and approval gates.

### Plain-Language Voice

A development artifact is working evidence. It can suggest what source truth
should become, but it is not source truth by itself.

### Domain Context

In this workspace, development artifacts commonly live under
`<tier>/<canonical-id>/development/`, `spells/<canonical-id>/development/`,
`development/refinement-runs/`, `development/task-sessions/`, or related
runtime evidence folders. An architecture development artifact can propose an
architecture rule, but the rule becomes authoritative only after it is patched
into the canonical architecture artifact through the owning route.

### Boundary

A development artifact should not be cited as canonical authority just because
it is detailed, validated for its own run, or generated by a trusted capability.
It may remain useful evidence even when the promotion route rejects or narrows
the proposed canonical change.

### Primary Consumers

- `framework/ARTIFACT-CONSTITUTION.md`
- `framework/DEVELOPMENT-TO-CANONICAL-PROMOTION.md`
- `arcana/architecture-pattern-inventory/`
- `arcana/task-session/`
- `arcana/refine/`
- `spells/invoke/`

### Related Definitions

- `DEF-ARC-CANONICAL-ARTIFACT`
- `DEF-ARC-PROMOTION-PATCH`
- `DEF-ARC-STAGED-DELTA`

## DEF-ARC-CANONICAL-ARTIFACT: Canonical Artifact

Status: active
Term: canonical artifact
Aliases: source artifact, source-of-truth artifact, authoritative artifact,
canonical source, promoted artifact

### Scientific/Formal Voice

A canonical artifact is a versioned Arcanum source artifact whose owning
contract gives it authority to define reusable behavior, terminology, process,
architecture, templates, schemas, registry state, validation policy, or other
durable repository semantics for its declared scope.

### Operational Interpretation

Use a canonical artifact to decide the current authoritative rule for its scope.
Mutate it only through the owner route named by its artifact type, adjacent
contract, framework policy, or registry/lifecycle rule. When development
evidence conflicts with a canonical artifact, treat the evidence as a promotion
candidate or drift finding until the canonical artifact is explicitly patched.

### Plain-Language Voice

A canonical artifact is the place the repository agrees to treat as source
truth for a specific kind of work.

### Domain Context

In this workspace, canonical artifacts include files under `arcana/`,
`spells/`, `transmutations/`, `framework/`, `definitions/`, `disciplines/`,
`registry/`, and `tools/` when those files define reusable Arcanum behavior or
policy. Canonical architecture artifacts may be package-level architecture docs,
architecture inventory outputs, or framework architecture standards, depending
on the owner and declared scope.

### Boundary

A canonical artifact is authoritative only for the scope it declares. It does
not inherit unrelated authority from adjacent development folders, generated
runtime surfaces, validation logs, or narrative summaries.

### Primary Consumers

- `framework/ARTIFACT-CONSTITUTION.md`
- `framework/DEVELOPMENT-TO-CANONICAL-PROMOTION.md`
- `definitions/DEFINITIONS.md`
- `registry/`
- `arcana/architecture-pattern-inventory/`

### Related Definitions

- `DEF-ARC-DEVELOPMENT-ARTIFACT`
- `DEF-ARC-PROMOTION-PATCH`
- `DEF-ARC-CONTRACT`

## DEF-ARC-PROMOTION-PATCH: Promotion Patch

Status: active
Term: promotion patch
Aliases: canonicalization patch, development-to-canonical patch, promotion
delta, canonical patch

### Scientific/Formal Voice

A promotion patch is a reviewed mutation to a canonical artifact that derives
from one or more development artifacts or other evidence sources and records
the target canonical artifact, source evidence, owner route, selected durable
claim or structure, transformation rationale, validation expectation, and
approval or rejection state.

### Operational Interpretation

Use a promotion patch when working content should move from development evidence
into canonical source. The patch should normalize the content into the target
artifact's voice and contract, cite the source evidence, update required lookup
or generated surfaces, run validation, and leave rejected or deferred material
behind as development evidence rather than silently carrying it into authority.

### Plain-Language Voice

A promotion patch is the careful move from "this looks right in development" to
"this is now the source rule."

### Domain Context

In this workspace, promotion patches are the process for cases such as applying
architecture development artifact content to a canonical architecture artifact,
promoting a local glossary term into `definitions/DEFINITIONS.md`, or moving a
validated capability change from `development/` into a `SKILL.md`, README,
framework constitution, or registry row.

### Boundary

A promotion patch is not a bulk copy, a commit by itself, or proof that all
source evidence is now canonical. It must name what was selected, what stayed
candidate, which owner accepted the mutation, and which validation passed or
remains blocking.

### Primary Consumers

- `framework/DEVELOPMENT-TO-CANONICAL-PROMOTION.md`
- `framework/ARTIFACT-CONSTITUTION.md`
- `arcana/definitions-governance/`
- `arcana/architecture-pattern-inventory/`
- `arcana/sigil-development/`
- `arcana/spellcraft/`

### Related Definitions

- `DEF-ARC-DEVELOPMENT-ARTIFACT`
- `DEF-ARC-CANONICAL-ARTIFACT`
- `DEF-ARC-STAGED-DELTA`
- `DEF-ARC-APPROVAL-TOKEN`

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

#### Scientific/Formal Voice

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

#### Plain-Language Voice

This is the allowed concept-type vocabulary. Profile-specific counts keep
baseline and extended semantics from being mixed in evidence reports.

#### Domain Context

In this workspace, DS-D1 types are used by DomainSpec concept registries,
`definitions/TAXONOMY.md`, and definitions-governance concept-registry
aggregation. Feature-local concepts should use these meta-types for typed
analysis, but new local vocabulary remains package-local until
definitions-governance promotes it.

### DS-D2: Typed Relationship System

#### Scientific/Formal Voice

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

#### Plain-Language Voice

This is the allowed relationship-verb vocabulary, grouped by backend, UI, and
cross-layer role, with optional cross-feature relations for composition-heavy
analyses.

#### Domain Context

In this workspace, DS-D2 relation verbs are explained by
`definitions/RELATIONSHIPS.md` and used by DomainSpec concept graphs, registry
aggregation, and integration-style analysis. The `contracts` relationship verb
is a DomainSpec typed edge and is distinct from `DEF-ARC-CONTRACT`.

**Canon boundary.** The canonical vocabulary is exactly the 25-type / 29-edge composition-extension profile above, as shipped in `TAXONOMY.md` and `RELATIONSHIPS.md`. No larger edge or category extension is adopted; any such proposal is deferred design rationale, not canonical vocabulary.

### DS-D3: Concept Graph

#### Scientific/Formal Voice

A feature-level concept graph is:

$$
G = (V, E, \tau, \lambda)
$$

where $V$ is concept vertices, $E \subseteq V \times V$ is directed edges, $\tau: V \rightarrow \mathcal{M}$ is meta-type assignment, and $\lambda: E \rightarrow \mathcal{R}$ is edge-type assignment.

#### Plain-Language Voice

A feature is modeled as a typed graph: nodes are concepts, edges are
relationships, and both carry explicit semantics.

#### Domain Context

In this workspace, concept graphs are the bridge between feature-level
DomainSpec artifacts and higher-level governance checks. They let agents audit
whether a feature's concepts and relationships follow DS-D1 and DS-D2 before
those concepts are reused by inventories, integration specs, or downstream
planning.

### DS-D7: Edge-Family Partition

#### Scientific/Formal Voice

Relationship families are disjoint:

$$
\mathcal{R} = \mathcal{R}_B \uplus \mathcal{R}_U \uplus \mathcal{R}_X
$$

and in composition-enabled analyses may extend to $\mathcal{R}^{+} = \mathcal{R} \uplus \mathcal{R}_{CF}$.

#### Plain-Language Voice

Each edge family has one semantic home. Optional cross-feature edges are
explicit extensions, not hidden overloads of the base vocabulary.

#### Domain Context

In this workspace, edge-family partitioning prevents backend, UI, cross-layer,
and cross-feature relationship meanings from collapsing into one ambiguous
edge list. It is used when DomainSpec examples, relationship catalogs, and
concept-registry aggregation need to explain why an edge belongs to one family
rather than another.

### DS-D8: Edge-Signature Operator

#### Scientific/Formal Voice

Let $\sigma: \mathcal{R} \rightarrow \mathcal{P}(\mathcal{M}) \times \mathcal{P}(\mathcal{M})$. A typed edge instance $e=(u,r,v)$ is valid iff:

$$
\tau(u) \in \pi_1(\sigma(r)) \land \tau(v) \in \pi_2(\sigma(r))
$$

#### Plain-Language Voice

Relation typing behaves like a graph type-checker: the source and target
concept types must fit the declared signature for the selected relationship.

#### Domain Context

In this workspace, DS-D8 is the validation rule behind concept-graph and
concept-registry edge checks. It is the reason definitions-governance
aggregation should reject an edge whose endpoint meta-types do not match the
declared DomainSpec relationship signature.

### DS-D10: Coverage-Status Taxonomy

#### Scientific/Formal Voice

Concept mapping status: `covered`, `strained`, `uncovered`. Edge modeling status: `works`, `strained`, `broken`. Cross-experiment synthesis must preserve these vocabularies without relabeling.

#### Plain-Language Voice

Fixed status vocabularies keep evidence comparable across experiments and
reruns.

#### Domain Context

In this workspace, DS-D10 status labels are used when DomainSpec coverage
experiments, concept mapping, and edge modeling need comparable evidence. They
help later reviewers distinguish a missing concept, a strained mapping, and a
broken relationship without inventing new status words in every report.

### DS-P1: Type Safety Property

#### Scientific/Formal Voice

All edge instances satisfy signature constraints (no relation may connect concept types that violate the declared signature).

#### Plain-Language Voice

No relationship may connect two concept types that its declared signature does
not allow.

#### Domain Context

In this workspace, DS-P1 is the acceptance property for DomainSpec typed
graphs and concept-registry aggregation. A feature graph that violates DS-P1
should be flagged before its relationships are reused as planning or
integration evidence.

### DS-P2: Backend/UI Partition Property

#### Scientific/Formal Voice

$\mathcal{M}_B \cap \mathcal{M}_U = \emptyset$ for the selected profile. Backend and UI type sets are intentionally non-overlapping to reduce ambiguity.

#### Plain-Language Voice

Backend types and UI types are separate buckets. A concept should not count as
both under the same profile.

#### Domain Context

In this workspace, DS-P2 helps DomainSpec feature artifacts and audits keep
backend model terms separate from UI projection terms. That separation is what
lets later guides, inventories, and implementation plans talk about backend
behavior and UI behavior without silently merging their meanings.

### DS-P3: Cross-Layer Direction Property

#### Scientific/Formal Voice

Edges in $\mathcal{R}_X$ are directed UI → backend. Cross-layer interactions use a single directional semantics for consistency.

#### Plain-Language Voice

Cross-layer edges point from UI concepts toward the backend concepts they
fetch, mutate, reflect, derive from, contract with, or mirror.

#### Domain Context

In this workspace, DS-P3 keeps DomainSpec cross-layer analysis directional:
UI artifacts may depend on, reflect, or invoke backend concepts, but the edge
vocabulary should not imply that backend domain concepts are authored by UI
views. This protects guide, integration, and planning artifacts from reversing
ownership when they explain UI/backend relationships.
