import { MockAgentAdapter } from "./agent-adapter.ts";
import { runBenchmarkKernel } from "./run-kernel.ts";
import type { AgentInvocation, TaskDefinition } from "./schemas.ts";

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

const runIds = ["kernel-smoke-001", "kernel-smoke-002"];
const statuses: string[] = [];

for (const runId of runIds) {
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
    adapter: new MockAgentAdapter({ patchArtifactPath: "fixtures/refactor-001.patch" })
  });
  statuses.push(attempt.scoreResult?.status ?? "missing-score");
  console.log(`${runId}: ${attempt.scoreResult?.status} (${attempt.oracleEvidence?.status ?? "no-evidence"})`);
  console.log(`  telemetry: artifacts/${runId}/telemetry.jsonl`);
}

if (statuses.some((status) => status !== "pass") || new Set(statuses).size !== 1) {
  process.exitCode = 1;
}
