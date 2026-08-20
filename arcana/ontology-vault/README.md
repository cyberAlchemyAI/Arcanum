# Ontology Vault

Ontology Vault is an Arcana sigil for selecting, creating, and maintaining a
governed ontology.

It helps a repository move from scattered notes, sessions, discoveries, premises, and conventions toward a traceable ontology: one where knowledge roles, maturity states, confidence, edge rules, and promotion decisions are explicit.

## Problem It Solves

Knowledge repositories often grow by accumulation. Sessions pile up, discoveries contradict each other, premises become hidden assumptions, and conventions drift from actual use.

Ontology Vault first determines what job the ontology must do. It then maps the
current structure, distills durable content from sessions, reviews falsifiable
premises, separates evidence confidence from commitment confidence, and
proposes convention changes with migration impact.

When a repository has both domain intent and implementation evidence, Ontology Vault can map branch-aware ontology: a business branch, a system branch, and a bridge layer between them.

When an architecture tool needs an ontology to understand enforceable
properties, Ontology Vault instead maps architecture element types, typed
properties, allowed relations, profiles, observation projections, and
explainable findings. That is a different primary job from tracing business
intent into implementation.

## Select The Ontology Type

Ontology Vault maintains a small, product-neutral
[ontology type catalog](catalogs/ontology-types.json). The types are routing
archetypes, not canonical classes or authority decisions.

| Type | Primary modeling job | Derived branch scope |
| --- | --- | --- |
| `knowledge-vault` | Knowledge roles, confidence, premises, sessions, evidence, and conventions. | None |
| `business-domain` | Domain meaning, rules, policies, workflows, outcomes, and value. | `business` |
| `system-runtime` | Components, runtime behavior, data, tests, telemetry, and deployment. | `system` |
| `business-system-bridge` | Realization, traceability, coverage, constraints, gaps, and drift. | `business,system` plus bridge |
| `authority-governance` | Authority kinds, source posture, owners, reliance, gates, and residue. | None |
| `architecture-property` | Architecture types, properties, relations, constraints, profiles, projections, and findings. | `system` |

Use `--ontology-type <id>` for an explicit selection. Clear intent selects one
type without asking. If two or more types remain plausible, Ontology Vault
offers the two or three strongest choices and states what each choice will
model. It must not silently default to a generic map.

A runtime profile may name a project-local type alias, but it must map that
alias to one catalog type. The alias remains local and does not extend Arcanum
vocabulary.

## Use When

- a repository has a `vault/`, `ontology/`, `discovery/`, `premise/`, `axiom/`, `constitution/`, `sessions/`, or similar knowledge-governance area,
- session records need to be distilled into durable claims and decisions,
- premises or working bets need review against evidence,
- confidence promotion or demotion needs explicit gates,
- ontology roles, tags, edge types, or maturity states are drifting,
- delegated research and synthesis findings need traceable links,
- business intent needs traceability to system implementation, tests, telemetry, or runtime constraints,
- an architecture needs a typed property model for profiles, source
  projections, and conformance findings,
- a project has a local ontology surface and needs a repeatable runtime profile
  for map, validation, confidence, drift, projection, or delegated-evidence
  runs before a dedicated runtime exists.

## Do Not Use When

- the repository only needs a lightweight inventory,
- the task is a single glossary or term definition,
- no one is willing to make governance decisions,
- the available evidence is too thin to support promotion or demotion,
- ontology maintenance would distract from urgent implementation.

## Core Concepts

- Knowledge role: what kind of claim a document makes and how it should be challenged.
- Maturity status: how reviewed, tested, or settled the document is.
- Evidence confidence: how much the world or source evidence supports the claim.
- Commitment confidence: how strongly the team is betting on the claim.
- Session record: raw conversation or work history that explains why a decision exists.
- Delegated research: raw evidence from one or more investigators before synthesis.
- Synthesis findings: traceable conclusions drawn from delegated research.
- Convention change: a proposed change to ontology rules, roles, statuses, tags, or edge types.
- Business ontology: domain language, intent, rules, policies, outcomes, user concepts, premises, and value claims.
- System ontology: components, services, APIs, events, jobs, tables, data flows, runtime constraints, metrics, tests, and deployment facts.
- Bridge ontology: cross-branch evidence that connects business intent to system realization, observation, tests, constraints, and drift.
- Architecture property ontology: element types, typed properties, allowed
  relations, constraint operators, profiles, observation projections, and
  explainable expected-versus-observed findings.

## Branch-Aware Authority Model

Business and system ontology branches should be coordinated, not isolated.

| Branch   | Authority                                                                                      | Typical Claims                                                                            |
| -------- | ---------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| Business | Meaning, intent, policy, value, outcome, and domain rules.                                     | What should be true, why it matters, who it affects, and how success is judged.           |
| System   | Implementation, runtime behavior, data shape, technical constraints, tests, and observability. | What exists in the system, how it behaves, where it runs, and how it is measured.         |
| Bridge   | Traceability, realization, coverage, constraints, evidence gaps, and drift.                    | How business claims connect to system artifacts and where alignment is missing or broken. |

The bridge layer is required when a claim asserts alignment between intent and implementation. A system artifact should not silently redefine business meaning, and a business claim should not pretend implementation exists without bridge evidence.

## Branch Edge Types

| Edge Type        | Meaning                                                                           |
| ---------------- | --------------------------------------------------------------------------------- |
| `realized_by`    | A business concept, rule, or behavior is implemented by a system artifact.        |
| `depends_on`     | A business behavior depends on a system capability.                               |
| `constrained_by` | A business rule or outcome is limited by a technical constraint.                  |
| `observed_by`    | A business outcome or behavior is measured by a metric, log, event, or trace.     |
| `tested_by`      | A business claim, rule, or outcome is verified by a test.                         |
| `drifts_from`    | Observed system behavior diverges from business intent.                           |
| `traced_to`      | A system artifact links back to a business premise, decision, discovery, or rule. |

## Output

The sigil can produce:

- ontology map,
- business ontology map,
- system ontology map,
- business-system bridge map,
- ontology drift report,
- traceability matrix,
- session distillation report,
- premise review,
- confidence promotion or demotion report,
- ontology convention change plan,
- ontology type selection receipt,
- architecture property map and profile/projection validation,
- project-local runtime profile validation,
- delegated research record,
- synthesis findings record,
- validation report.

## Project-Local Runtime Profiles

A runtime profile is a local execution boundary for applying Ontology Vault to
one project without turning that project's labels into reusable Arcanum law.

Use a runtime profile when a project has local ontology entries, local owner
routes, source-spine rules, implementation evidence, and allowed/blocked
runtime outputs. The profile names what Ontology Vault may read, what it may
emit, which owner gates control movement, and where residue and observability
go.

The profile also records one cataloged `ontology_type` and may retain one
project-local `ontology_type_alias`. Type selects the model shape; branch
arguments narrow traversal inside that model. Compatible explicit branch
arguments may override derived scope, but they never change the selected type.

Runtime profiles can run inline or through a governed agent backend. Agent
returns are delegated evidence; they can support maps, validation reports,
confidence review, or drift findings, but they do not decide authority.

Runtime profile outputs are non-authority unless an owner route permits the
movement. Blocked outputs include promotion verdicts, spec mutation, canonical
source mutation, runtime conformance verdicts, and generated projection as
authority.

## Run Artifact Or Durable Package

Ontology Vault distinguishes evidence about one run from the ontology a
project intends to keep evolving.

A bounded, single-branch, one-off map may remain one JSON run artifact when it
does not enrich existing ontology state, claim reusable identity, require a
bridge or multiple views, or act as a future state store. This keeps small maps
small.

A package is required as soon as any durable-package trigger is present:

- explicit durable, reusable, evolving, project-owned, or package intent;
- multiple branches or views, or a business-system bridge;
- stable IDs intended to survive the run;
- continued enrichment of existing nodes, relations, operations, sources,
  views, or residue;
- independently validated schemas, source bindings, navigation, or reusable
  projections; or
- a runtime profile mutation against an owned ontology surface.

Count and file size do not decide this. Ownership intent and reuse do.

The minimum package contains a profile, source identities with digests, nodes,
typed relations, residue, a human README or index, schemas or schema bindings,
a deterministic validator, and validation receipts. Branch views and a bridge
view are required when the package makes branch or alignment claims. Imports
from earlier run artifacts require a migration manifest. Load-bearing operation
composition remains an explicit extension rather than being flattened into a
receipt.

If package intent is clear but the package owner, exact root, or required
public/private classification is unresolved, Ontology Vault stops. It may emit
one blocked run receipt with `authority_effect: none`; it must not guess a
directory or append more product ontology state to an earlier invocation JSON.

Package validation is check-only by default. Writing a new validation receipt
is an explicit second action, and earlier receipts remain history.

## Integration

Use [inventory](../inventory/) to persist reusable ontology entries and source summaries.

Use [context-builder](../../transmutations/context-builder/) to prove future tasks can retrieve ontology evidence compactly.

Use [decision-gate](../decision-gate/) when convention changes or confidence promotions require human trade-off decisions.

Use [feature-glossary](../../transmutations/feature-glossary/) when local ontology terms need concise explanation for readers.

Use a repository-local governed subagent strategy when a runtime profile selects
an agent backend. The local strategy owns trigger checks, tension design,
explicit human confirmation, registration, closeout, and ledger evidence.

## Why This Is Arcana

Ontology Vault coordinates long-lived knowledge governance across sources, sessions, evidence, roles, confidence gates, and human decisions. It does not merely transform one artifact; it manages how a repository decides what its knowledge means and when that knowledge is mature enough to rely on.
