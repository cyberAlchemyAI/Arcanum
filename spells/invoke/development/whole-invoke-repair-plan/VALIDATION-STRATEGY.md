# Validation Strategy

## Global Phases

| Phase | Purpose | Rule |
| --- | --- | --- |
| pre-execution | Rehash source anchors, target baselines, schemas, runner identities, and predecessor receipts. | Any mismatch blocks before writes. |
| post-produce | Validate staged outputs, schemas, negative denominator, focused tests, and real consumer behavior. | Create outputs may be absent before their SWU; commands run only after production. |
| closeout | Verify exact changed inventory, generated parity, aggregate suites, terminal owner receipt, and continuity. | A failed earlier command cannot be masked by later cleanup. |

## Command Families

- `python3 -m json.tool <json>` for planning and fixture JSON syntax.
- `python3 -m unittest ...` for focused canonical tests.
- Canonical fixture runners for Define, Design, capability status, Plan source, preacceptance, accepted stream, and Refresh.
- `arcanum/tools/sync-generated-skill-package.sh --target . --spell invoke` for preview; `--apply` only in the separately authorized implementation SWU.
- `git diff --check -- <exact allowlist>` plus exact untracked-file checks.

## Negative Denominator

The complete implementation denominator must reject at least: self-issued status; missing/wrong/stale mode evidence; wrong producer owner; stale exact ref; partial bundle publication; missing `joined_driver_digest`; adapter substitution; schema-only terminal substitution; request/response version mismatch; stale requested effect; arbitrary frontier with nonhistorical IDs; completed-prefix frontier; private source/path in public output; unsupported `full` route; historical `full` evidence made unreadable; wrong generated mirror; and failed consumer falsely reported PASS.

## Final Laboratory Proof

A generic public fixture must run Define → Design → Plan compilation → two WPRA rehearsals → Implementation Readiness preflight → preacceptance real consumers → independent review preparation boundary → request/response validation rehearsal → accepted-stream no-effect supervisor → terminal/continuity closeout. It emits no owner request and performs no implementation or external effect.
