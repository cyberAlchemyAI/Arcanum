# Invoke Define Mode

## Identity

- Spell: `invoke`
- Mode: `define`
- Status: implemented (L0 contract, candidate template-family scaffold coverage)

## Purpose

Define mode produces or updates a governed specification and glossary baseline with explicit decisions, evidence-aware template routing, and transport-ready handoff artifacts.

## Implementation Coverage

- The define contract, the DomainSpec template baseline (`templates/domainspec-spec/` — SPEC + aspect docs), standalone implementation-layering/work-pack templates, and dedicated candidate family scaffolds are implemented.
- Named template families are scaffolded as candidate templates; canonical promotion still requires validation evidence and explicit approval.
- Implementation layering is integrated as a companion artifact policy: define may seed L0 or record a layering gap for downstream plan/full modes.
- Registry release remains blocked until required template and profile-family validation examples pass.

## Required Sigils

| Sigil                       | Role In Mode                                                          | Required Mode                                       |
| --------------------------- | --------------------------------------------------------------------- | --------------------------------------------------- |
| `context-builder`           | Build bounded define context from user goal and existing artifacts.   | lean or standard                                    |
| `structured-interview-kits` | Clarify missing context one question at a time and capture approvals. | gap-check or equivalent one-question interview mode |
| `inventory`                 | Resolve templates and record selection evidence.                      | lookup, ingest, validate                            |

## Optional Sigils

| Sigil               | Use When                                                                    | Notes                                                                  |
| ------------------- | --------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| `decision-gate`     | A blocker-level define decision cannot be resolved from available evidence. | Route only consequential unresolved choices.                           |
| `distill`           | The definition target is broad, ambiguous, or likely to split into multiple spec/glossary units. | Run a definition-scope sanity check and record `pass`, `flag`, `block`, or `not required`; do not create plan-ready work. |
| `spellcraft`        | Approved define output targets spell authoring or spell revision.           | Invoke emits handoff pack; Spellcraft owns spell lifecycle mutation, validation, install/adaptation, observation, and reflection. |
| `sigil-development` | Approved define output targets sigil authoring or sigil revision.           | Invoke emits handoff pack; Sigil Development owns sigil lifecycle mutation, validation, observability, reflection, and promotion readiness. |

## Inputs

- user goal and scope hints
- existing artifacts and local constraints
- template inventory or candidate-template permission
- optional existing implementation-layering artifact for update or reuse
- glossary sources from Necronomicon context when needed

## Execution Phases

| Phase | Sigil                                                  | Input                                               | Output                                                                     | Gate                                                                 | Failure Policy                                                                   |
| ----- | ------------------------------------------------------ | --------------------------------------------------- | -------------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| 1     | `context-builder`                                      | user goal, known constraints, existing artifacts    | bounded define context                                                     | mandatory define inputs are identified                               | block on missing core goal or contradictory scope                                |
| 2     | `structured-interview-kits`                            | bounded define context                              | approved intent record                                                     | one-question cadence and approval captured                           | block on unresolved blocker ambiguity                                            |
| 3     | `inventory`                                            | approved intent record and local template inventory | template selection record or candidate-template recommendation             | template eligibility is explicit and tie cases request user choice   | flag when no eligible template exists and candidate creation is unapproved       |
| 4     | `invoke define`                                        | approved intent and template record                 | spec artifact, glossary artifact, optional layering seed or layering gap note, define transport report, unresolved gaps | glossary linking and no-silent-upstream-mutation rules are satisfied | block on violated governance rule; otherwise return partial with unresolved gaps |
| 5     | optional `decision-gate`                               | unresolved define blocker                           | decision record and next route                                             | blocker decision resolved or explicitly deferred                     | keep blocker in gap ledger with recommended next action                          |
| 6     | optional handoff (`spellcraft` or `sigil-development`) | approved define outputs                             | lifecycle-authoring handoff pack                                           | handoff target is explicit and accepted                              | defer handoff if target authority is unavailable                                 |

## Mode Gates

- Template selection must include eligibility evidence and explicit user choice on tie cases.
- Current prebuilt template coverage includes the DomainSpec template baseline (`templates/domainspec-spec/`), standalone implementation-layering/work-pack companions, and dedicated candidate family scaffolds; any unsupported new family must be reported as a candidate-template gap, not treated as implemented coverage.
- Discovery-existence soft gate: define searches for a discovery artifact for the target scope; if none exists it halts with a recommendation to run discovery first. `--skip-discovery` is permitted but must write a `discovery_waiver_reason` into the spec frontmatter.
- Define mode may emit an implementation-layering seed; if skipped, it must record an explicit layering gap for downstream `plan`, `full`, and `validate` modes.
- Glossary linking uses deterministic statuses: `linked`, `partial`, or `no-match` with rationale.
- Candidate glossary promotion is never automatic.
- No silent upstream mutation; direct upstream edits require explicit approval.
- Define-stage transport appends stage reports and complements matching Necronomicon sections only when they already exist.
- Define mode must record a Dispatch Spec technique trace that names the techniques used to justify template selection, glossary routing, owner boundaries, and next route.
- Define mode runs a Distill sanity check when the target is broad, ambiguous, or split-prone; otherwise it records `not required` with rationale.
- A `flag` or `block` Distill result routes to clarification, definition split, or deferred follow-up; it must not be treated as plan readiness.

## Handoff Artifacts

- define context summary
- spec artifact path
- glossary artifact path
- implementation layering artifact path or explicit layering gap
- template selection evidence
- Dispatch Spec technique trace
- Distill validation status and rationale
- unresolved gaps and blocker decisions
- Necronomicon transport report
- recommended next route (`design`, `spellcraft`, `sigil-development`, or deferred follow-up)

## Mode Output Contract

Return:

```markdown
## Invoke Result

- Mode: define
- Spell: invoke
- Canonical ID: invoke
- Scope: library
- Phase status: pass | flag | block
- Mode contract: spells/invoke/define.md
- Outputs: <spec path>, <glossary path>, <layering seed path or gap>, <transport report path>
- Template selection: <selected template or candidate recommendation>
- Dispatch techniques: <technique ids and rationale>
- Distill validation: not required | pass | flag | block; <rationale>
- Decisions: <summary>
- Unresolved gaps: <summary>
- Next route: design | spellcraft | sigil-development | deferred
```
