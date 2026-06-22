# Staged Source-State Sync Proposal

## Proposal Status

- State: applied
- Created by: `SWU-GOAL-001` validation block
- Applies to: `SWU-GOAL-002`
- Requires approval token before active Craft ledger mutation: satisfied

## Problem

The public goal spell package contains stale Craft state and private
provenance/profile literals in:

- `arcanum/spells/goal/CRAFT.md`
- `arcanum/spells/goal/.craft/ledger.yml`

The README, public schema, define run, design run, plan run, and goal profile
exist, but the Craft view and ledger still describe earlier planned state and
private source locations.

## Proposed Repair

Apply a scoped public-boundary repair that:

1. Replaces private path/profile literals with public-safe opaque handles or
   neutral descriptions.
2. Updates the Craft view to show README, decision-profile schema, define,
   design, plan, and goal profile artifacts as authored.
3. Preserves the public/private split decision without naming private local
   paths or private repository names.
4. Keeps the spell status draft and promotion gate active.
5. Does not generate runtime surfaces, publish, commit, push, create a PR, or
   move parent gitlinks.

## Framed Diff Summary

```text
target: arcanum/spells/goal/.craft/ledger.yml and arcanum/spells/goal/CRAFT.md
operation: update
remove: absolute/private workspace provenance and filled-profile path literals
replace with: public-safe opaque upstream-design reference and private-runtime-profile-handle wording
update: stale planned artifact statuses for README, decision-profile.schema, invoke define/design/plan, and goal profile package
hold: active ledger mutation until approval token is present
```

## Approval And Apply

- Approval token: `APPROVAL-TOKEN-GOAL-PUBLIC-BOUNDARY-001.json`
- Decision record: `DECISION-RECORD-GOAL-PUBLIC-BOUNDARY-001.md`
- Apply receipt: `SWU-GOAL-002-APPLY-RECEIPT.yml`
- Result: pass

## Validation Expectation

- Hidden public-boundary scan over `arcanum/spells/goal` returns no private
  path/profile hits.
- Craft schema validation passes or manual ledger review records any schema
  validator gap.
- Markdown links pass for `CRAFT.md`.
- `git -C arcanum diff --check -- spells/goal definitions` passes.

## Decision Gate

See `DECISION-GATE-GOAL-PUBLIC-BOUNDARY.md`.
