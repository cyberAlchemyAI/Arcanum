# Whisper Schemas

This directory is the stable schema home for Whisper composition artifacts.

The first package is intentionally YAML-native. The current executable validator
loads Whisper substrates as YAML and checks behavior in code, so this package
defines a human-readable contract plus example fixtures rather than introducing
a separate JSON Schema engine before the examples justify it.

## Authority

| Surface | Authority |
| --- | --- |
| `README.md` | Explains package scope, fixture tiers, promotion policy, and validation commands. |
| `text-intent-substrate.schema.yaml` | Names required, optional, example-only, and deferred field families. |
| `examples/*.yaml` | Provide concrete fixtures. Examples are evidence, not base schema law. |
| `../tools/validate-whisper-draft.py` | Current executable validator for draft-facing behavior. |
| `../README.md` | Owns Whisper spell purpose, phase model, and high-level lifecycle. |

Generated runtime mirrors are not source authority. If a future README refresh
changes the runtime-facing spell contract, regenerate mirrors from the canonical
source instead of editing generated packages by hand.

## Package Files

```text
schemas/
  README.md
  text-intent-substrate.schema.yaml
  examples/
    substack-language-ai.yaml
    substack-object-first-abstraction.yaml
    readability-dynamics.yaml
    delivery-flow.yaml
    delivery-flow-pass.md
    delivery-flow-fail.md
```

## Fixture Tiers

| Fixture | Tier | Expected Use |
| --- | --- | --- |
| `examples/substack-language-ai.yaml` | `full_draft_validator_fixture` | Complete Substack proof fixture; should validate against its paired draft. |
| `examples/substack-object-first-abstraction.yaml` | `partial_compatibility_fixture` | Sequel substrate fixture; useful for field coverage, not yet a full draft-validator fixture. |
| `examples/readability-dynamics.yaml` | `optional_extension_fixture` | Minimal optional readability layer; should produce expected readability flags against a dense draft. |
| `examples/delivery-flow.yaml` | `optional_extension_fixture` | Configures conservative intent-narration and duplicate-block checks against paired pass/fail drafts. |

## Base Contract

A complete Whisper text intent substrate uses `text_intent_substrate` as its root
and includes:

- metadata;
- author objective;
- resonance, relevance, and trajectory cores;
- transport schema;
- candidate selection evidence;
- composition plan;
- draft artifact;
- validation seed;
- learning residue.

The advanced draft-validator path also requires a complete `pareto_tournament`
and matching `composition_parts` when the candidate set declares
`tournament_mode: pareto_aware`.

## Optional And Deferred Layers

`readability_dynamics` is an optional extension. It can flag dense paragraphs,
long sentence clusters, scan-anchor gaps, and abstraction terms that lack
grounding. Its candidate `delivery_flow` branch can also flag configured
intent-narration patterns and conservatively normalized duplicate prose blocks.
Semantic repetition, heading/body paraphrase, reading sequence, and preservation
of load-bearing examples remain human editorial checks. The extension is not a
required base field.

Review payload fields such as `block_id`, `part_id`, selected text, issue type,
requested change mode, and priority are deferred to a future review schema.

## Validation Commands

Parse every YAML package artifact:

```bash
python3 - <<'PY'
from pathlib import Path
import yaml
for path in Path('arcanum/spells/whisper/schemas').rglob('*.yaml'):
    loaded = yaml.safe_load(path.read_text(encoding='utf-8'))
    if not isinstance(loaded, dict):
        raise SystemExit(f'not a mapping: {path}')
    print(f'YAML PASS {path}')
PY
```

Validate the full Substack fixture against its paired draft:

```bash
python3 arcanum/spells/whisper/tools/validate-whisper-draft.py \
  --schema arcanum/spells/whisper/schemas/examples/substack-language-ai.yaml \
  --draft <paired-substack-language-ai-draft.md>
```

Check the optional readability fixture:

```bash
python3 arcanum/spells/whisper/tools/validate-whisper-draft.py \
  --schema arcanum/spells/whisper/schemas/examples/readability-dynamics.yaml \
  --draft <dense-draft-fixture.md>
```

The readability command is expected to print `FLAG whisper draft validation`
and exit 0.

Check the paired delivery-flow fixtures:

```bash
python3 arcanum/spells/whisper/tools/validate-whisper-draft.py \
  --schema arcanum/spells/whisper/schemas/examples/delivery-flow.yaml \
  --draft arcanum/spells/whisper/schemas/examples/delivery-flow-pass.md

python3 arcanum/spells/whisper/tools/validate-whisper-draft.py \
  --schema arcanum/spells/whisper/schemas/examples/delivery-flow.yaml \
  --draft arcanum/spells/whisper/schemas/examples/delivery-flow-fail.md
```

The first command must print `PASS`; the second must print `FLAG` with both
`intent_narration_detected` and `duplicate_prose_block` findings.

## Promotion Policy

This package is canonical as a schema home, but individual examples may still
have different maturity tiers. New fields should enter as example-only or
optional until repeated fixtures and validator behavior justify promotion into
the base contract.
