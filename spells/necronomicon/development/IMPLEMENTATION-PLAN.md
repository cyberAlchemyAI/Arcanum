---
module: necronomicon
version: current
status: draft
updatedAt: 2026-05-23
docType: implementation-plan
---

# Necronomicon Implementation Plan

## Objective

Implement Necronomicon as a substrate-first repository harness. The first implementation must prove inventory retrieval, session evidence capture, authority classification, gap recording, and owner-correct handoff before expanding setup, routing, research, or maintenance.

## Source Design References

- [DEFINE.md](DEFINE.md)
- [DESIGN.md](DESIGN.md)
- [GLOSSARY.md](GLOSSARY.md)
- [GLOSSARY-CONSISTENCY.md](GLOSSARY-CONSISTENCY.md)
- [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md)
- [WAVE-PLAN.md](WAVE-PLAN.md)
- [KNOWLEDGE-SUBSTRATE-FLOW.md](KNOWLEDGE-SUBSTRATE-FLOW.md)

## Delivery Boundary

This plan covers development-pack and first implementation planning. It does not execute code mutation beyond approved task-session work.

## Complexity

Complexity: medium.

Reason: work touches durable state contracts, adapter behavior, bootstrap generation, inventory/ontology boundaries, validation fixtures, and later runtime regeneration.

## Implementation Layers

| Layer | Goal | Promotion Evidence |
| --- | --- | --- |
| L0 Substrate Proof | Prove one knowledge question can produce required inventory lookup, authority classification, gap entry, and handoff. | Valid JSON, scenario fixture review, no-promotion proof, missing-inventory blocked-state proof. |
| L1 Setup And Manifest | Configure inventory and ontology substrate through setup state. | Temp installs and valid manifests. |
| L2 Session Workbench | Preserve active work across turns without corrupting authority. | Resume/checkpoint fixtures. |
| L3 Research And Lifecycle Handoff | Add bounded research and invoke/task handoffs on top of substrate. | Research/handoff fixtures with source trails. |
| L4 Routes, Maintenance, Release | Harden route presets, maintenance, docs, and runtime adapters. | Runtime matrix and release checks. |

## Work Streams

### Stream A: Canonical Contract Sync

Purpose: make substrate-first behavior authoritative.

Tasks:

1. Update `spells/necronomicon/README.md` to match the corrected MVP.
2. Search for stale language that names routing/bootstrap as the first proof.
3. Regenerate or update command snapshots only after the canonical contract is approved.

Validation:

- Markdown links pass.
- Stale-language search is reviewed.

### Stream B: L0 State Contracts

Purpose: define concrete state files for the substrate loop.

Tasks:

1. Define `gaps.json` schema.
2. Define `authority-classification.jsonl` schema.
3. Define `evidence.md` section contract.
4. Define handoff packet fields.
5. Add curated examples under development fixtures or documentation.

Validation:

- JSON examples parse.
- Examples cover inventory hit, missing-inventory blocked state, ontology candidate, and contradiction.

### Stream C: L0 Adapter-Mediated Substrate Proof

Purpose: prove behavior before broad bootstrap work.

Tasks:

1. Add adapter instructions for required inventory lookup.
2. Add blocked-state setup/install guidance when inventory is absent.
3. Add no-promotion closeout language.
4. Validate sample scenarios manually or with lightweight scripts.

Validation:

- Scenario output names facts, candidates, gaps, and owners.
- No output promotes a candidate directly.

### Stream D: L1 Bootstrap Configuration

Purpose: configure the substrate through setup state.

Tasks:

1. Add profile-aware manifest fields.
2. Add inventory root policy.
3. Add ontology profile and dependency auto-adds.
4. Generate `setup-decisions.md`, `gaps.json`, `routes/`, and `maintenance/`.
5. Validate temp installs.

Validation:

- `bash -n tools/bootstrap_arcanum.sh`.
- `jq empty` on manifests and gaps.
- Temp install scenarios pass.

### Stream E: L2-L4 Continuation Work

Purpose: deepen the harness after L0 and L1 pass.

Tasks:

1. Add active interaction and side notes.
2. Add checkpoint and candidate queues.
3. Add bounded research packets.
4. Add route presets and maintenance reports.
5. Regenerate docs and runtime adapters.

Validation:

- Resume/checkpoint fixtures.
- Research/handoff fixtures.
- Runtime matrix.

## Implementation Detail

### Authority Classification Algorithm

Input:

- user turn summary,
- inventory lookup results,
- source refs from repository search only when they are attached as inventory candidates after the required inventory context exists,
- session evidence,
- existing gaps.

Output:

- zero or more `SourceBackedFact` records,
- zero or more candidate records,
- zero or more gap records,
- optional handoff packet.

Ordered rules:

1. If an inventory entry directly answers the question and has source selectors, classify as `source_backed_fact`.
2. If inventory is missing, stop active substrate behavior and route to inventory setup/install guidance with a capability gap.
3. If repository sources support a durable claim but inventory lacks it, classify as `inventory_candidate` plus source references; do not present it as Necronomicon-known until inventorized or explicitly marked as candidate evidence.
4. If a claim affects domain concepts, premises, confidence, constitutions, axioms, or bridge evidence, classify as `ontology_candidate` or `premise_candidate`.
5. If two sources or memories conflict, classify as `contradiction` and write a gap.
6. If no source supports the claim, keep it as `session_evidence` or source gap.
7. If a next owner is known, emit a handoff packet with a no-promotion note.

Failure modes:

- Missing inventory root: block active Necronomicon substrate operation and route to inventory setup/install guidance.
- Ambiguous governance claim: write decision gap or route to `decision-gate`.
- Unsupported lifecycle request: route to `invoke` only with explicit gap context.

## Validation Strategy

| Slice | Validation |
| --- | --- |
| L0 state contracts | JSON parse, scenario review, no-promotion review. |
| L0 adapter proof | Manual sample scenarios and curated output inspection. |
| L1 bootstrap | shell syntax, temp installs, JSON validation. |
| L2 workbench | checkpoint/resume fixtures. |
| L3 research | local-source-only and web-unavailable scenarios. |
| L4 release | runtime matrix, docs links, stale-language search. |

## Blockers And Gaps

| Gap | Severity | Next Route |
| --- | --- | --- |
| Exact inventory command/API surface may differ by runtime. | medium | inspect `inventory` contract during L0. |
| Missing inventory setup path needs a concise user-facing blocked-state message. | medium | define in Stream B and adapter instructions. |
| Canonical README has not yet been updated to substrate-first language. | medium | Stream A. |
| Generated command snapshots will remain stale until regeneration. | low | L4 or after Stream A approval. |

## Next Route

`task-session` for Stream A and Stream B as a bounded first execution slice.

## Change History

| Date | Change |
| --- | --- |
| 2026-05-23 | Created substrate-first implementation plan. |
