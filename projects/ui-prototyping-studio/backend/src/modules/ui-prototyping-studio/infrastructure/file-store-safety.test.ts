import assert from "node:assert/strict";
import { mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { test } from "node:test";

import { createFileBackedStudioSessionStore } from "./file-studio-session-store.js";

// N10 (F12): a present-but-corrupt data file must FAIL LOUD, never silently reset to empty (data-loss guard).

test("N10: a corrupt data file throws instead of silently resetting to empty", () => {
  const dir = mkdtempSync(join(tmpdir(), "ups-corrupt-"));
  const file = join(dir, "studio.json");
  try {
    writeFileSync(file, "{ this is not json", "utf8");
    assert.throws(
      () => createFileBackedStudioSessionStore({ filePath: file }),
      /not valid JSON|data-loss guard/i,
    );
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test("N10: an ABSENT file still starts fresh (no false alarm)", () => {
  const dir = mkdtempSync(join(tmpdir(), "ups-fresh-"));
  try {
    const store = createFileBackedStudioSessionStore({ filePath: join(dir, "studio.json") });
    assert.ok(store.allocateSessionId().startsWith("ups-session-"));
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});
