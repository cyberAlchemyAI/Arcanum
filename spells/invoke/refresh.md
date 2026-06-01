# Invoke Refresh Mode

## Identity

- Spell: `invoke`
- Mode: `refresh`
- Status: implemented (L2 refresh contract, validation examples pending)

## Purpose

Refresh mode updates invoke-authored workflow artifacts from new session evidence without re-running the whole lifecycle and without pretending new evidence proves more than it proves.

It answers:

```text
Do the latest session outputs compose valid refresh input for the current workflow artifacts, and what artifact deltas should be proposed or applied?
```

Refresh mode is artifact-state synthesis. It does not execute target work, score benchmarks, complete downstream lifecycles, or silently mutate unrelated artifacts.

## Activation Gate

Normal refresh mode requires:

- source session outputs, result artifacts, or evidence selectors,
- target workflow root or target artifact inventory,
- intended refresh scope,
- evidence date,
- mutation mode: `proposal-only` or `apply-approved`,
- Context Builder-selected source context when the source session is broad,
- explicit approval when mutation mode is `apply-approved`.

Refresh blocks when source evidence is missing, target artifact inventory is missing, mutation scope is ambiguous, or a proposed status change lacks evidence.

## Required Sigils

| Sigil | Role In Mode | Required Mode |
| --- | --- | --- |
| `context-builder` | Select source evidence and target artifact context when refresh inputs span a session or several artifacts. | standard; strict for apply-approved |
| `structured-interview-kits` | Ask one focused question when refresh scope, mutation mode, or target inventory is ambiguous. | gap-check |
| `inventory` | Resolve target artifacts, templates, and refresh report paths. | lookup |

## Optional Sigils

| Sigil | Use When | Notes |
| --- | --- | --- |
| `decision-gate` | A status, blocker, or route update depends on a consequential unresolved decision. | Route only blocker-level choices. |
| `workflow-reflect` | The source evidence is a felt workflow gap rather than artifact-state evidence. | Reflection owns workflow improvement analysis. |
| `task-session` | The refresh report identifies executable work that needs a bounded task. | Refresh emits handoff context only. |

## Inputs

- source session reference or source evidence paths,
- latest result artifacts,
- target workflow root,
- target artifact inventory,
- refresh scope,
- evidence date,
- mutation mode,
- known blocker IDs,
- known task, SWU, wave, or route IDs,
- optional expected next route.

## Refresh Signal Model

Each input item is normalized as a `RefreshSignal`:

```yaml
id: <stable-id>
source_path: <path or session selector>
signal_type: evidence_added | blocker_opened | blocker_resolved | status_changed | route_changed | artifact_drift | no_op
target_artifacts:
  - <path>
claim: <what changed>
evidence: <why the claim is supported>
confidence: high | medium | low
mutation_safety: safe | needs_review | blocked
```

## Delta Classes

| Delta | Meaning | Example |
| --- | --- | --- |
| `evidence_added` | New artifact proves a known acceptance criterion or setup step. | A runner report now exists. |
| `blocker_opened` | Latest output names a missing input or unsafe next step. | Score smoke needs a real agent candidate. |
| `blocker_resolved` | A previously blocking condition is now evidenced. | Docker daemon passed preflight. |
| `status_changed` | A task, SWU, wave, or work-pack row should change state. | `ready` to `completed-materialization-probe`. |
| `route_changed` | The recommended next route changes. | From materialization probe to candidate/profile prep. |
| `artifact_drift` | Artifacts contradict each other after new evidence. | Work-pack says ready while task file says blocked. |
| `no_op` | Evidence is already represented or not relevant to the declared scope. | Re-running validation produces no new artifact state. |

## Mutation Modes

| Mode | Behavior |
| --- | --- |
| `proposal-only` | Default. Emit `REFRESH-REPORT.md` and, when useful, `REFRESH-PATCH-PROPOSAL.md`; do not edit target artifacts. |
| `apply-approved` | Apply scoped changes only when explicit approval, target inventory, and validation commands are present. |

## Output Artifacts

Minimum output:

- `REFRESH-REPORT.md`
- `refresh-report.json`

When mutation is not approved:

- `REFRESH-PATCH-PROPOSAL.md`

When mutation is approved:

- patched target artifacts,
- updated `refresh-report.json` with changed files and validation.

## Refresh Report Shape

```json
{
  "mode": "refresh",
  "phaseStatus": "pass|flag|block|no-op",
  "sourceSignals": [],
  "targetArtifacts": [],
  "deltaSummary": [],
  "proposedChanges": [],
  "appliedChanges": [],
  "skippedChanges": [],
  "blockers": [],
  "nextRoute": "",
  "validation": []
}
```

## Mode Gates

- Source evidence and target artifact inventory are mandatory.
- Refresh scope must be declared before proposal or apply output.
- Mutation mode defaults to `proposal-only`.
- `apply-approved` requires explicit approval, declared scope, and validation commands.
- Every proposed or applied change must map to at least one `RefreshSignal`.
- Setup proof must not be promoted into completion proof.
- Blockers must be opened or preserved before status is upgraded.
- Artifact drift must flag when the safe correction is not obvious.
- No-op is a valid phase status when latest evidence is already represented.
- Refresh must not execute target tasks, score benchmarks, or complete downstream lifecycles.
- Refresh must not rewrite entire artifacts when a small status delta is sufficient.

## Phase Status

| Status | Meaning |
| --- | --- |
| `pass` | Evidence-backed refresh proposal or approved update is complete. |
| `flag` | Useful deltas exist, but approval, ownership, or drift resolution is still needed. |
| `block` | Required source evidence, target inventory, scope, or approval is missing. |
| `no-op` | Latest evidence is already represented and no drift is found. |

## Relationship To Existing Invoke Modes

- `define`: creates initial conceptual baseline.
- `design`: creates architecture/design baseline.
- `plan`: creates implementation/work-pack baseline.
- `handoff`: moves selected session context into a new thread.
- `refresh`: updates existing workflow artifacts from new session evidence.
- `validate`: later validates full lifecycle output.

## Observability

When `.arcanum/observability/` exists, record:

- spell name and mode,
- source signal count,
- target artifact count,
- delta class counts,
- mutation mode,
- proposed/applied/skipped counts,
- blocker ownership split,
- no-op rationale when relevant,
- next route after refresh,
- validation commands or review checks.

## Output Shape

Return:

```markdown
## Invoke Validation Fixture Result

- Mode: refresh
- Spell: invoke
- Canonical ID: invoke
- Scope: library
- Phase status: pass | flag | block | no-op
- Mode contract: arcanum/spells/invoke/refresh.md
- Outputs: <refresh report path>, <patch proposal path or n/a>
- Mutation mode: proposal-only | apply-approved
- Source signals: <count and delta summary>
- Target artifacts: <paths>
- Proposed changes: <summary>
- Applied changes: <summary or n/a>
- Skipped changes: <summary or none>
- Validation: <commands or review checks>
- Decisions: <route decisions>
- Unresolved gaps: <invoke gaps; target artifact gaps>
- Next route: task-session | workflow-reflect | invoke plan | deferred
```
