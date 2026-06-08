# Robot-Talks

Robot-Talks is an Arcana sigil for coordinated cross-layer investigation.

It sends multiple investigators after distinct concerns, then synthesizes their evidence into tensions that a human can validate before any implementation work begins.

## Problem It Solves

Complex systems can fail because different layers believe different things. Documentation may describe one behavior while implementation does another. A frontend may assume one contract while a backend exposes another. Operational practice may depend on an unstated rule that no artifact owns.

A single investigator can miss these contradictions because broad coverage competes with depth. Robot-Talks solves that by splitting the inquiry by concern, collecting independent evidence, and synthesizing contradictions rather than summaries.

## Use When

- the problem spans two or more layers,
- contradictions must be identified before acting,
- independent perspectives are likely to reveal better evidence,
- the cost of misunderstanding is higher than the cost of a structured investigation,
- a human decision gate is needed before follow-up work begins.

## Do Not Use When

- the issue is a single-file bug,
- the user only needs a quick explanation of one component,
- the requested work is already well specified,
- implementation should begin immediately without an audit phase.

## Investigation Model

Robot-Talks has four phases:

1. Setup: define the central question, assumptions to challenge, agent roles, and decomposition strategy.
2. Exploration: each investigator reports findings, gaps, local tensions, and synthesis questions.
3. Synthesis: the orchestrator identifies contradictions across layers.
4. Human gate: the user decides whether each tension is actionable, deferred, invalid, or uncertain.

## Output

The primary output is a preserved investigation record containing:

- the scope definition,
- investigator roles,
- independent findings with evidence,
- synthesized tensions,
- human gate decisions,
- follow-up action links or notes.

## Why This Is Arcana

The sigil coordinates multiple reasoning threads, preserves state across phases, and requires human validation before action. Its value is not a single transformed artifact; it is governed inquiry that produces a responsible next move.