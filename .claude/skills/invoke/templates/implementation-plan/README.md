# Retired Implementation-Plan Template Family

This family is retained only as historical scaffolding for older validation fixtures. Active invoke planning no longer selects or emits an `IMPLEMENTATION-PLAN.md` artifact.

The active plan surface is:

```text
IMPLEMENTATION-LAYERING.md
WORK-PACK.md
  -> work-pack/waves/W*.md
  -> work-pack/tasks/TASK-*.md
  -> SWUs
```

## Selection Rules

1. Do not select this family for new invoke plan work.
2. Use [../implementation-layering.md](../implementation-layering.md) for layer governance.
3. Use [../work-pack.md](../work-pack.md) for executable planning, state, waves, tasks, and SWUs.
4. Use [../module-formulae/execution-pack.md](../module-formulae/execution-pack.md) when the plan needs wave execution packaging.

## Templates

| Template | Purpose |
| --- | --- |
| [implementation-plan.md](implementation-plan.md) | Retired implementation-plan contract retained for historical reference. |
| [examples/passing.md](examples/passing.md) | Historical passing implementation-plan example. |
| [examples/missing-input.md](examples/missing-input.md) | Historical missing-input negative example. |

## Gates

- Block new plan, full, and validate flows if they attempt to select this retired family as an active output.
- Route planning work to implementation-layering and work-pack instead.

## Validation

```bash
./tools/check_markdown_links.sh arcanum/spells/invoke/templates/implementation-plan/README.md
./tools/check_markdown_links.sh arcanum/spells/invoke/templates/implementation-plan/implementation-plan.md
./tools/check_markdown_links.sh arcanum/spells/invoke/templates/implementation-plan/examples/passing.md
./tools/check_markdown_links.sh arcanum/spells/invoke/templates/implementation-plan/examples/missing-input.md
```
