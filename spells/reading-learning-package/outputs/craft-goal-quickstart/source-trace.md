# Source Trace — Craft + Goal Quickstart

Every load-bearing *mechanism* claim in the manuscript maps to a source artifact
below. Analogies (expedition, logbook, autopilot, toll booth, conductor) are the
author's framing for teaching and are **not** source claims.

| Manuscript claim | Source authority |
| --- | --- |
| Craft keeps a durable project memory across sessions | `arcanum/arcana/craft/README.md` (durable local memory for nested contexts, blockers, decisions, gaps, next moves) |
| Two files: `.craft/ledger.yml` is source of truth, `CRAFT.md` is human view | `arcanum/arcana/craft/SKILL.md` <storage-contract>; `README.md` Storage Model |
| Row families: contexts, blockers, enablers, decisions, gaps, definitions, next moves | `arcanum/arcana/craft/SKILL.md` <core-methods> |
| Raw blockers cannot be resolved directly; must be refined into a closure condition | `arcanum/arcana/craft/SKILL.md` (`refine_blocker`, <non-use>, <quality-bar>) |
| Goal is a fail-closed control loop: read frontier → classify risk → dispatch → stage/approve | `.agents/skills/goal/SKILL.md` Control Spine; Execution Phases |
| Goal stops before file mutation, shell/network, publication, commit/push unless approved | `.agents/skills/goal/SKILL.md` Failure Policy; Trigger Conditions |
| Unknown risk resolves to protected (stop) | `.agents/skills/goal/SKILL.md` Classify risk phase; Gates (Risk classification) |
| Closing work needs real evidence; promotion gated by an approval token | `.agents/skills/goal/SKILL.md` Gates (Receipt closeout, Approval token); `.agents/skills/goal/CRAFT.md` |
| Goal routes work to owning capabilities (Craft, task-session, decision-gate) | `.agents/skills/goal/SKILL.md` Required Capabilities |
| Controller / OpenClaw modeled as an external **agent runtime** behind a host port | `arcanum/arcana/integration-spec/.../20260616T203246Z-openclaw-sdk-integration-refine/RESULT.md` |
| OpenClaw gateway/RPC is the recommended default; CLI subprocess valid for one-shot | same RESULT.md ("OpenClaw-Specific Decision") |
| Agent lifecycle: start a turn, wait for result, cancel a stuck run | same RESULT.md (Invocation mode; Timeout/cancellation) |

## Honesty flags

- **"Hermes-class controller"** is named as an *example* of a controller model. No
  Hermes integration is documented in this repository; it is framed as the
  general pattern, not a shipped feature.
- **Controller / OpenClaw section** describes a *design you grow into*. OpenClaw is
  a promotion-candidate integration model in `integration-spec`, not a finished
  one-click capability. The manuscript states this explicitly.
- The manuscript deliberately avoids any "fully autonomous" claim, matching Goal's
  fail-closed contract.

## No-promotion boundary

This package (manuscript, HTML, PDF, preset profile) is a **learning artifact**.
It does not promote Craft, Goal, or OpenClaw vocabulary or claims into canonical
definitions. The linked skill files remain the authority.
