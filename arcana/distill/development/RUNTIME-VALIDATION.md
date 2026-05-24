# Runtime Validation: Distill

Status: pass for local command resolution.

Updated: 2026-05-20

## Scope

Validate that Distill can be invoked through the local Arcanum command surface without weakening the manual package contract.

## Runtime Role Policy

B-CLO-001 is resolved:

- use true subagents when the active runtime supports them,
- use labeled Proposer/Balancer role simulation when subagents are unavailable,
- preserve the same Role Trace Contract in both paths.

The Codex command adapter records this policy and points to the canonical README/SKILL instead of duplicating the sigil internals.

## Adapter Files

| File | Purpose |
| --- | --- |
| `.codex/commands/distill.md` | Slash-style local command route for `/distill`. |
| `.codex/commands/arcanum-sigil-distill.md` | Arcanum-prefixed alias route. |

## Representative Resolution Check

Expected command:

```bash
tools/arcanum --resolve /distill
```

Expected result:

```text
COMMAND=distill
COMMAND_FILE=.codex/commands/distill.md
```

## Representative Run Review

The adapter preserves:

- canonical README/SKILL source links,
- subagent-first role policy,
- role simulation fallback,
- finite recursion and budget confirmation,
- technique trace requirements,
- output contract,
- navigable result closeout,
- observability closeout status.

Runtime behavior should be compared against [examples/standard-pass.md](examples/standard-pass.md) for the first live run.

## Verdict

pass.

The runtime adapter may be used for local representative invocation after validation examples pass. Registry promotion remains blocked by final B-CLO-002 approval.
