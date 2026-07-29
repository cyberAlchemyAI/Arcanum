---
name: html-preview-server
description: "Use when opening, serving, checking, or stopping an existing local HTML artifact through a verified loopback server and direct browser handoff."
argument-hint: "[open|start|status|stop] <html-path> [--root <directory>] [--port <port>]"
tier: formulae
domain: local-html-preview
version: 0.1.0
origin: generalized from repeated local HTML preview, localhost handoff, browser verification, and cleanup workflows
allowed-tools: Read, Glob, Grep, Bash
---

# Sigil: HTML Preview Server

<objective>
Resolve one existing local HTML artifact, start or reuse a managed loopback-only
server, verify the exact page URL, open it through the available browser runtime,
and preserve explicit status and cleanup controls.
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

- exact local HTML path, or a directory containing `index.html`;
- mode, defaulting to `open`.

Optional:

- explicit containing root;
- explicit port;
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

## Step 5 - Close with a fixed receipt

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
- leaving the user without the concrete URL or lifecycle state.
</anti-patterns>

<observability>
A meaningful execution is any `open`, `start`, `status`, or `stop` attempt that
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

- Mode: open | start | status | stop
- Target: <resolved path>
- Root: <resolved path>
- Server: started | reused | running | stopped | already-stopped | blocked
- URL: <verified loopback URL | none>
- HTTP verification: pass | fail | not run
- Browser navigation: observed | unavailable | skipped | failed
- Browser evidence: <title and console summary | none>
- State: <managed state path | none>
- Proof boundary: <what this run does and does not establish>
- Follow-up: <keep using URL | stop command | blocker>
```
</output-contract>
