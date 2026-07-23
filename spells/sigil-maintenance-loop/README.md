# Sigil Maintenance Loop

Status: reusable spell
Canonical ID: `sigil-maintenance-loop`
Aliases: none
Scope: library
Lifecycle owner: `spellcraft`

## Purpose

`sigil-maintenance-loop` improves a reusable sigil from execution evidence. It
automatically explores the repository Inventory before reflection, combines the
selected prior evidence with current telemetry, and routes only an approved,
targeted contract change through `sigil-development`.

Inventory exploration is read-only and does not require an additional user
prompt. Inventory remains a non-authority read model: its matches can inform a
reflection, but they cannot approve or promote a sigil change.

## Trigger Conditions

- A sigil has meaningful execution history.
- Telemetry shows repeated gaps, output drift, user corrections, or quality
  failures.
- The user asks to tune, reflect on, or improve a sigil.
- A maintainer asks whether a sigil still conforms to its declared contract.

## Required Sigils

| Sigil | Role In Spell | Required Mode |
| --- | --- | --- |
| `inventory` | Retrieve prior reusable evidence, exclusions, and gaps before reflection. | `lookup` |
| `signal-observer` | Record the current post-run behavior signal and Inventory lookup status. | `observe` |
| `workflow-reflect` | Analyze accumulated signals together with the Inventory lookup packet. | `reflect` |
| `sigil-development` | Apply an explicitly approved targeted update and validate the sigil. | `update` or `reflect` |

## Optional Sigils

| Sigil | Use When |
| --- | --- |
| `experiment-harness` | A reusable behavior change needs fixture-backed or live runtime evidence. |
| `observability-setup` | The target repository has no local observability package and the maintainer explicitly chooses to install one. |

## Inputs

| Input | Required | Notes |
| --- | --- | --- |
| `target_sigil_id` | yes | Canonical sigil ID under maintenance. |
| `invocation_envelope` | yes | Latest meaningful run, current user correction, or equivalent observer evidence. |
| `contract_area` | yes | Process, Quality Bar, Anti-Pattern, output contract, observability, or another bounded area. |
| `inventory_terms` | no | Additional lookup terms derived from the correction, gap category, or affected contract area. |
| `approved_change_scope` | only before mutation | Explicit user-approved boundary for `sigil-development`. |

## Prerequisites

- The target sigil has a readable canonical contract.
- A meaningful invocation envelope, manual maintenance trigger, or accumulated
  telemetry is available.
- The `inventory` sigil is resolvable. A repository-local Inventory package is
  preferred but is not required for the loop to report a useful evidence gap.
- Any mutating update has an explicit approved scope.

## Shared State

| State | Producer | Consumer |
| --- | --- | --- |
| `maintenance-target` | Spell intake | Every phase |
| `inventory-lookup-packet` | `inventory` | `signal-observer`, `workflow-reflect`, maintenance report |
| `telemetry-signal` | `signal-observer` | `workflow-reflect`, maintenance report |
| `reflection-report` | `workflow-reflect` | Approval gate, `sigil-development` |
| `change-receipt` | `sigil-development` | Validation and maintenance report |
| `maintenance-report` | Spell closeout | Human maintainer and optional downstream Inventory ingestion |

The `inventory-lookup-packet` includes, when available: machine-index entry IDs,
selectors, evidence-card IDs, EvidenceSet IDs, source references, inclusion
reasons, excluded matches, confidence, and unresolved gaps.

## Authority Boundaries

| Capability | Owns | Boundary |
| --- | --- | --- |
| `inventory` | Evidence lookup, exclusions, gaps, and non-authority read models. | A match does not approve a contract change or promote canonical meaning. |
| `signal-observer` | Post-run behavior signals. | A signal records evidence; it does not prescribe the mutation. |
| `workflow-reflect` | Evidence-backed maintenance analysis and proposals. | It proposes; it does not edit the target sigil. |
| `sigil-development` | Approved sigil contract mutation and validation. | It must stay within the approved change scope. |
| `spellcraft` | This composition, its lifecycle validation, and reusable readiness. | The spell references sigil contracts instead of copying their internal processes. |

## Handoff Artifacts

| Handoff | Artifact | Receiving Owner |
| --- | --- | --- |
| Inventory exploration | `inventory-lookup-packet` | `signal-observer` and `workflow-reflect` |
| Observation | `telemetry-signal` | `workflow-reflect` |
| Reflection | `reflection-report` | Human approval gate and `sigil-development` |
| Targeted update | `change-receipt` plus changed paths | Validation closeout |
| Lifecycle closeout | `maintenance-report` | Human maintainer; optional separately authorized Inventory ingestion |

Artifacts may be inline when the local runtime has no configured persistence
path. Any persisted artifact must use repository-local paths and preserve its
source boundary.

## Execution Phases

| Phase | Sigil | Input | Output | Gate | Failure Policy |
| --- | --- | --- | --- | --- | --- |
| 1. Inventory exploration | `inventory` | target ID, invocation terms, contract area | `inventory-lookup-packet` | lookup is attempted automatically; read `index.json` first when present | continue with `inventory_unavailable`, `machine_index_gap`, or `no_inventory_match` residue; an `index.md` fallback is a validation gap |
| 2. Signal observation | `signal-observer` | invocation envelope plus lookup status | `telemetry-signal` | evidence is meaningful enough to record | skip only when no meaningful run or manual trigger exists |
| 3. Workflow reflection | `workflow-reflect` | telemetry ledger plus lookup packet | `reflection-report` | a manual trigger or configured threshold is met | stop with `insufficient_signal` when neither current nor accumulated evidence supports a proposal |
| 4. Targeted update | `sigil-development` | reflection report plus approved scope | updated sigil or no-change decision and `change-receipt` | user approves the mutating change scope | block on missing approval, scope expansion, or contract-breaking change |
| 5. Validation and report | `sigil-development` and spell closeout | phase outputs and changed artifacts | validation receipt and `maintenance-report` | contract checks run and remaining gaps are named | flag missing reusable-behavior evidence; block on invalid contract or failed required checks |

### Automatic Inventory Exploration

Every invocation reaches Phase 1 before reflection. The runtime must:

1. derive lookup terms from `target_sigil_id`, the current correction or observer
   signal, and `contract_area`;
2. read the repository Inventory `index.json` first when it exists;
3. use `index.md` only for human orientation or as an explicitly flagged fallback;
4. return relevant matches, exclusions, source references, and unresolved gaps;
5. continue without asking for permission because lookup is read-only; and
6. never turn this automatic phase into `install`, `query`, `ingest`, `backfill`,
   or `sync`.

If no Inventory package exists, the phase records `inventory_unavailable` and
continues with the target contract and telemetry evidence. The spell does not
silently install or mutate a repository knowledge package.

## Gates

| Gate | Required Evidence | Result |
| --- | --- | --- |
| Target gate | Canonical target ID and readable sigil contract. | pass/block |
| Inventory exploration gate | Machine-index lookup attempted, or explicit unavailable/fallback residue. | pass/flag |
| Evidence gate | Meaningful current signal, manual trigger, or accumulated telemetry. | pass/block |
| Reflection gate | Proposal cites telemetry and distinguishes Inventory evidence, inference, and gaps. | pass/block |
| Change approval gate | User-approved bounded mutation scope. | pass/block |
| Validation gate | Contract, links, product-neutral wording, and relevant behavior checks. | pass/flag/block |

## Failure Policy

- Inventory absence, an unparsable machine index, or no matching entry is a
  visible `flag`, not permission to skip exploration silently.
- An Inventory fallback never becomes canonical evidence and must remain named
  in residue.
- Stop before reflection when there is no manual trigger and no meaningful
  current or accumulated signal.
- Stop before mutation when approval is absent or the proposed change exceeds
  the approved scope.
- Block contract-breaking or invalid updates; do not continue to later phases
  as if validation passed.
- Preserve rejected proposals and remaining gaps in the maintenance report.

## Local Customization

Consuming repositories may customize Inventory root paths, reflection
thresholds, persistence paths, evidence-gap severity, and validation commands.
They must preserve automatic read-only Inventory exploration, machine-index-first
lookup, explicit mutation approval, sigil authority boundaries, and the named
handoff packet.

## Observability

Record:

- target sigil and contract area;
- Inventory availability, machine-index parseability, selected and excluded
  match counts, and lookup gaps;
- signal counts and reflection trigger;
- proposed, accepted, and rejected changes;
- approval and validation status;
- reusable-behavior evidence state; and
- next reflection trigger.

When a repository observability package exists, emit one spell-level signal for
the completed or blocked maintenance attempt. Telemetry failure does not erase
the maintenance result.

## Experiment Harness

Reusable lifecycle validation lives under `development/`. It must cover at
least:

- parseable `index.json` with relevant evidence;
- parseable `index.json` with no relevant match;
- `index.md` fallback;
- no repository Inventory package;
- insufficient reflection signal; and
- rejected mutation approval.

Live runtime evidence is required before a behavior-changing revision is called
promotion-ready. Deterministic contract and fixture checks may establish
structural validity but do not replace live behavior evidence.

## Output Contract

Return:

```markdown
## Sigil Maintenance Result

- Target sigil: <canonical-id>
- Contract area: <area>
- Trigger: manual | usage-threshold | output-threshold | gap-threshold | severe-gap
- Inventory lookup: pass | fallback | unavailable | no-match
- Inventory matches: <entry/card/set ids or none>
- Inventory exclusions: <summary or none>
- Inventory gaps: <summary or none>
- Observed signals: <count and summary>
- Reflection decision: no-change | targeted-update | reflection-blocked
- Approved change scope: <scope or none>
- Files changed: <paths or none>
- Validation: pass | flag | block
- Reusable evidence: pass | flag | block | not-run
- Remaining residue: <items or none>
- Next lifecycle step: <step>
```

## Quality Bar

A successful run must attempt Inventory lookup before reflection, keep Inventory
non-authoritative, preserve the approval gate before mutation, cite the evidence
for every proposed change, validate any applied update, and report residue
without inflating readiness.

## Anti-Patterns

Avoid bypassing `index.json`, asking for permission to perform read-only lookup,
silently installing or mutating Inventory, treating Inventory matches as change
approval, reflecting from anecdote without a manual trigger, manually sequencing
only part of this spell, or claiming reusable readiness without behavior
evidence.
