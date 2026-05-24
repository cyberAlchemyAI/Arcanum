---
name: codex-goal-profile
description: "Use when converting an Arcanum work-pack task or SWU into a strong native Codex /goal command with outcome, verification surface, constraints, boundaries, iteration policy, and blocked stop condition."
argument-hint: "<work-pack-path> --swu <SWU-ID> --context-pack <markdown-path> --context-index <json-path> [--output <path>]"
tier: transmutations
domain: codex-goal-authoring
version: 0.2.0
origin: extracted from retired Arcanum goal spell after native Codex Goals became the runtime owner
allowed-tools: Read, Write, Glob, Grep
---

<objective>
Transform a selected Arcanum work-pack task or SWU into a native Codex `/goal` profile that preserves scope, evidence, constraints, stop conditions, and strict handoff-pack context.
</objective>

<logic-type>
Transmutation: bounded synthesis from work-pack execution contract to native Codex Goal command.
</logic-type>

<applicability>
Use this skill when:

- a work-pack, task, or SWU is ready for execution,
- native Codex Goals are available,
- the task may require continuation across turns,
- the user needs a compact, auditable `/goal` command rather than another planning artifact.
</applicability>

<inputs>
Expected inputs:

- work-pack path,
- selected task ID or SWU ID,
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
</inputs>

<process>
1. Confirm the selected task or SWU. If multiple SWUs are available and none is selected, stop and ask for the SWU.
2. Read only the work-pack row, parent task contract, source links, and validation context needed for that unit.
3. Check readiness:
   - dependencies are satisfied or explicitly named,
   - write scope is bounded,
   - done criteria are concrete,
   - validation surface is available,
   - handoff pack Markdown and JSON/index are available,
   - strict coverage passed,
   - fallback exploration is limited to named uncovered obligations or gaps,
   - blockers do not prevent safe execution.
4. If readiness fails, return a blocked profile with the exact unblock action rather than generating a runnable `/goal`.
5. Build the native Codex Goal using six fields:
   - outcome,
   - verification surface,
   - constraints,
   - boundaries,
   - iteration policy,
   - blocked stop condition.
6. Preserve work-pack navigation by referencing the task/SWU/source files in the profile.
7. Preserve handoff-pack navigation by referencing the Markdown pack and structured index.
8. Require the runtime final report to name any extra sources used outside the handoff pack, the gap that justified each source, and whether the source changed the result.
9. Do not claim runtime ownership. Codex native Goals own pause, resume, clear, continuation, and completion.
</process>

<quality-bar>
A good profile:

- can be pasted directly as a native Codex `/goal`,
- names the exact task or SWU,
- has a measurable completion condition,
- names the verification surface,
- constrains write scope,
- references the session-evidence handoff pack and JSON/index,
- requires pack-first execution,
- permits broad exploration only for named gaps from the pack,
- requires reporting extra sources used for named-gap fallback exploration,
- names dependencies and blockers,
- explains what Codex should do between iterations,
- states when to stop and what to report.
</quality-bar>

<anti-patterns>
Avoid:

- creating an Arcanum `/goal` command that competes with native Codex Goals,
- generating a goal for an unselected task bundle,
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
