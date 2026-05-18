# Interrogation: Necronomicon Concept Clarity

## Interrogation Scope

- Target: `spells/necronomicon`
- Mode: artifact readiness interrogation
- Inputs: repository research discovery, ontology harness contract, session spell contract, registry, local harness state, runtime adapters.
- Question: Is Necronomicon clear enough for an operator to know what it is, when to use it, and how it works?

## Findings

| ID | Severity | Finding | Evidence | Required Response |
| --- | --- | --- | --- | --- |
| I-001 | high | The name `Necronomicon` was overloaded between a single ontology harness run and a persistent harness. | README, registry, runtime aliases. | Reserve `Necronomicon` for the persistent harness and move ontology governance to `ontology-harness` / `arcanum-ontology-harness`. |
| I-002 | high | The session spell can sound like it owns every downstream behavior it routes to. | Session modes include route, research, implementation-research, maintain, update-capabilities. | State that the session is a coordinator and memory boundary, not the authority for ontology promotion, lifecycle authoring, or reusable artifact creation. |
| I-003 | medium | First-pass runtime behavior may be mistaken for a complete CLI engine. | Wave plan and layering docs emphasize adapter-mediated state. | Document the default flow as adapter-mediated: load state, classify, delegate, record, checkpoint when required. |
| I-004 | medium | `.arcanum/necronomicon/` may look like a local canonical source folder. | Local harness README and session guardrails warn against copied definition storage. | Repeat the negative boundary in the session contract's conceptual section. |
| I-005 | medium | Research is currently described as a mode/profile overlay, but its implementation authority is still not fully settled. | Session contract, wave plan, selected capabilities manifest, invoke research template. | Keep research as a bounded mode in the session contract, but carry an explicit gap about whether a reusable research sigil exists. |

## Hard Questions

| Question | Answer From Evidence | Verdict |
| --- | --- | --- |
| If a user says "run Necronomicon," what should happen? | Route to the persistent `necronomicon` harness. | pass |
| If a user says "start Necronomicon for this repo," what should happen? | Route to `necronomicon` setup/start mode. | pass |
| Where does durable memory live? | Under `.arcanum/necronomicon/`, especially session folders, route ledgers, decisions, gaps, checkpoints, research, maintenance, and capability updates. | pass |
| Is that folder authoritative? | No. It is project-local harness state; canonical definitions remain in Arcanum source and runtime adapters. | pass |
| Who owns ontology promotion? | `ontology-vault` through `ontology-harness`, optionally gated by `decision-gate`; the session only collects and routes candidates. | pass |
| Who owns define/design/plan/full/validate? | `invoke` when installed. | pass |
| Who owns reusable spell or sigil creation from maintenance outcomes? | `spellcraft` and `sigil-development`, with explicit user approval. | pass |
| Is there enough current documentation to prevent misuse without edits? | Not quite; the answer exists but is distributed across several files. | flag |

## Recommended Definition

Necronomicon is Arcanum's persistent repository harness surface.

**Necronomicon** is the persistent repository harness that keeps memory, routes work through selected Arcanum capabilities, records gaps and checkpoints, supports bounded research, and proposes maintenance from evidence. Ontology governance is owned by `ontology-harness` and can be invoked through `ontology-harness`, `arcanum-ontology-harness`, or `arcanum-spell-ontology-harness`.

It works by loading local harness state, classifying the user request, delegating to the owning sigil or spell through runtime adapters, recording what happened, and preserving only concise resumable state. It does not replace the registry, own canonical definitions, silently promote candidates, or persist secrets.

## Readiness Verdict

- Verdict: pass
- Reason: The concept is now singular: Necronomicon is the persistent repository harness, with ontology governance delegated to `ontology-harness`.
- Artifact update: add a near-top conceptual model and operating model to `spells/necronomicon/README.md`.
- Remaining ambiguity: research capability authority should be resolved in a later implementation layer.
