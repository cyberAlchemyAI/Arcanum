# Work-Pack: Whisper Idea-To-MVP Fixture

Status: guide fixture.
Execution owner: local task-session.

## Objective

Show one complete Arcanum idea-to-MVP path using the Whisper example:

```text
raw idea
  -> idea substrate
  -> candidate routes
  -> hard gates
  -> selected route
  -> composition parts
  -> SWU execution
  -> validation evidence
  -> residue and next loop
```

## Source Anchors

| Source | Role |
| --- | --- |
| `spells/whisper/README.md` | Spell contract, shared state, lifecycle, execution phases, SCU cores. |
| `spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/text-intent-substrate.yaml` | Core extraction, candidate tournament, hard gates, composition parts. |
| `spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/WORK-PACK.md` | Work-pack and SWU evidence for the Substack proof. |
| `spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/TASK-SESSION-PARETO-REPORT.md` | Validator-backed Pareto schema refresh evidence. |
| `spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/DRAFT-SUBSTACK-002.md` | Finished draft example for the fixture story. |

## Delivery Slices

| Slice | Output | Done Criteria | Status |
| --- | --- | --- | --- |
| S1-substrate | `idea-substrate.yml` | Generalizes Whisper's three cores into idea resonance, relevance, and trajectory. | complete |
| S2-candidates | `candidate-routes.yml` | Preserves selected and rejected candidates, objective scores, hard gates, and selection rule. | complete |
| S3-parts | `composition-parts.yml` | Names part responsibilities, dependencies, must-do, must-not-do, and validation checks. | complete |
| S4-playbook | `PLAYBOOK.md` | Shows how a user can reuse the fixture for a new idea. | complete |
| S5-evidence | `EVIDENCE-LEDGER.md` | Maps source evidence, validations, residues, and next-loop candidates. | complete |
| S6-negative-probe | `toy-nonwriting-probe.yml`, `validate-fixture.py` | Proves the generalized grammar blocks when one core is removed. | complete |

## Task Board

| Task | Goal | Write Scope | Validation |
| --- | --- | --- | --- |
| UGF-001 | Build the explanatory fixture files. | `development/user-guide/fixtures/whisper-idea-to-mvp/` | YAML parse plus source-path existence checks. |
| UGF-002 | Build the approachable HTML guide. | `development/user-guide/arcanum-development-loop.html` | HTML parser check and source reference scan. |
| UGF-003 | Synchronize refine and task-session evidence. | `development/user-guide/refinement-runs/20260601T211736Z-html-fixture-whisper-cores/` and `development/user-guide/task-sessions/20260601T211736Z-run-refine-strategy/` | Dispatch validation, JSON validation, receipt completeness. |

## Validation Surface

- `python3 -m json.tool` for run JSON files.
- YAML parse for fixture `.yml` files.
- Python HTML parser check for `arcanum-development-loop.html`.
- `formulae/dispatch-spec/scripts/validate-dispatch.py` for `REFINE-DISPATCH.json`.
- `python3 spells/whisper/tools/validate-whisper-draft.py --schema ... --draft ...` for the Whisper draft proof.
- `python3 development/user-guide/fixtures/whisper-idea-to-mvp/validate-fixture.py --negative` for fixture completeness and missing-core negative probe.

## Residue

- The fixture does not publish Whisper output.
- The fixture does not promote Whisper lessons into canonical Arcanum definitions.
- Browser validation of the HTML remains useful if the local Playwright wrapper is available.
- A later task can add an interactive form that lets a user fill the three cores directly in the page.
