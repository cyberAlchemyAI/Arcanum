# Distill Validation Examples

These examples validate the candidate Distill package before runtime adapter work and registry promotion.

Each file includes prompts, input context, expected output bodies, expected verdicts, and acceptance notes.

## Example Index

| Example | Coverage | Expected Verdict |
| --- | --- | --- |
| [standard-pass.md](standard-pass.md) | Standard mode, objective-output setup, smallest coherent unit, recomposition, evolution profile, navigation closeout | pass |
| [compact-pass.md](compact-pass.md) | Compact mode, one recursive round, always-on gates, skipped-technique reasons | pass |
| [tournament-pass.md](tournament-pass.md) | Tournament mode, three proposal tracks, set-based comparison, elimination conditions | pass |
| [deep-pass.md](deep-pass.md) | Deep mode, higher-risk context, multiple tracks, stronger cycle checks, premortem, human-gate readiness | pass |
| [technique-trigger-cases.md](technique-trigger-cases.md) | Conditional technique activation and deferral, including Cynefin, TRIZ, morphological analysis, Wardley mapping, set-based design, and navigable result check mapping | pass/flag |
| [negative-and-drift-cases.md](negative-and-drift-cases.md) | Infinite reduction, premature complexity, missing evolution profile, lost recomposition, objective-output drift, and navigation downgrade | flag/block |

## Validation Rule

Examples are not production outputs. They are expected-output fixtures that show what the SKILL contract should produce or reject.

Runtime work may begin only when these examples are reviewed in [../VALIDATION.md](../VALIDATION.md).
