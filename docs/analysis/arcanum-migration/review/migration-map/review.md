# Review — Arcanum migration map and Craft write-back claims

## Coverage

| attacker | lens | targets checked | findings raised | zero-findings defense |
| --- | --- | --- | --- | --- |
| `migration-review-attacker` | fidelity/governance and ownership/reference integrity | the prior migration recommendation; complete `analysis.md`; composition findings; unified-skill findings; artifact-lifecycle direction | 8 provisional; 5 load-bearing findings retained | n/a |
| parent | mechanics/correctness and operability | every proposed finding against the literal owner contracts, runtime sources, research conclusions, current Git semantics, and renamed paths | verified 5 load-bearing findings; retained 1 additional broken-reference finding | n/a |
| parent as final verifier | attempted refutation and severity check | Craft ownership and write-back; current/proposed boundary; skill identity; runtime topology; branch/baseline semantics; renamed links | 6 survived | The claims that composition is plural, Dispatch Spec validates, Orchestrate executes, Invoke is not a universal lifecycle owner, and no generic Craft write-back coordinator was found all survived attempted refutation. |

## Findings

| # | artifact and locator | evidence | severity | consequence | proposed fix |
| --- | --- | --- | --- | --- | --- |
| 1 | `analysis.md:23-29,33,62`; prior recommendation, `Estado durável — Craft` | The analysis calls Craft, Task Session, and Decision Gate the three main components, describes Craft as the broader state holder, and says a Task Session result can update it. Craft authority is narrower: `.craft/ledger.yml` is the source of truth for the selected Craft scope, while native artifacts and verdicts retain their owners (`arcana/craft/SKILL.md:135-149,312-316`). The composition findings do not identify a generic trigger, coordinator, semantic adapter, or packaged runner for external-result write-back. | MAJOR | Readers may infer that Craft owns all system state or that Task Session results propagate into Craft automatically. That would collapse Decision Gate, Invoke, Task Session, Goal, and telemetry ownership into the ledger. | Describe Craft as the source of truth for the selected Craft ledger only. State that an external result may feed a separately invoked, scoped Craft operation; no generic automatic write-back path has been established. |
| 2 | `analysis.md:23-29`; prior recommendation, architectural-domain table | The three-component description is a useful minimum product model, but the current composition is plural and also contains Invoke, Dispatch Spec, Orchestrate, continuation, Goal, readiness, capability distribution, and evidence owners. The prior table also presented an external artifact-lifecycle service beside existing components even though that service is a proposed boundary awaiting a bounded proof. | MAJOR | A migration inventory could omit load-bearing services while simultaneously treating target-architecture proposals as current implementation. | Separate three views: `minimum product model`, `current evidenced inventory`, and `candidate migration workstreams/target architecture`. Give every current claim an evidence status such as `documented`, `implemented`, or `observed`; label future boundaries `proposed`. |
| 3 | prior recommendation, Skills section | Stable `capability_id`, one minimum schema, and ID-based resolution were prescribed before the repository has resolved identity authority, same-concern precedence, projection parity, or path-bound consumers. The unified-skill findings keep those questions unresolved and falsify only naive path-blind consolidation. | MAJOR | Premature identity design could break resolvers, generated provenance, public paths, schemas, and downstream consumers while appearing to simplify the model. | Treat the unified model and stable ID as hypotheses. First decide authority and conflict rules, inventory internal and external path consumers, and prove compatibility aliases; only then select and version an identity/schema model. |
| 4 | prior recommendation, runtime sequence `Dispatch Spec → Orchestrate → Host projections → tools/arcanum` | Orchestrate consumes an already-valid dispatch plus host profile and active host operations (`runtime/orchestrate/SKILL.md:73-80,99-109`). Host projections expose/install capabilities and are not a downstream execution stage. `tools/arcanum` is a resolver and compatibility surface, not an Orchestrate-owned phase. | MAJOR | The sequence assigns the wrong direction and ownership to deployment, discovery, validation, and execution, producing a faulty migration order. | Replace the pipeline with a relationship map: Dispatch Spec validates route shape; Orchestrate executes admitted actions; host profiles and generated projections are runtime/deployment inputs; `tools/arcanum` remains deterministic resolution and legacy compatibility. |
| 5 | prior recommendation, final branch paragraph | The text says a new branch would inherit the dirty state. A new branch ref is based on a commit; uncommitted changes remain in the shared working tree but are not part of that branch's commit history. Existing research asks for an explicit evidence baseline and defers a successor repository decision, not branch creation itself. | MAJOR | The recommendation creates a false process gate and conflates branch isolation, working-tree state, evidence baseline, and clean-repository migration. | Require a named baseline before material migration—commit/tag when appropriate, or a snapshot manifest when the dirty state must remain. A migration branch may be created from that baseline; whether to create a successor repository remains a later decision. |
| 6 | `sessions/2026-08-26-1400-artifact-lifecycle-repository-direction.md:27-28` | Two provenance links still point to `docs/analysis/arcanum-composition-analysis/...`, which no longer exists after the directory was renamed to `arcanum-migration`. | MINOR | Navigation and provenance from the session artifact are broken. | Update the two relative links to `docs/analysis/arcanum-migration/...` in a separately authorized maintenance change. |

## Artifact verdicts

| artifact | KEEP or FIX | rationale |
| --- | --- | --- |
| prior migration recommendation | FIX | Five MAJOR findings survive: Craft ownership/write-back, current-versus-proposed state, premature skill identity design, incorrect runtime topology, and branch/baseline conflation. |
| `analysis.md` | FIX | Its minimal product explanation is useful, but it is not yet a sufficient migration inventory and overstates the Task Session-to-Craft transition. |

## Change requests

1. Bound Craft to its selected ledger and describe external write-back as a separate Craft-owned operation with a currently missing generic coordinator/adapter.
2. Split the migration documentation into minimum product model, evidenced current inventory, gaps, and proposed target workstreams.
3. Recast unified skill identity/schema/path consolidation as an open hypothesis gated by authority, precedence, consumer inventory, and compatibility trials.
4. Replace the linear runtime pipeline with an ownership-preserving relationship map.
5. Define a migration evidence baseline without claiming that Git branch creation itself captures or inherits uncommitted work.
6. Repair the renamed analysis links in the artifact-lifecycle session when that artifact is next maintained.

## Evidence boundary

The review checked the prior recommendation and the complete current
`analysis.md` against the cited canonical owner contracts, deterministic runtime
sources, composition research, unified-skill research, artifact-lifecycle
direction, current path layout, and Git working-tree semantics. It did not run an
end-to-end Arcanum dispatch, prove an external artifact store, enumerate external
consumers, select a final skill identity model, or approve edits to
`analysis.md`. The review was read-only over its targets. The previous
initial-definitions review was preserved as
`research/arcanum-composition/initial-definitions-review.md`.
