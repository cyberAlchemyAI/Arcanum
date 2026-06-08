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