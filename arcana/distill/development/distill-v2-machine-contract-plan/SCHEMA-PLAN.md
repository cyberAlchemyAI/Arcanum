# Distill v2 Machine Contract — Schema Plan

## Design Rule

The smallest coherent contract is not five documents. It is eight reusable
schemas whose concrete instances recompose into one exact Standard run:

```text
common primitives
  -> mode instance + technique instances
  -> profile (exact references only)
  -> source RunFrame
  -> append-only semantic trace
  -> substantive result
  -> deterministic Markdown projection
  -> exact stage receipt
```

Mode and Technique specs are independent because a mode changes orchestration
shape while a technique changes a local check. The profile composes them; it
must not embed private copies that can drift.

## Canonical Schema Candidates

These are plan targets, not accepted paths or authored schemas.

| Order | Candidate path | Owns | Must not own |
| --- | --- | --- | --- |
| 1 | `arcana/distill/schemas/distill-common-v2.schema.json` | IDs, digests, repository-relative exact refs, bounded counts, enums shared across the family. | Mode or result policy. |
| 2 | `arcana/distill/schemas/distill-mode-spec-v2.schema.json` | Mode identity, finite tracks/rounds, role policy, pitch-off, gates, closeout policy. | Technique definitions or verdicts. |
| 3 | `arcana/distill/schemas/distill-technique-spec-v2.schema.json` | Stable technique identity, type, hooks, activation, allowed inputs, emitted trace, pass/flag/block behavior. | Run budgets or concept state mutation. |
| 4 | `arcana/distill/schemas/distill-profile-v2.schema.json` | Exact mode/technique refs, profile version, objection categories, output-contract version, bounded override policy. | Embedded ModeSpec or TechniqueSpec copies. |
| 5 | `arcana/distill/schemas/distill-source-v2.schema.json` | Full RunFrame: seed, target context, objective/output pair, optimization goal, constraints, discovery, artifacts, lineage, exact profile/mode refs, evidence context. | Runtime evidence conclusions or a pre-authored verdict. |
| 6 | `arcana/distill/schemas/distill-trace-event-v2.schema.json` | Append-only setup, proposal, objection, reconciliation, technique, round, termination, and verdict-candidate events. | Mutable summaries or owner decisions. |
| 7 | `arcana/distill/schemas/distill-result-v2.schema.json` | Complete substantive ResultEnvelope, conditional verdict/route rules, navigation, deferred complexity, and `authority_effect: none`. | Invoke admission or mutation authority. |
| 8 | `arcana/distill/schemas/distill-stage-receipt-v2.schema.json` | Producer/finalizer identity, schema digests, exact artifact inventory, validation state, atomic publication status, receipt digest method. | Substantive reasoning not already present in trace/result. |

All schemas use JSON Schema Draft 2020-12, closed objects by default, explicit
`$id`, and exact `$ref` closure validated from the repository checkout.

## Machine Instances

### Modes

Five independent instances live under `arcana/distill/profiles/v2/modes/`:

- `compact.json`
- `standard.json`
- `tournament.json`
- `deep.json`
- `validate.json`

Every instance fixes finite minimum/default/maximum track and round bounds. No
`unbounded`, omitted maximum, or free-form role policy is permitted.

### Techniques

Eleven independent instances live under
`arcana/distill/profiles/v2/techniques/` using the canonical underscore IDs:

- `abstraction_level_guard`
- `recomposition_proof`
- `evolution_profile`
- `frame_expiry_note`
- `cognitive_load_check`
- `requisite_variety_check`
- `boundary_object_check`
- `concept_vs_knowledge_status`
- `premortem_pass`
- `set_based_tournament`
- `navigable_result_check`

The core profile lives at
`arcana/distill/profiles/v2/distill-core-profile-v2.json` and contains exact
references to these instances. Historical hyphenated adapter labels are mapped
only by a separately versioned compatibility projection if that route is
selected.

## Input Contract

The source is the executable semantic input, not an Invoke request wrapper. Its
minimum required surface is:

| Group | Required content |
| --- | --- |
| Identity | source ID, contract version, run ID, creation time, invocation source. |
| Intent | seed point, target context, objective, output artifact, optimization goal. |
| Policy | exact profile ref, exact mode ref, requested technique refs, finite override values when allowed. |
| Discovery | provided evidence, searched sources, blocker unknowns, non-blocker unknowns, assumptions. |
| Constraints | governance, cost, time, quality, domain, stop-rule tightening. |
| Artifacts | repository-relative path, SHA-256, `size_bytes`, semantic role; no absolute path, traversal, or URI. |
| Lineage | parent run/source when present and a reason for any objective/output-artifact revision. |
| Evidence context | optional exact runtime evidence refs and status; never a source of substantive verdict authority. |

The positive Standard fixture must exercise every required group. Negative
fixtures must prove that an Invoke-shaped request with missing RunFrame fields
is rejected even when it is valid against the old adapter schema.

## Cross-Artifact Invariants

JSON Schema is necessary but insufficient. The deterministic semantic validator
must additionally prove:

1. Every exact ref matches path, SHA-256, and `size_bytes`.
2. Source mode and technique refs resolve to the exact profile snapshot.
3. Every trace event has one run ID, monotonic sequence, valid predecessor, and
   a hook allowed by the referenced technique.
4. Role, track, and round events remain within the selected mode budget.
5. Always-required techniques run; conditional techniques run or record a valid
   skip reason; non-applicable techniques cannot run.
6. Result summaries are derivable from trace state and cannot erase objections,
   stable disagreements, or blocker tensions.
7. `block` has no implementation/task-session route; `pass` has a non-null
   selected unit; `flag` names every unresolved readiness effect.
8. Evidence context never upgrades or downgrades the substantive verdict.
9. Markdown is rendered from the accepted result only and adds no semantics.
10. Publication is all-or-nothing, and the receipt binds the exact final family.

## Owner Decision Freeze

The current Decision Gate must be amended before selection because it proposes
five schemas and embeds ModeProfile/TechniqueSpec together. The frozen graph must
select all of the following at once:

| Decision | Required selection | Recommended strict value |
| --- | --- | --- |
| D01 | semantic family version | `v2` |
| D02 | ownership boundary | Distill semantic family; Invoke adapters/evidence/handoff |
| D03 | technique ID wire form | underscore only for v2 writers |
| D04 | exact per-mode defaults and maxima | current documented defaults plus explicit finite maxima |
| D05 | execution-path vocabulary | `true_subagent`, `role_simulation`; derive telemetry `mixed` only |
| D06 | exact-ref shape | `path`, `sha256`, `size_bytes` |
| D07 | verdict/selected-unit/route conditionals | strict conditional rules in this plan |
| D08 | direct and evidence-gated family | one semantic family with optional evidence context |
| D09 | mode/technique decomposition | independent schemas and instances; profile references only |
| D10 | input completeness and revision rule | full RunFrame and explicit objective/output revision lineage |

The amended option should be named independently from the old `STRICT-V2`
option so an older five-schema selection cannot be mistaken for this scope.

## First Schema-Capable SWU

After the amended decision is selected and independently reviewed, start with
SWU-DV2-001: common structural primitives, the TechniqueSpec schema, one
`abstraction_level_guard` instance, one positive fixture, mutation-negative
fixtures, and a schema runner. This is the smallest end-to-end proof of the
newly clarified technique contract. Before that selection, canonical schema
authoring remains blocked.
