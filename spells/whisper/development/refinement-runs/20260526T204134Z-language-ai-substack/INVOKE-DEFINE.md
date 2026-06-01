# Invoke Define: Language AI Substack

## Status

- Mode: `define`
- Phase status: `pass`
- Preset: `compact`
- Target: `REFINE-SEED-PROPOSAL.md`
- Seed: `REFINE-SEED-PROPOSAL.md`
- Context: `stages/01-context-builder.md`

## Specification Baseline

Create a Whisper-guided Substack research post that argues generative AI makes language more operational: people can name, alias, schema, and compose their own symbolic tools without needing inherited software syntax, academic jargon, or a single domain vocabulary.

## Reader And Outcome

- Primary reader: AI-curious creative builders.
- Secondary reader: Arcanum research collaborators.
- Desired reader change: the reader sees names, aliases, schemas, and workflows as personal symbolic code, not just prose or prompt decoration.
- Success signal: the reader can explain why Arcanum-style naming and schema work functions as personal code and can imagine making their own reusable symbolic tools.

## Scope

In scope:

- refine the article intent and composition plan,
- preserve `text-intent-substrate.yaml` as the schema control surface,
- keep Arcanum as a live example without turning the post into a product pitch,
- preserve citation gaps as explicit gaps.

Out of scope:

- publishing the article,
- executing the full draft in this invoke stage,
- treating the Harari/Sapiens gossip reference as verified,
- claiming natural language replaces engineering.

## Acceptance Criteria

| Criterion | Evidence |
| --- | --- |
| Article target and reader change are explicit. | `REFINE-SEED-PROPOSAL.md`; `context-builder/CONTEXT-PACK.md` |
| Schema control surface is preserved. | `text-intent-substrate.yaml`; `WHISPER-SCHEMA.md` |
| Research policy is bounded. | `G1-harari-citation`; seed research decision |
| Next drafting work is bounded as a Task Session SWU, not executed here. | `SWU-WHISPER-ARTICLE-001` |

## Decisions

- Use the seed proposal as the define baseline rather than rewriting upstream artifacts.
- Select the `invoke.research` candidate family with a compact generic fallback, because the target is a research post with an explicit evidence/citation policy.
- Emit a layering seed for downstream plan/task-session work.

## Gate Result

- Status: `pass`
- Reason: mandatory define inputs are covered by the context-builder stage, no blocker ambiguity remains, and the only research gap is deferred by policy until a source-backed Harari claim is drafted.
