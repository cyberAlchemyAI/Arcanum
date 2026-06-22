---
name: codex-goal-profile
description: "Use when converting an Arcanum work-pack task, SWU, or explicitly selected one-shot stream into a compact native Codex /goal command with sidecar context, profile policy, verification surface, constraints, boundaries, iteration policy, and blocked stop condition."
argument-hint: "<work-pack-path> --swu <SWU-ID>|--task <TASK-ID>|--one-shot <STREAM-ID> --context-pack <markdown-path> --context-index <json-path> [--decision-profile <path>] [--output <path>]"
tier: transmutations
domain: codex-goal-authoring
version: 0.2.0
origin: extracted from retired Arcanum goal spell after native Codex Goals became the runtime owner
allowed-tools: Read, Write, Glob, Grep
---

<objective>
Transform a selected Arcanum work-pack task, SWU, or explicitly selected one-shot stream into a compact native Codex `/goal` profile that preserves scope, evidence, constraints, stop conditions, strict handoff-pack context, and optional runtime decision-profile policy.
</objective>

<logic-type>
Transmutation: bounded synthesis from work-pack execution contract to native Codex Goal command.
</logic-type>

<applicability>
Use this skill when:

- a work-pack, task, SWU, or explicitly selected one-shot stream is ready for execution,
- native Codex Goals are available,
- the task may require continuation across turns,
- the user needs a compact, auditable `/goal` command rather than another planning artifact.
- a richer Arcanum execution frame must be preserved through sidecar context instead of exceeding the native goal text budget.
</applicability>

<inputs>
Expected inputs:

- work-pack path,
- selected task ID, SWU ID, or explicit one-shot stream ID,
- parent task contract,
- dependencies,
- source contracts,
- write scope,
- done criteria,
- validation command or evidence surface,
- handoff pack Markdown path,
- handoff pack JSON/index path,
- strict coverage status,
- fallback exploration rule,
- blocker state,
- budget or stop constraints.
- native goal character budget, default `4000`,
- optional private/runtime decision profile path, for example `.arcanum/profiles/decision-profile.yml`,
- optional capability policy for one-shot runs: allowed sigils, subagent authorization, receipt expectations, and stop gates.
</inputs>

<compact-goal-budget>
Native Codex goal text should fit within the current runtime input limit. Default
budget: 4000 characters for the `/goal ...` line.

When the full execution vision does not fit:

1. Write or reference a sidecar profile/handoff artifact that carries the richer
   Arcanum context, capability policy, work-pack navigation, and verification
   details.
2. Keep the `/goal` line compact: name the outcome, verification surface, source
   sidecar, write boundary, iteration rule, and blocked stop condition.
3. Treat over-budget native goal text as `block` unless a sidecar-backed compact
   rewrite is produced.

Do not stuff the goal with every source excerpt. The native goal should point to
the selected evidence pack and sidecar; the pack carries density, the goal carries
control.
</compact-goal-budget>

<decision-profile-policy>
When a `--decision-profile` path is provided or clearly selected by the user,
read it as runtime-private policy evidence. A local profile may influence:

- risk posture and default-deny behavior,
- approval and mutation gates,
- slice size and sequencing,
- ownership boundaries,
- gap-filling and interrogation style,
- technique preferences,
- anti-pattern stop conditions.

The generated profile may summarize only operational effects needed for the
current goal. Do not copy private profile contents into reusable public examples,
canonical skill text, or public package fixtures. Record the profile path and the
policy fields consumed in the audit block.
</decision-profile-policy>

<one-shot-policy>
A one-shot profile is allowed only when the user explicitly selects a full stream
or the work-pack names a single ordered implementation line. A one-shot profile
must still be gated:

- run prerequisite/contract units before runtime units,
- stop at blocker-level decisions and route them through `decision-gate`,
- use `refine` only to repair or re-scope named design/plan gaps,
- use `invoke` only to author missing define/design/plan/handoff artifacts named
  by the pack,
- use `craft` only to update a scoped project ledger when the pack/profile asks
  for durable blocker, decision, gap, or next-move state,
- spawn subagents only when explicitly authorized by the work-pack, dispatch,
  sidecar profile, or operator instruction, and require role receipts before
  parent synthesis,
- keep Task Session or Codex runtime evidence separate from reusable sigil
  validation evidence.

The one-shot goal should empower Codex to finish the selected stream, not to
silently widen project scope.
</one-shot-policy>

<process>
1. Confirm the selected task, SWU, or explicit one-shot stream. If multiple SWUs are available and neither a single unit nor one-shot stream is selected, stop and ask for the unit.
2. Read only the work-pack row, parent task contract, source links, and validation context needed for that unit.
3. If a decision profile is provided, read only the fields needed for the current goal policy and preserve the private/public boundary.
4. Check readiness:
   - dependencies are satisfied or explicitly named,
   - write scope is bounded,
   - done criteria are concrete,
   - validation surface is available,
   - handoff pack Markdown and JSON/index are available,
   - strict coverage passed,
   - fallback exploration is limited to named uncovered obligations or gaps,
   - blockers do not prevent safe execution.
   - goal text can fit the character budget or a sidecar-backed compact rewrite is available,
   - one-shot capability policy is explicit when more than one SWU/task will run.
5. If readiness fails, return a blocked profile with the exact unblock action rather than generating a runnable `/goal`.
6. Build the native Codex Goal using six fields:
   - outcome,
   - verification surface,
   - constraints,
   - boundaries,
   - iteration policy,
   - blocked stop condition.
7. Keep the native goal within the selected character budget. If needed, emit a sidecar profile and have the goal reference it.
8. Preserve work-pack navigation by referencing the task/SWU/source files in the profile.
9. Preserve handoff-pack navigation by referencing the Markdown pack and structured index.
10. Preserve decision-profile navigation without copying private profile content.
11. Require the runtime final report to name any extra sources used outside the handoff pack, the gap that justified each source, and whether the source changed the result.
12. Do not claim runtime ownership. Codex native Goals own pause, resume, clear, continuation, and completion.
</process>

<quality-bar>
A good profile:

- can be pasted directly as a native Codex `/goal` within the configured character budget,
- names the exact task, SWU, or explicit one-shot stream,
- has a measurable completion condition,
- names the verification surface,
- constrains write scope,
- references the session-evidence handoff pack and JSON/index,
- requires pack-first execution,
- permits broad exploration only for named gaps from the pack,
- requires reporting extra sources used for named-gap fallback exploration,
- summarizes any decision-profile policy consumed without leaking private profile contents,
- gates one-shot subagent and sigil use through explicit capability policy and receipts,
- names dependencies and blockers,
- explains what Codex should do between iterations,
- states when to stop and what to report.
</quality-bar>

<anti-patterns>
Avoid:

- creating an Arcanum `/goal` command that competes with native Codex Goals,
- generating a goal for an unselected task bundle,
- generating an over-budget goal instead of compacting or using a sidecar,
- copying private decision-profile contents into public reusable artifacts,
- treating a decision profile as permission to ignore explicit human gates,
- authorizing subagents, `refine`, `invoke`, `craft`, or `decision-gate` as broad ambient authority instead of bounded capability lanes,
- omitting verification,
- hiding blockers,
- allowing broad write scope by default,
- generating a goal without strict handoff-pack coverage,
- treating fallback exploration as permission for broad discovery,
- saying "keep going until done" without a budget or stop condition,
- marking the goal complete without evidence.
</anti-patterns>

<output-contract>
Return:

```markdown
## Codex Goal Profile Result

- Source work-pack: <path>
- Selected unit: <task-or-swu-id>
- Readiness: pass | block
- Goal budget: <limit and pass | block>
- Decision profile: <path or none; consumed fields or n/a>
- One-shot mode: yes | no
- Capability policy: <allowed sigils/subagents and receipt gates or none>
- Sidecar profile: <path or n/a>
- Native Goal:
  ```text
  /goal <goal text>
  ```
- Verification surface: <command or evidence>
- Boundaries: <write scope and source context>
- Handoff pack: <markdown path and JSON/index path>
- Strict coverage: pass | block
- Fallback exploration: none | named gaps only | block
- Extra-source reporting: required | n/a
- Stop condition: <blocked report rule>
- Validation: <checks performed or not run>
```
</output-contract>
