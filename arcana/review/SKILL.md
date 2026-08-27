---
name: review
description: Red-team existing skills, constitutions, code, schemas, plans, or documents and return verified, severity-ranked change requests. Use when the target already exists and needs adversarial fidelity, correctness, ownership, operability, or abuse-resistance review. Use research instead when the question is whether a new claim or candidate survives.
---

# Review

<objective>
Attack an existing artifact from independent lenses, verify every surviving
finding against the literal target, and return actionable change requests
without modifying the target during the review.
</objective>

<ownership-boundary>
Review owns review-type judgment: attack lenses, severity, verification, and the
change-request report. The repository-local `subagent-strategy` skill owns the
dispatch trigger, proposal, confirmation, runtime bindings, dependency
execution, final approval, closeout, and observability.

Review does not create research verdicts on new candidates and does not apply
its own fixes. Fixes require a subsequent authorized change task.
</ownership-boundary>

<stage-handoff-contract>
Before a blocking sequential or zig-zag edge advances, the producing group must
emit an `arcanum.stage-handoff.v0.1` JSON record and pass
`node arcana/subagent-strategy/scripts/validate-stage-handoff.cjs <handoff.json>`.
The record binds the dispatch and edge identities, verdict, and evidence refs.
`needs_feedback` also binds the typed defect, repair owner group, feedback edge,
and remaining loop budget. Only `ready` unlocks the downstream group.
</stage-handoff-contract>

<output-mode>
Produce exactly one synthesis document named `review.md`:

- `inline`: render the complete document in chat and omit `working_folder`;
- `persisted`: write `<working_folder>/review.md` after the human confirms the
  destination.

Do not persist attacker transcripts, `attacks.md`, or `findings.md`. The proof of
a review finding is the cited or quoted target artifact, not an agent return.
</output-mode>

<attack-model>
Use two or more pairwise-tensioned attack lenses when the task merits a dispatch:

- fidelity/governance: contradictions with governing authority;
- mechanics/correctness: failures, broken validation, or doc/code mismatch;
- ownership/reference integrity: dangling pointers or double ownership;
- operability: steps a fresh operator cannot execute without invention;
- abuse/gaming: rules satisfiable in letter while defeated in purpose.

Roles:

- `explorer` as attacker: reads the whole target corpus through one lens;
- `writer` as synthesizer: deduplicates and severity-ranks findings;
- `skeptic` as verifier: tries to refute each finding against the target;
- optional `auditor`: checks coverage and ensures refuted findings were removed.

No attacker verifies its own finding. When the parent authored the target, a
surviving recommendation to revert that work escalates to the human rather than
being self-approved.
</attack-model>

<process>
1. Resolve the exact target corpus and choose inline or persisted output.
2. Ask `subagent-strategy` whether the review merits a dispatch. Keep a small
   direct review inline when coordination would add no value.
3. Design pairwise-tensioned attack lenses over the whole corpus; do not divide
   targets into unchallenged partitions.
4. Pass repository-local tension and human-confirmation gates.
5. Run attackers read-only, synthesize provisional findings, and have independent
   verifiers test them against the literal artifacts.
6. Drop refuted findings rather than softening them.
7. Write the single `review.md` document in the confirmed channel.
8. Obtain final approval and close every agent and dispatch record through
   `subagent-strategy`.
</process>

<finding-contract>
Every surviving finding contains:

- target file or artifact;
- exact locator and a short quotation or directly observed behavior;
- severity: `CRITICAL`, `MAJOR`, or `MINOR`;
- consequence;
- one bounded proposed fix.

Use `CRITICAL` for system breakage, corruption, or direct contradiction of
governing law; `MAJOR` for functional gaps, drift risks, or load-bearing
omissions; and `MINOR` for wording, stale metadata, or fuzzy pointers.

An artifact verdict is `FIX` when at least one CRITICAL or MAJOR finding
survives; otherwise it is `KEEP`. A verified `FIX` report is a successful review
deliverable, not a failed review.
</finding-contract>

<report-shape>
```markdown
# Review — <target corpus>

## Coverage
| attacker | lens | targets checked | findings raised | zero-findings defense |

## Findings
| # | artifact and locator | evidence | severity | consequence | proposed fix |

## Artifact verdicts
| artifact | KEEP or FIX | rationale |

## Change requests
1. <surviving requests ordered by severity>

## Evidence boundary
<what was and was not checked>
```
</report-shape>

<quality-bar>
- Every target is attacked from every declared lens.
- Every finding is independently verified against the target.
- Every surviving finding has a locator, evidence, severity, consequence, and
  bounded fix.
- Zero findings require a defense describing the attacks attempted.
- A universal zero-finding result is treated as a failure to attack unless the
  coverage auditor or parent demonstrates otherwise.
- Review remains read-only over the target artifacts.
</quality-bar>

<anti-patterns>
Avoid target partitioning disguised as tension, self-verification, findings
supported only by agent opinion, persisting transcripts, silently applying
fixes, lowering severity to preserve consensus, or calling a new-candidate
investigation a review.
</anti-patterns>
