# Two-Lane Dialectic Discipline

Status: active-pattern
Steward: Research Tower, Refine, and Robot Talks

## Purpose

Govern investigative and design work so a proposal is adjudicated against a genuine opposite before it closes. Run two lanes in tension:

- **Lane Z — zig-zag (build the idea):** take the hypothesis as given and build it out by alternating generation and critique — generate a concrete version, attack it with its own strongest counterexample, adjust, repeat. Lane Z's job is not to defend the idea but to find where it actually holds and where it breaks under its own weight.
- **Lane A — alternatives (challenge the problem, not the idea):** hold the underlying problem fixed and propose a genuinely different solution. Lane A may not produce a variant of Lane Z's idea; it exists because the most expensive failure mode is anchoring — shipping the first framing because nobody was assigned to disagree with it.

Both lanes are measured against a one-sentence, solution-independent statement of the underlying problem. The work closes only on a synthesis that names what each lane actually solved versus only reframed, and issues an explicit bridge decision per claim.

## Boundary

This discipline names the two-lane adjudication practice. It does not execute the lanes, prove a claim by running them, or promote a synthesis into a template, validator, ontology, or runtime contract — promotion routes through the owning lifecycle (task-session for execution, definitions-governance for the bridge-decision vocabulary, constitution-governance for enforced artifact shape). It is the **dialectic** (opposed-lanes → synthesis) sense of "two-lane" only; the separate human-prose × machine-representation sense of the same phrase is the sibling [`two-lane-representation`](two-lane-representation.md) discipline and is not this one.

## Evidence

- [Refine improvement — Lane A reframing](../../arcana/refine/development/refine-improvement/research.md) - a live Lane A pass that holds the `/refine` problem fixed and reframes it against anchoring, citing the two-lane shape directly.
- [IntegrationSpec refine seed](../../arcana/integration-spec/development/refinement-runs/20260616T144535Z-integration-spec-refine/REFINE-SEED-PROPOSAL.md) - applies Lane Z (build the hypothesis through critique) and Lane A (challenge the framing, reject renamed variants) to a concrete target.
- [Research Tower](../../arcana/research-tower/README.md) - emits the synthesis, bridge decisions, and residue that close a two-lane tower.
- [Robot Talks](../../arcana/robot-talks/README.md) - runs parallel investigators in tension and synthesizes them into human-gated tensions: the multi-lane generalization of the same advocate-versus-opposite structure.
- [Discipline Catalog](../DISCIPLINES.md) - records `two-lane-dialectic` as an active-pattern discipline.

## Validation

- Mode: prose-review
- Check: `python3 disciplines/scripts/validate-discipline-catalog.py` for catalog row shape, plus card review that each lane pair is genuinely opposed (advocate versus alternative, not two variants of one idea) and that closure issues a bridge decision per claim.
- Latest result: pass

## Quality Bar

A useful two-lane dialectic entry must:

- state the underlying problem as one solution-independent sentence and measure both lanes against it, not against the hypothesis,
- keep the two lanes structurally opposed — one builds the idea into its own counterexample, one proposes a genuinely different solution; a lane that only restates a variant of the other is not a second lane,
- require at least one real counterexample in the build lane rather than a friendly demo,
- close only on a synthesis that names what each lane solved versus only reframed and issues a bridge decision per claim (`borrow-carefully`, `analogy-only`, `block`, `promotion-candidate`, or `future-work`) with residue and a named owner,
- keep bridge decisions local — promotion into a template, validator, ontology, or runtime contract is a separate approved route,
- add a third lane only when a distinct second alternative earns its own owner; otherwise fold it into Lane A as a named candidate.

## Promotion Guardrail

Discipline evidence can recommend a route, but it cannot directly promote registry, ontology, glossary, sigil, or spell knowledge. A synthesis's bridge decision is local until an owning lifecycle promotes it.
