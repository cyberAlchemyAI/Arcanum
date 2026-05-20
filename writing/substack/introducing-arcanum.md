---
title: "Arcanum: When Agent Skills Become Infrastructure"
subtitle: "Introducing Arcanum, a framework for turning skills and agent workflows into reusable, observable, improvable capabilities."
status: draft
audience: "AI builders, agent engineers, software designers, toolmakers, and people building long-running human-agent workflows"
tags:
  - ai-agents
  - agent-engineering
  - cyber-alchemy
  - observability
  - software-design
---

# Arcanum: When Agent Skills Become Infrastructure

Agent builders are in the middle of discovering what skills are really for.

At first, a skill can look like a better prompt: a reusable instruction, a little local knowledge, maybe a tool workflow. But once people start building with skills, the harder questions appear quickly.

How should a skill be structured? When is it reusable? How does it fail? How does another agent know when to use it? How does a team validate that it works? How does the system remember which behaviors are good, which ones drift, and which ones should evolve?

Without answers to those questions, skills become easy to create but hard to govern. A user asks for help, the model reasons, writes, edits, searches, plans, or codes, and maybe the session produces a strong artifact. But once the thread moves on, the actual method is hard to reuse. The next agent has to infer what happened from scattered context. The next human has to remember what worked.

Arcanum is Cyber Alchemy's attempt to make that work visible.

Arcanum is a framework for turning skills and agent workflows into reusable capabilities through governed synthesis. It gives a shape to the work of turning vague intent into artifacts that humans and agents can understand, reuse, validate, observe, and improve.

It is not just a prompt library.

A prompt says what to do once. An Arcanum capability should explain when to use it, when not to use it, how it reasons, what it produces, how it fails, how it is validated, how it is observed, and who owns the next lifecycle step.

## Why This Exists

The more Cyber Alchemy works with agents, the clearer the pattern becomes: the interesting part is not a single answer. It is the emergence of reusable ways of thinking.

An agent can help define a product, critique an architecture, design a planning process, interrogate a spec, decompose implementation layers, validate an artifact, run experiments, or preserve a development trace. These are not just tasks. They are repeatable behaviors.

But repeatable behaviors need structure.

They need names. They need boundaries. They need quality bars. They need anti-patterns. They need output contracts. They need validation examples. They need observability. They need maintenance.

Without that structure, agent work becomes a pile of clever moments. Useful, but hard to govern.

Arcanum tries to turn those moments into capabilities.

## The Cyber Alchemy Method

The working method behind Arcanum is called the Cyber Alchemy Method.

The core idea is simple: good agent systems are built by turning vague intent and discovered evidence into governed artifacts.

Every serious run keeps five anchors visible:

| Anchor          | Question                                                                |
| --------------- | ----------------------------------------------------------------------- |
| Objective       | What is the work trying to solve?                                       |
| Output artifact | What should exist when this work is done?                               |
| Discovery       | What must be learned before the artifact can responsibly close?         |
| Tension         | What could make the artifact brittle, oversized, misleading, or unsafe? |
| Route           | Who or what owns the next lifecycle step?                               |

Those anchors matter because agent work can drift very easily.

If the objective is unclear, the agent can produce beautiful output that solves the wrong problem. If the output artifact is unnamed, the middle of the work becomes mushy. If discovery is skipped, the system just rearranges what it already knows. If tension is absent, the plan becomes overconfident. If route ownership is missing, the result lands with no responsible next step.

Cyber Alchemy treats the agent as a collaborator, not a passive executor. The agent helps shape the problem, gather evidence, expose tension, revise the artifact, and make the path forward legible.

## Sigils And Spells

Arcanum uses two main capability shapes: sigils and spells.

A sigil is one reusable agent capability.

Examples of sigil-shaped work include:

- implementation layering,
- decision gates,
- structured interviews,
- workflow reflection,
- experiment harnessing,
- sigil development itself.

A spell is a composition of sigils into a workflow.

Where a sigil is an atomic capability, a spell is a recipe. It defines which capabilities run, in what order, what state they share, which artifacts move between phases, what gates can stop the workflow, and how the run is observed.

This distinction is important because agents need lifecycle boundaries. A capability that defines a sigil should not silently become the authority for maintaining all sigils. A planning workflow should not quietly become an execution workflow. A spell can coordinate, but it should not copy and blur the internals of the capabilities it composes.

Arcanum tries to preserve those boundaries.

## Capabilities Need A Lifecycle

In Arcanum, a reusable capability is not done when the first draft exists.

It moves through a lifecycle:

1. Define the intent and local vocabulary.
2. Design the behavior, boundaries, interfaces, and failure modes.
3. Plan the implementation path.
4. Build the smallest responsible unit.
5. Validate with examples and expected outputs.
6. Observe real usage.
7. Reflect when evidence accumulates.
8. Revise without losing the original contract.

This is slower than writing a clever prompt.

It is also more honest.

If a capability is going to be reused by humans and agents across sessions, it needs more than vibes. It needs enough structure that a future run can tell whether it is succeeding.

### Invoke And Interrogation

Two of the most practical Arcanum entry points are `invoke` and `interrogation`.

`invoke` is the authoring spell. It turns unclear development intent into governed artifacts: definitions, design packets, implementation plans, work-packs, transport notes, and lifecycle handoffs. When an idea does not yet have a clear route, `invoke` helps decide whether the work needs a spec, architecture, plan, validation path, or lifecycle handoff.

`interrogation` is the pressure-testing sigil. It reviews an artifact, plan, or development packet and asks whether the work is actually ready to continue. It looks for missing context, weak boundaries, premature complexity, hidden blockers, and places where the artifact sounds complete but cannot yet support the next lifecycle step.

Together, they create a useful rhythm:

```text
invoke creates the governed artifact
interrogation challenges whether it is ready
the artifact is revised
the lifecycle route becomes clearer
```

That rhythm matters because agent work often looks polished before it is structurally sound. `invoke` gives the work form. `interrogation` gives it resistance.

## Observability Is Already Implemented

One of the most important parts of Arcanum is the observability layer.

The repository-local observability package is already implemented. It stores invocation signals, run envelopes, lookup indexes, hook operation records, reflection state, and reflection reports under `.arcanum/observability/`.

That means a capability can leave evidence behind after it runs.

The system can record:

- which capability ran,
- what mode it used,
- what artifact it targeted,
- which gates passed, flagged, or blocked,
- what output contract drift appeared,
- what workflow gaps were found,
- whether reflection should be triggered.

This matters because agents need memory that is not just chat memory.

Chat memory is conversational. Observability is operational. It gives the system a way to notice repeated failures, confusing handoffs, overused techniques, missing validation, or output drift.

The point is not surveillance. The point is maintenance.

A reusable capability should be able to learn from use.

## Experiment Harness Is Also Implemented

Arcanum also includes an implemented experiment harness.

The experiment harness gives reusable spells and sigils an artifact-local test loop. Realistic fixtures go in. User-facing outputs come out. Validation reports record whether the capability actually satisfies its contract.

The harness supports:

- fixture and expected-output checks,
- bounded Codex example runs,
- generated example prompts,
- captured example outputs,
- validation reports,
- quality bar and anti-pattern checks,
- observability emission after experiment reports.

This is where the framework starts to feel less like a philosophy and more like infrastructure.

If a capability claims it can define a sigil, produce an implementation plan, validate an artifact, or coordinate a workflow, the experiment harness gives Cyber Alchemy a way to ask: did it actually do that?

Not in theory. In a run. With evidence.

## The Smallest Responsible Unit

A recurring theme in Arcanum is the smallest responsible unit.

This is not the smallest possible unit. Tiny fragments can be meaningless. It is the smallest unit that still has a purpose, boundary, input, output, and recomposition path.

For example, when designing a new sigil, the smallest responsible unit might be a README and SKILL contract that can be run manually before any runtime adapter or registry promotion exists.

That unit is small enough to validate, but complete enough to mean something.

Then later layers can add examples, runtime adapters, observability, registry candidacy, and reflection policy.

The goal is to avoid two common failures:

- premature complexity, where the system designs for future scale before the current unit works,
- brittle minimalism, where the system is so small that it cannot evolve naturally.

Arcanum tries to hold the tension between those two.

## Why This Matters

The future of agent work is not just better models.

Better models matter, obviously. But model capability alone does not answer the lifecycle question:

How can useful agent behavior become durable?

How can a community inspect it, reuse it, improve it, and know when it should not be trusted?

How can the reasoning method be preserved, not just the output?

How can agent systems evolve without becoming a maze?

Arcanum is one answer Cyber Alchemy is exploring.

It is a framework for making agent capability explicit. It is also a working style: research first, name the artifact, expose tension, validate the result, observe usage, and route the next owner.

## What Exists Now

Arcanum currently includes:

- the Cyber Alchemy Method,
- a framework for sigil and spell lifecycle governance,
- a tier model for Formulae, Transmutations, and Arcana,
- registries for reusable sigils and spells,
- an implemented repository-local observability layer,
- an implemented experiment harness,
- lifecycle capabilities such as invoke, interrogation, sigil-development, spellcraft, implementation-layering, and task-session,
- development workflows for creating and validating new capabilities.

Some parts are still evolving. That is expected. The point is not to freeze the system early. The point is to make the system understandable enough that it can evolve in public.

## Invitation

Cyber Alchemy is sharing Arcanum because agent builders need better language for the work between "prompt" and "product."

There is a growing space of agent capabilities that are not quite apps, not quite prompts, not quite workflows, and not quite tests. They are reusable reasoning behaviors with lifecycle needs.

Arcanum gives Cyber Alchemy a way to name and build those.

If you are building agents, tools for thought, coding assistants, research workflows, design systems, or long-running human-agent collaborations, Cyber Alchemy would love to know what resonates and what feels missing.

The question Cyber Alchemy keeps returning to is:

What would agent work look like if every useful behavior could become a clear, validated, observable, improvable capability?

That is the direction Arcanum is trying to explore.
