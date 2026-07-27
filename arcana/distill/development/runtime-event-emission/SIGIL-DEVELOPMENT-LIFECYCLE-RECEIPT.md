# Sigil Development Lifecycle Receipt: DEC-DRE-001

## Identity

- Mode: `sigil-development --update distill`
- User authorization: execute all tasks
- Decision: accept the Invoke-authored design without widening
- Lifecycle status: accepted
- Execution policy: one SWU at a time; admit the declared successor only after
  the current SWU passes

## Accepted Authority Split

1. Distill owns runtime-event emission timing, producer behavior, direct usage
   telemetry, and evidence-emission closeout status.
2. Invoke retains the accepted event schema, resolver, semantic/provenance
   validator, and mutation-handoff authority.
3. Signal Observer retains append-only invocation telemetry and run-ID dedupe.
4. Bootstrap projects accepted canonical Distill files; generated files are
   never edited as authority.

No event or telemetry record gains verdict or mutation authority.

## Preserved Contract

The lifecycle update must preserve Distill's:

- Compact, Standard, Tournament, Deep, and Validate modes;
- proposal-track and recursive-round budgets;
- true-subagent-preferred role policy and labeled fallback;
- technique pack and activation/skipping rules;
- cycle guards, verdict meanings, recomposition, navigation, and next routes;
- existing output meanings, except for additive evidence/telemetry closeout
  fields explicitly approved by the work-pack.

## Baseline Binding

Existing source baselines at admission:

| Path | SHA-256 |
| --- | --- |
| `arcanum/arcana/distill/SKILL.md` | `43ac818225c2aca270d88a85fc2cf11d553c2283476ee97476bb70a307e37740` |
| `arcanum/arcana/distill/templates/usage-telemetry.md` | `84a01bd1da5aaa3fa66c3567078431e09f1fbb8624f9f68491d2c7f086cd98c4` |
| `arcanum/arcana/distill/development/VALIDATION.md` | `e6ed83a4c23988b30a4908a796148781e17e29740ea60cfbbbc70e96466012cc` |
| `arcanum/arcana/distill/development/READINESS-REVIEW.md` | `c85757c7265bad82b94c1f787b4ec20463f63b36cb0cc0bba3cd83a5946ca54a` |
| `arcanum/spells/invoke/development/distill-execution-evidence/GAP-LEDGER.md` | `8fef7cad3e666b23762bac3b10396b497a8053029fe7db9a56290f000bc4d007` |
| `arcanum/spells/invoke/development/distill-execution-evidence/VALIDATION.md` | `8be655525d394314bcaafef22e0a1211e7ead80833798d118046ab955ba5a1f2` |

The emitter, direct observer, and focused DRE runners were absent at admission.

## Selected Route

`SWU-DRE-001` is selected first. DRE-002 through DRE-007 may advance
sequentially only from their predecessor's passing receipt. `GAP-DEE-002`
remains open until the independent verification task passes.
