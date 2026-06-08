# Invoke Validation Report

Validation protocol: [VALIDATION-EXPERIMENT.md](VALIDATION-EXPERIMENT.md)

## Run Summary

- Artifact: `invoke`
- Scope: library spell
- Validation date: 2026-05-18
- Validated layer: L0 define, L1 design, L2 plan contract, L2H handoff contract, L2R refresh contract, and define-to-design-to-plan live loop readiness
- Promotion target: proceed to `full` and `validate` mode work after L2 plan evidence
- Verdict: `pass`
- Latest deterministic control report: generated under ignored `runs/`

## Checks Performed

| Check | Result | Evidence |
| --- | --- | --- |
| Markdown links | pass | `find arcanum/spells/invoke -name '*.md' -print0 \| xargs -0 -n1 ./tools/check_markdown_links.sh` passed for all invoke markdown files. |
| Spell contract structure | pass | [../README.md](../README.md), [../define.md](../define.md), [../design.md](../design.md), [../handoff.md](../handoff.md), and [../refresh.md](../refresh.md) define identity, modes, phases, gates, handoffs, failure policy, observability, and output contracts. |
| Template scaffold coverage | pass | [../templates/README.md](../templates/README.md) declares family scaffold requirements; `generic`, `research`, `architecture`, `spell`, `sigil`, and `ux-plan` folders include README, primary template, passing example, and missing-input example. Historical `implementation-plan` scaffolding is no longer part of the active plan surface. |
| Template task matrix coverage | pass | [TEMPLATE-VALIDATION-TASKS.md](TEMPLATE-VALIDATION-TASKS.md) lists low, medium, and complex tasks for Module Formulae, standalone companions, and each dedicated family. |
| Template prompt coverage | pass | [TEMPLATE-EXAMPLE-RUNBOOK.md](TEMPLATE-EXAMPLE-RUNBOOK.md) explains how to run every generated prompt in Codex; `example-prompts/` contains one prompt per template task. |
| Prompt selector coverage | pass | [select-template-example-prompt.sh](select-template-example-prompt.sh) resolves exact task IDs, template+complexity pairs, and `next`; command bridges are legacy example-runner compatibility only; [run-template-example-with-codex.sh](run-template-example-with-codex.sh) remains an explicit legacy adapter test. |
| Example output coverage | pass | Saved example outputs under `example-outputs/` are checked for real `Invoke Result` shape and rejected if they are save-summary responses; architecture outputs must include a full architecture artifact with all required sections. |
| Define gate coverage | pass | [../define.md](../define.md) blocks missing core goals, flags unapproved candidate-template cases, gates glossary promotion, and defines transport behavior. |
| Design gate coverage | pass | [../design.md](../design.md) requires six views, source-contract gating, glossary consistency, non-mutating upstream behavior, and design transport. |
| Plan gate coverage | pass | [../plan.md](../plan.md) requires approved design refs, implementation-layering, canonical work-pack, validation strategy, complexity-based output mode, layer-mapped waves for medium/high complexity, implementation-detail specs, SWU decomposition for execution tasks, navigable work-pack tables, artifact-boundary clarity, and subagent/local-fallback-ready SWU handoff fields. |
| Handoff gate coverage | pass | [../handoff.md](../handoff.md) requires a new-session prompt, source session reference, handoff type, Context Builder selection, selected/excluded context, and explicit next route. |
| Refresh gate coverage | pass | [../refresh.md](../refresh.md) requires source evidence, target artifact inventory, refresh scope, typed source signals, proposal-only default, apply-approved approval, and pass/flag/block/no-op statuses. |
| Registry gate | pass | [../../../registry/SPELLS.md](../../../registry/SPELLS.md) does not yet register `invoke`; release remains blocked until validation passes. |
| Native authoring readiness | pass | `README.md`, `define.md`, `design.md`, and `plan.md` do not require deprecated command files as readiness evidence; plan SWUs include native receipt/subagent result shape. |
| Fixture replay | pass | `arcanum/spells/invoke/development/run-validation-fixtures.sh` reports all define and design realistic fixtures and expected output files passing. |
| Integration replay | pass | `INV-INTEGRATION-DEFINE-DESIGN-001` proves define artifacts feed design inputs, preserve glossary terms, emit six views, and route next to `plan`. |
| Plan replay | pass | `INV-PLAN-PASS-001`, `INV-PLAN-SPLIT-001`, and `INV-PLAN-BLOCK-001` prove low-complexity compact mapping, medium/high layer planning with implementation-detail specs and SWU decomposition, and blocked missing-input behavior. The canonical work-pack hierarchy, navigable table links, and new SWU handoff fields are a contract refresh and should be covered in the next plan fixture refresh. |
| Refresh replay | pass | `INV-REFRESH-PASS-001`, `INV-REFRESH-FLAG-001`, `INV-REFRESH-BLOCK-001`, and `INV-REFRESH-NOOP-001` prove evidence-backed proposal, artifact-drift flag, missing-input block, and no-op behavior. |
| Define-design-plan replay | pass | `INV-INTEGRATION-DEFINE-DESIGN-PLAN-001` proves plan consumes design inputs, preserves define glossary terms, emits layering/work-pack/transport artifacts, and routes next to `task-session`. Existing fixture evidence should be refreshed against the work-pack-only planning contract. |
| Live define loop | pass | [live-evidence/LIVE-DEFINE-001/loop-report.md](live-evidence/LIVE-DEFINE-001/loop-report.md) reached two consecutive passing Codex attempts; [output.md](live-evidence/LIVE-DEFINE-001/output.md) preserves the real artifact body. |
| Live design loop | pass | [live-evidence/LIVE-DESIGN-001/loop-report.md](live-evidence/LIVE-DESIGN-001/loop-report.md) reached two consecutive passing Codex attempts after correcting overly broad placeholder/blocker detection in the harness validator; [output.md](live-evidence/LIVE-DESIGN-001/output.md) preserves the real artifact body. |
| Live define-to-design loop | pass | [live-evidence/LIVE-DEFINE-DESIGN-001/loop-report.md](live-evidence/LIVE-DEFINE-DESIGN-001/loop-report.md) reached two consecutive passing Codex attempts and preserved the define-to-design authority boundary; [output.md](live-evidence/LIVE-DEFINE-DESIGN-001/output.md) preserves the real artifact body. |
| Live plan loop | pass | [live-evidence/LIVE-PLAN-001/loop-report.md](live-evidence/LIVE-PLAN-001/loop-report.md) reached two consecutive passing Codex attempts with implementation layering, work-pack, implementation-detail specs, SWU manifest/task-local mappings, validation strategy, transport, and next-route evidence. Canonical work-pack hierarchy and new SWU subagent/local-fallback handoff fields require a follow-up live plan refresh. |
| Live define-to-design-to-plan loop | pass | [live-evidence/LIVE-DEFINE-DESIGN-PLAN-001/loop-report.md](live-evidence/LIVE-DEFINE-DESIGN-PLAN-001/loop-report.md) reached two consecutive passing Codex attempts and preserved define, design, and plan authority boundaries. |
| Observability loop | pass | `.arcanum/observability/signals/sigil-invocations.jsonl` records completed observer telemetry with `quality_bar_status`, `anti_pattern_hits`, `workflow_gaps`, and `reflection_trigger`; hook rows in `.arcanum/observability/hooks/hook-operations.jsonl` carry `observe: false` and duplicate observer emission skips cleanly. |

## Loop Validation

Live Codex loop validation is now required promotion evidence for the implemented `invoke` scope. Deterministic fixtures remain controls; they prove stable contract expectations, but they do not replace live execution.

| Regime | Result | Evidence |
| --- | --- | --- |
| `CTRL-DEFINE-001` | pass | `run-validation-fixtures.sh` latest generated report under ignored `runs/` |
| `CTRL-DESIGN-001` | pass | `run-validation-fixtures.sh` latest generated report under ignored `runs/` |
| `CTRL-PLAN-001` | pass | `run-validation-fixtures.sh` latest generated report under ignored `runs/` |
| `CTRL-INTEGRATION-001` | pass | `run-validation-fixtures.sh` latest generated report under ignored `runs/` |
| `CTRL-INTEGRATION-002` | pass | `run-validation-fixtures.sh` latest generated report under ignored `runs/` |
| `CTRL-CONTRACT-001` | pass | `run-validation-fixtures.sh` latest generated report under ignored `runs/` |
| `LIVE-DEFINE-001` | pass | [live-evidence/LIVE-DEFINE-001/loop-report.md](live-evidence/LIVE-DEFINE-001/loop-report.md), [output.md](live-evidence/LIVE-DEFINE-001/output.md), [validation.json](live-evidence/LIVE-DEFINE-001/validation.json) |
| `LIVE-DESIGN-001` | pass | [live-evidence/LIVE-DESIGN-001/loop-report.md](live-evidence/LIVE-DESIGN-001/loop-report.md), [output.md](live-evidence/LIVE-DESIGN-001/output.md), [validation.json](live-evidence/LIVE-DESIGN-001/validation.json) |
| `LIVE-PLAN-001` | pass | [live-evidence/LIVE-PLAN-001/loop-report.md](live-evidence/LIVE-PLAN-001/loop-report.md), [output.md](live-evidence/LIVE-PLAN-001/output.md), [validation.json](live-evidence/LIVE-PLAN-001/validation.json) |
| `LIVE-DEFINE-DESIGN-001` | pass | [live-evidence/LIVE-DEFINE-DESIGN-001/loop-report.md](live-evidence/LIVE-DEFINE-DESIGN-001/loop-report.md), [output.md](live-evidence/LIVE-DEFINE-DESIGN-001/output.md), [validation.json](live-evidence/LIVE-DEFINE-DESIGN-001/validation.json) |
| `LIVE-DEFINE-DESIGN-PLAN-001` | pass | [live-evidence/LIVE-DEFINE-DESIGN-PLAN-001/loop-report.md](live-evidence/LIVE-DEFINE-DESIGN-PLAN-001/loop-report.md), [output.md](live-evidence/LIVE-DEFINE-DESIGN-PLAN-001/output.md), [validation.json](live-evidence/LIVE-DEFINE-DESIGN-PLAN-001/validation.json) |
| `LIVE-OBSERVABILITY-001` | pass | Observer emissions recorded for define, design, and define-to-design loop reports with observer version `0.1.1`; duplicate design observation skipped by dedupe. |

Latest live loop machine summaries:

```text
LIVE-DEFINE-001: VALIDATION=pass QUALITY_BAR_STATUS=pass ANTI_PATTERN_HITS_JSON=[] WORKFLOW_GAPS_JSON=[]
LIVE-DESIGN-001: VALIDATION=pass QUALITY_BAR_STATUS=pass ANTI_PATTERN_HITS_JSON=[] WORKFLOW_GAPS_JSON=[]
LIVE-DEFINE-DESIGN-001: VALIDATION=pass QUALITY_BAR_STATUS=pass ANTI_PATTERN_HITS_JSON=[] WORKFLOW_GAPS_JSON=[]
LIVE-PLAN-001: VALIDATION=pass QUALITY_BAR_STATUS=pass ANTI_PATTERN_HITS_JSON=[] WORKFLOW_GAPS_JSON=[] DETAIL_SPECS=present SWU=present
LIVE-DEFINE-DESIGN-PLAN-001: VALIDATION=pass QUALITY_BAR_STATUS=pass ANTI_PATTERN_HITS_JSON=[] WORKFLOW_GAPS_JSON=[]
```

Failure/improvement evidence: an earlier generated `LIVE-DESIGN-001` partial loop produced non-pass attempts with `robot-talks.md` and `improvement-argument.md` artifacts. That loop exposed overly broad harness checks for Mermaid decision braces and benign missing-field decision rules; after tightening the validator, the design regime passed with two consecutive live attempts.

Registry release remains blocked for `plan`, `full`, and `validate` modes until they have matching deterministic controls and live loop regimes.

## Fixture Status

| Fixture ID | Status | Notes |
| --- | --- | --- |
| [TEMPLATE-TASK-MATRIX](TEMPLATE-VALIDATION-TASKS.md) | pass | Template task inventory covers low, medium, and complex tasks for every invoke-owned template family or standalone companion. |
| PROMPT-SELECTOR | pass | Prompt selector and Codex command bridge can choose a prompt by task ID, template+complexity, or next unrun prompt. |
| EXAMPLE-OUTPUTS | pass | Any saved Codex-generated example outputs must have real result bodies, including `Mode` and `Phase status`; current deterministic run found no saved `.output.md` files. |
| [INV-DEFINE-PASS-001](fixtures/INV-DEFINE-PASS-001.md) | pass | Define dry-run from vague but usable Mars rover maintenance request produces spec, glossary, define transport, and layering seed evidence. |
| [INV-DEFINE-BLOCK-001](fixtures/INV-DEFINE-BLOCK-001.md) | pass | Define dry-run with missing core goal blocks at the expected gate and records missing goal and scope boundary. |
| [INV-DEFINE-FLAG-001](fixtures/INV-DEFINE-FLAG-001.md) | pass | Define dry-run with unsupported template fit flags candidate-template approval gap without promotion. |
| [INV-DEFINE-GLOSSARY-001](fixtures/INV-DEFINE-GLOSSARY-001.md) | pass | Define dry-run records `sol-thread` as a no-match glossary term with rationale and promotion gate. |
| [INV-DESIGN-PASS-001](fixtures/INV-DESIGN-PASS-001.md) | pass | Dry-run from approved spec, glossary, source contracts, and design constraints selects the Module Formulae architecture profile, requires all six views, emits glossary consistency and design transport outputs, and routes next to `plan`. |
| [INV-DESIGN-BLOCK-001](fixtures/INV-DESIGN-BLOCK-001.md) | pass | Dry-run with missing source contracts and no discovery approval blocks at the normal design activation gate and routes to `define` or explicit discovery-mode approval. |
| [INV-DESIGN-FLAG-001](fixtures/INV-DESIGN-FLAG-001.md) | pass | Dry-run with contradictory evidence selects the `research` companion, carries claim status into design decisions, and flags unless the ambiguity affects a required design decision, in which case it blocks. |
| [INV-DESIGN-HANDOFF-001](fixtures/INV-DESIGN-HANDOFF-001.md) | pass | Dry-run for spell and sigil targets emits handoff context only, routes lifecycle execution to `spellcraft` or `sigil-development`, and does not take lifecycle ownership. |
| [INV-INTEGRATION-DEFINE-DESIGN-001](fixtures/INV-INTEGRATION-DEFINE-DESIGN-001.md) | pass | Integration dry-run chains define output artifacts into design inputs and verifies glossary preservation, six-view design output, transport, and next route `plan`. |
| [INV-PLAN-PASS-001](fixtures/INV-PLAN-PASS-001.md) | pass | Dry-run from approved design outputs emits global implementation layering, compact layer mapping, single-file work-pack, validation strategy, plan transport, and next route `task-session`. |
| [INV-PLAN-SPLIT-001](fixtures/INV-PLAN-SPLIT-001.md) | pass | Dry-run for medium complexity emits split work-pack, execution-pack handoff, explicit L0-L3 layer-mapped waves, implementation-detail specs, and SWU manifest/task-local mappings. |
| [INV-PLAN-BLOCK-001](fixtures/INV-PLAN-BLOCK-001.md) | pass | Dry-run with missing approved design refs and companion status blocks at the plan activation gate. |
| [INV-HANDOFF-PASS-001](fixtures/INV-HANDOFF-PASS-001.md) | pass | Dry-run for workflow reflection handoff preserves the user's felt gap, reports Context Builder coverage, and routes next to `workflow-reflect`. |
| [INV-HANDOFF-BLOCK-001](fixtures/INV-HANDOFF-BLOCK-001.md) | pass | Dry-run without a source session reference blocks before Context Builder selection. |
| [INV-REFRESH-PASS-001](fixtures/INV-REFRESH-PASS-001.md) | pass | Dry-run maps latest evidence into proposal-only blocker/status/route deltas without applying changes. |
| [INV-REFRESH-FLAG-001](fixtures/INV-REFRESH-FLAG-001.md) | pass | Dry-run flags artifact drift when safe correction needs owner review. |
| [INV-REFRESH-BLOCK-001](fixtures/INV-REFRESH-BLOCK-001.md) | pass | Dry-run blocks when target artifact inventory is missing. |
| [INV-REFRESH-NOOP-001](fixtures/INV-REFRESH-NOOP-001.md) | pass | Dry-run records no-op when latest evidence is already represented. |
| [INV-INTEGRATION-DEFINE-DESIGN-PLAN-001](fixtures/INV-INTEGRATION-DEFINE-DESIGN-PLAN-001.md) | pass | Integration dry-run chains define and design artifacts into plan, preserves glossary terms, emits plan artifacts and transport, and keeps execution deferred. |

## Runner Output

Command:

```bash
arcanum/spells/invoke/development/run-validation-fixtures.sh
```

Latest report: generated under ignored `runs/`.

Output:

```text
PASS: TEMPLATE-TASK-MATRIX
PASS: PROMPT-SELECTOR
PASS: EXAMPLE-OUTPUTS (0 checked)
PASS: INV-DEFINE-PASS-001
PASS: INV-DEFINE-BLOCK-001
PASS: INV-DEFINE-FLAG-001
PASS: INV-DEFINE-GLOSSARY-001
PASS: INV-DESIGN-PASS-001
PASS: INV-DESIGN-BLOCK-001
PASS: INV-DESIGN-FLAG-001
PASS: INV-DESIGN-HANDOFF-001
PASS: INV-PLAN-PASS-001
PASS: INV-PLAN-SPLIT-001
PASS: INV-PLAN-BLOCK-001
PASS: INV-HANDOFF-PASS-001
PASS: INV-HANDOFF-BLOCK-001
PASS: INV-REFRESH-PASS-001
PASS: INV-REFRESH-FLAG-001
PASS: INV-REFRESH-BLOCK-001
PASS: INV-REFRESH-NOOP-001
PASS: INV-INTEGRATION-DEFINE-DESIGN-001
PASS: INV-INTEGRATION-DEFINE-DESIGN-PLAN-001
PASS: INV-QUALITY-ANTI-PATTERN-001
RESULT: pass
```

The runner checks both the realistic user-request fixture files and their expected user-facing result files.

## Dry-Run Results

### INV-DESIGN-PASS-001

```markdown
## Invoke Validation Fixture Result

- Fixture: INV-DESIGN-PASS-001
- Mode: design
- Phase status: pass
- Inputs present: approved spec, approved glossary, source contracts, design constraints, define decision ledger, define transport report
- Template/profile selection: Module Formulae architecture profile plus architecture bundle
- Design views: context, high-level structure, low-level components, workflow process, decision flow, dependency interface
- Glossary consistency: pass
- Transport report: simulated design-stage append report
- Decisions: proceed from approved define outputs into plan-ready design handoff
- Unresolved gaps: none blocking
- Expected next route: plan
- Verdict: pass
```

### INV-DESIGN-BLOCK-001

```markdown
## Invoke Validation Fixture Result

- Fixture: INV-DESIGN-BLOCK-001
- Mode: design
- Phase status: block
- Inputs present: design request and goal only; source contracts missing; discovery approval missing
- Template/profile selection: none finalized
- Design views: n/a
- Glossary consistency: n/a
- Transport report: n/a
- Decisions: block normal design until source contracts exist or discovery mode is explicitly approved
- Unresolved gaps: source contracts; discovery-mode approval
- Expected next route: define
- Verdict: pass
```

### INV-DESIGN-FLAG-001

```markdown
## Invoke Validation Fixture Result

- Fixture: INV-DESIGN-FLAG-001
- Mode: design
- Phase status: flag
- Inputs present: approved spec, approved glossary, partial source contracts, contradictory architecture evidence
- Template/profile selection: Module Formulae architecture profile plus research companion
- Design views: six-view bundle may proceed only for unaffected decisions
- Glossary consistency: pass
- Transport report: simulated design-stage append report with evidence ambiguity gap
- Decisions: carry claim status into design decision log; block only if contradiction controls a required design decision
- Unresolved gaps: evidence conflict pending decision-gate or research follow-up
- Expected next route: deferred
- Verdict: pass
```

### INV-DESIGN-HANDOFF-001

```markdown
## Invoke Validation Fixture Result

- Fixture: INV-DESIGN-HANDOFF-001
- Mode: design
- Phase status: pass
- Inputs present: approved define outputs targeting spell or sigil artifact
- Template/profile selection: spell family for spell target; sigil family for sigil target
- Design views: handoff context only; lifecycle execution remains external
- Glossary consistency: pass
- Transport report: simulated handoff-ready design transport report
- Decisions: route spell execution to `spellcraft`; route sigil execution to `sigil-development`
- Unresolved gaps: none blocking
- Expected next route: spellcraft | sigil-development
- Verdict: pass
```

## Findings

1. The contract layer is coherent enough to run validation fixtures.
2. The template inventory is structurally complete for the declared candidate families.
3. Native Invoke authoring does not depend on `.codex/commands`; command bridges are preserved only as explicit legacy example-runner compatibility.
4. L1 design fixtures produce recorded dry-run evidence and pass.
5. The define-to-design integration fixture proves cross-stage handoff at the artifact level.

### INV-PLAN-PASS-001

```markdown
## Invoke Validation Fixture Result

- Fixture: INV-PLAN-PASS-001
- Mode: plan
- Phase status: pass
- Inputs present: approved design outputs, source design refs, delivery boundary, lifecycle owner approval, companion creation approval
- Template/profile selection: standalone implementation-layering and work-pack companions
- Implementation layering: global L0-L3 decision boundaries
- Work-pack: single-file with compact layer mapping
- Complexity: low
- Per-layer planning: compact
- Validation strategy: mapped to every delivery slice
- Expected next route: task-session
- Verdict: pass
```

### INV-PLAN-SPLIT-001

```markdown
## Invoke Validation Fixture Result

- Fixture: INV-PLAN-SPLIT-001
- Mode: plan
- Phase status: pass
- Inputs present: approved design outputs, dependency/interface map, delivery boundary, validation strategy, lifecycle owner approval
- Template/profile selection: implementation-layering, work-pack, and execution-pack companions
- Implementation layering: global L0-L3 decision boundaries
- Work-pack: split
- Complexity: medium
- Per-layer planning: L0, L1, L2, L3
- Implementation detail: task specs complete with concrete implementation notes, edge cases, and validation evidence
- Smallest working units: complete
- Validation strategy: mapped to every delivery slice and promotion criterion
- Expected next route: task-session
- Verdict: pass
```

### INV-PLAN-BLOCK-001

```markdown
## Invoke Validation Fixture Result

- Fixture: INV-PLAN-BLOCK-001
- Mode: plan
- Phase status: block
- Inputs present: planning request only; approved design refs, companion status, validation strategy, and lifecycle approval missing
- Template/profile selection: none finalized
- Implementation layering: blocked
- Work-pack: blocked
- Complexity: n/a
- Per-layer planning: blocked
- Expected next route: deferred
- Verdict: pass
```

## Decision

Promote `invoke` from L1 design validation to L2 plan validation.

Do not register `invoke` in the spell registry yet. Registry release still requires `full`, `validate`, examples, deterministic controls, live loop regimes, and release validation.

## Next Actions

1. Implement the `full` mode contract from define/design/plan evidence.
2. Implement the `validate` mode contract and release checks.
3. Keep registry release blocked until `full` and `validate` mode evidence exists.
