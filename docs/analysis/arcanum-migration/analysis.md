# Arcanum Migration Analysis

## Objective

The objective of this document is to map what exists on Arcanum today and what we want for the near future, so we can migrate the application to a new branch on this repo.

The first migration will be the MVP for Arcanum. This still needs to be well defined, but the idea is to have a system that allow users to build code and to keep track of what is being done.

## Context

Agents are making software production cheaper and superficially easier. A person can now produce considerably more code with the help of agents than would previously have been practical.

As the amount of work that can be produced increases, it becomes more important to keep track of what was done, assess the quality of the result and understand what needs to be done next.

The goal of Arcanum is to help a person produce more and better work without turning that increase in capacity into information overload. We approach this by keeping track of the work that has been done and connecting the evidence it produces, as well as what remains open, next steps and blockers, so the user can understand the current state of the work without keeping all of it in mind.

## Practical example

Suppose a user wants to add a new authentication flow to a product. That goal can be broken into smaller pieces of work, like implementing the endpoint and testing the result.

One piece may finish and provide evidence that part of the goal is complete. Another may reveal a blocker because the authentication library no longer supports the SDK.

Arcanum keeps track of these results and where they came from, preserving their provenance as the broader state of the work changes.

The objective is to keep states explicit, so the user can see what is complete, what remains open and what needs attention next.

## How Arcanum works

At a high level, Arcanum keeps the broader context of the work separate from the execution of specific parts of it, while keeping their relationship explicit. A specific piece of work can depend on other work and contribute to a broader objective, and the system needs to preserve those relationships as the work evolves.

The minimum product model used in this explanation has three components: Task Session, which governs what is executed; Decision Gate, which makes consequential decisions explicit; and Craft, which keeps track of project state that belongs to a selected Craft ledger.

Task Session governs the execution of a piece of work, keeping its scope, completion criteria, and validation explicit.

Decision Gate handles decisions that can materially change the course of the work, keeping the available options and the selected direction explicit before dependent work continues.

Craft maintains that ledger as the work evolves, so that decisions, blockers, and evidence remain explicit and can inform what should happen next. Other capabilities still own their native artifacts, receipts, and verdicts.

## Craft ledger

The Craft ledger is the project-local record of the state owned by one selected Craft scope. It keeps track of the work as it progresses, including blockers and decisions. One of its goals is to keep what remains open visible to the user.

One of the most important concepts in Craft is evidence. It is the basis used to verify outcomes and to justify conclusions and decisions. Evidence can come from observations or tests performed during the work.

At the current stage, Craft keeps track of information such as:

| Item | What it represents |
| --- | --- |
| **Context** | A part of the project whose state is being tracked. |
| **Artifact** | Something produced or used during the work. |
| **Blocker** | Something preventing work from progressing. |
| **Decision** | A choice that affects the direction of the work. |
| **Gap** | Something known to still be missing or unresolved. |
| **Evidence** | What supports a conclusion about the work. |
| **Next move** | What should happen next. |

## Task Session

A Task Session is the execution of one bounded piece of work. It keeps the task's objective, scope, expected result, completion criteria, and validation tied together while the work is being performed.

Execution can reveal missing dependencies, new blockers, or choices that change what should happen next. A Task Session should not silently absorb those changes. If the work can be completed within its scope, the session executes it and validates the result. If it cannot, the unresolved issue remains explicit instead of being guessed away.

A Task Session keeps explicit:

- **Scope** — what work is being executed.
- **Completion criteria** — what needs to be true for the work to be considered complete.
- **Validation** — how the result will be checked.
- **Outcome** — what happened during execution and what evidence it produced.

The result of a Task Session is therefore not only an artifact or code change. It also produces evidence about what was actually executed and validated. When that evidence affects Craft-owned state, a separate caller must identify the relevant ledger and invoke a scoped Craft operation. The result does not update Craft merely by existing, and the repository does not yet establish one generic mechanism that performs this write-back for every capability.

## Decision Gate

Some choices can materially change the direction of the work and should not be hidden inside execution. Decision Gate makes those choices explicit before dependent work continues.

When more than one viable path remains, it keeps the relevant alternatives and their consequences visible so that the direction of the work can be chosen explicitly rather than assumed by the agent.

A Decision Gate keeps explicit:

- **Decision** — what needs to be decided.
- **Options** — the viable paths being considered.
- **Trade-offs** — the relevant differences between those paths.
- **Selected direction** — the option chosen for the work to follow.

Not every implementation choice needs a Decision Gate. Local or easily reversible choices can remain inside execution. The gate is intended for decisions whose answer materially changes what should happen next.

## Why migration needs a wider map

The minimum product model explains why Arcanum separates project state, bounded execution, and consequential decisions. It does not describe every service that makes those relations work.

As the repository evolved, capabilities began producing different types of outputs, that do not have the same purpose or owner. Some are source material, some are temporary execution results, some are projections of another source, and some are evidence that must remain available without becoming active policy.

The migration therefore needs to answer a broader question: what must be governed so that Arcanum can keep useful evidence without allowing files, capabilities, and runtime paths to accumulate without a clear role?

The concerns below separate the preservation direction already chosen by the user from questions that still require investigation. The mapping pass must preserve the existing services and accumulated bytes and must not assume a clean rewrite. Candidate interfaces, schemas, proof flows, retention rules, and implementation details remain proposals unless an explicit decision record identifies both the accepted proposition and its accepting authority.

## Orientation inventory

Before choosing a migration architecture, Arcanum needs a compact view of the principal capability families that already exist and the relations that must be preserved. This table is an orientation index, not the executable migration inventory. Each row has a stable identity and describes one primary relation and its provisional evidence ceiling; it does not assign one maturity level to the whole capability or authorize a migration action.

In this inventory, **documented** means that a current owner contract describes the responsibility, **implemented** means that current code or schema provides the named binding, and **observed** means that a fixture, run, or receipt witnesses the behavior in its stated scope. A later status does not automatically prove the earlier one is complete, and a bounded observation must not be generalized beyond its exact flow.

| ID | Capability family | Owner and boundary | Primary exchange | Provisional evidence ceiling | Provisional migration disposition |
| --- | --- | --- | --- | --- | --- |
| `INV-CRAFT` | **Craft** | [`arcana/craft`](../../../arcana/craft/SKILL.md) owns state in the selected Craft ledger, not the native artifacts or verdicts produced elsewhere. | Scoped operations and external decision records can produce validated ledger transitions; only Craft owns the ledger write. | **Documented**; caller-mediated historical observations exist. Generic external-result write-back is not implemented as one universal binding. | **Preserve** the owner boundary; **repair or decide** write-back coordination. |
| `INV-TASK-SESSION` | **Task Session** | [`arcana/task-session`](../../../arcana/task-session/SKILL.md) owns one bounded execution and its evidence, not the state of downstream owners. | An explicit task or admitted work unit produces an outcome, validation evidence, and scoped closeout material. | **Documented and implemented** for bounded execution; one Task Session to Invoke Refresh flow is **observed**. Generic owner hooks remain incomplete. | **Preserve** bounded execution; **repair** missing owner hooks without widening its authority. |
| `INV-DECISION-GATE` | **Decision Gate** | [`arcana/decision-gate`](../../../arcana/decision-gate/SKILL.md) owns the decision record, not the Craft row or other state affected by the decision. | Decision context and viable options produce a selected direction that a caller may pass to the affected owner. | **Documented** with caller-specific tooling and historical observation. No universal direct Craft binding is established. | **Preserve** decision ownership; **adapt** owner-specific joins where needed. |
| `INV-INVOKE` | **Invoke and Refresh** | [`spells/invoke`](../../../spells/invoke/README.md) owns lifecycle authoring artifacts and Refresh, not every execution that may consume them. | Intent and current material can become definitions, designs, plans, work packs, refresh proposals, and owner receipts. | **Documented** with partial implementation; a bounded Task Session to Invoke Refresh owner-receipt chain is **observed**. | **Preserve** authored artifacts and receipts; **repair** incomplete readiness and refresh bindings. |
| `INV-DISPATCH` | **Dispatch Spec** | [`formulae/dispatch-spec`](../../../formulae/dispatch-spec/README.md) owns route representation and validation, not scheduling or native execution. | A proposed dispatch becomes a validated or rejected route with explicit dependencies and boundaries. | **Documented and implemented** as a deterministic validation surface. Runtime execution remains outside its authority. | **Preserve** as the route contract; **adapt** only with compatibility evidence. |
| `INV-ORCHESTRATE` | **Orchestrate** | [`runtime/orchestrate`](../../../runtime/orchestrate/SKILL.md) documents ownership of host-native execution preflight, scheduling, joins, gates, and closeout for an admitted dispatch. | A valid dispatch, host profile, authorization, and available host operations produce bounded execution results and receipts. | The full responsibility set is **documented**. **Implemented** evidence is established only for specifically inspected coordinator bindings; this orientation does not establish complete implementation or one repository-wide observed path for every admitted action. | **Preserve** as the runtime spine; **map and prove** each binding before expanding its scope. |
| `INV-CONTINUATION` | **Continuation Router** | [`arcana/continuation-router`](../../../arcana/continuation-router/SKILL.md) owns one-hop continuation admission, dispatch, and receipt joining, not downstream owner mutation. | A terminal result plus exact authorization or binding can produce a continuation dispatch and joined owner receipt. | **Documented**; a bounded continuation into Invoke Refresh is **observed**, not universal automation. | **Preserve** the explicit gate; **repair** only flows with a named missing binding. |
| `INV-GOAL` | **Goal** | [`spells/goal`](../../../spells/goal/README.md) owns its frontier snapshot, routing loop, and staged proposals, not protected mutation owned by Craft or another capability. | Goal state and read-only project context can produce routes, staged proposals, and receipts for separate owner action. | **Documented and partially implemented**; fixtures and bounded historical runs are **observed**, but live end-to-end owner dispatch and apply are not established. | **Preserve** the progression model; **repair** runtime seams before treating it as autonomous orchestration. |
| `INV-READINESS` | **Context and readiness** | [Context Builder](../../../transmutations/context-builder/SKILL.md), [Work-Pack Readiness Audit](../../../spells/work-pack-readiness-audit/README.md), and [Implementation Readiness](../../../spells/implementation-readiness/README.md) own context coverage and admission judgments, not mutation authority. | Source material and a proposed work unit produce context handoffs and readiness verdicts consumed before execution. | All three are **documented**. Bounded deterministic implementation evidence is established for Work-Pack Readiness Audit and Implementation Readiness, not for Context Builder; observation and gaps remain relation-specific. | **Preserve** the gates; **clarify** how their verdicts compose without duplicating authority. |
| `INV-CAPABILITY-LIFECYCLE` | **Capability lifecycle and distribution** | Canonical capability packages own their source definitions. [Registries](../../../registry/SIGILS.md) and [`tools/arcanum`](../../../tools/arcanum) govern lookup and compatibility surfaces. Host bootstrap profiles own generated native projections, while [Sigil Runtime Installer](../../../arcana/sigil-runtime-installer/SKILL.md) owns only the legacy `.codex/commands/` surface. Other owner-to-surface relations remain unresolved. | Canonical capability material is registered, projected, installed, resolved, and exposed through path-dependent representations. | Named bindings are **documented**, with bounded implemented resolver behavior only for the exact inspected surfaces. Cross-surface identity, precedence, projection parity, downstream consumers, and remaining ownership relations remain unestablished; inherited research evidence is provisional until snapshot revalidation. | **Preserve** current paths first; **adapt or merge** only after compatibility trials. |
| `INV-ARTIFACTS` | **Evidence and generated artifacts** | Native capabilities own their outputs; observability surfaces and historical artifacts preserve evidence without becoming active source authority. The [Artifact Constitution](../../../framework/ARTIFACT-CONSTITUTION.md) provides a documented classification boundary, but no implemented universal artifact-lifecycle owner has been established. | Runs produce receipts, reports, validation results, and historical artifacts whose retention and promotion rules vary by producer. | Artifact production is **observed** and lifecycle contracts are uneven. The external lifecycle boundary is a **proposed implementation direction**, not an accepted or implemented service. | **Preserve** existing bytes; **inventory** producers and consumers first; **evaluate and decide** the proposed Task Session to Invoke Refresh proof before expansion. |

### Mapping-pass contract

The executable mapping artifact has one canonical location: `docs/analysis/arcanum-migration/mapping/current-system-map.json`. Its [versioned schema](contracts/current-system-map.schema.json), [conforming example](contracts/current-system-map.example.json), and [validator](scripts/validate_mapping.py) define relation identity, field types, evidence locators, baseline binding, discovery coverage, unresolved-item ownership, and completion semantics. Relation IDs use `REL-<INVENTORY-ID>-NNN`; each relation belongs to one declared `INV-*` identity.

The validator is run from the repository root:

```text
python docs/analysis/arcanum-migration/scripts/validate_mapping.py --require-ready
```

A field may be recorded as unresolved only through a typed `unknowns` entry that identifies evidence already searched, an accountable owner, expected deliverable, acceptance criterion, review condition, closure authority, next action, and whether it blocks a migration decision. A named owner alone cannot satisfy closure.

### Discovery and coverage closure

The first pass must search the declared capability and evidence surfaces rather than treat the orientation IDs as the whole universe. At minimum, its discovery roots must cover `.agents/skills/`, `arcana/`, `spells/`, `formulae/`, `transmutations/`, `runtime/`, `registry/`, `tools/`, `framework/`, `.arcanum/observability/`, `sessions/`, `research/`, and `docs/analysis/`. Exclusions must name their path or pattern, reason, and authority.

Discovery must enumerate each producer × write location × artifact family × consumer edge. Every discovered edge must be linked to a relation record, explicitly excluded with a reason, or blocked by an owned open item. Every orientation ID must have at least one relation record. The pass is **structurally complete** only when the schema, baseline, IDs, and discovered edges reconcile; it is **decision-ready** only when no blocking unknown or open item remains. The validator checks both claims. Until decision readiness passes, the map cannot authorize deletion, path moves, capability consolidation, or a new architecture.

### Evidence boundary for this orientation

This orientation inspected repository HEAD `e3f67a7e728dce1504cfb7b04f521d363c4873f9` together with a dirty working tree. That state is **not** a migration baseline: the hashes below detect source drift but cannot reconstruct all dirty or untracked bytes. The executable map must instead bind `baseline` either to a resolvable clean Git commit or to a retrievable content-addressed bundle containing its declared paths; the validator rejects an absent or hash-mismatched bundle. Until one of those bindings exists, the map cannot be structurally complete.

The [composition findings](research/arcanum-composition/findings.md) remain the primary bounded source for current service relations. The [unified skill research](../../../research/unified-skill-model/findings.md) explicitly states that its corpus was dirty and not snapshot-bound, so its compatibility observations are orientation evidence only until the mapping pass rechecks their current locators and hashes.

All labels below are repository-root-relative paths, and every label links to the current source. These are evidence locators for this orientation, not a substitute for the map's reproducible baseline:

| Source | SHA-256 | Purpose |
| --- | --- | --- |
| [`docs/analysis/arcanum-migration/research/arcanum-composition/findings.md`](research/arcanum-composition/findings.md) | `2c7a85a8fb64fe089c579c253aef0d3b944f498c6a2c48a7f50b5ede163935a1` | Bounded service relations and observed flows. |
| [`research/unified-skill-model/findings.md`](../../../research/unified-skill-model/findings.md) | `0aa3b3d534e48a609362c3d51048670dc1d0c9c167c0f1b655f2d644247208fa` | Compatibility observations and their source-state limitation. |
| [`sessions/2026-08-26-1400-artifact-lifecycle-repository-direction.md`](../../../sessions/2026-08-26-1400-artifact-lifecycle-repository-direction.md) | `ce986b49d4db2e88bd3398bb994883807a908451f20f70e6cbc69c8a63fd1b1b` | Accepted preservation direction, proposed lifecycle boundary, and proposed first proof. |
| [`runtime/orchestrate/SKILL.md`](../../../runtime/orchestrate/SKILL.md) | `895fde1dd01bb53b70ac31328048c762aa20b1affbe0d3558ca5fb79497d4f19` | Full documented Orchestrate authority. |
| [`runtime/orchestrate/scripts/native_dispatch_coordinator.py`](../../../runtime/orchestrate/scripts/native_dispatch_coordinator.py) | `b30fe0f5b46ddbd17a0d966e07bf5a8691a58ce2ceed5b59efbb6d96d063d449` | Current inspected coordinator implementation. |
| [`transmutations/context-builder/SKILL.md`](../../../transmutations/context-builder/SKILL.md) | `d0372eef7096d8b05c6e9d61ca3596c074999a157fdd7dfce46dc442f4c69096` | Documented Context Builder handoff contract. |
| [`spells/work-pack-readiness-audit/README.md`](../../../spells/work-pack-readiness-audit/README.md) | `60ba55f84d3fe88bb60b4036a8218ab116b4285ac2611fa9dd23b008051a1f00` | Deterministic readiness runner. |
| [`spells/implementation-readiness/README.md`](../../../spells/implementation-readiness/README.md) | `6cddad54936159d94b4c2bce3e79b9b7c6b5f7bc5c542c3804c1ef4591d88018` | Executable readiness validation surfaces. |
| [`docs/analysis/arcanum-migration/contracts/current-system-map.schema.json`](contracts/current-system-map.schema.json) | `26d5364bc7b2e679104a349fbdafba2e0ba5e85a056adaffd27105fde7ced3b4` | Executable mapping and closure contract. |
| [`docs/analysis/arcanum-migration/contracts/current-system-map.example.json`](contracts/current-system-map.example.json) | `454222bf17398d87bd26adb20fa3e89b322f3281785ec8c19f1708d26fab0f38` | Conforming record, discovery, and baseline example. |
| [`docs/analysis/arcanum-migration/scripts/validate_mapping.py`](scripts/validate_mapping.py) | `a16f71fcb50dfe6091f530a22d7e53e683c85a9638153d0eb97859b48cbe9204` | Deterministic schema, baseline, relation, coverage, and readiness validation. |
| [`docs/analysis/arcanum-migration/requirements.txt`](requirements.txt) | `4046ca1e3a64f4ea791fb4fb3d8566242086ff1c8e2431e2c349e1052ffc6ba0` | Validator dependency boundary. |

## Recorded artifact-lifecycle direction

The [decision record](../../../sessions/2026-08-26-1400-artifact-lifecycle-repository-direction.md) records one accepted preservation direction: keep the existing services and accumulated work, do not start with a clean clone, and inventory producers and consumers before another repository-wide redesign. The user is the accepting authority for that direction.

The same record **proposes**, but does not establish as accepted or implemented:

- keeping reusable source in Git while execution output passes through one external lifecycle boundary and enters Git only through explicit promotion;
- using Task Session to Invoke Refresh as the first bounded proof, with content-hash preservation, cold verification, rehydration, and corruption and omission controls;
- reconsidering a successor repository only after that proof passes.

The mapping may evaluate these proposals without reopening the preservation direction. The lifecycle interface, physical store, retention periods, backup guarantees, compatibility mechanisms, garbage-collection policy, and proof acceptance criteria remain open decisions.

## Artifacts and their lifecycle

JSON and Markdown files are two visible forms of the same broader problem. The repository needs to know why a generated artifact exists, who produced it, who owns it, who will consume it, how long it should remain, and whether it may become source material.

A common minimum contract may give governed artifacts a stable identity, kind, schema version, owner, purpose, producer, consumers, status, authority class, source references, and retention rule. Each artifact type would still keep its own specific structure. A Markdown explanation and a JSON receipt may share lifecycle information without sharing the same content schema.

Markdown artifacts should remain small and purposeful. A new document should not be created when an existing document can responsibly carry the change, when no later reader or capability needs the result, or when the content is only temporary execution residue. Generated JSON should follow the same principle: it should have a declared contract and lifecycle rather than remain in the repository merely because a run produced it.

This points to one artifact-lifecycle concern with format-specific rules, rather than independent services for every file extension. The external boundary and explicit-promotion mechanism remain proposals. Their authority, interface, storage implementation, retention periods, rehydration guarantees, and garbage-collection policy require a separate decision after the mapping evidence exists.

## Skills and capabilities

Arcanum already has mechanisms for creating, registering, installing, and exposing skills, but those mechanisms do not yet form one authoritative lifecycle or one settled structural model.

The migration needs to make the role and effect of a skill easier to understand before it is invoked. A routing skill, for example, should not be confused with a skill that writes source code or owns durable state. At the same time, one skill can route work and produce an artifact, so a single exclusive list of types may hide important behavior.

A useful classification may need more than one dimension:

- the skill's primary role, such as routing, composing, writing, executing, validating, reviewing, observing, or owning state;
- the effects it may perform, such as read-only analysis, artifact creation, source mutation, state mutation, or an external side effect;
- whether its execution is deterministic, model-mediated, or hybrid;
- the kind of result it returns, such as text, code, an artifact, a decision, a receipt, a route, or a state transition.

These dimensions are candidates, not a final taxonomy. Before choosing them, the migration must determine which distinctions actually change routing, permission, validation, installation, or lifecycle behavior. It must also decide how a skill is identified, where its canonical authority lives, and how generated host projections remain compatible with that source.

## Execution, decisions, and project state

Describing work and executing it are different responsibilities. Dispatch Spec can describe and validate a route. Orchestrate can execute admitted actions through host-native operations. Task Session can govern one bounded unit of work. None of those responsibilities by itself grants authority to change every state affected by the result.

The same separation applies after execution. A receipt can show what happened without deciding how the project ledger should change. Decision Gate can resolve a consequential choice without directly owning the Craft row that records its project effect. Craft can apply a ledger operation without taking ownership of the native artifacts produced by those capabilities.

The migration must therefore decide whether Arcanum needs a generic write-back coordinator. Such a mechanism would have to identify the affected state, select the correct owner, translate evidence into a proposed owner operation, obtain any required approval, invoke the owner, and preserve the resulting receipt. The current repository supports parts of this relation in bounded flows, but it does not establish one universal implementation.

## Evidence, distribution, and compatibility

Arcanum needs evidence to distinguish a documented contract from an implemented binding and an observed execution. Observability, validation reports, and historical receipts help make that distinction, but they should not become active source authority merely because they are preserved.

The repository also exposes capabilities through registries, installers, generated skill packages, aliases, host-specific profiles, and compatibility tools. These surfaces may represent the same capability without being equally authoritative. The migration needs an explicit rule for identifying the canonical source, detecting projection drift, preserving consumers that depend on current paths, and retiring compatibility layers when they are no longer needed.

Evidence retention and compatibility are related to artifact lifecycle but are not the same thing. Retaining a historical result does not make it current policy, and generating a host-specific representation does not transfer ownership away from its canonical capability.

## Open migration questions

Open items are not complete merely because they have an owner. Each one remains blocking until its evidence and acceptance criterion are satisfied and the named closure authority records a resolution.

| ID | Question | Owner and next action | Deliverable and acceptance criterion | Review and closure authority |
| --- | --- | --- | --- | --- |
| `OPEN-ARTIFACT-SCOPE` | Which artifacts are governed outputs, and which source documents remain outside the generated-artifact lifecycle? | **Artifact mapping workstream** — enumerate producer × write location × artifact family × consumer edges and justified exclusions. | Coverage entries in `current-system-map.json`; every discovered edge is mapped, excluded with authority, or blocked. | Review when coverage reconciles; **migration Decision Gate** may close. |
| `OPEN-ARTIFACT-CONTRACT` | What lifecycle information is common to governed artifacts, and what remains format-specific? | **Artifact mapping workstream** — compare current JSON schemas, Markdown contracts, producers, and consumers. | A candidate contract with compatibility evidence; required common fields and format-specific extensions are unambiguous. | Review after compatibility checks; **migration Decision Gate** may close. |
| `OPEN-ARTIFACT-BOUNDARY` | Should the proposed external execution-artifact boundary be accepted, and with which storage, retention, recovery, and garbage-collection rules? | **Artifact-lifecycle design owner** — produce options, failure modes, compatibility obligations, and proof criteria. | A Decision Gate option packet; each viable option covers retention, recovery, corruption, omission, promotion, and compatibility. | Review after the map is decision-ready; **user through Decision Gate** may close. |
| `OPEN-SKILL-MODEL` | Which skill distinctions materially change routing, authority, validation, execution, or lifecycle behavior? | **Capability-lifecycle mapping workstream** — classify current skills across role, effect, determinism, and result dimensions. | Classification records in the map; every current skill is covered and every multi-role case remains representable. | Review when records reconcile with registries and runtime consumers; **migration Decision Gate** may close. |
| `OPEN-SOURCE-PRECEDENCE` | Which source governs when a capability contract, schema, registry entry, projection, and implementation disagree? | **Capability-lifecycle mapping workstream** — inventory precedence claims and projection consumers. | Precedence relations in the map; every conflict has one canonical owner or one explicit blocking contradiction. | Review after projection-consumer checks; **migration Decision Gate** may close. |
| `OPEN-CRAFT-WRITEBACK` | Should generic Craft write-back exist, and who coordinates it without taking ownership of Craft state? | **Craft integration mapping workstream** — map current callers, operation shapes, approvals, and receipts. | Relation records plus bounded alternatives; every known caller and owner transition is represented without transferring Craft authority. | Review when alternatives and consequences are evidenced; **user through Decision Gate** may close. |
| `OPEN-COMPATIBILITY` | Which paths, aliases, downloads, and generated packages must remain compatible? | **Compatibility mapping workstream** — enumerate consumers and run path/projection trials against the selected baseline. | Compatibility obligations in the map; every discovered consumer has a preserve, adapt, or retire disposition with evidence. | Review after trials pass or remain explicitly blocked; **migration Decision Gate** may close. |

The canonical map must carry these items in its typed `open_items` collection with their expected deliverable, acceptance criterion, review condition, closure authority, next action, and blocking state. They must be resolved before the migration plan chooses service implementations, directory moves, or compatibility deadlines. The plan must preserve the accepted no-clean-rewrite direction without treating the proposed artifact boundary as already decided.
