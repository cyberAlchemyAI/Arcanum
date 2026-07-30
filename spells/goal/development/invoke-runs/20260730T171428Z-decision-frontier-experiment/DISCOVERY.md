# Discovery: Decision Frontier Experiment

## Question

Can a decision-discovery DAG improve how Invoke, Craft, and Goal expose the
next meaningful decision without turning the DAG into a second execution
authority?

## External Source

The source pattern is Matt Pocock's Wayfinder skill, inspected at immutable
commit
[`2ab958093e83e0ec752e6c1c5932da465bf23e0c`](https://github.com/mattpocock/skills/blob/2ab958093e83e0ec752e6c1c5932da465bf23e0c/skills/engineering/wayfinder/SKILL.md).
Its license at that commit is MIT.

The useful mechanism is a decision-discovery graph:

- work backward from a destination into discrete decisions;
- express dependency edges between those decisions;
- distinguish precise tickets, fog, and explicit out-of-scope items;
- expose an unblocked and unclaimed frontier;
- claim before resolving;
- reconcile downstream nodes after a decision changes the graph;
- stop when the way is clear, not when implementation is complete.

This package adapts the mechanism rather than importing the upstream skill.

## Live Repository Tension

| Surface | Current live behavior | Experimental pressure |
| --- | --- | --- |
| Invoke | authors Define, Design, and Plan artifacts | ambiguity should become an explicit decision map before planning |
| Craft | owns the durable project ledger and already represents decisions and dependency relations | a tracker or Goal projection must not become competing authority |
| Goal | consumes a supplied frontier and selects the first routable node | frontier eligibility should be derived and explainable |
| Task Session | executes one selected bounded task or SWU | decision closure must not masquerade as task completion |

## Hypothesis

A cross-capability decision-frontier protocol can make planning more
deterministic if:

1. Invoke authors or refreshes a decision map when ambiguity is material;
2. Craft remains the source authority for accepted decision state;
3. Goal derives a read-only eligibility projection, claims one decision with
   digest binding, and stages reconciliation proposals;
4. Task Session remains the only execution route for a selected implementation
   unit.

## Smallest Safe Experiment

Use synthetic fixtures and a pure reducer under Goal development. Do not touch
canonical schemas or runtimes. Prove frontier computation, claim semantics,
fog/out-of-scope exclusion, reconciliation, deterministic replay, and the
decision-versus-execution boundary.

## Discovery Verdict

- concept fit: pass;
- implementation evidence: absent;
- canonical adoption: not authorized;
- next route: Invoke Define, Design, and Plan for Spellcraft review.

