# Interrogation refine-design-review

## Status

`flag`

## Command

- Owner command: `interrogation`
- Resolved command file: `.codex/commands/interrogation.md`
- Requested mode: `refine-design-review`
- Capability: `structured-interview-kits`
- Reviewed design artifact: `spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/stages/06-invoke-design.md`
- Reviewed design definition: `spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/DESIGN-REDEFINITION.md`
- Target artifact: `spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/REFINE-SEED-PROPOSAL.md`

## Evidence Baseline

- `stages/06-invoke-design.md` reports `pass` and names `DESIGN-REDEFINITION.md` as the produced design artifact.
- `DESIGN-REDEFINITION.md` provides six design views, a body-part composition plan, glossary consistency, risk handling, and a design handoff.
- `REFINE-SEED-PROPOSAL.md` requires a refined text intent substrate, body-part composition plan, accepted/rejected technique candidates, and a first SWU suitable for drafting before Task Session.
- `stages/05-distill.md` selected the **Draft-Readiness Composition Plan** and preserved citation and audience-translation flags.

## Review Finding

The design artifact is usable for the next refinement stage. It resolves the previous stage-07 dependency because invoke design now produced pass evidence and a six-view design surface.

The review does not block continuation, but it identifies repair needs that should be carried into `stages/08-distill-repair.md` before `invoke plan`.

## Repair Needs

| Repair Need | Severity | Required Handling |
| --- | --- | --- |
| `G1-harari-citation` | flag | Preserve as a bracketed verification gap unless bounded research verifies the exact claim, source, and wording. Do not quote or precisely attribute Harari/Sapiens in the drafting SWU without source evidence. |
| `G2-public-translation` | flag | Translate `whisper`, `invoke`, aliases, schemas, and Arcanum-style naming into reader-facing language before relying on them as examples. |
| `G3-meta-schema-example` | flag | Either provide one concrete public-facing sentence/example for `meta-schema` or omit the term from the first draft. |
| Layer acceptance recording | flag | Record that L1 composition proof is design-ready in the repair or planning artifact; do not mutate the seed retroactively from this review stage. |

## Decision

Accepted design unit: `Draft-Readiness Composition Plan`.

Rejected blocker status: the remaining issues are known repair flags, not design blockers. The design has enough structure to continue into repair and plan generation.

Recommended default: continue without asking the user a clarification question, because the required repairs are already explicit in the seed, distill result, and design artifact.

Unresolved risk if ignored: the article plan may later produce private Arcanum jargon, overclaim the language-as-code analogy, or invent an unsupported Harari/Sapiens attribution.

## Structured Interview Result

- Target scope: `spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/REFINE-SEED-PROPOSAL.md`
- Mode: `refine-design-review`
- Questions asked: 0
- Decisions recorded: 1
- Artifacts updated: `spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/stages/07-interrogation-refine-design-review.md`
- Remaining ambiguities: Harari citation verification, public translation of internal terms, and concrete `meta-schema` handling remain as downstream repair flags.
- Verdict: flag
- Next step: run distill repair against `DESIGN-REDEFINITION.md` and this review, then continue to `invoke plan` if repair preserves the flags.

## Validation

- Read `.codex/commands/interrogation.md`.
- Followed the embedded `structured-interview-kits` command contract.
- Reviewed `stages/06-invoke-design.md`, `DESIGN-REDEFINITION.md`, `REFINE-SEED-PROPOSAL.md`, and `stages/05-distill.md`.
- Preserved one-question cadence by asking no human question because no blocker ambiguity remained.
- Preserved stage ownership by writing only this review artifact and stage evidence.
