# Full Iterative Refinement: Skill-Aware Observation Development Pack

## Scope

Review whether the current observability development architecture, design, layering, and work-pack are good enough to guide implementation.

Reviewed artifacts:

- [../ARCHITECTURE-OVERVIEW.md](../ARCHITECTURE-OVERVIEW.md)
- [SKILL-AWARE-OBSERVATION-DESIGN.md](SKILL-AWARE-OBSERVATION-DESIGN.md)
- [DERIVE-INVOCATION-TELEMETRY-DESIGN.md](DERIVE-INVOCATION-TELEMETRY-DESIGN.md)
- [CONTINUATION-FEEDBACK-ATTRIBUTION-DESIGN.md](CONTINUATION-FEEDBACK-ATTRIBUTION-DESIGN.md)
- [SKILL-AWARE-OBSERVATION-LAYERING.md](SKILL-AWARE-OBSERVATION-LAYERING.md)
- [SKILL-AWARE-OBSERVATION-WORK-PACK.md](SKILL-AWARE-OBSERVATION-WORK-PACK.md)
- [../scripts/observe-invocation.sh](../scripts/observe-invocation.sh)
- [.codex/hooks/arcanum-user-prompt-submit.sh](../../../.codex/hooks/arcanum-user-prompt-submit.sh)
- [.codex/hooks/arcanum-stop.sh](../../../.codex/hooks/arcanum-stop.sh)
- [.codex/hooks/arcanum-post-tool-use.sh](../../../.codex/hooks/arcanum-post-tool-use.sh)

## Workflow Profile

- Profile: `iterative-refinement`
- Mode: full, role-simulated inside this task session
- Context Builder: 1 pass
- Invoke passes: define, redefine/design, plan
- Interrogation passes: 3
- Distill passes: tournament plus repair
- Research pass: bounded; used as analogy and risk evidence only

## External Evidence

The local repository remains authoritative. External evidence influenced only risk framing:

- OpenTelemetry event semantics support the pack's use of named event types plus compact attributes rather than large bodies.
- OpenTelemetry log data model supports separating occurrence attributes from resource/instrumentation identity, matching the ledger-plus-index direction.
- W3C Trace Context supports the value of stable correlation ids across later related events.
- Public Codex hook issue reports indicate `PostToolUse` coverage can be incomplete for some write paths, so write-path evidence must be opportunistic rather than required for correctness.

## Define Pass

The development pack is trying to add deterministic observability for explicit Codex skill invocations without creating a second observer system.

The correct core objective is:

> Preserve an auditable skill-mode run boundary from prompt detection through closeout derivation and ledger append, while keeping later user feedback as linked follow-up evidence rather than retroactive mutation.

## Interrogation Pass 1

### Finding REF-OBS-001: The Pack Was Too Confidently Marked `pass`

Severity: medium.

The architecture and design are coherent, but implementation readiness still depends on unresolved proof points:

- `derive-invocation-telemetry.sh` does not exist yet.
- `observe-invocation.sh` currently drops optional `skill` and `skill_detection` fields.
- `active-run-context.json` is described architecturally but is not implemented in the observer.
- `PostToolUse` evidence is useful but cannot be treated as complete mutation evidence.

Resolution: use `flag-ready-for-L0-L3` instead of broad `pass`.

### Finding REF-OBS-002: The First Implementation Window Should Include Docs Only After Regression Evidence

Severity: medium.

The work-pack puts documentation refresh as ready after skill detection, but the docs claim derivation and observer behavior too. Updating docs after only L0 would risk documenting planned behavior as current behavior.

Resolution: make SWU-OBS-005 ready after route regression evidence, or split it later if a minimal architecture note is needed.

### Finding REF-OBS-003: Tool Evidence Must Be Treated As Partial

Severity: medium.

The derivation design already says not to infer changed files from prose, but the implementation plan should be stricter: missing `PostToolUse` write events are not a failure by themselves.

Resolution: add hook-coverage assumptions and validation expectations that tolerate empty `files_changed` when deterministic evidence is absent.

## Tournament

| Lane | Model | Strength | Weakness | Verdict |
| --- | --- | --- | --- | --- |
| A | Detector-first | Fastest L0 proof. | Produces an observable envelope but not useful final telemetry alone. | Reject as too small. |
| B | Closeout-first | Aligns derivation with observer append. | Cannot start without a skill-mode envelope. | Use after L0. |
| C | Observed skill run slice | L0 detection, L1 derivation, L2 preservation, L3 route regression, docs after evidence. | More work before claiming ready. | Select. |
| D | Full feedback cycle now | Captures later user corrections immediately. | Expands into Necronomicon/session attribution before base telemetry is proven. | Defer L4. |

Selected model: **Observed skill run slice**.

## Redefine And Design Pass

The smallest coherent implementation unit is not only `SWU-OBS-001`. It is the first release window:

1. `SWU-OBS-001`: open skill-mode pending envelope.
2. `SWU-OBS-002`: derive observer-ready closeout envelope.
3. `SWU-OBS-003`: preserve skill metadata during append.
4. `SWU-OBS-004`: route regression coverage.
5. `SWU-OBS-005`: document what is implemented and what remains deferred.

Within that window, task-session can still execute one SWU at a time. The pack should not claim the bridge is implementation-ready as a feature until all five pass.

## Interrogation Pass 2

### Blocker Check

No blocker prevents starting L0. There is a blocker preventing a feature-ready claim:

- derivation script absent,
- observer preservation absent,
- route regression absent,
- docs not synchronized to actual behavior.

### Design Quality Verdict

Good architecture, but not yet release-ready. The architecture has the right boundaries:

- `.agents/skills` as skill discovery,
- `.codex/commands` as compatibility,
- derivation before append,
- one append authority,
- continuation feedback as linked follow-up evidence.

The plan needed sharper readiness language and one more explicit guardrail around hook evidence coverage.

## Repair Pass

Required repairs applied or queued:

- Work-pack gate language now distinguishes planning readiness from feature readiness.
- Documentation refresh dependency should wait until route regression evidence.
- Design now treats `PostToolUse` write evidence as partial.
- Architecture overview should label active-run context as planned L4 behavior until implemented.

## Plan Pass

Recommended next execution order:

1. Stabilize or validate the partial `SWU-OBS-001` hook edit already present in the worktree.
2. Implement `SWU-OBS-002` with explicit degradation when tool evidence is missing.
3. Implement `SWU-OBS-003` before claiming skill telemetry is explainable.
4. Add `SWU-OBS-004` fixture coverage across command, skill, markdown skill, unknown token, and mixed route.
5. Run `SWU-OBS-005` documentation sync from actual implementation evidence.
6. Defer `SWU-OBS-006` continuation feedback until the base closeout path passes.

## Final Interrogation

Final verdict: `FLAG`.

The development architecture and plan are directionally good and ready for bounded L0-L3 implementation, but the pack should not call the whole bridge complete or broadly pass-ready yet.

## Synthesis

Use the pack, with corrected readiness language:

- Architecture: good.
- Design: good after hook-evidence caveat.
- Layering: good.
- Work-pack: good after dependency/readiness correction.
- Implementation status: not feature-ready.
- Best next route: continue `task-session` one SWU at a time, starting with validation and repair of the interrupted `SWU-OBS-001` hook edit.
