# Experiment Harness Profile Proof Report

Status: deterministic profile proof passed.

## Scope

This proof validates the profile-aware Experiment Harness path after profile initialization became the default baseline.

It does not spend live Codex budget. Live loops remain promotion evidence.

## Proof Targets

| Target | Profile | Source | Result |
| --- | --- | --- | --- |
| `/tmp/tmp.RXwlBEDjwm/concept-layer-optimizer` | `sigil-development` | sandbox copy of `arcana/concept-layer-optimizer` | pass |
| `/tmp/tmp.RXwlBEDjwm/toy-spell` | `spellcraft` | generated toy spell contract under `/tmp` | pass |

## Evidence

| Check | Sigil Development Profile | Spellcraft Profile |
| --- | --- | --- |
| Profile initialization | pass | pass |
| `EXPERIMENT-PROFILE.md` generated | pass | pass |
| Prompt/regime files generated | pass | pass |
| Profile validation after report | pass | pass |
| Mock loop validation | pass | pass |

## Commands Run

```bash
arcana/experiment-harness/scripts/init-harness.sh /tmp/tmp.RXwlBEDjwm/concept-layer-optimizer --type sigil --profile sigil-development
arcana/experiment-harness/scripts/validate-harness.sh /tmp/tmp.RXwlBEDjwm/concept-layer-optimizer
EXPERIMENT_OBSERVE=0 arcana/experiment-harness/scripts/report-harness.sh /tmp/tmp.RXwlBEDjwm/concept-layer-optimizer
arcana/experiment-harness/scripts/validate-harness.sh /tmp/tmp.RXwlBEDjwm/concept-layer-optimizer

arcana/experiment-harness/scripts/init-harness.sh /tmp/tmp.RXwlBEDjwm/toy-spell --type spell --profile spellcraft
arcana/experiment-harness/scripts/validate-harness.sh /tmp/tmp.RXwlBEDjwm/toy-spell
EXPERIMENT_OBSERVE=0 arcana/experiment-harness/scripts/report-harness.sh /tmp/tmp.RXwlBEDjwm/toy-spell
arcana/experiment-harness/scripts/validate-harness.sh /tmp/tmp.RXwlBEDjwm/toy-spell

MAX_ATTEMPTS=1 PASS_STREAK=1 AUTO_IMPROVE=0 EXPERIMENT_LOOP_MOCK_DIR=/tmp/tmp.RXwlBEDjwm/mock-loops/concept \
  arcana/experiment-harness/scripts/loop-harness.sh /tmp/tmp.RXwlBEDjwm/concept-layer-optimizer LIVE-SIGIL-HARNESS-VALIDATION-001

MAX_ATTEMPTS=1 PASS_STREAK=1 AUTO_IMPROVE=0 EXPERIMENT_LOOP_MOCK_DIR=/tmp/tmp.RXwlBEDjwm/mock-loops/spell \
  arcana/experiment-harness/scripts/loop-harness.sh /tmp/tmp.RXwlBEDjwm/toy-spell LIVE-SPELLCRAFT-VALIDATE-001
```

## Final Validation

```text
sigil-development:
VALIDATION=pass
PROFILE_VALIDATION=pass
PROFILE_ID=sigil-development
LIFECYCLE_OWNER=sigil-development

spellcraft:
VALIDATION=pass
PROFILE_VALIDATION=pass
PROFILE_ID=spellcraft
LIFECYCLE_OWNER=spellcraft

mock loops:
LIVE-SIGIL-HARNESS-VALIDATION-001: LOOP_STATUS=pass
LIVE-SPELLCRAFT-VALIDATE-001: LOOP_STATUS=pass
```

## Remaining Promotion Gap

The generalized profile path is ready for deterministic lifecycle use. Real Codex loops are still required before claiming live promotion evidence for a production spell or sigil.
