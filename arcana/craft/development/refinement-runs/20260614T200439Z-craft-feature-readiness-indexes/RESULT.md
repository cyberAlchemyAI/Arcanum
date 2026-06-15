# Refine Result: Craft Feature Readiness Indexes

## Refined Synthesis

Craft should gain an additive execution-readiness index layer. The current contract is already strong at scoped ledger state, links, pending-by-node status, and source authority. The missing piece is a compact way for Craft to remember when a `next_move` points at an Invoke work-pack and to expose:

- which artifact is the current execution target;
- which SWU or work-pack slice is ready;
- which approval record authorizes the work;
- which execution mode is allowed;
- which product worktree or mutation boundary applies;
- which mutation or publication scopes remain blocked.

This stays inside Craft's role: Craft records ledger state and route memory. It does not execute the SWU, decide product gates, or rewrite Invoke/Refine results.

## Status

- Target: `arcana/craft`
- Status: `flag`
- Reason: the Refine loop now has local native stage receipts, but recommended subagent reviewers were not spawned and canonical Craft source files were not mutated.
- Research: `no-research`
- Runtime-backed Refine loop: executed locally through parent-native Codex stage receipts.

## Stage Evidence

- Context Builder evidence baseline: pass, `stages/S01-CONTEXT-BUILDER.md`
- Invoke Define: pass, `stages/S02-INVOKE-DEFINE.md`
- Interrogation refine-review: pass, `stages/S03-INTERROGATION-REFINE-REVIEW.md`
- Research decision: pass, `stages/S04-RESEARCH-DECISION.md`
- Distill: pass, `stages/S05-DISTILL.md`
- Invoke Redefine / Design: pass, `stages/S06-INVOKE-DESIGN-RECEIPT.md`
- Interrogation refine-design-review: pass, `stages/S07-INTERROGATION-DESIGN-REVIEW.md`
- Distill Repair: pass, `stages/S08-DISTILL-REPAIR.md`
- Invoke Plan: pass, `stages/S09-INVOKE-PLAN-RECEIPT.md`
- Final Interrogation and Synthesis: flag, `stages/S10-FINAL-INTERROGATION-SYNTHESIS.md`

## Execution Residue

- Subagent strategy receipt: `stages/subagent-strategy-receipt.md`
- Machine execution receipt: `stages/execution-receipt.json`
- Residue: recommended reviewers were not spawned because the active subagent tool policy requires an explicit user request for subagents, delegation, or parallel agent work.
- Impact: this run has enough data for `SWU-CFR-001` execution, but it should remain `flag` until subagent receipts exist or the maintainer accepts the local fallback.

## Proposed Contract Shape

Add optional readiness indexes under `indexes.execution_readiness`:

```yaml
indexes:
  execution_readiness:
    current_execution_target:
      context_id: CTX-...
      artifact_id: ART-...
      path: docs/features/example/WORK-PACK.md
      owner_route: task-session
    work_pack_gate_status:
      ART-...: flag
    ready_swu_ids:
      - SWU-EXAMPLE-001
    approval_record:
      ART-...: ART-APPROVAL-...
    execution_mode:
      ART-...: local-static
    product_worktree:
      ART-...: app-or-package-root
    blocked_mutation_scope:
      ART-...:
        - app-runtime
        - publication
    blocked_publication_scope:
      ART-...:
        - commit
        - push
        - pr
```

Ledger rows may also carry optional readiness fields when the information belongs directly to an artifact, gate, or next move. The index stays derived lookup data and must point back to row IDs or artifact paths.

## Design And Plan Outputs

- Design: `INVOKE-DESIGN.md`
- Glossary consistency: `GLOSSARY-CONSISTENCY.md`
- Plan: `INVOKE-PLAN.md`
- Implementation layering: `IMPLEMENTATION-LAYERING.md`
- Work-pack: `WORK-PACK.md`

## Boundary Notes

- Public/private boundary is active because the canonical Craft package lives in the public `arcanum` submodule.
- Private or workspace-specific examples should remain in parent-repository evidence artifacts, not in public Craft fixtures.
- Public examples can demonstrate the shape with fictional or already-public sample contexts.

## Recommended Next Routes

1. `sigil-development --update craft` to approve this as a Craft lifecycle update.
2. `task-session` on `SWU-CFR-001` after the maintainer selects a first executable unit.
3. Regenerate generated runtime surfaces only after canonical source mutation passes validation.
