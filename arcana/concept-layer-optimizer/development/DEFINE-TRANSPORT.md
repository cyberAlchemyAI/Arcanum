# Invoke Define Transport: Concept Layer Optimizer

## Observer Envelope

- run_id: arcanum-invoke-20260519T094802Z
- capability.id: invoke
- capability.kind: spell
- capability.tier: spell
- capability.mode: command
- target_artifact: arcana/concept-layer-optimizer/development/SIGIL-HANDOFF.md
- request summary: define a new sigil that recursively decomposes models, architectures, designs, or plans into coherent concept layers, balances smallest useful unit against context size, and supports proposer/balancer multi-agent conversations.
- expected outputs: sigil-development handoff, glossary, implementation-layering seed, define transport report.

## Bounded Define Context

The requested sigil is a planning optimizer, not an implementation executor. It should help a user reason before committing to a solution by recursively reducing a seed idea into meaningful concept units and selecting the smallest coherent unit that still fits the user's target context.

The sigil needs explicit safeguards against:

- premature complexity,
- premature optimization,
- infinite reduction,
- concept cycling,
- multiple agents arguing without convergence,
- proposals that cannot recompose into the upper layer.

## Template Selection Evidence

- Selected template family: invoke.sigil
- Template path: spells/invoke/templates/sigil/sigil.md
- Eligibility: the target artifact is a reusable sigil with interaction contract, runtime adapter expectations, observability needs, and sigil-development handoff.
- Tie cases: none. Spell and generic templates were not selected because the target is a single sigil, not a multi-sigil workflow or untyped artifact.
- Candidate status: the sigil template family is invoke-local candidate coverage; lifecycle execution remains with sigil-development.

## Decisions

- Proposed canonical id: concept-layer-optimizer.
- Proposed tier: Arcana, because the behavior is interactive, recursive, multi-role, and human-gated.
- Default budget: Standard.
- Default role configuration: one Proposer and one Balancer.
- Default recursive rounds: two.
- Multi-solution comparison: available through Tournament mode.
- Complexity balance must include an evolution-profile check so natural extensibility is not mistaken for speculative overbuilding.
- Literature-backed techniques were promoted into a Technique Pack contract with always-on gates, Balancer checks, conditional techniques, classifiers, and tournament mechanics.
- Later CyberAlchemy method review added objective-output artifact confirmation as a setup requirement so the optimizer can keep the final product visible while still allowing discovery to revise it.
- Later CyberAlchemy method review added navigable result check as a closeout requirement so dense concept maps remain usable by humans and future agents.
- Robot-Talks route: optional handoff when unresolved tensions span layers and need independent investigation.
- Decision-Gate route: optional handoff when a blocker decision prevents optimization-point selection.

## Outputs

- Sigil handoff: arcana/concept-layer-optimizer/development/SIGIL-HANDOFF.md
- Glossary: arcana/concept-layer-optimizer/development/GLOSSARY.md
- Implementation layering seed: arcana/concept-layer-optimizer/development/IMPLEMENTATION-LAYERING-SEED.md
- Define transport report: arcana/concept-layer-optimizer/development/DEFINE-TRANSPORT.md
- Literature research addendum: arcana/concept-layer-optimizer/development/LITERATURE-RESEARCH.md
- Interrogation review: arcana/concept-layer-optimizer/development/INTERROGATION-REVIEW.md
- Design-stage surface architecture: arcana/concept-layer-optimizer/development/MODE-TECHNIQUE-SURFACE-DESIGN.md
- Detailed technique specifications: arcana/concept-layer-optimizer/development/techniques/README.md
- Design-stage glossary consistency: arcana/concept-layer-optimizer/development/SURFACE-GLOSSARY-CONSISTENCY.md
- Design-stage transport report: arcana/concept-layer-optimizer/development/SURFACE-DESIGN-TRANSPORT.md
- Design continuation review: arcana/concept-layer-optimizer/development/DESIGN-CONTINUATION-REVIEW.md

## Glossary Linking

- linked: Robot-Talks handoff, Decision-Gate handoff.
- partial: target context, smallest coherent unit, proposer, balancer, tension ledger, premature complexity, requisite variety check, boundary-object check.
- no-match: seed point, concept layer, concept unit, closed system, optimization point, role conversation trace, stable disagreement, proposal track, recursive round, composition model, evolution profile, open-endedness, technique pack, abstraction-level guard, recomposition proof, frame-expiry note, cognitive load check, concept-vs-knowledge status, premortem pass, set-based tournament, hidden glue, brittle minimalism, cycle guard, pitch-off.

Candidate glossary promotion is not automatic and was not performed.

## Governance

- No upstream registry mutation was performed.
- No canonical glossary or Necronomicon term promotion was performed.
- Sigil-development owns lifecycle execution and promotion.
- Registry update should wait until README.md, SKILL.md, validation examples, and approval exist.

## Unresolved Gaps

- Non-blocking: final name can be changed during sigil-development.
- Non-blocking: exact budget labels can be refined after first validation examples.
- Non-blocking: runtime adapter must implement the resolved policy: true subagents when supported, role simulation fallback when unavailable.
- Non-blocking: README.md, SKILL.md, command adapter, and validation fixtures still need to be authored through sigil-development.
- Non-blocking: validation examples should include objective-output artifact drift and navigation-guide downgrade cases.

## Recommended Next Route

sigil-development

Use sigil-development to turn the handoff into the candidate sigil package, then validate examples before registry promotion.
