---
title: The Ontology That Lets Agents Learn Without Pretending Telemetry Is Truth
status: final-candidate
task: CAOL-009
route: article-synthesis
createdAt: 2026-05-23
updatedAt: 2026-05-24
---

# The Ontology That Lets Agents Learn Without Pretending Telemetry Is Truth

Software teams do not only lose knowledge because they forget to write things down. They lose knowledge because meaning keeps changing form.

An intention becomes a specification. A specification becomes code. Code becomes runtime behavior. Runtime behavior becomes logs, tests, failures, route choices, corrections, and small operational lessons. Some of those lessons matter. Most should not become rules.

That is the problem CyberAlchemy is trying to solve.

The goal is not to build a giant memory for agents. Memory is too soft for that. The goal is to build a governed path from observation to knowledge, where an agentic development system can learn from its work without pretending that every trace, failure, or success is automatically true.

The simplest version is this:

```text
observe work
  -> preserve evidence
  -> propose a knowledge change
  -> review confidence and scope
  -> promote, defer, reject, contradict, or retire
```

The hard part is that middle step: propose a knowledge change.

CyberAlchemy calls the central object a `PromotionRecord`.

It is the thing that keeps agent learning honest.

## Why Agents Need More Than Memory

Agentic systems are getting better at observing themselves. They can record tool calls, workflow routes, validation results, terminal states, generated files, failures, retries, and reflection notes. That is useful.

But a trace does not know what it means.

A failed run might reveal a bad prompt. It might reveal a missing source file. It might reveal a fragile route. It might reveal a one-off environment problem. It might reveal nothing at all. The telemetry cannot decide that by itself.

If the system treats every observation as knowledge, it becomes brittle. If it treats every observation as disposable, it never learns.

CyberAlchemy needs a third thing: a reviewable bridge between observation and authority.

That bridge is the PromotionRecord.

## Candidate Knowledge Is Not Promoted Knowledge

This whole model depends on one distinction:

```text
candidate knowledge can guide review
promoted knowledge can guide operation
```

Candidate knowledge is allowed to be useful. It can be retrieved. It can help an agent understand what might be true. It can carry evidence, confidence, and open questions.

But it must remain visibly candidate.

Promoted knowledge is different. It has passed the relevant gates. It has a scope. It has evidence. It has a review owner. It has a contradiction path. It says, "within this boundary, future agents may rely on this."

Without that distinction, an agentic system gets two bad choices: either forget everything or harden everything.

CyberAlchemy rejects both.

## Four Kinds Of Ontology

The model separates ontology into branches because different kinds of knowledge need different authority.

Business Ontology holds intent: domain language, actors, policies, value, rules, premises, and business-facing invariants.

System Ontology holds realization: codebase facts, services, APIs, data flows, tests, infrastructure, runtime behavior, and implementation surfaces.

Bridge Ontology holds correspondence: traceability, drift, evidence links, validation relationships, and the places where intent and realization no longer match.

Operational Ontology is the candidate extension: agent routes, capability behavior, workflow lessons, context solution patterns, route policies, and observed execution patterns.

That last branch is intentionally marked candidate. Agent operation is real system behavior, but the model should not silently promote "agent workflow lessons" into canonical ontology just because they are convenient. The branch needs acceptance and validation before it becomes a permanent peer.

So the architecture keeps Business, System, and Bridge as the stable baseline, while treating Operational Ontology as a candidate extension until accepted.

## The PromotionRecord

A PromotionRecord is one governed proposal or decision about knowledge.

It is not the whole ontology. It is not a memory entry. It is not a log. It is not an implementation plan.

It is a record that says:

```text
Here is the claim.
Here is the evidence.
Here is where it came from.
Here is the branch it targets.
Here is how confident we are in the evidence.
Here is how much the system should rely on it now.
Here is who reviews it.
Here is what happens if later evidence contradicts it.
```

The PromotionRecord is deliberately bounded. One primary claim per record. Pointers to evidence, not raw source dumps. Provenance, not folklore. Confidence fields, not vibes. A review owner, not an implicit blessing.

This makes promotion auditable.

It also makes rejection useful. A rejected or deferred record still teaches the system why a claim was not ready.

## Evidence Confidence Is Not Commitment Confidence

One of the most important ideas in the model is that confidence has two parts.

Evidence confidence asks:

```text
How well does the evidence support this claim?
```

Commitment confidence asks:

```text
How much should the system rely on this claim now?
```

Those are not the same question.

A claim can have strong evidence and low commitment. Maybe it is true but irrelevant. Maybe it is local to one repo. Maybe it is not worth making a rule.

A claim can also be important but weakly evidenced. That does not mean "promote it anyway." It means the system should name the risk and keep the claim gated.

This split prevents a common failure in agent systems: turning "we saw this happen" into "we should now govern future behavior by it."

## Signals Are Not Truth

CyberAlchemy uses the term `ReviewableSignal` rather than `VerifiedSignal` because "verified" can sound stronger than it is.

A signal can be verified as a valid envelope. It can have provenance. It can identify the route, capability, outcome, timestamp, terminal state, and dedupe status.

That still does not make it true in the ontology sense.

A ReviewableSignal can start a PromotionRecord. It can support a claim. It can challenge a claim. It can trigger a drift finding or maintenance route.

It cannot directly create promoted knowledge.

This is how observability becomes useful without becoming authoritarian.

## How A Signal Becomes Knowledge

The lifecycle looks like this:

```text
discovery
  -> inventory evidence
  -> reviewable signal / lifecycle evidence / user decision / source selector
  -> PromotionRecord draft
  -> evidence and confidence review
  -> candidate, premise, policy, constitution, axiom, contradiction, retirement, or rejection
  -> bridge validation
  -> operational use
  -> observability feedback
```

Notice that there is no direct line from telemetry to truth.

Everything passes through a PromotionRecord. Everything keeps its status. Everything that guides future agents needs a use scope and a contradiction path.

## Axioms, Constitutions, Policies, And Premises

The model also needs sharper language for stronger knowledge.

A premise is a falsifiable working bet. It may be useful, but it remains reviewable.

A policy is a scoped decision rule. It tells the system what to do in a defined situation.

A constitution is governance for form, model structure, allowed transformations, review gates, and process rules that preserve those structures or invariants.

An axiom is stronger: a behavior invariant or load-bearing principle that downstream governance depends on.

In plain language:

```text
signal: what happened
premise: what may be true
policy: what decision applies in this scope
constitution: what structure and rules preserve the model
axiom: what must remain invariant
```

Most useful knowledge should not become an axiom. That is the point. The ontology should have a high bar for the things that govern future behavior.

## Why Bridge Validation Matters

The bridge ontology is where the model earns its keep.

Business intent and system behavior drift apart all the time. Agent operation adds another layer of drift: the route may succeed while the intent is underspecified, or the implementation may pass while the original business claim is wrong.

Bridge validation asks whether the claim actually aligns across intent, system behavior, and operational evidence.

It has more than one possible outcome:

- `aligned`: the evidence supports the claim.
- `partial`: the claim is only true in a narrower scope.
- `drift`: behavior diverges from intent.
- `insufficient`: there is not enough evidence yet.
- `contradicted`: evidence actively challenges the claim.

That matters because "not proven" and "false" are different states. A good ontology keeps them separate.

## What This Means For Arcanum

In Arcanum, agentic work happens through things like context-builder, invoke, task-session, skills, sigils, spells, observability, signal-observer, and workflow reflection.

Those tools already create useful evidence. The architecture says what to do with it.

Example:

```text
an invoke or task-session run
  -> observability envelope
  -> ReviewableSignal
  -> PromotionRecord
  -> candidate operational lesson
  -> owner review and bridge validation
  -> scoped future guidance
```

The lesson might be simple: "future ontology synthesis runs need a strict context-builder handoff before design." That can be useful. But it should still carry evidence, confidence, scope, and an owner.

The system should not mutate a sigil, spell, or canonical ontology entry just because one run suggested it.

## What This Means For DomainSpec

DomainSpec gives the software lifecycle side of the model a strong backbone.

A software development agent needs to preserve the route from business intent to spec, from spec to execution, from execution to evidence, and from evidence to validation.

The CyberAlchemy model calls this a `LifecycleEvidenceEnvelope`.

It can carry:

- the original intent;
- the route or stage;
- the terminal outcome;
- evidence from the run;
- telemetry;
- drift or convergence context;
- validation proof.

That envelope can feed a PromotionRecord. The record can then decide whether the evidence supports a system ontology candidate, a bridge validation finding, an operational route policy, a contradiction, or a retirement.

Again: the execution result is evidence, not authority by itself.

## The First Working Slice

The first implementation should be intentionally small.

Not an adapter suite. Not a full ontology vault integration. Not a runtime mutation.

The first slice should be one review-only PromotionRecord fixture.

The question is:

```text
Can one observed operational lesson be represented with evidence, provenance, confidence, owner, bridge status, and route impact without pretending it is promoted knowledge?
```

If yes, the model has a working core.

If no, the model is still too vague or too heavy.

The planned first slice writes only inside the planning package. It creates a fixture and a validation result. It proves the model shape before connecting it to canonical ontology or runtime systems.

That restraint is important. Governance systems should prove they can govern themselves before governing everything else.

## What Is Still Open

This model is candidate architecture, not canonical CyberAlchemy authority.

The remaining questions are real:

- Should Operational Ontology become a permanent fourth branch, or remain an extension across System and Bridge?
- What are the concrete review-owner assignments?
- What signal recurrence and severity defaults should the first operational slice use?
- What should the bridge-validation evidence template look like?
- When is a behavior invariant strong enough to become an axiom?

Those questions do not block the article or the architecture package. They block promotion.

That is exactly how the system should work.

## The Larger Bet

Agentic development will not become trustworthy just because agents get better at action.

It becomes trustworthy when action is connected to evidence, evidence is connected to review, review is connected to authority, and authority remains open to contradiction.

CyberAlchemy's ontology model is a way to make that loop explicit.

It says:

```text
remember, but do not overbelieve
observe, but do not promote automatically
learn, but keep the ladder visible
```

That is the difference between an agent system with memory and an agent system with judgment.

## Evidence Notes

This article is grounded in the CAOL architecture package:

- local context pack and source map: [CONTEXT-HANDOFF.md](CONTEXT-HANDOFF.md), [SOURCE-MAP.md](SOURCE-MAP.md), [context-pack.json](context-pack.json);
- candidate glossary: [DEFINITIONS-GLOSSARY.md](DEFINITIONS-GLOSSARY.md);
- architecture and lifecycle: [ONTOLOGY-ARCHITECTURE.md](ONTOLOGY-ARCHITECTURE.md), [PROMOTION-LIFECYCLE.md](PROMOTION-LIFECYCLE.md);
- bounded research: [external-research-appendix.md](external-research-appendix.md);
- concept tournament and repairs: [CONCEPT-TOURNAMENT.md](CONCEPT-TOURNAMENT.md), [INTERROGATION-VERDICT.md](INTERROGATION-VERDICT.md);
- roadmap and first slice: [ROADMAP.md](ROADMAP.md), [FIRST-WORKING-SLICE.md](FIRST-WORKING-SLICE.md).

The article intentionally preserves the model's caveat: these are candidate design artifacts until reviewed and accepted. Candidate knowledge may guide review. Promoted knowledge may guide operation.
