# Evidence Ledger: Whisper Idea-To-MVP Fixture

Status: source and validation ledger.

## Source Evidence

| Evidence | Path | Used For |
| --- | --- | --- |
| Whisper spell contract | `spells/whisper/README.md` | Shared state, artifact lifecycle, execution phases, SCU core definitions. |
| Text intent substrate | `spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/text-intent-substrate.yaml` | Cores, candidate routes, hard gates, Pareto tournament, composition parts. |
| Whisper work-pack | `spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/WORK-PACK.md` | SWU contracts, task evidence, done criteria, residue. |
| Pareto task-session report | `spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/TASK-SESSION-PARETO-REPORT.md` | Evidence that Pareto became schema and validator backed. |
| Fresh draft | `spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/DRAFT-SUBSTACK-002.md` | Public-facing proof of the selected candidate and composition plan. |
| Draft validator | `spells/whisper/tools/validate-whisper-draft.py` | Executable validation surface. |

## Lifecycle Status Map

| State | Whisper Example | Fixture Translation |
| --- | --- | --- |
| idea | Raw author intent about language, AI, aliases, schemas, and personal code. | Start with a full messy idea prompt. |
| substrate | `text_intent_substrate` with resonance, relevance, and trajectory cores. | Extract promise, fit, and movement. |
| candidate | Three candidate route sets with scores and trade-offs. | Compare possible product, guide, research, or interface directions. |
| blocked | Anthropological bridge first fails opening-contract compliance. Citation precision remains gated. | Do not let attractive routes pass hard safety or evidence gates. |
| selected | `executable_language_research_note`. | Pick the non-dominated route that passes gates and preserves the idea's promise. |
| parts | Seven composition parts with dependencies and validation checks. | Turn a route into screens, stages, lanes, checks, or document sections. |
| ready task | Work-pack SWUs for draft, schema refresh, and fresh second draft. | Execute one bounded SWU with source links and validation. |
| validated | Draft validator and Pareto completeness checks pass. | Keep receipts and commands with the result. |
| residue | Publication review, exact citation verification, next transport pressure. | Preserve next loop instead of hiding uncertainty. |

## Validation Evidence

Current task-session validation should run:

```bash
python3 - <<'PY'
from html.parser import HTMLParser
from pathlib import Path
HTMLParser().feed(Path('development/user-guide/arcanum-development-loop.html').read_text())
PY

python3 - <<'PY'
from pathlib import Path
import yaml
for path in Path('development/user-guide/fixtures/whisper-idea-to-mvp').glob('*.yml'):
    yaml.safe_load(path.read_text())
    print(f'YAML OK: {path}')
PY

formulae/dispatch-spec/scripts/validate-dispatch.py \
  development/user-guide/refinement-runs/20260601T211736Z-html-fixture-whisper-cores/REFINE-DISPATCH.json

python3 spells/whisper/tools/validate-whisper-draft.py \
  --schema spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/text-intent-substrate.yaml \
  --draft spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/DRAFT-SUBSTACK-002.md

python3 development/user-guide/fixtures/whisper-idea-to-mvp/validate-fixture.py --negative
```

## Residue

- The HTML guide is approachable but still should be browser-reviewed across mobile and desktop before being treated as a polished frontend artifact.
- The fixture proves the thinking pattern, not a new reusable sigil contract.
- The non-writing toy probe is a low-cost falsification check, not broad external proof.
- Direct Harari/Sapiens quotation and page-level citation remain blocked unless source verification is added.
- Fundraising copy remains next transport pressure for Whisper, not part of this guide fixture.
