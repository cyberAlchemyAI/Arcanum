# Task Session Glossary

## Canonical Terms

| Term | Definition | Status |
| --- | --- | --- |
| Task Session | A governed execution loop for one selected task or SWU, including context building, decisions, gates, execution, validation, and evidence sync. | linked |
| Selected Unit | The single task or SWU that a Task Session is allowed to execute. | linked |
| Work-Pack | A planning artifact containing task/SWU records, dependencies, status, source links, and validation expectations. | linked |
| SWU | Smallest Working Unit: the smallest execution unit in a work-pack that can be independently completed and verified. | linked |
| Context Pack | A compact task-ready context bundle with selector-level evidence mapped to obligations. | linked |
| Handoff Pack | A context pack prepared for runtime delegation, emitted as Markdown plus JSON/index, persisted as session evidence, and accepted only when strict obligation coverage passes. | linked |
| Strict Coverage | Handoff rule requiring every parsed obligation to be covered by selected evidence or explicitly resolved before runtime delegation. | linked |
| Obligation | A requirement, constraint, done criterion, dependency, validation expectation, or source contract the session must satisfy or explicitly block on. | linked |
| Decision Pack | A set of option cards for unresolved implementation choices, including consequences and recommended defaults. | linked |
| Gate Verdict | The result of checking scope, dependencies, blockers, context coverage, write scope, runtime readiness, and validation availability. | linked |
| Runtime Adapter | A boundary component that turns gated Task Session state into a runtime-specific handoff command or profile. | linked |
| Codex Goal Profile | A compact native Codex Goal contract generated from a selected work-pack task/SWU plus constraints and validation expectations. | linked |
| Evidence Sync | Updating task/work-pack status and related records only after supporting validation or accepted substitute evidence exists. | linked |
| Blocker | A condition that prevents safe mutation or runtime delegation until resolved. | linked |
| Fallback Exploration | Runtime repository exploration beyond the handoff pack, allowed only for named uncovered obligations or context gaps. | linked |
| Authority Precedence | The order used to resolve conflicts between user instruction, task contract, work-pack, architecture/spec, implementation, and inferred notes. | linked |

## Consistency Rules

- Use `Task Session` for the sigil and governed execution loop.
- Use `context pack` for the general selected evidence bundle.
- Use `handoff pack` when the context pack is explicitly passed to a runtime adapter or native goal.
- Use `strict coverage` for the runtime handoff gate, not as a general synonym for normal context quality.
- Use `runtime adapter` for the boundary, not for the runtime itself.
- Use `Codex Goal` for the native runtime capability and `Codex Goal Profile` for the Arcanum-generated profile.
- Do not call generated context packs canonical documentation; they are execution evidence.

## Candidate Terms Not Promoted

| Term | Reason |
| --- | --- |
| Goal Session | Confuses Task Session ownership with native Codex Goal runtime ownership. |
| Task Agent | Too broad and agent-specific; Task Session is runtime-neutral. |
| Context Cache | Suggests reuse as a durable source of truth rather than task-scoped evidence. |
