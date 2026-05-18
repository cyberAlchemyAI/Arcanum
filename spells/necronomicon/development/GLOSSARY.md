---
module: necronomicon
version: current
status: draft
updatedAt: 2026-05-18
docType: glossary
---

# Necronomicon Glossary

## Terms

| Term | Definition | Status | Source |
| --- | --- | --- | --- |
| Necronomicon | Repository-local harness for durable session memory, turn routing, checkpoints, research packets, side notes, unblockers, handoffs, and maintenance recommendations. | linked | `spells/necronomicon/README.md` |
| Repository Harness | The persistent operating shell around selected repository-local Arcanum capabilities. | linked | `spells/necronomicon/README.md` |
| Session Memory Router | MVP product shape that classifies turns, preserves active state, routes work, captures side notes, and checkpoints. | linked | `spells/necronomicon/development/USAGE-VISION.md` |
| Workbench State Manager | Continuation product shape that manages lanes for main work, side notes, unblockers, research seeds, inventory candidates, ontology candidates, and deferred reminders. | linked | `spells/necronomicon/development/USAGE-VISION.md` |
| Active Interaction | Current back-and-forth flow whose owning capability interprets the next user response. | linked | `spells/necronomicon/README.md` |
| Turn Classification | Ordered decision process that determines whether a user turn is an interrupt, side note, pending response, handoff continuation, fresh route, or ambiguous turn. | linked | `spells/necronomicon/README.md` |
| Side Note | Mid-run user input captured without derailing the active flow, such as a fact, reminder, research seed, contradiction, or related task. | linked | `spells/necronomicon/development/USAGE-VISION.md` |
| Unblocker Task | Small bounded related task whose result can unblock an active decision, definition, design, plan, or implementation task. | linked | `spells/necronomicon/development/USAGE-VISION.md` |
| Research Seed | Candidate research idea captured for later bounded research. | linked | `spells/necronomicon/development/USAGE-VISION.md` |
| Inventory Candidate | Durable knowledge candidate that should route to `inventory` or `discovery-to-inventory` before becoming reusable compiled knowledge. | linked | `spells/necronomicon/development/KNOWLEDGE-SUBSTRATE-FLOW.md` |
| Ontology Candidate | Candidate concept, premise, confidence change, constitution, axiom, or bridge edge that must route through ontology governance before promotion. | linked | `spells/necronomicon/development/KNOWLEDGE-SUBSTRATE-FLOW.md` |
| Checkpoint | Durable session distillation separating facts, inferences, decisions, contradictions, unresolved questions, route patterns, and candidates. | linked | `spells/necronomicon/README.md` |
| Gap | Unresolved question, contradiction, blocked decision, capability gap, route miss, or promotion gap. | linked | `spells/necronomicon/README.md` |
| Route Decision | Recorded selection of a command or capability, including candidates, confidence, rationale, result, validation, and follow-up. | linked | `spells/necronomicon/README.md` |
| Handoff | Context packet that transfers work to an owning capability such as `invoke`, `inventory`, `ontology-harness`, or `task-session`. | linked | `spells/necronomicon/README.md` |
| Knowledge Substrate | Flow from raw interaction into session evidence, inventory, ontology candidates, premise/confidence review, and bridge-validated context. | linked | `spells/necronomicon/development/KNOWLEDGE-SUBSTRATE-FLOW.md` |
| Evidence Confidence | How well a claim is supported by source evidence or observed reality. | linked | `spells/necronomicon/development/KNOWLEDGE-SUBSTRATE-FLOW.md` |
| Commitment Confidence | How strongly the project should rely on a claim right now. | linked | `spells/necronomicon/development/KNOWLEDGE-SUBSTRATE-FLOW.md` |

## Glossary Rules

- Necronomicon terms are descriptive until source-backed by runtime state or owning capability output.
- Candidate terms do not promote inventory entries, ontology concepts, constitutions, or axioms.
- Terms used by `invoke` define/design/plan handoffs should preserve gap status when unresolved.

## Glossary Gaps

| Gap | Impact | Next Step |
| --- | --- | --- |
| Exact state-machine vocabulary for unblocker execution is still draft. | Implementation schemas may drift. | Finalize during plan layer. |
| Research packet vs research seed boundary needs implementation examples. | Agents may over-route to research. | Add examples in plan or validation fixtures. |
