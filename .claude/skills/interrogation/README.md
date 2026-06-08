# Structured Interview Kits

Structured Interview Kits is an Arcana sigil for running evidence-backed interviews one question at a time using pluggable interview modes.

It turns interviewing into a reusable system: select a mode, build a cheap evidence baseline, generate a discriminating question, ask it, record the answer, update the target artifact, and continue until exit criteria are met.

## Identity

- Canonical ID: `structured-interview-kits`
- Alias: `Interrogation`
- Alias command slug: `interrogation`
- Alias command: `arcanum-sigil-interrogation`

## Problem It Solves

Open-ended interviews can sprawl. Large question banks overwhelm users, and answers often fail to update the artifacts they were meant to clarify.

Structured Interview Kits solves this by enforcing a strict one-question cadence, evidence-backed prompts, explicit patch targets, and mode-specific exit criteria.

## Use When

- a plan, specification, audit, readiness review, or discovery artifact needs human clarification,
- interview behavior should be reusable across domains,
- questions should be generated from evidence rather than generic curiosity,
- each answer should update a concrete artifact,
- different interview modes are needed for different risks.

## Do Not Use When

- the user asked for a single quick answer,
- no artifact should be updated from the interview,
- the workflow cannot wait for human answers,
- the question set is already fixed and deterministic,
- the topic needs broad research before interviewing.

## Mode Model

Each interview mode should define:

- applicability signals,
- question formation strategy,
- required question fields,
- allowed patch targets,
- exit criteria,
- readiness verdict shape.

## Output

The sigil returns:

- selected mode,
- questions asked,
- answers recorded,
- artifacts updated,
- decisions captured,
- remaining ambiguities,
- readiness verdict.

## Why This Is Arcana

The sigil coordinates evidence gathering, mode selection, human gates, artifact mutation, and readiness interpretation across a multi-turn session.