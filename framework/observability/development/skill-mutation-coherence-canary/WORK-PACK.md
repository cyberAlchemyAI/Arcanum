---
observed_capability: invoke
invoke_mode: plan
artifact: work-pack
target_artifact: Skill-Mutation Coherence Canary
output_mode: single-file
complexity: medium
date: 2026-06-08
---

# WORK-PACK — Skill-Mutation Coherence Canary

Execution-ready SWUs for L0–L2. L3 is deferred (handoff, not tasked here).

## Shared SWU manifest

| SWU | Parent task | Layer | Write scope |
| --- | --- | --- | --- |
| SWU-1 | T1.1 emit skill_version | L0 | observability emission hook script(s) |
| SWU-2 | T1.2 compute_dci scorer | L0 | new `scripts/compute-dci.py` (read-only) |
| SWU-3 | T1.3 per-version report | L0 | `scripts/compute-dci.py` (report mode) |
| SWU-4 | T2.1 slice + flag | L1 | `scripts/compute-dci.py` (canary mode) |
| SWU-5 | T2.2 workflow-reflect readout | L1 | workflow-reflect lens config (proposal) |
| SWU-6 | T3.1 rework extractor | L2 | new `scripts/confirm-rework.py` |

## SWU detail

### SWU-1 — Emit `skill_version`
- **Acceptance evidence:** a freshly appended signal record contains a non-empty `skill_version`.
- **Verification:** invoke any skill, then `tail -1 .arcanum/observability/signals/sigil-invocations.jsonl | grep skill_version`.
- **Failure behavior:** unreadable skill file → `skill_version: "unknown"`; never block the run.

### SWU-2 — `compute_dci` scorer
- **Acceptance evidence:** clean records score 100; gap/fail records < 100; reproduces the prior
  backtest separation (clean mean 100, residue-bearing ~71.7 on the current store).
- **Verification:** `python3 scripts/compute-dci.py --store <jsonl> --self-check` prints the
  clean-vs-residue means and asserts no boundary overlap.
- **Failure behavior:** enum drift normalized; null status → fail (conservative).

### SWU-3 — Per-version report
- **Acceptance evidence:** one row per `skill_version` with mean DCI + N + residue-bearing count;
  null/observe-mode excluded.
- **Verification:** `python3 scripts/compute-dci.py --store <jsonl> --by-version`.

### SWU-4 — Slice + gross-regression flag
- **Acceptance evidence:** a synthetic two-version input with a planted ΔDCI ≥ 30 produces a flag;
  ΔDCI < 30 does not; any arm with N < 10 yields `insufficient-N`, never a flag.
- **Verification:** `python3 scripts/compute-dci.py --canary --fixture tests/two-version.jsonl`
  asserts the three cases.
- **Failure behavior:** < 2 versions or N < MIN_N → `insufficient-N`.

### SWU-5 — workflow-reflect readout (proposal)
- **Acceptance evidence:** every readout row carries `N` and the label
  "gross-regression-only, screening; not causal."
- **Verification:** reviewable check — the rendered lens config includes the label and N column.
- **Failure behavior:** missing label → block (honesty gate).

### SWU-6 — Rework extractor (post-hoc)
- **Acceptance evidence:** a seeded fixture with a known later same-file edit resolves `rework=1`;
  an untouched file resolves `0`; missing history resolves `unknown` (never a false confirm).
- **Verification:** `python3 scripts/confirm-rework.py --unit tests/reworked.json` and
  `--unit tests/clean.json` assert 1 and 0.
- **Failure behavior:** renamed paths via `--follow`; null `files_changed` reported as not-analyzable.

## Validation strategy

Each SWU has a runnable verification command or a reviewable check (above). The L0 scorer's
self-check ties back to the prior backtest numbers, so the spine is regression-tested against real
data. Honesty-gate checks (SWU-5 label, SWU-6 no-false-confirm) are hard blocks.

## Done criteria

L0–L2 SWUs pass their verification; the canary is surfaced (labeled, screening-only); the rework
anchor confirms/denies flags post-hoc. L3 remains a deferred handoff with its funding gate.

## Next route

`task-session` to execute SWU-1…SWU-6 (one parent task each). L3 → `experiment-harness` +
`sigil-development` when the per-skill fixture corpus is funded.
