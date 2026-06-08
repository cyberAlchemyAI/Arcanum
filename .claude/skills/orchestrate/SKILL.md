---
name: orchestrate
description: "Route repository work through installed Arcanum capabilities."
surface_kind: generated-native-runtime-package
runtime: claude
canonical_source: arcanum/runtime/orchestrate
alias_of: null
generated_by: tools/bootstrap_arcanum.sh --profile
mutation_policy: regenerate-from-canonical-source
---

# Skill: Arcanum Orchestrate

<objective>
Route repository work through installed Arcanum sigils and spells while preserving dispatch-spec, task-session, and observability boundaries.
</objective>

<installed-capabilities>
- `arcanum-orchestrate`: route requests through installed Arcanum capabilities.
- `dispatch-spec` sigil (`formulae` tier)
- `observability-setup` sigil (`formulae` tier)
- `codex-goal-profile` sigil (`transmutations` tier)
- `context-builder` sigil (`transmutations` tier)
- `feature-glossary` sigil (`transmutations` tier)
- `implementation-layering` sigil (`transmutations` tier)
- `architecture-pattern-inventory` sigil (`arcana` tier)
- `constitution-governance` sigil (`arcana` tier)
- `decision-gate` sigil (`arcana` tier)
- `definitions-governance` sigil (`arcana` tier)
- `distill` sigil (`arcana` tier)
- `experiment-harness` sigil (`arcana` tier)
- `inventory` sigil (`arcana` tier)
- `invoke-example-runner` sigil (`arcana` tier)
- `ontology-vault` sigil (`arcana` tier)
- `refine` sigil (`arcana` tier)
- `research-evidence-harness` sigil (`arcana` tier)
- `research-tower` sigil (`arcana` tier)
- `residuality-spec` sigil (`arcana` tier)
- `robot-talks` sigil (`arcana` tier)
- `scope-interview` sigil (`arcana` tier)
- `sigil-development` sigil (`arcana` tier)
- `sigil-runtime-installer` sigil (`arcana` tier)
- `signal-observer` sigil (`arcana` tier)
- `skill-decomposer` sigil (`arcana` tier)
- `skill-transcriptor` sigil (`arcana` tier)
- `spellcraft` sigil (`arcana` tier)
- `structured-interview-kits` sigil (`arcana` tier)
- `task-session` sigil (`arcana` tier)
- `ux-evidence-validator` sigil (`arcana` tier)
- `workflow-reflect` sigil (`arcana` tier)
- `x-ray` sigil (`arcana` tier)
- `arcanum-bootstrap` spell
- `discovery-to-inventory` spell
- `guide-architecture` spell
- `implementation-readiness` spell
- `invoke` spell
- `necronomicon` spell
- `observed-invocation-loop` spell
- `ontology-harness` spell
- `publication-research-pipeline` spell
- `repository-harness` spell
- `sigil-maintenance-loop` spell
- `whisper` spell
</installed-capabilities>

<process>
1. Classify the request as authoring, refinement, task execution, observability, install/setup, validation, or help.
2. Prefer the host runtime's native skill, agent, or instruction execution for model-backed work.
3. Use native skills, subagents, and dispatch-spec validators for active execution evidence.
4. Treat `tools/arcanum` helpers as deterministic handoff preparation or explicit legacy compatibility only.
5. Do not spawn nested model-backed CLIs for the same stage.
6. Return capability, mode, receipt kind, execution surface, status, artifacts, validation, observer status, blockers, and handoff note.
</process>
