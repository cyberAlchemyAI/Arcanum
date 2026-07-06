# UI Prototyping Studio

Accountable UI exploration: generate 1–3 bounded variants → intentionally select a baseline → annotate with canonical comments → synthesize a deterministic mutation draft → **explicit human approval** → apply → append-only revision manifest → hand off. Governance is a feature, not friction; **ergonomics is the first principle**.

This is a **standalone project** (extracted from the now-deprecated `domainspec` monorepo). It is deliberately scoped to what is real and buildable today.

## What's here

| Path | What it is |
|------|-----------|
| [SPEC.md](SPEC.md) | **Lean spec** — the L0→L2 survival/trust floor (this release). The buildable contract. |
| [CRAFT.md](CRAFT.md) · [.craft/](.craft/) | Craft ledger — live project state (contexts, decisions, blockers, gaps). Source of truth = `.craft/ledger.yml`. |
| [ide-ergonomics-experience-prototype.html](ide-ergonomics-experience-prototype.html) | Interactive click-through prototype for the IDE Ergonomics presentation: highlighted chat phrase → route card → candidate/side-node/handoff/delegation previews → durable workbench outputs. |
| [development/deep-spec-dispatch/](development/deep-spec-dispatch/) | The deep-spec exploration that produced the design + plan + readiness verdict ([RESULT.md](development/deep-spec-dispatch/RESULT.md), [DEEP-SPEC-PROPOSAL.md](development/deep-spec-dispatch/DEEP-SPEC-PROPOSAL.md), [ONE-SHOT-IMPLEMENTATION-PLAN.md](development/deep-spec-dispatch/ONE-SHOT-IMPLEMENTATION-PLAN.md)). |
| [development/standalone-extraction/](development/standalone-extraction/) | The plan to bring the code over and make this project runnable. |
| `provenance/` | Archive, not spine: the 19-doc full-vision DomainSpec spec (`legacy-domainspec-spec/`) and a vendored design-skills reference tree (`open-design-reference/`). Mine for detail; do not treat as current. |

## Scope (this release): L0→L2

Per the deep-spec readiness verdict, only **L0** exists in code (the 10-state session machine + governance enforcement). This release hardens that working floor:

- **L0** — the working exploration loop + governance invariants (auto-apply forbidden, approval-before-apply, append-only manifest, variantCount 1–3).
- **L1** — accessibility (keyboard, ARIA, focus, labels).
- **L2** — layout integrity (no overflow/clip/overlap, target size, responsive).

**Deferred** (design only, see `development/deep-spec-dispatch/`): L3 interaction-flow gates · L4 identity/DNA + conformance-delta · L5 fitness scoring · L6 human-evidence/trust. Plus open questions OQ-1..4.

## Status

- Spec spine + Craft ledger: **in place**.
- **Backend lifted and runnable** — the full mutation loop works through the `studio` CLI: generate/register variants (real HTML), select a baseline, comment, synthesize, **approve → apply → accept** (two-gate, with an honest per-component diff), record, hand off. Backend is node + fastify + TypeScript (run via `tsx`).
- **Shipped:** the browser **preview + click-to-annotate** surface (`studio preview <sid>`), AUTO `cycle`/`watch` verbs, in-preview **Accept/Revert** controls, and a Playwright e2e suite (`pnpm test:e2e`). Export stays the one terminal, `--confirm` edge (no button). (A full `web/` SPA scaffold is still deferred — the preview is a no-build loopback page, not an SPA.)

## Running

> ⚠️ **Before you test, read [TESTER-BRIEF.md](TESTER-BRIEF.md)** (a one-page safety/consent note) and follow [TEST-PROTOCOL.md](TEST-PROTOCOL.md) for a guided run.

Requires Node ≥ 20 and pnpm. The CLI lives in `backend/`:

```bash
cd backend
pnpm install
pnpm test            # node:test suite (unit + slice)

# Drive the studio. STUDIO_DATA is the data FILE inside a fresh per-run DIR, so the session
# state AND the artifacts (under <dir>/artifacts) are fully isolated and reset together.
# STUDIO_DOCS_ROOT points at a docs root for the handoff export.
export STUDIO_DATA=/tmp/ups-run-1/studio.json      # fresh DIR per run, not a bare /tmp file
export STUDIO_DOCS_ROOT="$(pwd)/.."

pnpm studio session open                         # -> { sessionId: ups-session-0001, ... }
pnpm studio prompt submit ups-session-0001 "a sign-up card"
# register real variant HTML (each <label>.html must stamp data-od-id on annotatable components):
pnpm studio variants register ups-session-0001 --from ./my-variants     # dir of a.html/b.html/c.html
#   (or)  pnpm studio variants register ups-session-0001 --label A --file a.html --label B --file b.html
pnpm studio baseline select ups-session-0001 B
pnpm studio baseline commit ups-session-0001
pnpm studio comment add ups-session-0001 --selector "[data-od-id=cta.primary]" --label "Primary button" --od-id cta.primary --intent reword --note "say Continue"
pnpm studio synthesize ups-session-0001          # -> { batch: { batchId: ups-batch-00001, ... } }
pnpm studio batch approve ups-session-0001 ups-batch-00001
# two-gate apply: stage an agent-proposed candidate (head does NOT advance), then accept:
pnpm studio apply ups-session-0001 ups-batch-00001 --candidate-from ./candidate.html   # -> openPath to view the staged diff
pnpm studio accept ups-session-0001              # -> head advances by one; openPath to the committed HTML
pnpm studio revisions ups-session-0001
pnpm studio handoff export ups-session-0001
```

**Seeing the result in a browser:** run `studio preview <sid>` and open the printed loopback URL in VSCode's Simple Browser — it renders the variants (sandboxed), the staged before/after + honest diff, a click-to-annotate panel, and in-preview **Accept/Revert** buttons. (`register`/`apply`/`accept` also print an `openPath` to the rendered `.html` on disk if you prefer `xdg-open`.) Variant HTML should be self-contained (inline styles) to render faithfully.

**Reset:** point `STUDIO_DATA` at a file inside a fresh **directory** per run (e.g. `/tmp/ups-run-2/studio.json`) — both the session state and the artifacts live under that directory, so a new dir is a clean slate. To reset in place: `rm -rf "$(dirname "$STUDIO_DATA")"`.
