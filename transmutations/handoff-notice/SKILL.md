---
name: handoff-notice
description: "Use when: publishing a durable repository-local handoff notice with a short verifiable locator, or resolving that locator in a later person, agent, or session context."
argument-hint: "publish <scope> | resolve <HN-code> | inspect <HN-code>"
tier: transmutations
domain: collaboration-continuity
version: 0.1.0
origin: generalized from teammate handoff memo and continuation-boundary practice
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Sigil: Handoff Notice

<objective>
Turn bounded work evidence into one durable repository-local handoff notice, return a short verifiable locator, and allow a later person or agent to resolve that locator without treating the notice as authority.
</objective>

<logic-type>
Transmutation: evidence-bounded collaboration synthesis with deterministic persistence and resolution.
</logic-type>

<trigger>
Use this sigil when the user wants to leave, publish, retrieve, inspect, or continue from a repository-local message for another person, role, future session, agent lane, or owner route.

Do not use it merely because a normal answer could contain a summary.
</trigger>

<inputs>
For `publish`, resolve:

- one explicit repository root,
- recipient and producer identity kinds and labels,
- notice type and current status,
- subject and project scope,
- why the notice matters now,
- key points grounded in current evidence,
- open calls that remain unresolved,
- boundaries that the recipient must preserve,
- concrete next actions and their owners,
- source references sufficient to re-open the work,
- optional next-owner route hint, terminal receipt reference, superseded locator, or resolution reference.

For `resolve` or `inspect`, require one exact `HN-...` code and one explicit repository root.
</inputs>

<process>
## Publish

1. Confirm the notice belongs in the declared repository and does not cross a public/private boundary.
2. Read only the evidence needed to write the handoff.
3. Separate observed results, open calls, and proposed next actions. Do not turn a proposal into an accepted decision.
4. Create an input payload matching `schemas/handoff-notice.schema.json`. Start from `templates/handoff-notice.json` when useful.
5. Keep the message concise enough to paste into chat while preserving source references and boundaries.
6. Resolve `scripts/handoff_notice.py` relative to this `SKILL.md`; never assume the current working directory is the skill package.
7. Run:

   ```bash
   python3 <resolved-skill-root>/scripts/handoff_notice.py publish \
     --repo-root <repository-root> \
     --input <payload.json>
   ```

8. Read the receipt. A passing receipt must contain a code, digest, exact JSON and Markdown paths, transport status, remote availability, and the communication-evidence authority boundary.
9. If the user asked to share the notice, route Git commit/push or external delivery separately. Do not claim access before that transport is verified.

## Resolve

1. Require the exact repository root and locator code.
2. Resolve the deterministic script relative to this `SKILL.md`, then run:

   ```bash
   python3 <resolved-skill-root>/scripts/handoff_notice.py resolve <HN-code> \
     --repo-root <repository-root>
   ```

3. Fail closed on unknown, malformed, out-of-scope, ambiguous, or digest-mismatched locators.
4. Present the notice's current status, open calls, boundaries, next actions, source references, and supersession state.
5. Return any next-route hint as a recommendation only. Do not rank, authorize, dispatch, mutate, or execute it.

## Inspect

Use `inspect` instead of `resolve` when only integrity, lifecycle, path, digest, and transport metadata are needed.
</process>

<quality-bar>
A successful execution must:

- preserve recipient, producer, status, scope, requested action, open calls, boundaries, and source references,
- generate one collision-checked locator bound to the repository fingerprint, immutable notice payload, artifact paths, and digest,
- write both JSON and readable Markdown representations,
- make index and artifact drift detectable,
- distinguish local storage, local Git state, and unverified remote availability,
- surface supersession without rewriting the old notice,
- state that the notice and locator grant no authority,
- return the downstream owner without performing its work,
- keep public examples and fixtures product-neutral.
</quality-bar>

<anti-patterns>
Avoid:

- naming the capability `notification` when no external delivery occurs,
- treating the code as a secret, permission, authentication token, task cursor, or readiness proof,
- resolving a code outside the explicitly declared repository,
- mutating a notice beneath a stable code,
- swallowing a digest mismatch or locator collision,
- equating `consumed` with `resolved`,
- answering a human-owned open call,
- impersonating the recipient,
- auto-committing, pushing, messaging, dispatching, or executing,
- claiming another party can access a local-only notice,
- copying private project prose into the public sigil package or fixtures.
</anti-patterns>

<observability>
A meaningful execution is an attempted `publish`, `resolve`, or `inspect` that produces an artifact, locator, validation result, or owner handoff.

Record compact telemetry using `templates/usage-telemetry.md`. Do not copy message bodies into telemetry.

Default reflection triggers:

- 5 meaningful executions,
- 10 generated or materially modified artifacts,
- 3 related locator, schema, or routing gaps,
- 1 severe gap.

Severe gaps include wrong-artifact resolution, cross-scope retrieval, accepted digest drift, private-content leakage, unauthorized Git or external delivery, notice-as-authority behavior, or route execution inside this sigil.
</observability>

<output-contract>
Return:

```markdown
## Handoff Notice Result

- Mode: publish | resolve | inspect
- Status: pass | blocked
- Code: HN-...
- Repository scope: <root or fingerprint>
- Notice: <JSON path>
- Message: <Markdown path>
- Digest verification: pass | fail
- Notice status: draft | open | flag | blocked | consumed | resolved | superseded
- Superseded by: <codes or none>
- Transport status: local-only | git-tracked-uncommitted | committed-local | unavailable
- Remote availability: unverified
- Authority: communication evidence only; grants no permission
- Open calls: <count>
- Next owner: <capability, person, role, or none>
- Validation: <checks performed>
- Follow-up: <separate transport or owner route, or none>
```
</output-contract>
