# Craft Workspace View

> Human view of [`.craft/ledger.yml`](.craft/ledger.yml). The ledger is the source of truth;
> this file is a linked rendering only.

- **Governed contexts:** Arcanum Manual; Craft ledger-integrity research; Arcanum composition analysis;
  Lens and resolution routing; Subagent strategy runtime hardening
- **Root contexts:** `CTX-ARCANUM-MANUAL-ROOT`, `CTX-CRAFT-LEDGER-INTEGRITY`,
  `CTX-ARCANUM-COMPOSITION-ANALYSIS`, `CTX-LENS-RESOLUTION-ROUTING`,
  `CTX-SUBAGENT-STRATEGY-RUNTIME-HARDENING`
- **Stage / gate:** manual `validate / pass`; ledger-integrity research `plan / flag`;
  composition analysis `execute / flag`; routing `review-audit / flag`; subagent strategy
  hardening `validate / flag`
- **Source of truth:** [`.craft/ledger.yml`](.craft/ledger.yml)

## Quick links

- **Next moves:** review [ARCANUM-MANUAL.md](development/user-guide/ARCANUM-MANUAL.md); for ledger
  integrity, explicitly confirm and execute the prepared governed research dispatch, then produce
  `research.md` and `findings.md` before proposing canonical Craft changes; for composition, expand
  the analysis from the accepted per-RQ findings while preserving the four unresolved boundaries,
  then run a separate adversarial review; for routing, decide whether to repair the four
  platform-neutral MAJOR findings while preserving the explicit Windows-repair deferral; for
  subagent strategy hardening, run the Windows and Ubuntu matrix and close or preserve the Linux
  evidence gap from its result.
- **Blocking decisions:** none
- **Active blockers:** none
- **Active gaps:** `GAP-CRAFT-LEDGER-INTEGRITY-RESEARCH-001` (research prepared but not executed);
  `GAP-ARCANUM-COMPOSITION-RESIDUE-001` (four research boundaries remain unresolved);
  `GAP-ROUTING-PLATFORM-NEUTRAL-REVIEW-001` (four verified platform-neutral findings remain open);
  `GAP-SUBAGENT-STRATEGY-LINUX-CI-001` (Ubuntu matrix result has not yet been observed)
- **Deliverables:** [**ARCANUM-MANUAL.md**](development/user-guide/ARCANUM-MANUAL.md) (pass) ·
  [validation evidence](development/user-guide/ARCANUM-MANUAL.validation.md) ·
  [surface x-ray HTML](development/user-guide/arcanum-surface-xray.html) ·
  [distill notes/corpus](.craft/artifacts/arcanum-manual-distill-notes.md) ·
  [manual research dispatch](.craft/artifacts/20260616-arcanum-manual-research-strategy.dispatch.json) ·
  [ledger-integrity dispatch](research/craft-ledger-integrity/craft-ledger-integrity-research.dispatch.json) ·
  [composition analysis](docs/analysis/arcanum-composition-analysis/analysis.md) ·
  [composition research baseline](docs/analysis/arcanum-composition-analysis/research/arcanum-composition/research-initial-definitions.md) ·
  [composition baseline review](docs/analysis/arcanum-composition-analysis/review.md) ·
  [composition research dispatch](docs/analysis/arcanum-composition-analysis/research/arcanum-composition/arcanum-composition-research.dispatch.json) ·
  [research returns](docs/analysis/arcanum-composition-analysis/research/arcanum-composition/research.md) ·
  [accepted findings](docs/analysis/arcanum-composition-analysis/research/arcanum-composition/findings.md) ·
  [dispatch lifecycle ledger](docs/analysis/arcanum-composition-analysis/research/arcanum-composition/dispatch-ledger.jsonl)

- **Routing evidence:** [post-promotion review](transmutations/resolution-router/development/validation/post-promotion-review/review.md)
  · [closing session](sessions/2026-08-25-2130-lens-resolution-routing.md)

- **Subagent strategy evidence:** [capability contract](arcana/subagent-strategy/SKILL.md),
  [native verifier](runtime/orchestrate/scripts/native_dispatch_coordinator.py),
  [cross-platform workflow](.github/workflows/subagent-strategy-runtime.yml), and
  [closing session](sessions/2026-08-27-1312-subagent-strategy-runtime-hardening.md)

## Purpose

Build a leverage-oriented Arcanum manual that explains **what Arcanum is**, **what its processes
are**, and **how each kind of user can use it**, by researching the full Arcanum knowledge surface
and authoring through `whisper`. `development/user-guide/` is the explanatory pattern base and the
final home for the manual.

## The strategy (validated dispatch route)

The research strategy is encoded as a single validated dispatch route,
[ART-MANUAL-RESEARCH-DISPATCH](.craft/artifacts/20260616-arcanum-manual-research-strategy.dispatch.json)
(`dispatch-spec` verdict: **pass**). It plans, but does not execute:

| Step | Capability | Pattern | Produces |
| --- | --- | --- | --- |
| s01 X-ray the Arcanum surface | `x-ray` | xray | layered map + `arcanum-surface-xray.html` |
| s02 Inventory the knowledge corpus | `inventory` | sequential | source-backed knowledge ledger |
| s03 Distill per audience | `distill` | distill | concept units grouped by reader leverage |
| s04 Whisper the manual | `whisper` | synthesis | `ARCANUM-MANUAL.md` |
| s05 Validate against source | `necronomicon` | validation | per-claim source-resolution evidence |

**Executed 2026-06-16** with operator-approved subagent fan-out: five read-only explorer lanes
(framework/method, sigils, spells, observability/lifecycle, user-guide pattern + audiences) joined
by parent synthesis → distill → whisper authoring → source validation (**pass**). Trace:
`dispatch-authored → subagent-strategy-approved → arcanum-surface-xrayed → knowledge-corpus-inventoried
→ concept-units-distilled → manual-whispered → arcanum-manual-validated`.

## Contexts

### <a id="context-ctx-arcanum-manual-root"></a>CTX-ARCANUM-MANUAL-ROOT — Arcanum Manual

- Stage / gate: validate / pass
- Next move: operator review of [ARCANUM-MANUAL.md](development/user-guide/ARCANUM-MANUAL.md),
  with an optional HTML/PDF companion, followed by the submodule commit and parent gitlink bump.
- Owns: [ledger](.craft/ledger.yml), [this view](CRAFT.md),
  [research dispatch](.craft/artifacts/20260616-arcanum-manual-research-strategy.dispatch.json),
  [user-guide base](development/user-guide/), [final manual](development/user-guide/ARCANUM-MANUAL.md)

### <a id="context-ctx-craft-ledger-integrity"></a>CTX-CRAFT-LEDGER-INTEGRITY — Craft ledger-integrity research

- Stage / gate: plan / **flag**
- Next move: obtain explicit operator confirmation; execute the prepared internal/external governed
  dispatch; produce `research.md` and `findings.md`; only then evaluate contract, validator, runtime,
  migration, or operator-discipline changes.
- Owns: [prepared dispatch](research/craft-ledger-integrity/craft-ledger-integrity-research.dispatch.json)
  and [closing session](sessions/2026-08-25-1645-craft-ledger-integrity-review-and-dispatch.md).
- Evidence boundary: route validation, material readiness, and two tension checks passed, but no
  research agents were launched and no dispatch event or research findings exist.

### <a id="context-ctx-arcanum-composition-analysis"></a>CTX-ARCANUM-COMPOSITION-ANALYSIS — Arcanum composition analysis

- Stage / gate: execute / **flag**
- Next move: expand [analysis.md](docs/analysis/arcanum-composition-analysis/analysis.md) from the
  accepted per-RQ findings while preserving the four unresolved boundaries, then run a separate
  adversarial review of the completed reader-facing analysis.
- Owns: [analysis](docs/analysis/arcanum-composition-analysis/analysis.md),
  [research initial definitions](docs/analysis/arcanum-composition-analysis/research/arcanum-composition/research-initial-definitions.md),
  [review](docs/analysis/arcanum-composition-analysis/review.md),
  [executed dispatch](docs/analysis/arcanum-composition-analysis/research/arcanum-composition/arcanum-composition-research.dispatch.json),
  [research returns](docs/analysis/arcanum-composition-analysis/research/arcanum-composition/research.md),
  [accepted findings](docs/analysis/arcanum-composition-analysis/research/arcanum-composition/findings.md),
  [dispatch lifecycle ledger](docs/analysis/arcanum-composition-analysis/research/arcanum-composition/dispatch-ledger.jsonl), and
  [research closeout](sessions/2026-08-25-2056-arcanum-composition-research.md).
- Evidence boundary: the confirmed dispatch is closed; findings contain one evidence-bounded row
  for each RQ, with seven answered and four unresolved. Two skeptics passed the final revision and
  the independent auditor returned `ACCEPT` after resolving all 86 cited locators. The introduction
  remains preserved and the reader-facing analysis has not yet been expanded from the findings.

### <a id="context-ctx-lens-resolution-routing"></a>CTX-LENS-RESOLUTION-ROUTING — Lens and resolution routing

- Stage / gate: review-audit / **flag**
- Next move: obtain an operator decision on whether to repair the four platform-neutral `MAJOR`
  findings; preserve the installed trio and do not alter Windows-specific failure paths meanwhile.
- Owns: [post-promotion review](transmutations/resolution-router/development/validation/post-promotion-review/review.md)
  and [closing session](sessions/2026-08-25-2130-lens-resolution-routing.md).
- Evidence boundary: the architecture, installation, dependency closure, semantic validators, and
  focused runtime tests passed. The review still returned `FIX` because promotion/evidence and
  authoring-governance findings remain. Windows-specific repairs were explicitly deferred.

### <a id="context-ctx-subagent-strategy-runtime-hardening"></a>CTX-SUBAGENT-STRATEGY-RUNTIME-HARDENING â€” Subagent strategy runtime hardening

- Stage / gate: validate / **flag**
- Next move: run the configured Windows and Ubuntu workflow matrix; on dual pass, mark this context
  `pass` and resolve `GAP-SUBAGENT-STRATEGY-LINUX-CI-001`, otherwise preserve the failure and open a
  bounded repair.
- Owns: [capability contract](arcana/subagent-strategy/SKILL.md),
  [native projection and topology verifier](runtime/orchestrate/scripts/native_dispatch_coordinator.py),
  [cross-platform workflow](.github/workflows/subagent-strategy-runtime.yml), and
  [closing session](sessions/2026-08-27-1312-subagent-strategy-runtime-hardening.md).
- Evidence boundary: 102 registrar tests, eight-process concurrency, runtime and Dispatch Spec
  suites, generation checks, guards, syntax checks, and junction confinement passed locally on
  Windows; Linux is configured but not yet witnessed.

## Decisions

- **<a id="decision-dec-routing-windows-portability-001"></a>DEC-ROUTING-WINDOWS-PORTABILITY-001**
  (**closed / deferral**): do not repair Windows-specific
  fixture, line-ending, WSL/bash, or PowerShell paths in this session. This does not convert those
  paths to pass; it records their accepted residue and prevents the closeout from implying they
  were fixed.

## Definitions (candidate, local)

- **<a id="definition-def-arcanum-manual-001"></a>Arcanum manual** (`DEF-ARCANUM-MANUAL-001`,
  candidate): a leverage-oriented explanatory artifact that lets a reader understand what Arcanum
  is, its processes, and how each kind of user can use it, with every claim backed by an Arcanum
  source path. It is documentation, not a canonical surface.

## Gaps

- **<a id="gap-gap-arcanum-composition-research-001"></a>GAP-ARCANUM-COMPOSITION-RESEARCH-001**
  (**resolved**): the governed dispatch was confirmed, executed, closed, and accepted. Evidence:
  [findings](docs/analysis/arcanum-composition-analysis/research/arcanum-composition/findings.md) and
  [dispatch lifecycle ledger](docs/analysis/arcanum-composition-analysis/research/arcanum-composition/dispatch-ledger.jsonl).
- **<a id="gap-gap-arcanum-composition-residue-001"></a>GAP-ARCANUM-COMPOSITION-RESIDUE-001**
  (**active / flag**): generic Craft write-back coordination and adaptation, same-concern source
  precedence, and product-authorized improvement classification remain unresolved. These are
  explicit evidence boundaries rather than audit failures. Evidence:
  [per-RQ findings](docs/analysis/arcanum-composition-analysis/research/arcanum-composition/findings.md).
- **<a id="gap-gap-craft-ledger-integrity-research-001"></a>GAP-CRAFT-LEDGER-INTEGRITY-RESEARCH-001**
  (**active / flag**): the reviewed ledger-integrity investigation is ready to dispatch but remains
  unexecuted. Causes, prevalence, responsibility boundaries, and minimum integrity properties are
  still unresolved. Evidence: [session record](sessions/2026-08-25-1645-craft-ledger-integrity-review-and-dispatch.md);
  route: [prepared dispatch](research/craft-ledger-integrity/craft-ledger-integrity-research.dispatch.json).
- **<a id="gap-gap-audience-taxonomy-001"></a>GAP-AUDIENCE-TAXONOMY-001** (**resolved**): "How each
  user can leverage it" needed an explicit reader/persona taxonomy. Resolved in the distill step — a
  7-persona taxonomy grounded in README Start-Here, `FRIEND-INSTALL-TUTORIAL.md`, the user-guide
  thesis, and registry use-when conditions; inferred personas are labelled as such. See
  [distill notes](.craft/artifacts/arcanum-manual-distill-notes.md) and
  [manual Part 3](development/user-guide/ARCANUM-MANUAL.md).

- **<a id="gap-gap-routing-platform-neutral-review-001"></a>GAP-ROUTING-PLATFORM-NEUTRAL-REVIEW-001**
  (**active / flag**): current-byte forward evidence,
  durable raw forward artifacts, canonical lifecycle enforcement, and mandatory ownership/input
  authoring surfaces remain open. Evidence:
  [post-promotion review](transmutations/resolution-router/development/validation/post-promotion-review/review.md).

- **<a id="gap-gap-subagent-strategy-linux-ci-001"></a>GAP-SUBAGENT-STRATEGY-LINUX-CI-001**
  (**active / flag**): the hardened lifecycle passes its local Windows evidence, but the configured
  Ubuntu execution has not yet been observed. Evidence:
  [cross-platform workflow](.github/workflows/subagent-strategy-runtime.yml) and
  [closing session](sessions/2026-08-27-1312-subagent-strategy-runtime-hardening.md).

## Boundary check

Craft governed local state and residue; `dispatch-spec` validated route shape only. The manual route was
executed as documentation work: it created a manual, an x-ray surface, distill notes, and validation
evidence under `development/user-guide/` and `.craft/`. **No sigil, spell, definition, registry, or
other canonical Arcanum surface was created, mutated, or promoted.** Subagents were read-only and
gathered/distilled only; the parent owned synthesis and authoring. The ledger-integrity route is a
separate open context and has not been executed; recording it here does not authorize a canonical
Craft change or repair the `spells/goal` witness. The composition-analysis research was executed as
a repository-only, evidence-producing route and did not mutate capability owners. Its findings do
not establish a universal runtime integration or authorize canonical changes. The repository has
an artifact constitution, validators, flow-local ledgers, and `.craft/artifacts/`, but no packaged
central service that manages retention, indexing, compaction, or cleanup for every generated JSON.
The lens/resolution routing work added canonical capability packages and repository skill surfaces
under explicit user authorization. Its Windows-specific failures remain intentionally unrepaired;
the platform-neutral review findings remain visible as an active Craft gap rather than being
silently converted to pass.
The subagent-strategy work changed canonical capability and runtime surfaces under explicit user
authorization. It records local Windows validation as evidence, not as proof that the configured
Ubuntu job passed; that distinction remains visible in the Craft gate and active gap.
