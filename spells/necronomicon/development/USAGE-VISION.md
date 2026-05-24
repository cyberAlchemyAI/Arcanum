# Necronomicon Day-To-Day Usage Vision

## Purpose

Define how a repository user should experience substrate-first Necronomicon during ordinary work. The product should feel like a working knowledge harness, not a command router with memory bolted on.

## Vision Statement

Necronomicon is the repository's governed working memory. It helps the user ask normal questions, recover what is already known, see what is unsupported or contradictory, and route the next step to the capability that owns it.

The default user feeling should be:

> I can ask what this repo knows, and Necronomicon will distinguish fact, candidate, gap, contradiction, and next owner.

## Product Promise

After Necronomicon is set up, the user should feel four things:

1. **Knowledge continuity:** "The repo remembers durable context without pretending chat is truth."
2. **Authority clarity:** "I can see what is source-backed, candidate-only, contradictory, or undecided."
3. **Governed routing:** "The next owner is named because of the claim's authority status, not because I memorized a command."
4. **Traceability:** "Important gaps and handoffs are captured for later work."

## Primary User

The primary user is a repository operator working with an agent across repeated sessions. They may be designing a feature, maintaining a framework, researching a decision, implementing a task, or reconciling workflow drift.

They know the repository goal, but should not need to know where every durable fact, ontology claim, or command surface lives.

## Daily Loop

| Moment | User Says | Necronomicon Should |
| --- | --- | --- |
| Ask what is known | "What do we know about Necronomicon setup?" | Query inventory first, then cite source-backed context and gaps. |
| Add working knowledge | "Side note: this should start from ontology and inventory." | Capture as session evidence, classify as product-boundary candidate, and route if needed. |
| Detect missing memory | "I thought we had decided this." | Search inventory and session evidence, then record missing coverage if absent. |
| Reconcile conflict | "This conflicts with the previous plan." | Record contradiction, name affected claims, and route to inventory lint, ontology review, or decision gate. |
| Govern a claim | "This is a core rule." | Treat as premise/constitution/axiom candidate and route to ontology owner. |
| Author a lifecycle artifact | "Define/design/plan this." | Hand grounded context and gaps to `invoke`. |
| Execute | "Implement the next slice." | Route to `task-session` only when the slice is bounded and source-backed enough. |
| Checkpoint | "Checkpoint this." | Distill source-backed facts, candidates, contradictions, decisions, gaps, and handoffs. |
| Maintain | "This keeps missing." | Use gap and route patterns to propose local harness improvements. |

## Everyday Commands And Natural Forms

| User Form | Expected Mode | Expected Behavior |
| --- | --- | --- |
| "What do we know about X?" | substrate lookup | Inventory-first retrieval with source refs and gaps. |
| "Remember this for later." | evidence capture | Store low-authority session evidence and classify durability. |
| "This should become durable." | inventorize candidate | Prepare inventory handoff; do not promote directly. |
| "This is a governance claim." | ontology candidate | Prepare ontology-vault or ontology-harness handoff. |
| "This contradicts Y." | contradiction handling | Record gap and recommend reconciliation owner. |
| `necronomicon resume` | resume | Summarize known facts, candidates, open gaps, and next owner. |
| `necronomicon checkpoint` | checkpoint | Distill facts, inference, decisions, candidates, contradictions, and gaps. |
| `necronomicon route "..."` | route | Route after authority status is clear enough. |
| `necronomicon maintain` | maintain | Propose improvements from repeated gaps, misses, and signals. |

## UX Principles

- **Knowledge first:** for durable questions, retrieve inventory before broad search or command routing.
- **Authority labels:** every durable answer should distinguish source-backed fact, candidate, gap, contradiction, or decision.
- **Candidate-only promotion:** Necronomicon can propose inventory and ontology candidates; owners promote them.
- **Plain language first:** users should ask natural questions rather than remember command names.
- **One question when blocked:** ask a focused clarification only when authority or owner cannot be determined.
- **Local-first evidence:** use inventory, session evidence, ontology outputs, docs, and code before web.
- **Governed handoff:** the next route follows from ownership: inventory for durable knowledge, ontology for governed claims, invoke for lifecycle authoring, task-session for execution.
- **Side notes without derailment:** capture notes and classify them without abandoning active work.
- **No silent capability changes:** setup and capability changes require explicit decisions.
- **Maintenance from evidence:** improve the harness from repeated gaps, corrections, route misses, and telemetry.

## State The User Should See

| State | User-Facing Meaning |
| --- | --- |
| Known facts | Source-backed or inventory-backed claims with selectors. |
| Session evidence | Useful context that is not yet authoritative. |
| Inventory candidates | Durable findings worth filing through `inventory`. |
| Ontology candidates | Claims requiring governance review. |
| Contradictions | Conflicts that need reconciliation. |
| Open gaps | Missing sources, missing capabilities, unresolved choices, or route misses. |
| Suggested next owner | Capability that can safely handle the next step. |

## Active Interaction Model

The substrate loop still needs turn continuity. If Necronomicon or a routed capability is waiting for the user's answer, the next user turn should usually continue that interaction unless the user clearly interrupts.

The active interaction record exists to preserve context, not to outrank the authority ladder. A user answer may update session evidence, but it becomes durable only after source backing, inventory filing, ontology review, or decision approval.

| Incoming Turn | Active Interaction Exists? | Default Interpretation |
| --- | --- | --- |
| "Yes, use option B." | yes | Apply to active decision/interview and record decision status. |
| "The target user is a platform admin." | yes | Attach to active discovery/define context as session evidence. |
| "Side note: this conflicts with the ontology plan." | yes | Capture as contradiction candidate without derailing active flow. |
| "`invoke define` this now." | yes or no | Explicit lifecycle command wins, but handoff includes current gaps. |
| "What were we doing?" | yes | Summarize known facts, candidates, pending prompt, and gaps. |

## Side Note Ergonomics

The ergonomic rule is: **capture first, switch only on intent**.

| Side Note Type | Example | Default Handling |
| --- | --- | --- |
| Durable project fact | "Side note: the installer already generates capabilities.json." | Capture as session evidence; propose inventory if source-backed. |
| Governance claim | "This should be a constitution." | Capture as ontology candidate; route to ontology-vault if consequential. |
| Contradiction | "This conflicts with the old wave plan." | Record contradiction gap and owner. |
| Research seed | "Research idea: compare inventory formats." | Add research candidate with scope gap. |
| Related unblocker | "Find the file that writes capabilities.json." | Run or queue if small and blocking. |
| Reminder | "Remember to regenerate adapters later." | Queue as deferred follow-up. |

At checkpoint time, Necronomicon should report side notes by authority destination:

```text
Captured while working:
- attached to active context: 1
- inventory candidates: 2
- ontology candidates: 1
- contradiction gaps: 1
- research candidates: 1
- deferred reminders: 1
```

## Discovery-To-Definition Flow

For feature work, Necronomicon should not always jump directly to `invoke define`. It should first determine whether the knowledge substrate has enough context.

```text
rough intent
  -> inventory lookup
  -> session evidence / missing source gaps
  -> inventory or ontology candidates
  -> decision gate when commitment is needed
  -> invoke define/design/plan
  -> task-session execution
  -> checkpoint
```

The user can explicitly skip ahead, but Necronomicon should name the skipped evidence or governance as gaps.

## Change History

| Date | Change |
| --- | --- |
| 2026-05-23 | Re-authored day-to-day UX around substrate-first behavior. |
