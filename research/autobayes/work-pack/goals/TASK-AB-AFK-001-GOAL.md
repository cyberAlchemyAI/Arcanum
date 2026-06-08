---
profile: autobayes-research
name: Codex Goal Profile - TASK-AB-AFK-001
description: Native Codex goal profile for subagent closeout hardening.
type: codex-goal-profile
status: pass
task_id: TASK-AB-AFK-001
swu_id: SWU-AB-AFK-001
last_updated: 2026-06-07
---

# Codex Goal Profile Result

- Source work-pack: `research/autobayes/work-pack/WORK-PACK.md`
- Selected unit: `SWU-AB-AFK-001` / `TASK-AB-AFK-001`
- Readiness: `pass`
- Verification surface:
  - `formulae/dispatch-spec/scripts/validate-dispatch.py research/autobayes/development/refinement-runs/20260607T044519Z-subagent-closeout-hardening/REFINE-DISPATCH.json --json`
  - `formulae/dispatch-spec/development/run-validation-fixtures.sh` if canonical Dispatch Spec files change
- Boundaries:
  - safe first scope: `research/autobayes/work-pack/`, refinement run folder
  - conditional canonical scope: Task Session and Dispatch Spec files named in context pack
- Handoff pack:
  - Markdown: `research/autobayes/work-pack/context/TASK-AB-AFK-001-CONTEXT.md`
  - JSON/index: `research/autobayes/work-pack/context/TASK-AB-AFK-001-CONTEXT.json`
- Strict coverage: `pass`
- Fallback exploration: `named gaps only`
- Extra-source reporting: `required`
- Stop condition: stop and report `blocked` if hidden open subagents could pass, if canonical write scope is unsafe, if validation cannot prove closeout behavior, or if the context pack/index is missing.

## Native Goal

```text
/goal Implement SWU-AB-AFK-001 from research/autobayes/work-pack/WORK-PACK.md: harden AutoBayes research subagent closeout so Task Session and Dispatch Spec can prove every spawned subagent was joined, closed, blocked, timed out, or handed off before a mostly-AFK research run reports success.

Outcome:
Create or update the minimum artifacts needed for a subagent lifecycle closeout gate. The result must make hidden open subagents impossible to treat as PASS. It must preserve thread-cap failures as explicit residue with reroute, and it must keep local research planning separate from canonical Arcanum mutation unless owner-ready implementation is justified.

Verification surface:
Read the handoff pack first:
- research/autobayes/work-pack/context/TASK-AB-AFK-001-CONTEXT.md
- research/autobayes/work-pack/context/TASK-AB-AFK-001-CONTEXT.json
Then validate:
- formulae/dispatch-spec/scripts/validate-dispatch.py research/autobayes/development/refinement-runs/20260607T044519Z-subagent-closeout-hardening/REFINE-DISPATCH.json --json
If canonical Dispatch Spec files are changed, also run:
- formulae/dispatch-spec/development/run-validation-fixtures.sh
If Task Session text is changed, inspect the output contract and anti-patterns for consistency and report the exact changed lines.

Constraints:
- Pack-first execution only. Start from the context pack and JSON index.
- Write first inside research/autobayes/work-pack/ and the refinement run folder.
- Canonical edits to arcana/task-session or formulae/dispatch-spec require explicit owner-ready rationale in the final report.
- Every spawned subagent must have a lifecycle record: spawned, joined, timed out, blocked, closed, or handed off.
- A hidden open subagent must block success.
- A thread-cap failure may pass only when recorded as explicit residue with reroute.
- Do not promote Inventory, Ontology, glossary, sigil, spell, runtime, Task Session, or Dispatch Spec canon without evidence and owner-ready validation.

Boundaries:
- Source work-pack: research/autobayes/work-pack/WORK-PACK.md
- Selected task: research/autobayes/work-pack/tasks/TASK-AB-AFK-001-subagent-closeout-hardening.md
- Handoff Markdown: research/autobayes/work-pack/context/TASK-AB-AFK-001-CONTEXT.md
- Handoff JSON/index: research/autobayes/work-pack/context/TASK-AB-AFK-001-CONTEXT.json
- Primary evidence: research/autobayes/sessions/task-session-autobayes-all-possible-subagents-result.md and research/autobayes/sessions/task-session-autobayes-full-mode-result.md

Iteration policy:
Work in small passes. First establish the lifecycle ledger contract, then the closeout gate, then any Task Session or Dispatch Spec wording/fixture changes. After each pass, run the relevant validation or record why it is not applicable. Use fallback exploration only for named gaps from the context pack, and report every extra source used, the gap it addressed, and whether it changed the result.

Blocked stop condition:
Stop and report blocked if the handoff Markdown or JSON index is missing, if validation cannot be run or substituted, if the design would allow open subagents to pass silently, if canonical write scope becomes necessary without owner-ready rationale, or if the work would require destructive cleanup outside the selected scope.
```

