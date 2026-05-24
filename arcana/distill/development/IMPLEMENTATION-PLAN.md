---
template_id: invoke.implementation-plan
template_type: implementation-plan
module: distill
status: draft
updatedAt: 2026-05-20
---

# Implementation Plan: Distill Sigil Development

## Implementation Objective

Develop Distill from approved design packet into a reusable Arcana sigil with a self-contained package, validation examples, runtime adapter, observability, registry candidacy, and reflection path.

The plan uses Distill's own optimization rule: begin with the smallest coherent candidate package that can be manually executed, then layer validation, runtime, registry, and maintenance only when evidence justifies promotion.

This refresh also applies nested implementation layering inside each top-level layer. Nested layers are used only where they clarify sequencing, validation, or handoff boundaries; they stop when the next unit is directly executable as a Smallest Working Unit.

## Source Design References

| Ref ID | Source | Required | Notes |
| --- | --- | --- | --- |
| SD-001 | [SIGIL-HANDOFF.md](SIGIL-HANDOFF.md) | yes | Defines identity, modes, output contract, operating model, and runtime expectations. |
| SD-002 | [MODE-TECHNIQUE-SURFACE-DESIGN.md](MODE-TECHNIQUE-SURFACE-DESIGN.md) | yes | Defines invocation, mode, technique, core, trace, and handoff surfaces. |
| SD-003 | [techniques/README.md](techniques/README.md) | yes | Indexes all TechniqueSpecs. |
| SD-004 | [GLOSSARY.md](GLOSSARY.md) | yes | Local term contract. |
| SD-005 | [DESIGN-CONTINUATION-REVIEW.md](DESIGN-CONTINUATION-REVIEW.md) | yes | Adds objective-output setup and navigable-result closeout. |
| SD-006 | [../../../arcana/sigil-development/SKILL.md](../../../arcana/sigil-development/SKILL.md) | yes | Lifecycle owner contract. |
| SD-007 | [../../../framework/CYBERALCHEMY-METHOD.md](../../../framework/CYBERALCHEMY-METHOD.md) | yes | Method principles: objective-output, discovery, tension, ergonomics, lifecycle ownership. |

## Delivery Boundary

- Included:
  - Candidate `README.md` and `SKILL.md`.
  - Validation examples and validation report.
  - Runtime adapter plan and optional command adapter.
  - Observability and reflection policy.
  - Registry candidate handoff.
- Excluded:
  - Immediate registry promotion before examples pass.
  - Global glossary promotion.
  - Runtime adapter behavior that requires true subagents without role simulation fallback.
  - Any application/source-code implementation outside this sigil package.
- Deferral rules:
  - Defer runtime adapter until manual candidate examples pass.
  - Defer registry candidate work until runtime and validation evidence exists.
  - Defer registry promotion until the final lifecycle approval gate.
  - Runtime role policy is subagent-first: use true subagents when the runtime supports them; otherwise use labeled role simulation with the same trace contract.

## Delivery Slices

| Slice ID | Outcome | Dependencies | Validation |
| --- | --- | --- | --- |
| S-CLO-001 | Candidate package exists and is manually executable. | SD-001 through SD-005 | README/SKILL review against sigil-development quality bar. |
| S-CLO-002 | Behavior examples prove pass, flag, and block outcomes. | S-CLO-001 | Validation examples include real output bodies and expected verdicts. |
| S-CLO-003 | Runtime and observability are ready for representative invocation. | S-CLO-002 | Command resolves, signal schema exists, representative closeout is recorded. |
| S-CLO-004 | Registry candidate is ready for final approval. | S-CLO-003 | Link validation, registry diff review, and approval-ready promotion recommendation. |
| S-CLO-005 | Reflection and maintenance loop is defined. | S-CLO-003 | Reflection thresholds and iteration policy are documented. |

## Dependency Plan

| Dependency | Needed By | Readiness | Risk |
| --- | --- | --- | --- |
| Approved design packet | all slices | ready | Low; design continuation review passes. |
| Sigil-development contract | S-CLO-001, S-CLO-005 | ready | Low; existing lifecycle owner. |
| Runtime adapter decision | S-CLO-003 | ready | Low; policy is subagent-first with role simulation fallback when runtime subagents are unavailable. |
| Validation examples | S-CLO-003, S-CLO-004 | missing | Medium; promotion must wait for real outputs. |
| Registry approval | S-CLO-004, S-CLO-005 | final gate | Low; explicit user/lifecycle approval is the last step after readiness evidence exists. |

## Layer Window

- Layering companion: [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md)
- Selected start layer: L0 Candidate Package
- Selected stop layer: L4 Reflection And Maintenance
- Layer deferrals: runtime, registry, and reflection are deferred until earlier evidence passes.
- Nested layering: enabled for L0, L1, and L2 by default; scoped for L3 and L4 where approval, governance, or maintenance decisions would otherwise be hidden.
- Maximum default nesting depth: top-level layer plus one micro-layer.
- Nested stop condition: stop when the remaining work is directly executable as a listed SWU.

## Nested Layer Coverage

| Layer | Micro-Layers Covered | Planning Treatment |
| --- | --- | --- |
| L0 Candidate Package | L0.1 README Surface, L0.2 SKILL Execution Contract, L0.3 Balance And Complexity Contract, L0.4 Navigation Closeout | Task/SWU mapping must prove README and SKILL are independently navigable and mutually consistent. |
| L1 Behavior Validation | L1.1 Golden Runs, L1.2 Technique Trigger Runs, L1.3 Drift And Failure Runs, L1.4 Validation Report | Examples are grouped by behavior evidence instead of one undifferentiated examples bundle. |
| L2 Runtime And Observability | L2.1 Command Surface, L2.2 Role Execution Policy, L2.3 Signal Schema, L2.4 Runtime Validation | Runtime access, role policy, telemetry, and representative run evidence are gated independently. |
| L3 Registry Candidate | L3.1 Candidate Metadata, L3.2 Routing And Link Check, L3.3 Promotion Recommendation | Registry candidate work waits for evidence, then proceeds through metadata, navigation, and an approval-ready recommendation. Final approval is handled as the last lifecycle gate. |
| L4 Reflection And Maintenance | L4.1 Reflection Signals, L4.2 Maintenance Change Classes, L4.3 Evolution Loop | Maintenance is planned as an evidence loop, not a final prose afterthought. |

## Task Decomposition

| Task ID | Slice ID | Micro-Layers | Task | Done When |
| --- | --- | --- | --- | --- |
| TASK-CLO-001 | S-CLO-001 | L0.1, L0.4 | Author user-facing README. | README explains problem, use conditions, modes, inputs, outputs, lifecycle, examples pointer, non-use conditions, and start-here navigation. |
| TASK-CLO-002 | S-CLO-001 | L0.2, L0.3, L0.4 | Author executable SKILL contract. | SKILL includes objective, logic type, applicability, inputs, process, technique pack, quality bar, anti-patterns, output contract, observability, origin, complexity balance, and navigable closeout. |
| TASK-CLO-003 | S-CLO-002 | L1.1, L1.2, L1.3 | Build validation examples and runbook. | Passing, technique-trigger, and negative example prompts/outputs exist with expected pass/flag/block verdicts. |
| TASK-CLO-004 | S-CLO-002 | L1.4 | Run manual validation and record findings. | Validation report cites examples, gaps, micro-layer coverage, and promotion decision. |
| TASK-CLO-005 | S-CLO-003 | L2.3, L4.1 | Define observability and reflection artifacts. | Usage telemetry schema, meaningful execution definition, thresholds, and reflection path are documented. |
| TASK-CLO-006 | S-CLO-003 | L2.1, L2.2, L2.4 | Add runtime command adapter after manual behavior passes. | Adapter resolves through local command surface, uses subagent-first role policy with role simulation fallback, and preserves output/observability contracts. |
| TASK-CLO-007 | S-CLO-004 | L3.1, L3.2, L3.3 | Prepare registry candidate and docs links. | Registry/docs candidate metadata and link validation are prepared without final promotion approval. |
| TASK-CLO-008 | S-CLO-005 | L4.1, L4.2, L4.3 | Final readiness, release, and maintenance review. | End-to-end review confirms package, examples, runtime, observability, registry recommendation, reflection loop, maintenance classes, and final approval state. |

## Execution Detail Authority

Execution detail lives in the task files under [work-pack/tasks/](work-pack/tasks/). This implementation plan keeps lifecycle structure, dependency logic, shared SWU identity, and promotion gates. It should not duplicate the full execution instructions owned by each task file.

| Task ID | Execution Detail File | Micro-Layers | Detail Status |
| --- | --- | --- | --- |
| TASK-CLO-001 | [TASK-CLO-001.md](work-pack/tasks/TASK-CLO-001.md) | L0.1, L0.4 | task-local detail complete |
| TASK-CLO-002 | [TASK-CLO-002.md](work-pack/tasks/TASK-CLO-002.md) | L0.2, L0.3, L0.4 | task-local detail complete |
| TASK-CLO-003 | [TASK-CLO-003.md](work-pack/tasks/TASK-CLO-003.md) | L1.1, L1.2, L1.3 | task-local detail complete |
| TASK-CLO-004 | [TASK-CLO-004.md](work-pack/tasks/TASK-CLO-004.md) | L1.4 | task-local detail complete |
| TASK-CLO-005 | [TASK-CLO-005.md](work-pack/tasks/TASK-CLO-005.md) | L2.3, L4.1 | task-local detail complete |
| TASK-CLO-006 | [TASK-CLO-006.md](work-pack/tasks/TASK-CLO-006.md) | L2.1, L2.2, L2.4 | task-local detail complete |
| TASK-CLO-007 | [TASK-CLO-007.md](work-pack/tasks/TASK-CLO-007.md) | L3.1, L3.2, L3.3 | task-local detail complete |
| TASK-CLO-008 | [TASK-CLO-008.md](work-pack/tasks/TASK-CLO-008.md) | L4.1, L4.2, L4.3 | task-local detail complete |

## Smallest Working Units

Shared manifest:

SWU IDs are ordered by execution handoff sequence. Micro-layer IDs remain the conceptual coverage map and may be non-contiguous when a task intentionally proves a later micro-layer before another task begins.

| SWU ID | Parent Task | Micro-Layer | Goal | Write Scope | Acceptance Evidence | Verification Command |
| --- | --- | --- | --- | --- | --- | --- |
| SWU-CLO-001 | TASK-CLO-001 | L0.1 | Draft README usage surface. | `arcana/distill/README.md` | README has purpose, use/do-not-use, mode summary, objective-output artifact, and next route. | `rg -n "Use When|Do Not Use|Modes|Output Artifact|Next" arcana/distill/README.md` |
| SWU-CLO-002 | TASK-CLO-001 | L0.4 | Add README navigation and links. | `arcana/distill/README.md` | Links point to development packet, examples, validation, and start-here path. | `rg -n "Start Here|development|examples|SIGIL-HANDOFF|VALIDATION" arcana/distill/README.md` |
| SWU-CLO-003 | TASK-CLO-002 | L0.2 | Draft SKILL core process. | `arcana/distill/SKILL.md` | Process includes setup, discovery, Proposer/Balancer, techniques, verdict, handoff. | `rg -n "objective-output|Proposer|Balancer|Technique|output-contract" arcana/distill/SKILL.md` |
| SWU-CLO-004 | TASK-CLO-002 | L0.3 | Add Quality Bar, Anti-Patterns, complexity balance, and output contract. | `arcana/distill/SKILL.md` | Reviewable success/failure criteria and complexity exception rule exist. | `rg -n "<quality-bar>|<anti-patterns>|complexity|evolution profile|<output-contract>" arcana/distill/SKILL.md` |
| SWU-CLO-005 | TASK-CLO-002 | L0.4 | Add navigable result closeout to SKILL. | `arcana/distill/SKILL.md` | Closeout requires start-here, artifact use, decisions, unresolved tensions, and next action. | `rg -n "Navigable|start-here|next action|unresolved" arcana/distill/SKILL.md` |
| SWU-CLO-006 | TASK-CLO-003 | L1.1 | Create golden passing examples. | `arcana/distill/development/examples/` | Standard and Compact or Tournament examples include real expected outputs. | review example files |
| SWU-CLO-007 | TASK-CLO-003 | L1.2 | Create technique trigger examples. | `arcana/distill/development/examples/` | Technique examples show activation reason, contribution, and deferral/deactivation when relevant. | review example files |
| SWU-CLO-008 | TASK-CLO-003 | L1.3 | Create negative and drift examples. | `arcana/distill/development/examples/` | Infinite reduction, objective-output drift, premature complexity, missing evolution profile, and navigation downgrade examples exist. | review example files |
| SWU-CLO-009 | TASK-CLO-004 | L1.4 | Write validation report. | `arcana/distill/development/VALIDATION.md` | Report records examples, micro-layer coverage, verdicts, gaps, and L2 promotion decision. | review report |
| SWU-CLO-010 | TASK-CLO-005 | L2.3 | Define usage telemetry. | `arcana/distill/templates/usage-telemetry.md` | Meaningful execution and signal fields are named. | review template |
| SWU-CLO-011 | TASK-CLO-005 | L4.1 | Define reflection thresholds. | `arcana/distill/README.md`, `templates/` | Manual, threshold, drift, navigation, and gap triggers are documented. | review docs |
| SWU-CLO-012 | TASK-CLO-006 | L2.1 | Add runtime adapter. | `.codex/commands/` or runtime adapter path | Adapter points to canonical SKILL and preserves closeout. | `tools/arcanum --resolve /distill` |
| SWU-CLO-013 | TASK-CLO-006 | L2.2 | Define runtime role execution policy. | runtime adapter docs or `arcana/distill/README.md` | Runtime states subagent-first execution when supported, role simulation fallback when unavailable, and tournament limits. | review policy section |
| SWU-CLO-014 | TASK-CLO-006 | L2.4 | Validate runtime representative run. | `development/` and observability ledgers | Closeout includes observation fields, role policy, and output contract. | representative run review |
| SWU-CLO-015 | TASK-CLO-007 | L3.1 | Prepare registry/docs candidate metadata. | `registry/`, `README.md`, `framework/README.md` if applicable | Candidate entry and package links exist without silently promoting the sigil. | link validation/review |
| SWU-CLO-016 | TASK-CLO-007 | L3.2 | Run routing and link check. | registry/docs links | README, SKILL, examples, validation, and adapter links are reachable. | link validation/review |
| SWU-CLO-017 | TASK-CLO-007 | L3.3 | Record promotion recommendation. | `development/REGISTRY-PROMOTION.md` or equivalent | Recommendation names promote, hold, or revise with evidence and final approval marked pending unless already granted. | review promotion record |
| SWU-CLO-018 | TASK-CLO-008 | L4.2 | Define maintenance handoff. | `README.md`, `SKILL.md`, `templates/` | Maintenance change classes, reflection route, and lifecycle owner are explicit. | review maintenance section |
| SWU-CLO-019 | TASK-CLO-008 | L4.3 | Define evolution loop. | `README.md`, `SKILL.md`, `development/READINESS-REVIEW.md` | Observability, reflection report, design update, validation rerun, and release note are linked. | review evolution loop |
| SWU-CLO-020 | TASK-CLO-008 | L4.3 | Final readiness review. | `development/READINESS-REVIEW.md` | Pass/flag/block readiness and B-CLO-002 approval state recorded with end-to-end evidence. | review readiness report |

## Blocker And Gate Ledger

| ID | Status | Scope | Impact | Resolution |
| --- | --- | --- | --- | --- |
| B-CLO-001 | resolved | Runtime role execution policy. | No longer blocks L2 adapter details. | Always use true subagents when the runtime supports them; if the runtime does not support subagents, use labeled Proposer/Balancer role simulation with the same trace contract. |
| B-CLO-002 | final gate | Registry promotion approval. | Blocks only final promotion/release, not candidate metadata or link preparation. | Ask user/lifecycle owner as the last step after readiness evidence exists; record promote, hold, or revise. |

## Validation Strategy

| Check ID | Check | Scope | Tool Or Evidence |
| --- | --- | --- | --- |
| V-CLO-001 | Folder/package review. | README/SKILL/templates/development | Manual review plus `rg` link checks. |
| V-CLO-002 | Mode behavior examples. | Compact, Standard, Tournament, Deep, Validate | Example outputs with expected verdicts. |
| V-CLO-003 | Technique trigger examples. | technique pack | Examples for closure, recomposition, evolution, navigation, tournament. |
| V-CLO-004 | Output contract review. | SKILL and examples | Output follows Distill Result shape. |
| V-CLO-005 | Observability review. | telemetry templates and representative run | Signal fields and reflection triggers present. |
| V-CLO-006 | Registry readiness. | registry/docs links | Link validation, promotion recommendation, and final approval status. |

## Work-Pack Handoff

- Work-pack companion: [WORK-PACK.md](WORK-PACK.md)
- Required manifest entries: all TASK-CLO tasks and SWU-CLO manifest.
- Deferred entries: runtime adapter waits for validation evidence; registry promotion waits for the final approval gate.

## Execution-Pack Handoff

- Execution-pack: split work-pack with task files and wave files under `development/work-pack/`.
- Wave grouping:
  - W0 baseline and package contract.
  - W1 candidate package.
  - W2 validation examples.
  - W3 runtime and observability.
  - W4 registry and reflection.
- Parallelization boundary:
  - README and SKILL can be drafted in parallel only after W0.
  - Runtime must not begin before validation evidence.
  - Registry candidate metadata must not begin before runtime evidence.
  - Registry promotion must not happen before the final approval gate.

## Closure Criteria

| Criterion | Evidence |
| --- | --- |
| Candidate package is self-contained. | README.md and SKILL.md exist and pass quality-bar review. |
| Behavior is validated. | Examples and VALIDATION.md show pass/flag/block cases. |
| Runtime is safe to install. | Adapter preserves SKILL contract and subagent-first role policy with role simulation fallback. |
| Observability supports reflection. | Usage telemetry and reflection thresholds exist. |
| Registry promotion is governed. | Final approval record, promotion recommendation, and link validation exist. |

## Gate Result

- Status: pass
- Reason: Plan covers the complete sigil-development lifecycle with parent layer boundaries, nested micro-layer coverage, task details, SWUs, validation strategy, and gated runtime/registry promotion.
