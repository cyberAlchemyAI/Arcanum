# Resolution Route Manifest

Resolve every dependency relative to the directory containing
`resolution-router/SKILL.md`. This keeps canonical and generated repo-scoped
skill packages deterministic when installed as sibling folders.

## Dependencies

| role | skill ID | relative path | status |
|---|---|---|---|
| lens analysis | `lens-router` | `../lens-router/SKILL.md` | available |
| lens packet contract | `lens-router` | `../lens-router/references/lens-packet.md` | available |
| low writer | `low-resolution-explanation` | `../low-resolution-explanation/SKILL.md` | available |
| medium writer | `medium-resolution-explanation` | `../medium-resolution-explanation/SKILL.md` | unavailable |
| high writer | `high-resolution-explanation` | `../high-resolution-explanation/SKILL.md` | unavailable |

## Resolution rules

Before loading a target marked `available`, verify that the exact file exists.
If it does not, report a manifest drift error rather than searching broadly for
a same-named skill.

For a target marked `unavailable`, do not search for substitutes and do not
silently downgrade. Return the route decision and expected target path so the
missing writer can be authored later.

Do not mark a route available until its skill passes structural validation and
the executable local contract checks in `validation.md`. Require fresh-agent
forward tests before registry promotion.

## Reserved IDs

The medium and high IDs above are reserved now to prevent future naming drift.
Changing an ID or path requires updating this manifest, the corresponding skill
metadata, and all validation scenarios in one change.

The earlier candidates used `working-resolution-explanation` and
`deep-resolution-explanation`. The user-confirmed taxonomy supersedes those
candidate IDs with `medium-resolution-explanation` and
`high-resolution-explanation`. Do not install both naming systems.
