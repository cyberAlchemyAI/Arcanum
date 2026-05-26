# Goal Handoff Draft: Refine Whisper Article Idea

## Objective

Run the canonical Refine loop on the Whisper article seed for a `substack_research_post` about language, generative AI, aliases, schemas, and personal code.

## Target

`spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/REFINE-SEED-PROPOSAL.md`

## Runtime Mode

- Preset: `compact` recommended for first experiment.
- Research: `research-if-gap-appears`.
- External research confirmation: required if the run wants to use the Yuval Harari / Sapiens gossip reference as a source-backed claim.

## Stage Dispatch Contract

Resolve before dispatch:

```bash
tools/arcanum --resolve context-builder
tools/arcanum --resolve invoke
tools/arcanum --resolve interrogation
tools/arcanum --resolve distill
```

Dispatch stages through:

```bash
tools/arcanum --exec --output <stage-output> <command> <stage-request>
```

## Required Stage Outputs

| Stage | Expected Output |
| --- | --- |
| Context Builder | source context pack for Whisper design and article seed |
| Invoke Define | article definition and glossary baseline |
| Interrogation refine-review | critique of definition, missing audience/source decisions |
| Research decision | local-first, bounded only if Harari reference becomes load-bearing |
| Distill | smallest coherent article unit and candidate selection |
| Invoke Design | article architecture/composition design |
| Interrogation refine-design-review | critique of design and schema fit |
| Distill Repair | repaired substrate or explicit unresolved tensions |
| Invoke Plan | non-executed plan and first drafting SWU |
| Final Interrogation + Result | final synthesis and recommended Task Session route |

## Blocked Conditions

- No target public can be selected.
- Desired reader change remains unclear after one focused question.
- Harari/Sapiens reference is used as a precise claim without citation verification.
- The plan collapses into generic AI hype instead of explaining language as personal symbolic code.

## Task Session Handoff Candidate

After Refine passes or flags with non-blocking gaps, hand off:

```text
task-session target:
spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/

task:
SWU-WHISPER-ARTICLE-001 - draft the Substack post from the refined TextIntentSubstrate and composition plan.
```

## Operator Note

If you want a short run, choose `compact`. If you want this to become a publishable flagship essay, choose `standard` and allow bounded research for the Harari anchor.
