import { MockAgentAdapter } from "./agent-adapter.ts";
import { evaluateWithDocker } from "./docker-evaluator.ts";
import { loadSweBenchSampleManifest } from "./swe-bench-provider.ts";
import type { AgentInvocation } from "./schemas.ts";

const image = process.env.BENCHMARK_DOCKER_IMAGE ?? "test-nestjs-app:latest";
const [task] = await loadSweBenchSampleManifest("fixtures/swe-bench-local-sample.json");

if (!task) {
  console.error("sample manifest produced no tasks");
  process.exit(1);
}

const runId = "docker-smoke-001";
const invocation: AgentInvocation = {
  runId,
  taskId: task.id,
  adapterId: "mock-agent",
  contextBudgetTokens: 2048,
  timeoutMs: 1000
};
const adapter = new MockAgentAdapter({ patchArtifactPath: String(task.metadata?.patchPath) });
const agentResult = await adapter.run({ task, invocation });
const evidence = await evaluateWithDocker({
  task,
  agentResult,
  runId,
  image
});

console.log(`${runId}: ${evidence.status} (${image})`);
console.log(`  evidence: artifacts/${runId}/oracle-evidence.json`);

if (evidence.status !== "pass") {
  process.exitCode = 1;
}
