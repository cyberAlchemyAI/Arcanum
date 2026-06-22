---
module: inventory-attachment-hook
version: draft
status: refinement-draft
updatedAt: 2026-06-21
docType: runtime-integration-model
---

# Runtime Integration Model: Inventory Attachment Hook

This model is non-authoritative design evidence. Canonical implementation still
requires a later owner route that patches canonical sources first and then
regenerates runtime mirrors.

## Purpose

Inventory Attachment Hook must work when a managed Arcanum skill or spell is
invoked through chat, such as `$refine`, `$inventory`, or `$craft`.

The runtime model is not an editor UI model. VS Code, Cursor, sidebars, panels,
and command-palette behavior are later host-interface projections.

## Smallest Runtime Unit

`ChatSkillAttachmentCloseout`

Responsibility: close one chat-invoked managed skill or spell with a primary
result, observability evidence, and optional Inventory Attachment candidate
evidence.

## Shared Lifecycle

```text
1. Resolve capability identity
2. Run primary skill/spell
3. Preserve primary result
4. Build observed invocation envelope
5. Append or explicitly skip primary telemetry
6. Evaluate inventoryAttachment policy
7. Select durable safe outputs
8. Hand selected outputs to Inventory as candidate evidence
9. Record attach/skip/dedupe/warn/block status
10. Return one closeout receipt
```

Inventory Attachment starts only after the observed invocation envelope exists
and primary telemetry has been handled. Attachment never replaces the primary
result and never promotes Inventory records into definitions, ontology,
constitutions, axioms, disciplines, sigils, or spells.

## Shared Contract

Every runtime lane must supply or explicitly skip these fields.

| Field | Required | Notes |
| --- | --- | --- |
| `invocation_id` | yes | Stable enough for idempotency and closeout. |
| `capability.id` | yes | Skill, sigil, or spell id. |
| `capability.kind` | yes | `skill`, `sigil`, or `spell`. |
| `capability.source_ref` | yes | Canonical source or generated package provenance. |
| `request.summary` | yes | Privacy-safe summary, not raw private prompt by default. |
| `execution.status` | yes | `completed`, `partial`, `blocked`, or `failed`. |
| `execution.outputs` | yes | Durable output refs or empty with skipped reason. |
| `execution.validation` | yes | Commands, checks, or reviewable validation notes. |
| `observability.status` | yes | recorded, deduped, skipped, failed, or unavailable. |
| `inventoryAttachment.policy` | optional | Absence means normal no-op. |
| `inventoryAttachment.result` | yes when attempted | attached, skipped, deduped, warned, blocked, or failed. |
| `residue` | yes | Empty list when none. |

## Proof Strength

Runtime evidence has levels. A lane may be acceptable for design with a flag,
but implementation readiness depends on the proof level it can produce.

| Level | Name | Meaning | Readiness |
| --- | --- | --- | --- |
| L0 | prose closeout | Agent reports what happened without durable envelope or receipt. | not enough |
| L1 | manual fallback receipt | Parent agent records the shared receipt fields and explicit skipped/unavailable observer reason. | flag |
| L2 | deterministic wrapper | A wrapper resolves the capability, gathers receipt fields, and calls or skips observer deterministically. | flag/pass depending on fixtures |
| L3 | native runtime receipt | Host runtime skill/subagent returns structured receipt fields consumed by the observer/attachment path. | pass when fixtures pass |
| L4 | native hook bridge | Host hook opens, updates, closes, observes, and attaches without relying on agent memory. | strongest pass |

Generic and Claude Code lanes may start at L1 or L2 when no host hook exists.
Codex chat `$skill` proof should target L4 by adding a skill-aware bridge for
`.agents/skills/` invocations.

## Runtime Lanes

### Codex Lane

Codex currently has generated skill packages under `.agents/skills/`. Existing
command hooks under `.codex/hooks.json` plus `.codex/hooks/` are prior evidence
for envelope mechanics only; `/command` compatibility is not an acceptance
requirement for this route.

The target Codex projection is skill-aware:

```text
$skill-name chat invocation
  -> resolve .agents/skills/<skill-name>/SKILL.md
  -> open observed envelope with capability metadata
  -> run primary native skill
  -> close through Stop hook or equivalent wrapper
  -> evaluate Inventory Attachment
  -> append telemetry and attachment closeout evidence
```

Legacy `/command` hooks are useful prior evidence, but the proof surface for
this route is direct chat `$skill-name` invocation.

### Claude Code Lane

Claude Code uses generated `.claude/skills/` packages and `.claude/agents/`
workers. Its projection should not copy Codex hook mechanics. It should produce
the same closeout receipt through native skill execution or a stage worker:

```text
chat/native skill invocation
  -> generated Claude skill package
  -> bounded worker or parent agent execution
  -> receipt with primary result, artifacts, validation, blockers, residue
  -> observed envelope and attachment handoff
```

Claude-specific tool-name translation and agent boundaries are host-local
projection details.

### Generic Runtime Lane

Generic runtimes may lack native hooks. Their projection is a deterministic
wrapper or explicit local observer pass:

```text
managed invocation wrapper
  -> resolve capability metadata
  -> execute or hand off native skill prompt
  -> build envelope from declared receipt fields
  -> call observer append authority when available
  -> evaluate Inventory Attachment
  -> write closeout receipt or skipped reason
```

The wrapper may be `tools/arcanum`, a dry-run adapter, or another deterministic
host adapter. It must not become the canonical contract.

When no native hook API exists, the lane must still emit a fallback receipt with
the shared closeout fields. It must mark hook enforcement as `fallback`,
`wrapper`, or `unavailable`; it must not pretend native hook evidence exists.

## Authority Boundaries

| Boundary | Rule |
| --- | --- |
| canonical to generated | Patch canonical Arcanum sources first; generated mirrors are refreshed from canonical source. |
| observability to Inventory | Observability handles the run before Inventory receives selected outputs. |
| Inventory to promotion | Inventory writes candidate read models only. Promotion requires a separate owner route. |
| runtime to host UI | Runtime closeout does not define editor UI behavior. |
| hook operation to capability telemetry | Hook operation rows are infrastructure evidence and must not trigger attachment recursion. |

## Existing Gap

The repository already identifies that direct Codex `$skill-name` invocation can
bypass deterministic observability because existing hook logic is command-shaped.
The first implementation route must therefore create or document a skill-aware
observation bridge before claiming Inventory Attachment works for chat-invoked
skills.

## Acceptance Model

The model is acceptable when a pilot chat invocation can prove:

1. capability metadata is resolved;
2. primary result is preserved even if attachment fails;
3. telemetry is recorded, deduped, or explicitly skipped;
4. `inventoryAttachment` absent/disabled is a normal no-op;
5. enabled attachment produces candidate Inventory evidence;
6. unsafe or private outputs are rejected;
7. recursion guard prevents Inventory from attaching its own attachment rows;
8. closeout reports primary, observability, and attachment status together.

Until a lane has L3 or L4 proof, its status is `flag`, not `pass`.
