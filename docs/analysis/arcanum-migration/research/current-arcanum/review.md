# Review — Current Arcanum research package

**Verdict: FIX.** Five MAJOR and two MINOR findings survived independent falsification. `research-initial-definitions.md` and `research.md` remain fit for purpose; `findings.md` and the closing session need correction before their synthesis can safely inform `analysis.md` or migration decisions.

## Coverage

Dispatch: `2026-08-28-current-arcanum-detailed-review`

The review used three independent attackers, one evidence-preserving writer, and one independent skeptic. Every attacker inspected all four frozen targets. The writer deduplicated the returns without erasing disagreements; the skeptic then tried to refute every provisional finding. Only the skeptic's terminal dispositions appear below.

| Agent | Lens | Targets | Result |
|---|---|---|---|
| Beer, Stafford | Fidelity, governance, ownership, research authority | All four | 6 provisional findings |
| Turing, Alan | Mechanics, reproducibility, coverage, reference integrity | All four | 5 provisional findings |
| Kahneman, Daniel | Operability, explanatory sufficiency, abuse resistance, decision safety | All four | 6 provisional findings |
| Shannon, Claude | Evidence-preserving synthesis | All targets and attacker returns | 8 deduplicated candidates |
| Popper, Karl | Independent falsification and false-positive control | All targets, returns, and candidates | 5 MAJOR verified, 2 MINOR verified, 1 refuted |

Frozen targets:

- `docs/analysis/arcanum-migration/research/current-arcanum/research-initial-definitions.md`
- `docs/analysis/arcanum-migration/research/current-arcanum/research.md`
- `docs/analysis/arcanum-migration/research/current-arcanum/findings.md`
- `sessions/2026-08-28-1239-current-arcanum-research.md`

All four target hashes remained unchanged through the terminal gate.

## Findings

### MAJOR-01 — The RQ coverage table does not establish the coverage it claims

**Locator:** `findings.md:139-166`; compare `research-initial-definitions.md:36-94` and `sessions/2026-08-28-1239-current-arcanum-research.md:21`.

The table has a single `Status` column even though the registered synthesis required separate administrative and evidential states. Several rows also answer a different question from the registered obligation. In particular, RQ-14 asks which source is authoritative during disagreement, but the corresponding findings row reports that a bounded historical cross-owner chain exists. RQ-20 asks about coordination, workarounds, mitigations, effectiveness, and cost, while its row answers general complexity and projection cost. RQ-06, RQ-15, and RQ-19 are also materially incomplete or shifted.

**Consequence:** Row presence, combined with the session statement that all twenty-four questions are covered, can promote unanswered evidence obligations into apparently completed coverage.

**Required change:** Rebuild the table against the literal `RQ-00`–`RQ-23` questions, restore exact identifiers, separate administrative from evidential state, and correct the session's coverage statement.

### MAJOR-02 — Evidence classes are collapsed while the synthesis claims they remain distinct

**Locator:** `findings.md:78-89,132-137,155-156`; `research-initial-definitions.md:101-105`; `research.md:241-246`.

The baseline correctly says that code does not prove successful execution and fixtures do not prove integration. The synthesis nevertheless groups contracts, source text, stored receipts, and pre-existing records under “Documentary assertion,” then claims the finer evidence classes remain distinct. It also calls the bounded Task Session core “functioning” based on implementation inspection and fixtures, although the raw return states that no fixture suite was executed and stored evidence was inspected rather than replayed.

**Consequence:** A later reader cannot reliably tell whether a behavior is documented, implemented, fixture-backed, historically observed, recomputed, or exercised in the current inquiry.

**Required change:** Tag every material claim as contract, implementation, fixture/test, historical receipt, current execution, or recomputation. Relabel Task Session as implemented with stored fixture evidence and current execution unverified.

### MAJOR-03 — Operational-cost language exceeds the measured evidence

**Locator:** `findings.md:60,74,105,107,150,163`; `research.md:100-110,251-256,267,277,300-301,327-334`.

The synthesis asserts operational friction, increased diagnosis cost, and added projection or coordination cost. The raw returns preserve bounded evidence of manual mediation and a demonstrated blocked Research topology, but they explicitly leave aggregate runtime consequence, recurrence, operator time, error rate, cognitive burden, and projection-consumer impact unmeasured.

**Consequence:** Unsupported burden language can bias problem severity and migration priority despite the package's own `claim <= proof` constraint.

**Required change:** Keep the witnessed manual mediation and blocked-topology consequence. Mark aggregate friction, diagnosis cost, coordination cost, and projection cost as unknown or unmeasured; do not erase separately demonstrated implementation limitations.

### MAJOR-04 — The blocked-close narrative overstates causal and ownership evidence

**Locator:** `findings.md:97,103,130`; `sessions/2026-08-28-1239-current-arcanum-research.md:21`; handoff and close-input artifacts cited at `findings.md:195`.

The targets attribute the registered topology to the active generated projection and state that the registrar rejected close because it expected six agents. The preserved handoff proves a registered/canonical topology disagreement and a blocked gate. The preserved close input proves that a three-agent close was attempted, and the missing ledger close row proves non-acceptance. None of these immutable artifacts preserves the registrar diagnostic or proves which component authored the registered topology.

**Consequence:** The package assigns causation and failure ownership more strongly than its preserved evidence supports.

**Required change:** State only the proved topology mismatch, blocked handoff, submitted three-agent close, and absent close row. Label the exact rejection reason and projection provenance as parent-reported unless an original immutable diagnostic is cited.

### MAJOR-05 — A historical registrar failure is presented as current behavior

**Locator:** `findings.md:103,130,182`; `sessions/2026-08-28-1239-current-arcanum-research.md:36,41`; current registrar implementation at `arcana/subagent-strategy/scripts/append-dispatch.cjs:296-316,555-564` and its acceptance test at `arcana/subagent-strategy/development/test-append-dispatch.cjs:515-526`.

The research describes truthful partial-fan-out close as currently impossible and carries that point into the session's current open questions. Later bounded remediation now distinguishes planned, launched, and unlaunched counts and accepts truthful partial counts for non-resolved closes. The original 2026-08-28 dispatch remains historically open, but that is no longer equivalent to current registrar behavior.

**Consequence:** A later update to `analysis.md` could misstate a dated, subsequently remediated failure as an active system limitation.

**Required change:** Date-bind the failure to the registrar observed on 2026-08-28 and explicitly separate the still-open historical ledger row from current close-record behavior.

### MINOR-01 — Load-bearing claim traceability is too fuzzy

**Locator:** `findings.md:17,43-58,95-109,184-195`.

The defect is traceability, not evidence absence. The findings document provides thematic anchors, and `research.md` contains detailed source locators, but the broad “Raw evidence returns: research.md” pointer does not identify which return supports several enumeration, projection-drift, runtime, and operability claims.

**Consequence:** Reviewers must reconstruct provenance manually, increasing the chance that parent synthesis is mistaken for reproduced or directly inspected evidence.

**Required change:** Add stable raw-return heading or line locators and exact original-source locators wherever the current thematic anchors do not resolve a load-bearing claim.

### MINOR-02 — Candidate `KILL` verdicts drift from the governing Research contract

**Locator:** `findings.md:168-182`; `.agents/skills/research/SKILL.md:92-100,120-129`.

The Research contract permits `KILL` only for `no-witness` or `tautological`. The matrix instead uses labels such as “contradicted implementation claim,” “authority boundary,” and “executable counterexample.” The underlying negative evidence may still be sound, so the verified defect is contract vocabulary and deterministic interpretation, not necessarily the substance of each rejection.

**Consequence:** Human and deterministic consumers cannot interpret terminal verdicts consistently with the governing Research contract.

**Required change:** Restate each bounded candidate and normalize supported `KILL` rows to `no-witness` with an exact zeroing fact, or leave the candidate pending.

## Refuted candidate

The skeptic dropped the proposed defect concerning reuse of the exact `7,817` files / `29` scopes denominator. The requested caveat already exists: `findings.md:17,199` and `research.md:64,145` describe the count as a dirty-tree, non-reproducible point-in-time snapshot and do not claim that it is a durable repository-universe denominator.

## Artifact verdicts

| Artifact | Verdict | Rationale |
|---|---|---|
| `research-initial-definitions.md` | KEEP | The scope, questions, evidence ceilings, and present-system boundary are coherent. The later synthesis does not fully satisfy them. |
| `research.md` | KEEP | It preserves raw returns, limitations, disagreement, and the blocked lifecycle without promoting them to accepted findings. |
| `findings.md` | FIX | It contains all seven surviving defects: RQ coverage, evidence classification, claim strength, traceability, causal attribution, temporal accuracy, and verdict vocabulary. |
| `sessions/2026-08-28-1239-current-arcanum-research.md` | FIX | It repeats the overbroad coverage, causal, evidence-separation, and current-state claims. |

## Change requests

1. Rebuild the RQ table against the literal `RQ-00`–`RQ-23` obligations with separate administrative and evidential states.
2. Apply the declared evidence taxonomy claim by claim and distinguish current execution from implementation, fixtures, and stored historical evidence.
3. Remove or qualify unmeasured aggregate operational-cost language while retaining bounded witnessed consequences.
4. Narrow the topology and close-rejection narrative to preserved evidence; label unsupported provenance and causation.
5. Date-bind the partial-fan-out failure and distinguish the open historical row from remediated current behavior.
6. Add exact claim-level source and raw-return locators where thematic anchors remain ambiguous.
7. Normalize candidate verdicts to the Research contract's permitted `KILL` vocabulary.
8. Update the closing session so its summary and open questions match the corrected evidence state.

## Evidence boundary

This review used only the frozen targets, the declared governing and comparator corpus, and repository-local artifacts directly relevant to the claims under test. Later partial-closeout remediation was used only to test whether a historical claim remained valid as a current-state assertion; it was not retroactively credited to the original research.

The review did not use external research, excluded worktree changes, future architecture, or migration design. No reviewed target was edited. The only review deliverable created by this dispatch is this file.

Cleared axes remain meaningful: the initial definitions preserve the present-system boundary and `claim <= proof`; raw returns remain explicitly provisional; owner-preserving handoffs are supported; the package openly discloses the blocked original handoff, absent original skeptic gate, partial fan-out, dirty-tree state, and open historical ledger row.
