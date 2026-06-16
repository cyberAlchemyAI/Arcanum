# Interview Discipline

Status: active-pattern
Steward: Structured Interview Kits

## Purpose

Govern one-question-at-a-time elicitation when repository evidence is insufficient, ambiguous, or requires owner intent before responsible mutation can continue.

## Boundary

This discipline names interview practice. It does not replace source evidence, make decisions for the owner, or mutate artifacts without the lifecycle that owns the result.

## Evidence

- [Structured Interview Kits](../../arcana/structured-interview-kits/README.md) - defines one-question cadence and evidence-backed prompts.
- [Discipline Catalog](../DISCIPLINES.md) - records `interview` as an active-pattern discipline for cases that cannot be responsibly inferred from repo evidence.

## Validation

- Mode: prose-review
- Check: interview transcript or receipt review and `python3 disciplines/scripts/validate-discipline-catalog.py`.
- Latest result: pass

## Quality Bar

A useful interview discipline entry must:

- ask only when evidence or owner intent is genuinely needed,
- preserve one-question cadence,
- connect answers to the artifact or decision they affect,
- keep the owner decision distinct from agent inference,
- route resulting mutations through the owning lifecycle.

## Promotion Guardrail

Interview answers can supply owner intent, but they cannot directly promote registry, ontology, glossary, sigil, spell, or discipline knowledge without the appropriate owner route.
