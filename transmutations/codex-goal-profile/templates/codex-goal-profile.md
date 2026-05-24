# Codex Goal Profile: {unit-id}

## Source

| Field | Value |
| --- | --- |
| Work-pack | {path} |
| Parent task | {task id and link} |
| Selected SWU | {swu id and link} |
| Source contracts | {links} |
| Handoff pack | {session-evidence markdown path} |
| Handoff index | {session-evidence json/index path} |

## Readiness

| Check | Status | Evidence |
| --- | --- | --- |
| Dependencies satisfied | pass, flag, or block | {evidence} |
| Write scope bounded | pass, flag, or block | {paths} |
| Done criteria concrete | pass, flag, or block | {criteria} |
| Verification surface available | pass, flag, or block | {command or review evidence} |
| Handoff pack available | pass, flag, or block | {markdown path and JSON/index path} |
| Strict coverage passed | pass or block | {coverage summary} |
| Fallback exploration bounded | pass or block | {named gaps only} |
| Blockers clear | pass, flag, or block | {blocker state} |

## Native Codex Goal

```text
/goal {outcome}, verified by {verification surface}, while preserving {constraints}. Use the handoff pack at {handoff markdown path} and structured index at {handoff json/index path} as selected source context, plus only {allowed write scope}. Broaden repository exploration only for named gaps from the pack: {named gaps or none}. If you use extra sources, report the named gap, source path, and whether it changed the result. Between iterations, {iteration policy}. If blocked or no valid paths remain, stop with {blocked report shape}.
```

## Audit Notes

- Outcome: {what should be true}
- Verification surface: {test, command, report, artifact, benchmark, or review}
- Constraints: {what must remain true}
- Boundaries: {files, tools, repos, resources}
- Handoff pack: {markdown path and JSON/index path}
- Strict coverage: {pass or block}
- Fallback exploration: {none or named gaps only}
- Extra-source reporting: {required or n/a}
- Iteration policy: {how Codex chooses next action after each attempt}
- Blocked stop condition: {when to stop and what to report}
