# Tier Classification

## Candidate

- Target name: github-project-issue-loop
- Source: GitHub Projects issue delivery loop, including issue selection, assignment, refine, invoke, task-session, PR publication, and board sync.

## Tier Fit

| Tier | Fit | Rationale |
| --- | --- | --- |
| Formulae | low | The workflow has deterministic checks, but success depends on contextual issue selection, repository evidence, lifecycle routing, and validation judgment. |
| Transmutations | medium | The workflow transforms a ticket into refined context and artifacts, but it also claims external state, executes implementation, opens PRs, and syncs boards. |
| Arcana | high | The workflow coordinates external project state, repository context, lifecycle sigils, implementation, validation, PR publication, telemetry, and reflection gates. |

## Decision

- Selected tier: arcana
- Rejected tiers: formulae, transmutations
- Notes: Use Formulae helpers for deterministic GitHub/project validation and Transmutation helpers for context synthesis inside the larger Arcana loop.
