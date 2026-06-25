# Schema Artifact Audit - Whisper

- Task: `SWU-WSC-001`
- Result: pass for L0 audit
- Audit date: 2026-06-23
- Scope: `arcanum/spells/whisper/`
- Write boundary honored: this refinement-run folder only

## Executive Finding

Whisper has a strong schema lineage but not yet a stable schema home. The
current authority is split across:

- the canonical spell lifecycle contract in `arcanum/spells/whisper/README.md`;
- development-run schema evidence in `text-intent-substrate.yaml` and
  `WHISPER-SCHEMA.md`;
- executable enforcement in `tools/validate-whisper-draft.py`;
- optional readability evidence in the 2026-06-23 readability Task Session.

The future canonical package should be assembled from these artifacts, not
copied wholesale from a development run. Article-specific source context,
draft-specific target paths, and run-local provenance must remain examples or
evidence.

## Classification Legend

| Classification | Meaning |
| --- | --- |
| `canonical-source-candidate` | Stable enough to seed a canonical schema or schema README after owner acceptance. |
| `example-candidate` | Useful as a fixture or example, but not base authority. |
| `provenance-only` | Explains why a field exists or how it changed; should not be imported as schema authority. |
| `generated` | Derived artifact or runtime mirror; regenerate from source if needed. |
| `superseded` | Historical proposal replaced by later accepted evidence. |

## Artifact Classification Matrix

| Artifact | Classification | Field Families | Canonicalization Use | Notes |
| --- | --- | --- | --- | --- |
| `arcanum/spells/whisper/README.md` | `canonical-source-candidate` | artifact lifecycle, shared state, SCU cores, review contract | Seed schema package README authority and owner rules. | Canonical spell contract, but it does not yet define `schemas/` as a stable home. |
| `.agents/skills/whisper/SKILL.md` | `generated` | same lifecycle surface as README | Do not hand-edit; regenerate after canonical source changes. | Generated native runtime package with `canonical_source: spells/whisper/README.md`. |
| `arcanum/spells/whisper/development/DESIGN.md` | `canonical-source-candidate` plus `provenance-only` | early `TextIntentSubstrate`, transport defaults, artifact state machine | Use as design rationale and compare against the fuller current substrate. | It contains stable concepts but older field shapes. |
| `arcanum/spells/whisper/development/WHISPER-PRESENTATION.html` | `provenance-only` | public explanation of substrate fields | Use as explanatory reference only. | Presentation HTML is not a schema source. |
| `20260526T204134Z-language-ai-substack/text-intent-substrate.yaml` | `canonical-source-candidate` plus `example-candidate` | metadata, source context, objective, SCU cores, transport schema, Pareto tournament, composition plan, composition parts, draft artifact, validation, learning residue, execution policy | Primary machine-readable candidate for base field contracts and first canonical example. | Do not copy wholesale because it includes article-specific and run-local values. |
| `20260526T204134Z-language-ai-substack/WHISPER-SCHEMA.md` | `canonical-source-candidate` plus `provenance-only` | human-readable substrate explanation, audience decision, lifecycle chain, Pareto consensus | Seed future schema README language after removing article-specific claims. | Useful bridge from machine schema to human contract. |
| `20260526T204134Z-language-ai-substack/REFRESH-REPORT.md` | `provenance-only` | Pareto drift signals, deltas, blockers, validation | Preserve as why-history for Pareto promotion. | It prepared the later schema and validator SWU. |
| `20260526T204134Z-language-ai-substack/REFRESH-PATCH-PROPOSAL.md` | `superseded` plus `provenance-only` | proposed two-tier Pareto shape and validator additions | Retain as historical proposal, not current contract. | Superseded by accepted schema and Task Session execution evidence. |
| `20260526T204134Z-language-ai-substack/TASK-SESSION-PARETO-REPORT.md` | `provenance-only` with strong promotion evidence | `pareto_tournament`, `composition_parts`, validator checks | Use as promotion evidence for the canonical package spec. | Confirms the two-tier Pareto implementation passed validation. |
| `20260526T204134Z-language-ai-substack/WORK-PACK.md` and task-session context files | `provenance-only` | execution history, gates, receipts | Preserve as execution lineage only. | Do not import work-pack state into schema. |
| `20260526T204134Z-language-ai-substack/refresh-report.json` and `evidence-index.json` | `provenance-only` | machine evidence index and refresh record | Keep as traceability support. | Parseable evidence, not schema authority. |
| `20260526T204134Z-language-ai-substack/DRAFT-SUBSTACK-001.md` and `DRAFT-SUBSTACK-002.md` | `example-candidate` | draft output against substrate | Use as validation fixtures for examples. | Draft 02 currently validates against the main substrate. |
| `20260526T204134Z-language-ai-substack/DRAFT-SUBSTACK-002.review.html` and `.public.html` | `generated` | rendered review/public surfaces | Regenerate from draft/schema inputs when needed. | Do not use generated output as schema source. |
| `20260526T204134Z-language-ai-substack/stages/**` | `provenance-only` | refine/invoke/interrogation/distill decisions and flags | Preserve for audit trail and rationale. | Too stage-local for canonical schema authority. |
| `20260531T164421Z-readability-dynamics/**` | `provenance-only` | readability-density concern, staged refinement, dispatch | Use as design history for readability. | Predates the implemented validator layer. |
| `20260623T052410Z-readability-dynamics-invoke/readability-dynamics-fixture.yaml` | `example-candidate` | `transport_schema`, `readability_dynamics` | Use as optional-layer example fixture. | Parses and exercises flag behavior against Draft 02. |
| `20260623T052410Z-readability-dynamics-invoke/TASK-SESSION-READABILITY-REPORT.md` | `provenance-only` with L0 promotion evidence | readability validator behavior and fixture results | Use as evidence that optional readability checks execute. | Not broad enough for full canonical promotion. |
| `20260623T052410Z-readability-dynamics-invoke/DEFINE.md`, `DESIGN.md`, `IMPLEMENTATION-LAYERING.md`, `WORK-PACK.md`, `SPELLCRAFT-RESULT.md`, `INVOKE-RESULT.md` | `provenance-only` | readability intent, design, gates, owner acceptance | Use to explain why `readability_dynamics` exists and why it remains optional. | Planning evidence, not base schema source. |
| `20260623T045653Z-object-first-abstraction/text-intent-substrate.yaml` | `example-candidate` | sequel substrate with parent sequence, reference candidates, style lens, transport relationship | Use as a future compatibility fixture. | Useful because it tests a post-sequence substrate, but lacks the full Pareto/composition-parts layer. |
| `20260623T045653Z-object-first-abstraction/composition-plan.md` | `provenance-only` | narrative composition plan | Use as writing evidence only. | Not schema authority. |
| `arcanum/spells/whisper/tools/validate-whisper-draft.py` | `canonical-source-candidate` | YAML load contract, Pareto checks, opening contract, length checks, optional readability checks | Executable reference for current validation semantics. | It is stronger evidence for currently enforced fields than prose-only artifacts. |
| `arcanum/spells/whisper/tools/build-whisper-review-html.py` | `provenance-only` | schema loading, `composition_parts` part role lookup, review payload schema | Defer review-payload schema integration to later package work. | Related consumer, not base schema authority. |
| `arcanum/spells/whisper/review/README.md` | `provenance-only` | review build commands and current development schema path | Refresh later so it points to canonical schema examples. | Currently depends on development-run path in its example command. |
| `arcanum/spells/whisper/templates/draft-review-base.html` | `provenance-only` consumer support | review UI payload placeholder | Keep outside base schema package unless review payload is promoted. | Template is source support for the review surface, not schema source. |
| `arcanum/spells/whisper/tools/__pycache__/**` | `generated` | Python bytecode | Ignore. | Local generated artifact. |

## Field-Family Classification

| Field Family | Status | Promote As | Example-Only Or Deferred Parts |
| --- | --- | --- | --- |
| `text_intent_substrate` wrapper | stable candidate | Base package root. | None. |
| `metadata.substrate_version`, `transport_type`, `artifact_status` | stable candidate | Base metadata contract. | `source_packet`, parent run IDs, and run status values. |
| `source_context` | example-only | Example fixture content. | Raw intent, AI result, live example, citation gaps, and reference candidates are article-specific. |
| `author_objective` | stable candidate | Base objective contract. | Concrete reader-change text belongs to examples. |
| `resonance_core`, `relevance_core`, `trajectory_core` | stable candidate | Core SCU schema families. | Concrete tones, publics, body parts, and sequence names belong to examples or transport profiles. |
| `transport_schema` | stable candidate | Transport sub-contract. | `substack_research_post` is the first profile; fundraising remains an extension pressure. |
| `opening_contract` | stable candidate | Transport validation sub-contract. | Reader-grounding terms and external-reference terms are profile/example values. |
| `scu_candidate_set` | compatibility candidate | Legacy/compatibility candidate layer. | The stronger canonical contract should prefer `pareto_tournament` where present. |
| `pareto_tournament` | stable candidate | Base advanced selection contract. | Candidate scores and selected candidate IDs are example values. |
| `composition_plan` | stable candidate | Planning contract. | `construction_sequence` entries are example/profile values. |
| `composition_parts` | stable candidate | Two-tier part-hook contract. | Specific part IDs are example/profile values. |
| `draft_artifact` | stable candidate | Artifact pointer/status contract. | Concrete target paths are example values. |
| `validation` | stable candidate | Validation-report contract seed. | Required terms and check labels are profile/example values. |
| `learning_residue` | stable candidate | Residue capture contract. | Concrete lesson slots and content are example values. |
| `execution_policy` | candidate/deferred | Optional execution policy section. | Needs package-spec review before base promotion. |
| `readability_dynamics` | candidate-stable optional layer | Optional extension example and possibly later optional schema module. | Needs broader fixture matrix before full promotion. |
| Review payload fields (`block_id`, `part_id`, selected text, issue type) | deferred | Future review schema, not first base package. | Requires a separate review-payload package decision. |

## Proposed Canonical Package Boundary

The next package-spec SWU should propose a stable home such as:

```text
arcanum/spells/whisper/schemas/
  README.md
  text-intent-substrate.schema.yaml
  examples/
    substack-language-ai.yaml
    substack-object-first-abstraction.yaml
    readability-dynamics.yaml
```

This audit does not create those files. It only names the safest split:

- base contract: field families and validation semantics that repeat across
  Whisper runs;
- transport profile: `substack_research_post` defaults and opening contract;
- examples: language-AI Draft 02, Object sequel, and readability fixture;
- provenance: refresh reports, work-packs, staged runs, and generated review
  outputs.

## Validation Evidence

Inventory:

```text
find arcanum/spells/whisper -type f | sort | wc -l
# 119

rg -l "text_intent_substrate|transport_schema|scu_candidate_set|pareto_tournament|composition_parts|readability_dynamics|WHISPER-SCHEMA|Refresh Report|schema" arcanum/spells/whisper --glob '!tools/__pycache__/**' | sort | wc -l
# 97
```

YAML parse checks:

```text
YAML PASS arcanum/spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/text-intent-substrate.yaml keys=16
YAML PASS arcanum/spells/whisper/development/refinement-runs/20260623T045653Z-object-first-abstraction/text-intent-substrate.yaml keys=13
YAML PASS arcanum/spells/whisper/development/refinement-runs/20260623T052410Z-readability-dynamics-invoke/readability-dynamics-fixture.yaml keys=2
```

Draft 02 compatibility:

```text
python3 arcanum/spells/whisper/tools/validate-whisper-draft.py --schema arcanum/spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/text-intent-substrate.yaml --draft arcanum/spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/DRAFT-SUBSTACK-002.md
# PASS whisper draft validation
```

Readability fixture behavior:

```text
python3 arcanum/spells/whisper/tools/validate-whisper-draft.py --schema arcanum/spells/whisper/development/refinement-runs/20260623T052410Z-readability-dynamics-invoke/readability-dynamics-fixture.yaml --draft arcanum/spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/DRAFT-SUBSTACK-002.md
# FLAG whisper draft validation
```

The readability command exits 0 with `FLAG` findings, which supports
candidate-stable optional behavior without treating readability as fully
promoted.

## Gate Outcome

`SWU-WSC-001` is complete. The workpack should now remain blocked at L1 until
Spellcraft accepts a package specification for `arcanum/spells/whisper/schemas/`.

No canonical schema authority changed in this Task Session.
