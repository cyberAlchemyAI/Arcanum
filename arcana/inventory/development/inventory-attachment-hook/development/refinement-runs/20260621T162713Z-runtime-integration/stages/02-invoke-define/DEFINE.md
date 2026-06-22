---
module: inventory-attachment-hook
runId: 20260621T162713Z-runtime-integration
stage: s2-invoke-define
status: pass
updatedAt: 2026-06-21
docType: invoke-define
---

# Define: Runtime Integration Contract

## Definition

Runtime integration for Inventory Attachment Hook is the host-specific projection
of one shared Arcanum closeout contract:

```text
managed chat invocation
  -> primary skill/spell result
  -> observed invocation envelope
  -> primary telemetry append or explicit skip
  -> Inventory Attachment eligibility and handoff
  -> candidate Inventory evidence or explicit skip/dedupe/warn/block
  -> closeout receipt with primary status, observability status, and attachment status
```

The integration is successful when Codex, Claude Code, and generic runtimes can
each produce this lifecycle for a chat-invoked managed skill or spell without
making their host-specific hooks or generated packages canonical authority.

## Scope

In scope:

- explicit `$skill` or managed spell invocation from chat;
- native runtime package metadata;
- observation envelope setup and closeout;
- Inventory Attachment policy lookup and handoff;
- runtime-specific receipt shape and validation;
- local fallback when deterministic hooks are unavailable.

Out of scope:

- VS Code, Cursor, panel, or command-palette UX;
- always-on attachment for every skill;
- ontology, definitions, constitutions, axioms, or discipline promotion;
- implementation of hook scripts in this refine run.

## Shared Terms

| Term | Meaning |
| --- | --- |
| managed chat invocation | A user or agent invokes an Arcanum skill, sigil, or spell through the active chat runtime, such as `$refine` or `$inventory`. |
| host runtime lane | A projection of the shared contract into Codex, Claude Code, or a generic runtime. |
| invocation envelope | Privacy-safe run record containing capability id, kind, mode, request summary, status, outputs, validation, and observer fields. |
| attachment handoff | Candidate-only request from the observed invocation closeout into Inventory. |
| host-interface projection | Editor or UI shell behavior layered above runtime integration. Deferred for this route. |

## Decisions

| Decision | Resolution |
| --- | --- |
| First proof surface | Chat-invoked managed skills/spells, not VS Code UI. |
| Authority | Canonical Arcanum sources define the contract; generated packages and host hooks project it. |
| Attachment authority | Inventory records are candidate read models only. |
| Failure default | Warn/skip by default; block only when the policy marks attachment required or strict telemetry applies. |
| Research | No external research; local repository evidence names the current gap clearly. |

## Unresolved Gaps

| Gap | Owner | Route |
| --- | --- | --- |
| Direct `$skill-name` Codex invocation lacks deterministic observation. | observability/OIL implementation | future task-session after design |
| Implicit skill selection cannot be fully observed without platform metadata or wrapper execution. | runtime adapter design | generic fallback marker and explicit invocation first |
| Claude Code hook parity depends on native worker/receipt discipline rather than Codex Stop hooks. | Claude runtime lane | generated package and stage-worker receipt contract |

## Invoke Result

- Mode: define
- Spell: invoke
- Canonical ID: invoke
- Scope: library
- Phase status: pass
- Mode contract: `spells/invoke/define.md`
- Outputs: this definition artifact
- Template selection: target-local refinement stage artifact
- Dispatch techniques: `sequence`, `x_ray`, `tournament`, `owner_boundary_check`, `observability_grouping`
- Distill validation: required in stage s5
- Next route: design
