# Ontology Vault

Ontology Vault is an Arcana sigil for creating and maintaining a governed knowledge vault.

It helps a repository move from scattered notes, sessions, discoveries, premises, and conventions toward a traceable ontology: one where knowledge roles, maturity states, confidence, edge rules, and promotion decisions are explicit.

## Problem It Solves

Knowledge repositories often grow by accumulation. Sessions pile up, discoveries contradict each other, premises become hidden assumptions, and conventions drift from actual use.

Ontology Vault turns that material into governed knowledge. It maps the current structure, distills durable content from sessions, reviews falsifiable premises, separates evidence confidence from commitment confidence, and proposes convention changes with migration impact.

When a repository has both domain intent and implementation evidence, Ontology Vault can map branch-aware ontology: a business branch, a system branch, and a bridge layer between them.

## Use When

- a repository has a `vault/`, `ontology/`, `discovery/`, `premise/`, `axiom/`, `constitution/`, `sessions/`, or similar knowledge-governance area,
- session records need to be distilled into durable claims and decisions,
- premises or working bets need review against evidence,
- confidence promotion or demotion needs explicit gates,
- ontology roles, tags, edge types, or maturity states are drifting,
- delegated research and synthesis findings need traceable links,
- business intent needs traceability to system implementation, tests, telemetry, or runtime constraints.

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
- delegated research record,
- synthesis findings record,
- validation report.

## Integration

Use [inventory](../inventory/) to persist reusable ontology entries and source summaries.

Use [context-builder](../../transmutations/context-builder/) to prove future tasks can retrieve ontology evidence compactly.

Use [decision-gate](../decision-gate/) when convention changes or confidence promotions require human trade-off decisions.

Use [feature-glossary](../../transmutations/feature-glossary/) when local ontology terms need concise explanation for readers.

## Why This Is Arcana

Ontology Vault coordinates long-lived knowledge governance across sources, sessions, evidence, roles, confidence gates, and human decisions. It does not merely transform one artifact; it manages how a repository decides what its knowledge means and when that knowledge is mature enough to rely on.
