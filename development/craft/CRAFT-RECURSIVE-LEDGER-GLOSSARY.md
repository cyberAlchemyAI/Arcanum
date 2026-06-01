# Craft Recursive Ledger Glossary

## Purpose

This glossary stabilizes the first operational vocabulary for Craft's recursive ledger MVP.

All terms are candidate definitions until validated through examples and later architecture/work-pack artifacts.

## Terms

| Term | Candidate Definition | Status | Notes |
| --- | --- | --- | --- |
| Craft Context | A bounded development space with its own purpose, lifecycle state, artifacts, relationships, gate, and next move. | candidate | May represent a project, subproject, method slice, experiment, or work area. |
| Recursive Ledger | A ledger where contexts can contain other contexts while also relating across branches through blockers, enablers, dependencies, and evidence. | candidate | The core MVP object. |
| Context Tree | The parent/child containment structure of contexts. | candidate | Tree structure handles nesting, but cross-context relations require graph edges. |
| Cross-Context Relation | A blocker, enabler, dependency, informing relation, or supersession between contexts that may not share the same parent. | candidate | Needed for cross-project blockers and enablers. |
| Context Artifact | A file, decision, output, work-pack, validation result, handoff, or generated product owned by a context. | candidate | Artifacts may also participate in blocker/enabler relations. |
| Gate | The current pass, flag, or block verdict for a context. | candidate | Gate is local to the context but may be affected by cross-context relations. |
| Blocker | A relation where one context, artifact, decision, or missing condition prevents another context from progressing. | candidate | Must include source, target, reason, and evidence when possible. |
| Enabler | A relation where one context, artifact, decision, or condition makes another context able to progress. | candidate | Enablers are first-class, not just inverse blockers. |
| Next Responsible Move | The next action that should happen for a context, given its stage, gate, blockers, and enablers. | candidate | Should stay concrete enough to route to define, design, plan, task-session, or another capability. |
| Owned Artifact | An artifact for which a context is the primary development or maintenance owner. | candidate | A file can be referenced by many contexts but should have one primary owner where possible. |
| Context Stage | The lifecycle state of a context: idea, define, design, plan, execute, validate, reflect, blocked, or closed. | candidate | Mirrors Craft's Define -> Design -> Plan -> Execute -> Validate -> Reflect cycle with operational additions. |
| Ledger Row | A structured entry describing one context, artifact, relationship, gate, or event. | candidate | Can be represented in Markdown first, with optional JSON later. |
| Priority Scoring | A future mechanism for ranking contexts or next moves using blockers, enablers, readiness, importance, and confidence. | deferred | Explicitly out of MVP scope. |
| Work-Pack | A task-execution ledger that decomposes work into tasks, SWUs, gates, blockers, and validation. | existing-aligned | In Craft ledger terms, a work-pack is usually an artifact owned by a context. |
| Base Type | A shared blocker, gate, or enabler type that applies across Craft contexts. | candidate | Provides stable vocabulary for later scoring and role mapping. |
| Context-Specific Type | A local subtype that extends one base type inside a context family. | candidate | Lets Craft express domain-specific blockers without fragmenting the base vocabulary. |
| Operational Lane | A responsibility lane such as `business`, `tech`, `qa`, `validator`, or `auditor` that describes the expertise needed for a typed ledger item. | candidate | Lanes are clearer than generic owner roles for delegation planning. |
| Type Role Mapping | A candidate association from condition type plus operational lane to responsible role or future route. | deferred | Modeled now, automated later. |
| Delegation Role | A local responsibility assignment inferred from a type and lane, such as `architect`, `product_owner`, `qa_owner`, `validator`, or `auditor`. | candidate | Roles should remain separate from concrete tools until routing is validated. |
| Blocker Refiner | A role responsible for turning a raw blocker into a typed, lane-owned, evidence-backed blocker with a closure condition before resolution is allowed. | candidate | Default route is `/refine`; the refiner prepares resolution but does not necessarily resolve the blocker. |
| Blocker Refinement Gate | A gate that prevents a blocker from being marked resolved until it has been refined or explicitly waived by human decision. | candidate | Helps prevent false closure of vague blockers. |

## Boundary Rules

1. A Craft Context is broader than a task.
2. A Work-Pack may belong to a Craft Context, but it is not the whole context.
3. A Context Tree is not enough because blocker/enabler relationships can cross branches.
4. Enablers should be modeled explicitly rather than inferred from blocker resolution.
5. Priority scoring must wait until relationship semantics are stable.
6. Context-specific types must extend base types instead of creating disconnected vocabularies.
7. Type-to-lane mapping should be clear before type-to-role delegation is automated.
8. Every blocker needs refinement before it can be marked resolved, unless an explicit human waiver is recorded.

## Open Definition Questions

| Question | Why It Matters | Status |
| --- | --- | --- |
| Can one artifact have multiple owning contexts? | Shared artifacts may appear in nested projects. | open |
| Should blocker/enabler relations attach to contexts only, or also to artifacts and decisions? | Fine-grained blockers may need artifact-level targets. | open |
| Should lifecycle stage be a fixed enum or extensible per context type? | Different contexts may need specialized stages. | open |
| Should the root ledger be one file or a folder with indexes? | Affects readability and future automation. | open |
| Can a ledger item carry multiple base types? | Real blockers may have mixed causes, such as authority plus validation. | open |
| Who owns the lane and role catalogs? | Type-to-lane-to-role delegation needs stable authority before automation. | open |
