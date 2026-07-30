---
name: html-preview-server
description: "Use when opening, serving, checking, listing, or stopping existing local HTML artifacts through a verified loopback server and direct browser handoff."
argument-hint: "[open|start|status|stop] <html-path> [--root <directory>] [--port <port>] | list [--limit <count>]"
tier: formulae
domain: local-html-preview
version: 0.2.0
origin: generalized from repeated local HTML preview, localhost handoff, browser verification, and cleanup workflows
allowed-tools: Read, Glob, Grep, Bash
---

# Sigil: HTML Preview Server

<objective>
Resolve one existing local HTML artifact, start or reuse a managed loopback-only
server, verify the exact page URL, open it through the available browser runtime,
and preserve explicit discovery, status, and cleanup controls.
</objective>

<logic-type>
Formulae: deterministic target resolution, contained static serving, readiness
verification, browser handoff, and managed shutdown.
</logic-type>

<commands>
- `html-preview-server <html-path>`: alias for `open`.
- `html-preview-server open <html-path>`: start or reuse, verify, navigate the
  concrete URL through the available browser runtime, and return the URL.
- `html-preview-server start <html-path>`: start or reuse and verify without
  requiring browser navigation.
- `html-preview-server status <html-path>`: inspect the managed target server.
- `html-preview-server stop <html-path>`: stop only the managed server for the
  exact target.
- `html-preview-server list [--limit <count>]`: return sanitized recent, online,
  and offline views without changing server state. Default limit: `20`; maximum:
  `100`.
- `--root <directory>`: use an explicit containing server root instead of the
  HTML file's parent.
- `--port <port>`: request a specific loopback port. Default: `0`, which asks the
  operating system for a free port.
</commands>

<applicability>
Use this sigil when:

- the user asks to open, serve, or preview an existing local `.html` or `.htm`
  artifact;
- the user asks for the localhost URL directly;
- the user asks which managed HTML previews were used recently or are currently
  online or offline;
- a generated static artifact needs HTTP-relative asset behavior;
- a managed preview server must be checked or stopped;
- a browser-visible validation should begin from one exact local artifact.

Do not use this sigil when:

- the user is asking to create, edit, critique, or redesign the HTML;
- the target already has a project-owned development-server command that the user
  explicitly selected;
- the request is remote deployment, public sharing, tunneling, or LAN exposure;
- the target is not a local HTML artifact or directory containing `index.html`;
- browser automation would perform consequential external actions.
</applicability>

<inputs>
Required:

- mode, defaulting to `open`.
- for `open`, `start`, `status`, or `stop`: an exact local HTML path, or a
  directory containing `index.html`.

Optional:

- explicit containing root;
- explicit port;
- `list` result limit from `1` through `100`;
- consuming environment browser runtime;
- request to preserve or stop the server after inspection.
</inputs>

<process>
## Step 1 - Resolve the exact preview target

1. Resolve the caller-supplied path without broad repository discovery.
2. Require an existing `.html` or `.htm` file. A directory is accepted only when
   it contains `index.html`.
3. Default the serving root to the HTML file's containing directory.
4. When `--root` is supplied, resolve it and require the target's real path to
   remain inside that root.
5. Do not inspect or modify unrelated repository files.

## Step 2 - Run the deterministic lifecycle helper

Use the installed package script:

```bash
node <skill-directory>/scripts/html-preview-server.mjs \
  <open|start|status|stop> <html-path> \
  [--root <directory>] [--port <port>]
```

1. Bind only `127.0.0.1`.
2. Use a dynamic port unless the caller requested an exact port.
3. Reuse a healthy managed server for the same target.
4. Reject traversal outside the real serving root.
5. Do not expose directory listings.
6. Store lifecycle state only in the operating system temporary directory.
7. Treat the helper's JSON receipt as server lifecycle evidence, not browser or
   application evidence.
8. After a successful `open`, `start`, or `stop`, update the separate sanitized
   history under an owner-only lock. Retain no token, PID, authorization header,
   or stale URL in history.
9. Perform health and exact-byte work outside the history lock. Recover a stale
   history lock only when its owner is absent and its age exceeds the bounded
   stale threshold.
10. Treat history as auxiliary evidence. If history persistence fails after a
    primary lifecycle result is known, preserve that lifecycle result and return
    `history_update: failed`; never report a completed stop as blocked.

## Step 3 - Open directly when mode is `open`

1. Consume the exact verified `url` from the helper receipt.
2. Use the active shared browser runtime to navigate that URL immediately. Do not
   ask the user for a second confirmation merely to open the local loopback page.
3. Prefer the repository's already-provided browser runtime. Never create a
   `package.json`, package root, or new dependency solely to obtain a browser.
4. Record whether navigation reached the expected URL, the observed page title,
   and any console errors.
5. If a headed browser surface is unavailable, preserve the successful HTTP proof
   and return the clickable URL; do not claim a visible browser was opened.
6. Do not follow external links or submit forms unless the user separately
   authorizes that browser interaction.

## Step 4 - Preserve lifecycle intent

1. `open` and `start` leave the managed server running so the returned URL remains
   usable.
2. `status` performs no startup or shutdown.
3. `stop` is idempotent and shuts down only a server that authenticates as the
   managed server for the exact target.
4. Report whether the server was started, reused, already stopped, or stopped.

## Step 5 - List sanitized recent, online, and offline views

For `list`:

1. Read only the owner-managed temporary state directory and sanitized history.
   Do not crawl for HTML, inspect arbitrary processes, or sweep ports.
2. Merge retained history with compatible legacy live-state records.
3. Classify an entry as `online` only when its state shape is valid, its
   token-authenticated health check passes, its target/root identity matches, and
   its exact target bytes verify at list time.
4. Classify every other retained target as `offline` with a bounded reason such
   as `stopped`, `no-live-state`, `stale-state`, `invalid-state`,
   `identity-conflict`, `target-missing`, or `verification-failed`.
5. Set `url: null` for every offline entry. A previously allocated loopback URL
   is not reusable evidence.
6. Define `recent` as successful helper `open` requests ordered by
   `last_open_requested_at`. This timestamp does not prove browser navigation.
7. Keep all targets that currently verify online and the 50 most recent offline
   history entries. Treat history as OS-temporary rather than durable
   cross-reboot storage.
8. Return untruncated counts and at most the requested number of items per view.
   `list` starts, stops, repairs, and restarts nothing.

## Step 6 - Close with a fixed receipt

Return the output contract. Keep HTTP reachability, browser observation, and
application behavior as separate evidence fields.
</process>

<quality-bar>
A successful execution must:

- resolve one exact local HTML target;
- default to the containing directory without broad repository analysis;
- bind only to `127.0.0.1`;
- use a collision-resistant dynamic port by default;
- reuse a healthy same-target server rather than start a duplicate;
- list known targets without requiring the caller to remember an exact path;
- keep recent, online, and offline semantics explicit and deterministic;
- authenticate and exact-byte verify every entry classified online;
- retain only sanitized, owner-only, capped OS-temporary history;
- preserve truthful primary lifecycle receipts when auxiliary history fails;
- keep network verification outside the history critical section and recover
  only conservatively stale history locks;
- return no stale URL for an offline entry;
- verify the exact target URL over HTTP;
- reject path traversal and avoid directory listings;
- open the verified URL directly in `open` mode when a browser runtime exists;
- return the concrete clickable URL even when a headed browser is unavailable;
- keep the server alive after `open` or `start` and stop it only through explicit
  `stop` or caller-owned cleanup;
- avoid new package roots and dependency installation;
- separate server, browser, and application proof.
</quality-bar>

<anti-patterns>
Avoid:

- binding to `0.0.0.0`, a LAN address, or a public tunnel by default;
- using a fixed port without checking for collision;
- starting duplicate servers for one target;
- using `xdg-open` success as the only proof of reachability;
- treating HTTP 200 as proof that the page is correct, accessible, or usable;
- treating browser navigation as proof of application readiness;
- serving a repository root when the containing directory is sufficient;
- silently widening the root to fix missing assets;
- installing Playwright, adding `package.json`, or creating a package root only
  for preview;
- stopping unrelated processes from unverified PID state;
- exposing health tokens, token fingerprints, PIDs, authorization headers, raw
  state, or stale URLs through aggregate output;
- treating `recent` as proof that browser navigation occurred;
- treating offline preview state as remote deployment or network status;
- making `list` start, stop, repair, or restart a server;
- holding the aggregate history lock across health or exact-byte network checks;
- turning an auxiliary history-write failure into a false primary lifecycle
  failure;
- crawling the repository for HTML or scanning unmanaged processes and ports;
- leaving the user without the concrete URL or lifecycle state.
</anti-patterns>

<observability>
A meaningful execution is any `open`, `start`, `status`, `stop`, or `list`
attempt that
returns a user-facing receipt.

When the consuming repository has standard Arcanum observability, summarize the
latest execution through the general post-run hook using:

- sigil: `html-preview-server`;
- tier: `formulae`;
- mode;
- target kind: file or directory-index;
- root policy: containing-directory or explicit-root;
- port policy: dynamic or explicit;
- server state: started, reused, running, stopped, already-stopped, or blocked;
- HTTP verification status;
- browser navigation: observed, unavailable, skipped, or failed;
- console error count when observed;
- for `list`: history scope, known/recent/online/offline counts, ignored malformed
  record counts, and returned-item counts;
- anti-pattern hits;
- workflow gaps;
- output-contract drift;
- reflection trigger.

Default reflection triggers are 5 meaningful executions, 10 generated receipts,
3 related workflow gaps, or 1 severe security or lifecycle gap.
</observability>

<output-contract>
Return:

```markdown
## HTML Preview Server Result

- Mode: open | start | status | stop | list
- Target: <resolved path>
- Root: <resolved path>
- Server: started | reused | running | stopped | already-stopped | blocked
- URL: <verified loopback URL | none>
- HTTP verification: pass | fail | not run
- Browser navigation: observed | unavailable | skipped | failed
- Browser evidence: <title and console summary | none>
- State: <managed state path | none>
- History update: recorded | failed | not applicable
- Proof boundary: <what this run does and does not establish>
- Follow-up: <keep using URL | stop command | blocker>
```

For `list`, return the helper's sanitized JSON receipt containing:

- `receipt_version: html-preview-server/list-v1`;
- untruncated `known`, `recent`, `online`, and `offline` counts;
- limited `recent`, `online`, and `offline` arrays;
- online URLs only;
- ignored malformed-record counts;
- the proof boundary separating helper `open` requests, managed-loopback health,
  browser navigation, and remote network status.
</output-contract>
