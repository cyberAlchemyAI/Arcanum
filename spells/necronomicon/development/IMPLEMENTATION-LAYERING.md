---
title: Necronomicon UX Implementation Layering
status: draft
updatedAt: 2026-05-15
owner: Arcanum maintainers
scope: workflow
---

# Necronomicon UX Implementation Layering

This document defines a progressive implementation layering model for the Necronomicon UX harness.

Scope note: Layer 0 is the minimum working unit POC that proves the concept with the smallest useful end-to-end slice. Every later layer must explicitly improve and preserve the guarantees from previous layers.

## Context

- Target: Necronomicon UX harness
- Current state: partially implemented planning and spell-contract work
- Primary user/operator: a repository user or assistant running Arcanum through generated local runtime adapters
- Primary constraint: reliable adapter-mediated state without turning `.arcanum/necronomicon/` into a copied canonical definition store
- Source references: [WAVE-PLAN.md](WAVE-PLAN.md), [spells/necronomicon/README.md](../../../spells/necronomicon/README.md), [tools/bootstrap_arcanum.sh](../../../tools/bootstrap_arcanum.sh)

## Layering Method

- POC-first: prove the guided harness shell with the smallest generated state and one routed lifecycle request.
- Decision-first: each layer exists to answer one important question about harness viability.
- Progressive hardening: each layer adds one bounded improvement theme: setup state, memory, research, maintenance, then release packaging.
- Non-regression: prior layer guarantees remain true in later layers.
- Evidence-gated promotion: the next layer starts only after current-layer exit evidence exists.

## Layer Boundary Heuristic

A layer ends at the smallest slice that changes what the team can responsibly decide next.

Use this sentence to define each boundary:

```text
After this layer, we know whether {decision unlocked}.
```

Use this value/cost heuristic when deciding whether to keep work in the current layer or move it later:

```text
Layer value = decision unlocked + user-visible outcome + risk reduced
Layer cost = implementation time + verification time + coordination burden

Stop the layer when the next unit of work has lower value-per-cost for the current decision than starting the next decision layer.
```

## Layer Decision Table

| Layer | Decision Question | Minimum Working Unit | User/Operator Outcome | Risk Reduced | Main Cost Drivers | Promotion Decision |
| ----- | ----------------- | -------------------- | --------------------- | ------------ | ----------------- | ------------------ |
| L0 (POC) | After this layer, we know whether adapter-mediated Necronomicon state can guide one repository from setup baseline to one routed lifecycle request without a full CLI. | Update the spell contract and bootstrap a single GitHub Copilot runtime with profile-aware manifest, setup decisions, gap ledger, route folder, and invoke lifecycle route gap handling. | A user can inspect generated harness state and see how a lifecycle request would route. | Proves the first-pass runtime boundary and avoids premature CLI scope. | Shell generation changes, one adapter path, JSON validation, link checks. | Continue to L1 when generated state is valid and the adapter instructions can explain setup and lifecycle routing. |
| L1 | After this layer, we know whether setup choices and dependency auto-adds are repeatable across supported profiles without silent manifest mutation. | Add setup-profile interview behavior, option cards, profile changes behind confirmation, and temp installs for `basic-inventory`, `ontology-harness`, and `custom`. | Users understand profile trade-offs and can revise setup through gated decisions. | Reduces setup ambiguity, dependency drift, and accidental capability mutation. | Multi-scenario bootstrap validation, adapter copy, setup-decision sync. | Harden to L2 when profile changes are auditable and setup can be skipped or resumed from existing state. |
| L2 | After this layer, we know whether session memory, checkpoints, and bounded research can preserve evidence while keeping promotions and secrets gated. | Add checkpoint mode, memory classes, gap ledger updates, research mode when selected, source trail, web-unavailable behavior, and privacy redaction. | Operators can distill work, record gaps, and run bounded research without creating false authority. | Reduces memory drift, unbounded research, secret persistence, and silent ontology promotion. | Checkpoint schema, research brief contract, redaction checks, promotion route mapping. | Scale to L3 when checkpoints and research briefs update gaps correctly and never promote candidates directly. |
| L3 | After this layer, we know whether recurring routes and maintenance can improve harness behavior from evidence rather than ad hoc edits. | Add common route presets, route miss tracking, stale preset review, selected-signal coverage, and maintenance reports. | Users can configure repeatable routes and get evidence-backed maintenance recommendations. | Reduces repeated route misses, stale presets, missing telemetry, and reusable-artifact bloat. | Route schema, signal ingestion, maintenance synthesis, approval gates. | Package to L4 when maintenance recommendations are local-first, evidence-backed, and explicitly approved before reusable artifact creation. |
| L4 | After this layer, we know whether the harness UX is release-ready across runtimes and consumer regeneration. | Run hardening across GitHub Copilot, Claude, Codex, and none runtimes; regenerate docs/examples; validate no copied canonical stores under `.arcanum/necronomicon/`. | Consumers receive a coherent project harness with validated adapters, docs, manifests, and examples. | Reduces release regression, adapter mismatch, stale docs, and generated-state contamination. | Temp installs, docs sync, consumer regeneration, status checks. | Release when all scenario validations pass and dirty-state review shows no accidental unrelated changes. |

## Capability or Scope Progression

| Capability / Scope Area | L0 (POC Proof) | L1 (First Hardening) | L2 (Reliability / Governance) | L3 (Maintenance) | L4 (Scale / Packaging) |
| ----------------------- | -------------- | -------------------- | ----------------------------- | ---------------- | ----------------------- |
| Runtime boundary | Adapter-mediated manifest and route proof | Resumable setup and gated profile changes | Checkpoint and research artifacts remain adapter-mediated | Maintenance remains evidence-backed and approval-gated | Supported runtime matrix validates consistently |
| Generated state | Manifest, setup decisions, gaps, routes folder | Profile-aware dependency auto-adds | Sessions, checkpoints, research runs, gap updates | Maintenance reports and signal coverage | Consumer examples and docs regenerated |
| Human gates | Lifecycle route gap handling | One-question setup and confirmation cards | Candidate promotion routes and redaction checks | Approval before route/capability/artifact changes | Release gate before registry or consumer claims |
| Validation | `bash -n`, `jq empty`, markdown links | Profile temp installs and adapter inspection | Checkpoint, research, privacy, and gap-ledger checks | Route and maintenance behavior checks | Full temp install and no-copied-store checks |

## Layer Definitions

| Layer | Objective | Builds On | Included Scope | Explicitly Deferred | Exit Evidence | Value/Cost Notes |
| ----- | --------- | --------- | -------------- | ------------------- | ------------- | ---------------- |
| L0 (POC) | Prove the first-pass adapter-mediated harness shell. | none | Spell UX contract, minimal profile-aware bootstrap output, single GitHub Copilot adapter route behavior, initial gap ledger. | Interactive setup wizard, checkpointing, research mode, maintenance, multi-runtime hardening. | Valid shell syntax, valid JSON, markdown links, inspected adapter text. | Smallest useful proof because it validates state shape and routing without building every mode. |
| L1 | Make setup repeatable and understandable. | L0 | Setup profile options, dependency auto-adds, setup decisions, gated profile/capability mutation, multiple profile scenarios. | Checkpoint distillation, bounded research, maintenance synthesis, release matrix. | Temp installs for core profiles, adapter setup copy inspection, setup decisions updated after confirmed choices. | Setup comes before deeper session behavior because all later modes depend on trustworthy manifest state. |
| L2 | Make memory, checkpoints, and research auditable. | L1 | Checkpoint artifacts, memory classes, candidate routing, research sigil mode, source trails, gap ledger updates, privacy redaction. | Route preset UX, maintenance reports, consumer regeneration. | Checkpoint review does not promote candidates, research is bounded, gap ledger parses, secret samples are redacted. | The verification cost is justified once setup is stable, because evidence quality becomes the next main risk. |
| L3 | Add recurring routes and maintenance feedback. | L2 | Common routes, route misses, stale review, all-selected signal coverage, maintenance reports, local-first recommendations. | Multi-runtime release packaging and public docs sync. | Route presets respect explicit command precedence, maintenance uses evidence and gap patterns, reusable creation requires approval. | Maintenance has higher value after route and research evidence exists to observe. |
| L4 | Harden and package for release. | L3 | Runtime matrix, docs and consumer regeneration, no copied canonical folders, final status checks. | Future extraction of session-memory or checkpoint sigils until reuse pressure appears. | All temp installs pass, generated manifests validate, docs links pass, no copied canonical store exists. | Scale work now has value only after behavior has survived local governance and maintenance checks. |

## Layer 0 - Minimum Working Unit POC

### Goal

Prove that Necronomicon can act as a project harness shell through generated local state and adapter instructions, without requiring a full local CLI runtime.

### Included Scope

- Update the authoritative `necronomicon` UX contract to describe setup profiles, dependency rules, route behavior, and output fields.
- Generate a profile-aware `capabilities.json`, `setup-decisions.md`, `gaps.json`, and route folder for one GitHub Copilot runtime scenario.
- Preserve lifecycle authoring routing to `invoke` when installed and capability-gap guidance when missing.

### Explicitly Deferred Beyond L0

- Full setup wizard interaction across all supported runtimes.
- Checkpoint and memory artifact generation.
- Bounded research mode and web-unavailable behavior.
- Maintenance reports and cross-sigil synthesis.
- Consumer regeneration and release hardening.

### Exit Evidence

- `bash -n arcanum/tools/bootstrap_arcanum.sh` passes.
- Generated JSON validates with `jq empty`.
- Markdown link checks pass for changed documents.
- Generated GitHub Copilot adapter text shows setup, route, invoke gap behavior, and no copied canonical definition store under `.arcanum/necronomicon/`.

### Promotion Decision

- Continue when: the generated state is valid, inspectable, and sufficient for adapter-mediated routing.
- Pivot when: adapter instructions cannot preserve state consistency without a small helper command.
- Stop when: the harness requires a full CLI before any useful setup or route proof exists.

## Layer-by-Layer Improvement Model

### Layer 1 Improvements Over L0

- Added scope: profile choices, dependency auto-adds, setup decisions, and confirmation cards across core setup scenarios.
- Hardening delta: setup changes become explicit, resumable, and auditable.
- Verification delta: temp installs cover `basic-inventory`, `ontology-harness`, and `custom` profile dependency cases.
- Prior guarantees preserved: adapter-mediated runtime remains first-pass, no silent capability mutation occurs, and generated state remains local harness state.

### Layer 2 Improvements Over L1

- Added scope: checkpoints, memory classes, candidate routing, bounded research, source trails, and gap-ledger updates.
- Hardening delta: facts, inference, decisions, candidates, contradictions, and secrets are separated before durable persistence.
- Verification delta: checkpoint and research scenarios validate promotion gates, privacy redaction, and local-source-only fallback.
- Prior guarantees preserved: setup choices remain traceable, candidate promotions remain gated, and Necronomicon state does not become canonical definition storage.

### Layer 3 Improvements Over L2

- Added scope: common route presets, route miss tracking, stale review, selected-signal coverage, and maintenance reports.
- Hardening delta: repeated behavior becomes configurable and maintainable from evidence.
- Verification delta: route preset tests, stale preset checks, signal coverage checks, and maintenance recommendation review.
- Prior guarantees preserved: explicit command names keep precedence, route changes require approval, and reusable artifact creation is not automatic.

### Layer 4 Improvements Over L3

- Added scope: multi-runtime hardening, docs sync, consumer regeneration, and release gate checks.
- Hardening delta: the local harness UX becomes safe to publish and regenerate for consumers.
- Verification delta: supported runtime matrix, generated manifest validation, markdown links, no-copied-store checks, and final dirty-state review.
- Prior guarantees preserved: all earlier setup, privacy, routing, candidate, and maintenance gates remain true.

## Implementation Wave Backbone

| Wave | Target Layer | Goal | Key Artifacts | Verification |
| ---- | ------------ | ---- | ------------- | ------------ |
| W0 | L0 | Establish baseline and avoid unrelated changes. | Status notes, inspected source files. | Root and nested status checks, `bash -n`. |
| W1-W2 | L0-L1 | Update spell contract and generate profile-aware state. | Spell docs, bootstrap changes, manifest, setup decisions, gap ledger. | JSON validation, temp installs, markdown links. |
| W3 | L1 | Add interactive setup wizard behavior. | Adapter setup instructions, option cards, setup update paths. | Adapter inspection and setup resume checks. |
| W4-W5 | L2 | Add checkpoints, memory, and bounded research. | Checkpoints, research briefs, gap ledger updates, redaction policy. | Promotion gate checks, source trail checks, privacy checks. |
| W6-W7 | L3 | Add common routes and maintenance loop. | Route presets, maintenance reports, signal records. | Route precedence checks, stale route checks, maintenance evidence review. |
| W8-W9 | L4 | Regenerate consumers and harden release. | Docs, consumer runtime files, release validation notes. | Runtime matrix, links, manifests, no-copied-store checks, final status. |

## Non-Regression Guardrails

- Generated harness state must never persist credentials, tokens, passwords, private keys, or raw secret values.
- `.arcanum/necronomicon/` remains project-local harness state, not a copied canonical definition store.
- Explicit command names keep precedence over route presets.
- Inventory and ontology candidates remain candidates until the appropriate inventory or ontology-vault flow approves promotion.
- Human-gated setup, checkpoint, research clarification, and maintenance decisions continue to use one-question-at-a-time structured interviews.
- Maintenance recommendations remain evidence-backed and local-first unless reusable promotion is explicitly approved.

## Open Decisions

- Whether repeated adapter inconsistency justifies a small shell helper before a full CLI exists.
- Which consumer example should become the primary regeneration proof after the runtime contract stabilizes.
- When reuse pressure is sufficient to extract session-memory, session-checkpoint, or Necronomicon maintenance behavior into reusable sigils.

## Recommended Next Layer

Start with L0. The smallest useful proof is the adapter-mediated manifest and route baseline, because it validates the core product bet before spending coordination cost on setup wizard depth, checkpoints, research, maintenance, or multi-runtime release work.

Major deferred scope: bounded research, maintenance synthesis, multi-runtime hardening, and reusable sigil extraction remain outside the POC until generated state and basic routing are proven.