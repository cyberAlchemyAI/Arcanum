# SWU-OIL-008 Evidence

## Scope

- Parent task: T-VERIFY
- Goal: verify full telemetry and reflection loop.
- Write scope: validation evidence only.

## Verification Commands

```bash
bash -n framework/observability/scripts/observe-invocation.sh
bash -n framework/observability/scripts/reflect-invocation-signals.sh
bash -n framework/observability/scripts/run-observed-adapter-pilot.sh
bash -n arcana/experiment-harness/scripts/observe-harness.sh
framework/observability/scripts/run-observed-adapter-pilot.sh --observability-dir <temp-dir>
arcana/experiment-harness/development/run-phase-gates.sh
```

## Results

```text
SWU_OIL_008_PILOT=pass
Phase 0: pass - baseline controls, syntax checks, generic validation, observation, and threshold reflection signal ran
Phase 1: pass - invoke live regime files validate
Phase 2: pass - single-attempt loop creates a valid attempt bundle
Phase 3: pass - pass streak resets after failure and succeeds after two consecutive passes
Phase 4: pass - failed attempt creates robot-talks and improvement argument artifacts
Phase 5: pass - patch application and rollback work in an isolated git repo
Phase 6: pass - invoke pilot loop passes with mocked live output
Phase 7: pass - new harness initialization creates loop-ready layout
REPORT=arcana/experiment-harness/development/runs/20260518T120720Z.md
```

## Coverage

- Generic observer syntax passed.
- Reflection runner syntax passed.
- Adapter pilot syntax passed.
- Experiment harness observer syntax passed.
- Hook-driven adapter pilot emitted telemetry for skill, sigil, and spell.
- Experiment harness still passes its phase gates after delegating to the generic observer.
- Reflection threshold signal remains covered by phase gate 0.

## Status

- SWU status: complete
- Parent task status: complete
- Work-pack status: verified
