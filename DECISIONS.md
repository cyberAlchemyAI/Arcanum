# Decisions

## GUIDE-B-003: First Guide Spellcraft Target

| Field | Value |
| --- | --- |
| Status | `pass` |
| Timestamp | `2026-05-29T19:00:44Z` |
| Target scope | `development/user-guide/packages/guide/` |
| Consequential work blocked | Mutation-capable `spellcraft` for Guide. |
| Source | `development/user-guide/packages/guide/WORK-PACK.md`, `development/user-guide/packages/guide/SPELLCRAFT-HANDOFF.md` |

### Decision Question

Should the first Guide spellcraft target be narrow `guide-architecture` or generic `guide`?

### Options

| Option | Benefit | Cost / Risk | Choose When | Downstream Impact |
| --- | --- | --- | --- | --- |
| `guide-architecture` | Narrow, fixture-backed, easier to validate; directly matches the existing `/guide this architecture` route fixture. | May feel less general at first; later generalization step required. | We want the smallest reliable spellcraft slice. | Spellcraft can start with architecture-specific phases, fixtures, and validation. |
| `guide` | Matches the long-term user-facing command immediately. | Broader surface, more dispatch cases, higher risk of vague orchestration and under-specified validation. | We want to design the generic umbrella now and accept slower validation. | Spellcraft must define route families and stricter dispatch budgets before implementation. |

### Recommendation

Select `guide-architecture` first, then generalize to `guide` after one validated spell slice exists.

### Selected Option

`guide-architecture`

### Rationale

The user selected option 1 via `invoke refresh 1`. `guide-architecture` is narrow, fixture-backed, and directly matches the existing `/guide this architecture` route fixture. This keeps the first spellcraft slice small enough to validate before generalizing to a broader `guide` spell.

### Remaining Blockers

- None for first spellcraft target selection. `GUIDE-B-003` is resolved.

### Deferred Decisions

- Runtime dispatch budget defaults.
- Allowed callable capabilities in Guide L0.

### Assumptions

- User ledger and Translate L0/L2 evidence remain valid inputs.
- Spellcraft should start with `guide-architecture`, then generalize later to `guide`.
