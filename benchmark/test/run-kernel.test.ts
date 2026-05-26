import { strict as assert } from "node:assert";
import { mkdtemp } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";

import { MockAgentAdapter } from "../src/agent-adapter.ts";
import { runBenchmarkKernel } from "../src/run-kernel.ts";
import type { AgentInvocation, TaskDefinition } from "../src/schemas.ts";

const task: TaskDefinition = {
  id: "fixture.refactor.001",
  objective: "Apply the fixture patch and preserve calculator behavior.",
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
  }
};

test("fixture-local kernel applies and scores the same patch twice from clean state", async () => {
  const artifactsRoot = await mkdtemp(join(tmpdir(), "benchmark-kernel-"));
  const statuses: string[] = [];

  for (const runId of ["run-fixture-001", "run-fixture-002"]) {
    const invocation: AgentInvocation = {
      runId,
      taskId: task.id,
      adapterId: "mock-agent",
      contextBudgetTokens: 2048,
      timeoutMs: 1000
    };

    const attempt = await runBenchmarkKernel({
      task,
      invocation,
      adapter: new MockAgentAdapter({ patchArtifactPath: "fixtures/refactor-001.patch" }),
      artifactsRoot
    });

    statuses.push(attempt.scoreResult?.status ?? "missing-score");
    assert.equal(attempt.agentResult?.status, "patch");
    assert.equal(attempt.oracleEvidence?.status, "pass");
    assert.equal(attempt.scoreResult?.status, "pass");
    assert.deepEqual(
      attempt.telemetry.map((event) => event.stage),
      ["queued", "preparing", "invoking", "applying-patch", "evaluating", "scoring", "completed"]
    );
    assert.match(attempt.scoreResult?.evidenceRef ?? "", /oracle-evidence\.json$/);
    assert.ok(attempt.oracleEvidence?.artifacts.stdoutPath);
    assert.ok(attempt.oracleEvidence?.artifacts.stderrPath);
  }

  assert.deepEqual(statuses, ["pass", "pass"]);
});
