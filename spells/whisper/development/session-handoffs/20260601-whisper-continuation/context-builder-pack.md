# Context Builder Pack: Whisper Continuation

## Identity

- Pack ID: `20260601-whisper-continuation`
- Target lifecycle: `spells/whisper`
- Handoff type: `execution-continuation`
- Created: 2026-06-01
- Source session reference: current Codex thread, plus committed Whisper artifact history in Git.

## Obligations

| Obligation | Coverage | Selected Source | Why It Matters |
| --- | --- | --- | --- |
| Continue from committed Whisper state | covered | Git commit `503217a` and current `main` | Prevents replaying stale uncommitted assumptions. |
| Preserve the public draft and review split | covered | `DRAFT-SUBSTACK-002.public.html`; `DRAFT-SUBSTACK-002.review.html` | The public page is for readers; the review page is for agent-addressable comments. |
| Continue readability dynamics work | covered | `spells/whisper/development/refinement-runs/20260531T164421Z-readability-dynamics/RESULT.md` | Next work should implement the schema/validator/renderer path identified by refine. |
| Use task-session for bounded execution | covered | `spells/whisper/development/refinement-runs/20260531T164421Z-readability-dynamics/stages/09-invoke-plan.md` | The next session should run one SWU, not redesign Whisper from scratch. |
| Avoid unrelated dirty worktree scope | covered | `git status -sb` current state | Current checkout has unrelated Inventory/Ontology/Craft/runtime changes; Whisper paths are clean. |

Strict coverage: `pass`

## Selected Context

### Current Git State

- Current branch: `main`
- Current HEAD: `75b2230 Ignore local runtime and cache artifacts`
- Remote: `origin/main` is aligned with `main` at handoff creation time.
- Whisper lifecycle commit: `503217a Commit Whisper lifecycle and review artifacts`
- Public draft commit: `1e3b8bf Add public Whisper draft HTML`
- `503217a` is an ancestor of current `HEAD`.
- `spells/whisper` and `registry/SPELLS.md` are clean at handoff creation time.

### Committed Whisper Artifacts

- Spell contract: `spells/whisper/README.md`
- Design baseline: `spells/whisper/development/DESIGN.md`
- Presentation: `spells/whisper/development/WHISPER-PRESENTATION.html`
- Machine-readable substrate: `spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/text-intent-substrate.yaml`
- Draft markdown: `spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/DRAFT-SUBSTACK-002.md`
- Public reading HTML: `spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/DRAFT-SUBSTACK-002.public.html`
- Comment/review HTML: `spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/DRAFT-SUBSTACK-002.review.html`
- Review template: `spells/whisper/templates/draft-review-base.html`
- Review generator: `spells/whisper/tools/build-whisper-review-html.py`
- Review payload extractor: `spells/whisper/tools/extract-whisper-review-payload.sh`
- Draft validator: `spells/whisper/tools/validate-whisper-draft.py`
- Readability dynamics refine run: `spells/whisper/development/refinement-runs/20260531T164421Z-readability-dynamics/`

### Key Decisions To Preserve

- First transport remains `substack_research_post`.
- Next transport pressure remains `fundraising_copy`, but fundraising is not the next execution task.
- Whisper uses `SCU`/Smallest Coherent Unit language, not `SRU`.
- Pareto tiering is `two_tier`.
- Part-level mini-tournaments are triggered only for delegated, revised, or validation-failed parts.
- Harari/Sapiens is a bridge after the reader-grounded opening, not the opening move.
- Review HTML exists to preserve stable `block_id`, `part_id`, selected text, requested change mode, and Playwright-extractable agent payload.
- Public HTML exists for sharing and should remain separate from the commentable review surface.
- Readability dynamics should be schema-first, validator-backed, and renderer-aware, not CSS-only.

### Validation Evidence

Recent validation from the source session:

- `python3 -m py_compile spells/whisper/tools/build-whisper-review-html.py spells/whisper/tools/validate-whisper-draft.py`: pass.
- `python3 spells/whisper/tools/validate-whisper-draft.py --schema spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/text-intent-substrate.yaml --draft spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/DRAFT-SUBSTACK-002.md`: pass.
- `python3 formulae/dispatch-spec/scripts/validate-dispatch.py spells/whisper/development/refinement-runs/20260531T164421Z-readability-dynamics/REFINE-DISPATCH.json --json`: pass.
- `jq empty` over Whisper JSON artifacts: pass.
- Public HTML was checked in browser via localhost Playwright at desktop and mobile sizes before commit.

## Excluded Context

| Candidate | Reason Excluded |
| --- | --- |
| `arcana/inventory/**` current dirty changes | Not Whisper obligation-relevant. |
| `arcana/ontology-vault/**` current dirty changes | Separate lifecycle thread. |
| `development/craft/**` current dirty changes | Separate Craft session. |
| `tools/**` current dirty changes | Runtime/tooling work, not needed for the next Whisper SWU unless a command blocker appears. |
| `writing/substack/introducing-arcanum.*` | General Arcanum article wording changes, not the Whisper Substack draft artifact. |
| `registry/SIGILS.md` | Non-Whisper registry changes for other sigils. |

## Recommended Next SWU

Run `task-session` for:

`SWU-WHISPER-READABILITY-001`

Objective:

Add a non-breaking `readability_dynamics` schema section and validator checks, without rewriting the draft first.

Primary sources:

- `spells/whisper/development/refinement-runs/20260531T164421Z-readability-dynamics/RESULT.md`
- `spells/whisper/development/refinement-runs/20260531T164421Z-readability-dynamics/stages/06-invoke-design.md`
- `spells/whisper/development/refinement-runs/20260531T164421Z-readability-dynamics/stages/09-invoke-plan.md`
- `spells/whisper/development/refinement-runs/20260526T204134Z-language-ai-substack/text-intent-substrate.yaml`
- `spells/whisper/tools/validate-whisper-draft.py`

Acceptance:

- YAML parses.
- Existing draft validation still passes.
- New readability checks flag paragraph-wall risks without blocking the current draft unless an explicit hard gate is violated.
- No public/review HTML regeneration is required until the renderer SWU.

