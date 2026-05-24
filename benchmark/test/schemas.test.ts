import { strict as assert } from "node:assert";
import test from "node:test";

import { validateOracleEvidence, validateTaskDefinition } from "../src/schemas.ts";

const representativeTask = {
  id: "fixture.refactor.001",
  objective: "Refactor a local fixture without changing semantic behavior.",
  source: {
    suite: "local-fixture",
    upstreamId: "fixture-001"
  },
  repository: {
    kind: "fixture",
    fixturePath: "fixtures/refactor-001"
  },
  labels: ["refactor", "tech-debt"],
  oracle: {
    type: "semantic",
    command: "npm test",
    expectedExitCode: 0
  },
  evaluatorProfile: {
    kind: "fixture-local",
    timeoutMs: 30000
  },
  metadata: {
    sourceContract: "ARCHITECTURE.md"
  }
};

const representativeEvidence = {
  runId: "run-fixture-001",
  taskId: "fixture.refactor.001",
  oracleType: "semantic",
  status: "pass",
  command: "npm test",
  exitCode: 0,
  durationMs: 128,
  artifacts: {
    stdoutPath: "artifacts/run-fixture-001/stdout.log",
    stderrPath: "artifacts/run-fixture-001/stderr.log"
  },
  metrics: {
    testsPassed: 1
  }
};

test("representative task fixture validates", () => {
  const result = validateTaskDefinition(representativeTask);

  assert.deepEqual(result, { ok: true, issues: [] });
});

test("representative oracle evidence validates", () => {
  const result = validateOracleEvidence(representativeEvidence);

  assert.deepEqual(result, { ok: true, issues: [] });
});

test("invalid task fixture fails with useful issues", () => {
  const result = validateTaskDefinition({
    ...representativeTask,
    repository: { kind: "fixture" },
    oracle: { type: "unknown", command: "", expectedExitCode: "0" },
    evaluatorProfile: { kind: "fixture-local", timeoutMs: 0 }
  });

  assert.equal(result.ok, false);
  assert.match(result.issues.join("\n"), /repository\.fixturePath/);
  assert.match(result.issues.join("\n"), /oracle\.type/);
  assert.match(result.issues.join("\n"), /oracle\.command/);
  assert.match(result.issues.join("\n"), /oracle\.expectedExitCode/);
  assert.match(result.issues.join("\n"), /evaluatorProfile\.timeoutMs/);
});

test("invalid oracle evidence fails with useful issues", () => {
  const result = validateOracleEvidence({
    ...representativeEvidence,
    oracleType: "unknown",
    status: "maybe",
    durationMs: -1,
    artifacts: null
  });

  assert.equal(result.ok, false);
  assert.match(result.issues.join("\n"), /oracleType/);
  assert.match(result.issues.join("\n"), /status/);
  assert.match(result.issues.join("\n"), /durationMs/);
  assert.match(result.issues.join("\n"), /artifacts/);
});
