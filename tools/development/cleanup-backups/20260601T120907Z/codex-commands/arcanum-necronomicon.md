# Arcanum Necronomicon

<!-- arcanum:capability-id necronomicon -->
<!-- arcanum:capability-kind spell -->
<!-- arcanum:capability-tier spell -->
<!-- arcanum:command arcanum-necronomicon -->

## Observer Envelope: Task Zero

Before doing domain work, establish the observer envelope for this Arcanum invocation.

- `run_id`: use an existing hook-provided run id when present; otherwise use `arcanum-arcanum-necronomicon-<UTC timestamp>`.
- `capability.id`: `necronomicon`
- `capability.kind`: `spell`
- `capability.tier`: `spell`
- `capability.mode`: `command`
- `target_artifact`: this command file
- request summary: summarize the user request before execution.
- expected outputs: list intended artifacts before execution when known.

Closeout is mandatory but must not hide the primary result. At the end, report:

- `OBSERVATION`
- `LEDGER`
- `REFLECTION_TRIGGER`
- `RECOMMENDATION`
- `DEDUPE_KEY`

If deterministic hook or wrapper telemetry is unavailable, preserve the result and report the observability gap.


## Objective

Create, set up, resume, research, route, maintain, update, or close a repository-local Necronomicon harness.

## Process

1. Read `.arcanum/necronomicon/capabilities.json` when it exists.
2. Resolve the mode as setup, start, resume, route, checkpoint, research, implementation-research, update-capabilities, fallback-discover, maintain, or close.
3. Load active session memory from `.arcanum/necronomicon/sessions/` when resuming, routing, checkpointing, researching, or maintaining.
4. Prefer selected local capabilities from the manifest before considering fallback candidates.
5. Route ontology, vault, premise, branch, bridge, confidence, or session-distillation work to `arcanum-ontology-harness` or `arcanum-spell-ontology-harness` when installed.
6. Route lifecycle authoring requests and implementation-research handoffs to `arcanum-spell-invoke` when installed.
7. In research mode, use bounded source order: session, inventory, ontology, docs, code, then web when available and allowed.
8. In maintain mode, aggregate route telemetry plus selected sigil/spell signals and run `arcanum-spell-sigil-maintenance-loop` when installed.
9. If no selected capability matches, inspect installed commands and canonical registry references, then offer 2-5 fallback candidates before adding anything.
10. Record route attempts, decisions, memory changes, gap updates, and capability update recommendations under `.arcanum/necronomicon/` when mutation is allowed.
11. Return session ID, selected route, confidence, fallback status, files updated, validation result, observability result, and next action.

## Guardrails

- Keep `.arcanum/necronomicon/` as harness state only.
- Do not copy formulae, transmutations, arcana, spells, registries, or framework folders into it.
- Do not add fallback capabilities silently.
- Do not treat session memory as more authoritative than source documents, registries, or implementation evidence.

## Canonical Spell Snapshot

Canonical source: https://github.com/cyberAlchemyAI/arcanum/blob/main/spells/necronomicon/README.md

````markdown
# Necronomicon

## Identity

- Canonical ID: `necronomicon`
- Primary alias: `Necronomicon`
- Aliases: `Repository Harness`, `Arcanum Harness`
- Scope: library

## Purpose

Necronomicon creates, resumes, and maintains a repository-local harness session with explicit setup profiles, durable working memory, routing history, checkpoints, bounded research workflows (repository and web), and maintenance recommendations.

The spell makes Necronomicon the project harness shell for a repository without turning `.arcanum/necronomicon/` into a copied canonical definition store. Runtime adapters remain the first-pass execution surface. Session state records what was selected, why a route was chosen, which fallback candidates were offered, what unresolved gaps remain, and what should persist between turns and sessions.

## Conceptual Model

Necronomicon is the persistent repository harness for Arcanum. It keeps durable session state, selected capability routing, checkpoints, research briefs, fallback discovery, and maintenance recommendations around the repository's installed sigils and spells.

Use `arcanum-necronomicon`, `necronomicon`, or `arcanum-spell-necronomicon` when the repository needs a resumable operating shell with memory, routes, gaps, and handoffs. Use `ontology-harness`, `arcanum-ontology-harness`, or `arcanum-spell-ontology-harness` for a single ontology governance run.

The harness spell does not replace the capabilities it routes to. It is a coordinator and memory boundary. Inventory remains responsible for reusable repository knowledge, ontology-vault remains responsible for ontology promotion, invoke remains responsible for define/design/plan/full/validate lifecycle authoring, and maintenance authoring still routes through `spellcraft` or `sigil-development`.

## Day-To-Day Use Vision

Necronomicon should feel like the repository's working memory and routing desk. The user should be able to begin a normal work session with a plain request, let Necronomicon recover the relevant context, route to the right installed capability, and leave behind enough trace that the next session can continue without replaying the whole conversation.

The everyday loop is:

1. **Open the repo:** the user asks Necronomicon to resume or start work in the repository.
2. **Recover context:** Necronomicon loads setup decisions, current session memory, recent routes, gaps, and checkpoints.
3. **Route the request:** Necronomicon chooses the owning capability, such as `invoke`, `task-session`, `ontology-harness`, `implementation-readiness`, or `inventory`.
4. **Execute through the owner:** the selected sigil or spell does the real work while Necronomicon records route, rationale, validation, and follow-up.
5. **Checkpoint when useful:** Necronomicon distills facts, decisions, contradictions, and unresolved questions into concise durable memory.
6. **Improve the harness:** when route misses or repeated gaps accumulate, Necronomicon proposes capability, preset, or maintenance changes for explicit approval.

Necronomicon should support these daily activities without ceremony:

| Activity | User Intent | Necronomicon Behavior |
| --- | --- | --- |
| Start the day | "Where were we?" | Resume memory, summarize open work, surface blockers, suggest next routes. |
| Pick up a feature | "Continue the cache invalidation work." | Load prior decisions and route to `invoke`, `implementation-readiness`, or `task-session`. |
| Ask project questions | "What do we know about auth boundaries?" | Search memory and inventory, then route to context or ontology flows when needed. |
| Research a decision | "Find evidence before we choose." | Run bounded research with source trail, contradictions, and a synthesis checkpoint. |
| Make architecture or ontology sense | "Map domain intent to implementation." | Route to `ontology-harness` and keep promotion candidates gated. |
| Execute a task | "Implement the next slice." | Route to the task owner and record outcome, validation, and gaps. |
| End the day | "Checkpoint this." | Write a concise checkpoint and update the gap ledger. |
| Maintain the harness | "This route keeps missing." | Use telemetry and route history to propose explicit updates. |

The target user experience is low-friction: the user should not need to remember which sigil owns every workflow. Explicit commands still win, but ordinary language should be enough for Necronomicon to propose a route, name its confidence, and ask only one focused question when the route is ambiguous.

## Operating Model

Necronomicon works in four layers:

| Layer | Responsibility | Persistent State |
| --- | --- | --- |
| Harness setup | Select a base profile, dependencies, fallback policy, privacy policy, and runtime surface. | setup decisions, capability manifest |
| Session memory | Keep compact durable memory, decisions, route history, checkpoints, and unresolved gaps. | session folder, route ledger, gap ledger |
| Routed execution | Classify user intent and delegate to selected local sigils or spells through runtime adapters. | route records, validation status, follow-ups |
| Maintenance | Read route misses, telemetry, stale signals, and repeated gaps to propose explicit harness improvements. | maintenance reports, capability update reports |

The default flow is:

1. Load setup decisions, capability manifest, existing memory, route history, and gaps.
2. Classify the request against explicit command names, aliases, selected profiles, and route presets.
3. Delegate execution to the selected command adapter when a route is available.
4. Record the route attempt, result, validation, unresolved gaps, and next action.
5. Write checkpoints, research briefs, maintenance reports, or handoffs only when the selected mode requires them.

## Interaction State Model

Necronomicon must distinguish a new route request from a continuation of an active interaction. A user response during research, discovery, setup, definition, decision review, or task execution should usually continue the active run rather than be classified from scratch.

Each active Necronomicon session tracks an `active_interaction` record:

| Field | Meaning |
| --- | --- |
| `interaction_id` | Stable ID for the current back-and-forth flow. |
| `owning_capability` | The sigil or spell currently responsible for interpreting the next user turn. |
| `mode` | The active mode, such as `research`, `implementation-research`, `invoke define`, `setup-profile`, or `task-session`. |
| `status` | `awaiting-user`, `running`, `handoff-ready`, `blocked`, `completed`, or `abandoned`. |
| `pending_prompt` | The question, choice, approval, or evidence request the user is answering. |
| `expected_response_shape` | Free-form answer, option choice, approval, correction, artifact path, scope clarification, or interruption. |
| `continuation_policy` | Whether the next turn should continue the active run by default, require confirmation, or route fresh. |
| `handoff_target` | The next capability to route to after this interaction completes. |
| `side_note_queue` | Facts, research seeds, unblocker tasks, contradictions, reminders, or parking-lot items captured without derailing the active flow. |

Incoming user turns are classified in this order:

1. **Explicit interrupt or command:** if the user names a command, asks to stop, asks to switch topics, or starts a clearly unrelated task, route as a new request after recording the active interaction status.
2. **Side note:** if the user marks the turn as a note, aside, reminder, research idea, parking-lot item, or "for later", capture it in the side note queue and keep the active flow unless the user asks to switch.
3. **Pending response:** if an active interaction is `awaiting-user`, treat the turn as a response to the owning capability unless it clearly interrupts.
4. **Handoff continuation:** if an active interaction is `handoff-ready`, route to the handoff target after summarizing what will move forward.
5. **Fresh route:** if no active interaction exists, classify against normal routing rules.
6. **Ambiguous turn:** if both continuation and fresh route are plausible, ask one focused question: continue the active flow or start a new route.

This policy applies to any sigil or spell run that can ask the user for clarification, approval, scope, evidence, or decisions. Necronomicon owns the conversation state and route ledger; the active capability owns how to interpret the answer inside its mode contract.

Side notes are first-class harness input. A side note may become attached active-context, an inventory candidate, a research candidate, a small unblocker task, an ontology candidate, a contradiction, or a deferred reminder. Necronomicon should capture first and switch only when the user intends to switch.

Small related unblockers are allowed to become tasks directly when they are bounded and unblock the active work, such as checking current API prices, confirming a version limit, or retrieving one vendor policy. If they are not blocking, they should stay queued as side notes or research candidates. If they are broad, Necronomicon should ask one scope question before running them.

## Discovery-To-Definition Funnel

Feature definition should not jump straight to `invoke define` when the problem is still unclear. Necronomicon should treat feature work as a funnel:

| Stage | Purpose | Owning Route | Exit Signal |
| --- | --- | --- | --- |
| Discover | Understand intent, boundaries, users, constraints, and known artifacts. | `context-builder`, `scope-interview`, or Necronomicon `implementation-research` | Scope is clear enough to research or define. |
| Research | Gather local and optional web evidence, contradictions, and decision options. | Necronomicon `research` or `implementation-research` | Evidence brief and unresolved gaps are recorded. |
| Decide | Resolve consequential choices exposed by discovery or research. | `decision-gate` or owning capability gate | Decision is approved, deferred, or blocked. |
| Define | Produce governed spec and glossary baseline. | `invoke define` | Define output is pass, flag, or block. |
| Design/Plan | Convert the definition into architecture, implementation layering, plan, or work-pack. | `invoke design`, `invoke plan`, or `implementation-readiness` | Handoff is ready for task execution. |
| Execute | Run a bounded implementation or documentation task. | `task-session` or the selected executor | Result, validation, and follow-up are recorded. |

The funnel is not mandatory for every request. Explicit `invoke define` should route directly to `invoke` when enough context exists. When context is missing, Necronomicon should create or resume an active discovery/research interaction, then hand off to `invoke define` only when the required define inputs are ready or the user explicitly accepts the risk.

## Governed Knowledge Substrate

The "soul" of Necronomicon is the governed knowledge substrate: the path from raw conversation and discovery into reusable inventory, ontology candidates, reviewed premises, confidence changes, constitutions, and axioms.

Necronomicon coordinates this flow but does not promote knowledge by itself.

| Layer | Meaning | Owning Capability | Promotion Rule |
| --- | --- | --- | --- |
| Session evidence | Raw or distilled interaction history, decisions, contradictions, open questions. | Necronomicon checkpoint, `ontology-vault distill-sessions` | Evidence only; never authoritative by itself. |
| Discovery baseline | Scoped understanding of problem, users, vocabulary, constraints, and unknowns. | `discovery-to-inventory` | Can become inventory entries when source-backed. |
| Inventory knowledge | Reusable project facts, glossary terms, source summaries, and capability evidence. | `inventory`, `feature-glossary` | Durable lookup substrate; still not ontology promotion. |
| Ontology candidates | Candidate concepts, relationships, premises, branch claims, bridge edges, and drift findings. | `ontology-harness`, `ontology-vault map`, `ontology-vault distill-sessions` | Candidate-only until reviewed by owning ontology mode. |
| Premises | Working bets or assumptions under review. | `ontology-vault premise-review` | Promote, revise, split, demote, retire, or escalate. |
| Confidence states | Evidence confidence and commitment confidence for claims or premises. | `ontology-vault promote-confidence` | Promotion requires source evidence, contradiction handling, and gate compliance. |
| Constitutions | Codified governance rules, process conventions, and agent/human operating constraints. | `ontology-vault convention-update`, `decision-gate` | Require explicit approval, migration impact, and rollback path. |
| Axioms | Load-bearing truths or foundational principles that justify downstream governance. | `ontology-vault promote-confidence`, `decision-gate` | Highest bar; require strong evidence, explicit commitment, and review path. |

The normal substrate flow is:

```text
conversation / session / rough idea
  -> Necronomicon checkpoint or active interaction
  -> discovery-to-inventory
  -> inventory + glossary
  -> ontology-harness / ontology-vault map
  -> premise-review and confidence review
  -> decision-gate for consequential promotions
  -> constitution or axiom only when promotion gates pass
  -> bridge validation against system evidence
  -> Necronomicon memory and routing context
```

This flow applies across day-to-day work:

- During discovery, Necronomicon routes vague scope to `discovery-to-inventory` so findings become inventory rather than chat residue.
- During research, Necronomicon keeps raw evidence and synthesis separate, then records ontology candidates and contradictions.
- During feature definition, Necronomicon uses inventory and ontology context before handing off to `invoke define`.
- During implementation, Necronomicon preserves bridge evidence between business intent and system artifacts.
- During maintenance, Necronomicon routes repeated contradictions, route misses, or drift findings to ontology review, decision gates, or harness updates.

Promotion is deliberately slow. A session can create a candidate premise; repeated evidence can raise evidence confidence; a decision can raise commitment confidence; a convention update can produce a constitution; only heavily reviewed, load-bearing knowledge should become an axiom.

Inventory is the retrieval surface for this substrate. Necronomicon should query inventory before broad repository search when the user asks what is already known, and should propose inventorizing durable discoveries after discovery, research, decision, implementation, or maintenance work.

Use `invoke` for research only when the research is directly supporting lifecycle authoring. If the user needs evidence before there is a spec/design/plan target, Necronomicon should run harness research or `discovery-to-inventory`, then store durable results through `inventory`. If the research is feeding `invoke define`, `invoke design`, or `invoke plan`, Necronomicon may hand off the packet using the invoke research brief shape.

## What Necronomicon Is Not

- It is not a second Arcanum registry.
- It is not a copied store of canonical sigil or spell definitions.
- It is not a full local CLI engine in the first-pass runtime model.
- It is not the authority for ontology promotion, inventory promotion, lifecycle authoring, or reusable artifact creation.
- It is not raw chat transcript storage.
- It is not allowed to persist secrets.

## Trigger Conditions

- A user asks to start, create, resume, close, or maintain a Necronomicon harness.
- A user asks to run setup, checkpoint, research, or implementation-research through the harness.
- Repository work needs durable memory across repeated agent interactions.
- A request should route first through selected repository-local sigils or spells.
- A selected capability is missing and the user wants fallback suggestions from Arcanum.
- Repeated route misses suggest that the repository harness should add, remove, or refresh capabilities.

## Setup Profiles

| Profile                   | Primary Intent                                                          | Default Outcome                                              |
| ------------------------- | ----------------------------------------------------------------------- | ------------------------------------------------------------ |
| `basic-inventory`         | Lightweight harness for reusable repository memory and routing.         | Enables inventory-first setup with route/memory baseline.    |
| `ontology-harness`        | Harness with ontology governance and business/system bridge validation. | Adds ontology-vault flows and related dependencies.          |
| `research`                | Bounded evidence gathering with synthesis checkpoints.                  | Enables research policy and optional robot-talks escalation. |
| `implementation-research` | Discovery-first implementation planning before execution.               | Enables project-scoped implementation-research handoffs.     |
| `custom`                  | User-shaped capability mix with explicit trade-off decisions.           | Enables selective capabilities with dependency auto-adds.    |

Profiles are composable. Treat `basic-inventory` or `ontology-harness` as the base profile, then layer `research` and/or `implementation-research` as overlays when needed.

| Composition                                             | Expected Behavior                                                                               |
| ------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| `basic-inventory + research`                            | Inventory-first bounded research with optional web escalation.                                  |
| `ontology-harness + research`                           | Ontology-grounded bounded research using inventory, ontology outputs, and optional web sources. |
| `basic-inventory + implementation-research`             | Implementation discovery handoff using inventory/context and invoke lifecycle routing.          |
| `ontology-harness + implementation-research`            | Implementation discovery handoff with ontology constraints and invoke lifecycle routing.        |
| `ontology-harness + research + implementation-research` | Full discovery stack with ontology-grounded research and implementation handoff readiness.      |

## Dependency Rules

1. Selecting `necronomicon` for human-gated setup, checkpoint review, research clarification, or maintenance decisions requires `structured-interview-kits`.
2. Selecting `ontology-vault` auto-adds `inventory` and `context-builder`.
3. Selecting `ontology-harness` auto-adds `ontology-vault`, `inventory`, and `context-builder`.
4. `research` may recommend `robot-talks` only as escalation for cross-layer contradictions.
5. `implementation-research` requires a research project scope and handoff target before execution routing.
6. Any auto-added dependency must be written into capability update records and setup decisions.
7. `observability-setup`, `signal-observer`, and `workflow-reflect` are required for Necronomicon telemetry, signal capture, and maintenance reflection.
8. `spellcraft` and `sigil-development` are required authoring paths for approved maintenance outcomes.
9. `invoke` is the required lifecycle authoring spell for implementation-research handoffs and define/design/plan/full/validate requests when installed.
10. `research` and `implementation-research` are composable overlays and are not mutually exclusive with `basic-inventory` or `ontology-harness`.
11. When `implementation-research` is selected without `research`, Necronomicon should request missing research scope inputs and continue with a constrained implementation-research handoff.
12. When `ontology-harness` is active, research and implementation-research flows must use ontology outputs before relying on external web sources.
13. `maintain` mode must aggregate signals from all selected sigils and spells, not only route-level telemetry.
14. `sigil-maintenance-loop` is required for cross-sigil maintenance synthesis when available in the installed spell surface.

## Required Sigils And Spells

| Artifact                    | Role In Spell                                                                                                            | Required Mode                                                                             |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------- |
| `ontology-harness`          | Provide ontology governance, session distillation, premise review, branch mapping, and bridge validation contract.       | direct or delegated                                                                       |
| `inventory`                 | Track repository knowledge entries and capability evidence when inventory exists.                                        | lookup, ingest, validate                                                                  |
| `context-builder`           | Build compact context packs for session resume, routing, and evidence retrieval.                                         | lean, standard, or deep                                                                   |
| `structured-interview-kits` | Provide one-question setup and decision interview modes for human-gated Necronomicon flows.                              | setup-profile, gap-check, checkpoint-review, research-clarification, maintenance-decision |
| `observability-setup`       | Initialize and validate repository-local telemetry paths used by Necronomicon.                                           | setup, validate, maintain                                                                 |
| `signal-observer`           | Capture route misses, outcomes, and quality gaps as structured maintenance signals.                                      | post-route, maintain                                                                      |
| `workflow-reflect`          | Analyze accumulated signals into evidence-backed maintenance recommendations.                                            | maintain, closeout                                                                        |
| `spellcraft`                | Author or revise local and reusable spells from approved maintenance recommendations.                                    | maintain, compose                                                                         |
| `sigil-development`         | Author or revise local and reusable sigils from approved maintenance recommendations.                                    | maintain, author                                                                          |
| `sigil-maintenance-loop`    | Consolidate and prioritize cross-sigil maintenance actions from accumulated signal evidence.                             | maintain, reflect                                                                         |
| `invoke`                    | Provide unified define/design/plan/full/validate lifecycle authoring and implementation-research handoff execution.      | route, implementation-research, maintain                                                  |

## Recommended Capabilities

| Capability                | Use When                                                                         | Notes                                              |
| ------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------- |
| `task-session`            | A routed request resolves to one bounded implementation or documentation task.   | Use for scoped execution with decisions and gates. |
| `decision-gate`           | Capability updates, ontology promotions, or route ambiguity require user choice. | Ask only consequential questions.                  |
| `sigil-runtime-installer` | Selected capabilities need generated runtime command adapters.                   | Use for add, remove, or refresh operations.        |

## Interview Modes

Necronomicon uses `structured-interview-kits` for human-gated flows.

| Interview Mode           | Use When                                                | Expected Outcome                                      |
| ------------------------ | ------------------------------------------------------- | ----------------------------------------------------- |
| `setup-profile`          | First run, profile change, or missing setup decisions.  | Selected setup profile and persisted setup rationale. |
| `gap-check`              | Route misses, contradictions, or unresolved scope.      | Gap entries and next recommended route.               |
| `checkpoint-review`      | Checkpoint candidates need user confirmation or triage. | Candidate routing decisions and updated gap ledger.   |
| `research-clarification` | Research question or scope is underspecified.           | Bounded research brief inputs.                        |
| `maintenance-decision`   | Maintenance mode proposes route/capability changes.     | Approved, deferred, or rejected maintenance actions.  |

## Optional Capabilities

| Capability                       | Use When                                                                                                | Notes                                       |
| -------------------------------- | ------------------------------------------------------------------------------------------------------- | ------------------------------------------- |
| `ontology-vault`                 | Session memory needs ontology distillation, premise review, confidence promotion, or bridge validation. | Usually present through `ontology-harness`. |
| `architecture-pattern-inventory` | Routing or ontology branches depend on repository structure.                                            | Useful for system/runtime branches.         |
| `feature-glossary`               | The session needs plain-language concept summaries.                                                     | Explanatory, not authoritative.             |

## Modes

| Mode                      | Purpose                                                                                                  | Primary Outputs                                            |
| ------------------------- | -------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| `setup`                   | Establish or revise setup profile, policies, and capability baseline.                                    | setup decisions, profile summary, manifest updates         |
| `start`                   | Create a new repository harness session.                                                                 | session folder, memory seed, capability manifest reference |
| `resume`                  | Continue from existing memory, decisions, and route history.                                             | refreshed context summary, next action                     |
| `route`                   | Route a user request through selected Necronomicon capabilities.                                         | selected command, route record, result summary             |
| `checkpoint`              | Distill session state into gated candidate and gap artifacts.                                            | checkpoint artifact, candidate list, route recommendations |
| `research`                | Run bounded repository and web research with source trail and synthesis gate.                            | research brief, contradictions, post-research options      |
| `implementation-research` | Run project-scoped implementation discovery before execution as a composable overlay with base profiles. | implementation handoff, invoke route recommendation        |
| `update-capabilities`     | Add, remove, or refresh selected sigils and spells.                                                      | capability update report, regenerated runtime command plan |
| `fallback-discover`       | Offer Arcanum registry candidates when no selected capability matches.                                   | candidate list, user decision, optional update path        |
| `maintain`                | Propose harness improvements from telemetry, misses, and repeated gaps.                                  | maintenance report, approved update actions                |
| `close`                   | Write final memory, decisions, route summary, and handoff.                                               | handoff artifact, observability summary                    |

## Prerequisites

- Repository root is known.
- Arcanum runtime support is installed or the user approves installation.
- `.arcanum/observability/` exists or can be initialized.
- `invoke` should be installed for lifecycle authoring and implementation-research handoff routing; if missing, installation approval is required.
- The active runtime command surface is known when command execution is requested.

## Shared State

| State                                                      | Owner      | Updated By                           | Consumed By                            |
| ---------------------------------------------------------- | ---------- | ------------------------------------ | -------------------------------------- |
| `.arcanum/necronomicon/README.md`                          | repository | bootstrap or harness spell           | user, local agents                     |
| `.arcanum/necronomicon/capabilities.json`                  | repository | bootstrap, capability update flow    | session router                         |
| `.arcanum/necronomicon/setup-decisions.md`                 | repository | setup mode, profile updates          | setup, resume, maintain                |
| `.arcanum/necronomicon/gaps.json`                          | repository | checkpoint, research, maintain       | setup, route, maintain                 |
| `.arcanum/necronomicon/routes/common-routes.json`          | repository | setup, maintain, update-capabilities | route, maintain                        |
| `.arcanum/necronomicon/sessions/<session-id>/SESSION.md`   | session    | harness spell                        | user, resume flow                      |
| `.arcanum/necronomicon/sessions/<session-id>/memory.md`    | session    | harness spell, close flow            | resume flow, router                    |
| `.arcanum/necronomicon/sessions/<session-id>/routes.jsonl` | session    | route flow                           | resume flow, signal observer           |
| `.arcanum/necronomicon/sessions/<session-id>/decisions.md` | session    | decision gate, harness spell         | resume flow, user                      |
| `.arcanum/necronomicon/sessions/<session-id>/active-interaction.json` | session | harness spell, active capability | turn classification, resume flow       |
| `.arcanum/necronomicon/sessions/<session-id>/checkpoints/` | session    | checkpoint mode, close flow          | resume, route, maintenance             |
| `.arcanum/necronomicon/research/<project-id>/`             | repository | implementation-research mode         | implementation-readiness, task-session |
| `.arcanum/necronomicon/maintenance/<date>-report.md`       | repository | maintain mode                        | capability updates, local authors      |
| `.arcanum/necronomicon/sessions/<session-id>/handoff.md`   | session    | close flow                           | future sessions                        |
| `.arcanum/necronomicon/capability-updates/`                | repository | update-capabilities flow             | bootstrap, sigil-runtime-installer     |
| `.arcanum/observability/`                                  | repository | harness spell and routed commands    | reflection workflows                   |

## Runtime UX Contract

1. Setup is interview-driven: ask one question at a time using `setup-profile` mode.
2. Profile selection and profile changes use option cards with:
   - what the profile enables,
   - what it costs,
   - what state it creates,
   - recommended default,
   - when to avoid it.
3. When a later answer implies profile or capability mutation, require a gated confirmation card before writing state.
4. Confirmation cards must include current value, proposed value, reason, auto-added dependencies, consequences, rejected alternatives, and target update path.
5. Ask only unanswered setup questions when setup decisions already exist.
6. Generated state must redact or omit secret values.

## Checkpoint And Memory Policy

1. Checkpoint triggers include user request, before close, before capability updates, after major research synthesis, after repeated route misses, and before implementation transitions.
2. Checkpoints write to `.arcanum/necronomicon/sessions/<session-id>/checkpoints/<timestamp>.md`.
3. Checkpoint content separates source-backed facts, inferred claims, decisions, contradictions, unresolved questions, route patterns, capability gaps, and promotion candidates.
4. Promotion candidates remain candidate-only and must route through owning flows (`inventory`, `ontology-vault`, `decision-gate`).
5. Memory classes tracked by Necronomicon are project memory, session memory, route memory, user instruction memory, and ontology candidate memory.
6. Gap-related unresolved items from checkpoints are written to `.arcanum/necronomicon/gaps.json`.
7. Checkpoint and memory artifacts must apply state privacy redaction before persistence.

## Research Scope Policy

1. Research mode uses a bounded source order: session memory and checkpoints, inventory, ontology outputs, repository docs, code, then web sources.
2. Web research is allowed when the active runtime and tool surface support external fetch/search operations.
3. If web access is unavailable, run repository-only research and return a `web-unavailable` note in the result.
4. Web findings must include source URL, retrieval timestamp, and confidence or quality notes before durable synthesis.
5. Contradictions between local and web sources must be captured in the research brief and gap ledger before promotion.
6. When `ontology-harness` is active, ontology outputs are required local sources before web escalation.

## Maintenance Loop

1. `maintain` mode reads route misses, corrections, repeated tasks, capability updates, quality gaps, output drift, and all selected sigil/spell signals from local observability telemetry.
2. Maintenance must read the gap ledger before proposing actions.
3. Use `signal-observer`, `workflow-reflect`, and `sigil-maintenance-loop` to produce evidence-backed recommendations.
4. Maintenance should flag selected capabilities with missing or stale signal coverage as explicit maintenance gaps.
5. Recommendation classes include route preset updates, capability updates, setup profile revisions, local spell proposals, reusable spell proposals, local sigil proposals, reusable sigil proposals, and defer.
6. Route spell creation through `spellcraft` and sigil creation through `sigil-development`.
7. Require explicit user approval before creating or promoting reusable artifacts.

## Execution Phases

| Phase | Capability             | Input                                                 | Output                             | Gate                               | Failure Policy                                   |
| ----- | ---------------------- | ----------------------------------------------------- | ---------------------------------- | ---------------------------------- | ------------------------------------------------ |
| 1     | setup resolver         | repository root, mode, existing decisions             | selected profile and policy draft  | required setup decisions exist     | run `setup-profile` interview mode               |
| 2     | capability load        | `capabilities.json`, setup decisions, runtime folders | selected command surface           | selected capabilities are readable | flag stale entries                               |
| 3     | memory and gap load    | memory, decisions, checkpoints, `gaps.json`           | compact session + open-gap context | source context is explicit         | start fresh session memory if missing            |
| 4     | interaction classification | user request, active interaction, profile, route presets | continuation, handoff, or route candidates | active pending response is honored | ask whether to continue or route fresh when ambiguous |
| 5     | selected routing       | selected capabilities and policy gates                | chosen local command               | command adapter exists             | fallback discover when no selected match exists  |
| 6     | bounded execution      | chosen command and mode contract                      | routed result and active interaction update | mode-specific gate satisfied       | report partial and next safest route             |
| 7     | checkpoint handling    | route result and checkpoint policy                    | checkpoint artifact and candidates | candidate-only promotions enforced | defer promotions to owning flows                 |
| 8     | gap ledger update      | unresolved items, contradictions, misses              | updated `gaps.json` entries        | JSON remains valid                 | flag when ledger write fails                     |
| 9     | maintenance evaluation | route history and observability signals               | maintenance recommendations        | evidence cited for recommendations | defer unsupported recommendations                |
| 10    | close or continue      | session status and next action                        | handoff or resumable continuation  | blockers named                     | leave session resumable                          |

## Routing Rules

1. Load the active session memory, decisions, active interaction, route history, and capability manifest before routing.
2. Prefer explicit runtime command names, exact spell IDs, exact sigil IDs, and exact aliases.
3. If an active interaction is awaiting user input, continue that owning capability unless the user clearly interrupts.
4. Route setup, start, create, resume, close, memory, handoff, checkpoint, research, implementation-research, maintenance, capability update, or fallback discovery requests to this spell.
5. Route ontology, vault, premise, confidence, convention, branch map, session distillation, and bridge validation requests to `ontology-harness` or `arcanum-ontology-harness`.
6. Route one bounded task with done criteria to `task-session` when selected.
7. Route compact evidence or context pack requests to `context-builder` when selected.
8. Route unclear feature definition requests through discovery and research before `invoke define` unless enough define inputs already exist.
9. If no selected route matches, inspect installed command surfaces and canonical Arcanum registries when available.
10. Offer 2-5 fallback sigils or spells with the reason each candidate may fit.
11. Ask before adding fallback candidates to the Necronomicon capability manifest.
12. Record every route attempt in `routes.jsonl` with request summary, candidates, selected route, confidence, fallback use, result, validation, active interaction status, and follow-up.
13. Route ontology promotion candidates through `ontology-vault` flows, inventory candidates through inventory flows, and consequential unresolved choices through `decision-gate`.
14. In `research` mode, include web sources when runtime support is available and preserve bounded stop conditions.
15. Route lifecycle authoring requests (`define`, `design`, `plan`, `full`, `validate`) and implementation-research handoffs to `arcanum-spell-invoke` when installed.
16. If `invoke` is unavailable for those routes, report a capability gap and route to `update-capabilities` for install approval.
17. Route cross-sigil maintenance synthesis to `arcanum-spell-sigil-maintenance-loop` when installed, and report a maintenance capability gap when it is missing.

## Route Confidence

| Confidence | Meaning                                                                         |
| ---------- | ------------------------------------------------------------------------------- |
| high       | Explicit command name, exact canonical ID, or exact alias.                      |
| medium     | Selected capability trigger, description, or mode strongly matches the request. |
| low        | Fallback registry candidate may fit but is not selected in the session.         |
| block      | No credible selected or fallback route exists.                                  |

Ask one focused clarification when multiple medium or high routes tie.

## Capability Update Flow

1. Read `.arcanum/necronomicon/capabilities.json` and the installed runtime command folders.
2. Identify stale selected entries, missing adapters (including missing `invoke` lifecycle route coverage), new available Arcanum registry entries, and repeated route misses.
3. Identify missing or stale signal coverage for selected sigils/spells and prioritize maintenance-loop remediation.
4. Present add, remove, refresh, or author options.
5. Use `sigil-runtime-installer` or bootstrap to regenerate runtime commands when installation changes are approved.
6. Use `spellcraft` or `sigil-development` when the needed behavior does not exist yet.
7. Write a report under `.arcanum/necronomicon/capability-updates/`.
8. Update session memory and route future matching through the new capability set.

## Local Customization

- Harness root: `.arcanum/necronomicon/`
- Session root: `.arcanum/necronomicon/sessions/`
- Capability manifest: `.arcanum/necronomicon/capabilities.json`
- Runtime adapter root: `.arcanum/runtimes/`
- Observability root: `.arcanum/observability/`
- Default memory strictness: standard
- Default fallback policy: ask-before-add
- Default session ID format: timestamp plus slug, for example `2026-05-14-sonar-loop-routing`
- Default checkpoint policy: standard
- Default profile when unspecified: `basic-inventory`

## Guardrails

- Do not copy canonical sigil or spell definition folders into `.arcanum/necronomicon/`.
- Do not make session memory authoritative over source documents, registries, or implementation evidence.
- Do not add fallback capabilities silently.
- Do not mark a route successful if the selected command was unavailable or its validation failed.
- Keep durable memory concise and resumable; avoid storing raw full chat transcripts unless the user explicitly requests that.
- Preserve unrelated local runtime commands and discovery bridges.
- Do not persist credentials, passwords, API keys, private keys, or secret values in Necronomicon state.
- Do not auto-create reusable spells or sigils from maintenance suggestions without explicit user approval.

## Observability

Record session-level telemetry when `.arcanum/observability/` exists:

- spell name,
- mode,
- session ID,
- selected capability count,
- request classification,
- route confidence,
- selected command,
- selected profile,
- checkpoint trigger and artifact path,
- research mode budget and stop condition,
- web source usage and web-unavailable fallback status,
- implementation-research handoff status,
- per-sigil signal coverage and stale-signal flags,
- maintenance recommendation classes,
- fallback candidates offered,
- capability updates proposed or applied,
- files changed,
- validation result,
- blockers,
- follow-up actions.

## Output Contract

Return:

```markdown
## Spell Result

- Spell: Necronomicon
- Canonical ID: necronomicon
- Mode: setup | start | resume | route | checkpoint | research | implementation-research | update-capabilities | fallback-discover | maintain | close
- Profile: basic-inventory | ontology-harness | research | implementation-research | custom
- Repository: <path>
- Session ID: <id>
- Capabilities loaded: <count>
- Route: <selected command or none>
- Route preset used: <id or none>
- Confidence: high | medium | low | block
- Fallback offered: yes | no
- Checkpoint: written | skipped | n/a
- Research brief: path or none
- Implementation handoff: path or none
- Invoke route: used | missing | n/a
- Gap ledger updates: <count or none>
- Maintenance recommendations: <count or none>
- Files updated: <paths or none>
- Validation: <checks>
- Follow-up: <items or none>
```

````
