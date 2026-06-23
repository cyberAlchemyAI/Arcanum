# Example 02 (medium) — `distill` + `emit-validator`

**Modes:** `distill` then `emit-validator` · **Input:** lesson L-xray-02 (right-rail beside the stack) · **Expected:** a `seed` `ux-pattern` and a validator claim map with **no invented fields**.

## Step A — `distill` output body (real artifact)

```yaml
pattern_id: detail-beside-the-subject
name: Detail beside the subject (no divided attention)
intent: keep explanatory detail co-visible with the element it explains
problem: a separate or below detail panel forces eye travel, splitting attention during active reading
solution: a sticky inspector adjacent to the inspected structure that updates on hover/selection
when_to_use: a layered or structured artifact a user reads while needing per-item detail
anti_pattern: a modal or below-the-fold panel for per-item detail during active reading
forces: [reading continuity, screen width, per-item depth]
evidence_link: L-xray-02 (screenshot_diff; screenshots 19-21)
status: seed
residue: anecdote signal — one session; cannot drive a validator hard gate yet
```

(Matches the founding example `../../examples/detail-beside-the-subject.md` — the harness re-derives it to prove `distill` is repeatable.)

## Step B — `emit-validator` output body (real claim map)

Claim map pre-sorted into the validator's five authority classes; handoff target `ux-evidence-validator --mode spec`:

```yaml
pattern_id: detail-beside-the-subject
handoff: ux-evidence-validator --mode spec
claim_map:
  - claim: "the detail panel is in-viewport and horizontally adjacent to the inspected element when that element is active"
    claim_class: hard_gate                 # mechanically checkable via DOM geometry
    feeds_field: "spec.scenario.assertion (bounding-box adjacency + both in viewport)"
    fixtures_needed: [good: "rail beside target", bad: "panel below fold", false_positive: "adjacent but occluded"]
  - claim: "detail updates within one interaction of selecting/hovering the subject"
    claim_class: soft_flag                 # latency/UX heuristic, not a hard gate
    feeds_field: "spec.soft_flag"
  - claim: "co-visibility reduces perceived effort / divided attention"
    claim_class: human_study               # subjective, not browser-observable
    feeds_field: "residue.human_review"
  - claim: "looks balanced beside a wide stack"
    claim_class: screenshot_review
    feeds_field: "spec.screenshot_review"
honesty_note: "status=seed (anecdote). The hard_gate claim is a spec/fixture PROPOSAL; promotion to a calibrated gate needs fixture-plan -> calibrate + a 2nd session."
```

## Conformance
- [x] pattern conforms to `ux-pattern` schema; `status: seed`
- [x] every `claim_map` entry names a real validator field (`feeds_field`) — no invented fields
- [x] honesty rule: anecdote pattern's hard_gate is a *proposal*, explicitly not a promoted gate
- [x] enters at `--mode spec` (never runs the harness)

**Result: pass.**
