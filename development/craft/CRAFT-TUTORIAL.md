# Craft Tutorial

## Who This Is For

This tutorial is for a reader who has not used Craft and does not yet know why a
project would need a Craft ledger. It uses the Guide package pattern:

1. Frame the thing being explained.
2. Inspect the context that already exists.
3. Explain in a useful order.
4. Ask for active understanding.
5. Record what should be remembered next.

## The Problem

AI-assisted projects lose state easily. A chat gets compacted. A task spans more
than one session. A decision is made in a review note but never appears in the
next plan. A blocker gets "resolved" because someone wants to keep moving, even
though no evidence was attached.

Craft exists for that moment. It gives the project a small, file-backed ledger
where important work state survives the conversation that produced it.

## The One-Sentence Version

Craft is a project-local ledger for nested work: contexts, artifacts, blockers,
decisions, gaps, evidence, next moves, and recomposition.

The ledger is not a chat transcript. It is not a dashboard. It is the source of
truth for what the project currently knows about its own work.

## The Mental Model

Think of Craft as a map of unfinished work.

- A context says where the work lives.
- An artifact says what file, receipt, handoff, or proof exists.
- A blocker says why motion is unsafe or impossible.
- A decision says what a human or governance route selected.
- A gap says what is still weak, missing, or deferred.
- A next move says what should happen after this point.
- Recomposition says how a child context changed its parent.

That last point matters. Craft is built for projects inside projects. A child
context can investigate a blocker, run a review, or create a proof. It is not
done until the parent ledger records what changed upstream.

## The Files

```text
.craft/
  ledger.yml        # source of truth
  index.json        # optional rebuildable lookup surface
  artifacts/        # receipts, handoffs, evidence, exports
CRAFT.md            # human-readable view derived from the ledger
```

`ledger.yml` owns the state. `CRAFT.md` helps humans read it. If they disagree,
the ledger wins.

## The Protocol

Use Craft when the work needs durable state:

1. Resolve the right Craft space.
2. Read the ledger before changing the project.
3. Add or update rows for real changes.
4. Keep blockers visible until evidence closes them.
5. Record decisions with question, selected option, rationale, impact, and evidence.
6. Recompose child contexts into the parent before calling them done.
7. Export or refresh `CRAFT.md` as a view, not as authority.

Do not use Craft for every tiny edit. Use it when the project state itself needs
memory.

## A Small Example

A product launch has an API boundary question and missing pilot evidence.

Craft records:

- `CTX-PRODUCT-LAUNCH-ROOT`: the launch readiness context.
- `CTX-PRODUCT-LAUNCH-API-REVIEW`: a child context for the API review.
- `DEC-API-BOUNDARY-001`: the selected API boundary.
- `BLK-PILOT-EVIDENCE-001`: the active blocker that prevents readiness.
- `GAP-SEED-DATA-001`: fixture data has not been checked against a pilot run.
- `ART-API-REVIEW-RECEIPT`: evidence that the child review happened.

The API review can close, but the launch root remains flagged. That is the
point: Craft lets one part of the work pass without pretending the whole project
is ready.

See the public-safe fixtures:

- `../../arcana/craft/examples/product-launch-ledger.yml`
- `../../arcana/craft/examples/product-launch-CRAFT.md`
- `../../arcana/craft/examples/platform-governance-ledger.yml`
- `../../arcana/craft/examples/platform-governance-CRAFT.md`

## Blockers, Lanes, and Roles

A blocker is not just a red flag. In Craft, a good blocker says:

- what kind of condition blocks motion,
- which part of the work raised it,
- which part of the work cannot safely move,
- which responsibility lane owns the next move,
- which local role or route may handle it,
- what evidence would prove it closed.

That gives a blocker a shape instead of a mood.

```yaml
item_id: BLK-PILOT-EVIDENCE-001
kind: blocker
base_type: evidence_blocker
primary_lane: validator
secondary_lanes:
  - product
status: active
refinement_status: refined
default_role: evidence_reviewer
allowed_roles:
  - evidence_reviewer
  - validator
delegation_route: task-session
requires_human: false
role_confidence: candidate
closure_condition: A pilot run produces a receipt that satisfies the launch evidence checklist.
evidence: ART-PILOT-EVIDENCE-PLAN
decision_ref: none
reason: Launch readiness cannot pass until at least one pilot evidence receipt exists.
```

The important distinction:

| Thing | Meaning | Example |
| --- | --- | --- |
| Blocker type | Why motion is blocked. | `evidence_blocker` |
| Lane | What kind of responsibility is needed. | `validator` |
| Role | The local handler that may take that responsibility. | `evidence_reviewer` |
| Route | The workflow that may produce evidence. | `task-session` |
| Closure condition | What must be true before the row can close. | A receipt satisfies the checklist. |

Role fields are suggestions until a decision, owner policy, route contract, or
receipt backs them. A lane says "this is validation responsibility." A role says
"in this project, the evidence reviewer may handle validation." A route says
"this workflow is a reasonable way to produce the proof."

A raw blocker cannot close directly. First it must become typed and refined, or
a human/governance decision must explicitly waive it.

## What Craft Protects

Craft protects three boundaries.

First, it separates evidence from confidence. A row should say why it can be
trusted.

Second, it separates child progress from parent readiness. A child context can
pass while the parent still has residue.

Third, it separates human-readable views from machine authority. `CRAFT.md` is
for orientation. `ledger.yml` is the source.

## Common Mistakes

| Mistake | Consequence | Better Move |
| --- | --- | --- |
| Closing a raw blocker directly. | False closure. | Refine it first; attach evidence or a waiver decision. |
| Treating dispatch validation as execution proof. | Route shape gets confused with work done. | Record dispatch as route evidence only. |
| Updating `CRAFT.md` but not `ledger.yml`. | Human view drifts from authority. | Update the ledger, then refresh the view. |
| Making one root ledger own every subproject. | Scoped blockers become invisible. | Resolve the owning Craft space first. |
| Leaving a child context closed but unrecomposed. | The parent never learns what changed. | Add recomposition evidence and parent next move. |

## The First Run

For a new project, start small:

1. Create one root context.
2. Add one description.
3. Add one candidate definition.
4. Add one blocker.
5. Open one child context to refine that blocker.
6. Close one decision.
7. Add one gap.
8. Set the next move.
9. Recompose the child context into the parent.
10. Validate the ledger.
11. Export `CRAFT.md`.

If that feels like too much, Craft is probably too heavy for the task. If that
feels like exactly the information you keep losing, Craft is the right tool.

## Teach-Back Check

Before using Craft, answer these in your own words:

1. What is the source of truth: `ledger.yml` or `CRAFT.md`?
2. What must happen before a raw blocker can close?
3. Why can a child context pass while the parent stays flagged?
4. What evidence proves the next move is allowed?

If those answers are clear, you are ready to read or operate a Craft ledger.
