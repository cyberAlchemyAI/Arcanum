---
module: inventory-attachment-hook
runId: 20260621T162713Z-runtime-integration
status: executed-flag
updatedAt: 2026-06-21
docType: refine-result
---

# Refine Result: Runtime Integration Model And Design

## Status

Runtime-backed Refine stages ran after operator confirmation.

Scope clarified by operator: the first working surface is skill or spell
invocation through chat. VS Code, Cursor, editor panels, and command-palette UX
are deferred host-interface projections.

## Outputs

- `arcanum/arcana/inventory/development/inventory-attachment-hook/RUNTIME-INTEGRATION-MODEL.md`
- `arcanum/arcana/inventory/development/inventory-attachment-hook/RUNTIME-INTEGRATION-DESIGN.md`

## Stage Evidence

| Stage | Verdict | Artifact |
| --- | --- | --- |
| Context Builder evidence baseline | pass | `stages/01-context-builder/CONTEXT-PACK.md` |
| Invoke Define | pass | `stages/02-invoke-define/DEFINE.md` |
| Interrogation refine-review | pass | `stages/03-refine-review/REVIEW.md` |
| Research decision | pass | `stages/04-research-decision/RESEARCH-DECISION.md` |
| Distill | pass | `stages/05-distill/DISTILL.md` |
| Invoke Design | flag | runtime model/design artifacts |
| Runtime lane review | flag | `stages/07-runtime-lane-review/REVIEW.md` |
| Distill Repair | pass | `stages/08-distill-repair/REPAIR.md` |
| Invoke Plan refresh | pass | `stages/09-invoke-plan/PLAN-REFRESH.md` |
| Final synthesis | flag | `stages/10-final/FINAL-REVIEW.md` |

## Final Verdict

`flag`

The runtime integration design is coherent and ready for bounded implementation,
but runtime proof is not complete.

The decisive gap is not VS Code. The gap is that explicit chat `$skill-name`
invocation must produce deterministic closeout evidence directly, without using
`/command` compatibility as the proof path.

## Synthesis

The accepted model is:

```text
canonical Arcanum contract
  -> generated/native runtime package
  -> chat skill invocation closeout
  -> observed envelope and telemetry
  -> optional Inventory Attachment candidate handoff
  -> closeout receipt
```

All lanes accept the shared contract as pre-implementation design:

- Codex needs a skill-aware bridge for `.agents/skills/<skill>/SKILL.md`.
- Claude Code needs native skill/stage-worker receipt gates.
- Generic runtimes need an explicit no-native-hook fallback receipt schema.
- Boundary review requires canonical-first edits, candidate-only Inventory
  authority, public-boundary checks, recursion guards, and UI deferral.

## Recommended Next Route

Run `task-session` for `SWU-IAH-RUNTIME-001`:

```text
Add skill-aware Codex observation bridge for explicit chat `$skill-name`
invocation and fixture proof.
```
