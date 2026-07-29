#!/usr/bin/env node

import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import {
  mkdir,
  mkdtemp,
  rm,
  symlink,
  writeFile,
} from "node:fs/promises";
import { request } from "node:http";
import { tmpdir } from "node:os";
import path from "node:path";
import { promisify } from "node:util";
import { fileURLToPath } from "node:url";

const execFileAsync = promisify(execFile);
const developmentRoot = path.dirname(fileURLToPath(import.meta.url));
const artifactRoot = path.resolve(developmentRoot, "..");
const serverScript = path.join(
  artifactRoot,
  "scripts",
  "html-preview-server.mjs",
);

function parseJson(value) {
  return JSON.parse(value.trim());
}

async function invoke(args, environment) {
  const { stdout } = await execFileAsync(process.execPath, [serverScript, ...args], {
    env: environment,
    maxBuffer: 1024 * 1024,
  });
  return parseJson(stdout);
}

async function invokeBlocked(args, environment) {
  try {
    await invoke(args, environment);
  } catch (error) {
    assert.notEqual(error.code, 0);
    return parseJson(error.stderr);
  }
  assert.fail(`Expected command to block: ${args.join(" ")}`);
}

async function rawStatus(url, requestPath) {
  const parsed = new URL(url);
  return new Promise((resolve, reject) => {
    const outgoing = request(
      {
        host: parsed.hostname,
        port: parsed.port,
        method: "GET",
        path: requestPath,
      },
      (response) => {
        response.resume();
        response.on("end", () => resolve(response.statusCode));
      },
    );
    outgoing.on("error", reject);
    outgoing.end();
  });
}

async function main() {
  const fixtureRoot = await mkdtemp(
    path.join(tmpdir(), "html-preview-server-fixture-"),
  );
  const stateDirectory = path.join(fixtureRoot, "runtime-state");
  const environment = {
    ...process.env,
    ARCANUM_HTML_PREVIEW_STATE_DIR: stateDirectory,
  };
  const siteRoot = path.join(fixtureRoot, "site");
  const siblingRoot = path.join(fixtureRoot, "sibling");
  await mkdir(path.join(siteRoot, "assets"), { recursive: true });
  await mkdir(siblingRoot, { recursive: true });

  const primaryTarget = path.join(siteRoot, "index.html");
  const specialTarget = path.join(siteRoot, "résumé 100% #1.html");
  const sameNameTarget = path.join(siblingRoot, "index.html");
  const outsideFile = path.join(fixtureRoot, "outside.txt");
  const hiddenFile = path.join(siteRoot, ".hidden.txt");
  const nonHtmlFile = path.join(siteRoot, "notes.txt");
  const stylesheet = path.join(siteRoot, "assets", "site.css");
  const escapeLink = path.join(siteRoot, "outside-link.txt");

  await writeFile(
    primaryTarget,
    '<!doctype html><html><head><link rel="stylesheet" href="assets/site.css"><title>Primary</title></head><body>primary</body></html>\n',
  );
  await writeFile(
    specialTarget,
    "<!doctype html><html><title>Special</title><body>special</body></html>\n",
  );
  await writeFile(
    sameNameTarget,
    "<!doctype html><html><title>Sibling</title><body>sibling</body></html>\n",
  );
  await writeFile(stylesheet, "body { color: #123456; }\n");
  await writeFile(outsideFile, "outside\n");
  await writeFile(hiddenFile, "hidden\n");
  await writeFile(nonHtmlFile, "not html\n");
  await symlink(outsideFile, escapeLink);

  const managedTargets = new Set();
  const checks = [];
  try {
    const opened = await invoke(["open", primaryTarget], environment);
    managedTargets.add(primaryTarget);
    assert.equal(opened.status, "pass");
    assert.equal(opened.mode, "open");
    assert.equal(opened.server_state, "started");
    assert.equal(opened.host, "127.0.0.1");
    assert.equal(opened.verification.http_status, 200);
    assert.equal(opened.verification.exact_target_verified, true);
    assert.equal(
      opened.verification.target_sha256,
      opened.verification.response_sha256,
    );
    checks.push("dynamic open exact-byte verification");

    const reused = await invoke(["start", primaryTarget], environment);
    assert.equal(reused.server_state, "reused");
    assert.equal(reused.pid, opened.pid);
    assert.equal(reused.port, opened.port);
    assert.equal(reused.url, opened.url);
    checks.push("same-target reuse");

    const running = await invoke(["status", primaryTarget], environment);
    assert.equal(running.server_state, "running");
    assert.equal(running.pid, opened.pid);
    checks.push("read-only healthy status");

    const stylesheetResponse = await fetch(
      new URL("assets/site.css", opened.url),
    );
    assert.equal(stylesheetResponse.status, 200);
    assert.equal(
      await stylesheetResponse.text(),
      "body { color: #123456; }\n",
    );
    assert.equal(
      await rawStatus(opened.url, "/.hidden.txt"),
      404,
    );
    assert.ok(
      [403, 404].includes(
        await rawStatus(opened.url, "/%2e%2e/outside.txt"),
      ),
    );
    assert.equal(await rawStatus(opened.url, "/outside-link.txt"), 403);
    checks.push("contained assets and traversal controls");

    const conflictingPort =
      opened.port === 65535 ? opened.port - 1 : opened.port + 1;
    const portConflict = await invokeBlocked(
      ["start", primaryTarget, "--port", String(conflictingPort)],
      environment,
    );
    assert.equal(portConflict.status, "block");
    assert.match(portConflict.error, /different explicit port/);

    const rootConflict = await invokeBlocked(
      ["start", primaryTarget, "--root", fixtureRoot],
      environment,
    );
    assert.equal(rootConflict.status, "block");
    assert.match(rootConflict.error, /incompatible target identity/);
    checks.push("healthy identity conflict refusal");

    const concurrentTarget = specialTarget;
    const concurrent = await Promise.all([
      invoke(["start", concurrentTarget], environment),
      invoke(["start", concurrentTarget], environment),
    ]);
    managedTargets.add(concurrentTarget);
    assert.deepEqual(
      concurrent.map((receipt) => receipt.server_state).sort(),
      ["reused", "started"],
    );
    assert.equal(concurrent[0].pid, concurrent[1].pid);
    assert.equal(concurrent[0].url, concurrent[1].url);
    assert.match(concurrent[0].url, /r%C3%A9sum%C3%A9%20100%25%20%231\.html$/);
    checks.push("concurrent start lock and encoded path");

    const sibling = await invoke(["start", sameNameTarget], environment);
    managedTargets.add(sameNameTarget);
    assert.notEqual(sibling.server_key, opened.server_key);
    assert.notEqual(sibling.state_file, opened.state_file);
    assert.notEqual(sibling.url, opened.url);
    checks.push("same basename distinct identity");

    const missing = await invokeBlocked(
      ["start", path.join(siteRoot, "missing.html")],
      environment,
    );
    assert.equal(missing.status, "block");
    assert.match(missing.error, /does not exist/);
    const nonHtml = await invokeBlocked(
      ["start", nonHtmlFile],
      environment,
    );
    assert.equal(nonHtml.status, "block");
    assert.match(nonHtml.error, /\.html or \.htm/);
    checks.push("invalid target fail-closed behavior");

    const stopped = await invoke(["stop", primaryTarget], environment);
    managedTargets.delete(primaryTarget);
    assert.equal(stopped.server_state, "stopped");
    const stoppedAgain = await invoke(["stop", primaryTarget], environment);
    assert.equal(stoppedAgain.server_state, "already-stopped");
    const stoppedStatus = await invoke(["status", primaryTarget], environment);
    assert.equal(stoppedStatus.server_state, "stopped");
    checks.push("authenticated idempotent stop");

    process.stdout.write(
      `${JSON.stringify(
        {
          status: "pass",
          test_count: checks.length,
          checks,
        },
        null,
        2,
      )}\n`,
    );
  } finally {
    for (const target of managedTargets) {
      try {
        await invoke(["stop", target], environment);
      } catch {
        // Best-effort cleanup for a test-owned temporary target.
      }
    }
    await rm(fixtureRoot, { recursive: true, force: true });
  }
}

main().catch((error) => {
  process.stderr.write(`${error.stack ?? error.message}\n`);
  process.exitCode = 1;
});
