# Tester Brief — read before you test (1 page)

Thank you for testing the **UI Prototyping Studio**. This page is your safety + consent note. It is short
on purpose. Read it, then follow [TEST-PROTOCOL.md](TEST-PROTOCOL.md).

## What you're testing (and what you're NOT)

You are testing the **governance loop**: can you, a human, *supervise* an AI agent (Claude Code) as it
proposes UI changes — and stay in control of every decision that sticks? Specifically: you generate
variants, pick a baseline, leave comments, and then **you alone** approve / apply / accept each durable
change.

A browser **preview + click-to-annotate** surface now ships (`studio preview <sid>`), with in-preview
Accept/Revert controls. The *polished* visual styling is still maturing, so your feedback here is primarily
about the **control surface** — staying in control of every durable change — not the pixels.

## The one safety caveat — please understand this before you consent

The studio's core enforces **what** can change (an out-of-scope edit is rejected) but does **not** yet
enforce **who** is acting. Concretely:

- The durable gates (`approve`, `apply`, `accept`) have **no human-vs-agent identity check**. The CLI runs
  every command under one actor (`STUDIO_ACTOR`, default `cli-user`) — so the system **cannot tell your
  command apart from the agent's**.
- This means: **if the agent ignored its instructions, it could approve + apply + accept its own change,
  and the core would not stop it.** The only thing preventing that is the agent's written operating
  contract (its "never-do" rules) — not the code.

Why it's still safe to test:
- **Bounded:** an out-of-scope change is always rejected (the scope fence is real, server-enforced).
- **Reversible + visible:** every change is an append-only revision you can see in `revisions`.
- **Your job:** you are the supervisor. Watch that **you** are the one approving/applying/accepting. If
  you ever see a revision recorded that *you* did not approve, that is exactly the issue we want you to
  report — note it and flag it.

A real identity gate is a planned next step; for this test it is deliberately deferred and disclosed (so
you can give informed consent). By proceeding you acknowledge this caveat.

## Ground rules

- Use a **fresh `STUDIO_DATA` path per run** (the protocol tells you how) so each run starts clean.
- Everything runs locally on your machine; nothing is sent anywhere.
- If something is confusing, that's data — write it down. Confusion is a finding, not your fault.

Ready? → [TEST-PROTOCOL.md](TEST-PROTOCOL.md)
