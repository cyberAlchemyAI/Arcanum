---
name: refine
description: "Use when: turning a vague refinement target, design concern, folder, idea, or existing work-pack into a confirmed refinement seed before Task Session execution."
argument-hint: "<target> [--preset compact|standard|full|deep] [--research no|bounded|if-gap] [--local-fallback]"
tier: arcana
domain: refinement-governance
version: 0.1.0
origin: created from one-loop refinement seed using refine loop ownership and sigil-development handoff
allowed-tools: Read, Write, Glob, Grep, AskQuestions, Bash, Task
---

# Sigil: Refine

<objective>
Create a confirmed refinement seed from a vague or under-specified target, then route the approved unit to Task Session with Codex Goal as the default runtime.
</objective>

<logic-type>
Arcana: refinement seed governance with research offer, budget preflight, confirmation gate, and runtime handoff.
</logic-type>

<required-sigils>

Refine is a preflight controller. It prepares an executable refinement-loop plan whose stages must use the actual installed skill/sigil contracts below when Task Session runs the approved unit.

| Sigil | Required For | Evidence Required |
| --- | --- | --- |
| `context-builder` | Build or consume the local evidence baseline before Define, critique, Distill, or handoff. | Context pack path or blocked coverage reason. |
| `invoke` | Produce Define, Redefine, Design, and Plan phase artifacts when those phases are in the selected preset. | Invoke artifact path, mode, and verdict. |
| `interrogation` | Critique the definition, design, plan, handoff, and final synthesis according to the selected preset. | Interrogation artifact path and pass/flag/block verdict. |
| `distill` | Select or repair the smallest coherent unit, including tournament mode when required by the preset. | Distill artifact path, selected unit, and rejected alternatives. |
| `sigil-development` | Own reusable sigil lifecycle handoff, examples, observability, validation, reflection, and promotion readiness. | Handoff artifact path or lifecycle blocked reason. |
| `task-session` | Execute an approved work-pack task or SWU only after Refine has produced and confirmed a seed/preflight. | Proposed or executed Task Session route and handoff status. |

</required-sigils>

<execution-plan-contract>

Every required stage in the prepared loop must be dispatched by Task Session/Codex Goal through the actual skill/sigil workflow available in the current runtime. Do not replace a stage with freeform prose when the skill is installed and applicable.

For each planned and executed stage:

1. Preserve the stage's observation envelope, invocation summary, artifact path, or blocked reason.
2. Keep the stage's native authority boundary. Refine may prepare and synthesize the execution plan, but Task Session owns execution and the required skills own their stage internals.
3. If a required skill is unavailable, the Task Session run must return `BLOCK` unless the user explicitly authorizes a local emulation for that run.
4. If the selected preset skips a stage, record why the preset allowed the skip.
5. If external research is selected or becomes necessary, ask for explicit confirmation before browsing.

</execution-plan-contract>

<applicability>
Use this sigil when:

- the user asks to refine a target but has not selected one approved work-pack task or SWU,
- a folder, design, plan, idea, or concern needs a bounded refinement seed,
- the user needs to see budget, loop count, research mode, and Codex Goal readiness before execution,
- the next safe step is Task Session execution through Codex Goal,
- a seed work-pack should be proposed before mutation-capable work begins.
</applicability>

<non-applicability>
Do not use this sigil when:

- an approved task/SWU is already selected and the user only wants Task Session execution,
- the request is a trivial direct edit,
- the user wants only Invoke design/plan artifacts without execution routing,
- strict Codex Goal handoff cannot be prepared and the user has not explicitly requested local fallback.
</non-applicability>

<inputs>
Expected inputs, if available:

- target folder, artifact, idea, design concern, plan, or work-pack,
- desired preset: compact, standard, full, or deep,
- desired research mode: no, bounded, or if-gap,
- existing source context or constraints,
- preferred output location for seed artifacts,
- explicit local fallback permission, if Codex Goal is unavailable or unsafe.
</inputs>

<ownership-boundary>
Refine owns seed proposal and confirmation. It does not own execution.

- Task Session owns context packs, gates, runtime handoff, execution, validation, and evidence sync.
- The Refine Loop owns refinement phases, pass limits, research bounds, repair rules, and synthesis requirements.
- Context Builder owns context and Codex Goal handoff packs.
- Codex Goal Profile owns native `/goal` text.
- Sigil Development owns reusable sigil lifecycle and promotion readiness.
</ownership-boundary>

<research-policy>
Refine must always offer research before refinement.

Options:

- `no-research`: use only local repository and supplied context.
- `bounded-research`: one external comparison pass within Refine Loop bounds.
- `research-if-gap-appears`: default; start local-first and ask again only if Interrogation or Distill identifies a named external-context gap.

Research bounds come from `arcana/refine/REFINEMENT-LOOP.md`. External research cannot override local repository evidence.
</research-policy>

<preset-policy>
Presets select loop budget; they do not redefine loop mechanics.

- `compact`: one refinement loop without research unless selected.
- `standard`: one refinement loop plus one repair/synthesis pass.
- `full`: full Refine Loop path, including research offer, tournament or repair when needed, plan, and final interrogation.
- `deep`: full path plus checkpoint before mutation-heavy delegation.

If the user asks for "full", use `full`. If no preset is supplied, recommend the smallest preset that can answer the target safely and ask for confirmation.
</preset-policy>

<process>
1. Resolve the target and determine whether a seed is needed.
2. If a work-pack and selected task/SWU already exist, skip seed creation and prepare a preflight for that unit.
3. Prepare a bounded local evidence baseline for the seed using available context; if strict coverage is needed for execution, require Task Session to build the persisted Context Builder handoff pack.
4. Build the refinement loop execution plan: required stages, preset-specific skips, research mode, stage order, expected artifacts, and blocked stop conditions.
5. Offer research using the research policy and record the selected mode. If research is selected, ask for explicit confirmation before browsing.
6. Prepare a seed proposal with target, task title, source context, write scope, done criteria, validation surface, preset, loop count, research mode, planned skill-stage obligations, Codex Goal readiness, and proposed Task Session route.
7. Make the approved Task Session/Codex Goal route responsible for dispatching `context-builder`, `invoke`, `interrogation`, `distill`, `invoke`, and `sigil-development` according to the planned loop.
11. Default runtime route to Codex Goal:

```text
/task-session to <seed-work-pack> --task <TASK-ID> --runtime codex --via goal
```

12. Check whether the proposed seed can support strict Codex Goal handoff. If required fields are missing, return a blocked handoff report instead of falling back silently.
13. Ask for confirmation before writing seed artifacts or delegating.
14. After confirmation, write the minimal seed work-pack when needed and route through Task Session.
15. If the user explicitly requested local fallback, route through Task Session without `--via goal` and record the override.
</process>

<quality-bar>
A successful Refine run must:

- produce a clear seed proposal before mutation,
- prepare required loop stages so Task Session/Codex Goal can dispatch the installed skills without manual supervision,
- require the Task Session result to preserve each required stage's observation envelope, artifact path, or blocked reason,
- offer research and record the selected research mode,
- reference the Refine Loop rather than duplicating loop mechanics,
- default to Codex Goal execution after confirmation,
- block unsafe Codex Goal handoff with exact missing fields,
- require user confirmation before writing seed artifacts or delegating,
- keep Task Session as execution owner,
- return a navigable route to the next lifecycle owner.
</quality-bar>

<observability>
For meaningful executions, emit or prepare a post-run signal through the local observability package when available.

Use `templates/usage-telemetry.md` as the sigil-local telemetry shape and `templates/reflection-report.md` for manual, threshold, or severe-gap reflection.

Recommended signal fields:

- target,
- seed needed,
- selected preset,
- selected research mode,
- confirmation result,
- Codex Goal eligibility,
- blocked handoff fields,
- seed artifact path,
- proposed Task Session route,
- delegation result when Task Session runs,
- local fallback override, if any.

Reflection should be considered when users repeatedly reject seed proposals, Codex Goal handoff blocks on the same missing field, or research mode selection causes repeated confusion.

Default reflection triggers:

- 5 meaningful executions,
- 10 generated or materially updated artifacts,
- 3 related workflow gaps,
- 1 severe workflow gap.
</observability>

<promotion-gate>
Refine is promotion-ready only after Sigil Development reviews example runs and experiment evidence showing:

- vague targets produce useful seed proposals,
- existing work-packs skip unnecessary seed creation,
- research choices are offered and recorded,
- unsafe Codex Goal handoffs block with exact missing fields,
- confirmed seeds can route into Task Session with `--runtime codex --via goal`,
- at least one live example captures the final refinement result produced by Task Session/Codex Goal rather than only the proposed route.
</promotion-gate>

<anti-patterns>
Avoid:

- copying the Refine Loop phases into a second source of truth,
- manually executing or emulating Context Builder, Invoke, Interrogation, Distill, or Sigil Development in Refine when the run should be delegated to Task Session/Codex Goal,
- using Refine as a Task Session replacement,
- running external research without explicit confirmation,
- silently falling back from Codex Goal to local execution,
- creating broad work-packs without write scope, done criteria, and validation,
- marking refinement complete before Task Session evidence returns.
</anti-patterns>

<output-contract>
Return:

```markdown
## Refine Seed Proposal

- Target: <target>
- Seed needed: yes | no
- Proposed task: <task id and title>
- Source context: <paths/selectors>
- Write scope: <paths or none>
- Done criteria: <criteria>
- Validation surface: <command or review evidence>
- Preset: compact | standard | full | deep
- Loop count: <n>
- Research: no-research | bounded-research | research-if-gap-appears
- Planned execution stages:
  - context-builder: <required | blocked | skipped by preset>
  - invoke-define: <required | blocked | skipped by preset>
  - interrogation: <required | blocked | skipped by preset>
  - distill: <required | blocked | skipped by preset>
  - invoke-design-plan: <required | blocked | skipped by preset>
  - sigil-development: <required | blocked | not_applicable>
- Runtime default: codex-goal
- Goal eligibility: pass | block
- Blocked handoff fields: <items or none>
- Proposed Task Session route: <command>
- Confirmation required: yes
```
</output-contract>
