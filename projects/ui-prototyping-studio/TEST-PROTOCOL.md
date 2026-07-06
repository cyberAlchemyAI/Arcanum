# Test Protocol — governance loop (≈30 min)

**Scope (read this line):** this protocol tests **governance / integrity ergonomics** — can a human
supervise the agent and stay in control of every durable change. It does **NOT** test visual prototyping
ergonomics. A browser preview + click-to-annotate surface now ships (`studio preview <sid>`), but please
don't rate "how pretty/usable the UI looks"; rate "did I understand what was happening and stay in control."

**Before you start:** read [TESTER-BRIEF.md](TESTER-BRIEF.md) (the safety/consent note). Setup is in the
[README "Running"](README.md#running) section. Use a **fresh `STUDIO_DATA` path** for each full run-through.

## What we capture (your feedback)

For each task below, jot: ✅/❌ did it do what you expected · 😕 anything confusing · 🛑 anything that felt
unsafe or out of your control · a quote of the exact moment if it stuck. There's a form at the bottom.

## The tasks

You may drive the CLI yourself, or have Claude Code drive it while you supervise (the realistic mode).
Either way, **you** make every approve/apply/accept decision.

1. **Start + prompt.** `session open`, then `prompt submit … "<a UI idea, e.g. a sign-up card>"`.
   - *Watch:* do you understand what state you're in and what to do next?
2. **Get variants on screen.** Register variant HTML (`variants register --from <dir>` with `a.html`/
   `b.html`/`c.html`, each stamping `data-od-id` on its components). Open the printed `openPaths` in your
   browser.
   - *Watch:* could you actually see the variants? Was finding/opening them obvious or fiddly?
3. **Choose a baseline.** `baseline select <id> <A|B|C>` then `baseline commit`.
   - *Watch:* was it clear this was *your* choice to make?
4. **Comment on a component.** `comment add … --od-id <id> --note "<change you want>"`.
   - *Watch:* could you express what you wanted? (Note: you currently type a selector — is that painful?)
5. **Synthesize + approve.** `synthesize`, review the draft change list, then `batch approve`.
   - *Watch:* did you feel you understood what you were approving before you approved it?
6. **Two-gate apply (the heart of it).** `apply <sid> <bid> --candidate-from <candidate.html>` — this
   **stages** the change and prints an `openPath` + an honest per-component diff; the design is **not yet
   live**. Open the path, look at what changed, then **`accept`** (or **`discard`** to reject).
   - *Watch:* did "stage then accept" make you feel in control? Could you tell the change had NOT been
     applied until you accepted? Did the diff match what you opened?
7. **Try to reject.** Run another `apply` with an out-of-scope change (edit a component you did NOT
   comment on) — it should be **REJECTED**. Then `discard` a staged change.
   - *Watch:* did the system stop a change you didn't authorize? Did that build or hurt your trust?
8. **Look back.** `revisions` — confirm the history shows only changes **you** accepted.
   - 🛑 *Critical check:* is there any revision you did **not** approve? If yes, STOP and flag it (this is
     the F2 caveat from the brief).
9. **Hand off.** `handoff export` — does the result look like something you could give to a developer?

## Feedback form (copy + fill per run)

```
Tester:            Date:            STUDIO_DATA path:
Mode: [ ] I drove the CLI   [ ] Claude Code drove, I supervised
Per task (1–9): ✅/❌ + one line of what happened or confused you
  1: …   2: …   3: …   4: …   5: …   6: …   7: …   8: …   9: …
Overall:
- Did you feel IN CONTROL of every change that stuck?  [ ] yes  [ ] mostly  [ ] no — where it broke:
- The 🛑 safety check (task 8): any revision you didn't approve?  [ ] none  [ ] yes — describe:
- Biggest point of confusion:
- One thing that would most improve the control experience:
- (Out of scope, but note it) anything about SEEING/visual that frustrated you:
```

Drop completed forms in `evidence/` (or send them back). This is the only channel to evidence for the
project's still-unproven ergonomics claim — thank you.
