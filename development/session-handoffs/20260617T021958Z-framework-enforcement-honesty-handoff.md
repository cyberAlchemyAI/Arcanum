# Session Handoff: Framework Improvement — Enforcement-Honesty + Authorship-vs-Execution

## Identity

- Source session reference: a private consuming-project session that produced and red-team-reviewed an
  operating-contract draft, then ran a reverse-direction reflection ("do the draft skills expose gaps in
  the Arcanum framework?"). Evidence retained in the **private parent** (not copied here — open/private
  boundary): the review findings + the framework gap-analysis return.
- Destination label: `framework-enforcement-honesty`
- Handoff type: `new-lifecycle-idea` (framework improvement from usage evidence)
- Target project or lifecycle: `arcanum/framework/` docs + `arcana/sigil-development` reflection
- Created for: start a bounded session that lands the two high-value framework improvements (and one
  minor rider) and routes the two deferred candidates correctly — without leaking private content into
  the public submodule.

## New Session Prompt

```text
Continue the framework improvement from arcanum/development/session-handoffs/20260617T021958Z-framework-enforcement-honesty-handoff.md.

Goal: land two evidence-backed authoring-discipline gaps the framework currently does NOT cover, plus one
minor pairing check. All work is PROPOSAL-ONLY until the owner confirms (arcanum is the public submodule;
submodule-first/parent-last if committed). Do NOT embed any private consuming-project specifics — the
patterns are general; the evidence stays referenced, not copied.

Apply (direct framework-doc edits, owner-confirmed):
- #1 ENFORCEMENT-HONESTY -> arcanum/framework/ANTI-PATTERNS.md (new bullet under "Minimum Contents").
- #2 AUTHORSHIP-vs-EXECUTION -> arcanum/framework/QUALITY-BAR.md (Arcana-tier shape + one example criterion).
- #4 QB<->AP PAIRING CHECK -> arcanum/framework/SIGIL-DEVELOPMENT-WORKFLOW.md checklist (one paired item)
  + keep both placeholders in framework/templates/sigil-template.md.

Route, do NOT inline:
- #5 (generalized evidence-class ladder) and #6 (new artifact_type "operating-contract") -> sigil-development --reflect.
  Both are below the evidence threshold (single instance; #6 touches a candidate constitution with no validator).
- #3 (teach-only-runnable) is a DUPLICATE of existing ANTI-PATTERNS coverage -> no-op.

First read this handoff, then read the three target framework files before editing. Make one scoped
commit per file only after owner sign-off.
```

## Route Rationale

- Recommended next route: `sigil-development --reflect` (it owns "improve Quality Bar, Anti-Patterns,
  templates, output contracts after evidence shows gaps"). #1/#2/#4 are self-contained framework-doc edits
  that reflect can author directly; #5/#6 need reflect's evidence-threshold judgment.
- Lifecycle owner: `sigil-development` (framework authoring discipline). `invoke` produced this handoff only.
- Why not act now: arcanum is the **public submodule**; per SUBMODULE-DISCIPLINE these are proposal-only
  until the owner confirms, and a single instance does not justify the two deferred structural changes.

## The candidates (evidence-bound; strict already-covered vs real-gap)

| # | Candidate | Verdict | Target | Value |
|---|---|---|---|---|
| 1 | **Enforcement-honesty** — don't assert a runtime guarantee/gate the system doesn't enforce; if a control is documentary-only, say so and name what *does* enforce it | **REAL GAP** — framework has `claim ≤ proof` (epistemic) but no `claim-of-enforcement ≤ actual-enforcement`; CYBERALCHEMY "Human Gate" asserts gates without requiring disclosure of documentary-only controls | `ANTI-PATTERNS.md` "Minimum Contents" | **highest** |
| 2 | **Authorship vs execution** — a human-gated contract must forbid the agent *authoring* the decision (command string / recommendation-to-yes), not only *executing* the verb | **REAL GAP** — framework "authority" = lifecycle-routing only; "prepare options and trade-offs" arguably licenses the relay | `QUALITY-BAR.md` Arcana shape + example | **high** |
| 4 | **QB↔AP pairing** — shipping Anti-Patterns without a Quality Bar (or vice-versa) = incomplete contract | REAL GAP (small) — pairing is documented as conceptual but never a hard authoring check | `SIGIL-DEVELOPMENT-WORKFLOW.md` checklist | medium |
| 3 | Two-layer scoping / teach-only-runnable | **ALREADY COVERED** (ANTI-PATTERNS "looks complete but wrong" / boundary-expansion) — duplicate | — | n/a |
| 5 | Generalized evidence-class ladder (machine_checkable / heuristic_flag / artifact_review / empirical_study / not_automatable) | real but **bloat risk** — QUALITY-BAR is deliberately terse | `sigil-development --reflect` | defer (≥2 instances) |
| 6 | New `artifact_type: operating-contract` (project-local agent-as-engine contract, distinct from tier `skill-contract`) | real but **premature** — candidate constitution, no validator, single instance | `sigil-development --reflect` | defer |

## Proposed change text (for the next session to apply, owner-confirmed)

- **#1 → ANTI-PATTERNS.md** (new bullet): *"Avoid asserting a runtime guarantee, gate, or refusal the
  executing system does not enforce; if a control is documentary-only, the artifact must say so and name
  what actually enforces it."*
- **#2 → QUALITY-BAR.md** (Arcana shape + example): *"For a contract with human gates: a successful
  execution must forbid the agent from authoring the gate's decision content (command string,
  recommendation-to-yes), not only from executing the verb."*
- **#4 → SIGIL-DEVELOPMENT-WORKFLOW.md** checklist (one paired item): *"Quality Bar AND Anti-Patterns
  both present — a contract with one side only is incomplete."*

## Context Builder Selection

| Obligation | Coverage | Selected Source | Why It Matters |
| --- | --- | --- | --- |
| name the real gaps vs duplicates | covered | the session's framework gap-analysis (private parent) | distinguishes #1/#2/#4 (real) from #3 (duplicate) and #5/#6 (defer) |
| target the right framework files | covered | `ANTI-PATTERNS.md`, `QUALITY-BAR.md`, `SIGIL-DEVELOPMENT-WORKFLOW.md`, `framework/templates/sigil-template.md` (read this session) | each change has an exact home |
| preserve open/private boundary | covered | SUBMODULE-DISCIPLINE (private parent) | evidence originated in a private project; only the general patterns cross into public arcanum |
| route deferred items | covered | `arcana/sigil-development/SKILL.md` reflection mode | #5/#6 need reflect's evidence-threshold judgment, not a unilateral edit |

Strict coverage: `pass`

## Boundary & discipline notes

- **Open/private boundary:** the triggering evidence is private (a consuming-project operating-contract
  review). This handoff and the proposed changes contain **only general authoring-discipline patterns** —
  no private project names, code, or specifics. Keep it that way.
- **Submodule discipline:** `arcanum/` is the public submodule. This handoff is written but **uncommitted**;
  any approved framework edit is **proposal-only** until owner sign-off, then submodule-first/parent-last,
  `make bump-check` before pushing the parent.
- **Anti-overclaim (self-applied):** every "REAL GAP" was checked against the actual framework file
  contents this session; #3 was demoted to duplicate rather than proposed. The verdicts are `claim ≤ proof`.

## Recommended next routes

1. `sigil-development --reflect` for the whole set (authors #1/#2/#4, judges #5/#6 against threshold).
2. Or, if the owner wants only the two high-value wins: direct edits to `ANTI-PATTERNS.md` (#1) and
   `QUALITY-BAR.md` (#2), one scoped commit each, after sign-off.
