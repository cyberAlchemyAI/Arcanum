import { strict as assert } from "node:assert";
import test from "node:test";

import { loadSweBenchSampleManifest } from "../src/swe-bench-provider.ts";
import { validateTaskDefinition } from "../src/schemas.ts";

test("local SWE-bench sample manifest normalizes to valid docker tasks", async () => {
  const tasks = await loadSweBenchSampleManifest("fixtures/swe-bench-local-sample.json");

  assert.equal(tasks.length, 1);
  assert.equal(tasks[0]?.source.suite, "swe-bench-local-mirror");
  assert.equal(tasks[0]?.repository.kind, "docker");
  assert.equal(tasks[0]?.evaluatorProfile.kind, "docker");
  assert.deepEqual(validateTaskDefinition(tasks[0]), { ok: true, issues: [] });
  assert.equal(tasks[0]?.metadata?.patchPath, "fixtures/refactor-001.patch");
});
