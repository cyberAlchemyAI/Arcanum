# WORK-PACK: Language AI Substack

## Purpose

Canonical non-executed plan and Task Session handoff manifest for the repaired Whisper refinement run.

This work-pack converts the accepted `Draft-Readiness Composition Plan` into a reference-checked execution route. It does not publish the article; it makes the next route ready for `task-session` by checking the Harari bridge before drafting while enforcing a reader-grounded opening contract.

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | pass | Reference-checked Task Session handoff executed locally. |
| complexity | low | One reference decision plus one drafting SWU, no repository code changes, no runtime migration, no blocker gate. |
| outputMode | single-file | Split wave/task files are unnecessary for this one-SWU drafting route. |
| executionPackRef | n/a | Not required for low complexity. |
| layeringArtifactRef | `IMPLEMENTATION-LAYERING.md` | Companion layer boundary artifact. |
| activeLayerWindow | L2 | First draft proof complete; operator review is next. |
| lastUpdatedAt | 2026-05-29T11:20:12Z | Task Session created a fresh second draft from the enforced Pareto schema. |
| readinessProfile | pareto-enforced-two-draft-review | Produced two independently reviewable drafts and validator-backed Pareto schema enforcement. |

## Objective Summary

- Objective: verify the Harari/Sapiens bridge first, then produce a first reviewable Substack draft from the repaired refinement substrate and composition plan.
- Primary inputs: `REFERENCE-CHECK-HARARI.md`, `REFINE-SEED-PROPOSAL.md`, `DESIGN-REDEFINITION.md`, `stages/08-distill-repair.md`, `IMPLEMENTATION-LAYERING.md`.
- Success condition: a draft exists that covers the planned body parts, preserves citation integrity, translates internal Arcanum vocabulary for public readers, and passes operator review checks for objective, audience, resonance, and structure.

## Planning Mapping

| Planning Source | Work-Pack Target | Mapping Rule |
| --- | --- | --- |
| `REFINE-SEED-PROPOSAL.md` | Objective, constraints, first SWU | Preserve thesis, target public, non-goals, research policy, and done criteria. |
| `DESIGN-REDEFINITION.md` | Delivery slice and drafting outline | Use the seven-part composition plan as the draft skeleton. |
| `stages/08-distill-repair.md` | Blockers and constraints | Carry repair flags forward as drafting constraints, not blockers. |
| `IMPLEMENTATION-LAYERING.md` | Active layer and validation gate | Execute L2 draft proof only; defer L3 publication readiness. |
| `REFRESH-REPORT.md` | Pareto decision and next execution route | Use the approved `two_tier` decision to prepare the schema/validator refresh SWU. |

## Delivery Slices

| Slice ID | Outcome | Layer | Dependencies | Validation |
| --- | --- | --- | --- | --- |
| S-001 | Harari/Sapiens reference strategy checked before drafting. | L2 | L0 intent proof passed; L1 composition proof accepted with flags. | Reference check records source strategy, safe wording, and quote/page verification limits. |
| S-002 | First reviewable Substack draft from repaired substrate. | L2 | S-001 reference strategy; L0 intent proof passed; L1 composition proof accepted with flags. | Draft review against objective, audience, resonance, structure, and citation-integrity checks. |
| S-003 | Two-tier Pareto tournament schema and validator path prepared. | L2 | `/invoke lets go with two tier`; `REFRESH-REPORT.md`; `REFRESH-PATCH-PROPOSAL.md`. | Task Session validates schema parse, draft validator pass, and Pareto completeness checks. |
| S-004 | Fresh second Substack draft created from zero using the Pareto schema. | L2 | Pareto schema enforced; old draft excluded as writing source. | Validator pass plus freshness comparison against `DRAFT-SUBSTACK-001.md`. |

## Task Status Board

| Task ID | Goal | Layer | Complexity | Source | Gate Status | Status |
| --- | --- | --- | --- | --- | --- | --- |
| TASK-WHISPER-REFERENCE-CHECK | Establish safe Harari/Sapiens reference strategy before drafting. | L2 | low | `REFERENCE-CHECK-HARARI.md`; `stages/08-distill-repair.md` | ready | complete |
| TASK-WHISPER-ARTICLE-DRAFT | Produce first Substack draft from approved substrate and composition plan. | L2 | low | `REFERENCE-CHECK-HARARI.md`; `REFINE-SEED-PROPOSAL.md`; `DESIGN-REDEFINITION.md`; `stages/08-distill-repair.md`; `IMPLEMENTATION-LAYERING.md` | pass | complete |
| TASK-WHISPER-SCHEMA-REFRESH | Add operational two-tier Pareto tournament schema and validator checks. | L2 | low | `REFRESH-REPORT.md`; `REFRESH-PATCH-PROPOSAL.md`; `text-intent-substrate.yaml`; `spells/whisper/tools/validate-whisper-draft.py` | pass | complete |
| TASK-WHISPER-DRAFT-V2-FRESH | Create a fresh second Substack draft from zero using the enforced Pareto schema. | L2 | low | `text-intent-substrate.yaml`; `TASK-SESSION-PARETO-REPORT.md`; `spells/whisper/tools/validate-whisper-draft.py` | pass | complete |

## SWU Execution Handoff

| SWU ID | Parent Task | Source Anchors | Related Context | Dependencies | Write Scope | Done Criteria | Acceptance Evidence | Validation Surface | Execution Owner | Handoff Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-WHISPER-REFERENCE-001 | TASK-WHISPER-REFERENCE-CHECK | `REFERENCE-CHECK-HARARI.md`; `stages/08-distill-repair.md#Repair Decisions` | `REFINE-SEED-PROPOSAL.md`; `DESIGN-REDEFINITION.md` | No execution dependency beyond this work-pack. | Update reference strategy only; do not draft the article or publish externally. | Reference strategy records source, safe paraphrase, citation limits, and direct-quote/page verification policy. | `REFERENCE-CHECK-HARARI.md` exists and gives a draft-safe bridge. | Check source strategy before drafting. | local-fallback | complete |
| SWU-WHISPER-ARTICLE-001 | TASK-WHISPER-ARTICLE-DRAFT | `REFERENCE-CHECK-HARARI.md`; `REFINE-SEED-PROPOSAL.md#Draft Text Intent Substrate`; `DESIGN-REDEFINITION.md#Composition Plan`; `stages/08-distill-repair.md#Repair Decisions`; `IMPLEMENTATION-LAYERING.md#Layer Decision Table` | `GLOSSARY.md`; `INVOKE-DEFINE.md`; `text-intent-substrate.yaml` | `SWU-WHISPER-REFERENCE-001` complete. | Create a draft artifact inside this refinement run folder, for example `DRAFT-SUBSTACK-001.md`; do not edit source spell code or publish externally. | Draft includes reader-grounded hook, Harari bridge after the hook, research context, core insight, Arcanum example, implications, and invitation; Harari is paraphrased through the checked shared-fiction/cooperation bridge unless exact quote/page is verified; internal vocabulary is translated; `meta-schema` has one concrete public-facing example or is omitted. | `DRAFT-SUBSTACK-001.md` plus `TASK-SESSION-REPORT.md` and `tools/validate-whisper-draft.py` confirm opening contract, objective fit, audience fit, resonance fit, structure completeness, constraint compliance, Arcanum translation clarity, and citation integrity. | Tool check: run `python3 spells/whisper/tools/validate-whisper-draft.py --schema spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/text-intent-substrate.yaml --draft spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/DRAFT-SUBSTACK-001.md`; then compare draft against `REFERENCE-CHECK-HARARI.md`, `REFINE-SEED-PROPOSAL.md` validation checks, and `stages/08-distill-repair.md` guardrails. | local | complete |
| SWU-WHISPER-PARETO-001 | TASK-WHISPER-SCHEMA-REFRESH | `REFRESH-REPORT.md`; `REFRESH-PATCH-PROPOSAL.md`; `text-intent-substrate.yaml#scu_candidate_set` | `DESIGN-REDEFINITION.md`; `DRAFT-SUBSTACK-001.md`; `spells/whisper/tools/validate-whisper-draft.py` | `two_tier` decision approved by `/invoke lets go with two tier`. | Update only `text-intent-substrate.yaml`, `spells/whisper/tools/validate-whisper-draft.py`, and the Task Session report/evidence needed for this SWU. | Schema includes `pareto_tournament.tiering: two_tier`, objectives, hard gates, candidate protocol, candidate scores, dominance rule, consensus rule, selected candidate, rejected alternatives, and part-level mini-tournament hooks for delegated or failing sections; validator checks Pareto completeness and existing draft validation still passes. | `TASK-SESSION-PARETO-REPORT.md` records the decision, validation commands, negative probe, and remaining publication gaps. | YAML parse, `jq empty refresh-report.json`, `python3 -m py_compile spells/whisper/tools/validate-whisper-draft.py`, draft validator pass, and negative Pareto incompleteness probe pass. | local | complete |
| SWU-WHISPER-DRAFT-V2-001 | TASK-WHISPER-DRAFT-V2-FRESH | `text-intent-substrate.yaml#pareto_tournament`; `text-intent-substrate.yaml#composition_plan`; `TASK-SESSION-PARETO-REPORT.md` | `WORK-PACK.md`; `spells/whisper/tools/validate-whisper-draft.py` | Pareto schema enforcement complete. | Create `DRAFT-SUBSTACK-002.md` and task-session evidence; do not use `DRAFT-SUBSTACK-001.md` as a writing source; do not publish externally. | Draft uses selected Pareto candidate, starts from reader-grounded naming/workflow experience, introduces Harari only after the hook, translates Arcanum terms, includes a concrete schema/meta-schema example, avoids direct quotation, and passes validator plus freshness comparison. | `DRAFT-SUBSTACK-002.md`, `task-session-context-draft-v2-fresh.md`, and `TASK-SESSION-DRAFT-V2-REPORT.md`. | Run validator against `DRAFT-SUBSTACK-002.md` and run normalized 8-word shingle freshness comparison against `DRAFT-SUBSTACK-001.md`. | local | complete |

## Task Contract: TASK-WHISPER-DRAFT-V2-FRESH

### Objective

Create a second Substack draft from zero using the enforced Pareto schema and selected candidate, without using `DRAFT-SUBSTACK-001.md` as writing material.

### Implementation Detail

1. Use `text-intent-substrate.yaml` as the source of truth for objective, audience, tone, opening contract, citation policy, selected Pareto candidate, and composition parts.
2. Bind the draft to `pareto_tournament.consensus.selected_candidate_set: executable_language_research_note`.
3. Preserve the selected technique stack: language as executable medium, Arcanum as live case, and invitation to name a workflow.
4. Open with a concrete reader-facing naming or workflow moment.
5. Introduce Harari/Sapiens only after the opening hook and only as paraphrased bridge material.
6. Do not quote or page-cite `Sapiens`.
7. Do not use `DRAFT-SUBSTACK-001.md` as a drafting source; use it only as an optional post-draft freshness comparison.

### Failure Modes

- Draft borrows phrasing or structure too closely from `DRAFT-SUBSTACK-001.md`.
- Draft obeys prose constraints but ignores the selected Pareto candidate.
- Draft starts with Harari, `Sapiens`, or external authority.
- Draft becomes a product pitch or generic AI essay instead of an exploratory research note.

## Task Contract: TASK-WHISPER-ARTICLE-DRAFT

### Objective

Produce the first Substack draft from the repaired substrate, using the checked Harari bridge without expanding scope into external publication, fundraising copy, or unverified source claims.

### Implementation Detail

1. Open from a concrete reader-facing moment where naming, language, or workflow compression becomes operational.
2. Move from that grounded hook into the checked Harari/Sapiens bridge: shared stories and symbolic coordination make human cooperation possible.
3. Frame generative AI as a collaborator in building personal symbolic systems, avoiding generic AI hype.
4. State the core insight: names, aliases, schemas, and meta-schemas can behave as personal symbolic code when they make thought and workflow reusable.
5. Use Arcanum as a live example, but translate internal vocabulary before relying on it:
   - `whisper` as a way to shape a writing intent,
   - `invoke` as a way to turn intent into a governed plan,
   - aliases as reusable names for workflows,
   - schemas as shared shapes for thinking and action.
6. Use Harari through `REFERENCE-CHECK-HARARI.md`; do not quote or page-cite `Sapiens` unless exact edition/page has been verified.
7. For `meta-schema`, either give one plain public example or omit the term from the first draft.
8. Close with an invitation that asks readers what they would name, compress, or schema for their own creative practice.

### Failure Modes

- Draft reads like a product pitch for Arcanum instead of a public research post.
- Draft invents or precisely attributes a Harari/Sapiens claim without source evidence.
- Draft uses internal terms as if the public reader already knows them.
- Draft overclaims that natural language replaces engineering.

## Task Contract: TASK-WHISPER-SCHEMA-REFRESH

### Objective

Make Whisper's Pareto-aware dynamic operational by encoding the approved `two_tier` tournament model and validating that the schema is complete before future drafts rely on it.

### Implementation Detail

1. Add a `pareto_tournament` contract to `text-intent-substrate.yaml` with:
   - `tiering: two_tier`,
   - objectives for `resonance`, `relevance`, and `trajectory`,
   - hard gates for opening contract, citation integrity, and audience legibility,
   - candidate protocol fields,
   - dominance and consensus rules,
   - selected candidate and rejected alternatives with trade-off preservation.
2. Preserve the existing `scu_candidate_set` as historical/compatibility evidence or mirror it into the new tournament contract without deleting current rationale.
3. Add `composition_parts` hooks for part-local mini-tournaments when a part is delegated, revised, or fails validation.
4. Extend `validate-whisper-draft.py` with Pareto contract checks before prose validation.
5. Keep the existing draft content stable unless validation reveals a direct schema-induced failure.

### Failure Modes

- Pareto remains a label rather than a checkable tournament protocol.
- Validator only checks that the field exists, not that objectives, candidates, gates, and selected plan are coherent.
- Part-level tournaments run for every paragraph instead of only delegated/failing sections.
- Existing opening-contract validation regresses while adding Pareto checks.

## Blockers And Gaps

| Gap ID | Scope | Description | Execution Handling |
| --- | --- | --- | --- |
| G1-harari-citation | citation integrity | Exact Harari/Sapiens source and wording are not verified. | Use `REFERENCE-CHECK-HARARI.md` as a safe paraphrase strategy; only quote/page-cite after owned-copy verification. |
| G2-public-translation | audience fit | Internal Arcanum terms need reader-facing translation. | Translate before examples; do not depend on private vocabulary. |
| G3-meta-schema-example | concept clarity | `meta-schema` may be too abstract for first draft. | Provide one concrete public-facing example or omit. |
| G4-pareto-schema-refresh | schema completeness | Pareto-aware dynamics needed validator-backed `two_tier` schema enforcement. | Resolved by `TASK-SESSION-PARETO-REPORT.md`; keep validator enforcement active for future draft and schema edits. |

No blocker remains for the completed L2 draft-plus-schema proof. Publication readiness still depends on operator review and exact `Sapiens` citation verification if the post needs direct quotation or page-level attribution.

## Validation Strategy

- Objective fit: draft advances the working thesis from `REFINE-SEED-PROPOSAL.md`.
- Audience fit: draft is readable by AI-curious creative builders without requiring Arcanum insider context.
- Resonance fit: tone preserves wonder, agency, and grounded intellectual excitement.
- Structure completeness: draft includes hook, research context, core insight, Arcanum example, implications, and invitation.
- Opening contract compliance: validator confirms the first prose paragraph does not start with Harari/Sapiens and the external reference appears only after the reader-grounded hook.
- Constraint compliance: draft avoids generic AI hype, condescension, mysticism without examples, product-pitch framing, and overclaiming.
- Citation integrity: draft contains no precise Harari/Sapiens attribution unless source evidence is included.

## Next Route

Operator review should compare `DRAFT-SUBSTACK-001.md` and `DRAFT-SUBSTACK-002.md`, then either select one or ask Whisper to synthesize a third version from named strengths. Exact `Sapiens` citation verification remains a publication-readiness follow-up. The next transport pressure is fundraising copy, which should reuse the enforced Pareto schema rather than reopening the Substack schema refresh.
