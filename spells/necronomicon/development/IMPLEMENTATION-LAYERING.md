---
title: Necronomicon Implementation Layering
status: draft
updatedAt: 2026-05-23
owner: Arcanum maintainers
scope: workflow
---

# Necronomicon Implementation Layering

## Context

- Target: Necronomicon knowledge substrate harness.
- Current state: concept/design pack re-authored to start from inventory and ontology handling.
- Primary user/operator: a repository user or assistant using Arcanum through local runtime adapters.
- Primary constraint: preserve knowledge authority. Necronomicon may retrieve, classify, remember, and route; it must not promote inventory or ontology truth by itself.

## Layering Method

- Substrate-first: Layer 0 proves inventory retrieval, evidence capture, authority classification, gap recording, and handoff.
- Configuration-second: setup profiles and bootstrap state configure the substrate after its value is proven.
- Statefulness-third: active interaction, side notes, checkpoints, and research deepen continuity after the substrate loop works.
- Evidence-gated promotion: each layer creates validation evidence before the next layer expands behavior.

## Layer Boundary Heuristic

```text
Layer value = decision unlocked + user-visible outcome + risk reduced
Layer cost = implementation time + verification time + coordination burden
```

Stop a layer when the next unit of work adds less value to the current decision than starting the next decision layer.

## Layer Decision Table

| Layer | Decision Question | Minimum Working Unit | User/Operator Outcome | Risk Reduced | Promotion Decision |
| --- | --- | --- | --- | --- | --- |
| L0 Substrate Proof | After this layer, do we know whether Necronomicon can answer knowledge questions by retrieving required inventory, classifying authority, recording gaps, and routing candidates without false promotion? | One adapter-mediated substrate loop over a local question: required inventory check, inventory lookup, session evidence, authority classification, `gaps.json`, and handoff packet. | User gets an answer that distinguishes known facts, candidates, contradictions, and next owner. | Prevents command-router drift and false authority. | Continue when the loop works with valid state, explicit no-promotion labels, and a clear blocked state when inventory is absent. |
| L1 Setup And Manifest | After this layer, do we know whether repository setup can configure the substrate repeatably across inventory/ontology profiles? | Profile-aware bootstrap manifest, setup decisions, inventory root policy, ontology profile state, privacy policy, and dependency auto-adds. | User can inspect what substrate is enabled and why. | Reduces setup ambiguity and hidden dependency drift. | Continue when temp installs produce valid manifests and setup decisions. |
| L2 Session Workbench | After this layer, do we know whether active work can continue across turns without corrupting authority? | Active interaction, side notes, checkpoints, route ledger, candidate queues, and resume summary. | User can resume ongoing discovery, governance, or planning work. | Reduces chat-residue loss and accidental truth promotion. | Continue when checkpoint/resume preserves facts vs candidates vs gaps. |
| L3 Research And Lifecycle Handoff | After this layer, do we know whether bounded research and lifecycle authoring can use the substrate without becoming unbounded search or invoke-by-default? | Harness research packets, source trails, contradiction handling, inventory/ontology candidate output, and invoke handoff only when authoring begins. | User can gather evidence before defining, designing, or planning. | Reduces unbounded research and premature lifecycle authoring. | Continue when research outputs are source-backed and handoffs are owner-correct. |
| L4 Routes, Maintenance, Release | After this layer, do we know whether repeated route/gap patterns can improve the harness safely across runtimes? | Route presets, route miss tracking, maintenance reports, observability signal coverage, docs, and runtime matrix validation. | User gets a maintainable project harness that improves from evidence. | Reduces stale routes, missing telemetry, and reusable-artifact bloat. | Release when matrix validation passes and no copied canonical store appears. |

## Capability Progression

| Capability Area | L0 | L1 | L2 | L3 | L4 |
| --- | --- | --- | --- | --- | --- |
| Inventory | lookup and missing-inventory gap | root and profile policy | checkpoint candidates | research synthesis filing | maintenance coverage |
| Ontology | candidate routing | ontology profile selection | premise and bridge candidate queues | research-to-governance handoff | governance route maintenance |
| Session state | evidence draft only | configured state paths | active interaction and checkpoints | research packets | release-ready persistence |
| Routing | handoff recommendation | configured selected capabilities | route history | invoke/task handoffs | route presets and maintenance |
| Validation | JSON parse and scenario review | temp installs | checkpoint/resume fixtures | research/handoff fixtures | runtime matrix |

## Layer Definitions

### L0: Substrate Proof

Included:

- required inventory availability check,
- inventory-first query behavior,
- source-backed fact vs candidate classification,
- session evidence record,
- gap ledger entry,
- handoff packet to inventory, ontology, decision, invoke, or task owner.

Deferred:

- full setup wizard,
- active interaction state,
- route presets,
- bounded web research,
- maintenance loop,
- multi-runtime release.

Exit evidence:

- `gaps.json` parses with `jq empty`,
- a sample knowledge question produces a source-backed/candidate/gap classification from inventory-backed context,
- missing inventory produces setup/install guidance rather than degraded Necronomicon output,
- no candidate is promoted by Necronomicon,
- handoff packet names the owning capability.

### L1: Setup And Manifest

Included:

- profile-aware `capabilities.json`,
- `setup-decisions.md`,
- inventory root policy,
- ontology profile and dependency rules,
- privacy policy,
- bootstrap temp install validation.

Deferred:

- interactive setup wizard depth,
- checkpoint artifacts,
- research packets,
- maintenance reports.

Exit evidence:

- temp installs for basic inventory, ontology profile, and custom profile,
- valid JSON manifests,
- setup decisions explain auto-added dependencies and exclusions.

### L2: Session Workbench

Included:

- `active-interaction.json`,
- `side-notes.jsonl`,
- checkpoint artifact,
- candidate queues,
- route ledger,
- resume summary.

Deferred:

- web research,
- route preset management,
- cross-sigil maintenance.

Exit evidence:

- resume scenario preserves active owner,
- checkpoint separates facts, inference, decisions, candidates, and gaps,
- side notes do not derail active flow unless explicitly switched.

### L3: Research And Lifecycle Handoff

Included:

- bounded local-first research packet,
- source trail,
- contradiction handling,
- inventory/ontology post-research options,
- invoke handoff when authoring is ready.

Deferred:

- public release matrix,
- long-term maintenance automation.

Exit evidence:

- research cannot proceed without question/scope/stop condition,
- web-unavailable behavior is explicit,
- invoke receives context only after substrate status and gaps are named.

### L4: Routes, Maintenance, Release

Included:

- route presets,
- route miss tracking,
- maintenance report,
- observability signal aggregation,
- runtime matrix,
- docs and generated adapter regeneration.

Exit evidence:

- route presets respect explicit command precedence,
- maintenance proposes evidence-backed changes only,
- supported runtime installs validate,
- no canonical definition folders are copied under `.arcanum/necronomicon/`.

## Non-Regression Guardrails

- Session evidence remains low authority.
- Inventory and ontology promotion stay downstream.
- Missing inventory is recorded as a gap, not hidden.
- Explicit command names keep precedence over route presets.
- Secrets are never persisted in harness state.
- Generated `.arcanum/necronomicon/` remains harness state, not a copied registry or definition store.

## Recommended Next Layer

Start with L0 Substrate Proof. The first implementation task should prove one knowledge question can flow through required inventory lookup, authority classification, gap recording, and a handoff recommendation. It must also prove that missing inventory blocks active Necronomicon operation and routes to inventory setup.

## Major Deferred Scope

Bootstrap manifest expansion, active workbench state, research mode, route presets, maintenance synthesis, and release hardening are deferred until the substrate loop proves Necronomicon's distinct value.

## Change History

| Date | Change |
| --- | --- |
| 2026-05-23 | Rebuilt layering around inventory and ontology substrate first. |
