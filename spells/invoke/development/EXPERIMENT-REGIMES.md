# Invoke Experiment Regimes

This document is the human-readable control sheet for revalidating the implemented `invoke` scope.

The experiment validates:

- `define` as a standalone phase,
- `design` as a standalone phase,
- `plan` as a standalone phase,
- `handoff` as a standalone session/thread handoff phase,
- `refresh` as a standalone artifact refresh phase,
- `define -> design` as an integration chain,
- `define -> design -> plan` as an integration chain,
- Quality Bar and Anti-Pattern behavior,
- required live Codex execution for the current implemented scope.

Generated evidence belongs under ignored folders:

- `development/example-outputs/`
- `development/example-runs/`
- `development/experiment-loops/`
- `development/runs/`

Durable evidence belongs under tracked fixtures, prompts, and future loop regime files:

- `development/fixtures/`
- `development/example-prompts/`
- `development/regimes/`
- this regimes document.

## Command Sequence

Run deterministic controls first. These are controls, not promotion evidence:

```bash
arcanum/spells/invoke/development/run-validation-fixtures.sh
arcanum/arcana/experiment-harness/scripts/validate-harness.sh arcanum/spells/invoke
```

Then run the live regimes as the blocking promotion evidence:

```bash
arcanum/arcana/experiment-harness/scripts/loop-harness.sh arcanum/spells/invoke LIVE-DEFINE-001
arcanum/arcana/experiment-harness/scripts/loop-harness.sh arcanum/spells/invoke LIVE-DESIGN-001
arcanum/arcana/experiment-harness/scripts/loop-harness.sh arcanum/spells/invoke LIVE-PLAN-001
arcanum/arcana/experiment-harness/scripts/loop-harness.sh arcanum/spells/invoke LIVE-DEFINE-DESIGN-001
arcanum/arcana/experiment-harness/scripts/loop-harness.sh arcanum/spells/invoke LIVE-DEFINE-DESIGN-PLAN-001
arcanum/arcana/experiment-harness/scripts/loop-harness.sh arcanum/spells/invoke LIVE-OBSERVABILITY-001
```

Direct single-run Codex prompts remain useful for development smoke tests:

```bash
RERUN=1 arcanum/spells/invoke/development/run-template-example-with-codex.sh invoke-define-live-pass
RERUN=1 arcanum/spells/invoke/development/run-template-example-with-codex.sh invoke-design-live-pass
RERUN=1 arcanum/spells/invoke/development/run-template-example-with-codex.sh invoke-plan-live-pass
RERUN=1 arcanum/spells/invoke/development/run-template-example-with-codex.sh invoke-define-design-live-pass
RERUN=1 arcanum/spells/invoke/development/run-template-example-with-codex.sh invoke-define-design-plan-live-pass
```

Finally emit observability from the latest live loop report:

```bash
latest_report="$(find arcanum/spells/invoke/development/experiment-loops -name loop-report.md | sort | tail -n 1)"
arcanum/arcana/experiment-harness/scripts/observe-harness.sh arcanum/spells/invoke "$latest_report"
```

The observer telemetry must include:

- `quality_bar_status`,
- `anti_pattern_hits`,
- `workflow_gaps`,
- `reflection_trigger`.

## CTRL-DEFINE-001: Define Phase Control

Goal: prove `invoke define` handles useful, missing, unsupported, and glossary-sensitive input shapes.

Inputs:

- `fixtures/INV-DEFINE-PASS-001.md`
- `fixtures/INV-DEFINE-BLOCK-001.md`
- `fixtures/INV-DEFINE-FLAG-001.md`
- `fixtures/INV-DEFINE-GLOSSARY-001.md`

Expected outputs:

- `INV-DEFINE-PASS-001.expected.md` returns `Phase status: pass`.
- `INV-DEFINE-BLOCK-001.expected.md` returns `Phase status: block`.
- `INV-DEFINE-FLAG-001.expected.md` returns `Phase status: flag`.
- `INV-DEFINE-GLOSSARY-001.expected.md` records no-match glossary promotion as gated.

Pass criteria:

- missing core goal blocks,
- candidate template creation flags when unapproved,
- glossary promotion is never automatic,
- define transport evidence is present.

Failure examples:

- vague input passes without naming missing scope,
- unsupported template is promoted silently,
- new glossary terms are treated as approved definitions.

Evidence paths:

- tracked expected outputs in `development/fixtures/`,
- generated control report in `development/runs/`.

## CTRL-DESIGN-001: Design Phase Control

Goal: prove `invoke design` consumes approved define outputs and produces a governed six-view design bundle.

Inputs:

- `fixtures/INV-DESIGN-PASS-001.md`
- `fixtures/INV-DESIGN-BLOCK-001.md`
- `fixtures/INV-DESIGN-FLAG-001.md`
- `fixtures/INV-DESIGN-HANDOFF-001.md`

Expected outputs:

- pass when approved spec, glossary, source contracts, and constraints exist,
- block when source contracts are missing and discovery mode is not approved,
- flag or block when contradictory evidence controls a design decision,
- hand off spell and sigil lifecycle work to `spellcraft` or `sigil-development`.

Pass criteria:

- all six design views are represented,
- glossary consistency is explicit,
- dependency/interface notes and risks are present,
- design mode does not create work-pack tasks,
- downstream spell/sigil contracts are not mutated from design mode.

Failure examples:

- missing source contracts are treated as approved,
- design silently performs deferred `plan` or `full` behavior,
- design edits spell or sigil contracts instead of producing handoff context.

Evidence paths:

- tracked expected outputs in `development/fixtures/`,
- generated control report in `development/runs/`.

## CTRL-INTEGRATION-001: Define To Design Control

Goal: prove design consumes define artifacts without inventing upstream authority.

Input:

- `fixtures/INV-INTEGRATION-DEFINE-DESIGN-001.md`

Expected outputs:

- define expected output names spec, glossary, and define transport artifacts,
- design expected output names architecture, glossary consistency, and design transport artifacts,
- architecture preserves define glossary terms,
- design routes next to `plan`.

Pass criteria:

- design consumes the approved define output,
- glossary terms remain consistent,
- unresolved define gaps remain visible,
- design emits six views and transport evidence.

Failure examples:

- design introduces source contracts not present in define evidence,
- design removes glossary uncertainty,
- design routes to implementation without `plan`.

Evidence paths:

- tracked integration fixture bundle in `development/fixtures/`,
- generated control report in `development/runs/`.

## CTRL-PLAN-001: Plan Phase Control

Goal: prove `invoke plan` consumes approved design outputs and produces governed planning artifacts without executing implementation.

Inputs:

- `fixtures/INV-PLAN-PASS-001.md`
- `fixtures/INV-PLAN-SPLIT-001.md`
- `fixtures/INV-PLAN-BLOCK-001.md`

Expected outputs:

- pass for low complexity with global implementation layering, compact layer mapping, single-file work-pack, validation strategy, and plan transport,
- pass for medium/high complexity with split work-pack, execution-pack handoff, and explicit layer-mapped waves,
- block when approved design refs or required companions are missing.

Pass criteria:

- approved design refs are required,
- implementation-layering and canonical work-pack companions are present,
- low complexity keeps compact layer mapping,
- medium/high complexity includes L0-L3 layer-mapped waves,
- medium/high complexity includes implementation-detail specs for execution tasks,
- medium/high complexity includes SWU manifest and task-local SWU mappings,
- SWUs include dependencies, write scope, done criteria, validation, execution-owner recommendation, and handoff notes,
- task-board task IDs and SWU parent tasks link to task contracts when split task files exist,
- SWU rows include source context links needed by workers,
- algorithmic or domain-logic tasks include ordered rules, pseudocode, state-transition, classification, data-flow, edge-case, or failure-mode details,
- validation strategy is mapped to delivery slices,
- plan mode does not execute tasks.

Failure examples:

- plan proceeds without approved design refs,
- medium/high complexity omits layer-mapped waves,
- task descriptions stay vague, such as "implement this bundle", without implementation details,
- medium/high work-packs omit SWU decomposition,
- SWUs omit dependencies, done criteria, validation, or execution-owner handoff fields,
- work-pack tables require repository searching because task IDs, parent tasks, or source context are not linked,
- duplicate artifacts claim the same task, state, or SWU authority,
- split task files are placeholders rather than useful task-local execution contracts,
- an algorithmic task lacks inputs, outputs, ordered rules, edge cases, and validation evidence,
- layer promotion is based on preference rather than evidence,
- output executes implementation tasks.

Evidence paths:

- tracked expected outputs in `development/fixtures/`,
- generated control report in `development/runs/`.

## CTRL-HANDOFF-001: Session Handoff Control

Goal: prove `invoke handoff` creates a new session/thread artifact from a prompt, source session reference, and Context Builder selection.

Inputs:

- `fixtures/INV-HANDOFF-PASS-001.md`
- `fixtures/INV-HANDOFF-BLOCK-001.md`

Expected outputs:

- pass when the prompt, source session reference, handoff type, and Context Builder coverage exist,
- block when the source session reference is missing,
- preserve the user's felt workflow gap for reflection handoffs,
- route workflow-reflection handoffs to `workflow-reflect`.

Pass criteria:

- prompt and source session reference are mandatory,
- handoff type is explicit or selected with rationale,
- Context Builder coverage is reported,
- selected context maps to obligations from the new prompt and handoff type,
- irrelevant source-session history is excluded rather than copied forward,
- next route is explicit.

Failure examples:

- whole-session transcript is treated as a context pack,
- handoff proceeds without a source session reference,
- workflow-reflection gap is rewritten as a generic improvement request,
- handoff mutates the target sigil, spell, or work-pack instead of preparing a new thread artifact.

Evidence paths:

- tracked expected outputs in `development/fixtures/`,
- generated control report in `development/runs/`.

## CTRL-REFRESH-001: Artifact Refresh Control

Goal: prove `invoke refresh` maps latest session evidence to scoped artifact deltas without executing target work or silently mutating artifacts.

Inputs:

- `fixtures/INV-REFRESH-PASS-001.md`
- `fixtures/INV-REFRESH-FLAG-001.md`
- `fixtures/INV-REFRESH-BLOCK-001.md`
- `fixtures/INV-REFRESH-NOOP-001.md`

Expected outputs:

- pass when evidence-backed proposal-only deltas exist,
- flag when artifact drift exists and safe correction needs owner review,
- block when source evidence or target artifact inventory is missing,
- no-op when latest evidence is already represented.

Pass criteria:

- every proposed or applied change maps to a refresh signal,
- proposal-only is the default mutation mode,
- apply-approved requires explicit approval,
- setup proof is not promoted into completion proof,
- no-op is a first-class phase status,
- next route is explicit.

Failure examples:

- refresh applies changes without approval,
- refresh infers completion from weak evidence,
- missing target inventory proceeds,
- no-op reruns cause artifact churn,
- artifact drift is resolved without owner review.

Evidence paths:

- tracked expected outputs in `development/fixtures/`,
- generated control report in `development/runs/`.

## CTRL-INTEGRATION-002: Define To Design To Plan Control

Goal: prove plan consumes design artifacts without inventing upstream authority.

Input:

- `fixtures/INV-INTEGRATION-DEFINE-DESIGN-PLAN-001.md`

Expected outputs:

- define expected output names spec, glossary, and define transport artifacts,
- design expected output names architecture, glossary consistency, and design transport artifacts,
- plan expected output names implementation layering, canonical work-pack, validation strategy, and plan transport artifacts,
- plan preserves define glossary terms through design authority,
- plan includes implementation details for task-level execution handoff,
- plan routes next to `task-session`.

Pass criteria:

- plan consumes approved design output,
- implementation layering contains global L0-L3 decision boundaries,
- low-complexity work-pack contains compact layer mapping,
- validation strategy is present,
- implementation detail is explicit enough that task-session does not receive vague bundle-level task labels,
- execution remains deferred.

Failure examples:

- plan introduces design approvals not present in evidence,
- plan removes glossary uncertainty from prior phases,
- plan emits vague task bundles without implementation details,
- plan executes tasks or mutates source code.

Evidence paths:

- tracked integration fixture bundle in `development/fixtures/`,
- generated control report in `development/runs/`.

## CTRL-CONTRACT-001: Quality Bar And Anti-Patterns Control

Goal: prove experiment validation distinguishes real success from polished-looking boundary violations.

Input:

- `fixtures/INV-QUALITY-ANTI-PATTERN-001.md`

Expected output:

- `fixtures/INV-QUALITY-ANTI-PATTERN-001.expected.md`

Pass criteria:

- pass, partial, and fail Quality Bar classifications are represented,
- Anti-Pattern hits can flag or block,
- expected telemetry fields are present.

Failure examples:

- save-summary output passes,
- output claims pass while naming missing required source contracts,
- anti-pattern hits are not exposed to observer telemetry.

Evidence paths:

- tracked quality fixture and expected output,
- generated report machine summary.

## LIVE-DEFINE-001: Live Codex Define Loop

Goal: prove a real Codex execution produces a user-facing `Invoke Result` for define mode.

Input:

- `example-prompts/invoke-define-live-pass.md`

Command:

```bash
arcanum/arcana/experiment-harness/scripts/loop-harness.sh arcanum/spells/invoke LIVE-DEFINE-001
```

Expected output:

- `example-outputs/invoke-define-live-pass.output.md`

Pass criteria:

- output contains `## Invoke Result`,
- output contains `Mode: define`,
- output contains `Phase status: pass`,
- output includes spec, glossary, define transport, and next route evidence,
- output is not a save-summary.

Failure examples:

- Codex CLI unavailable,
- output missing or empty,
- output says only that a file was saved,
- output lacks spec or glossary evidence.

## LIVE-DESIGN-001: Live Codex Design Loop

Goal: prove a real Codex execution produces a governed design artifact from approved define/source-contract inputs.

Input:

- `example-prompts/invoke-design-live-pass.md`

Command:

```bash
arcanum/arcana/experiment-harness/scripts/loop-harness.sh arcanum/spells/invoke LIVE-DESIGN-001
```

Expected output:

- `example-outputs/invoke-design-live-pass.output.md`

Pass criteria:

- output contains `## Invoke Result`,
- output contains `Mode: design`,
- output contains `Phase status: pass`,
- output includes source contracts,
- output includes six design views,
- output includes risks, dependency/interface notes, glossary consistency, design transport, and next route evidence,
- output is not a save-summary.

Failure examples:

- design proceeds without approved inputs,
- output omits one or more design views,
- output mutates downstream spell/sigil contracts,
- output creates work-pack tasks.

## LIVE-PLAN-001: Live Codex Plan Loop

Goal: prove a real Codex execution produces governed planning artifacts from approved design outputs.

Input:

- `example-prompts/invoke-plan-live-pass.md`

Command:

```bash
arcanum/arcana/experiment-harness/scripts/loop-harness.sh arcanum/spells/invoke LIVE-PLAN-001
```

Expected output:

- `example-outputs/invoke-plan-live-pass.output.md`

Pass criteria:

- output contains `## Invoke Result`,
- output contains `Mode: plan`,
- output contains `Phase status: pass`,
- output includes implementation layering, canonical work-pack, validation strategy, blocker ledger, plan transport, and next route evidence,
- medium/high complexity output includes L0-L3 layer-mapped waves,
- medium/high complexity output includes SWU manifest and task-local SWU lists,
- medium/high complexity output includes subagent/local-fallback-ready SWU handoff fields,
- output links task-board task IDs, SWU parent tasks, and SWU source context for split work-packs,
- output is not a save-summary.

Failure examples:

- output plans without approved design refs,
- output omits implementation-layering or work-pack evidence,
- output omits layer-mapped waves for medium/high complexity,
- output omits SWU dependencies, done criteria, validation, execution owner, or handoff note,
- output omits task-contract or source-context links in split work-pack tables,
- output creates split task files that are not useful execution contracts,
- output claims task execution.

## LIVE-DEFINE-DESIGN-001: Live Codex Define To Design Loop

Goal: prove a real Codex execution can produce an inspectable define-to-design chain in one output.

Input:

- `example-prompts/invoke-define-design-live-pass.md`

Command:

```bash
arcanum/arcana/experiment-harness/scripts/loop-harness.sh arcanum/spells/invoke LIVE-DEFINE-DESIGN-001
```

Expected output:

- `example-outputs/invoke-define-design-live-pass.output.md`

Pass criteria:

- output contains `## Invoke Result`,
- output contains define and design phase sections,
- define section includes spec, glossary, and define transport evidence,
- design section includes approved source contract references, six views, glossary consistency, design transport, and next route,
- output states that design consumes define outputs instead of inventing approvals.

Failure examples:

- design output does not reference define artifacts,
- source contracts are invented or silently approved,
- output collapses the chain into a summary instead of real artifacts.

## LIVE-DEFINE-DESIGN-PLAN-001: Live Codex Define To Design To Plan Loop

Goal: prove a real Codex execution can produce an inspectable define-to-design-to-plan chain in one output.

Input:

- `example-prompts/invoke-define-design-plan-live-pass.md`

Command:

```bash
arcanum/arcana/experiment-harness/scripts/loop-harness.sh arcanum/spells/invoke LIVE-DEFINE-DESIGN-PLAN-001
```

Expected output:

- `example-outputs/invoke-define-design-plan-live-pass.output.md`

Pass criteria:

- output contains `## Invoke Result`,
- output contains define, design, and plan phase sections,
- define section includes spec, glossary, and define transport evidence,
- design section includes approved source contract references, six views, glossary consistency, design transport, and next route,
- plan section includes global implementation-layering artifact, canonical work-pack, validation strategy, plan transport, and next route,
- output states that plan consumes approved design outputs instead of inventing approvals,
- output is not a save-summary.

Failure examples:

- plan output does not reference design artifacts,
- implementation-layering evidence is missing,
- output routes directly to execution without work-pack gates,
- output collapses the chain into a summary instead of real artifacts.

## LIVE-OBSERVABILITY-001: Live Observability Loop

Goal: prove the experiment harness can close the loop through telemetry and hook ledgers.

Input:

- latest loop report from one of the live regimes,
- repository observability package under `.arcanum/observability/`.

Command:

```bash
latest_report="$(find arcanum/spells/invoke/development/experiment-loops -name loop-report.md | sort | tail -n 1)"
arcanum/arcana/experiment-harness/scripts/observe-harness.sh arcanum/spells/invoke "$latest_report"
```

Pass criteria:

- capability telemetry includes `quality_bar_status`, `anti_pattern_hits`, `workflow_gaps`, and `reflection_trigger`,
- hook operation rows are recorded with `observe: false`,
- duplicate observer emissions are skipped,
- observer failures do not mutate generated outputs.
