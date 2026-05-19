# Sigil Handoff: Sigilcraft Session Process

## Sigil Identity

- Current canonical id: sigil-development
- Proposed user-facing name: Sigilcraft
- Proposed canonical id: sigilcraft
- Candidate tier: Arcana
- Current owning surface: arcana/sigil-development/
- Proposed owning surface: arcana/sigilcraft/ after explicit rename approval
- Lifecycle owner for this development session: sigil-development
- Compatibility expectation: keep `sigil-development` as an alias or compatibility route during migration.

## Define Intent Record

The development idea is that sigil work and spell work should behave like craft sessions, not isolated tasks. A craft session carries an idea from early refinement through artifact shaping, validation, observation, and eventual execution handoff.

`invoke` remains the governed authoring spell for define, design, plan, full, and validate outputs. It can prepare a handoff, but it should not become the whole craft lifecycle. Sigilcraft should own the lifecycle of sigils; Spellcraft should own the lifecycle of spells; Task Session should own bounded execution.

Recommended first prompt shape for a future sigilcraft session:

```text
I understand this as a sigilcraft session for: <candidate sigil or revision>.
Current stage: <idea | define | design | package | validate | observe | reflect | iterate | promote>.
The next responsible move is: <question, artifact, gate, or handoff>.
Do you want to continue this session at that stage?
```

## Session Thesis

Sigilcraft should be modeled as a stateful development session with stage memory, artifact ledgers, explicit gates, and resumable handoffs. A single invocation can perform one move inside the session, but the capability should describe the larger process from idea to execution-ready sigil.

This keeps three responsibilities separate:

- `invoke` prepares governed definition, design, plan, glossary, and work-pack artifacts.
- `sigilcraft` guides a sigil through lifecycle development and maintenance.
- `task-session` executes one bounded implementation or documentation task once the work is ready.

## Inputs

| Input | Required | Validation Rule |
| --- | --- | --- |
| Candidate sigil or revision target | yes | A sigil name, behavior gap, or candidate idea is stated or inferable. |
| Session stage | no | If missing, infer the smallest safe stage and record the assumption. |
| Existing artifacts | no | Existing README, SKILL, templates, telemetry, or development notes are treated as evidence. |
| Desired rename behavior | no | Rename from `sigil-development` to `sigilcraft` requires explicit approval before filesystem, adapter, registry, or command mutation. |
| Governance constraints | no | Authority boundaries, compatibility needs, and promotion rules must be preserved. |
| Execution target | no | If implementation is requested, route to `task-session` after lifecycle gates pass. |

## Outputs

| Output | Consumer | Contract |
| --- | --- | --- |
| Session state summary | User, future sigilcraft run | Names target, current stage, last decision, open gaps, and next responsible move. |
| Artifact ledger | Reviewer, lifecycle owner | Lists produced or consumed artifacts with ownership and stage. |
| Decision ledger | User, decision-gate, future run | Records accepted assumptions, deferred decisions, and blocker choices. |
| Sigil package or patch plan | Sigilcraft, task-session | Describes files to create or update without silently mutating upstream contracts. |
| Validation result | User, registry maintainer | Reports pass, flag, or block against quality bar and anti-patterns. |
| Observability signal | workflow-reflect, sigilcraft | Captures meaningful session execution and reflection triggers. |
| Execution handoff | task-session | Provides a bounded task only after scope, write set, done criteria, and validation are clear. |

## Modes

| Mode | Trigger | Behavior |
| --- | --- | --- |
| start | A new sigil idea or unclear maintenance request appears. | Capture target, intent, first stage, assumptions, and first gate. |
| refine | The idea is still blurry or overbroad. | Ask focused questions, reduce ambiguity, and prepare invoke define context when useful. |
| define | A governed baseline is needed. | Use or hand off to `invoke define`; record spec, glossary, and lifecycle gaps. |
| shape | README, SKILL, templates, or behavior contracts must be authored or revised. | Apply sigil lifecycle edits through the owning sigil surface. |
| validate | The package needs readiness review. | Check tier fit, links, quality bar, anti-patterns, output contract, examples, and observability. |
| trial | Behavior needs examples before promotion. | Run or prepare representative low, medium, and complex examples. |
| observe | The sigil was meaningfully used. | Emit telemetry and update session state. |
| reflect | Usage evidence or manual request asks for improvement. | Synthesize signals into no-change, targeted update, or reflection-required outcomes. |
| iterate | A targeted lifecycle improvement is approved. | Apply scoped changes and preserve the core contract unless evidence says it is wrong. |
| promote | The sigil is ready for registry or canonical exposure. | Prepare explicit promotion evidence and approval gates. |
| handoff | Work is ready for bounded execution. | Produce a task-session handoff with write scope, acceptance evidence, and validation command. |

## Session State Model

| State Field | Owner | Updated By | Consumed By |
| --- | --- | --- | --- |
| session target | sigilcraft | start, refine | every later stage |
| current stage | sigilcraft | every stage closeout | resume, handoff, observability |
| artifact ledger | sigilcraft | define, shape, validate, iterate | validation, promotion, task-session |
| decision ledger | sigilcraft | refine, define, validate, reflect | decision-gate, future resume |
| open gaps | sigilcraft | every gate | next route selection |
| execution handoff | sigilcraft | handoff | task-session |
| telemetry summary | observed invocation loop | observe, reflect | workflow-reflect, sigilcraft |

## Interaction Contract

| Interaction | Producer | Consumer | Failure Behavior |
| --- | --- | --- | --- |
| Intent capture | User, sigilcraft | invoke, sigilcraft | Block if target or purpose is contradictory. |
| Define handoff | sigilcraft | invoke | Flag if define artifacts are useful but rename or authority decisions remain open. |
| Lifecycle edit | sigilcraft | README, SKILL, templates | Block if the edit would silently rename commands, adapters, or registry entries. |
| Spell boundary | sigilcraft | spellcraft | Route to Spellcraft when the target is a spell composition rather than a sigil. |
| Execution boundary | sigilcraft | task-session | Defer until write scope, done criteria, and validation evidence are explicit. |
| Observation | sigilcraft, observed invocation loop | workflow-reflect | Flag if telemetry cannot connect back to a stage, quality bar, or output contract. |

## Runtime Adapter Expectations

| Expectation | Required | Notes |
| --- | --- | --- |
| Resume-aware closeout | yes | Each meaningful run should report current stage, files touched, open gaps, and next route. |
| Compatibility alias | yes, if renamed | `sigil-development` should continue resolving during migration if `sigilcraft` becomes canonical. |
| No hidden command mutation | yes | Runtime adapters and registries must not be renamed during define without explicit approval. |
| Observed invocation envelope | yes | Record sigilcraft stage, generated outputs, validation status, and workflow gaps. |
| Spellcraft boundary | yes | Spell lifecycle changes remain under Spellcraft. |

## Observability

| Signal | Trigger | Payload Summary |
| --- | --- | --- |
| sigilcraft-session-started | A new session begins or resumes. | Target, stage, request summary, existing artifacts, inferred assumptions. |
| sigilcraft-stage-closed | A stage produces an artifact or decision. | Stage, outputs, validation result, open gaps, next route. |
| sigilcraft-handoff-issued | Work routes to invoke, spellcraft, decision-gate, or task-session. | Source stage, target route, handoff artifact, blocker status. |
| sigilcraft-rename-gap | Rename from `sigil-development` to `sigilcraft` is proposed but not approved. | Affected surfaces, compatibility need, pending decision. |
| sigilcraft-reflection-triggered | Usage threshold, output threshold, gap threshold, severe gap, or manual review appears. | Signal summary, proposed iteration, rejected changes. |

## Quality Bar

A successful sigilcraft session model must:

- treat sigil creation and maintenance as a lifecycle rather than a one-time file-writing task,
- preserve authority boundaries between invoke, sigilcraft, spellcraft, and task-session,
- make the active stage and next route explicit at every closeout,
- keep rename and adapter migration behind explicit approval,
- support resumable state through artifact and decision ledgers,
- define observability that can drive later reflection,
- keep execution handoff bounded enough for task-session.

## Anti-Patterns

Avoid:

- turning `invoke` into the owner of sigil lifecycle execution,
- treating every craft session move as a complete task,
- renaming filesystem paths, registries, or command adapters during definition,
- mixing sigil lifecycle and spell lifecycle in one authority,
- emitting telemetry that does not name the session stage or lifecycle gap,
- handing off to task-session before the scope and validation evidence are explicit.

## Rename Migration Questions

| Decision | Current Recommendation | Status |
| --- | --- | --- |
| Should `sigilcraft` become the canonical id? | Likely yes, because it aligns with Spellcraft and describes craft as lifecycle. | pending approval |
| Should `sigil-development` remain available? | Yes, as a compatibility alias during migration. | recommended |
| Should Spellcraft also gain session-state language? | Yes, but through Spellcraft's own lifecycle update. | pending separate route |
| Should invoke contracts replace `sigil-development` with `sigilcraft` immediately? | No. First define the compatibility model, then update invoke references deliberately. | deferred |

## Sigil-Development Handoff

- Handoff status: flagged
- Handoff notes: This define session is ready for sigil-development/sigilcraft lifecycle work. The main open blocker is not conceptual; it is governance: the rename from `sigil-development` to `sigilcraft` needs explicit approval and a compatibility plan before runtime, registry, or path mutation.

## Gate Result

- Status: flag
- Reason: The session-process model is coherent enough for lifecycle design, but canonical rename, alias policy, and adapter migration remain approval-gated.
