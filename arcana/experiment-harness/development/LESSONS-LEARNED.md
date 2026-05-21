# Loop-First Experiment Harness Lessons Learned

## Phase 0: Stabilize Current Work

- Deterministic controls are still valuable because they isolate contract regressions from model/runtime drift.
- Live-output gates should not be added to the deterministic runner before a loop runner exists; doing so makes the baseline fail for the wrong reason.
- Quality Bar and Anti-Pattern findings need machine-readable report lines so observer telemetry can preserve them.

## Phase 1: Regime Model

- Regimes need both human-readable intent and machine-checkable fields.
- Prompt mapping should stay explicit with `- Prompt: \`example-prompts/<id>.md\`` so scripts do not infer incorrectly.
- Durable regime files should be tracked; loop outputs should stay ignored.

## Phase 2: Single-Attempt Loop

- The loop needs a mock execution path for validating harness behavior without spending live Codex calls.
- Attempt bundles should copy the exact prompt used so later review is not dependent on changed prompt files.
- Validation should write JSON first; human reports can be derived from it.

## Phase 3: Stability Loop

- Two consecutive passes are stricter than two total passes and force the loop to reset after a regression.
- A loop report should show every attempt, not only the final verdict.
- Stable pass logic is mechanical; semantic quality still depends on regime patterns and later observer judging.

## Phase 4: Robot-Talks Improvement Gate

- Robot-talks should create reasoning artifacts, not silently edit files.
- Improvement arguments must include regression criteria before patching is allowed.
- A deterministic reflector can enforce artifact shape now; a richer runtime/subagent reflector can replace it later.

## Phase 5: Patch And Rollback Manager

- No-op improvements are important because not every failure has a safe automatic patch.
- Rollback must operate only on the patch the loop applied.
- Dirty worktree ownership checks are necessary before enabling real full-artifact auto-edits broadly.

## Phase 6: Invoke Pilot End-To-End

- Mocked invoke loops prove harness control flow, not live model stability.
- Real invoke promotion still requires live Codex loops for define, design, define-to-design, and observability.

## Phase 7: Generalize To All Spells And Sigils

- New artifacts should start with loop-ready structure so validation habits are consistent from creation.
- External project support depends on runtime adapters exposing the loop command, not only the old `next/run/validate` commands.

## Phase Gate Run 20260518T083859Z

- **Phase 0:** The deterministic baseline can stay green while loop-first features are added behind separate gates.
- **Phase 1:** Explicit prompt paths and required output patterns make regimes both readable and scriptable.
- **Phase 2:** Mocked execution lets us verify bundle shape without spending live Codex calls.
- **Phase 3:** Two consecutive passes catch instability that a two-total-pass rule would miss.
- **Phase 4:** Reflection artifacts can be generated deterministically before richer subagent-based robot-talks exists.
- **Phase 5:** Rollback should be validated in isolation before enabling broad full-artifact edits.
- **Phase 6:** Mocked invoke loops prove harness control flow, but real Codex loops are still required for promotion evidence.
- **Phase 7:** Loop-ready layout can be installed at artifact creation time without running live Codex.

## Phase Gate Run 20260518T111056Z

- **Phase 0:** The deterministic baseline can stay green while loop-first features are added behind separate gates.
- **Phase 1:** Explicit prompt paths and required output patterns make regimes both readable and scriptable.
- **Phase 2:** Mocked execution lets us verify bundle shape without spending live Codex calls.
- **Phase 3:** Two consecutive passes catch instability that a two-total-pass rule would miss.
- **Phase 5:** Rollback should be validated in isolation before enabling broad full-artifact edits.
- **Phase 6:** Mocked invoke loops prove harness control flow, but real Codex loops are still required for promotion evidence.
- **Phase 7:** Loop-ready layout can be installed at artifact creation time without running live Codex.

## Phase Gate Run 20260518T111131Z

- **Phase 0:** The deterministic baseline can stay green while loop-first features are added behind separate gates.
- **Phase 1:** Explicit prompt paths and required output patterns make regimes both readable and scriptable.
- **Phase 2:** Mocked execution lets us verify bundle shape without spending live Codex calls.
- **Phase 3:** Two consecutive passes catch instability that a two-total-pass rule would miss.
- **Phase 4:** Reflection artifacts can be generated deterministically before richer subagent-based robot-talks exists.
- **Phase 5:** Rollback should be validated in isolation before enabling broad full-artifact edits.
- **Phase 6:** Mocked invoke loops prove harness control flow, but real Codex loops are still required for promotion evidence.
- **Phase 7:** Loop-ready layout can be installed at artifact creation time without running live Codex.

## Phase Gate Run 20260518T120123Z

- **Phase 0:** The deterministic baseline can stay green while loop-first features are added behind separate gates.
- **Phase 1:** Explicit prompt paths and required output patterns make regimes both readable and scriptable.
- **Phase 2:** Mocked execution lets us verify bundle shape without spending live Codex calls.
- **Phase 3:** Two consecutive passes catch instability that a two-total-pass rule would miss.
- **Phase 4:** Reflection artifacts can be generated deterministically before richer subagent-based robot-talks exists.
- **Phase 5:** Rollback should be validated in isolation before enabling broad full-artifact edits.
- **Phase 6:** Mocked invoke loops prove harness control flow, but real Codex loops are still required for promotion evidence.
- **Phase 7:** Loop-ready layout can be installed at artifact creation time without running live Codex.

## Phase Gate Run 20260518T120720Z

- **Phase 0:** The deterministic baseline can stay green while loop-first features are added behind separate gates.
- **Phase 1:** Explicit prompt paths and required output patterns make regimes both readable and scriptable.
- **Phase 2:** Mocked execution lets us verify bundle shape without spending live Codex calls.
- **Phase 3:** Two consecutive passes catch instability that a two-total-pass rule would miss.
- **Phase 4:** Reflection artifacts can be generated deterministically before richer subagent-based robot-talks exists.
- **Phase 5:** Rollback should be validated in isolation before enabling broad full-artifact edits.
- **Phase 6:** Mocked invoke loops prove harness control flow, but real Codex loops are still required for promotion evidence.
- **Phase 7:** Loop-ready layout can be installed at artifact creation time without running live Codex.

## Phase Gate Run 20260521T122458Z

- **Phase 0:** The deterministic baseline can stay green while loop-first features are added behind separate gates.
- **Phase 1:** Explicit prompt paths and required output patterns make regimes both readable and scriptable.
- **Phase 2:** Mocked execution lets us verify bundle shape without spending live Codex calls.
- **Phase 3:** Two consecutive passes catch instability that a two-total-pass rule would miss.
- **Phase 4:** Reflection artifacts can be generated deterministically before richer subagent-based robot-talks exists.
- **Phase 5:** Rollback should be validated in isolation before enabling broad full-artifact edits.
- **Phase 6:** Mocked invoke loops prove harness control flow, but real Codex loops are still required for promotion evidence.
- **Phase 7:** Loop-ready layout and profile metadata can be installed at artifact creation time without running live Codex.

## Phase Gate Run 20260521T131937Z

- **Phase 0:** The deterministic baseline can stay green while loop-first features are added behind separate gates.
- **Phase 1:** Explicit prompt paths and required output patterns make regimes both readable and scriptable.
- **Phase 2:** Mocked execution lets us verify bundle shape without spending live Codex calls.
- **Phase 3:** Two consecutive passes catch instability that a two-total-pass rule would miss.
- **Phase 4:** Reflection artifacts can be generated deterministically before richer subagent-based robot-talks exists.
- **Phase 5:** Rollback should be validated in isolation before enabling broad full-artifact edits.
- **Phase 6:** Mocked invoke loops prove harness control flow, but real Codex loops are still required for promotion evidence.
- **Phase 7:** Loop-ready layout and profile metadata can be installed at artifact creation time without running live Codex.

## Phase Gate Run 20260521T141939Z

- **Phase 0:** The deterministic baseline can stay green while loop-first features are added behind separate gates.
- **Phase 1:** Explicit prompt paths and required output patterns make regimes both readable and scriptable.
- **Phase 2:** Mocked execution lets us verify bundle shape without spending live Codex calls.
- **Phase 3:** Two consecutive passes catch instability that a two-total-pass rule would miss.
- **Phase 4:** Reflection artifacts can be generated deterministically before richer subagent-based robot-talks exists.
- **Phase 5:** Rollback should be validated in isolation before enabling broad full-artifact edits.
- **Phase 6:** Mocked invoke loops prove harness control flow, but real Codex loops are still required for promotion evidence.
- **Phase 7:** Loop-ready layout and profile metadata can be installed at artifact creation time without running live Codex.

## Phase Gate Run 20260521T142113Z

- **Phase 0:** The deterministic baseline can stay green while loop-first features are added behind separate gates.
- **Phase 1:** Explicit prompt paths and required output patterns make regimes both readable and scriptable.
- **Phase 2:** Mocked execution lets us verify bundle shape without spending live Codex calls.
- **Phase 3:** Two consecutive passes catch instability that a two-total-pass rule would miss.
- **Phase 4:** Reflection artifacts can be generated deterministically before richer subagent-based robot-talks exists.
- **Phase 5:** Rollback should be validated in isolation before enabling broad full-artifact edits.
- **Phase 6:** Mocked invoke loops prove harness control flow; live promotion evidence is recorded separately in LIVE-PROMOTION-CLOSEOUT.md.
- **Phase 7:** Loop-ready layout and profile metadata can be installed at artifact creation time without running live Codex.

## Phase Gate Run 20260521T151209Z

- **Phase 0:** The deterministic baseline can stay green while loop-first features are added behind separate gates.
- **Phase 1:** Explicit prompt paths and required output patterns make regimes both readable and scriptable.
- **Phase 2:** Mocked execution lets us verify bundle shape without spending live Codex calls.
- **Phase 3:** Two consecutive passes catch instability that a two-total-pass rule would miss.
- **Phase 4:** Reflection artifacts can be generated deterministically before richer subagent-based robot-talks exists.
- **Phase 5:** Rollback should be validated in isolation before enabling broad full-artifact edits.
- **Phase 6:** Mocked invoke loops prove harness control flow; live promotion evidence is recorded separately in LIVE-PROMOTION-CLOSEOUT.md.
- **Phase 7:** Loop-ready layout and profile metadata can be installed at artifact creation time without running live Codex.
