# Invoke Refresh Mode Design

## Purpose

`invoke refresh` updates invoke-authored workflow artifacts from new session evidence without re-running the whole lifecycle and without pretending new evidence proves more than it proves.

It answers:

```text
Do the latest session outputs compose a valid refresh input for the current workflow artifacts, and if so, what artifact deltas should be proposed or applied?
```

## Mode Status

- Proposed mode: `refresh`
- Proposed layer: L2R, adjacent to `handoff`
- Lifecycle owner: `invoke`
- Implementation owner after approval: `spellcraft` or `task-session` on an invoke work-pack SWU

## Trigger Conditions

Use `invoke refresh` when:

- a session produced new evidence for an existing work-pack, plan, design, handoff, blocker, or status board;
- a new blocker or resolved blocker should be reflected in workflow artifacts;
- a task/session result changes the next route;
- artifacts may now be stale relative to latest outputs;
- the user asks to "refresh artifacts with this input" or equivalent.

Do not use it when:

- the target work has not produced inspectable evidence;
- the user is asking to execute a task rather than update artifact state;
- the desired update is actually a workflow reflection or a new lifecycle definition.

## Inputs

Required:

- source session outputs or latest result artifact paths;
- target workflow root or artifact inventory;
- intended refresh scope;
- evidence date;
- mutation mode: `proposal-only` or `apply-approved`.

Optional:

- source session reference;
- target lifecycle owner;
- known blocker IDs;
- expected artifacts such as `WORK-PACK.md`, `IMPLEMENTATION-LAYERING.md`, `TASK-*.md`, `W*.md`, handoff files, report files, or observability envelopes.

## Refresh Input Model

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
| `evidence_added` | New artifact proves a known acceptance criterion or setup step. | Raw runner JSON now exists. |
| `blocker_opened` | Latest output names a missing input or unsafe next step. | Score smoke needs a real agent candidate. |
| `blocker_resolved` | A previously blocking condition is now evidenced. | Docker daemon passed preflight. |
| `status_changed` | A task/SWU/work-pack row should change state. | `ready` to `completed-materialization-probe`. |
| `route_changed` | The recommended next route changes. | From materialization probe to candidate/profile prep. |
| `artifact_drift` | Artifacts contradict each other after new evidence. | Work-pack says ready while task file says blocked. |
| `no_op` | Evidence is already represented or not relevant. | Re-running a command produces no new state. |

## Artifact Refresh Policy

`invoke refresh` may propose or apply updates only to artifacts in the declared refresh scope.

It must:

- preserve source evidence links;
- distinguish setup proof from score/completion proof;
- update blockers before updating completion claims;
- keep target lifecycle ownership visible;
- record skipped artifacts and why;
- output a refresh report even when no mutation is needed.

It must not:

- infer benchmark scores or task completion from unrelated evidence;
- mutate upstream artifacts outside the scope;
- resolve a blocker without evidence;
- rewrite entire docs when a small status delta is sufficient;
- execute target tasks.

## Output Artifacts

Minimum output:

- `REFRESH-REPORT.md`
- `refresh-report.json`

When mutation is not yet approved:

- `REFRESH-PATCH-PROPOSAL.md`

When mutation is approved:

- patched target artifacts;
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

## Gates

Block when:

- source evidence is missing;
- target artifact inventory is missing;
- a proposed status change lacks evidence;
- mutation scope is ambiguous;
- the user asks for apply mode but approval is absent.

Flag when:

- useful refresh proposals exist but need human approval;
- artifacts conflict but the safe correction is not obvious;
- target lifecycle ownership is unclear.

Pass when:

- every proposed or applied delta maps to evidence;
- stale artifacts are corrected or intentionally left with a recorded reason;
- validation checks pass.

No-op when:

- latest evidence is already represented and no drift is found.

## Relationship To Existing Invoke Modes

- `define`: creates initial conceptual baseline.
- `design`: creates architecture/design baseline.
- `plan`: creates implementation/work-pack baseline.
- `handoff`: moves selected session context into a new thread.
- `refresh`: updates existing workflow artifacts from new session evidence.
- `validate`: later validates full lifecycle output.

## Observability Additions

Record:

- refresh mode;
- source signal count;
- target artifact count;
- delta class counts;
- mutation mode;
- applied/proposed/skipped counts;
- blocker ownership split;
- no-op rationale when relevant;
- next route after refresh.

## Design Decision

Recommended implementation: add `refresh` as a mode contract plus fixtures first, then add routing and templates. This keeps the command reviewable and avoids a hidden auto-mutation path.

## Interrogation Refresh

Interrogation result: [INVOKE-REFRESH-INTERROGATION.md](INVOKE-REFRESH-INTERROGATION.md)

Applied constraints:

- default mutation mode is `proposal-only`,
- `apply-approved` requires explicit approval and declared scope,
- no-op is first-class phase status,
- artifact drift flags when the safe correction is not obvious,
- refresh does not replace `workflow-reflect` or `task-session`.

## Distill Refresh

Distill result: [INVOKE-REFRESH-DISTILL.md](INVOKE-REFRESH-DISTILL.md)

Smallest coherent unit:

```text
RefreshSignal -> Delta -> RefreshReport
```

This unit is now the design center. Routing, templates, apply-approved mutation, command adapters, and observability are extensions around that unit, not the core behavior.
