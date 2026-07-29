#!/usr/bin/env node

import { createHash, randomBytes } from "node:crypto";
import { createReadStream } from "node:fs";
import {
  chmod,
  mkdir,
  readFile,
  realpath,
  rename,
  rmdir,
  stat,
  unlink,
  writeFile,
} from "node:fs/promises";
import { createServer } from "node:http";
import { tmpdir } from "node:os";
import path from "node:path";
import { spawn } from "node:child_process";
import { fileURLToPath } from "node:url";

const HOST = "127.0.0.1";
const RECEIPT_VERSION = "html-preview-server/v1";
const HEALTH_PATH = "/.well-known/arcanum-html-preview-server/status";
const STOP_PATH = "/.well-known/arcanum-html-preview-server/stop";
const SCRIPT_PATH = fileURLToPath(import.meta.url);
const DEFAULT_STATE_ROOT = path.join(tmpdir(), "arcanum-html-preview-server");

const MIME_TYPES = new Map([
  [".css", "text/css; charset=utf-8"],
  [".gif", "image/gif"],
  [".htm", "text/html; charset=utf-8"],
  [".html", "text/html; charset=utf-8"],
  [".ico", "image/x-icon"],
  [".jpeg", "image/jpeg"],
  [".jpg", "image/jpeg"],
  [".js", "text/javascript; charset=utf-8"],
  [".json", "application/json; charset=utf-8"],
  [".map", "application/json; charset=utf-8"],
  [".mjs", "text/javascript; charset=utf-8"],
  [".png", "image/png"],
  [".svg", "image/svg+xml; charset=utf-8"],
  [".txt", "text/plain; charset=utf-8"],
  [".webp", "image/webp"],
  [".woff", "font/woff"],
  [".woff2", "font/woff2"],
]);

function usage() {
  process.stdout.write(`Usage:
  html-preview-server.mjs <html-path>
  html-preview-server.mjs <open|start|status|stop> <html-path> [--root <directory>] [--port <port>]
`);
}

function emit(value, stream = process.stdout) {
  stream.write(`${JSON.stringify(value, null, 2)}\n`);
}

function fail(message, details = {}) {
  const error = new Error(message);
  error.details = details;
  throw error;
}

function parsePublicArgs(argv) {
  const values = [...argv];
  if (values.includes("--help") || values.includes("-h")) {
    return { help: true };
  }

  const knownModes = new Set(["open", "start", "status", "stop"]);
  let mode = "open";
  if (knownModes.has(values[0])) {
    mode = values.shift();
  }

  const target = values.shift();
  if (!target) fail("An exact HTML target path is required.");

  let root;
  let port = 0;
  while (values.length > 0) {
    const flag = values.shift();
    if (flag === "--root") {
      root = values.shift();
      if (!root) fail("--root requires a directory.");
    } else if (flag === "--port") {
      const rawPort = values.shift();
      if (rawPort === undefined) fail("--port requires an integer.");
      port = Number(rawPort);
      if (!Number.isInteger(port) || port < 0 || port > 65535) {
        fail("--port must be an integer between 0 and 65535.");
      }
    } else {
      fail(`Unknown argument: ${flag}`);
    }
  }

  return { help: false, mode, target, root, port };
}

function parseServeArgs(argv) {
  const parsed = {};
  const values = [...argv];
  while (values.length > 0) {
    const flag = values.shift();
    const value = values.shift();
    if (!value) fail(`Internal argument ${flag} is missing a value.`);
    parsed[flag.replace(/^--/, "")] = value;
  }
  for (const field of ["root", "entry", "state", "token", "port"]) {
    if (!(field in parsed)) fail(`Internal serve argument --${field} is required.`);
  }
  return {
    root: parsed.root,
    entry: parsed.entry,
    statePath: parsed.state,
    token: parsed.token,
    port: Number(parsed.port),
  };
}

function isContained(root, candidate) {
  const relative = path.relative(root, candidate);
  return (
    relative === "" ||
    (!relative.startsWith(`..${path.sep}`) &&
      relative !== ".." &&
      !path.isAbsolute(relative))
  );
}

async function resolveTarget(targetInput, rootInput) {
  const inputPath = path.resolve(targetInput);
  let inputStat;
  try {
    inputStat = await stat(inputPath);
  } catch {
    fail("HTML target does not exist.", { target: inputPath });
  }

  let entryCandidate = inputPath;
  let targetKind = "file";
  if (inputStat.isDirectory()) {
    entryCandidate = path.join(inputPath, "index.html");
    targetKind = "directory-index";
  }

  let entry;
  try {
    entry = await realpath(entryCandidate);
  } catch {
    fail("HTML target is unreadable or a directory has no index.html.", {
      target: entryCandidate,
    });
  }
  const entryStat = await stat(entry);
  if (!entryStat.isFile()) {
    fail("HTML target must resolve to a regular file.", { target: entry });
  }
  if (![".html", ".htm"].includes(path.extname(entry).toLowerCase())) {
    fail("Target must be an .html or .htm file.", { target: entry });
  }

  let root;
  let rootPolicy;
  if (rootInput) {
    try {
      root = await realpath(path.resolve(rootInput));
    } catch {
      fail("Explicit server root does not exist.", {
        root: path.resolve(rootInput),
      });
    }
    if (!(await stat(root)).isDirectory()) {
      fail("Explicit server root must be a directory.", { root });
    }
    rootPolicy = "explicit-root";
  } else {
    root = path.dirname(entry);
    rootPolicy = "containing-directory";
  }

  if (!isContained(root, entry)) {
    fail("HTML target escapes the resolved server root.", { root, target: entry });
  }

  const entryRelative = path.relative(root, entry);
  const encodedEntry = entryRelative
    .split(path.sep)
    .map((segment) => encodeURIComponent(segment))
    .join("/");
  return {
    target: entry,
    targetKind,
    root,
    rootPolicy,
    entryRelative,
    entryUrlPath: `/${encodedEntry}`,
  };
}

function stateRoot() {
  return process.env.ARCANUM_HTML_PREVIEW_STATE_DIR
    ? path.resolve(process.env.ARCANUM_HTML_PREVIEW_STATE_DIR)
    : DEFAULT_STATE_ROOT;
}

function statePathFor(target) {
  const digest = createHash("sha256").update(target).digest("hex").slice(0, 20);
  return path.join(stateRoot(), `${digest}.json`);
}

async function withTargetLock(statePath, operation) {
  const lockPath = `${statePath}.lock`;
  await mkdir(path.dirname(statePath), { recursive: true, mode: 0o700 });
  await chmod(path.dirname(statePath), 0o700);
  const deadline = Date.now() + 7000;
  while (true) {
    try {
      await mkdir(lockPath, { mode: 0o700 });
      break;
    } catch (error) {
      if (error.code !== "EEXIST") throw error;
      if (Date.now() >= deadline) {
        fail("Timed out waiting for the target lifecycle lock.", {
          state_file: statePath,
        });
      }
      await new Promise((resolve) => setTimeout(resolve, 50));
    }
  }
  try {
    return await operation();
  } finally {
    try {
      await rmdir(lockPath);
    } catch (error) {
      if (error.code !== "ENOENT") throw error;
    }
  }
}

async function readState(statePath) {
  try {
    return JSON.parse(await readFile(statePath, "utf8"));
  } catch {
    return null;
  }
}

async function removeState(statePath) {
  try {
    await unlink(statePath);
  } catch (error) {
    if (error.code !== "ENOENT") throw error;
  }
}

async function writeState(statePath, state) {
  await mkdir(path.dirname(statePath), { recursive: true, mode: 0o700 });
  await chmod(path.dirname(statePath), 0o700);
  const temporaryPath = `${statePath}.${process.pid}.tmp`;
  await writeFile(temporaryPath, `${JSON.stringify(state, null, 2)}\n`, {
    mode: 0o600,
  });
  await chmod(temporaryPath, 0o600);
  await rename(temporaryPath, statePath);
}

function authorizationHeaders(state) {
  return { authorization: `Bearer ${state.token}` };
}

async function fetchWithTimeout(url, options = {}, timeoutMs = 1200) {
  return fetch(url, {
    ...options,
    signal: AbortSignal.timeout(timeoutMs),
  });
}

async function health(state) {
  if (!state?.base_url || !state?.token) return null;
  try {
    const response = await fetchWithTimeout(
      `${state.base_url}${HEALTH_PATH}`,
      { headers: authorizationHeaders(state) },
      700,
    );
    if (!response.ok) return null;
    const payload = await response.json();
    return payload.token_fingerprint === state.token_fingerprint
      ? payload
      : null;
  } catch {
    return null;
  }
}

function sha256(value) {
  return createHash("sha256").update(value).digest("hex");
}

async function verifyTargetUrl(url, target) {
  const response = await fetchWithTimeout(url, {}, 2400);
  if (!response.ok) {
    fail("Managed server started but the exact HTML URL did not pass readiness.", {
      url,
      http_status: response.status,
    });
  }
  const responseBytes = Buffer.from(await response.arrayBuffer());
  const targetBytes = await readFile(target);
  const responseSha256 = sha256(responseBytes);
  const targetSha256 = sha256(targetBytes);
  if (responseSha256 !== targetSha256) {
    fail("Managed server returned different bytes than the exact HTML target.", {
      url,
      target,
      response_sha256: responseSha256,
      target_sha256: targetSha256,
    });
  }
  return {
    http_status: response.status,
    content_type: response.headers.get("content-type") ?? "unknown",
    target_sha256: targetSha256,
    response_sha256: responseSha256,
    exact_target_verified: true,
  };
}

function publicReceipt(mode, serverState, resolved, state, verification) {
  return {
    receipt_version: RECEIPT_VERSION,
    status: "pass",
    mode,
    server_state: serverState,
    target: resolved.target,
    target_kind: resolved.targetKind,
    root: resolved.root,
    root_policy: resolved.rootPolicy,
    host: state.host,
    port: state.port,
    url: state.url,
    pid: state.pid,
    state_file: state.state_file,
    server_key: state.server_key,
    helper_sha256: state.helper_sha256,
    verification,
    proof_boundary:
      "Proves managed loopback HTTP reachability for the exact target; does not prove visual correctness, usability, application readiness, or external integrations.",
  };
}

async function startOrReuse(mode, resolved, requestedPort) {
  const statePath = statePathFor(resolved.target);
  await withTargetLock(statePath, async () => {
    const previous = await readState(statePath);
    const previousHealth = await health(previous);
    if (previousHealth) {
      if (
        previous.target !== resolved.target ||
        previous.root !== resolved.root
      ) {
        fail("A healthy managed server exists with incompatible target identity.", {
          requested_target: resolved.target,
          requested_root: resolved.root,
          running_target: previous.target,
          running_root: previous.root,
        });
      }
      if (requestedPort !== 0 && previous.port !== requestedPort) {
        fail("A healthy managed server exists on a different explicit port.", {
          requested_port: requestedPort,
          running_port: previous.port,
        });
      }
      const verification = await verifyTargetUrl(previous.url, resolved.target);
      emit(publicReceipt(mode, "reused", resolved, previous, verification));
      return;
    }
    if (previous) await removeState(statePath);

    const token = randomBytes(32).toString("hex");
    const tokenFingerprint = createHash("sha256")
      .update(token)
      .digest("hex")
      .slice(0, 16);
    const child = spawn(
      process.execPath,
      [
        SCRIPT_PATH,
        "__serve",
        "--root",
        resolved.root,
        "--entry",
        resolved.entryRelative,
        "--state",
        statePath,
        "--token",
        token,
        "--port",
        String(requestedPort),
      ],
      { detached: true, stdio: "ignore" },
    );
    child.unref();

    const deadline = Date.now() + 5000;
    let state;
    while (Date.now() < deadline) {
      await new Promise((resolve) => setTimeout(resolve, 50));
      state = await readState(statePath);
      if (
        state?.token_fingerprint === tokenFingerprint &&
        (await health(state))
      ) {
        break;
      }
      state = null;
    }
    if (!state) {
      fail("Managed server did not become healthy before the startup timeout.", {
        target: resolved.target,
        requested_port: requestedPort,
        state_file: statePath,
      });
    }

    try {
      const verification = await verifyTargetUrl(state.url, resolved.target);
      emit(publicReceipt(mode, "started", resolved, state, verification));
    } catch (error) {
      try {
        await fetchWithTimeout(`${state.base_url}${STOP_PATH}`, {
          method: "POST",
          headers: authorizationHeaders(state),
        });
      } catch {
        // Preserve the original readiness failure.
      }
      throw error;
    }
  });
}

async function statusMode(resolved) {
  const statePath = statePathFor(resolved.target);
  const state = await readState(statePath);
  const currentHealth = await health(state);
  if (!currentHealth) {
    emit({
      receipt_version: RECEIPT_VERSION,
      status: "pass",
      mode: "status",
      server_state: state ? "stale" : "stopped",
      target: resolved.target,
      root: resolved.root,
      url: null,
      state_file: statePath,
      verification: "not_run",
    });
    return;
  }
  if (state.target !== resolved.target || state.root !== resolved.root) {
    fail("Managed server identity conflicts with the requested status root.", {
      requested_target: resolved.target,
      requested_root: resolved.root,
      running_target: state.target,
      running_root: state.root,
    });
  }
  const verification = await verifyTargetUrl(state.url, resolved.target);
  emit(publicReceipt("status", "running", resolved, state, verification));
}

async function stopMode(resolved) {
  const statePath = statePathFor(resolved.target);
  await withTargetLock(statePath, async () => {
    const state = await readState(statePath);
    const currentHealth = await health(state);
    if (!currentHealth) {
      if (state) await removeState(statePath);
      emit({
        receipt_version: RECEIPT_VERSION,
        status: "pass",
        mode: "stop",
        server_state: "already-stopped",
        target: resolved.target,
        root: resolved.root,
        url: null,
        state_file: statePath,
        verification: "not_run",
      });
      return;
    }
    if (state.target !== resolved.target || state.root !== resolved.root) {
      fail("Managed server identity conflicts with the requested stop root.", {
        requested_target: resolved.target,
        requested_root: resolved.root,
        running_target: state.target,
        running_root: state.root,
      });
    }

    const response = await fetchWithTimeout(`${state.base_url}${STOP_PATH}`, {
      method: "POST",
      headers: authorizationHeaders(state),
    });
    if (!response.ok) {
      fail("Managed server refused authenticated shutdown.", {
        url: state.base_url,
        http_status: response.status,
      });
    }

    const deadline = Date.now() + 2000;
    while (Date.now() < deadline && (await health(state))) {
      await new Promise((resolve) => setTimeout(resolve, 50));
    }
    await removeState(statePath);
    emit({
      receipt_version: RECEIPT_VERSION,
      status: "pass",
      mode: "stop",
      server_state: "stopped",
      target: resolved.target,
      root: resolved.root,
      url: state.url,
      state_file: statePath,
      verification: "shutdown_authenticated",
    });
  });
}

function authorized(request, token) {
  return request.headers.authorization === `Bearer ${token}`;
}

function responseJson(response, statusCode, value) {
  const body = `${JSON.stringify(value)}\n`;
  response.writeHead(statusCode, {
    "content-type": "application/json; charset=utf-8",
    "content-length": Buffer.byteLength(body),
    "cache-control": "no-store",
  });
  response.end(body);
}

async function serveMode(args) {
  const root = await realpath(args.root);
  if (!(await stat(root)).isDirectory()) {
    fail("Internal server root must be a directory.");
  }
  const entry = path.resolve(root, args.entry);
  if (!isContained(root, entry)) fail("Internal entry escapes the server root.");

  let closing = false;
  const tokenFingerprint = createHash("sha256")
    .update(args.token)
    .digest("hex")
    .slice(0, 16);
  const server = createServer(async (request, response) => {
    try {
      const requestUrl = new URL(request.url ?? "/", `http://${HOST}`);
      if (requestUrl.pathname === HEALTH_PATH) {
        if (!authorized(request, args.token)) {
          responseJson(response, 404, { status: "not_found" });
          return;
        }
        responseJson(response, 200, {
          status: "running",
          pid: process.pid,
          token_fingerprint: tokenFingerprint,
        });
        return;
      }
      if (requestUrl.pathname === STOP_PATH) {
        if (request.method !== "POST" || !authorized(request, args.token)) {
          responseJson(response, 404, { status: "not_found" });
          return;
        }
        responseJson(response, 200, { status: "stopping" });
        if (!closing) {
          closing = true;
          setImmediate(() => {
            server.close(async () => {
              await removeState(args.statePath);
              process.exit(0);
            });
          });
        }
        return;
      }

      if (!["GET", "HEAD"].includes(request.method ?? "")) {
        response.writeHead(405, { allow: "GET, HEAD" });
        response.end();
        return;
      }

      let decodedPath;
      try {
        decodedPath = decodeURIComponent(requestUrl.pathname);
      } catch {
        response.writeHead(400);
        response.end();
        return;
      }
      const decodedSegments = decodedPath.split("/").filter(Boolean);
      if (decodedSegments.some((segment) => segment.startsWith("."))) {
        response.writeHead(404);
        response.end();
        return;
      }
      let candidate = path.resolve(root, `.${decodedPath}`);
      if (!isContained(root, candidate)) {
        response.writeHead(403);
        response.end();
        return;
      }

      let candidateStat;
      try {
        candidateStat = await stat(candidate);
        if (candidateStat.isDirectory()) {
          candidate = path.join(candidate, "index.html");
          candidateStat = await stat(candidate);
        }
        candidate = await realpath(candidate);
      } catch {
        response.writeHead(404);
        response.end();
        return;
      }
      if (!isContained(root, candidate) || !candidateStat.isFile()) {
        response.writeHead(403);
        response.end();
        return;
      }

      response.writeHead(200, {
        "content-type":
          MIME_TYPES.get(path.extname(candidate).toLowerCase()) ??
          "application/octet-stream",
        "content-length": candidateStat.size,
        "cache-control": "no-store",
        "x-content-type-options": "nosniff",
      });
      if (request.method === "HEAD") {
        response.end();
        return;
      }
      const stream = createReadStream(candidate);
      stream.on("error", () => response.destroy());
      stream.pipe(response);
    } catch {
      if (!response.headersSent) response.writeHead(500);
      response.end();
    }
  });

  const cleanup = async () => {
    if (closing) return;
    closing = true;
    server.close(async () => {
      await removeState(args.statePath);
      process.exit(0);
    });
  };
  process.on("SIGTERM", cleanup);
  process.on("SIGINT", cleanup);

  await new Promise((resolve, reject) => {
    server.once("error", reject);
    server.listen({ host: HOST, port: args.port }, resolve);
  });
  const address = server.address();
  const port = typeof address === "object" && address ? address.port : args.port;
  const encodedEntry = args.entry
    .split(path.sep)
    .map((segment) => encodeURIComponent(segment))
    .join("/");
  const baseUrl = `http://${HOST}:${port}`;
  const helperSha256 = sha256(await readFile(SCRIPT_PATH));
  const serverKey = createHash("sha256")
    .update(`${entry}\0${root}`)
    .digest("hex")
    .slice(0, 20);
  await writeState(args.statePath, {
    receipt_version: RECEIPT_VERSION,
    target: entry,
    root,
    entry: args.entry,
    host: HOST,
    port,
    base_url: baseUrl,
    url: `${baseUrl}/${encodedEntry}`,
    pid: process.pid,
    server_key: serverKey,
    helper_sha256: helperSha256,
    token: args.token,
    token_fingerprint: tokenFingerprint,
    state_file: args.statePath,
    started_at: new Date().toISOString(),
  });
}

async function main() {
  if (process.argv[2] === "__serve") {
    await serveMode(parseServeArgs(process.argv.slice(3)));
    return;
  }

  const args = parsePublicArgs(process.argv.slice(2));
  if (args.help) {
    usage();
    return;
  }
  const resolved = await resolveTarget(args.target, args.root);
  if (args.mode === "status") {
    await statusMode(resolved);
  } else if (args.mode === "stop") {
    await stopMode(resolved);
  } else {
    await startOrReuse(args.mode, resolved, args.port);
  }
}

main().catch((error) => {
  emit(
    {
      receipt_version: RECEIPT_VERSION,
      status: "block",
      error: error.message,
      details: error.details ?? {},
    },
    process.stderr,
  );
  process.exitCode = 1;
});
