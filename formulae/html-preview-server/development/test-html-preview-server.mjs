#!/usr/bin/env node

import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import {
  mkdir,
  mkdtemp,
  readFile,
  rm,
  symlink,
  utimes,
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

    const openedStateSnapshot = await readFile(opened.state_file, "utf8");
    const historyFile = path.join(stateDirectory, "history.json");
    const historySnapshot = await readFile(historyFile, "utf8");
    assert.doesNotMatch(historySnapshot, /"token"|"pid"|"url"/);
    const listedAfterOpen = await invoke(["list"], environment);
    assert.equal(
      listedAfterOpen.receipt_version,
      "html-preview-server/list-v1",
    );
    assert.deepEqual(listedAfterOpen.counts, {
      known: 1,
      recent: 1,
      online: 1,
      offline: 0,
    });
    assert.equal(listedAfterOpen.recent[0].target, primaryTarget);
    assert.equal(listedAfterOpen.online[0].verification, "pass");
    assert.equal(listedAfterOpen.online[0].url, opened.url);
    assert.equal(listedAfterOpen.recent[0].last_mode, "open");
    assert.equal(listedAfterOpen.recent[0].offline_reason, null);
    assert.doesNotMatch(
      JSON.stringify(listedAfterOpen),
      /"token"|"token_fingerprint"|"pid"|"authorization"|"state_file"|"base_url"|"server_key"|"host"|"port"|"helper_sha256"|"started_at"/,
    );
    checks.push("sanitized recent and online list");

    await rm(historyFile);
    const listedLegacyState = await invoke(["list"], environment);
    assert.equal(listedLegacyState.counts.known, 1);
    assert.equal(listedLegacyState.counts.recent, 0);
    assert.equal(listedLegacyState.online[0].last_mode, "legacy-state");
    await writeFile(historyFile, historySnapshot, { mode: 0o600 });
    checks.push("legacy active state list compatibility");

    const historyLock = path.join(stateDirectory, "history.lock");
    await writeFile(
      historyLock,
      `${JSON.stringify({
        pid: 999_999,
        acquired_at: "2000-01-01T00:00:00.000Z",
      })}\n`,
      { mode: 0o600 },
    );
    const staleLockTime = new Date(Date.now() - 60_000);
    await utimes(historyLock, staleLockTime, staleLockTime);
    const reopenedAfterStaleLock = await invoke(
      ["open", primaryTarget],
      environment,
    );
    assert.equal(reopenedAfterStaleLock.server_state, "reused");
    assert.equal(reopenedAfterStaleLock.history_update, "recorded");
    checks.push("stale history-lock recovery");

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

    const parallelTargets = [
      path.join(siteRoot, "parallel-a.html"),
      path.join(siteRoot, "parallel-b.html"),
    ];
    await Promise.all(
      parallelTargets.map((target, index) =>
        writeFile(
          target,
          `<!doctype html><html><title>Parallel ${index}</title></html>\n`,
        ),
      ),
    );
    const parallelStarted = await Promise.all(
      parallelTargets.map((target) => invoke(["start", target], environment)),
    );
    for (const target of parallelTargets) managedTargets.add(target);
    assert.equal(
      parallelStarted.every((receipt) => receipt.history_update === "recorded"),
      true,
    );
    const parallelListed = await invoke(
      ["list", "--limit", "100"],
      environment,
    );
    assert.equal(
      parallelTargets.every((target) =>
        parallelListed.online.some((entry) => entry.target === target),
      ),
      true,
    );
    await Promise.all(
      parallelTargets.map((target) => invoke(["stop", target], environment)),
    );
    for (const target of parallelTargets) managedTargets.delete(target);
    checks.push("different-target concurrent history writes");

    const listedMixed = await invoke(["list", "--limit", "100"], environment);
    assert.equal(listedMixed.counts.known, 5);
    assert.equal(listedMixed.counts.recent, 1);
    assert.equal(listedMixed.counts.online, 3);
    assert.equal(listedMixed.counts.offline, 2);
    assert.equal(
      listedMixed.recent.some((entry) => entry.target === specialTarget),
      false,
    );
    assert.equal(
      listedMixed.recent.some((entry) => entry.target === sameNameTarget),
      false,
    );
    checks.push("start-only targets excluded from recent list");

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

    const historyBeforeFailure = await readFile(historyFile, "utf8");
    await rm(historyFile);
    await mkdir(historyFile);
    const stopped = await invoke(["stop", primaryTarget], environment);
    managedTargets.delete(primaryTarget);
    assert.equal(stopped.server_state, "stopped");
    assert.equal(stopped.history_update, "failed");
    const statusAfterHistoryFailure = await invoke(
      ["status", primaryTarget],
      environment,
    );
    assert.equal(statusAfterHistoryFailure.server_state, "stopped");
    await rm(historyFile, { recursive: true });
    await writeFile(historyFile, historyBeforeFailure, { mode: 0o600 });
    const stoppedAgain = await invoke(["stop", primaryTarget], environment);
    assert.equal(stoppedAgain.server_state, "already-stopped");
    assert.equal(stoppedAgain.history_update, "recorded");
    const listedStopped = await invoke(["list"], environment);
    const stoppedEntry = listedStopped.offline.find(
      (entry) => entry.target === primaryTarget,
    );
    assert.equal(stoppedEntry.preview_state, "offline");
    assert.equal(stoppedEntry.offline_reason, "stopped");
    assert.equal(stoppedEntry.url, null);
    assert.equal(
      listedStopped.recent.some((entry) => entry.target === primaryTarget),
      true,
    );

    await writeFile(opened.state_file, openedStateSnapshot, { mode: 0o600 });
    const listedStale = await invoke(["list"], environment);
    assert.equal(
      listedStale.offline.find((entry) => entry.target === primaryTarget)
        .offline_reason,
      "stale-state",
    );
    const staleCleanup = await invoke(["stop", primaryTarget], environment);
    assert.equal(staleCleanup.server_state, "already-stopped");
    const stoppedStatus = await invoke(["status", primaryTarget], environment);
    assert.equal(stoppedStatus.server_state, "stopped");
    checks.push(
      "truthful stop receipt under history failure and retained offline history",
    );

    const malformedStateId = "a".repeat(20);
    const symlinkedStateId = "b".repeat(20);
    await writeFile(
      path.join(stateDirectory, `${malformedStateId}.json`),
      "{not-json}\n",
    );
    await symlink(
      outsideFile,
      path.join(stateDirectory, `${symlinkedStateId}.json`),
    );
    const listedWithInvalidState = await invoke(["list"], environment);
    assert.equal(
      listedWithInvalidState.ignored_records.managed_state,
      2,
    );
    assert.doesNotMatch(
      JSON.stringify(listedWithInvalidState),
      /outside\n|not-json/,
    );
    const invalidLimit = await invokeBlocked(
      ["list", "--limit", "0"],
      environment,
    );
    assert.match(invalidLimit.error, /--limit must be an integer/);
    checks.push("malformed-state isolation and bounded list arguments");

    const validHistory = await readFile(historyFile, "utf8");
    await writeFile(historyFile, "{malformed-history}\n");
    const listedMalformedHistory = await invoke(["list"], environment);
    assert.equal(listedMalformedHistory.ignored_records.history, 1);
    assert.equal(listedMalformedHistory.counts.online, 2);
    await rm(historyFile);
    await symlink(outsideFile, historyFile);
    const listedSymlinkedHistory = await invoke(["list"], environment);
    assert.equal(listedSymlinkedHistory.ignored_records.history, 1);
    assert.equal(listedSymlinkedHistory.counts.online, 2);
    await rm(historyFile);
    await writeFile(historyFile, validHistory, { mode: 0o600 });
    checks.push("malformed and symlinked history isolation");

    const retentionRoot = path.join(fixtureRoot, "retention");
    await mkdir(retentionRoot, { recursive: true });
    const retentionTargets = [];
    for (let index = 0; index < 52; index += 1) {
      const target = path.join(
        retentionRoot,
        `retained-${String(index).padStart(2, "0")}.html`,
      );
      await writeFile(
        target,
        `<!doctype html><html><title>Retained ${index}</title></html>\n`,
      );
      retentionTargets.push(target);
      await invoke(["start", target], environment);
      await invoke(["stop", target], environment);
    }
    const listedRetention = await invoke(
      ["list", "--limit", "100"],
      environment,
    );
    assert.equal(listedRetention.counts.online, 2);
    assert.equal(listedRetention.counts.offline, 50);
    assert.equal(listedRetention.counts.known, 52);
    assert.equal(listedRetention.returned_counts.offline, 50);
    const listedDefaultLimit = await invoke(["list"], environment);
    assert.equal(listedDefaultLimit.counts.offline, 50);
    assert.equal(listedDefaultLimit.returned_counts.offline, 20);
    assert.equal(listedDefaultLimit.offline.length, 20);
    await rm(retentionTargets.at(-1));
    const listedMissingTarget = await invoke(
      ["list", "--limit", "100"],
      environment,
    );
    assert.equal(
      listedMissingTarget.offline.find(
        (entry) => entry.target === retentionTargets.at(-1),
      ).offline_reason,
      "target-missing",
    );
    checks.push("offline retention bound and missing-target classification");

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
