# Invoke Result

- Mode: full
- Spell: invoke
- Canonical ID: invoke
- Scope: library
- Phase status: pass
- Mode contract: .agents/skills/invoke/SKILL.md
- Outputs: INVOKE-DEFINE.md, INVOKE-DESIGN.md, IMPLEMENTATION-LAYERING.md, WORK-PACK.md, PLAN-TRANSPORT.md
- Template selection: development package with full specs, implementation layering, work-pack, and transport
- Dispatch techniques: `sequence`, `owner_boundary_check`, `artifact_contract_bridge`, `validation_loop`, `scu_swu_reduction`, `execution_receipt_handoff`
- Distill validation: pass; selected one SWU for early-mode Dispatch/Distill hardening
- Decisions: keep define Distill conditional and design Distill required at design-unit depth; preserve plan/task-session execution boundary
- Unresolved gaps: none blocking
- Next route: task-session
