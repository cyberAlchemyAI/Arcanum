# Execution Pack — Single readiness gate

## Choreography

```text
W0 contract
  → W1 audit producer
    → W2 Task Session consumer
      → W3 integration and generated packaging
```

The waves are sequential because every later owner consumes a validated receipt from the prior semantic contract. Within a wave, SWUs remain sequential at first; parallelism may be reconsidered only after the first implementation proves that write scopes and schemas are independent.

## Owner handoffs

- W0/W1: Spellcraft lifecycle owner for `work-pack-readiness-audit`.
- W2: Sigil Development lifecycle owner for `task-session`.
- W3: joint validation receipts, parent-coordinated; canonical sources first and generated packages second.

## Gates

- W0 → W1: new schemas valid and legacy fixtures unchanged.
- W1 → W2: deterministic manifest generation and semantic-equivalence fixtures pass.
- W2 → W3: wrong-unit, stale-plan, baseline, replay, and adapter-bypass fixtures all block; exact case admits.
- Close: end-to-end fixture proves no pre-execution Refresh or second full audit while post-execution closeout still uses Invoke Refresh.

## Execution ceiling

This pack is authoring evidence only. It does not select, admit, or execute an SWU.
