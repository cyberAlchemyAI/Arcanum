# Session Handoff Template Family

Use this family when `invoke handoff` prepares a new session or thread from an existing session reference.

## Selection Rules

1. Select `session-handoff` when the requested output is a new thread/session artifact, continuation prompt, reflection packet, research direction, or lifecycle split from current session context.
2. Require both a new-session prompt and a source session reference.
3. Use Context Builder to select obligation-linked context from the referenced session.
4. Preserve the handoff type and route rationale instead of flattening all handoffs into generic summaries.
5. Route lifecycle work to the owning capability; this template creates the handoff, not the downstream lifecycle result.

## Templates

| Template | Purpose |
| --- | --- |
| [session-handoff.md](session-handoff.md) | Session/thread handoff artifact contract. |
| [examples/passing.md](examples/passing.md) | Minimal passing session handoff example. |
| [examples/missing-input.md](examples/missing-input.md) | Missing-input negative example. |

## Gates

- New-session prompt is required.
- Source session reference is required.
- Handoff type must be explicit or selected with rationale.
- Context Builder coverage must be reported.
- Execution continuations require strict obligation coverage before routing to `task-session` or runtime-goal handoff.
- The artifact must not pretend to open the thread automatically; it prepares the prompt and context for the new thread.

## Validation

Run link validation for this directory after edits:

```bash
./tools/check_markdown_links.sh arcanum/spells/invoke/templates/session-handoff/README.md
./tools/check_markdown_links.sh arcanum/spells/invoke/templates/session-handoff/session-handoff.md
./tools/check_markdown_links.sh arcanum/spells/invoke/templates/session-handoff/examples/passing.md
./tools/check_markdown_links.sh arcanum/spells/invoke/templates/session-handoff/examples/missing-input.md
```
