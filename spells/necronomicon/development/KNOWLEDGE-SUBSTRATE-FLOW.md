# Necronomicon Knowledge Substrate Flow

## Purpose

Clarify how Necronomicon's day-to-day harness flow interacts with discovery, inventory, ontology governance, axioms, constitutions, premises, confidence levels, and bridge evidence.

This is the inner loop that gives the harness continuity and judgment. Without it, Necronomicon is only a command router.

## Core Idea

Necronomicon turns repeated work into governed knowledge.

It does this by moving material through increasingly strict states:

```text
raw interaction
  -> session evidence
  -> discovery baseline
  -> inventory knowledge
  -> ontology candidate
  -> reviewed premise
  -> confidence decision
  -> constitution or axiom
  -> bridge-validated operating context
```

Each state has a different authority level. The harness may collect, remember, and route candidates, but promotion belongs to the owning capability.

## Authority Ladder

| State | Authority | Typical Source | Owner | Can Necronomicon Create It? | Can Necronomicon Promote It? |
| --- | --- | --- | --- | --- | --- |
| Raw interaction | Very low | Chat, notes, user answer | Session | yes | no |
| Session evidence | Low | Checkpoint, route record, handoff | Necronomicon | yes | no |
| Discovery baseline | Low-medium | Scope interview, brownfield scan | `discovery-to-inventory` | route/create via owner | no |
| Inventory entry | Medium | Source-backed discovery, docs, code summaries | `inventory` | route/create via owner | no |
| Glossary term | Medium | Discovery baseline, local vocabulary | `feature-glossary` | route/create via owner | no |
| Ontology candidate | Medium | Inventory, sessions, research, ontology map | `ontology-vault` | collect as candidate | no |
| Premise | Medium, explicitly uncertain | Candidate claim or working bet | `ontology-vault premise-review` | collect as candidate | no |
| Confidence decision | Medium-high | Evidence and commitment review | `ontology-vault promote-confidence` | no | no |
| Constitution | High | Approved convention or process rule | `ontology-vault convention-update`, `decision-gate` | no | no |
| Axiom | Highest | Load-bearing reviewed principle | `ontology-vault`, `decision-gate` | no | no |
| Bridge evidence | Alignment-specific | Tests, telemetry, code, docs, drift reports | `ontology-harness`, `ontology-vault validate` | collect as candidate | no |

## Capability Roles

| Capability | Role In The Substrate |
| --- | --- |
| Necronomicon | Owns active interaction, session memory, route ledger, checkpoints, gaps, and handoffs. |
| `discovery-to-inventory` | Converts vague or brownfield discovery into source-backed baseline, glossary, and inventory entries. |
| `inventory` | Stores reusable source-backed knowledge and lookup entries. |
| `feature-glossary` | Clarifies vocabulary so later ontology and define work use stable language. |
| `ontology-harness` | Orchestrates ontology governance across inventory, ontology-vault, and context-builder. |
| `ontology-vault` | Owns ontology mapping, premise review, confidence promotion/demotion, convention updates, and bridge validation. |
| `decision-gate` | Resolves consequential promotions, trade-offs, conventions, and commitment choices. |
| `invoke` | Uses approved context to define, design, plan, and validate development artifacts. |
| `task-session` | Executes bounded implementation or documentation work after enough definition exists. |

## Inventory UX Loop

Inventory should feel like a quiet memory layer, not a filing chore.

Necronomicon should expose inventory through three user-facing motions:

| Motion | User Experience | Internal Route |
| --- | --- | --- |
| Inventorize | "Keep this so we do not rediscover it later." | checkpoint -> `discovery-to-inventory` or `inventory ingest` |
| Retrieve | "What do we already know about this?" | `inventory lookup` before broad source search |
| Reconcile | "This conflicts with what we knew." | `inventory lint` or contradiction entry, then ontology review if consequential |

The agent should not ask the user to choose files and entry types unless the choice affects meaning. In normal use it should:

1. detect whether inventory exists;
2. search inventory before raw files for durable project questions;
3. name retrieved entries briefly and cite paths or selectors;
4. mark missing coverage as a gap instead of pretending the memory is complete;
5. offer to inventorize durable findings after discovery, research, implementation, or decision work.

Inventory retrieval should return task-shaped context, not a wiki dump:

```text
query
  -> matching inventory entries
  -> source selectors
  -> confidence and gaps
  -> task obligation fit
  -> recommended next route
```

This keeps the user experience fast: the user asks a normal question, Necronomicon retrieves relevant inventory in the background, and only surfaces the parts that affect the next decision.

## Research Entry And Invoke Boundary

Not every research run should call `invoke`.

Necronomicon has two research surfaces:

| Surface | Owner | Use When | Output |
| --- | --- | --- | --- |
| Harness research | Necronomicon, optionally `discovery-to-inventory` and `inventory` | The user needs evidence, discovery, or reusable knowledge before a lifecycle artifact exists. | Research packet, inventory candidates, gaps, next route. |
| Invoke research companion | `invoke` | Research is directly supporting `define`, `design`, or `plan`. | `invoke` research brief using the selected template family. |

The `invoke` research templates are useful shapes for evidence tables, contradictions, gaps, options, and gate results. Necronomicon may reuse that shape for a harness research packet, but the route should not become `invoke` unless the user is asking for lifecycle authoring or the research has a clear handoff into `invoke define`, `invoke design`, or `invoke plan`.

Recommended rule:

```text
research to understand -> Necronomicon research or discovery-to-inventory
research to remember -> inventory ingest or query synthesis
research to govern claims -> ontology-harness / ontology-vault
research to author a spec/design/plan -> invoke with research companion
```

When a harness research packet becomes durable, route it to inventory as one or more entries:

- source summaries for important source documents,
- concept entries for reusable ideas,
- decision entries for selected options,
- contradiction entries for unresolved conflicts,
- synthesis entries for cross-source answers.

When the packet becomes authoring input, hand it to `invoke` as context and include:

- research question,
- scope boundary,
- source ledger,
- claim status,
- contradictions,
- unresolved gaps,
- decision options,
- inventory selectors,
- ontology or confidence gaps.

## Flow Through A Feature

When a user says, "I want a billing export feature," Necronomicon should not assume this is ready for `invoke define`.

Recommended flow:

1. **Active interaction starts:** Necronomicon records a discovery interaction and asks only for missing high-signal scope.
2. **Discovery baseline:** route to `discovery-to-inventory` when the idea is vague, brownfield, or vocabulary-heavy.
3. **Inventory update:** persist source-backed facts, terms, known constraints, and unresolved gaps.
4. **Ontology candidate extraction:** if the feature touches domain rules, policies, user roles, or business/system alignment, route candidates to `ontology-harness`.
5. **Premise review:** if a claim is a working bet, route to `ontology-vault premise-review`.
6. **Confidence review:** if the team wants to rely on the claim, route to `ontology-vault promote-confidence`.
7. **Decision gate:** if promotion changes behavior, conventions, architecture, or commitment, ask for explicit approval.
8. **Define:** once intent, vocabulary, constraints, and unresolved gaps are explicit, route to `invoke define`.
9. **Bridge validation:** as implementation appears, route business/system alignment checks through `ontology-harness` or `ontology-vault validate`.
10. **Checkpoint:** Necronomicon records decisions, candidates, gaps, handoff, and next route.

## Axiom And Constitution Promotion

Axioms and constitutions should be rare.

| Candidate Type | Promotion Trigger | Required Evidence |
| --- | --- | --- |
| Premise | A working bet needs review or is blocking definition/design. | Supporting evidence, counterevidence, usage, falsification criteria. |
| Constitution | A repeated operating rule needs codification. | Current rule, proposed rule, affected flows/files, migration impact, rollback path, approval. |
| Axiom | A load-bearing principle justifies many downstream rules. | Strong evidence, repeated use, contradiction review, explicit commitment, review path. |

Necronomicon may say "this looks like a candidate premise/constitution/axiom." It must not say "this is now an axiom" without the owning ontology and decision gates.

## Confidence Model

Necronomicon must preserve the split used by Ontology Vault:

| Confidence Type | Question It Answers | Example |
| --- | --- | --- |
| Evidence confidence | How well is this claim supported by sources or observed reality? | "We have tests and telemetry showing this behavior." |
| Commitment confidence | How strongly should the project rely on this claim right now? | "We are willing to design the plan around this premise." |

The split matters because a project can have:

- high evidence, low commitment: true but not strategically important,
- low evidence, low commitment: exploratory idea,
- low evidence, high commitment: dangerous bet needing explicit gate,
- high evidence, high commitment: promotion candidate.

## Interaction With Active Turns

The knowledge substrate depends on the active interaction model.

If Necronomicon is in a discovery, research, premise-review, or confidence-review loop, user replies should continue that loop by default. The reply should update the active artifact and only then decide whether to:

- ask the next question,
- route to another capability,
- checkpoint,
- mark a gap,
- or hand off to `invoke define`, `invoke plan`, or `task-session`.

Side notes are the exception that should not derail the loop. When the user says "side note", "for later", "research idea", "parking lot", or gives an otherwise related fact while work is running, Necronomicon should capture it as session evidence and classify it separately:

| Side Note Class | Substrate Destination |
| --- | --- |
| Active artifact input | Attach to current discovery, research packet, define record, plan, or task context. |
| Durable project fact | Candidate for `inventory ingest` or `discovery-to-inventory`. |
| Research idea | Research backlog item with scope, source, and stop-condition gaps. |
| Related unblocker | Bounded side task whose result can unblock the active decision, definition, design, or plan. |
| Contradiction | Inventory lint gap, ontology candidate, or decision-gate candidate depending on impact. |
| Governance claim | Candidate premise, confidence review input, constitution candidate, or axiom candidate. |
| Reminder | Deferred follow-up item in the side note queue. |

The default closeout for side notes is compact triage, not immediate execution. Related unblockers are the exception: if the task is narrow, safe, and blocks the current work, Necronomicon may run or queue it immediately while preserving the active interaction.

Examples:

- get current API prices for a vendor comparison,
- check one vendor quota or limit,
- confirm the latest package version when planning an integration,
- locate the repository file that owns a behavior,
- fetch one policy or migration guide needed by the active decision.

At checkpoint time, Necronomicon should report what was attached, what should be inventorized, what should become research, what unblockers ran or remain queued, what needs governance, and what remains parked.

## State Artifacts

| Artifact | Purpose |
| --- | --- |
| `active-interaction.json` | Remembers whether the next user turn continues discovery, research, premise review, decision gate, or task execution. |
| `side-notes.jsonl` | Captures side notes, research seeds, parking-lot items, and mid-run facts without replacing the active interaction. |
| `memory.md` | Human-readable session continuity. |
| `routes.jsonl` | Routing evidence and route confidence. |
| `gaps.json` | Unresolved questions, contradictions, blocked decisions, capability gaps, and promotion gaps. |
| `checkpoints/<timestamp>.md` | Durable distillation of facts, inferences, decisions, contradictions, candidates, and next routes. |
| `research/<project-id>/` | Bounded evidence trail and synthesis artifacts. |
| ontology outputs | Maps, premise reviews, confidence reports, convention updates, bridge validations. |

## Rules Of Thumb

- Discovery creates candidates; inventory makes source-backed knowledge reusable.
- Inventory entries can inform ontology, but they are not ontology promotions.
- Ontology candidates can inform define/design, but unresolved promotion gaps must stay visible.
- A premise is a useful uncertainty, not a truth.
- A constitution is a codified operating rule, not a casual preference.
- An axiom is a load-bearing principle, not a slogan.
- Bridge evidence is required before claiming that implementation realizes intent.
- Necronomicon remembers and routes; ontology-vault promotes or demotes.

## Next Implementation Slice

1. Add substrate fields to `active-interaction.json`: candidate type, authority level, owning capability, promotion status, and next gate.
2. Extend checkpoint shape with `knowledge_candidates`: inventory entries, ontology concepts, premises, constitutions, axioms, bridge edges, and confidence changes.
3. Add route presets from discovery to `discovery-to-inventory`, from inventory to `ontology-harness`, and from reviewed context to `invoke define`.
4. Add a worked example from rough feature idea to inventory entry, premise review, `invoke define`, and checkpoint.
