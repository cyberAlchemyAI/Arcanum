---
module: necronomicon
version: current
status: draft
updatedAt: 2026-05-23
docType: wave-plan
---

# Necronomicon Wave Plan

## Purpose

This plan restarts Necronomicon implementation around the corrected center of gravity: inventory and ontology substrate handling. The goal is to prove Necronomicon as a knowledge harness before expanding setup, routing, research, maintenance, and release behavior.

## North Star

Necronomicon should help the user understand:

- what the repository already knows,
- which facts are source-backed,
- which claims are only candidates,
- where contradictions or missing coverage exist,
- which capability owns the next step,
- why no promotion happened silently.

## Implementation Principles

1. Inventory is required for Necronomicon; without inventory, the harness routes to setup/install guidance instead of degraded operation.
2. Inventory retrieval comes before broad source search for durable knowledge questions.
3. Session evidence is useful, but low authority.
4. Ontology-sensitive claims remain candidates until `ontology-harness` or `ontology-vault` handles them.
5. Bootstrap configures the substrate; it is not the first proof of product value.
6. Research is bounded and follows substrate rules.
7. Invoke receives lifecycle authoring context only after knowledge, vocabulary, and gaps are explicit.
8. Maintenance recommendations come from accumulated gaps, route misses, and observability signals.
9. Necronomicon state never becomes a copied canonical definition store.
10. Generated state must not persist secrets.

## Wave Overview

| Wave | Name | Target Layer | Primary Outcome |
| --- | --- | --- | --- |
| 0 | Baseline And Safety | L0 | Confirm current contracts, dirty state, and validation gates. |
| 1 | Substrate Contract | L0 | Define state shapes and adapter behavior for inventory-first retrieval and authority classification. |
| 2 | Substrate Proof | L0 | Implement one adapter-mediated substrate loop and validate sample scenarios. |
| 3 | Setup And Manifest | L1 | Generate profile-aware setup state that configures inventory and ontology handling. |
| 4 | Session Workbench | L2 | Add active interaction, side notes, checkpoints, and candidate queues. |
| 5 | Research And Handoffs | L3 | Add bounded research packets and lifecycle handoff rules. |
| 6 | Routes And Maintenance | L4 | Add route presets, route miss tracking, maintenance reports, and signal coverage. |
| 7 | Docs And Release Gate | L4 | Regenerate adapters/docs and validate supported runtimes. |

## Wave 0: Baseline And Safety

### Objective

Avoid trampling unrelated work and confirm the current Necronomicon development pack is the active target.

### Work Items

1. Check git status for Necronomicon and bootstrap files.
2. Validate current shell syntax for bootstrap.
3. Validate current `.arcanum/necronomicon/capabilities.json` when present.
4. Identify generated artifacts that should remain local.

### Validation

- `git status --short -- spells/necronomicon/development tools/bootstrap_arcanum.sh .arcanum/necronomicon`
- `bash -n tools/bootstrap_arcanum.sh`
- `jq empty .arcanum/necronomicon/capabilities.json`

### Exit Criteria

- Dirty state is known.
- Current runtime state is understood.
- Implementation can proceed without reverting unrelated changes.

## Wave 1: Substrate Contract

### Objective

Define the concrete state and adapter contract for the L0 substrate loop.

### Work Items

1. Add or revise Necronomicon canonical README language so substrate-first behavior is authoritative.
2. Define `gaps.json` schema with source gaps, contradiction gaps, decision gaps, capability gaps, and route gaps.
3. Define `authority-classification.jsonl` shape.
4. Define session evidence shape.
5. Define handoff packet shape.
6. Define adapter instructions for:
   - required inventory lookup,
   - blocked-state setup/install guidance when inventory is missing,
   - source-backed vs candidate labels,
   - no-promotion closeout.

### Deliverables

- Updated canonical Necronomicon contract.
- Schema snippets or examples in development docs.
- Adapter instruction delta for bootstrap generation.

### Validation

- Markdown link check for changed docs.
- Manual contract review against `DEFINE.md`, `DESIGN.md`, and `IMPLEMENTATION-LAYERING.md`.

### Exit Criteria

- Implementers can build the substrate loop without reopening product design.

## Wave 2: Substrate Proof

### Objective

Prove the smallest working Necronomicon loop.

### Work Items

1. Implement required inventory availability detection.
2. Implement or document adapter-mediated inventory lookup before broad search.
3. Write a sample session evidence artifact.
4. Write an authority classification record.
5. Write or update `gaps.json`.
6. Write a handoff packet with owner and no-promotion note.
7. Add scenario fixtures:
   - inventory hit,
   - missing inventory blocked state,
   - ontology candidate,
   - contradiction gap.

### Deliverables

- L0 substrate proof artifacts under `.arcanum/necronomicon/` or curated development fixtures.
- Scenario fixtures for review.

### Validation

- `jq empty` on generated JSON.
- Scenario review confirms facts/candidates/gaps are distinct.
- Candidate promotion is absent.

### Exit Criteria

- Necronomicon has proven distinct value beyond routing.

## Wave 3: Setup And Manifest

### Objective

Make bootstrap generate setup state that configures the substrate.

### Work Items

1. Add setup profile options:
   - `basic-inventory`,
   - `ontology-harness`,
   - `custom`.
2. Add inventory root policy.
3. Add ontology profile and dependency auto-add rules.
4. Generate `setup-decisions.md`.
5. Generate initial `gaps.json`, route folder, maintenance folder, and policy blocks.
6. Preserve no-copied-definition-store guardrails.

### Validation

- Temp installs for inventory profile, ontology profile, and custom profile.
- JSON validation.
- Setup decisions mention dependencies, exclusions, privacy, and inventory root.

### Exit Criteria

- Setup makes substrate choices inspectable and repeatable.

## Wave 4: Session Workbench

### Objective

Make substrate work resumable across turns and sessions.

### Work Items

1. Add `active-interaction.json`.
2. Add `side-notes.jsonl`.
3. Add checkpoint artifact format.
4. Add candidate queues for inventory, ontology, premise, contradiction, and decision items.
5. Add resume summary behavior.

### Validation

- Continuation scenario preserves active owner.
- Side note scenario captures without derailment.
- Checkpoint separates source-backed facts, inferences, candidates, contradictions, and gaps.

### Exit Criteria

- Necronomicon can preserve work without inflating memory authority.

## Wave 5: Research And Handoffs

### Objective

Add bounded evidence gathering and lifecycle handoff on top of the substrate.

### Work Items

1. Add local-first research packet contract.
2. Add source trail and stop condition.
3. Add contradiction handling.
4. Add inventory filing option.
5. Add ontology review option.
6. Add invoke handoff when lifecycle authoring is ready.

### Validation

- Research blocks without question and scope.
- Research emits source trail and gaps.
- Invoke handoff includes authority labels and unresolved gaps.

### Exit Criteria

- Research and lifecycle authoring consume substrate context instead of bypassing it.

## Wave 6: Routes And Maintenance

### Objective

Make repeated substrate outcomes improve the harness from evidence.

### Work Items

1. Add route presets.
2. Add route miss tracking.
3. Add stale route review.
4. Add maintenance report.
5. Aggregate observability and gap ledger signals.
6. Route reusable spell/sigil changes through owning lifecycle tools.

### Validation

- Explicit command names outrank presets.
- Maintenance recommendations cite evidence.
- Reusable artifact creation requires approval.

### Exit Criteria

- Necronomicon improves local harness behavior without library bloat.

## Wave 7: Docs And Release Gate

### Objective

Package the substrate-first Necronomicon for supported runtime consumers.

### Work Items

1. Sync canonical docs.
2. Regenerate command adapters.
3. Validate Codex, GitHub Copilot, Claude, and none runtimes where supported.
4. Search for stale route-first language.
5. Verify generated `.arcanum/necronomicon/` has no copied canonical definition store.

### Validation

- Shell syntax checks.
- JSON validation.
- Markdown links.
- Runtime temp installs.
- Dirty-state review.

### Exit Criteria

- Necronomicon is release-ready as a substrate-first repository harness.

## Recommended Start

Start with Wave 1, then implement Wave 2 as the first proof. Avoid spending implementation time on profile-aware bootstrap until the substrate contract is concrete enough to configure.

## Change History

| Date | Change |
| --- | --- |
| 2026-05-23 | Restarted wave plan around inventory and ontology substrate handling. |
