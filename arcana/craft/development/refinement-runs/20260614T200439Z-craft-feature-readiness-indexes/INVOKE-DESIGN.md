# Invoke Design: Craft Feature Readiness Indexes

## Design Identity

- Spell: `invoke`
- Mode: `design`
- Target artifact: Craft execution-readiness index update.
- Target owner: `arcana/craft` lifecycle owner.
- Source mode: discovery-mode design from approved local evidence.
- Phase status: `pass`
- Next route: `plan`

## Context View

Craft currently owns project-local recursive ledgers with source authority in `.craft/ledger.yml`, a human view in `CRAFT.md`, and optional generated indexes. The active contract already requires IDs, links, current next moves, active blockers, decisions, gaps, artifacts, and pending-by-node status.

Observed workflow pressure comes from handoffs among Refine strategy proposals, Invoke work-packs, Craft status, and later execution. A ledger may know the next move but not expose whether the move is executable, which SWU is ready, which approval applies, or which scopes remain blocked.

## High-Level Structure View

Add one optional readiness layer to the existing Craft model:

1. Source rows keep owning the facts: contexts, artifacts, typed items, decisions, and gaps.
2. `indexes.execution_readiness` derives lookup handles from those rows.
3. `state all` and exported `CRAFT.md` render the readiness handles when present.
4. Task execution remains owned by `task-session`, `sigil-development`, or another lifecycle owner.

This is an additive extension, not a replacement for current indexes.

## Low-Level Components View

| Component | Owner | Change |
| --- | --- | --- |
| Ledger schema | `arcana/craft/templates/ledger.schema.yml` | Add optional readiness index contract and validation notes. |
| Skill contract | `arcana/craft/SKILL.md` | Extend linking/indexing and all-status output to mention readiness handles. |
| README | `arcana/craft/README.md` | Summarize readiness indexing without making Craft an executor. |
| Examples | `arcana/craft/examples/` | Add public-safe readiness sample data where a work-pack exists or use a small synthetic fixture. |
| Generated surfaces | `.agents/skills/craft`, `.claude/skills/craft`, other runtime packages | Regenerate from canonical sources after approval. |
| Validation | YAML parse, schema review, grep checks, diff check | Prove additive compatibility and public boundary safety. |

## Workflow Process View

1. A plan or work-pack is authored by Invoke.
2. A Craft ledger records that work-pack as an artifact and sets a next move.
3. The optional readiness index points to the executable artifact, ready SWU IDs, approval record, execution mode, and blocked scopes.
4. `craft state all` reports pending work plus execution readiness.
5. A future executor selects one SWU and produces a receipt.
6. Craft records receipt evidence and updates readiness indexes, but does not execute the work itself.

## Decision Flow View

| Decision | Selection | Rationale |
| --- | --- | --- |
| Additive index vs required row family | Additive index | Existing ledgers remain valid and only execution-planned scopes need the fields. |
| Store readiness in index vs separate artifact | Index plus row links | Craft state should remain navigable without turning work-packs into ledger roots. |
| Include approvals | Yes | Approval scope determines what may run and what remains blocked. |
| Include product worktree | Yes, optional | Some Craft spaces coordinate a workspace while product mutation happens in a nested worktree. |
| Include blocked publication scopes | Yes, optional | Local/static work can be approved while commit, push, PR, or CI promotion remain blocked. |
| Mutate Invoke/Refine now | No | This work-pack targets Craft only; cross-sigil changes remain separate owner routes. |

## Dependency Interface View

- Upstream input: Invoke work-pack fields such as gate status, ready SWUs, owner route, execution mode, and approval record.
- Craft interface: ledger rows and indexes, plus `CRAFT.md` export/status output.
- Downstream interface: Task Session or Sigil Development selects one SWU and returns receipt evidence.
- Boundary: readiness indexes must not claim execution proof. They point to artifacts, approvals, gates, and blocked scopes.

## Risks

- Overreach: adding execution fields could make Craft look like an executor. Mitigation: skill text and README must state that Craft records readiness only.
- Privacy leak: examples could copy private workspace details into public `arcanum`. Mitigation: use public-safe examples or synthetic values.
- Index drift: derived readiness indexes could contradict source rows. Mitigation: validation requires indexes to point back to row IDs or paths.
- Status noise: all-status output could become too verbose. Mitigation: render a compact readiness block only when fields exist.

## Handoff To Plan

Plan mode should create a medium-complexity split work-pack with L0-L3 layers, task-local SWUs, public-boundary validation, and generated-surface synchronization as the final layer.
