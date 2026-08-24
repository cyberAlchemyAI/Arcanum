# Decision Gate

Decision Gate is an Arcana sigil for resolving blocker-level multi-option decisions before planning, implementation, document mutation, or other consequential changes continue.

It prevents an agent from silently choosing among viable options when the choice belongs to the user, project owner, or reviewer. The sigil identifies unresolved decisions, presents options with trade-offs, records the selected path, and returns a clear pass or block result.

## Problem It Solves

Agents often encounter choices that look small but shape the rest of the work: scope boundaries, persistence strategy, fallback behavior, rollout mode, verification level, ownership, naming, or policy strictness.

If those decisions are guessed, later work may be technically correct but aligned to the wrong assumption. Decision Gate solves this by making blocker decisions explicit before mutation happens.

## Use When

- a task has more than one viable path,
- a choice will affect future implementation, documentation, governance, cost, risk, or user experience,
- the agent cannot responsibly infer the user's preference,
- work should stop until a decision is made,
- a reusable decision record is needed.

## Do Not Use When

- the choice is purely local and reversible,
- the user already made the decision clearly,
- the task only needs factual lookup,
- the decision can be safely handled by a deterministic rule,
- asking would add delay without changing the outcome.

## Decision Model

Decision Gate uses a simple pass/block model:

- `PASS`: all blocker-level decisions are resolved and recorded.
- `BLOCK`: at least one blocker-level decision remains unresolved, so consequential mutation should not proceed.

Non-blocking choices can be recorded as assumptions or deferred decisions, but they must not be mixed with blocker decisions.

## Option Admissibility

Decision Gate asks for preference only after a deterministic prefilter. The
caller or owning validator supplies typed structural evidence for each action,
defer, or stop candidate. `scripts/prefilter-options.py` rejects structurally
inadmissible options and protected or irreversible options that lack a named
owner gate.

The remaining cardinality controls the route:

- zero admissible options returns structural `block`;
- one admissible option returns `direct` to that route or its owner gate;
- two or more admissible options returns `gate` and presents only those options.

`direct` is not consent or execution, and the prefilter never satisfies a
protected owner gate. Its machine contracts are
`schemas/option-admissibility-request.schema.json` and
`schemas/option-admissibility-receipt.schema.json`.

## Complexity-Calibrated Explanations

When the user selects “Explain / more context” or otherwise signals uncertainty,
Decision Gate routes the explanation through
[`complexity-example-ladder`](../../transmutations/complexity-example-ladder/).

The explanation must include low, medium, and complex examples. Complexity grows
through interacting concepts, dependencies, state, boundaries, consequences, and
exceptions—not through extra prose or jargon. Comparative examples reuse one shared
scenario per rung and cover every admissible action option evenly. The examples are
explanatory only: they do not change admissibility, recommendation, consent, owner
authority, or the gate result.

## Typed One-Use Overrides

Free-form approval is not an override. A reusable caller must supply a typed
artifact conforming to `schemas/override.schema.json`, then consume it for one
exact run with `scripts/consume-override.py`.

Consumption checks target, normalized scope, hazard, issuance, expiry, and
prior use. A valid non-protected override is updated under an exclusive lock so
`consumed_by` names the first consuming run before success returns. Stale,
mismatched, malformed, or replayed inputs block without rewriting the
artifact.

The generic consumer never admits destructive, authority, promotion,
publication, or spend hazards. Those always route to their owning gate. A
free-form owner-receipt path is not sufficient proof because Decision Gate
cannot invent another owner's receipt contract.

## Output

The sigil produces a decision record with:

- decision question,
- options considered,
- trade-offs,
- selected option,
- rationale,
- source of decision,
- timestamp,
- remaining blockers, if any.

## Why This Is Arcana

The sigil governs whether other work may proceed. It coordinates ambiguity, user choice, persistence, and stop/go authority across a task lifecycle. Its value is not just the decision artifact; it is the gate that prevents hidden assumptions from becoming implementation facts.
