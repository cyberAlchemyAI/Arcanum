# Goal Spell Local Definitions

Status: draft local glossary
Canonical source for Arcanum-wide promoted terms:
`arcanum/definitions/DEFINITIONS.md`

## Authority Rule

This file defines local spell vocabulary for the `goal` package. Terms marked
with `DEF-ARC-*` are promoted to the Arcanum-wide canonical definitions source;
this file explains their goal-spell use without overriding that authority.

## DEF-ARC-GOAL-SPELL: Goal Spell

Status: promoted
Term: goal spell

### Scientific/Formal Voice

An Arcanum spell that routes a bounded goal over a governed work graph through
frontier reading, risk classification, owner and technique selection, delegated
execution, audit, staged delta proposal, and approval-gated promotion.

### Plain-Language Voice

A goal spell is the conductor for a goal: it decides what can run, who should do
it, when to stop, and what must be approved before source truth changes.

### Domain Context

In `arcanum/spells/goal`, the goal spell is the draft reusable spell described
by `README.md` and specified by this Invoke run. It composes existing
capabilities instead of replacing them.

## DEF-ARC-STAGED-DELTA: Staged Delta

Status: promoted
Term: staged delta

### Scientific/Formal Voice

A proposed change to an authoritative source that records target, operation,
framed diff, validation expectation, and promotion state before any active
source-of-truth mutation is applied.

### Plain-Language Voice

A staged delta is a held change: visible, reviewable, and not yet applied.

### Domain Context

In `arcanum/spells/goal`, staged deltas are how accepted node progress waits for
approval before Craft ledger mutation.

## DEF-ARC-APPROVAL-TOKEN: Approval Token

Status: promoted
Term: approval token

### Scientific/Formal Voice

An explicit authorization artifact that binds an approver, a reviewed batch or
operation, a decision record, and an approval state before a protected mutation
may execute.

### Plain-Language Voice

An approval token is the clear "yes for this exact batch" that lets a protected
change move from proposal to apply.

### Domain Context

In `arcanum/spells/goal`, the approval token controls batch promotion and must
link to durable decision evidence before staged deltas can apply.

## GOAL-DEF-FRONTIER: Craft Frontier

Status: local
Term: Craft frontier

### Scientific/Formal Voice

The current set of open next moves, blockers, gaps, and candidate SWUs read
from a Craft scope for one goal-loop round.

### Plain-Language Voice

The frontier is the work the goal spell can see right now.

### Domain Context

The goal spell reads the frontier before risk classification. The snapshot is a
handoff artifact for the round and not a replacement for the Craft ledger.

## GOAL-DEF-RISK-TIER: Risk Tier

Status: local
Term: risk tier

### Scientific/Formal Voice

A per-node classification used to decide whether work may route autonomously or
must stop for explicit approval. Unknown risk resolves to the protected tier.

### Plain-Language Voice

Risk tier is the spell's traffic light for a node.

### Domain Context

The goal spell uses risk tiers to separate read-only or staged-proposal work
from mutation, publication, shell, network, commit, push, and promotion work.

## GOAL-DEF-DISPATCH-ROUTE: Dispatch Route

Status: local
Term: dispatch route

### Scientific/Formal Voice

A validated route that names the owner capability, selected technique, inputs,
expected receipt, gates, and fallback behavior for one frontier node.

### Plain-Language Voice

A dispatch route says who should handle the node and what proof they must bring
back.

### Domain Context

The goal spell assembles dispatch routes but relies on `formulae/dispatch-spec`
for route-shape validation.

## GOAL-DEF-EXECUTION-RECEIPT: Execution Receipt

Status: local
Term: execution receipt

### Scientific/Formal Voice

A terminal evidence record returned by a delegated owner, including status,
scope, changed files when applicable, validation, residue, and reroute
information.

### Plain-Language Voice

An execution receipt is the proof that a delegated lane ended cleanly or
reported exactly why it could not.

### Domain Context

The goal spell cannot audit or close a node until every delegated lane has a
terminal receipt.

## GOAL-DEF-DECISION-PROFILE: Decision Profile

Status: local
Term: decision profile

### Scientific/Formal Voice

An optional runtime policy object, shaped by `decision-profile.schema`, that
parameterizes risk defaults, approval behavior, slice size, owner boundaries,
gap-filling behavior, technique weights, and anti-pattern stops.

### Plain-Language Voice

A decision profile tunes how cautious or narrow the goal spell should be.

### Domain Context

The public goal spell ships only the schema and neutral defaults. Filled
profiles belong to consuming repositories and stay outside the public package.

## GOAL-DEF-GAP-DISCOVERY: Gap Discovery

Status: local
Term: gap discovery

### Scientific/Formal Voice

An optional, bounded module that runs after the active frontier is empty, mines
residue and evidence for untracked work, dedupes by `(kind, target)`, and queues
new proposals without reopening the active frontier directly.

### Plain-Language Voice

Gap discovery looks for missed work only after current work is dry, then queues
it politely.

### Domain Context

The goal spell uses gap discovery only within a configured budget and keeps its
output as proposed next slices.

## GOAL-DEF-PROPORTIONALITY-GUARD: Proportionality Guard

Status: local
Term: proportionality guard

### Scientific/Formal Voice

A budget and technique-selection guard that tracks turn, token, spawn, and
no-progress limits, down-routes overbuilt techniques, and stops before the
ceiling is exceeded.

### Plain-Language Voice

The proportionality guard keeps the spell from using a heavy tool for a light
job or running past the budget.

### Domain Context

The goal spell records down-routes and stop reasons through this guard, but
promotion still requires separate reusable-behavior validation.
