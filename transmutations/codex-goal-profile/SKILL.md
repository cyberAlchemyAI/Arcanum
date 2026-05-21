---
name: codex-goal-profile
description: "Use when converting an Arcanum work-pack task or SWU into a strong native Codex /goal command with outcome, verification surface, constraints, boundaries, iteration policy, and blocked stop condition."
argument-hint: "<work-pack-path> --swu <SWU-ID> [--output <path>]"
tier: transmutations
domain: codex-goal-authoring
version: 0.1.0
origin: extracted from retired Arcanum goal spell after native Codex Goals became the runtime owner
allowed-tools: Read, Write, Glob, Grep
---

<objective>
Transform a selected Arcanum work-pack task or SWU into a native Codex `/goal` profile that preserves scope, evidence, constraints, and stop conditions.
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
7. Do not claim runtime ownership. Codex native Goals own pause, resume, clear, continuation, and completion.
</process>

<quality-bar>
A good profile:

- can be pasted directly as a native Codex `/goal`,
- names the exact task or SWU,
- has a measurable completion condition,
- names the verification surface,
- constrains write scope,
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
- Stop condition: <blocked report rule>
- Validation: <checks performed or not run>
```
</output-contract>
