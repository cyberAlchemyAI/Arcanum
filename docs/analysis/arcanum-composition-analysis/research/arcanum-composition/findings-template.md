# Findings — Arcanum Composition

> Output contract imported and locally specialized from
> `../domainspec/.claude/skills/research/SKILL.md`. This template is binding for
> the confirmed dispatch.

## Research-question coverage

Include exactly one row for every registered question `RQ-0` through `RQ-10`.
Do not combine RQs in this table and do not omit a question silently.

| RQ id | status | answer | addressable evidence | contrary evidence / material uncertainty | boundary |
|---|---|---|---|---|---|
| RQ-0 | unresolved |  |  |  |  |
| RQ-1 | unresolved |  |  |  |  |
| RQ-2 | unresolved |  |  |  |  |
| RQ-3 | unresolved |  |  |  |  |
| RQ-4 | unresolved |  |  |  |  |
| RQ-5 | unresolved |  |  |  |  |
| RQ-6 | unresolved |  |  |  |  |
| RQ-7 | unresolved |  |  |  |  |
| RQ-8 | unresolved |  |  |  |  |
| RQ-9 | unresolved |  |  |  |  |
| RQ-10 | unresolved |  |  |  |  |

Allowed statuses are only:

- `answered`: cited evidence resolves the whole RQ within its confirmed scope;
- `unresolved`: record any supported partial conclusion and the exact residual gap;
- `deferred`: record why the confirmed dispatch excluded it;
- `retired`: cite the authoritative scope decision that retired it.

Every load-bearing answer must cite the original repository source and, when
useful, the stable return ID in `research.md`. Classify each cited support as one
of:

- `documentary assertion`;
- `executable observation`;
- `independent recomputation`;
- `formal proof`.

Do not treat these evidence classes as interchangeable. Do not infer absence
from failure to find evidence. An `unresolved` row must name what was inspected,
what check was attempted, and the exact remaining gap. State material contrary
evidence, residual uncertainty, and the boundary beyond which the answer does
not apply. Use `none found in <named scope>` only when that scope is explicit.

## Candidate verdict matrix

Keep candidate judgment orthogonal to RQ coverage.

| candidate | owner (precedent) | witnessed? (non-vacuity) | sound? (definitional) | verdict | use-mode |
|---|---|---|---|---|---|

- `GO`: witnessed and sound; use-mode is `build-from-owned`,
  `already-deployed`, or `novel-attempt`.
- `KILL`: only `no-witness` or `tautological`, recorded as a typed negative.
- Ownership labels a candidate; it is never by itself a negative verdict.

## Conclusions

State only conclusions supported by the RQ coverage and candidate matrix.

## Implications

Keep current-state consequences separate from later design or implementation
decisions.

## Dissent and contrary evidence

Preserve surviving disagreements, counterexamples, conflicting authorities,
and reversals.

## Limitations and evidence boundary

State missing witnesses, uninspected surfaces, failed checks, uncertainty, and
the exact limits of generalization.

## One-line answer to the research goal

Close with one sentence answering the dispatch objective at no greater strength
than the evidence permits.
