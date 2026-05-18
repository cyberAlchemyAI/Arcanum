# Necronomicon Day-To-Day Usage Vision

## Purpose

Define how a repository user should experience Necronomicon during ordinary work, so implementation can iterate toward a concrete product shape instead of only a capability map.

## Vision Statement

Necronomicon is the repository's persistent working memory and routing desk.

It should let a user return to a repository, ask in normal language what they want to do next, and rely on the harness to recover relevant context, choose or suggest the right installed Arcanum capability, record what happened, and keep future sessions resumable.

## Product Promise

After Necronomicon is set up, the user should feel three things:

1. **Continuity:** "The repo remembers where we left off."
2. **Routing relief:** "I do not need to remember every sigil or spell name."
3. **Traceability:** "Important decisions, gaps, and routes are captured without turning chat into a source of truth."

## Primary User

The primary user is a repository operator working with an agent across repeated sessions. They may be designing a feature, maintaining a framework, researching a decision, implementing a task, or cleaning up workflow drift.

They know the repository goal, but they should not need to know the whole Arcanum command catalog.

## Daily Loop

| Moment | User Says | Necronomicon Should |
| --- | --- | --- |
| Start | "Resume Necronomicon." | Load setup decisions, active memory, recent route history, open gaps, and last checkpoint. |
| Orient | "Where are we?" | Return a compact status: current focus, last decisions, blockers, suggested next route. |
| Continue | "Keep going on the implementation plan." | Route to `invoke`, `implementation-readiness`, or `task-session` using prior memory. |
| Clarify | "What is still unclear?" | Read gaps, route misses, contradictions, and candidate decisions. |
| Research | "Check the evidence before we decide." | Create a bounded research brief, use local sources first, then web when available and allowed. |
| Decide | "Which path should we take?" | Route consequential choices through `decision-gate` or the owning capability. |
| Execute | "Implement the next slice." | Route to the task owner, then record result, validation, and follow-up. |
| Preserve | "Checkpoint this." | Distill facts, inferred claims, decisions, contradictions, gaps, and promotion candidates. |
| Improve | "This workflow keeps missing." | Run maintenance from route history, telemetry, gaps, and selected capability signals. |
| Close | "Wrap this session." | Write handoff, memory update, route summary, validation status, and next action. |

## Everyday Commands

These are the commands and natural-language forms the user should naturally reach for.

| User Form | Expected Mode | Expected Behavior |
| --- | --- | --- |
| `necronomicon start` | `start` | Create or select a session and seed memory. |
| `necronomicon resume` | `resume` | Load prior state and summarize next options. |
| `necronomicon route "..."` | `route` | Classify the request and delegate to the selected capability. |
| `necronomicon research "..."` | `research` | Run bounded evidence gathering with a synthesis gate. |
| `necronomicon checkpoint` | `checkpoint` | Write durable memory and update gaps. |
| `necronomicon maintain` | `maintain` | Propose harness improvements from evidence. |
| `necronomicon close` | `close` | Write final memory, handoff, and follow-up. |
| "Where were we?" | `resume` | Summarize active state and recommended next route. |
| "Continue this feature." | `route` | Use memory to route to implementation or planning owner. |
| "What should I run for this?" | `fallback-discover` or `route` | Suggest 2-5 candidate capabilities with confidence. |

## UX Principles

- **Plain language first:** explicit commands are supported, but the harness should understand normal work requests.
- **Continuation before routing:** when a capability is waiting for the user's answer, treat the next turn as part of that active interaction unless the user clearly interrupts.
- **One question when stuck:** ask only one focused clarification when route confidence is tied or blocked.
- **Owner routing:** Necronomicon records and coordinates; owning sigils and spells execute specialized work.
- **Concise memory:** store durable summaries, decisions, gaps, and route evidence, not raw transcript dumps.
- **Local-first evidence:** use session memory, inventory, ontology outputs, docs, and code before web research.
- **Candidate-only promotion:** checkpointed insights are candidates until inventory, ontology-vault, or a gate promotes them.
- **Side notes without derailment:** let users add project facts, research ideas, or reminders while another flow is active.
- **No silent capability changes:** adding, removing, or refreshing capabilities requires an explicit decision record.
- **Maintenance from evidence:** improve routes and capabilities from repeated misses, user corrections, gaps, and telemetry.

## State The User Should See

Necronomicon should expose state in human terms:

| State | User-Facing Meaning |
| --- | --- |
| Current focus | The work Necronomicon thinks the session is about. |
| Last useful checkpoint | The latest durable summary worth resuming from. |
| Open gaps | Questions, contradictions, missing evidence, or blocked decisions. |
| Route history | What Necronomicon tried, why, and whether it worked. |
| Suggested next routes | Likely next actions with confidence and rationale. |
| Maintenance suggestions | Evidence-backed improvements to routes, capabilities, or profiles. |

## Active Interaction Model

Necronomicon needs an explicit turn-state model so it knows whether a user message is a new request or an answer inside an existing flow.

The default rule is: **continue the active interaction before routing fresh**.

If Necronomicon or a routed capability has just asked the user for a research clarification, setup choice, decision approval, feature boundary, artifact path, or implementation choice, the next user turn belongs to that active interaction. A fresh route starts only when the user clearly names a new command, changes topic, cancels, asks to checkpoint/close, or gives an answer that cannot fit the pending prompt.

| Incoming Turn | Active Interaction Exists? | Default Interpretation |
| --- | --- | --- |
| "Yes, use option B." | yes, awaiting decision | Apply to active decision or interview. |
| "The target user is a platform admin." | yes, awaiting feature clarification | Apply to active discovery/define flow. |
| "Search the web too." | yes, active research | Update research scope and continue research. |
| "Actually checkpoint this first." | yes | Interrupt active flow, checkpoint, then offer to resume. |
| "`invoke define` this now." | yes or no | Explicit command wins; hand off or ask whether to abandon active flow if risky. |
| "What were we doing?" | yes | Summarize active interaction and pending prompt. |
| "Start a new task." | yes | Ask one confirmation before abandoning or pausing active flow. |
| "Side note: the billing API has a daily export limit." | yes | Capture as a side note, link if relevant, and keep active flow running. |
| "Research idea for later: compare queue backoff policies." | yes | Add to research backlog unless the user says to switch now. |

An active interaction should record:

| Field | Example |
| --- | --- |
| Owning capability | `necronomicon research`, `invoke define`, `structured-interview-kits`, `decision-gate` |
| Pending prompt | "Which source scope should research include?" |
| Expected answer | option choice, free text, approval, correction, artifact path |
| Current artifact | research brief, define intent record, decision record, checkpoint candidate |
| Handoff target | `invoke define`, `invoke plan`, `task-session`, `deferred` |
| Side note queue | durable facts, research seeds, reminders, contradictions, follow-up ideas |

This applies to any sigil or spell that can ask the user something. Necronomicon owns the active interaction record; the owning capability owns the semantics of the answer.

## Side Note Ergonomics

Sometimes the user is waiting for work to finish, thinking out loud, or adding a related fact that should not hijack the active flow.

Necronomicon should support lightweight side notes:

| Side Note Type | Example | Default Handling |
| --- | --- | --- |
| Project fact | "Side note: the billing API has a daily export limit." | Capture as session evidence, suggest inventory if durable. |
| Research seed | "Research idea: compare webhook retry strategies." | Add to research backlog with source/scope gaps. |
| Related unblocker | "Can you get current API prices while this runs?" | Create a bounded side task if it unblocks a decision or plan. |
| Contradiction | "This conflicts with what we said about admin roles." | Record contradiction and route to inventory lint, ontology, or decision review if consequential. |
| Reminder | "Remember to check the migration guide later." | Add follow-up item without changing the current route. |
| Active-task input | "Also, the export must be CSV." | If it fits the active artifact, attach it to the active interaction. |

The ergonomic rule is: **capture first, switch only on intent**.

If the user marks the message as a note, aside, reminder, idea, parking-lot item, or "for later", Necronomicon should not abandon the active interaction. It should acknowledge briefly, record the item, and continue or resume the active work.

If the side note is directly relevant to the active artifact, Necronomicon can attach it to that artifact and say so. If it is related but not immediately needed, place it in the side note queue and expose it at checkpoint or resume time.

Suggested side note states:

| State | Meaning |
| --- | --- |
| `captured` | Recorded but not triaged. |
| `attached` | Applied to the current active interaction or artifact. |
| `inventorize-candidate` | Durable enough to route to inventory. |
| `research-candidate` | Worth a bounded research run later. |
| `unblocker-task` | Small enough to run or queue as a related side task. |
| `ontology-candidate` | May affect premises, confidence, constitutions, axioms, or bridge claims. |
| `deferred` | Kept as reminder or parking-lot item. |

At checkpoints, Necronomicon should show side notes as a compact queue:

```text
Captured while working:
- attached to current task: 1
- inventory candidates: 2
- research ideas: 1
- unblocker tasks: 1
- contradictions: 1
- deferred reminders: 1
```

The user should be able to say "process the side notes", "inventorize the durable ones", "turn the research ideas into a research plan", "run the unblockers", or "ignore the parking lot for now".

Related unblockers should have a sharper ergonomic contract than open research. They are small tasks whose result can unblock the active discussion, definition, design, or plan. Examples include getting API prices, checking a current limit, finding a version constraint, looking up one vendor policy, or confirming whether a repository file exists.

Necronomicon should handle them with this decision rule:

```text
if it blocks the active decision and is small -> run now or queue as active side task
if it is useful later but not blocking -> add to side note queue as research-candidate
if it is broad or ambiguous -> ask one scope question before running
if it is durable after completion -> inventorize the result or attach it to the research packet
```

The user-facing acknowledgment should stay compact: "Captured as a side unblocker; I will check API pricing and attach the result to the current decision packet." If execution cannot happen immediately because another operation owns the turn, Necronomicon should queue it with status `ready` and show it at the next checkpoint.

## Discovery-To-Definition Flow

For feature work, Necronomicon should not always jump directly to `invoke define`. It should decide whether discovery and research are needed first.

| User Request | Necronomicon Should Ask | Likely Route |
| --- | --- | --- |
| "Define a billing export feature." | Is the goal and boundary already clear enough to define? | `invoke define` if yes; discovery if no. |
| "I have an idea for better onboarding." | What problem, user, and success criteria are known? | discovery, then research if evidence is missing. |
| "Research options for caching." | What scope, sources, and stop condition should bound the research? | `research`, then decision or `invoke define`. |
| "Build the next slice." | Is there an approved definition or plan? | `task-session` if yes; `invoke plan` or discovery if no. |

The intended funnel is:

```text
rough intent
  -> discovery / scope clarification
  -> bounded research when evidence is missing
  -> decision gate when trade-offs matter
  -> invoke define
  -> invoke design or plan
  -> task-session execution
  -> checkpoint / resume
```

The funnel is flexible. A user can explicitly skip ahead, but Necronomicon should name the risk and preserve the skipped discovery or research as a gap.

## Knowledge Substrate Flow

The discovery and definition funnel sits on top of the knowledge substrate:

```text
session evidence
  -> discovery-to-inventory
  -> inventory + glossary
  -> ontology candidates
  -> premise and confidence review
  -> constitutions or axioms when gates pass
  -> bridge-validated context
  -> invoke define / design / plan
```

This is how Necronomicon turns ordinary work into durable project understanding. Discovery should feed `discovery-to-inventory`; inventory should feed `ontology-harness` when knowledge needs governance; ontology review should feed `invoke` only after gaps and confidence are explicit.

Necronomicon can collect candidate premises, axioms, constitutions, confidence changes, and bridge edges, but it cannot promote them. Promotion belongs to `ontology-vault` and consequential commitment belongs to `decision-gate`.

## Inventory Experience

Inventory should stay mostly invisible until it matters.

In normal conversation, the user should be able to say:

| User Intent | Harness Behavior |
| --- | --- |
| "What do we know about auth boundaries?" | Query inventory first, summarize the relevant entries, name source gaps, then route deeper if needed. |
| "Keep this for later." | Create a checkpoint and route durable findings to `inventory ingest` or `discovery-to-inventory`. |
| "This contradicts what we decided." | File a contradiction or lint gap, then route to ontology or decision review if the contradiction is consequential. |
| "Use this research to define the feature." | Hand the research packet, inventory selectors, and gaps to `invoke define`. |

The agent should not expose inventory as a separate paperwork step unless the user explicitly asks for curation. The ergonomic default is:

```text
answer the user
show retrieved memory when it affects the answer
record durable findings in the background when permitted
surface gaps and contradictions as next actions
```

## Research And Invoke Ergonomics

Invoke should not become the default research engine.

Use harness research when the user is still exploring evidence, scope, or options. Use `discovery-to-inventory` when the discovery should become reusable project knowledge. Use `inventory query` or `inventory lookup` when the question is primarily retrieval. Use `invoke` only when the research exists to produce or support `define`, `design`, or `plan`.

The invoke research template is still valuable as a shared packet shape: research question, scope boundary, source ledger, evidence table, contradictions, claim status, unresolved gaps, options, and gate result. Necronomicon can create a harness research packet in that shape, then either inventorize it or hand it to invoke when lifecycle authoring starts.

## Route Examples

| Request | Likely Route | Why |
| --- | --- | --- |
| "Define this new workflow." | `invoke define` | Lifecycle authoring belongs to `invoke`. |
| "Figure out what this feature should be." | discovery, then `invoke define` | The feature is not ready for governed definition yet. |
| "We are in research; include the docs folder too." | active `research` interaction | This is a continuation, not a fresh route. |
| "Do we already know the auth model?" | `inventory lookup`, then context or ontology if needed | Retrieval should use the compiled knowledge layer first. |
| "Save these findings for future agents." | `inventory ingest` or `discovery-to-inventory` | Durable knowledge belongs in inventory, not only checkpoint text. |
| "Research this so we can define it." | harness research, then `invoke define` with research packet | Evidence gathering precedes lifecycle authoring. |
| "Plan the next implementation layer." | `invoke plan` or `implementation-readiness` | Planning needs governed lifecycle artifacts or staged readiness. |
| "What concepts are emerging from these sessions?" | `ontology-harness` | Ontology mapping and session distillation belong to ontology governance. |
| "Summarize enough context for a task." | `context-builder` | Compact task context is a context-builder concern. |
| "This command keeps routing wrong." | `maintain` | Repeated route misses are harness maintenance evidence. |

## Success Criteria

Necronomicon is working when:

- a user can resume a repository after days away and see useful next actions,
- common requests route correctly without requiring command memorization,
- checkpoints preserve decisions and gaps without becoming false authority,
- research has visible source boundaries and stop conditions,
- maintenance recommendations cite route history, gaps, or telemetry,
- capability changes are explicit and reversible,
- ontology, lifecycle authoring, task execution, and maintenance remain owned by their proper capabilities.

## Open Product Questions

| Question | Why It Matters | Suggested Next Step |
| --- | --- | --- |
| Should Necronomicon always create a session, or support stateless route-only use? | Affects friction for small tasks. | Default to resumable sessions, allow route-only when persistence is unnecessary. |
| How visible should route ledgers be to users? | Too much telemetry can become noise. | Show summaries by default, link detailed ledgers when requested. |
| What is the minimum checkpoint worth writing? | Prevents memory spam. | Write checkpoints on user request, close, major decisions, research synthesis, or repeated misses. |

## Settled MVP Decisions

| Decision | Reason | Revisit Trigger |
| --- | --- | --- |
| Keep `research` as a Necronomicon mode for MVP. | Current usage needs bounded evidence gathering before a separate reusable sigil is justified. | Extract when repeated non-Necronomicon workflows need the same research contract. |
| Treat invoke research templates as packet shapes, not route ownership. | Prevents `invoke` from becoming the default research engine. | Revisit only if invoke gains a first-class research mode contract. |
| Make state schemas and classifier fixtures the next plan target. | Reflection surfaced schema and fixture gaps as the main blocker after define/design. | Complete before implementation work starts. |

## Next Iteration

Use this vision to drive the next implementation slice:

1. Define `active-interaction.json`, `side-notes.jsonl`, route, gap, checkpoint, and unblocker task schemas.
2. Add classifier fixtures for continuation, explicit interrupt, side note, unblocker, fresh route, ambiguous route, and checkpoint closeout.
3. Add a `resume` summary shape.
4. Add route confidence language for ordinary user requests.
5. Define a minimal checkpoint artifact.
6. Add one end-to-end example: start, discover/research, hand off to `invoke define`, checkpoint, resume.
