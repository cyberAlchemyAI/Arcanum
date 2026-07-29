# Handoff Notice

Handoff Notice is a Transmutation sigil for turning bounded work context into a durable, repository-local collaboration notice that another person or agent can retrieve with a short code.

It creates two immutable representations of the same notice:

- a machine-readable JSON record,
- a human-readable Markdown message.

The returned `HN-...` code is a content-derived locator. It is not a secret, permission, decision, task cursor, or proof that the notice was pushed to a shared remote.

## Use When

- work needs a concise continuation message for another person, role, session, or agent lane,
- the message should survive chat or session boundaries,
- a handoff needs explicit open calls, boundaries, next actions, and source references,
- the receiving party should be able to verify that the stored notice has not drifted,
- a repository commit will be used later as the transport.

## Do Not Use When

- an external message must be sent immediately,
- Git commit or push is the actual requested operation,
- a human-owned decision needs resolution,
- a task or SWU needs selection and execution,
- a terminal receipt needs route ranking or dispatch,
- the notice would cross a public/private boundary.

Those operations remain with their existing owners. A notice can point to them, but it cannot perform or authorize them.

## Modes

### `publish`

Validate one JSON payload, bind it to the declared repository, persist its JSON and Markdown representations, update the local locator index, and return the locator and verification receipt.

```bash
python3 <handoff-notice-package>/scripts/handoff_notice.py publish \
  --repo-root /path/to/repository \
  --input /path/to/notice-input.json
```

The default output root is:

```text
.arcanum/handoff-notices/
├── index.json
└── notices/
    ├── HN-<digest-prefix>.json
    └── HN-<digest-prefix>.md
```

`created_at` is generated when omitted. Preserve an explicit `created_at` value when an idempotent replay must return the same code. Codes normally contain 12 digest characters and extend deterministically if that prefix is already bound to different content.

### `resolve`

Resolve one exact code inside one explicit repository scope, verify its digest and index entry, and return the notice:

```bash
python3 <handoff-notice-package>/scripts/handoff_notice.py resolve HN-0123456789AB \
  --repo-root /path/to/repository
```

### `inspect`

Perform the same integrity checks as `resolve`, but return metadata without copying the notice body into the receipt:

```bash
python3 <handoff-notice-package>/scripts/handoff_notice.py inspect HN-0123456789AB \
  --repo-root /path/to/repository
```

In an agent chat with the runtime package installed, the intended handoff is:

```text
$handoff-notice resolve HN-0123456789AB in /path/to/repository
```

The agent resolves the deterministic script relative to the `SKILL.md` it loaded; it must not assume the shell's current directory is the package directory.

## Sharing Boundary

`publish` writes a local artifact. Another person or agent can retrieve the code only after the notice files travel through an explicitly owned transport such as:

- a reviewed Git commit and push,
- a shared filesystem,
- an approved external delivery system.

The sigil reports whether the notice is untracked, tracked with local changes, or present in the current local commit. It deliberately reports remote availability as `unverified`.

## Relationship To Existing Owners

- `continuation-router` owns route ranking, authorization, one-hop dispatch, and owner receipt joining.
- `task-session` owns task or SWU selection, readiness, bounded execution, and closeout.
- Git publication remains a separately authorized workflow.
- Messaging systems remain separately authorized external delivery workflows.

## Why This Is A Transmutation

The agent must synthesize a useful handoff from source evidence and human intent. Once that payload exists, a deterministic script validates, stores, hashes, and resolves it. The capability stops before autonomous orchestration or external delivery.
