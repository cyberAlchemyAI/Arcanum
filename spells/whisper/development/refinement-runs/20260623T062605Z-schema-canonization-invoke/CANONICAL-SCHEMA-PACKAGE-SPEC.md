# Canonical Schema Package Spec - Whisper

- Task: `SWU-WSC-002`
- Status: package-spec pass
- Scope: design/review artifact only
- Target future home: `arcanum/spells/whisper/schemas/`
- Canonical package files created in this SWU: none

## Decision

The first canonical Whisper schema package should be a human-readable contract
plus YAML example fixtures. Do not start with standalone JSON Schema.

Reason: the current executable surface, `tools/validate-whisper-draft.py`,
loads YAML substrates and enforces behavior through code: Pareto completeness,
composition-part bindings, opening contract rules, word and character limits,
required terms, and optional readability dynamics. A JSON Schema could be added
later, but creating one now would either duplicate incomplete behavior or create
a second authority before the examples prove out.

## Target Package Shape

```text
arcanum/spells/whisper/schemas/
  README.md
  text-intent-substrate.schema.yaml
  examples/
    substack-language-ai.yaml
    substack-object-first-abstraction.yaml
    readability-dynamics.yaml
```

### File Contracts

| Target File | Role | Initial Content Source | Validation Tier |
| --- | --- | --- | --- |
| `schemas/README.md` | Human contract for schema authority, example tiers, promotion policy, generated-surface policy, and validation commands. | Whisper README lifecycle contract, `SCHEMA-ARTIFACT-AUDIT.md`, this package spec. | Markdown review and path-reference scan. |
| `schemas/text-intent-substrate.schema.yaml` | YAML-native schema contract that names required, optional, example-only, and deferred field families. | Audit field-family table plus current validator behavior. | YAML parse; field-family review; later examples checked against it. |
| `schemas/examples/substack-language-ai.yaml` | Full validator fixture for the current main Substack proof. | `20260526T204134Z-language-ai-substack/text-intent-substrate.yaml`, with run-local paths adjusted only if required. | YAML parse and `validate-whisper-draft.py` against Draft 02. |
| `schemas/examples/substack-object-first-abstraction.yaml` | Partial compatibility fixture for a sequel post substrate. | `20260623T045653Z-object-first-abstraction/text-intent-substrate.yaml`. | YAML parse; schema-field coverage review. Draft-validator pass is deferred until Pareto and draft fields are added. |
| `schemas/examples/readability-dynamics.yaml` | Optional extension fixture for readability density behavior. | `20260623T052410Z-readability-dynamics-invoke/readability-dynamics-fixture.yaml`. | YAML parse and expected `FLAG` from `validate-whisper-draft.py` against Draft 02. |

## Authority Model

| Layer | Owns | Must Not Own |
| --- | --- | --- |
| Whisper README | Spell purpose, phases, sigil roles, artifact lifecycle, and high-level schema-home reference after L2. | Concrete schema field lists or example data. |
| `schemas/README.md` | Schema package authority, usage instructions, fixture tiers, and promotion policy. | Spell lifecycle details already owned by Whisper README. |
| `text-intent-substrate.schema.yaml` | Field-family contract and required/optional/deferred classifications. | Article-specific source context or draft-specific values. |
| `examples/*.yaml` | Concrete substrates and optional extension fixtures. | Base schema requirements. |
| `tools/validate-whisper-draft.py` | Executable validation semantics until a schema engine exists. | Human explanation of schema package authority. |
| `.agents/skills/whisper/**` | Generated runtime mirror. | Source authority; it must be regenerated from canonical source when needed. |

## Field Ownership

| Field Family | Package Treatment | Owner |
| --- | --- | --- |
| `text_intent_substrate` wrapper | Required root for complete substrates; allowed omitted wrapper only for minimal extension fixtures if validator supports it. | Base contract |
| `metadata.substrate_version` | Required for complete substrates. | Base contract |
| `metadata.transport_type` | Required for complete substrates. | Base contract |
| `metadata.artifact_status` | Required for complete substrates. | Base contract |
| `metadata.source_packet` and run IDs | Example-only provenance. | Examples |
| `source_context` | Optional example content, not base requirement. | Examples |
| `intake_decisions`, `distill_trace`, `composition_plan_seed`, `validation_report` | Development/provenance fields unless later promoted by evidence. | Examples/provenance |
| `author_objective` | Required for complete substrates. | Base contract |
| `resonance_core`, `relevance_core`, `trajectory_core` | Required SCU core families for complete substrates. | Base contract |
| `transport_schema` | Required for complete draft-validator fixtures; transport-specific values live in profiles/examples. | Base contract plus transport profile |
| `transport_schema.opening_contract` | Required when draft validation is expected. | Transport profile |
| `transport_schema.length_words` and `max_characters` | Required when draft validation is expected. | Transport profile |
| `scu_candidate_set` | Compatibility family; required only when a run captures candidate-set history. | Compatibility contract |
| `pareto_tournament` | Required when `scu_candidate_set.tournament_mode` is `pareto_aware` and draft validation is expected. | Base advanced selection contract |
| `composition_plan` | Required when `pareto_tournament` participates in draft validation. | Base planning contract |
| `composition_parts` | Required for two-tier Pareto draft validation. | Base advanced selection contract |
| `draft_artifact` | Required for complete publishable draft flows; concrete paths are example values. | Base contract plus examples |
| `validation` | Required for complete flows as a validation-report seed. | Base contract |
| `learning_residue` | Required for complete flows as a residue-capture contract. | Base contract |
| `execution_policy` | Optional candidate field; include as optional in schema contract. | Optional contract |
| `readability_dynamics` | Optional extension, not base requirement. | Optional extension |
| Review payload fields | Deferred from first schema package. | Future review schema |

## Example Policy

Examples must declare their validation tier in comments or a top-level
metadata/status field inside the future package contract.

| Example | Tier | Required Checks |
| --- | --- | --- |
| `substack-language-ai.yaml` | `full_draft_validator_fixture` | YAML parse; Draft 02 validator pass; Pareto and composition parts present. |
| `substack-object-first-abstraction.yaml` | `partial_compatibility_fixture` | YAML parse; field-family coverage review. Do not require draft-validator pass until it has `pareto_tournament`, `composition_parts`, and a draft artifact. |
| `readability-dynamics.yaml` | `optional_extension_fixture` | YAML parse; Draft 02 validator returns expected `FLAG` with exit 0. |

Examples must not preserve development-run authority. They may preserve
development-run values as fixture data, but the package README should say that
examples are evidence, not base schema law.

## Validation Commands For Package Creation

Run these during `SWU-WSC-003` after the future package files exist.

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

```bash
python3 arcanum/spells/whisper/tools/validate-whisper-draft.py \
  --schema arcanum/spells/whisper/schemas/examples/substack-language-ai.yaml \
  --draft arcanum/spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/DRAFT-SUBSTACK-002.md
```

```bash
python3 arcanum/spells/whisper/tools/validate-whisper-draft.py \
  --schema arcanum/spells/whisper/schemas/examples/readability-dynamics.yaml \
  --draft arcanum/spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/DRAFT-SUBSTACK-002.md
# expected: FLAG whisper draft validation, exit 0
```

```bash
test -f arcanum/spells/whisper/schemas/README.md
test -f arcanum/spells/whisper/schemas/text-intent-substrate.schema.yaml
test -f arcanum/spells/whisper/schemas/examples/substack-language-ai.yaml
test -f arcanum/spells/whisper/schemas/examples/substack-object-first-abstraction.yaml
test -f arcanum/spells/whisper/schemas/examples/readability-dynamics.yaml
```

```bash
rg -n "development/refinement-runs" arcanum/spells/whisper/schemas/README.md \
  arcanum/spells/whisper/schemas/text-intent-substrate.schema.yaml
# expected: no development-run authority references in base contract files
```

The examples may cite development provenance when useful, but base contract
files must not point at development runs as runtime authority.

## Non-Goals For SWU-WSC-003

The package creation SWU should not:

- refresh `arcanum/spells/whisper/README.md`;
- update `.agents/skills/whisper/**`;
- redesign `validate-whisper-draft.py`;
- create a JSON Schema engine;
- promote review payload fields into the base package;
- claim `readability_dynamics` is a required base field.

## Next Gate

`SWU-WSC-002` is complete when this specification exists and validates against
the audit and Whisper lifecycle contract.

After completion, `SWU-WSC-003` may create only:

```text
arcanum/spells/whisper/schemas/**
```

`SWU-WSC-004` remains blocked until the canonical package exists and validates.

