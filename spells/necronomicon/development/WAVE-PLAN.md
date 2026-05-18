# Necronomicon UX Wave Plan

## Purpose

This plan turns the Necronomicon project harness UX vision into implementation waves. The target is to evolve `necronomicon` from a command router with memory into a guided project harness that helps users set up inventory, ontology, research, checkpoints, common routes, and maintenance workflows.

The plan is intentionally wave-based so each slice can be implemented, validated, and shipped without requiring the entire harness to exist at once.

## North Star

Necronomicon should be the project harness shell for a repository. It should help a user:

- establish reusable project knowledge through inventory,
- add ontology governance when the project needs premises, axioms, confidence, or business/system bridge validation,
- run sessions with explicit memory and checkpoints,
- route work through selected spells and sigils,
- perform bounded research across inventory, ontology, docs, code, and web when runtime support is available,
- route lifecycle authoring requests through `invoke` when installed,
- maintain the harness from repeated route misses, user corrections, telemetry, and selected sigil/spell signal coverage,
- propose new routes, spells, or sigils only when evidence supports them.

## Existing Inputs

- [spells/necronomicon/README.md](../../../spells/necronomicon/README.md) - current session harness spell.
- [spells/ontology-harness/README.md](../../../spells/ontology-harness/README.md) - ontology harness and Necronomicon alias contract.
- [arcana/inventory/SKILL.md](../../../arcana/inventory/SKILL.md) - inventory-first compiled knowledge layer.
- [arcana/ontology-vault/SKILL.md](../../../arcana/ontology-vault/SKILL.md) - ontology governance, premises, confidence, branch mapping, and session distillation.
- [arcana/structured-interview-kits/SKILL.md](../../../arcana/structured-interview-kits/SKILL.md) - one-question-at-a-time interview engine for setup, gap checks, checkpoint review, and maintenance decisions.
- [arcana/robot-talks/SKILL.md](../../../arcana/robot-talks/SKILL.md) - optional cross-layer research escalation.
- [arcana/decision-gate/SKILL.md](../../../arcana/decision-gate/SKILL.md) - optional gate for consequential unresolved choices that do not fit inventory, ontology, or maintenance routes.
- `observability-setup` capability (runtime surface) - repository-local telemetry setup and validation baseline.
- [arcana/signal-observer/SKILL.md](../../../arcana/signal-observer/SKILL.md) - post-run signal capture.
- [arcana/workflow-reflect/SKILL.md](../../../arcana/workflow-reflect/SKILL.md) - telemetry-backed maintenance reflection.
- [arcana/spellcraft/SKILL.md](../../../arcana/spellcraft/SKILL.md) - composed workflow design and maintenance.
- [arcana/sigil-development/SKILL.md](../../../arcana/sigil-development/SKILL.md) - local and reusable sigil authoring for approved maintenance outcomes.
- `sigil-maintenance-loop` capability (runtime surface) - cross-sigil maintenance synthesis and prioritization.
- `invoke` spell route (runtime surface) - lifecycle authoring route for define, design, plan, full, and validate.
- [tools/bootstrap_arcanum.sh](../../../tools/bootstrap_arcanum.sh) - runtime adapter and harness state generation.

## Implementation Principles

1. Inventory is the default substrate for any meaningful project harness.
2. Ontology is a heavier profile, not a mandatory first-run burden.
3. If `ontology-vault` or `ontology-harness` is selected, inventory and context-builder are mandatory dependencies.
4. The `research` sigil must be bounded by question, scope, budget, and synthesis checkpoint, with web access only when runtime tooling supports it.
5. Robot Talks is an escalation path for cross-layer contradiction discovery, not the default research behavior.
6. `research` is a new selectable sigil that can be enabled alongside any setup profile. It is not itself a setup profile or repository.
7. Lifecycle authoring requests (`define`, `design`, `plan`, `full`, `validate`) should route through `invoke` when installed.
8. `maintain` mode must aggregate route telemetry and all selected sigil/spell signals, then synthesize cross-sigil maintenance actions when available.
9. `observability-setup`, `signal-observer`, and `workflow-reflect` are required for telemetry-backed maintenance behavior.
10. `spellcraft` and `sigil-development` are required authoring paths for approved maintenance outcomes.
11. Checkpoints create candidates for ontology concepts, premises, axioms, and decisions. They do not silently promote them.
12. Maintenance proposes route, spell, and sigil changes from evidence. It must not auto-create reusable artifacts without approval.
13. Necronomicon harness state remains project-local state. It must not become a copied canonical definition store.
14. Human-gated Necronomicon flows use `structured-interview-kits` as the canonical interview engine instead of hand-rolling separate question loops.
15. Generated harness state must never persist secrets. Sensitive local context should be omitted or redacted before it reaches manifests, checkpoints, research briefs, gap ledgers, or maintenance reports.
16. Reusable spell changes should live in `spells/<canonical-id>/development/` until Spellcraft validation promotes canonical spell changes.
17. Lifecycle authoring can use `invoke` to prepare specs, designs, and work-packs, but spell creation and revision still route through `spellcraft`, and sigil creation or revision routes through `sigil-development`.

## Interview Decisions And Gap Closures

This section records decisions made during the gap-finding interview so implementation waves can preserve the rationale.

| Decision                         | Selected Option                                                                                                                                                                                                                | Rejected Alternatives                                                                                 | Plan Impact                                                                                                                                                                                                              |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Setup mutability after bootstrap | Gated profile change. The setup wizard may propose profile or capability changes, but the user must confirm them and the rationale must be written to setup decisions.                                                         | Static after bootstrap; auto-adjust within guardrails.                                                | Wave 2 must record profile revisions and dependency auto-adds as decisions. Wave 3 must present profile/capability changes as confirmation cards rather than silently mutating the active manifest.                      |
| Candidate promotion authority    | Route ontology candidates through ontology-vault modes. Necronomicon may collect candidates, but ontology promotion belongs to `ontology-vault` flows such as `promote-confidence`, `premise-review`, and `convention-update`. | Direct Necronomicon promotion queue; decision-gate for all consequential candidates.                  | Waves 4 and 5 must distinguish candidate collection from promotion. Inventory candidates route through inventory flows; ontology candidates route through ontology-vault modes.                                          |
| First-pass runtime surface       | Adapter-first manifest runtime. The first implementation should generate manifests, state files, setup decisions, route presets, and assistant adapter instructions.                                                           | Shell helper plus adapters; full local CLI harness.                                                   | Waves marked as runtime behavior ship adapter-mediated behavior and generated state contracts first. Full executable CLI commands remain outside the first implementation pass unless a later wave explicitly adds them. |
| Interview engine                 | `structured-interview-kits` is canonical for human-gated flows. Setup, gap checks, checkpoint review, research clarification, and maintenance decisions should use the one-question-at-a-time interview contract.              | Optional capability; setup-wizard-only usage; self-contained Necronomicon interview logic.            | Wave 1 must declare the dependency. Wave 2 must include it in relevant manifests. Wave 3 must express setup as a structured interview mode rather than ad hoc prompts.                                                   |
| Gap tracking                     | Maintain a project-local gap ledger. Unresolved questions, contradictions, capability gaps, route misses, and blocked decisions should roll up into `.arcanum/necronomicon/gaps.json`.                                         | Checkpoint-only gaps; maintenance-only rollup.                                                        | Waves 2, 4, 5, and 7 must write or update gap ledger entries with source, severity, owning route, status, and next action.                                                                                               |
| Gap ledger format                | `gaps.json` is the canonical source of truth. Markdown summaries may be generated later, but Wave 2 should write one machine-readable file first.                                                                              | `gaps.md` canonical; both files from the start; defer format choice.                                  | Manifest `gap_ledger_path` must point to `.arcanum/necronomicon/gaps.json`, and validation must parse it with `jq empty`.                                                                                                |
| State privacy                    | No secrets in generated harness state. Necronomicon should redact or omit credentials, tokens, passwords, private keys, and secret values from manifests, checkpoints, research briefs, gap ledgers, and maintenance reports.  | Strict evidence-only state; configurable privacy levels.                                              | Wave 2 must add a `state_privacy_policy`. Waves 4, 5, and 7 must apply redaction before writing durable artifacts.                                                                                                       |
| Lifecycle authoring route        | Route `define`, `design`, `plan`, `full`, and `validate` through `invoke` when installed; otherwise report capability gap and offer install path.                                                                              | Keep lifecycle authoring in ad hoc Necronomicon route handlers.                                       | Waves 1, 2, 6, 7, and 9 must preserve invoke-first lifecycle routing and gap handling when invoke is missing.                                                                                                            |
| Maintenance synthesis scope      | `maintain` aggregates route telemetry and all selected sigil/spell signals, then routes cross-sigil synthesis through `sigil-maintenance-loop` when available.                                                                 | Route-only telemetry; manual per-sigil reviews.                                                       | Waves 1, 7, and 9 must enforce all-signal coverage and explicit cross-sigil synthesis fallback behavior.                                                                                                                 |
| Research modeling                | Model `research` as a new selectable sigil, not a setup profile or repository. Setup profiles describe the base harness shape; selected sigils add behavior.                                                                   | Research as setup profile; implicit research overlay on all profiles; repository-like research state. | Waves 1, 2, 5, 6, and 9 must treat research enablement as sigil selection state. `research_policy.enabled` follows whether the `research` sigil is selected.                                                             |

## First-Pass Runtime Boundary

For this plan, runtime behavior means assistant-mediated execution over generated, versioned project state. The first implementation should produce reliable adapter instructions and machine-readable harness files, then validate that GitHub Copilot, Claude, and Codex adapters can guide the user through the modes.

The first implementation should not attempt a full local CLI engine for `setup`, `route`, `checkpoint`, `research`, or `maintain`. Shell helpers may be added later only when repeated validation shows that adapter instructions alone cannot preserve state consistently.

## Wave Overview

| Wave | Name                           | Primary Outcome                                                      | Ships Runtime Behavior? |
| ---- | ------------------------------ | -------------------------------------------------------------------- | ----------------------- |
| 0    | Baseline And Safety            | Confirm current contracts, dirty state, and validation gates.        | No                      |
| 1    | Spell Contract Reshape         | Update `necronomicon` with profiles, modes, and UX contract. | Partial                 |
| 2    | Manifest Schema And Profiles   | Add setup profile schema and dependency rules to bootstrap output.   | Yes                     |
| 3    | Interactive Setup Wizard       | Add setup questions and option cards to runtime adapters.            | Yes                     |
| 4    | Checkpoints And Memory         | Add checkpoint mode, memory policy, and checkpoint artifacts.        | Yes                     |
| 5    | Research Sigil                 | Add bounded research sigil with source-grounded synthesis.           | Yes                     |
| 6    | Common Routes Interface        | Add local route presets and route validation.                        | Yes                     |
| 7    | Maintenance Loop               | Add Necronomicon maintenance mode from telemetry and route misses.   | Yes                     |
| 8    | Docs And Consumer Regeneration | Sync docs, generated adapters, and example consumers.                | Yes                     |
| 9    | Hardening And Release Gate     | Validate temp installs, manifests, links, and behavior scenarios.    | No                      |

## Wave 0 - Baseline And Safety

### Objective

Establish a clean implementation baseline and avoid trampling unrelated local changes.

### Work Items

1. Check status in root and nested repositories.
2. Read current versions of the core source files.
3. Confirm which generated consumer examples should be regenerated.
4. Re-run the current validation suite used for the prior Necronomicon work.
5. Record any unrelated dirty files to avoid accidental edits.

### Files To Inspect

- [spells/necronomicon/README.md](../../../spells/necronomicon/README.md)
- [spells/ontology-harness/README.md](../../../spells/ontology-harness/README.md)
- [tools/bootstrap_arcanum.sh](../../../tools/bootstrap_arcanum.sh)
- [arcana/sigil-runtime-installer/SKILL.md](../../../arcana/sigil-runtime-installer/SKILL.md)
- [registry/SPELLS.md](../../../registry/SPELLS.md)

### Validation

- `bash -n tools/bootstrap_arcanum.sh`
- status checks for root, `arcanum`, and any regenerated consumer repository.

### Exit Criteria

- Known dirty state is classified.
- Current Necronomicon behavior is understood.
- Implementation can proceed without reverting user work.

## Wave 1 - Spell Contract Reshape

### Objective

Make `necronomicon` describe the intended product UX before modifying runtime generation.

### Work Items

1. Add a `Setup Profiles` section:
   - `basic-inventory`,
   - `ontology-harness`,
   - `custom`.
2. Add a `Dependency Rules` section:
   - selecting `necronomicon` includes `structured-interview-kits` for human-gated flows,
   - selecting `ontology-vault` adds `inventory` and `context-builder`,
   - selecting `ontology-harness` adds `ontology-vault`, `inventory`, and `context-builder`,
   - selecting the `research` sigil adds `inventory` and `context-builder` when missing and recommends `robot-talks` as escalation only,
   - `observability-setup`, `signal-observer`, and `workflow-reflect` are required,
   - `spellcraft` and `sigil-development` are required maintenance authoring paths,
   - `invoke` is required for lifecycle authoring when installed,
   - `decision-gate` is an optional capability used only for consequential unresolved choices that do not fit inventory, ontology, or maintenance routes,
   - `research` is a selected sigil, not a setup profile or repository,
   - maintain mode aggregates all selected sigil/spell signals and uses `sigil-maintenance-loop` when available.
3. Extend modes to include:
   - `setup`,
   - `checkpoint`,
   - `research` when the `research` sigil is selected,
   - `maintain`.
4. Add runtime UX language for interactive setup and option cards.
5. Define Necronomicon interview modes against the `structured-interview-kits` contract:
   - `setup-profile`,
   - `gap-check`,
   - `checkpoint-review`,
   - `research-clarification`,
   - `maintenance-decision`.
6. Add checkpoint and memory policy sections.
7. Add maintenance loop section that references `signal-observer`, `workflow-reflect`, `sigil-maintenance-loop`, `spellcraft`, and `sigil-development`, including all-selected signal aggregation.

### Deliverables

- Updated [spells/necronomicon/README.md](../../../spells/necronomicon/README.md).
- Updated output contract with profile, selected sigils, checkpoint, research, route preset, maintenance fields, invoke route status, web fallback status, and per-sigil signal coverage flags.

### Validation

- Manual spellcraft contract check:
  - identity,
  - trigger conditions,
  - required capabilities,
  - optional capabilities,
  - modes,
  - shared state,
  - execution phases,
  - gates,
  - observability,
  - output contract.
- Markdown link validation for changed docs.

### Exit Criteria

- The spell file is an authoritative UX contract for later bootstrap and adapter changes.

## Wave 2 - Manifest Schema And Profiles

### Objective

Make bootstrap capable of generating profile-aware and capability-aware Necronomicon harness state.

### Work Items

1. Add setup profile inputs to [tools/bootstrap_arcanum.sh](../../../tools/bootstrap_arcanum.sh):
   - `--necronomicon-profile basic-inventory|ontology-harness|custom`,
   - optional `--enable-sigil research`,
   - optional `--inventory-root <path>`,
   - optional `--memory-policy lean|standard|strict`,
   - optional `--fallback-policy suggest-only|ask-before-add|guarded-auto`,
   - optional `--checkpoint-policy manual|standard|strict`.
2. Implement dependency auto-add logic.
   - `necronomicon` auto-adds `structured-interview-kits` when setup, checkpoint, research clarification, or maintenance modes are enabled.
   - selecting the `research` sigil auto-adds `inventory` and `context-builder` when missing.
   - Each auto-add is recorded in `dependency_auto_adds` with the triggering requester, added capability, reason, and source rule.
3. Extend `.arcanum/necronomicon/capabilities.json` with an explicit manifest contract. The manifest should be both human-inspectable and machine-readable, with enough detail to explain why each capability is active.

   | Field                   | Type   | Required | Definition                                                                                                                                                                          |
   | ----------------------- | ------ | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
   | `version`               | string | Yes      | Manifest schema version, independent from Arcanum package version. Start with `0.2.0` for the profile-aware schema.                                                                 |
   | `profile`               | string | Yes      | Selected setup profile: `basic-inventory`, `ontology-harness`, or `custom`.                                                                                                         |
   | `runtime`               | string | Yes      | Runtime adapter target that generated this harness, such as `github-copilot`, `claude`, `codex`, or `none`.                                                                         |
   | `install_prefix`        | string | Yes      | Root for generated runtime state, normally `.arcanum`.                                                                                                                              |
   | `inventory_root`        | string | Yes      | Inventory location used by Necronomicon. May be `.arcanum/inventory/` or a project-selected existing knowledge base path.                                                           |
   | `setup_decisions_path`  | string | Yes      | Path to the durable human-readable setup rationale.                                                                                                                                 |
   | `common_routes_path`    | string | Yes      | Path to project-local route presets, normally `.arcanum/necronomicon/routes/common-routes.json`.                                                                                    |
   | `gap_ledger_path`       | string | Yes      | Path to the project-local gap ledger, normally `.arcanum/necronomicon/gaps.json`.                                                                                                   |
   | `selected_sigils`       | array  | Yes      | Sigils explicitly selected by setup or user choice. Includes `research` when the research sigil is enabled.                                                                         |
   | `selected_spells`       | array  | Yes      | Spells explicitly selected by setup or user choice.                                                                                                                                 |
   | `dependency_auto_adds`  | array  | Yes      | Capability additions made by dependency rules. Each entry should include requester, added capability, reason, and source rule.                                                      |
   | `excluded_capabilities` | array  | Yes      | Capabilities the user intentionally excluded, including exclusions that override profile defaults when allowed.                                                                     |
   | `harness_commands`      | array  | Yes      | Commands exposed by this setup, including `setup`, `start`, `resume`, `route`, `checkpoint`, `research` when selected, `update-capabilities`, `maintain`, and `close` when enabled. |
   | `fallback_policy`       | string | Yes      | Route fallback behavior: `suggest-only`, `ask-before-add`, or `guarded-auto`.                                                                                                       |
   | `state_privacy_policy`  | object | Yes      | Redaction and persistence rules for generated harness state.                                                                                                                        |
   | `memory_policy`         | object | Yes      | How the session stores project, session, route, user-instruction, and ontology-candidate memory.                                                                                    |
   | `checkpoint_policy`     | object | Yes      | When checkpoints trigger, where they are written, and whether promotion candidates are allowed.                                                                                     |
   | `research_policy`       | object | Yes      | Research sigil enablement, run artifact path template, budget, source order, robot-talks escalation rule, and durable-finding rules.                                                |
   | `maintenance_policy`    | object | Yes      | Whether route/capability signals are collected, where reports are written, and whether auto-authoring is blocked.                                                                   |
   | `route_policy`          | object | Yes      | Route preset resolution order, confidence thresholds, miss tracking, and stale-route validation behavior.                                                                           |
   | `created_at`            | string | Yes      | ISO 8601 creation timestamp.                                                                                                                                                        |
   | `updated_at`            | string | Yes      | ISO 8601 last update timestamp.                                                                                                                                                     |

   Policy details should be concrete rather than labels only:
   - `memory_policy` defines retention level (`lean`, `standard`, `strict`), allowed memory classes, evidence requirements, and whether user-instruction memory is session-only.
   - `checkpoint_policy` defines triggers, checkpoint interval, destination path, required sections, and the rule that ontology/inventory promotions remain candidates until approved.
   - `research_policy` defines sigil enablement (`enabled: true` only when the `research` sigil is selected), required inputs, per-session run artifact path template, budget limits, search order, robot-talks escalation, synthesis gate, and whether durable findings may be written to inventory.
   - `maintenance_policy` defines signal capture scope (including selected capabilities), cross-sigil synthesis behavior, report path, recommendation classes, stale-signal gap handling, and the invariant that reusable spells or sigils require explicit approval before creation.
   - `route_policy` defines exact command precedence, preset matching, fallback behavior, route miss tracking, and stale preset review.
   - `state_privacy_policy` defines forbidden persisted values, redaction behavior, artifact coverage, and the rule that secrets must be typed directly into terminals or secret stores rather than captured in Necronomicon state.

4. Generate `.arcanum/necronomicon/setup-decisions.md` with selected profile, selected capabilities, trade-offs, and auto-added dependencies.
5. Generate empty route and maintenance folders:
   - `.arcanum/necronomicon/routes/`,
   - `.arcanum/necronomicon/maintenance/`.
     Do not generate a repository-like research root such as `.arcanum/necronomicon/research/`; the `research` sigil writes per-session run artifacts using the manifest path template.
6. Generate an initial gap ledger at `.arcanum/necronomicon/gaps.json` with no open gaps and a documented schema.
7. Generate a default no-secrets state privacy policy in the manifest and setup decisions file.

### Deliverables

- Updated [tools/bootstrap_arcanum.sh](../../../tools/bootstrap_arcanum.sh).
- Updated generated manifest shape.
- Generated setup decisions document.
- Generated gap ledger.

### Validation

Run temp installs for at least these scenarios:

1. `basic-inventory` installs inventory and context-builder without ontology-vault.
2. `ontology-harness` installs inventory, context-builder, ontology-vault, and ontology-harness.
3. custom profile selecting ontology-vault auto-adds inventory and context-builder.
4. `basic-inventory` with `--enable-sigil research` includes `research` in selected sigils, writes `research_policy.enabled: true`, writes a per-session `research_policy.artifact_path_template`, and recommends robot-talks without forcing it for every route.
5. custom profile preserves invoke lifecycle routing and does not require a dedicated pre-execution research command.
6. state privacy validation: running bootstrap with a sample secret value present in env vars produces a manifest, setup-decisions file, and `gaps.json` that contain no raw secret values; the redaction marker appears wherever sensitive context would otherwise be written, and the `state_privacy_policy` block lists the forbidden persisted value classes.

Validate generated JSON with `jq empty`.

### Exit Criteria

- Bootstrap produces valid profile-aware Necronomicon harness state.
- Dependency auto-adds are explicit in the manifest and setup decisions file.
- Generated state is sufficient for assistant adapters to act as the first-pass runtime without a full local CLI.
- Gap ledger path exists and is referenced by the manifest.
- State privacy policy exists and forbids persisting secrets in generated harness artifacts.

## Wave 3 - Interactive Setup Wizard

### Objective

Make runtime setup understandable to users by explaining choices and trade-offs.

### Work Items

1. Update generated `arcanum-necronomicon` adapters for GitHub Copilot, Claude, and Codex.
2. Add setup process for `setup` and `start --setup`.
   - Model setup as a `structured-interview-kits` mode named `setup-profile`.
   - Ask exactly one setup question at a time.
   - Patch setup decisions and manifest state after each consequential answer.
3. Define option cards for profile choices:
   - what the profile enables,
   - what it costs,
   - what state it creates,
   - recommended default,
   - when to avoid it.
4. Add setup questions:
   - harness profile,
   - inventory root,
   - ontology need,
   - research sigil need,
   - memory policy,
   - fallback policy,
   - maintenance signal policy.
5. Ensure adapters ask only unanswered questions when setup decisions already exist.
6. When later answers imply profile or capability changes, present a gated confirmation card before mutating the manifest. The card must show current value, proposed value, reason, auto-added dependencies, consequences, rejected alternatives, and the target update path.

### Deliverables

- Updated adapter generation in [tools/bootstrap_arcanum.sh](../../../tools/bootstrap_arcanum.sh).
- Updated [arcana/sigil-runtime-installer/SKILL.md](../../../arcana/sigil-runtime-installer/SKILL.md).
- Updated generated command examples after regeneration.

### Validation

- Inspect generated GitHub Copilot adapter text.
- Inspect generated Claude and Codex command text.
- Confirm setup questions explain consequences, not just labels.
- Confirm setup can be skipped when manifest already exists.
- Confirm profile and capability changes require explicit confirmation and update `.arcanum/necronomicon/setup-decisions.md`.

### Exit Criteria

- Users can understand what they are setting up and why each choice matters.

## Wave 4 - Checkpoints And Memory

### Objective

Add explicit checkpoint behavior so session distillation becomes reliable and ontology promotions are deliberate.

### Work Items

1. Add `checkpoint` mode to the spell process.
2. Define checkpoint triggers:
   - user request,
   - before close,
   - before capability updates,
   - after major research synthesis,
   - after route misses or repeated correction,
   - after N meaningful routes.
3. Define checkpoint output path:
   - `.arcanum/necronomicon/sessions/<session-id>/checkpoints/<timestamp>.md`.
4. Define checkpoint content:
   - objective,
   - active context,
   - source-backed facts,
   - inferred claims,
   - decisions,
   - unresolved questions,
   - contradictions,
   - route patterns,
   - capability gaps,
   - candidate inventory entries,
   - candidate ontology concepts,
   - candidate premises,
   - candidate axioms,
   - candidate bridge edges,
   - next recommended route.
5. Add memory classes:
   - project memory,
   - session memory,
   - route memory,
   - user instruction memory,
   - ontology candidate memory.
6. Add candidate routing rules:
   - inventory entry candidates route to inventory `ingest`, `backfill`, or `sync` flows with source references,
   - ontology concept candidates route to `ontology-vault map` or `ontology-vault promote-confidence`,
   - premise and axiom candidates route to `ontology-vault premise-review`,
   - bridge edge candidates route to ontology-vault branch or bridge validation flows,
   - convention candidates route to `ontology-vault convention-update`,
   - consequential unresolved choices that do not fit inventory, ontology, or maintenance routes route to `decision-gate` when installed; otherwise the choice is logged in the gap ledger with a capability gap entry.
7. Add unresolved questions, contradictions, capability gaps, and blocked decisions to the project-local gap ledger during checkpoint review.
8. Apply state privacy redaction before writing checkpoint or memory artifacts.

### Deliverables

- Updated [spells/necronomicon/README.md](../../../spells/necronomicon/README.md).
- Generated checkpoint folder in setup where appropriate.
- Optional checkpoint template under a future templates location if needed.

### Validation

- Checkpoint mode lists candidate promotions without silently applying them.
- Checkpoint mode names the downstream promotion route for each candidate type.
- Memory sections separate facts, inference, decisions, and candidates.
- Close flow references the latest checkpoint.
- Checkpoint review updates the gap ledger when unresolved items remain open.
- Checkpoint and memory artifacts do not persist secrets or raw sensitive values.

### Exit Criteria

- Session memory has reliable distillation points and promotion candidates remain gated.

## Wave 5 - Research Sigil

### Objective

Create `research` as a bounded Necronomicon sigil that transforms information gathering without turning Necronomicon into an unbounded search loop or repository-like state store.

### Work Items

1. Add a Necronomicon-owned `research` sigil contract and expose `research` mode only when the sigil is enabled.
2. Define required research inputs:
   - question,
   - scope,
   - budget,
   - source plan,
   - stop condition.
     Default budget when the caller does not supply one: `sources_max: 8`, `depth_max: 2`, `escalations_max: 1`.
3. Define research search order:
   - active session memory and checkpoints,
   - `.arcanum/inventory/`,
   - ontology outputs and premise/axiom ledgers,
   - repository docs,
   - codebase,
   - web sources when available,
   - optional robot-talks escalation.
4. Define research brief output:
   - question,
   - search trail,
   - sources inspected,
   - inventory entries used or missing,
   - ontology concepts touched,
   - premises and axioms affected,
   - contradictions,
   - open questions,
   - recommended next route.
     Store research briefs as per-session run artifacts, not as a repository-style research folder.
5. Add post-research action options:
   - file synthesis into inventory,
   - create premise candidate,
   - create axiom candidate,
   - create ontology concept candidate,
   - create bridge edge candidate,
   - mark contradiction,
   - open decision gate,
   - defer.
6. Add robot-talks escalation criteria.
7. Route ontology post-research actions through ontology-vault modes instead of promoting them directly from research mode.
8. Add research contradictions, unanswered source gaps, and blocked synthesis questions to the gap ledger with the research brief as source.
9. If web access is unavailable, continue with local-source-only research and return a `web-unavailable` note in the research result.
10. Apply state privacy redaction before writing research briefs, source trails, or durable inventory synthesis candidates.

### Deliverables

- Updated [spells/necronomicon/README.md](../../../spells/necronomicon/README.md).
- New Necronomicon-owned `research` sigil contract.
- Research sigil manifest policy with per-session run artifact path template.
- Adapter copy that explains research as a bounded selected sigil.

### Validation

- Research mode is unavailable when the `research` sigil is disabled; routing should offer `update-capabilities` to enable it.
- Research mode cannot proceed without question and scope when enabled.
- Research mode records sources and search trail.
- Robot-talks is opt-in or escalation-only.
- Research mode reports `web-unavailable` when runtime/tooling cannot access web sources.
- Durable inventory filing requires source references.
- Ontology post-research actions produce ontology-vault handoffs, not direct canonical ontology edits.
- Research mode updates the gap ledger for unresolved or contradictory findings.
- Research artifacts omit or redact secrets and sensitive local context.

### Exit Criteria

- The selected `research` sigil can produce evidence-backed synthesis and next-route recommendations without uncontrolled exploration or repository-like copied state.

## Wave 6 - Common Routes Interface

### Objective

Give users a composable interface for recurring project routes.

### Work Items

1. Add a project-local route preset model under `.arcanum/necronomicon/routes/`.
2. Use a filename that avoids old runtime-book confusion, such as `common-routes.json` or `README.md`; do not use `ROUTES.md` as a canonical runtime registry.
3. Define route preset fields:
   - route ID,
   - trigger text,
   - selected route target,
   - fallback candidates,
   - confidence rule,
   - checkpoint policy,
   - last used,
   - miss count,
   - validation status.
4. Add default route presets:
   - research unknown concept -> `research` sigil when selected; otherwise `update-capabilities` to enable `research`,
   - map business intent to system evidence -> `ontology-harness`,
   - prepare implementation task -> `invoke plan`, then `task-session`,
   - lifecycle authoring (`define`, `design`, `plan`, `full`, `validate`) -> `invoke` when installed,
   - execute bounded task -> `task-session`,
   - create reusable workflow -> `spellcraft`,
   - repeated missing behavior -> `maintain`, then `sigil-development`,
   - cross-sigil maintenance synthesis -> `maintain`, then `sigil-maintenance-loop`.
5. Add interactive route preset creation to `update-capabilities` or `maintain`.

### Deliverables

- Route preset schema in spell docs.
- Bootstrap-generated route folder and optional default route file.
- Adapter routing process that checks route presets after exact command matches.

### Validation

- Route presets are local harness state.
- Route presets do not override explicit command names.
- Stale route presets can be flagged by maintenance mode.

### Exit Criteria

- Users can configure repeatable project routes without editing canonical Arcanum registries.

## Wave 7 - Maintenance Loop

### Objective

Give Necronomicon an evidence-backed loop for improving its own route and capability surface.

### Work Items

1. Add `maintain` mode.
2. Use `signal-observer` after meaningful sessions to capture:
   - route misses,
   - user corrections,
   - repeated tasks,
   - capability updates,
   - quality gaps,
   - output drift,
   - repeated requests for new behavior,
   - signal coverage across all selected sigils and spells.
3. Read the gap ledger before producing maintenance recommendations so repeated unresolved gaps can become route or capability proposals.
4. Use `workflow-reflect` and `sigil-maintenance-loop` to analyze Necronomicon signals and produce cross-sigil synthesis.
5. Produce maintenance reports under `.arcanum/necronomicon/maintenance/<date>-report.md`.
6. Classify recommendations:
   - add route preset,
   - add existing capability,
   - revise setup profile,
   - create local spell,
   - propose reusable library spell,
   - create local sigil,
   - propose reusable library sigil,
   - address missing or stale selected-signal coverage,
   - defer pending more signals.
7. Route spell creation through `spellcraft`.
8. Route sigil creation through `sigil-development`.
9. Route cross-sigil maintenance synthesis to `sigil-maintenance-loop` when installed; if missing, record a maintenance capability gap and route to capability update.
10. Require user approval before creating or promoting new reusable artifacts.

### Deliverables

- Updated spell `maintain` mode.
- Maintenance report contract.
- Bootstrap-generated maintenance folder.
- Adapter instructions for maintenance recommendations.

### Validation

- Maintenance mode proposes changes from evidence, not anecdotes.
- Maintenance mode includes open gap ledger patterns in its evidence base.
- Maintenance mode includes all-selected signal coverage checks and marks stale/missing signal coverage as explicit gaps.
- Maintenance mode does not mutate canonical sigils or spells directly.
- Maintenance reports omit or redact secrets and sensitive local context.
- Local-first recommendations are distinguished from reusable library promotion.

### Exit Criteria

- Necronomicon can improve its project harness behavior without creating library bloat.

## Wave 8 - Docs And Consumer Regeneration

### Objective

Update public-facing docs and generated examples after the runtime contract stabilizes.

### Work Items

1. Update [spells/ontology-harness/README.md](../../../spells/ontology-harness/README.md) to clarify inventory dependency for ontology profile.
2. Update [spells/README.md](../../../spells/README.md) if setup profiles change how users understand Necronomicon.
3. Update [registry/SPELLS.md](../../../registry/SPELLS.md) only if public registry wording must change.
4. Update [arcana/sigil-runtime-installer/SKILL.md](../../../arcana/sigil-runtime-installer/SKILL.md) with setup profile and wizard support.
5. Regenerate a consumer example, likely Sonar Loop, after bootstrap changes.
6. Update CyberAlchemy teaching page if the final UX differs from the current tour.

### Deliverables

- Updated docs.
- Regenerated consumer runtime files.
- Updated teaching artifact.

### Validation

- Markdown link checks on changed markdown files.
- JSON validation on generated manifests.
- Search for stale language that implies `.arcanum/necronomicon/` is a copied definition store.

### Exit Criteria

- Docs, generated adapters, and teaching page agree with the implemented behavior.

## Wave 9 - Hardening And Release Gate

### Objective

Validate the whole harness UX before committing or releasing.

### Work Items

1. Run shell syntax checks.
2. Run temp bootstrap installs across supported runtimes:
   - GitHub Copilot,
   - Claude,
   - Codex,
   - none.
3. Exercise profile cases:
   - basic inventory,
   - ontology harness,
   - base profile with `research` sigil enabled,
   - custom with ontology-vault dependency auto-add.
4. Validate generated JSON files.
5. Validate markdown links.
6. Inspect generated command adapters for setup wizard and mode coverage.
7. Confirm lifecycle authoring requests route to `invoke` when installed, with explicit gap handling when missing.
8. Confirm cross-sigil maintenance synthesis routes to `sigil-maintenance-loop` when installed, with fallback gap handling when missing.
9. Confirm Necronomicon harness state does not contain copied canonical definitions.
10. Confirm old runtime-book folders are blocked or migrated safely.
11. Confirm root and nested repo statuses before commit.

### Validation Commands

Use guard from repository root where appropriate:

```bash
./tools/guard bash -n arcanum/tools/bootstrap_arcanum.sh
```

For generated JSON:

```bash
jq empty <generated-capabilities-json>
```

For changed markdown files:

```bash
./tools/check_markdown_links.sh <changed-markdown-file>
```

### Exit Criteria

- All temp install scenarios pass.
- Generated manifests validate.
- Runtime adapters include setup, research when the `research` sigil is selected, checkpoint, route, update-capabilities, maintain, and close.
- No copied `formulae/`, `transmutations/`, `arcana/`, `spells/`, `registry/`, or `framework/` folders appear under `.arcanum/necronomicon/`.

## Cross-Wave Data Contracts

### Capabilities Manifest

Planned fields for `.arcanum/necronomicon/capabilities.json`:

```json
{
  "version": "0.2.0",
  "profile": "basic-inventory",
  "runtime": "github-copilot",
  "install_prefix": ".arcanum",
  "inventory_root": ".arcanum/inventory",
  "setup_decisions_path": ".arcanum/necronomicon/setup-decisions.md",
  "common_routes_path": ".arcanum/necronomicon/routes/common-routes.json",
  "gap_ledger_path": ".arcanum/necronomicon/gaps.json",
  "selected_sigils": ["research"],
  "selected_spells": [],
  "dependency_auto_adds": [
    {
      "requester": "ontology-harness",
      "added_capability": "inventory",
      "reason": "ontology routes require source-grounded knowledge reuse",
      "source_rule": "ontology-harness requires ontology-vault, inventory, and context-builder"
    }
  ],
  "excluded_capabilities": [],
  "harness_commands": [],
  "fallback_policy": "ask-before-add",
  "state_privacy_policy": {
    "level": "standard-redaction",
    "forbidden_persisted_values": [
      "credentials",
      "tokens",
      "passwords",
      "private-keys",
      "secret-values"
    ],
    "artifact_coverage": [
      "manifest",
      "setup-decisions",
      "checkpoints",
      "research-briefs",
      "gap-ledger",
      "maintenance-reports"
    ],
    "redaction_marker": "[REDACTED]",
    "secret_entry_instruction": "type secrets directly into the terminal or configured secret store"
  },
  "memory_policy": {
    "level": "standard",
    "classes": [
      "project-memory",
      "session-memory",
      "route-memory",
      "user-instruction-memory",
      "ontology-candidate-memory"
    ],
    "evidence_required_for_facts": true,
    "user_instruction_scope": "session-only"
  },
  "checkpoint_policy": {
    "level": "standard",
    "trigger_after_meaningful_routes": 5,
    "triggers": [
      "user-request",
      "before-close",
      "before-capability-update",
      "after-major-research-synthesis",
      "after-route-miss"
    ],
    "path_template": ".arcanum/necronomicon/sessions/<session-id>/checkpoints/<timestamp>.md",
    "promotion_mode": "candidate-only"
  },
  "research_policy": {
    "sigil": "research",
    "enabled": true,
    "artifact_path_template": ".arcanum/necronomicon/sessions/<session-id>/research-runs/<timestamp>.md",
    "required_inputs": [
      "question",
      "scope",
      "budget",
      "source_plan",
      "stop_condition"
    ],
    "search_order": ["session", "inventory", "ontology", "docs", "code", "web"],
    "web_sources": "runtime-supported-optional",
    "web_unavailable_behavior": "local-sources-plus-note",
    "default_budget": {
      "sources_max": 8,
      "depth_max": 2,
      "escalations_max": 1
    },
    "robot_talks": "escalation-only",
    "durable_inventory_findings": "source-references-required"
  },
  "maintenance_policy": {
    "signals": "enabled",
    "signal_scope": "route-and-all-selected-sigils-and-spells",
    "cross_sigil_synthesis": "sigil-maintenance-loop-when-installed",
    "flag_missing_signal_coverage": true,
    "report_path_template": ".arcanum/necronomicon/maintenance/<date>-report.md",
    "recommendation_classes": [
      "add-route-preset",
      "add-existing-capability",
      "revise-setup-profile",
      "create-local-spell",
      "propose-reusable-library-spell",
      "create-local-sigil",
      "propose-reusable-library-sigil",
      "defer"
    ],
    "auto_author": false
  },
  "route_policy": {
    "explicit_command_precedence": true,
    "lifecycle_authoring_route": "invoke-when-installed",
    "cross_sigil_maintenance_route": "sigil-maintenance-loop-when-installed",
    "preset_match_min_confidence": "medium",
    "track_misses": true,
    "stale_after_miss_count": 3,
    "stale_review_route": "maintain"
  },
  "created_at": "2026-05-15T00:00:00Z",
  "updated_at": "2026-05-15T00:00:00Z"
}
```

### Checkpoint Artifact

Planned fields for checkpoint markdown:

- session ID,
- timestamp,
- current objective,
- active context,
- source-backed facts,
- inferred claims,
- decisions,
- contradictions,
- unresolved questions,
- route patterns,
- capability gaps,
- candidate inventory entries,
- candidate ontology concepts,
- candidate premises,
- candidate axioms,
- candidate bridge edges,
- next recommended route.

### Gap Ledger

Default project-local gap ledger path:

```text
.arcanum/necronomicon/gaps.json
```

Each gap entry should include:

- gap ID,
- status: `open`, `blocked`, `in-review`, `closed`, or `deferred`,
- source artifact,
- source mode,
- severity: `low`, `medium`, `high`, or `blocker`,
- owning route,
- affected capability,
- observed evidence,
- unresolved question or contradiction,
- next action,
- linked checkpoint, research brief, decision, or maintenance report,
- created timestamp,
- updated timestamp.

Initial `gaps.json` shape:

```json
{
  "version": "0.1.0",
  "ledger_path": ".arcanum/necronomicon/gaps.json",
  "open_count": 0,
  "entries": [
    {
      "id": "gap-0001",
      "status": "open",
      "severity": "medium",
      "source_artifact": ".arcanum/necronomicon/sessions/<session-id>/checkpoints/<timestamp>.md",
      "source_mode": "checkpoint",
      "owning_route": "research",
      "affected_capability": "ontology-vault",
      "observed_evidence": [],
      "unresolved_question": "What premise needs review before promotion?",
      "contradiction": null,
      "next_action": "route to ontology-vault premise-review",
      "links": [],
      "created_at": "2026-05-15T00:00:00Z",
      "updated_at": "2026-05-15T00:00:00Z"
    }
  ]
}
```

### Route Preset

Planned route preset fields:

```json
{
  "id": "prepare-implementation-task",
  "trigger": "prepare implementation task",
  "selected_route_target": "invoke",
  "fallback_candidates": ["task-session"],
  "confidence_rule": "medium when request includes implementation uncertainty",
  "checkpoint_policy": "before-invoke",
  "last_used": null,
  "miss_count": 0,
  "validation_status": "unvalidated"
}
```

## Counterarguments And Mitigations

| Concern                                         | Risk                                            | Mitigation                                                                                                                                               |
| ----------------------------------------------- | ----------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Two setup modes are too simple.                 | Users outgrow the binary quickly.               | Keep the headline base profiles (`basic-inventory`, `ontology-harness`) plus `custom`, and make `research` a selectable sigil with dependency auto-adds. |
| Always adding inventory with ontology is heavy. | Small repos may resist setup overhead.          | Allow inventory to point at existing docs/wiki, but keep the dependency concept mandatory.                                                               |
| Research mode can become unbounded.             | Agent spends time searching without conclusion. | Require question, scope, budget, source plan, and synthesis checkpoint.                                                                                  |
| Robot Talks is too expensive for normal use.    | Multi-agent research can add noise.             | Make it escalation-only for cross-layer contradictions.                                                                                                  |
| Checkpoints create false authority.             | Session summaries may outrank source evidence.  | Separate facts, inference, decisions, and candidates; require evidence links for promotion.                                                              |
| New memory sigils may overfit early.            | Premature abstraction creates maintenance cost. | Implement checkpoint behavior inside `necronomicon` first; extract later if reused.                                                              |
| Common routes can become stale.                 | Bad routing persists.                           | Track last-used, miss count, and validation status; review during maintenance.                                                                           |
| Maintenance loop can create bloat.              | Too many local or library artifacts.            | Propose local-first changes and require approval before spell/sigil creation.                                                                            |

## Recommended Implementation Order

1. Wave 1 - Spell Contract Reshape.
2. Wave 2 - Manifest Schema And Profiles.
3. Wave 3 - Interactive Setup Wizard.
4. Wave 4 - Checkpoints And Memory.
5. Wave 5 - Research Sigil.
6. Wave 6 - Common Routes Interface.
7. Wave 7 - Maintenance Loop.
8. Wave 8 - Docs And Consumer Regeneration.
9. Wave 9 - Hardening And Release Gate.

Do not start with unrelated reusable sigils. The planned exception is `research`: implement it first as a Necronomicon-owned sigil, then promote it to a reusable library asset only after reuse pressure appears. Extract `session-memory`, `session-checkpoint`, or `necronomicon-maintenance-loop` only after reuse pressure appears.
