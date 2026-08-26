# Review

Review is an Arcana type-owner skill for adversarial assessment of existing
artifacts. It applies tensioned attack lenses, independent verification, and a
severity-ranked change-request contract through the dispatch lifecycle owned by
[`subagent-strategy`](../subagent-strategy/).

A review is read-only over its targets and produces exactly one synthesis
document, `review.md`, either inline or in a human-confirmed working folder. It
does not persist attacker transcripts and does not apply its own fixes.

Use [`research`](../research/) when the question concerns a new claim or
candidate rather than defects in an existing artifact. The canonical executable
contract is [SKILL.md](SKILL.md).
