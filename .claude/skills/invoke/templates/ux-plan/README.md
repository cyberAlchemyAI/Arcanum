# UX-Plan Template Family

Use this family when invoke needs experience planning for users, workflows, screens, surfaces, states, content, accessibility, or interaction risk.

## Selection Rules

1. Select `ux-plan` when the request is about user experience or workflow behavior rather than implementation delivery.
2. Keep UX planning separate from implementation; route delivery work to architecture or implementation-plan after the experience contract is stable.
3. Block only when target users or workflow scope are unknown and cannot be inferred from evidence.

## Templates

| Template | Purpose |
| --- | --- |
| [ux-plan.md](ux-plan.md) | Experience planning contract. |
| [examples/passing.md](examples/passing.md) | Minimal passing UX-plan example. |
| [examples/missing-input.md](examples/missing-input.md) | Missing-input negative example. |

## Gates

- User goals and workflow scope are required.
- Surface and state assumptions must be explicit.
- Accessibility considerations must be recorded before handoff.

## Validation

```bash
./tools/check_markdown_links.sh arcanum/spells/invoke/templates/ux-plan/README.md
./tools/check_markdown_links.sh arcanum/spells/invoke/templates/ux-plan/ux-plan.md
./tools/check_markdown_links.sh arcanum/spells/invoke/templates/ux-plan/examples/passing.md
./tools/check_markdown_links.sh arcanum/spells/invoke/templates/ux-plan/examples/missing-input.md
```