# Arcanum Definitions Index

Status: active
Canonical source: [DEFINITIONS.md](DEFINITIONS.md)

## Terms

| ID | Term | Status | Canonical section | Plain-language intuition |
| --- | --- | --- | --- | --- |
| DEF-ARC-CONTRACT | contract | active | [Contract](DEFINITIONS.md#def-arc-contract-contract) | The promise around the work: what it is allowed to mean, do, require, and prove. |
| DEF-ARC-SCHEMA | schema | active | [Schema](DEFINITIONS.md#def-arc-schema-schema) | The form the evidence must fit. |
| DEF-ARC-GOAL-SPELL | goal spell | active | [Goal Spell](DEFINITIONS.md#def-arc-goal-spell-goal-spell) | The conductor for a goal: what can run, who owns it, when to stop, and what needs approval. |
| DEF-ARC-STAGED-DELTA | staged delta | active | [Staged Delta](DEFINITIONS.md#def-arc-staged-delta-staged-delta) | A held change: visible, reviewable, and not yet applied. |
| DEF-ARC-APPROVAL-TOKEN | approval token | active | [Approval Token](DEFINITIONS.md#def-arc-approval-token-approval-token) | The clear yes for this exact batch that lets a protected change apply. |
| DS-D1 | meta-type system | active | [DS-D1](DEFINITIONS.md#ds-d1-meta-type-system) | The allowed concept-type vocabulary (25 backend + 11 UI types). |
| DS-D2 | typed relationship system | active | [DS-D2](DEFINITIONS.md#ds-d2-typed-relationship-system) | The allowed relationship verbs (29 edges), partitioned by layer role. |
| DS-D3 | concept graph | active | [DS-D3](DEFINITIONS.md#ds-d3-concept-graph) | Every feature is a typed graph of nodes and edges. |
| DS-D7 | edge-family partition | active | [DS-D7](DEFINITIONS.md#ds-d7-edge-family-partition) | Each edge family has a unique semantic home. |
| DS-D8 | edge-signature operator | active | [DS-D8](DEFINITIONS.md#ds-d8-edge-signature-operator) | Relation typing as a graph type-checker. |
| DS-D10 | coverage-status taxonomy | active | [DS-D10](DEFINITIONS.md#ds-d10-coverage-status-taxonomy) | Fixed status vocabularies keep evidence comparable. |
| DS-P1 | type safety property | active | [DS-P1](DEFINITIONS.md#ds-p1-type-safety-property) | No relation may connect types that violate the signature. |
| DS-P2 | backend/UI partition property | active | [DS-P2](DEFINITIONS.md#ds-p2-backendui-partition-property) | Backend and UI type sets are non-overlapping. |
| DS-P3 | cross-layer direction property | active | [DS-P3](DEFINITIONS.md#ds-p3-cross-layer-direction-property) | Cross-layer edges are directed UI → backend. |

## Alias Lookup

| Alias | Definition ID |
| --- | --- |
| artifact contract | DEF-ARC-CONTRACT |
| apply token | DEF-ARC-APPROVAL-TOKEN |
| autonomous goal loop | DEF-ARC-GOAL-SPELL |
| batch approval token | DEF-ARC-APPROVAL-TOKEN |
| DAG goal loop | DEF-ARC-GOAL-SPELL |
| dispatch schema | DEF-ARC-SCHEMA |
| execution contract | DEF-ARC-CONTRACT |
| goal loop | DEF-ARC-GOAL-SPELL |
| handoff contract | DEF-ARC-CONTRACT |
| JSON Schema | DEF-ARC-SCHEMA |
| ledger schema | DEF-ARC-SCHEMA |
| mode contract | DEF-ARC-CONTRACT |
| output contract | DEF-ARC-CONTRACT |
| proposed delta | DEF-ARC-STAGED-DELTA |
| proposed ledger delta | DEF-ARC-STAGED-DELTA |
| promotion token | DEF-ARC-APPROVAL-TOKEN |
| row-family schema | DEF-ARC-SCHEMA |
| source contract | DEF-ARC-CONTRACT |
| staged proposal | DEF-ARC-STAGED-DELTA |
| YAML schema | DEF-ARC-SCHEMA |

## Governance Notes

- Use `definitions-governance` to add, revise, or audit Arcanum-wide terms.
- Every canonical definition should carry scientific/formal, plain-language, and
  domain-context voices in the canonical source.
- Keep capability-local glossaries local until a term is intentionally promoted.
- Link to definition IDs from downstream artifacts when a term carries authority.
