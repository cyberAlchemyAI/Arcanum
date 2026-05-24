import { strict as assert } from "node:assert";
import test from "node:test";

import { MockAgentAdapter } from "../src/agent-adapter.ts";
import type { AgentInvocation, TaskDefinition } from "../src/schemas.ts";

const task: TaskDefinition = {
  id: "fixture.refactor.001",
  objective: "Refactor a local fixture without changing semantic behavior.",
  source: {
    suite: "local-fixture"
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
  }
};

const invocation: AgentInvocation = {
  runId: "run-fixture-001",
  taskId: task.id,
  adapterId: "mock-agent",
  contextBudgetTokens: 2048,
  timeoutMs: 1000
};

test("mock adapter returns a typed patch result", async () => {
  const adapter = new MockAgentAdapter({ patchArtifactPath: "artifacts/run-fixture-001/patch.diff" });

  const result = await adapter.run({ task, invocation });

  assert.deepEqual(result, {
    runId: "run-fixture-001",
    taskId: "fixture.refactor.001",
    status: "patch",
    patchArtifactPath: "artifacts/run-fixture-001/patch.diff"
  });
});

test("mock adapter returns no-patch state", async () => {
  const adapter = new MockAgentAdapter({ mode: "no-patch" });

  const result = await adapter.run({ task, invocation });

  assert.deepEqual(result, {
    runId: "run-fixture-001",
    taskId: "fixture.refactor.001",
    status: "no-patch"
  });
});

test("mock adapter returns error state", async () => {
  const adapter = new MockAgentAdapter({ mode: "error", errorMessage: "planned failure" });

  const result = await adapter.run({ task, invocation });

  assert.deepEqual(result, {
    runId: "run-fixture-001",
    taskId: "fixture.refactor.001",
    status: "error",
    errorMessage: "planned failure"
  });
});

test("mock adapter returns timeout state", async () => {
  const adapter = new MockAgentAdapter({ mode: "timeout" });

  const result = await adapter.run({ task, invocation });

  assert.deepEqual(result, {
    runId: "run-fixture-001",
    taskId: "fixture.refactor.001",
    status: "timeout",
    errorMessage: "mock adapter timeout"
  });
});
