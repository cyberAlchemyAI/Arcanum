# Context Pack: Language AI Substack

## Identity

- Task/SWU: `SWU-WHISPER-ARTICLE-001`
- Target: `spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/REFINE-SEED-PROPOSAL.md`
- Mode: `lean`
- Emit: `both`
- Handoff: `codex-goal`
- Strict coverage: `pass`
- Session evidence path: `spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/context-builder`
- Run id: `arcanum-context-builder-20260527T073920Z`

## Obligation Matrix

| ID | Obligation | Required Evidence | Status |
| --- | --- | --- | --- |
| `O1-target-output` | Define the downstream draft target and expected article output. | Seed target, article shape, first SWU. | `covered` |
| `O2-schema-control` | Preserve `text-intent-substrate.yaml` as schema control surface. | YAML metadata, composition plan, draft artifact. | `covered` |
| `O3-reader-default` | Preserve primary reader as AI-curious creative builders. | Relevance core and audience decision. | `covered` |
| `O4-research-policy` | Preserve research-if-gap-appears and Harari citation policy. | Research decision and citation gap. | `covered` |
| `O5-non-goals` | Avoid publish/product-pitch/task-session execution scope creep. | Write scope and Whisper lifecycle. | `covered` |
| `O6-validation` | Carry validation checks into the handoff. | YAML validation and schema task candidate. | `covered` |
| `O7-artifact-update` | Produce both Markdown and JSON/index session evidence. | Context-builder command and skill contracts. | `covered` |

## Selected Excerpts

### `REFINE-SEED-PROPOSAL.md`

- Selectors: `#Target`, `#Article Shape`, `#Research Decision`, `#Write Scope`, `#Done Criteria`, `#Recommended First Task Session SWU`
- Obligations: `O1-target-output`, `O4-research-policy`, `O5-non-goals`, `O7-artifact-update`
- Evidence: The seed names the Substack research post, defines the reader change and success signal, permits only run-folder artifacts during refine, blocks publishing and unverified Harari claims, and identifies `SWU-WHISPER-ARTICLE-001` as the first drafting unit.

### `text-intent-substrate.yaml`

- Selectors: `metadata`, `source_context.citation_gap`, `author_objective`, `relevance_core`, `trajectory_core`, `transport_schema`, `composition_plan`, `draft_artifact`, `execution_policy`
- Obligations: `O2-schema-control`, `O3-reader-default`, `O4-research-policy`, `O6-validation`
- Evidence: The schema records `artifact_status: schema_defined`, primary public `AI-curious creative builders`, the citation gap policy, body-part sequence, validation checks, draft target, and task-session use policy.

### `WHISPER-SCHEMA.md`

- Selectors: `#Purpose`, `#Audience Decision`, `#Lifecycle Artifact Chain`, `#Pareto Consensus`, `#First Draft Plan`, `#Task Session Candidate`
- Obligations: `O2-schema-control`, `O3-reader-default`, `O6-validation`
- Evidence: The human schema explains the selected AI result, audience, lifecycle artifacts, Pareto consensus, body-part plan, and drafting rule for the Harari reference.

### `spells/whisper/README.md`

- Selectors: `#Purpose`, `#Artifact Lifecycle Contract`, `#Execution Phases`, `#Output Contract`
- Obligations: `O5-non-goals`, `O6-validation`
- Evidence: Whisper owns the composition lifecycle; task-session is only for bounded drafting, verification, or revision after the schema and composition plan are ready.

## Excluded Candidates

- `RUNTIME-HANDOFF.md` - excluded because it documents native refine orchestration and does not add article or handoff obligations.
- `stages/01-context-builder-retry.md` and `stages/01-context-builder-retry2.md` - excluded because they only record prior `codex-exec` output failure.
- Full repository search results - excluded because compact mode had full coverage from explicit run-folder and Whisper sources.

## Gaps And Resolutions

- `G1-harari-citation`: deferred. External research is not needed for the context pack. It becomes required only if a later draft uses Harari/Sapiens as a precise or source-backed claim.

## Runtime Notes

- Draft from the schema; do not rewrite the schema first.
- Translate Arcanum terms before relying on them as examples.
- Keep the draft in the run folder and preserve citation gaps as bracketed notes.
- Do not execute task-session from this context-builder run.

## Output Paths

- Handoff Markdown: `spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/GOAL-HANDOFF.md`
- Context Markdown: `spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/context-builder/CONTEXT-PACK.md`
- JSON/index: `spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/context-builder/evidence-index.json`
