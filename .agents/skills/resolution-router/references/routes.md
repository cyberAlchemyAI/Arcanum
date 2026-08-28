# Resolution Route Manifest

Resolve writer paths relative to `resolution-router/SKILL.md`.

| role | skill ID | relative path | status |
|---|---|---|---|
| lens analysis | `lens-router` | `../lens-router/SKILL.md` | available |
| low writer | `low-resolution-explanation` | `../low-resolution-explanation/SKILL.md` | available |
| medium writer | `medium-resolution-explanation` | `../medium-resolution-explanation/SKILL.md` | available |
| high writer | `high-resolution-explanation` | `../high-resolution-explanation/SKILL.md` | unavailable |

Before loading an available dependency, verify that the exact file exists. Report
manifest drift rather than searching for a substitute. For an unavailable
target, report the missing implementation and do not silently downgrade.

Mark a route available only after its writer passes the applicable checks in
`validation.md` and realistic human-facing tests. The medium and high IDs are
reserved; do not also install the superseded `working-resolution-explanation`
or `deep-resolution-explanation` names.
