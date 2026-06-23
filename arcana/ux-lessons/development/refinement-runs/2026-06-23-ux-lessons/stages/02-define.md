# Stage 2 — Invoke Define

- **Capability:** invoke · **Mode:** define · **Receipt kind:** native-stage · **Status:** pass

## Definition: what `ux-lessons` IS

`ux-lessons` is a capability that **captures the learning residue of a UI iteration session and promotes it into reusable, consumer-ready UX patterns.**

It owns three artifacts and nothing else:

1. **session-capture** — a pointer + signal summary of one iteration session (what changed, in what order, why, with screenshot evidence). Borrows the session-signal substrate; does not re-implement it.
2. **lesson** — one captured iteration unit, still contextual: trigger/failure-mode → change → before/after + evidence → generalizable principle + signal strength (anecdote | repeated | cross-session).
3. **ux-pattern** — the reusable distillate of one or more lessons: a pattern card (name, intent, problem, solution, when-to-use, anti-pattern, evidence link) **plus two consumer-intake blocks**.

## What it explicitly does NOT do
- Does not run Playwright validation (that is `ux-evidence-validator`).
- Does not mutate studio sessions or generate variants (that is `ui-prototyping-studio`).
- Does not re-implement session-signal capture, generic pattern storage mechanics, or residue ledgers — it composes the owners of those.

## Producer → consumer shape
`session → lesson → ux-pattern → { validator intake, studio intake }`

## Open definitional question (for Design)
Is the artifact contract rich enough to need its own owner (a **thin sigil**), or can it be a **schema-less spell** composing existing owners? Deferred to the route-menu in Design (s6).
