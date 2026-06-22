# Codex Goal Profile: {unit-id}

## Source

| Field | Value |
| --- | --- |
| Work-pack | {path} |
| Parent task | {task id and link} |
| Selected SWU | {swu id and link} |
| One-shot stream | {stream id and ordered units, or n/a} |
| Source contracts | {links} |
| Handoff pack | {session-evidence markdown path} |
| Handoff index | {session-evidence json/index path} |
| Decision profile | {runtime-private profile path or n/a} |
| Sidecar profile | {sidecar/handoff profile path or n/a} |

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
| Goal budget | pass or block | {character limit and measured/estimated length} |
| One-shot capability policy | pass, flag, or block | {allowed sigils/subagents and receipt gates} |

## Native Codex Goal

```text
/goal {compact outcome}, verified by {verification surface}. Use {sidecar or handoff pack path} as the execution frame and stay within {allowed write scope}. Capability lanes: {allowed sigils/subagents or none}. Broaden only for named gaps: {named gaps or none}. Between iterations, {iteration policy}. Stop with {blocked report shape}.
```

## Audit Notes

- Outcome: {what should be true}
- Verification surface: {test, command, report, artifact, benchmark, or review}
- Constraints: {what must remain true}
- Boundaries: {files, tools, repos, resources}
- Handoff pack: {markdown path and JSON/index path}
- Strict coverage: {pass or block}
- Goal budget: {limit, measured length, pass or block}
- Decision profile: {path or n/a; consumed policy fields or n/a}
- One-shot mode: {yes or no}
- Capability policy: {allowed sigils/subagents and receipt gates or none}
- Sidecar profile: {path or n/a}
- Fallback exploration: {none or named gaps only}
- Extra-source reporting: {required or n/a}
- Iteration policy: {how Codex chooses next action after each attempt}
- Blocked stop condition: {when to stop and what to report}
