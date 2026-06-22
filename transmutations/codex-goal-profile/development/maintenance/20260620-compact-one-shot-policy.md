# Codex Goal Profile Maintenance - Compact One-Shot Policy

Date: 2026-06-20
Observed sigil: `codex-goal-profile`
Maintenance route: `sigil-maintenance-loop` with `sigil-development --update`
Reflection trigger: manual user request

## Signal Summary

The latest use of `codex-goal-profile` exposed a practical runtime gap: a rich
one-shot goal profile can exceed the native `/goal` input budget. The user also
requested support for private runtime decision profiles and for one-shot goals
that can use bounded Arcanum capability lanes such as `refine`, `invoke`,
`craft`, `decision-gate`, and subagents.

## Observer Pass

Observer mode: local fallback.

Reason: the change was tightly coupled to one sigil contract and its generated
runtime mirrors. No parallel subagent was spawned; the observer pass inspected
the current sigil package, generated mirrors, examples, and the private
`.arcanum/profiles/decision-profile.yml` path as runtime evidence.

## Applied Changes

- Added compact goal budget policy with default 4000-character target.
- Added sidecar profile/handoff pattern for dense Arcanum execution frames.
- Added private decision-profile policy that permits runtime influence while
  forbidding public copying of private profile contents.
- Added explicit one-shot stream policy for ordered multi-SWU execution.
- Added bounded capability lanes for `refine`, `invoke`, `craft`,
  `decision-gate`, and subagents with receipt/stop gates.
- Updated canonical package docs, template, examples, design, validation, and
  work-pack.
- Synced active `.agents` and `.claude` native skill mirrors for this sigil.

## Rejected Changes

- Did not edit deprecated `.codex/commands` snapshots. Those legacy command
  adapters regenerate only when explicitly requested with the legacy command
  profile, and editing their embedded snapshots by hand would create broad
  generated churn.
- Did not copy the private decision profile contents into public Arcanum
  package files.
- Did not make Codex Goal own Arcanum lifecycle execution. The transmutation
  still only produces a native goal profile.

## Remaining Gaps

| Gap | Severity | Next route |
| --- | --- | --- |
| No fixture runner counts generated `/goal` text against the 4000-character budget. | medium | Add a small validation fixture if repeated usage needs automated enforcement. |
| Deprecated command snapshots remain stale until the legacy command generator is explicitly run. | low | Regenerate only when maintaining legacy command surfaces. |

## Validation Notes

- Canonical and generated skill/package text were updated together for the
  active native skill surfaces.
- The private profile path was inspected for policy shape only; contents were
  not copied into public reusable docs.

## Next Lifecycle Step

Use the updated transmutation on the next one-shot profile request. If overlong
goals recur, add a length-count fixture and promote it into `VALIDATION.md`.
