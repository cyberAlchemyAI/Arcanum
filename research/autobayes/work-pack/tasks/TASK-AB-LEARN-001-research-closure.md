---
profile: autobayes-research
name: TASK-AB-LEARN-001 - Research Closure
description: Selected SWU for closing the remaining AutoBayes learning research.
type: work-pack-task
task_id: TASK-AB-LEARN-001
swu_id: SWU-AB-LEARN-001
status: completed
last_updated: 2026-06-07
---

# TASK-AB-LEARN-001 - Research Closure

## Objective

Close the remaining AutoBayes research tower into a final source-backed learning pack that the Arcanum developer can use without rereading the whole paper every time.

The result must preserve source language first, translate into Arcanum language second, and leave explicit residue where the paper or related literature is still unresolved.

## Write Scope

Primary write scope:

- `research/autobayes/`
- `research/autobayes/tracks/`
- `research/autobayes/residue/`
- `research/autobayes/levels/`
- `research/autobayes/work-pack/`
- `research/autobayes/development/refinement-runs/20260607T070805Z-research-closure-plan/`

Do not mutate canonical Arcanum source, registries, ontology, inventory, sigils, spells, runtime contracts, or generated global skill surfaces during this research closure task.

## Required Closure Objects

Produce or update these local research objects:

1. `tracks/paper-claim-ledger.md`
2. `tracks/bayesian-lens-definition-card.md`
3. `tracks/parameter-exposure-card.md`
4. `tracks/cups-caps-boundary-shift-card.md`
5. `tracks/two-step-symbolic-loss-calculation.md`
6. `tracks/implementation-residue-note.md`
7. final updates to `GLOSSARY.md`, `DEFINITIONS.md`, `DISTILLED-KNOWLEDGE.md`, `NEXT.md`, and `residue/open-residue.md`
8. optional final synthesis artifact `FINAL-LEARNING-PACK.md`

## Done Criteria

- Every major paper layer has a source-backed claim ledger entry: model syntax, inversion, local loss, parameter exposure, optimization semantics, and examples.
- Each open residue item AB.1 through AB.7 is either closed, promoted into a sharper local research object, or left open with an explicit reason.
- The local glossary and definitions distinguish paper source meaning, Arcanum reading, misuse warning, and promotion status.
- The distilled knowledge can be used by the Arcanum developer as an operator-facing model without rereading the paper.
- Any `borrow-now` bridge item becomes only a proposed Arcanum work-pack candidate, never a canonical mutation.
- Subagent execution, if used, records a lifecycle ledger with no hidden open agents.
- Extra sources outside the handoff pack are reported with the named gap they addressed and whether they changed the result.

## Validation Surface

Run:

```bash
formulae/dispatch-spec/scripts/validate-dispatch.py research/autobayes/development/refinement-runs/20260607T070805Z-research-closure-plan/REFINE-DISPATCH.json --json
```

Then perform read-back checks over the final research artifacts:

```bash
rg -n "source kind|promotion_scope|Status:|closed-|open-question|Arcanum reading|Misuse|Do not promote" research/autobayes
```

If subagents are spawned, also report the subagent lifecycle ledger and block success if any spawned agent is pending, hidden, unjoined, or unclosed.

## Blockers

Block if:

- the handoff Markdown or JSON index is missing;
- the AutoBayes paper or already-recorded source receipts cannot support a claim being closed;
- the task would require canonical Arcanum mutation instead of local research output;
- subagent lifecycle closeout is incomplete;
- extra external sources are used without naming the source gap they answer.

## Completion Evidence

- Final learning pack: `research/autobayes/FINAL-LEARNING-PACK.md`.
- Required closure objects created under `research/autobayes/tracks/`.
- Shared surfaces updated: `GLOSSARY.md`, `DEFINITIONS.md`, `DISTILLED-KNOWLEDGE.md`, `NEXT.md`, and `residue/open-residue.md`.
- Dispatch validation returned `validation=pass`.
- Read-back validation found source-kind, promotion-scope, status, Arcanum-reading, misuse, and no-promotion markers across the tower.
- Subagents were not spawned during this parent-lane closure run; subagent closeout is `n/a`.
