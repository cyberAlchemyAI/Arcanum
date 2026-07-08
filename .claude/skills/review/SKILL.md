---
name: review
description: Red-team dispatch over EXISTING artifacts (skills, constitutions, code, docs) — attack what exists and hunt flaws to improve it. Routed here from domainspec-subagents-strategy as the LIVE type skill for `dispatch_type: review`. Defines review-type judgment only — attack lenses, severity taxonomy, verification discipline, and the change-request findings shape. Use research (not review) when the question is whether a NEW claim/candidate survives; use review when the target already exists and the deliverable is verified change requests.
---

# review — operating guide for `dispatch_type: review`

**What this is.** You are running a review dispatch: a red team. The targets already exist —
skills, constitutions, code, docs — and the dispatch attacks them to surface flaws worth fixing.

**What you produce.** **Verified change requests** — not verdicts on new candidates (that is
`research`), and not the fixes themselves. Applying a change request is a follow-up act outside
the dispatch, or a re-run after fixes within the loop ceiling — the owner's call. The deliverable
is `attacks.md` + `findings.md` in the `working_folder`.

**The procedure.** Shape it → Run it → Gate it → Write the outputs → Close.

## 1. Shape it

Pick the attackers, their lenses, and the shape that carries their findings to a record.

**Roles** — review runs the four agent roles with red-team semantics; each guards one failure
mode, and no agent guards two:

| `role` | red-team function | guards against | model |
|---|---|---|---|
| `explorer` | **attacker** — attacks the full target corpus from ONE declared attack lens | blind spots — one lens sees what another cannot | heavier for subtle lenses |
| `skeptic` | **verifier** — refutes findings against the literal artifact; runs the actual check | false positives — plausible-but-wrong findings surviving | heavy |
| `writer` | **synthesizer** — dedupes, severity-ranks, writes the cited change requests; conventionally a single writer | "great attack, no record" | heavy |
| `auditor` | **coverage auditor** — placed downstream of the verifiers; checks every target was attacked from every declared lens and no refuted finding survived | "passed because nothing was attacked" | light |

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
  attacker group runs `robot_talks`, the synthesizer downstream of it MUST receive each attacker's
  **initial AND final** positions (both present in `working_folder`), so premature convergence /
  collapse in the attack discussion stays detectable.
- **Verifiers** — `skeptic`s in a zig-zag exchange with the synthesizer.
- The **feedback** back-edge exists only when there is a verifier/auditor group AND material may be
  missing — never by default (shown dashed).
- An optional **coverage-auditor** group (its single agent's role is `auditor`) is placed by its
  incoming edge, downstream of the verifiers, and is the natural dedicated `final_approver`.

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

**Finding discipline.** Every finding carries the file, quoted evidence, severity, and a one-line
proposed fix. A finding the verifier refutes is **dropped, not softened** — claim ≤ proof, demote
never inflate.

**Zero-findings red flag.** An attacker returning zero findings must state what it attacked and
why the artifact survived each attempt. ALL attackers returning zero findings is a red flag —
treat it as a failure to attack, not as cleanliness. **Who fires it:** the coverage auditor fires
this flag; a dedicated `final_approver` only *checks that the auditor fired it* — a dedicated
approver does no other work. When no coverage-auditor group is declared and `final_approver` is
`parent`, `parent` fires the flag itself — `parent` is the strategist session, not a dedicated
approver bound by "no other work".

## 4. Write the outputs

Results land in the `working_folder` — a repo-relative docs path, confirmed at the gate. Which
files depends on how many agents ran:

| agents | files |
|---|---|
| **2 or more** | `attacks.md` + `findings.md` |
| **1** | `findings.md` only |

- **`attacks.md`** — the collected attacker and verifier returns, verbatim.
- **`findings.md`** — the cited change requests. Every surviving finding cites the attack return it
  came from and quotes the artifact. Shape: per-artifact section → table of surviving findings
  (`| # | file | evidence | severity | proposed fix |`) → per-artifact verdict (KEEP / FIX) → a
  closing change-request list ordered by severity.

The requirement is the FILES, not who writes them — the strategist may write them itself or
delegate to the `writer`.

## 5. Close

The dispatch is `resolved` when the `final_approver` accepts the change-request list. For review,
acceptance includes checking that every surviving finding is cited and every refuted finding was
dropped. **FIX verdicts are deliverables, not non-resolution** — a review that ships FIX verdicts
and is accepted is resolved.

## Standing rules

1. **Claim ≤ proof** — a refuted finding is dropped, never softened. Demote, never inflate.
2. **Attack the whole corpus, differ by lens** — attackers spread lenses, not target partitions.
3. **Read-only over the targets** — attackers never modify the artifacts under attack.
4. **No self-verification** — an attacker's verifier is never the attacker itself.

## Names

Draw `agent_name` from `telemetry/agents/agent-pool.yaml` (ordered `role_fit`). Prefer the primary
`role_fit` entry and a `field` fit to the target corpus. Never reuse a name within one dispatch,
and never let an attacker verify its own attack.

## See also

- **Router** — the `domainspec-subagents-strategy` skill: triggers, the human gate, lifecycle,
  the anti-bias principle, `final_approver`, and the `exit_reason` vocabulary. Nothing here
  overrides it.
- **Record/sheet mechanics + field definitions** — the `register-dispatch` skill: the two appends,
  the appender, validation, and enums.
- **Discussion rules for a `robot_talks` group** — the `robot-talks` skill governs the intra-group
  confrontation, except that this dispatch keeps its single human gate at the entry confirm and
  adds no second gate.
- **Anti-bias gate** — the `check-tension` skill runs the pairwise-tension rubric on the sheet at
  the confirm gate.
