---
stage: 3
name: Interrogation (refine-review)
capability: interrogation
mode: refine-review
status: flag
verdict: proceed-with-repairs
dispatch_id: refine-dci-mutation-metric-20260608
---

# Interrogation refine-review

## Q1. Does `observer_version` stratification actually neutralize co-mutation?

Only partially. Holding `observer_version` fixed controls drift in the *shared* observer harness,
but the **skill file itself contains its quality-bar/gap-reporting instructions** — a mutation can
change what the skill reports while `observer_version` stays constant. **Repair:** stratification is
necessary but not sufficient; the design must pair it with at least one *observer-independent*
ground-truth signal, or explicitly mark the differential as "reporting-confounded."

## Q2. Is the workload actually held fixed?

Live telemetry is not a fixed workload — different tasks ran before/after. **Repair:** the credible
differential requires a **replay** of the same fixtures through v_old and v_new (experiment-harness).
The live-slice design must be labeled as a weak observational signal, not a controlled experiment.

## Q3. Small N — is this detectable at all?

task-session has 32 execution-bearing records *total*, split across versions it's far fewer. A
mutation tested on a handful of runs cannot move a 0.30 rate detectably. **Repair:** the power
analysis must report the **minimum runs per version**; if it's larger than a fixture corpus can
cheaply provide, the honest verdict is "detects only large regressions, not subtle ones."

## Q4. What counts as the unit and the effect direction?

A residue *increase* after a mutation = regression; a *decrease* = improvement. But a mutation that
makes the skill attempt harder work could raise residue legitimately. **Repair:** hold the fixture
corpus (and thus difficulty) fixed via replay; interpret ΔDCI only within a fixed-corpus replay.

## Verdict

**flag — proceed with four repairs** (pair stratification with ground-truth; require replay for any
causal claim; power-report minimum runs; fix the corpus to fix difficulty). Carried to design.
