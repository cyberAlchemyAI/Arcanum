# Sigil Registry

This registry is the quick-reference index for reusable sigils in Arcanum.

Use it when you know the kind of work you need and want to find the right sigil folder quickly. Each entry summarizes what the sigil does, when to use it, its tier, and where its full instructions live.

## Registry Table

| Sigil                          | Tier           | Summary                                                                                                                                                                                                  | Use When                                                                                                                                                                    | Folder                                                                                |
| ------------------------------ | -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| Observability Setup            | Formulae       | Installs or verifies a repository-local sigil observability package with JSONL ledgers, config, and reflection state.                                                                                    | A consuming repository needs a portable place for sigils to append telemetry and track reflection thresholds.                                                               | [formulae/observability-setup/](../formulae/observability-setup/)                     |
| Context Builder                | Transmutations | Builds a compact task-ready context pack from selector-level evidence and obligation-linked excerpts.                                                                                                    | A task needs focused project evidence without whole-file dumps or unrelated background.                                                                                     | [transmutations/context-builder/](../transmutations/context-builder/)                 |
| Codex Goal Profile             | Transmutations | Turns one Arcanum work-pack task or SWU into a native Codex `/goal` profile with outcome, verification, boundaries, iteration policy, and blocked stop condition.                                      | A work-pack unit should run through Codex native Goals without losing Arcanum scope, source links, validation, or synchronization obligations.                              | [transmutations/codex-goal-profile/](../transmutations/codex-goal-profile/)         |
| Implementation Layering        | Transmutations | Turns an implementation goal into staged layers, starting with the smallest useful proof and progressing through evidence-based hardening.                                                               | You need to plan a feature, workflow, infrastructure change, or system improvement without overloading the first build step.                                                | [transmutations/implementation-layering/](../transmutations/implementation-layering/) |
| Architecture Pattern Inventory | Arcana         | Maps a repository architecture and generates a reusable architecture pattern inventory package with concept cards, relationship cards, dependency rules, testing alignment, and observability alignment. | A codebase needs a selective architecture context pack for future agents or reviewers.                                                                                      | [arcana/architecture-pattern-inventory/](../arcana/architecture-pattern-inventory/)   |
| Definitions Governance         | Arcana         | Maintains canonical definitions, synchronized lookup indexes, explanatory intuition, and downstream drift checks.                                                                                        | Critical terms need stable authority and downstream documents must not redefine them.                                                                                       | [arcana/definitions-governance/](../arcana/definitions-governance/)                   |
| Decision Gate                  | Arcana         | Resolves blocker-level multi-option decisions before consequential work continues and persists a reusable decision record.                                                                               | A task has unresolved choices that affect scope, implementation, rollout, verification, risk, or future maintenance.                                                        | [arcana/decision-gate/](../arcana/decision-gate/)                                     |
| Distill                       | Arcana         | Reduces a broad model, architecture, design, or plan into the smallest coherent concept unit that still fits the target context and proves recomposition before downstream work begins.                  | A broad idea or plan needs proportionate decomposition, role-based critique, finite recursive rounds, and a navigable next route before implementation.                     | [arcana/distill/](../arcana/distill/)                                                 |
| Experiment Harness             | Arcana         | Creates profile-aware experiment harnesses for reusable spells and sigils, runs live/runtime loops, validates outputs, reports profile status, and records observability evidence.                     | A spell or sigil needs repeatable fixtures, prompts, regimes, live promotion evidence, validation reports, or observed lifecycle feedback.                                  | [arcana/experiment-harness/](../arcana/experiment-harness/)                           |
| Feature Glossary               | Transmutations | Creates or updates a concise vocabulary layer for a feature, workflow, product area, or bounded project scope.                                                                                           | Local terms need shared meaning with source links, but not global definition authority.                                                                                     | [transmutations/feature-glossary/](../transmutations/feature-glossary/)               |
| Inventory                      | Arcana         | Installs and maintains a repository-local compiled knowledge inventory with immutable raw sources, generated markdown entries, indexes, tags, logs, lookup, and linting.                                 | A repository needs reusable knowledge that compounds across sources, questions, architecture mapping, and context-building runs.                                            | [arcana/inventory/](../arcana/inventory/)                                             |
| Ontology Vault                 | Arcana         | Maps and governs vault-like knowledge with roles, sessions, premises, confidence promotion, convention changes, delegated evidence, synthesis findings, and optional business-system branches.           | A repository has sessions, discoveries, premises, ontology conventions, confidence rules, delegated research, or intent-to-system traceability that need governed evidence. | [arcana/ontology-vault/](../arcana/ontology-vault/)                                   |
| Residuality Spec               | Arcana         | Helps define or harden specs through stressor analysis, desired residue, degradation behavior, attractor discovery, and resilience decisions.                                                            | A feature, workflow, or architecture slice needs concrete survivability and degradation behavior instead of vague resilience claims.                                        | [arcana/residuality-spec/](../arcana/residuality-spec/)                               |
| Refine                         | Arcana         | Creates a confirmed refinement seed with research offer, budget preset, and Codex Goal default route before Task Session execution.                                                                      | A vague target, folder, idea, design concern, or work-pack needs a bounded refinement seed before Task Session executes through Codex Goal.                                  | [arcana/refine/](../arcana/refine/)                                                   |
| Robot-Talks                    | Arcana         | Coordinates a multi-agent investigation to discover contradictions across system layers before implementation begins.                                                                                    | A problem spans multiple layers and misunderstanding the system is more expensive than a structured investigation.                                                          | [arcana/robot-talks/](../arcana/robot-talks/)                                         |
| Scope Interview                | Arcana         | Interviews a greenfield idea, brownfield repository, or mixed project scope into a structured discovery baseline.                                                                                        | Project boundaries, observed evidence, stated intent, hypotheses, and blocker decisions need clarification before planning.                                                 | [arcana/scope-interview/](../arcana/scope-interview/)                                 |
| Signal Observer                | Arcana         | Observes completed sigil invocations, derives behavior-level telemetry signals, appends JSONL, and recommends reflection or targeted maintenance.                                                        | A sigil run should become reusable evidence for future quality and workflow improvement.                                                                                    | [arcana/signal-observer/](../arcana/signal-observer/)                                 |
| Sigil Development              | Arcana         | Guides sigil creation, revision, observability, telemetry, reflection, and iteration through a governed lifecycle.                                                                                       | You are creating, improving, observing, reflecting on, or maintaining a sigil.                                                                                              | [arcana/sigil-development/](../arcana/sigil-development/)                             |
| Sigil Runtime Installer        | Arcana         | Installs thin runtime adapters for GitHub Copilot, Claude, or Codex so agents can invoke Arcanum sigils from local command surfaces.                                                                     | A repository should expose Arcanum sigils as slash-command style skills without copying canonical sigil internals.                                                          | [arcana/sigil-runtime-installer/](../arcana/sigil-runtime-installer/)                 |
| Skill Decomposer               | Arcana         | Extracts one reusable capability from a broad or tangled source and prepares a boundary-safe handoff for conversion.                                                                                     | A source contains several possible sigils, mixed behaviors, or one fragment that needs boundary analysis before authoring.                                                  | [arcana/skill-decomposer/](../arcana/skill-decomposer/)                               |
| Skill Transcriptor             | Arcana         | Converts a complete coherent skill, prompt, command, or workflow into an Arcanum-compliant sigil package plan.                                                                                           | A source is already one coherent reusable capability and needs tier classification, neutral rewrite, validation, and registry guidance.                                     | [arcana/skill-transcriptor/](../arcana/skill-transcriptor/)                           |
| Spellcraft                     | Arcana         | Designs, installs, validates, observes, and revises spells that compose multiple sigils into localized workflows.                                                                                        | Several sigils should run together with shared state, gates, handoffs, and spell-level observability.                                                                       | [arcana/spellcraft/](../arcana/spellcraft/)                                           |
| Structured Interview Kits (Interrogation) | Arcana         | Runs one-question-at-a-time interviews using pluggable modes, evidence-backed prompts, and artifact updates.                                                                                             | Human clarification should be reusable, decision-discriminating, and synchronized into target artifacts.                                                                    | [arcana/structured-interview-kits/](../arcana/structured-interview-kits/)             |
| Task Session                   | Arcana         | Executes one bounded task through scope resolution, decision trade-offs, gate checks, validation, and synchronized evidence.                                                                             | A single task needs guided execution with explicit blockers, done criteria, and reviewable completion evidence.                                                             | [arcana/task-session/](../arcana/task-session/)                                       |
| Workflow Reflect               | Arcana         | Analyzes accumulated sigil observability signals and writes evidence-backed workflow improvement proposals.                                                                                              | A sigil has enough telemetry, repeated gaps, or a manual request for retrospective improvement.                                                                             | [arcana/workflow-reflect/](../arcana/workflow-reflect/)                               |
| x-ray                          | Arcana         | Seed sigil for turning supplied context into a guided HTML explanation page with actors, flows, transformations, relationships, assumptions, and open questions.                                       | A component, process, architecture, plan, or system needs a structured explanation surface rather than a loose summary.                                                      | [arcana/x-ray/](../arcana/x-ray/)                                                     |

## By Tier

### Formulae

- [Observability Setup](../formulae/observability-setup/) - repository-local telemetry package setup for sigil usage.

Formulae are deterministic operational sigils. See [formulae/](../formulae/) for the tier concept.

### Transmutations

- [Codex Goal Profile](../transmutations/codex-goal-profile/) - native Codex `/goal` profile generation from work-pack tasks/SWUs.
- [Context Builder](../transmutations/context-builder/) - compact task-ready context packs from selector-level evidence.
- [Feature Glossary](../transmutations/feature-glossary/) - scoped vocabulary glossary synthesis with source links.
- [Implementation Layering](../transmutations/implementation-layering/) - staged implementation planning from minimum proof to progressive hardening.

Transmutations are bounded cognitive synthesis sigils. See [transmutations/](../transmutations/) for the tier concept.

### Arcana

- [Architecture Pattern Inventory](../arcana/architecture-pattern-inventory/) - repository architecture mapping and pattern inventory package generation.
- [Definitions Governance](../arcana/definitions-governance/) - canonical definitions maintenance and downstream drift checks.
- [Decision Gate](../arcana/decision-gate/) - blocker-level multi-option decision resolution before consequential work proceeds.
- [Distill](../arcana/distill/) - concept-layer reduction, smallest coherent unit selection, recomposition proof, and lifecycle routing.
- [Experiment Harness](../arcana/experiment-harness/) - profile-aware experiment harnesses, live/runtime loops, validation reports, and observed promotion evidence.
- [Inventory](../arcana/inventory/) - repository-local compiled knowledge inventory with ingest, lookup, lint, validate, and backfill modes.
- [Ontology Vault](../arcana/ontology-vault/) - governed knowledge-vault mapping, session distillation, premise review, confidence promotion, business-system branch bridging, and convention change control.
- [Residuality Spec](../arcana/residuality-spec/) - stressor, residue, degradation, and attractor analysis for resilient specifications.
- [Refine](../arcana/refine/) - refinement seed proposal with research offer and Codex Goal default routing.
- [Robot-Talks](../arcana/robot-talks/) - multi-agent cross-layer tension discovery.
- [Scope Interview](../arcana/scope-interview/) - project discovery baseline through evidence-backed interview.
- [Signal Observer](../arcana/signal-observer/) - post-run behavior signal derivation and telemetry append.
- [Sigil Development](../arcana/sigil-development/) - governed sigil lifecycle with observability and reflection.
- [Sigil Runtime Installer](../arcana/sigil-runtime-installer/) - GitHub Copilot, Claude, and Codex adapter installation for Arcanum sigils.
- [Skill Decomposer](../arcana/skill-decomposer/) - source mapping, capability extraction, boundary decisions, and handoff to conversion.
- [Skill Transcriptor](../arcana/skill-transcriptor/) - coherent source-to-sigil conversion with tier classification and package validation.
- [Spellcraft](../arcana/spellcraft/) - spell composition design, installation, validation, observation, and revision.
- [Structured Interview Kits](../arcana/structured-interview-kits/) - pluggable one-question interview modes with artifact updates. Alias: Interrogation.
- [Task Session](../arcana/task-session/) - guided execution of one bounded task with gates and completion evidence.
- [Workflow Reflect](../arcana/workflow-reflect/) - accumulated-signal reflection and improvement proposal generation.
- [x-ray](../arcana/x-ray/) - seed sigil for guided HTML explanation pages from supplied context.

Arcana are autonomous orchestration sigils. See [arcana/](../arcana/) for the tier concept.

## Spells

Spells compose multiple sigils into localized workflows. See [spells/](../spells/) for the concept and [Spell Registry](SPELLS.md) for offered compositions.

## Entry Requirements

A sigil should be added to this registry when it has:

- a dedicated folder under the correct tier,
- a human-facing `README.md`,
- an executable `SKILL.md`,
- a clear Quality Bar,
- clear Anti-Patterns,
- an output contract,
- observability or reflection guidance when the sigil is expected to be reused.

## Maintenance Rule

Update this registry whenever a sigil is added, renamed, retired, moved between tiers, or materially changes its purpose.
