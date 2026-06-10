# Infra-Spec Candidate — Public Provenance & Handoff

Observed capability: `invoke` · Mode: `define` · Date: 2026-06-10

Target artifact: `infra-spec` candidate formulae package

Target owner / lifecycle: `sigil-development` (next owner)

## Public-local evidence

This candidate is self-contained in `formulae/infra-spec/`:

1. `infra-spec.schema.yml` and `infra-spec.schema.json` define the same Draft 2020-12 contract.
2. `scripts/validate-infra-spec.py` checks both schema shape and five governance rules.
3. `fixtures/spine-pass.json` exercises the passing floor.
4. The nine `fixtures/v-*.json` cases exercise expected blocking outcomes.

The package is candidate evidence only. It is not an authority promotion, provider binding, deployment engine, or proof of a realized infrastructure instance.

## Output paths owned by this candidate

- `formulae/infra-spec/{README.md, SPEC.md, infra-spec.schema.json, infra-spec.schema.yml}`
- `formulae/infra-spec/scripts/validate-infra-spec.py`
- `formulae/infra-spec/fixtures/{spine-pass.json, v-*.json, README.md}`

## Gap ownership split

- **invoke-specific gaps:** none material (define authoring completed; schema + validator + fixtures emitted).
- **target-artifact gaps:** ladder transition rules are unproven; `boundary.kind` needs per-value fixtures; no real instance has been piloted; minimal-twin fixtures could be sharpened; any candidate-status change remains Arcanum-owner gated.

## Recommended next route

`sigil-development --new` to own the infra-spec lifecycle (validate, observe, reflect, and assess promotion readiness), then a pilot `task-session` authoring one representative public `infra-spec` instance.

## Open questions

- Which public example should host the first representative instance?
- What evidence should an Arcanum owner require before changing the candidate status?
