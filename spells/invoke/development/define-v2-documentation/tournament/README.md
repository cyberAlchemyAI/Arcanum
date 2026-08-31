# Invoke Define v2 Documentation Tournament

This package compares three documentation structures by asking isolated agents
to author real `invoke.define-source.v2` inputs and then compiling those inputs
with the canonical Invoke producer.

The controlled variable is information order. Every generated guide contains
the same section bodies; only their sequence differs:

- `guide-alpha.md`: schema-order reference;
- `guide-beta.md`: tutorial-first walkthrough;
- `guide-gamma.md`: ownership-first progressive reference.

The candidate labels are intentionally opaque inside the guides. Trial agents
may read only their assigned guide, the three public task cases, and their own
trial manifest and output directory. They must not read `content/`, `oracle/`,
`dispatch/`, another guide, another trial, the Invoke schemas, compiler, tests,
or prior results.

## State

- Canonical criterion: `CRITERION.json`, validated by
  `criterion.schema.json`; proposed and not frozen.
- Human view: `CRITERION.md`, generated deterministically by
  `render_criterion.py`; it is not a second authority.
- Agent runs: not started.
- Criterion arithmetic and generated-view parity: passing locally.
- Read-only guide-equivalence verification: passing locally.
- Human authorization: required before any multi-agent run.
- Authority: local development evidence only; no Invoke lifecycle, promotion,
  publication, deployment, or production authority.

## Local preparation commands

```sh
python3 arcanum/spells/invoke/development/define-v2-documentation/tournament/validate_criterion.py --json
python3 arcanum/spells/invoke/development/define-v2-documentation/tournament/verify_guide_equivalence.py --json
python3 arcanum/spells/invoke/development/define-v2-documentation/tournament/validate_tournament.py --preconfirmation --json
```

These are read-only preconfirmation commands. They reconstruct expected
criterion and guide views in memory and report `writes: 0`. Use
`render_criterion.py --write` or `render_candidates.py` only as an explicit
candidate-generation step; any resulting byte change invalidates prior
digests, closure, and confirmation.

The oracle sources exist only to prove that each case is satisfiable and that
the scorer recognizes a correct result. They are forbidden inputs to trial
agents.
