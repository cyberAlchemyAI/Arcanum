# Distill v2 Machine Contract — Decision Record

- Gate ID: `DISTILL-V2-DECISION-GATE-2026-08-27`
- Status: `PASS`
- Machine decisions resolved: 10 of 10 (`D01`–`D10`)
- Grouped gate decisions resolved: 2 of 2
- Blockers remaining: 0
- Authority effect: `none`
- Normal Task Session route: excluded by explicit user direction for this gate
- Contract-posture request digest: `6cc714f48d32148bafde442353290c9a73ea74aa41ecc81a164d8d71b24cff0a`
- Contract-posture routing: `gate` (`4/4` options admissible)
- Mode-budget request digest: `d0e15255433e49017977e6b5faa2149910e1de6e71d4759cd7afab055615a73a`
- Mode-budget routing: `gate` (`4/4` options admissible)
- Machine decision source: `DISTILL-V2-DECISION-RECORD.json`

## Decision 1 — Contract Posture

Question: should the eight-schema Distill semantic core be strict or accept
historical adapter vocabulary directly?

### `STRICT-V2-8` — Recommended

- Benefit: one canonical writer vocabulary, smaller validators, clearer ownership.
- Cost/risk: old hyphen IDs and alternate wire fields need explicit adapter mapping.
- Choose when: v2 should be the clean semantic authority and compatibility is a boundary concern.
- Downstream impact: resolves D02, D03, D05–D10 with independent ModeSpec and
  TechniqueSpec instances, underscore IDs, `true_subagent`/`role_simulation`,
  `path`/`sha256`/`size_bytes`, strict verdict/route rules, one semantic family,
  and a complete normalized RunFrame.

### `COMPATIBILITY-V2-8`

- Benefit: historical hyphen IDs, execution labels, and exact-ref variants can enter the core directly.
- Cost/risk: larger schemas and validators; adapter vocabulary becomes permanent semantic surface.
- Choose when: existing producers cannot be versioned or mapped at the boundary.
- Downstream impact: all aliases, mappings, precedence rules, and ambiguity negatives must be implemented before the first writer.

### `DEFER-DISTILL-V2-CONTRACT`

Records the decision as deferred and leaves every schema SWU blocked.

### `STOP-DISTILL-V2`

Ends this v2 effort without schema or runtime mutation.

Selected option: `STRICT-V2-8`.

- Source: exact user selection in the active Decision Gate conversation.
- Recorded: 2026-08-27.
- Rationale: v2 is the clean semantic authority; compatibility remains an
  explicit versioned adapter concern rather than entering the core vocabulary.
- Decision effect: resolves the contract posture only; no schema or implementation authority.

## Decision 2 — Exact Mode Budgets

Decision 1 selected an action option, so this is now the active blocker question.

### `FROZEN-DOCUMENTED-BUDGETS`

| Mode | Tracks min/default/max | Rounds min/default/max |
| --- | --- | --- |
| Compact | 1 / 1 / 1 | 1 / 1 / 1 |
| Standard | 1 / 1 / 1 | 2 / 2 / 2 |
| Tournament | 3 / 3 / 3 | 2 / 2 / 2 per track |
| Deep | 2 / 2 / 2 | 3 / 3 / 3 per track |
| Validate | 1 / 1 / 1 | 1 / 1 / 2 |

- Benefit: smallest deterministic denominator; directly reflects documented defaults.
- Cost/risk: callers cannot request a deeper or wider bounded run without a new profile version.

### `BOUNDED-OVERRIDE-BUDGETS` — Recommended

| Mode | Tracks min/default/max | Rounds min/default/max |
| --- | --- | --- |
| Compact | 1 / 1 / 1 | 1 / 1 / 1 |
| Standard | 1 / 1 / 1 | 1 / 2 / 3 |
| Tournament | 2 / 3 / 5 | 1 / 2 / 3 per track |
| Deep | 2 / 2 / 4 | 2 / 3 / 5 per track |
| Validate | 1 / 1 / 1 | 1 / 1 / 2 |

- Benefit: preserves documented defaults while making every override finite and testable.
- Cost/risk: larger fixture matrix and higher worst-case reasoning cost.

### `DEFER-MODE-BUDGETS`

Leaves ModeSpec instances and budget-negative fixtures blocked.

### `STOP-DISTILL-V2`

Ends this v2 effort without schema or runtime mutation.

Selected option: `BOUNDED-OVERRIDE-BUDGETS`.

- Source: exact user selection `1`, mapped by the immediately preceding Decision Gate presentation.
- Recorded: 2026-08-27.
- Rationale: preserve documented defaults while allowing finite, schema-testable
  overrides without unbounded tracks or rounds.
- Decision effect: resolves D04 only; no schema or implementation authority.

## Remaining Gate Rules

- The standing `Explain / more context` choice never selects an option.
- A selected action resolves semantic design only; it does not authorize
  publication, deployment, registry promotion, external effects, or unrelated Invoke mutation.
- Because the user excluded the broken normal Task Session process, the eventual
  implementation continuation must be separately bounded to exact schema targets,
  baselines, validations, and stop conditions after this gate passes.

## Sources

- `../SCHEMA-PLAN.md`
- `../DISTILL-VALIDATION.json`
- `../../audits/2026-08-27-distill-v2/DISTILL-V2-AUDIT.json`
- `../../techniques/README.md`
- `../../SIGIL-HANDOFF.md`
- `DISTILL-V2-CONTRACT-POSTURE-REQUEST.json`
- `DISTILL-V2-CONTRACT-POSTURE-RECEIPT.json`
- `DISTILL-V2-MODE-BUDGET-REQUEST.json`
- `DISTILL-V2-MODE-BUDGET-RECEIPT.json`

## Next Step

Decision Gate is complete. The next safe route is to prepare a separately
bounded direct implementation contract for SWU-DV2-001 because the normal Task
Session route was explicitly excluded. Gate PASS does not itself authorize
schema mutation, publication, deployment, registry promotion, or external effects.
