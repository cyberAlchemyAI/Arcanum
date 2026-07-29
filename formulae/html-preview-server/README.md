# HTML Preview Server

HTML Preview Server opens an existing local HTML artifact through a verified,
loopback-only HTTP server without turning a small preview request into a repository
investigation or a new package root.

It provides four modes:

- `open` starts or reuses the exact target server, verifies the page, opens the URL
  through the available browser runtime, and returns the concrete URL;
- `start` starts or reuses the server and returns the verified URL without requiring
  browser evidence;
- `status` reports whether the target's managed server is healthy;
- `stop` shuts down only the managed server bound to that exact target.

`open` is the default when a caller supplies only an HTML path.

## Use this sigil when

- a user says “open this HTML,” “preview this page,” or “open this in the HTML
  server”;
- a generated HTML artifact should be reviewed through HTTP rather than `file://`;
- relative assets need the containing directory to remain the serving root;
- a prior preview server should be reused or stopped safely.

Do not use it to edit HTML, deploy remotely, expose a LAN listener, create a
tunnel, attest application readiness, or replace a project-owned development
server.

## Canonical command

From the Arcanum repository:

```bash
node formulae/html-preview-server/scripts/html-preview-server.mjs \
  open path/to/page.html
```

Optional controls:

```bash
node formulae/html-preview-server/scripts/html-preview-server.mjs \
  start path/to/page.html --port 8123

node formulae/html-preview-server/scripts/html-preview-server.mjs \
  status path/to/page.html

node formulae/html-preview-server/scripts/html-preview-server.mjs \
  stop path/to/page.html
```

The default port is dynamic. The containing directory is the default root. Use
`--root <directory>` only when the artifact's relative asset layout requires a
broader, explicitly bounded root.

## Browser handoff

The lifecycle helper owns deterministic server operations and HTTP readiness.
The invoking agent owns browser navigation:

1. consume the helper's `url`;
2. navigate that exact URL through the active browser runtime;
3. record title, page reachability, and console errors when browser evidence is
   requested or available;
4. return the clickable loopback URL even when a headed browser cannot be shown.

Do not create `package.json` or install Playwright solely for this handoff. Use the
browser runtime already provided by the consuming environment.

## State and cleanup

Runtime state is stored under the operating system temporary directory in
`arcanum-html-preview-server/`. State files contain a private health token, use
owner-only permissions, and are never repository artifacts.

The stop path authenticates against the managed server before shutdown. It does
not kill arbitrary process IDs from state files.

## Tier rationale

This is a Formulae sigil. Target resolution, root containment, loopback binding,
readiness, reuse, status, and cleanup are fixed mechanical operations with a stable
JSON receipt. Browser comprehension or visual quality remains outside the sigil's
deterministic proof boundary.

## Lifecycle status

Status: `candidate`

The artifact-local experiment harness covers low, medium, and complex lifecycle
cases. Promotion requires live repeated use and observed receipts; a passing local
script test does not itself establish broad runtime portability.
