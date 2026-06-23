---
name: ux-lessons
description: "Use when: turning a UI iteration session into saved lessons and reusable ux-patterns that later feed ux-evidence-validator and ui-prototyping-studio."
argument-hint: "<session-or-pattern-ref> [--mode capture|distill|promote|emit-validator|emit-studio]"
tier: arcana
domain: frontend-ux-learning
version: 0.1.0-seed
origin: created from the 2026-06-23 refine run (arcana/ux-lessons/development/refinement-runs/2026-06-23-ux-lessons) using the x-ray HTML iteration session as the founding fixture
allowed-tools: Read, Write, Glob, Grep
---

# Sigil: UX Lessons

<objective>
Capture the learning residue of a UI iteration session as typed `lesson` records, distill recurring lessons into reusable `ux-pattern` cards, and emit those patterns as consumer-ready intents for `ux-evidence-validator` and `ui-prototyping-studio` — without re-implementing session capture, pattern storage, or validation.
</objective>

<logic-type>
Arcana: cross-session UX learning translation. A thin producer that owns two typed artifacts and two consumer adapters and composes existing owners for everything else.
</logic-type>

<status>
Seed. The artifact contract, modes, and one founding example exist. No experiment-harness evidence and no cross-session promotion evidence yet. Claim ≤ proof: a `ux-pattern` is `seed` until usage evidence supports it.
</status>

<thin-sigil-boundary>
UX Lessons owns ONLY:

- the `lesson` schema,
- the `ux-pattern` schema,
- the two consumer adapters (`emit-validator`, `emit-studio`),
- the promotion honesty gate.

It COMPOSES (never re-implements) these owners:

| Concern | Owner (composed) |
| ------- | ---------------- |
| session signal capture | `signal-observer` / `observed-invocation-loop` |
| session → analysis shape | `workflow-reflect` (shape borrowed) |
| lesson → pattern reduction | `distill` |
| reusable pattern store mechanics | `architecture-pattern-inventory` (cards under a `ux` tag) |
| residue ledger | `residuality-spec` |

It NEVER: runs Playwright validation (that is `ux-evidence-validator`), or mutates studio sessions / generates variants (that is `ui-prototyping-studio`). UX Lessons emits cards and intents; the consumers own execution.
</thin-sigil-boundary>

<modes>
| Mode | Use when | Output |
| ---- | -------- | ------ |
| `capture` | A UI iteration session just happened; harvest raw lessons. | One or more `lesson` records (anecdote-tagged on first capture). |
| `distill` | ≥1 lessons describe a recurring move. | A candidate `ux-pattern` card (status `seed`). |
| `promote` | A pattern has accrued cross-session signal. | Pattern status advanced `seed → calibrated → promoted`, honesty gate enforced. |
| `emit-validator` | A pattern should feed evidence validation. | A claim map across the validator's five authority classes → handoff to `ux-evidence-validator --mode spec`. |
| `emit-studio` | A pattern should steer prototyping. | A `CommentEvent` → `MutationTask` annotation intent for `ui-prototyping-studio`. |
| `emit-studio-fitness` `[PARKED]` | A pattern should bias studio explore/exploit selection. | A `studio_fitness_intent` (`ux-pattern` → `FitnessSignal`/`FitnessVector` candidate). **Designed, not built** — re-tags the `emit-validator` claim map onto the studio's hard-gate/soft-gradient split (`confidence = f(signal_strength)`; anecdote ⇒ soft only). |

> **`emit-studio-fitness` is PARKED.** The mapping is designed and falsification-tested (`development/refinement-runs/2026-06-23-ux-lessons-w8-studio-fitness/RESULT.md`) but **not built**. Un-park only when ui-prototyping-studio ships a per-candidate axe/layout evaluator in the cycle AND resolves **OQ-5** (soft-score weights). Until then it emits nothing.
</modes>

<lesson-schema>
One captured iteration unit, still contextual.

```yaml
lesson_id:               # kebab id, e.g. L-xray-02
session_ref:             # pointer to the session (path / run-id / signal ref)
context:                 # what was being built and for whom
iteration_step:          # which move in the session
trigger:                 # what prompted the change
failure_mode:            # the problem the change fixed
change:                  # what was done
before_after:
  before_ref:            # artifact/screenshot before
  after_ref:             # artifact/screenshot after
  screenshot_refs: []    # evidence images
evidence: []             # enum-constrained, see below
signal_strength:         # anecdote | repeated | cross_session
generalizable_principle: # the reusable claim
residue:                 # what is unresolved / parked
promoted_to:             # pattern_id | null
```

**Evidence enum** (`evidence[]` values must be one of) — the replayable shapes `ux-evidence-validator` already consumes:
`dom_measurement | aria_snapshot | screenshot_diff | trace_event`.

**Honesty rule:** `signal_strength: anecdote` ⇒ `promoted_to` may NOT target a validator `hard_gate`. Anecdote lessons can feed `soft_flag` / `screenshot_review` only.
</lesson-schema>

<ux-pattern-schema>
The reusable distillate (architecture-pattern-inventory card shape + two intake blocks).

```yaml
pattern_id:              # kebab id, e.g. detail-beside-the-subject
name:
intent:
problem:
solution:
when_to_use:
anti_pattern:
forces: []
evidence_link:           # lesson_id(s) + evidence refs
status:                  # seed | calibrated | promoted
residue:
consumer_intake:
  validator:             # one or more
    - claim_class:       # hard_gate | soft_flag | screenshot_review | human_study | not_automatable
      mode:              # ux-evidence-validator mode entered, e.g. spec
      feeds_field:       # the exact validator field/claim this feeds
  studio:
    intent:              # e.g. reposition | reword | restructure
    comment_event_template:   # CommentEvent shape
    mutation_task:            # MutationTask shape
```

**Anti-overbuild guard:** a `consumer_intake` entry may only assert a check if it names the exact consumer field it feeds. No speculative fields.
</ux-pattern-schema>

<consumer-contracts>
- **ux-evidence-validator** (`emit-validator`): a `ux-pattern` becomes a **claim map pre-sorted into the five authority classes** (`hard_gate`, `soft_flag`, `screenshot_review`, `human_study`, `not_automatable`), entering at `--mode spec` then `fixture-plan` → `calibrate`. UX Lessons never runs the harness. This is the ready path.
- **ui-prototyping-studio** (`emit-studio`): a `ux-pattern` becomes a `CommentEvent{ target{odId, selector, elementLabel}, severity, intent, note }` → `MutationTask{ odId, changeType }`. The annotation path is ready. The **variant-generation / fitness** intake is a named upgrade, **deferred** until studio **OQ-5** is resolved AND an axe-core + layout-overflow fitness evaluator exists.
</consumer-contracts>

<applicability>
Use this sigil when:

- a UI iteration session produced changes worth keeping as reusable lessons,
- a recurring UX move should become a named, evidence-linked pattern,
- a pattern should be handed to `ux-evidence-validator` as validator-safe claims,
- a pattern should be handed to `ui-prototyping-studio` as annotation intents,
- prior-session residue should be recovered and deduplicated into patterns.
</applicability>

<non-applicability>
Do not use this sigil when:

- you want to run browser validation now (use `ux-evidence-validator`),
- you want to generate or mutate UI variants now (use `ui-prototyping-studio`),
- the input is generic workflow telemetry, not UX iteration (use `workflow-reflect`),
- you need a generic pattern store unrelated to UX (use `architecture-pattern-inventory`),
- there is no session evidence — patterns may not be invented without a lesson.
</non-applicability>

<inputs>
Expected inputs, if available:

- a session reference (path, run-id, or signal ref) for `capture`,
- existing `lesson` records for `distill`,
- a `ux-pattern` id for `promote` / `emit-*`,
- the target consumer for `emit-*`,
- screenshot / evidence artifacts.
</inputs>

<process>
1. Resolve the mode and the session/pattern reference.
2. `capture`: read the session evidence; write `lesson` records using `templates/lesson.md`; tag `signal_strength` honestly (first capture is usually `anecdote`); constrain `evidence[]` to the enum.
3. `distill`: group lessons describing the same move; call `distill` to reduce them to one coherent `ux-pattern` card using `templates/ux-pattern.md`; set `status: seed`.
4. `promote`: only advance `status` when signal strength supports it; enforce the honesty rule (anecdote ⇏ hard_gate); record residue for parked items.
5. `emit-validator`: produce the five-class claim map and the `--mode spec` handoff; every claim names the field it feeds.
6. `emit-studio`: produce the `CommentEvent` → `MutationTask` intent; never write to studio sessions.
7. Store patterns as `ux`-tagged `architecture-pattern-inventory` cards; do not create a new store.
8. Preserve the evidence/inference boundary in every artifact (source evidence vs distilled principle).
9. Emit an observability signal for meaningful executions.
</process>

<quality-bar>
A successful run must:

- write typed `lesson` / `ux-pattern` artifacts that conform to the schemas,
- keep `evidence[]` within the enum,
- enforce the anecdote → no-hard-gate honesty rule,
- name the exact consumer field every `consumer_intake` entry feeds,
- compose the five owners rather than re-implementing them,
- never run validation or mutate studio sessions,
- store patterns as `ux`-tagged inventory cards, not a new store,
- keep a `ux-pattern` at `seed` until usage evidence supports promotion,
- emit an observability signal for meaningful executions.
</quality-bar>

<anti-patterns>
Avoid:

- inventing a `ux-pattern` with no backing `lesson`,
- promoting an anecdote-signal pattern to a validator hard gate,
- adding `consumer_intake` fields that name no consumer field,
- forking a second reusable-pattern store instead of using `architecture-pattern-inventory`,
- re-implementing session capture, distillation, or residue mechanics owned elsewhere,
- shipping the studio variant/fitness intake before its named unblock (OQ-5 + fitness evaluator),
- claiming promotion readiness without experiment-harness evidence.
</anti-patterns>

<observability>
Meaningful execution: any `capture`, `distill`, `promote`, or `emit-*` that writes or attempts to write a lesson, pattern, or consumer intent.

Recommended signal fields: sigil name, mode, lessons captured, patterns distilled, pattern status changes, honesty-rule enforcements, consumer emitted, blocked reasons, reflection trigger state.
</observability>

<promotion-gate>
UX Lessons is promotion-ready only after experiment evidence shows:

- ≥2 sessions captured into lessons with honest signal tagging,
- ≥1 `ux-pattern` distilled and emitted to BOTH consumers with zero invented fields,
- the anecdote → no-hard-gate rule enforced at least once,
- cross-session promotion (`anecdote → repeated → cross_session`) demonstrated,
- the validator claim map ingested by `ux-evidence-validator --mode spec`,
- the studio annotation intent validated against `ui-prototyping-studio` SPEC.
</promotion-gate>

<output-contract>
Return:

```markdown
## UX Lessons Result

- Mode: capture | distill | promote | emit-validator | emit-studio
- Session/pattern ref: <ref>
- Lessons captured: <n or n/a>
- Pattern: <pattern_id and status, or n/a>
- Honesty rule: enforced | not-triggered
- Consumer emitted: ux-evidence-validator | ui-prototyping-studio | none
- Composed owners touched: <list>
- Evidence boundary: <source vs inference note>
- Status: pass | flag | block
- Next: <recommended next mode or route>
```
</output-contract>
