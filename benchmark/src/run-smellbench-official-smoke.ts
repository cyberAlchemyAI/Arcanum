import { mkdir, writeFile } from "node:fs/promises";
import { join } from "node:path";

import {
  DEFAULT_SMELLBENCH_DATASET,
  DEFAULT_SMELLBENCH_RUN_ID,
  loadSmellBenchCandidateManifest,
  materializeSmellBenchCandidateManifest,
  runOfficialSmellBenchSmoke,
  writeSmellBenchOracleEvidence,
  writeSmellBenchScore
} from "./smellbench.ts";

const runId = process.env.SMELLBENCH_RUN_ID ?? DEFAULT_SMELLBENCH_RUN_ID;
const sourcePath = process.env.SMELLBENCH_CANDIDATE_SOURCE ?? "fixtures/smellbench-agent-patches.json";
const reportPath = join("artifacts", runId, "official-smellbench-report.json");

await mkdir(join("artifacts", runId), { recursive: true });

const report: Record<string, unknown> = {
  runId,
  datasetName: DEFAULT_SMELLBENCH_DATASET,
  candidateSource: sourcePath,
  status: "blocked"
};

let taskId = "unknown";
let candidateManifestPath: string | undefined;

try {
  const candidates = await loadSmellBenchCandidateManifest(sourcePath);
  taskId = candidates[0]?.taskId ?? "unknown";
  candidateManifestPath = await materializeSmellBenchCandidateManifest({ candidates, runId });
  report.candidateManifestPath = candidateManifestPath;

  const result = await runOfficialSmellBenchSmoke({ candidates, runId });
  report.status = result.ok ? "pass" : "failed";
  report.upstreamEvaluation = result;
  const score = await writeSmellBenchScore({
    runId,
    taskId,
    upstreamResultsDir: result.upstreamResultsDir,
    candidateManifestPath,
    errorMessage: result.ok ? undefined : `SmellBench evaluator exited with ${result.exitCode}`
  });
  report.score = score;
  report.oracleEvidencePath = await writeSmellBenchOracleEvidence({ runId, score });
  await writeReport(reportPath, report);

  if (!result.ok || score.status === "infra-fail") {
    console.error(`SmellBench official smoke did not produce accepted plumbing proof: ${score.status}`);
    process.exit(1);
  }

  console.log(`${runId}: SmellBench evaluator completed with score status ${score.status}`);
  console.log(`  report: ${reportPath}`);
} catch (error) {
  const message = error instanceof Error ? error.message : String(error);
  report.status = "blocked";
  report.blockers = [message];
  report.score = await writeSmellBenchScore({
    runId,
    taskId,
    candidateManifestPath,
    errorMessage: message
  });
  await writeReport(reportPath, report);
  console.error(`SmellBench official smoke blocked: ${message}`);
  process.exit(2);
}

async function writeReport(path: string, value: unknown): Promise<void> {
  await writeFile(path, `${JSON.stringify(value, null, 2)}\n`, "utf8");
}
