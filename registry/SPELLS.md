# Spell Registry

This registry lists reusable spell compositions offered by Arcanum.

Each spell references existing sigils and defines a workflow around them. Repository-local adaptations should live under `.arcanum/spells/` in the consuming repository.

## Spells

| Spell                    | Aliases                                          | Purpose                                                                                                                                                                   | Sigils Composed                                                  | Use When                                                                                                                                                         | File                                                                 |
| ------------------------ | ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| Arcanum Bootstrap        | Arcanum Install; Sigil Forge Install             | Install Arcanum into a consuming repository with all or selected sigils, selected spells, observability folders, and optional runtime adapters.                           | `sigil-runtime-installer`, `observability-setup`                 | A repository should receive Arcanum locally and optionally expose it through GitHub Copilot, Claude, or Codex.                                                   | [README.md](../spells/arcanum-bootstrap/README.md)               |
| Repository Harness       | Repository Codex                                 | Install a reusable repository knowledge and architecture harness, then verify task-context retrieval.                                                                     | `inventory`, `architecture-pattern-inventory`, `context-builder` | A repository needs compiled knowledge, architecture mapping, and focused task context to work together.                                                          | [README.md](../spells/repository-harness/README.md)             |
| Ontology Harness         | Necronomicon Vault; Ontology Codex               | Turn vault-like sessions, discoveries, premises, conventions, and optional business-system branches into a traceable ontology governance layer.                           | `inventory`, `ontology-vault`, `context-builder`                 | A repository needs ontology mapping, session distillation, confidence promotion, premise review, convention-change gates, or intent-to-system bridge validation. | [README.md](../spells/ontology-harness/README.md)                 |
| Necronomicon             | Repository Harness; Arcanum Harness              | Create or resume a repository-local Necronomicon with durable memory, selected capability routing, fallback discovery, capability updates, and handoff artifacts.         | `ontology-harness`, `inventory`, `context-builder`               | Repository work should route through selected local Arcanum commands while preserving session memory and auditable capability changes.                           | [README.md](../spells/necronomicon/README.md)                    |
| Implementation Readiness |                                                  | Move from rough implementation intent to layered plan, resolved decisions, and a task execution loop.                                                                     | `implementation-layering`, `decision-gate`, `task-session`       | A feature or workflow needs staged implementation planning before execution.                                                                                     | [README.md](../spells/implementation-readiness/README.md) |
| Discovery To Inventory   |                                                  | Turn vague or brownfield scope into discovery baseline, glossary, and reusable inventory entries.                                                                         | `scope-interview`, `feature-glossary`, `inventory`               | Early discovery should become persistent reusable knowledge rather than a one-off conversation.                                                                  | [README.md](../spells/discovery-to-inventory/README.md)     |
| Whisper                  | Whisper                                          | Turn author intent into governed text through substrate extraction, SCU candidate selection, composition planning, drafting, validation, and learning residue.            | `structured-interview-kits`, `distill`                           | A research post, article, fundraising copy, or other text artifact needs explicit audience, resonance, trajectory, body parts, and review criteria.              | [README.md](../spells/whisper/README.md)                   |
| Sigil Maintenance Loop   |                                                  | Observe sigil executions, reflect on accumulated signals, and route targeted sigil updates.                                                                               | `signal-observer`, `workflow-reflect`, `sigil-development`       | A reusable sigil needs evidence-based maintenance from telemetry.                                                                                                | [README.md](../spells/sigil-maintenance-loop/README.md)     |
| Observed Invocation Loop | Capability Observability Loop                    | Wrap Arcanum-managed skill, sigil, and spell invocations with telemetry append, threshold evaluation, and reflection routing.                                             | `signal-observer`, `workflow-reflect`                            | Managed capability invocations should reliably emit telemetry and route reflection without going through the experiment harness.                                  | [README.md](../spells/observed-invocation-loop/README.md)   |
| Goal                     | Autonomous DAG Goal Loop; DAG Goal Loop          | Drive a Craft-backed work graph through a fail-closed control loop that reads frontier state, routes eligible nodes, audits receipts, stages deltas, and promotes only behind explicit approval. | `craft`, `dispatch-spec`, `observed-invocation-loop`, `decision-gate`, `task-session`, `observability-setup`, `signal-observer` | A Craft scope has open next moves, gaps, blockers, or not-started SWUs and should continue toward a goal without direct protected mutation.                       | [README.md](../spells/goal/README.md)                       |

## Alias Rules

- Canonical spell IDs remain stable and map to filenames.
- Aliases are human-facing lookup names and may be more evocative.
- An alias must resolve to exactly one spell in the active registry.
- Local repositories may add local aliases under `.arcanum/spells/` without changing this registry.
- Spell run reports should record both the alias used and the canonical spell ID.

## Entry Requirements

A spell should be added here when it has:

- a purpose and trigger condition,
- required and optional sigils,
- phase definitions,
- shared state and handoff artifacts,
- gates and failure policy,
- observability guidance,
- output contract.
