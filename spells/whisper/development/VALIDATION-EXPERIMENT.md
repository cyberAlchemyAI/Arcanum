# Whisper Editorial Admission Validation Experiment

- Artifact: `arcanum/spells/whisper`
- Artifact type: spell
- Profile: `spellcraft-candidate`
- Harness owner: Experiment Harness
- Baseline level: L0 fixture definition
- Current enforcement: `not-enforced`

## Goal

Prove that editorial admission decisions keep machine validation, human editorial judgment, human comprehension, and post-apply review separate. A successful structure or render check must not supply missing human evidence, transfer approval to another surface, or raise a candidate transport to `pass`.

## Hypotheses

| ID | Claim | Causal control |
| --- | --- | --- |
| H1 | Structure and render success cannot replace required comprehension. | Keep both machine axes at `pass`; remove only comprehension evidence. |
| H2 | Full-derivative generation requires frozen intent, exact approval, and an accounted surface. | Change one admission input in each red fixture. |
| H3 | Candidate transport proof caps final status at `flag`. | Hold all evidence at `pass`; change only proof status from proven to candidate. |
| H4 | Post-apply review must bind the applied artifact. | Keep the review present but bind it to the pre-apply digest. |

## Fixture contract

The [fixture manifest](fixtures/editorial-admission/manifest.json) inventories one green control and seven red controls. Each fixture declares:

- a stable fixture ID;
- a low, medium, or complex regime;
- product-neutral inputs;
- expected evidence-binding, generation-admission, and status outcomes where applicable;
- a primary expected verdict and reason;
- a current observation of `not-enforced`.

The JSON shape is provisional experiment input. It is not the run-receipt schema. Synthetic SHA-256 values express matching and mismatching references; digest recomputation is deferred to the evidence-binding implementation.

## Regimes

| Regime | Purpose | Fixtures |
| --- | --- | --- |
| low | Isolate one policy input with minimal evidence. | candidate ceiling, volatile intent, ambient approval |
| medium | Exercise independent human and machine evidence axes. | proven control, missing comprehension, approval mismatch |
| complex | Exercise composed surface or artifact lineage. | unaccounted rendered retell, prior-digest post-apply review |

## Baseline rule

No Whisper run-receipt schema or editorial-admission evaluator exists at this baseline. Therefore the fixture outcomes are expectations, not observed implementation results. The [baseline record](editorial-admission-baseline.json) reports every case as `not-enforced`; it must not convert missing enforcement into `pass` or `fail`.

## Evidence required for this unit

1. All fixture JSON parses.
2. The manifest references exactly eight unique, existing cases.
3. One green control and all seven named red controls are present.
4. Every case includes a regime, primary expected verdict and reason, and `not-enforced` observation.
5. The public files contain no private project language.

## Deferred implementation

This baseline does not add schemas, evaluators, runners, live output, canonical spell behavior, or a final `VALIDATION.md`. Later units must execute these fixtures and replace `not-enforced` observations with reproducible results. Promotion remains blocked until that work and the full low/medium/complex validation report are complete.

## Validation commands

```bash
find arcanum/spells/whisper/development/fixtures/editorial-admission -type f -print
find arcanum/spells/whisper/development/fixtures/editorial-admission -name '*.json' -print0 | xargs -0 -n1 python3 -m json.tool >/dev/null
python3 -m json.tool arcanum/spells/whisper/development/editorial-admission-baseline.json >/dev/null
```

Run the host work pack's private-language sweep over this definition and the fixture directory. The sweep must return no matches.

## Promotion gate

- Fixture baseline completion: eligible for `pass` when the evidence above is complete.
- Editorial-admission enforcement: `not-enforced`.
- Reusable spell validation: `flag` until schemas, evaluators, runners, and final reports exist.
- Promotion readiness: `block`.
