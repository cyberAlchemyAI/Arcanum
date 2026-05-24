# Invoke Plan Transport: Distill Sigil Development

## Observer Envelope

- run_id: arcanum-invoke-plan-refresh-distill-nested-layering-20260519
- capability.id: invoke
- capability.kind: spell
- capability.tier: spell
- capability.mode: plan
- target_artifact: arcana/distill/development/IMPLEMENTATION-PLAN.md
- request summary: refresh the full Distill sigil-development plan using nested implementation layering inside each lifecycle layer.
- expected outputs: refreshed implementation plan, refreshed work-pack, refreshed task/SWU handoff, traceability updates, and plan transport report.

## Planning Context Summary

The design packet is ready for sigil-development, but the candidate package and validation path do not yet exist. This plan starts with the smallest coherent development unit: a manual candidate package (`README.md` and `SKILL.md`) that can run Standard mode before examples, runtime adapters, or registry machinery are added.

The nested layering refresh keeps that top-level decision intact while adding micro-layer boundaries inside L0 through L4. The micro-layers clarify which SWUs prove README surface, SKILL execution, complexity balance, validation examples, runtime policy, registry approval, and reflection maintenance.

## Template Selection Evidence

- Selected template family: invoke.implementation-plan
- Companion templates: implementation-layering and work-pack
- Complexity: medium
- Output mode: split
- Eligibility: scope has more than five tasks, multiple artifacts, runtime and registry gates, and validation examples.
- Tie cases: low-complexity single-file plan rejected because runtime, examples, registry, and reflection exceed the low-complexity threshold.
- Refresh evidence: nested layering did not change complexity class; it improved execution granularity inside the existing medium-complexity split plan.

## Distill Application

- Seed point: Distill development packet.
- Target context: Arcanum sigil-development lifecycle.
- Objective-output pair: develop reusable Arcana sigil; output is a plan bundle.
- Smallest coherent unit: manual executable candidate package.
- Optimization point: L0 package before L1 examples, L2 runtime, L3 registry, and L4 maintenance.
- Recomposition proof: package -> examples -> runtime -> registry -> reflection reconstructs the full reusable sigil lifecycle.
- Nested layering proof: L0-L4 stay as the parent lifecycle layers, while L0.1-L4.3 micro-layers stop at SWUs instead of creating another open-ended planning recursion.
- Navigable result: start with [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md), then [IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md), then [WORK-PACK.md](WORK-PACK.md).

## Outputs

- Implementation layering: [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md)
- Implementation plan: [IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md)
- Work-pack: [WORK-PACK.md](WORK-PACK.md)
- Work-pack context: [work-pack/shared/context.md](work-pack/shared/context.md)
- Work-pack traceability: [work-pack/shared/traceability.md](work-pack/shared/traceability.md)
- Wave files: [work-pack/waves/](work-pack/waves/)
- Task files: [work-pack/tasks/](work-pack/tasks/)
- Plan transport: [PLAN-TRANSPORT.md](PLAN-TRANSPORT.md)

## Decisions

- Use medium-complexity split planning.
- Use L0 manual candidate package as the first implementation layer.
- Use nested micro-layering for L0, L1, and L2 by default; use it for L3 and L4 where approval or maintenance decisions need explicit evidence.
- Map every SWU to a micro-layer.
- Keep task files as the execution-detail authority; the implementation plan keeps lifecycle structure and shared SWU identity.
- Defer runtime adapter until validation examples pass.
- Defer registry promotion until runtime and validation evidence exist.
- Resolve runtime role policy as subagent-first: use true subagents when the runtime supports them; otherwise use labeled role simulation with the same trace contract.
- Treat registry promotion approval as the final lifecycle gate, not as a blocker to preparing candidate metadata.

## Unresolved Gaps

- Target-artifact gap: README.md and SKILL.md are not authored yet.
- Target-artifact gap: examples and VALIDATION.md do not exist yet.
- Target-artifact gap: runtime adapter implementation remains deferred to L2, but the role policy is decided.
- Target-artifact gap: registry approval remains deferred to the final lifecycle gate.
- Target-artifact gap: nested layering is planning-only until W0/W1 execution proves the README/SKILL package.
- Invoke gap: none observed.

## Recommended Next Route

sigil-development

Start with W0 and W1. Author README.md and SKILL.md before examples, runtime, registry, or reflection work.

Within W1, execute SWUs in handoff order: README surface and navigation, then SKILL execution, balance, and navigation. Use the micro-layer map to confirm conceptual coverage without forcing SWU IDs to mirror micro-layer IDs.

## Invoke Result

- Mode: plan
- Spell: invoke
- Canonical ID: invoke
- Scope: library
- Phase status: pass
- Mode contract: spells/invoke/plan.md
- Outputs: IMPLEMENTATION-PLAN.md, IMPLEMENTATION-LAYERING.md, WORK-PACK.md, PLAN-TRANSPORT.md
- Design views: not applicable for plan mode
- Glossary consistency: pass
- Implementation layering: IMPLEMENTATION-LAYERING.md with L0-L4 coverage and L0.1-L4.3 nested micro-layer coverage
- Work-pack: WORK-PACK.md split
- Complexity: medium
- Per-layer planning: L0, L1, L2, L3, L4 plus nested micro-layer mapping
- Implementation detail: task specs complete
- Smallest working units: complete, with micro-layer mapping
- Template/profile selection: invoke.implementation-plan plus implementation-layering and work-pack companions
- Validation strategy: examples, validation report, runtime check, observability review, registry approval
- Decisions: L0 candidate package first; nested layers stop at SWUs; runtime and registry deferred
- Unresolved gaps: target artifact gaps only
- Next route: sigil-development
