---
name: review
description: Red-team dispatch over EXISTING artifacts (skills, constitutions, code, docs) — attack what exists and hunt flaws to improve it. Routed here from domainspec-subagents-strategy as the LIVE type skill for `dispatch_type: review`. Defines review-type judgment only — attack lenses, severity taxonomy, verification discipline, and the change-request report shape. A review produces ONE artifact, `review.md` (the cited change-request report), and the human chooses at the confirm gate whether it is delivered inline (chat) or persisted to a `working_folder`. Use research (not review) when the question is whether a NEW claim/candidate survives; use review when the target already exists and the deliverable is verified change requests.
---

# review — operating guide for `dispatch_type: review`

**What this is.** You are running a review dispatch: a red team. The targets already exist —
skills, constitutions, code, docs — and the dispatch attacks them to surface flaws worth fixing.

**What you produce.** **Verified change requests**, in exactly **one** document: `review.md`. Not
verdicts on new candidates (that is `research`), and not the fixes themselves — applying a change
request is a follow-up act outside the dispatch, or a re-run after fixes within the loop ceiling.

**Where it lands is the human's choice**, made at the confirm gate and recorded on the row as
`output_mode`:

| `output_mode` | where `review.md` goes | `working_folder` |
|---|---|---|
| `inline` (default) | rendered in chat, no file written | must be **absent** |
| `persisted` | written as `<working_folder>/review.md` | **required**, confirmed at the gate |

**The procedure.** Shape it → Run it → Gate it → Write the report → Close.

> ## ⚠️ `review.md` is review's ONLY artifact — a deliberate exception; do not "fix" it
>
> **The naming.** In `research` and `experiment`, `<type>.md` (`research.md`, `experiment.md`) is the
> **collected verbatim returns**, and `findings.md` is the synthesis. **Review inverts this on
> purpose:** `review.md` is the **synthesis** — the cited change-request report. If you are here
> because review "looks inconsistent with the other types" — it is, knowingly.
>
> **No transcript. At all.** A review persists **no verbatim attacker/verifier returns**: no
> `attacks.md`, no `findings.md`, no appendix of returns inside `review.md`. Attacker returns are
> **working material, not evidence** — a review's proof is the **quoted artifact**, and that lives in
> `review.md` itself. Persisting the returns bought traceability of process, not of truth.
>
> **This was contested and the owner overruled the objection** (2026-07-13, §14/§14.1 — recorded, not
> erased). The objection: without the transcript, the durable record of P14 collapse detection is one
> line in the Coverage section, written by the very synthesizer whose collapse it is meant to detect,
> so no later reader can re-derive whether the attackers actually diverged. **Owner ruling: accepted
> as a known cost.** A review is audited on its conclusions and the artifact quotations that carry
> them — not on its attack process. Do not re-litigate this in a skill edit; amend §14 if you want it
> changed.
>
> (Historical: reviews before 2026-07-13 wrote `attacks.md` + `findings.md`. Those files stay on
> disk as history — the names differ, so nothing is silently reinterpreted.)

## 1. Shape it

Pick the attackers, their lenses, and the shape that carries their findings to a record.

**Roles** — review runs the four agent roles with red-team semantics; each guards one failure
mode, and no agent guards two:

| `role` | red-team function | guards against | model |
|---|---|---|---|
| `explorer` | **attacker** — attacks the full target corpus from ONE declared attack lens | blind spots — one lens sees what another cannot | heavier for subtle lenses |
| `skeptic` | **verifier** — refutes findings against the literal artifact; runs the actual check | false positives — plausible-but-wrong findings surviving | heavy |
| `writer` | **synthesizer** — dedupes, severity-ranks, writes `review.md`; conventionally a single writer | "great attack, no record" | heavy |
| `auditor` | **coverage auditor** — placed downstream of the verifiers; checks every target was attacked from every declared lens and no refuted finding survived; authors the **Coverage** section of `review.md`. **Does work, therefore cannot be the dedicated `final_approver`** (P12) | "passed because nothing was attacked" | light |

A group has no role of its own: its function is read off its agents' roles, and its place in the
workflow off its `connections`. Model is guidance chosen per agent by task difficulty, validated
by the human at the confirm gate.

**Attack lenses** — the tension axes for review. Each attacker takes ONE lens; a group of
n ≥ 2 attackers must spread **≥ 2 distinct lenses, pairwise tensioned** — for every pair a
competent observer could name in advance a question on which the two disagree. The `check-tension`
skill runs this anti-bias check on the sheet at the confirm gate. Established lenses:

- **fidelity / governance** — does the artifact contradict or silently extend its governing law?
- **mechanics / correctness** — does it actually run? doc-vs-code mismatches, broken validation.
- **ownership / reference integrity** — dangling pointers, double-owned concepts, claims about another doc the target does not satisfy.
- **operability** — can a fresh operator execute it end-to-end without inventing steps?
- **abuse / gaming** — can the rules be satisfied in letter while defeated in spirit?

Attackers each read the **whole corpus** (full reading), differing by lens — never by partitioning
the targets between them. `robot_talks: true` on the attacker group is recommended: after the
parallel attacks, each attacker confronts the others' findings along the lens tension before the
group returns one argued result.

**Topology** — the canonical shape:

```
attackers ──sequential──▶ synthesizer ◀──zig-zag──▶ verifiers
    ▲                         │
    └┄┄┄┄┄┄┄┄feedback┄┄┄┄┄┄┄┄┄┘   (conditional)
```

- **Attackers** — a group of `explorer`s, n 2–4, `robot_talks` recommended.
- **Synthesizer** — 1 `writer`, exchanging with the verifiers via **zig-zag**. Because the
  attacker group runs `robot_talks`, the synthesizer MUST receive each attacker's **initial AND
  final** positions (P14, collapse detection). Since review persists no transcript, the strategist
  passes both **in the synthesizer's `initial_prompt`** — and the durable record of collapse is
  the one-line collapse note in `review.md`'s Coverage section, not a file of returns.
- **Verifiers** — `skeptic`s in a zig-zag exchange with the synthesizer.
- The **feedback** back-edge exists only when there is a verifier/auditor group AND material may be
  missing — never by default (shown dashed).
- An optional **coverage-auditor** group (its single agent's role is `auditor`) is placed by its
  incoming edge, downstream of the verifiers.

**The coverage auditor is NOT the `final_approver`** (corrected 2026-07-13 — the prior text called it
"the natural dedicated `final_approver`", which contradicted P12 two paragraphs later). P12's dedicated
approver **does no other work in the dispatch**; the coverage auditor audits coverage, which is work.
So the approver is **`parent`**, or a *separate* agent that does nothing but approve. Both can coexist:
the auditor fires the zero-findings flag, and the approver checks that it fired.

**Author-approval warning (open gap, P12).** P12 forbids the approver from sitting in a working group —
it does **not** forbid `parent` from being the author of the artifact under review. When the strategist
reviews its own change set, `final_approver: parent` puts the author in the approval seat, and
"we already acknowledged that, and kept it anyway" becomes a sentence the approver can say. In that
case, **a surviving finding that recommends reverting the author's own work escalates to the human** —
the parent may not resolve it. This is a stated gap in P12, not a rule it currently enforces.

**Declare the output mode.** The sheet states `output_mode` (and, when `persisted`, the
`working_folder` path). The human confirms both at the gate — see the router's lifecycle step 2.

## 2. Run it

Spawn each group's agents with the Agent tool — **ALL agents of a group in ONE message**, so they
run in parallel. Each agent's `initial_prompt` is its launch prompt.

Schedule groups **by dependency**: a group is READY when every group with a `sequential`/`zig-zag`
edge into it has produced what it must respond to (a zig-zag edge counts only in its `from`→`to`
direction — the `from` endpoint opens the exchange). Launch all READY groups concurrently;
`feedback` edges never count as dependencies; a sheet with no connections declares its groups
independent. Declared order is a narration tiebreak only.

The zig-zag between synthesizer and verifiers converges the moment a verifier turn raises no
objection — the loop cap is a ceiling for non-convergence, not a quota to burn.

**Attackers run read-only over the targets.** They never modify the artifacts under attack —
findings are the only output.

## 3. Gate it

Every surviving finding is one the verifier could not refute. Severity taxonomy:

- **CRITICAL** — breaks the system, corrupts a record, or flatly contradicts governing law.
- **MAJOR** — functional gap, drift risk, doc-vs-code mismatch, load-bearing omission.
- **MINOR** — wording, stale data, fuzzy pointer.

Per-artifact verdict: **KEEP** or **FIX** (FIX iff ≥ 1 CRITICAL or MAJOR survives verification).
A FIX verdict is a deliverable, not a non-resolution.

**Finding discipline.** Every finding carries **the file, a quotation from the artifact under
attack, the severity, and a one-line proposed fix**. The quoted artifact IS the evidence — a
finding whose evidence is only "an attacker said so" is not a finding. (Before 2026-07-13 a
finding also cited the attack return it came from; that rule is **retired** with the transcript —
§14. Cite the artifact, not the agent.)

A finding the verifier refutes is **dropped, not softened** — claim ≤ proof, demote never inflate.

**Zero-findings red flag.** An attacker returning zero findings must state what it attacked and
why the artifact survived each attempt. ALL attackers returning zero findings is a red flag —
treat it as a failure to attack, not as cleanliness. **Who fires it:** the coverage auditor fires
this flag; a dedicated `final_approver` only *checks that the auditor fired it* — a dedicated
approver does no other work. When no coverage-auditor group is declared and `final_approver` is
`parent`, `parent` fires the flag itself — `parent` is the strategist session, not a dedicated
approver bound by "no other work".

## 4. Write the report — `review.md`

One document, whatever the `output_mode`. Under `inline` it is rendered in chat verbatim in this
shape; under `persisted` it is written to `<working_folder>/review.md`. **The shape does not change
with the mode** — inline is a delivery channel, not a lighter deliverable.

```
# Review — <target corpus>

## Coverage            (the auditor's section; the audit trail that replaces the transcript)
| attacker | lens | findings raised | zero-findings defence (if any) |
- collapse note: did the robot_talks attackers converge prematurely? (P14)
- lens coverage: was every target attacked from every declared lens?

## <artifact 1>
| # | file | evidence (quoted from the artifact) | severity | proposed fix |
**Verdict:** KEEP | FIX

## <artifact 2>
…

## Change requests     (all surviving findings, ordered by severity)
1. CRITICAL — …
2. MAJOR — …
```

The requirement is the DOCUMENT, not who writes it — the strategist may write it itself or
delegate to the `writer`. **Never write `attacks.md` or `findings.md` from a review** (§14).

## 5. Close

The dispatch is `resolved` when the `final_approver` accepts the change-request list. For review,
acceptance includes checking that every surviving finding quotes its artifact and every refuted
finding was dropped. **FIX verdicts are deliverables, not non-resolution** — a review that ships
FIX verdicts and is accepted is resolved.

Report `exit_reason` + `agents_spawned` in chat (and in `review.md` when persisted), then append
the close row.

## Standing rules

1. **Claim ≤ proof** — a refuted finding is dropped, never softened. Demote, never inflate.
2. **Attack the whole corpus, differ by lens** — attackers spread lenses, not target partitions.
3. **Read-only over the targets** — attackers never modify the artifacts under attack.
4. **No self-verification** — an attacker's verifier is never the attacker itself.
5. **One document, two channels** — `review.md` is the only artifact; `inline` vs `persisted` is
   the human's call at the gate, and it changes where it lands, never what it contains.

## Names

Draw `agent_name` from `telemetry/agents/agent-pool.yaml` (ordered `role_fit`). Prefer the primary
`role_fit` entry and a `field` fit to the target corpus. Never reuse a name within one dispatch,
and never let an attacker verify its own attack.

## See also

- **Router** — the `domainspec-subagents-strategy` skill: triggers, the human gate, lifecycle,
  the anti-bias principle, `final_approver`, and the `exit_reason` vocabulary. Nothing here
  overrides it.
- **Record/sheet mechanics + field definitions** — the `register-dispatch` skill: the two appends,
  the appender, validation, and enums (including `output_mode`).
- **Discussion rules for a `robot_talks` group** — the `robot-talks` skill governs the intra-group
  confrontation, except that this dispatch keeps its single human gate at the entry confirm and
  adds no second gate.
- **Anti-bias gate** — the `check-tension` skill runs the pairwise-tension rubric on the sheet at
  the confirm gate.
