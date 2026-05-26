import { mkdir, writeFile } from "node:fs/promises";
import { join } from "node:path";

import {
  DEFAULT_SWEBENCH_DATASET,
  assertInstanceInDataset,
  loadPredictionInputs,
  preflightOfficialSweBench,
  probeOfficialSweBenchDataset,
  runOfficialSweBenchEvaluation,
  writeOfficialSweBenchScore,
  writeSweBenchPredictionsJsonl
} from "./official-swebench.ts";

const runId = process.env.SWEBENCH_RUN_ID ?? "swebench-lite-official-smoke";
const sourcePath = process.env.SWEBENCH_PREDICTION_SOURCE ?? "fixtures/swebench-lite-agent-patches.json";
const runnerImage = process.env.SWEBENCH_RUNNER_IMAGE ?? "swebench-official-runner";
const predictionsPath = join("artifacts", runId, "predictions.jsonl");
const reportPath = join("artifacts", runId, "official-swebench-report.json");

await mkdir(join("artifacts", runId), { recursive: true });

const preflight = await preflightOfficialSweBench(runnerImage);
const report: Record<string, unknown> = {
  runId,
  datasetName: DEFAULT_SWEBENCH_DATASET,
  split: "test",
  runnerImage,
  predictionSource: sourcePath,
  predictionsPath,
  preflight,
  status: "blocked"
};
const blockers = [...preflight.blockers];
let instanceId = "unknown";

try {
  const predictions = await loadPredictionInputs(sourcePath);
  instanceId = predictions[0]?.instanceId ?? "unknown";
  await writeSweBenchPredictionsJsonl(predictions, predictionsPath);
} catch (error) {
  const message = error instanceof Error ? error.message : String(error);
  blockers.push(`missing or invalid instance-aligned patch source: ${message}`);
}

if (blockers.length > 0) {
  report.blockers = blockers;
  report.score = await writeOfficialSweBenchScore({
    runId,
    instanceId,
    datasetName: DEFAULT_SWEBENCH_DATASET,
    errorMessage: blockers.join("; ")
  });
  await writeReport(reportPath, report);
  console.error(`official SWE-bench smoke blocked: ${blockers.join("; ")}`);
  process.exit(2);
}

try {
  report.datasetProbe = await probeOfficialSweBenchDataset();
  await assertInstanceInDataset(instanceId, DEFAULT_SWEBENCH_DATASET, "test", runnerImage);
} catch (error) {
  const message = error instanceof Error ? error.message : String(error);
  report.blockers = [`failed to load real SWE-bench Lite metadata: ${message}`];
  report.score = await writeOfficialSweBenchScore({
    runId,
    instanceId,
    datasetName: DEFAULT_SWEBENCH_DATASET,
    errorMessage: message
  });
  await writeReport(reportPath, report);
  console.error(`official SWE-bench smoke blocked: ${message}`);
  process.exit(2);
}

const result = await runOfficialSweBenchEvaluation({
  predictionsPath,
  runId,
  datasetName: DEFAULT_SWEBENCH_DATASET,
  maxWorkers: 1
});
report.status = result.ok ? "pass" : "failed";
report.officialEvaluation = result;
report.score = await writeOfficialSweBenchScore({
  runId,
  instanceId,
  datasetName: DEFAULT_SWEBENCH_DATASET,
  errorMessage: result.ok ? undefined : `official evaluation exited with ${result.exitCode}`
});
await writeReport(reportPath, report);

if (!result.ok) {
  console.error(`official SWE-bench evaluation failed with exit code ${result.exitCode}`);
  process.exit(1);
}

console.log(`${runId}: official SWE-bench evaluation completed`);
console.log(`  report: ${reportPath}`);

async function writeReport(path: string, value: unknown): Promise<void> {
  await writeFile(path, `${JSON.stringify(value, null, 2)}\n`, "utf8");
}
