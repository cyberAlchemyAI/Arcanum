# Decision Record: Goal Public-Boundary Repair

## Decision

- Decision id: `DEC-GOAL-PUBLIC-BOUNDARY-REPAIR-001`
- Decision source: user message on 2026-06-21
- Selected option: Option 1, apply staged public-boundary repair
- Batch id: `GOAL-STAGED-DELTA-PUBLIC-BOUNDARY-001`
- Result: approved

## User Policy

Inside public `arcanum`, keep only generic spell contracts, public schemas,
neutral defaults, opaque handles, and development evidence safe for the public
package. The private root repository carries the concrete instance of the
decision-profile schema with the user's filled profile.

## Rationale

This preserves the public/private boundary while allowing the goal work-pack to
continue. The public spell can describe a private runtime profile handle and a
consuming-repository profile instance, but must not include local absolute paths,
private repository/workspace names, or filled profile content.

## Approved Scope

- `arcanum/spells/goal/CRAFT.md`
- `arcanum/spells/goal/.craft/ledger.yml`

## Non-Scope

- No generated runtime surfaces.
- No private profile contents.
- No commit, push, PR, publication, or parent gitlink movement.
- No runtime implementation beyond clearing the W0 public-boundary gate.

## Validation Required

- Approval token schema parses and validates.
- Craft ledger YAML parses.
- Markdown links pass for `CRAFT.md` and W0 evidence.
- Hidden public-boundary scan over `arcanum/spells/goal` has no private path or
  private workspace/profile literals.
- `git -C arcanum diff --check -- spells/goal definitions` passes.
