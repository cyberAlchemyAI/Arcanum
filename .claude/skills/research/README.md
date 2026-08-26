# Research

Research is an Arcana type-owner skill for governed, evidence-backed research
dispatches. It adds research-specific roles, skeptic gates, source discipline,
and findings semantics to the portable lifecycle owned by
[`subagent-strategy`](../subagent-strategy/).

Every governed research dispatch must first have a validated
`research-initial-definitions.md` in its working folder. The sibling
[`research-initial-definitions`](../research-initial-definitions/) skill owns
that informational baseline and its deterministic structural validator.
The working folder always identifies one research beneath a repo-local directory
literally named `research`; that container may appear at any repository depth.

Use Research for multi-source synthesis, precedent work, falsification, or
multi-perspective audit. Use [`review`](../review/) when an existing artifact
needs verified change requests. A small direct lookup remains inline.

The canonical executable contract is [SKILL.md](SKILL.md). Generated runtime
packages under `.agents/skills/` and `.claude/skills/` are derived surfaces.
