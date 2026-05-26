import { mkdir, rm, writeFile } from "node:fs/promises";
import { dirname, join, resolve } from "node:path";

import { MockAgentAdapter } from "./agent-adapter.ts";
import { evaluateWithDocker } from "./docker-evaluator.ts";
import type { EvidenceStatus, ScoreResult, TaskDefinition } from "./schemas.ts";
import { loadSweBenchSampleManifest } from "./swe-bench-provider.ts";

export interface BatchRunnerOptions {
  manifestPath: string;
  image: string;
  batchId?: string;
  projectRoot?: string;
  artifactsRoot?: string;
}

export interface BatchTaskReport {
  runId: string;
  taskId: string;
  status: ScoreResult["status"];
  evidencePath: string;
  scorePath: string;
  telemetryPath: string;
  oracleStatus?: EvidenceStatus;
}

export interface BatchReport {
  batchId: string;
  manifestPath: string;
  image: string;
  generatedAt: string;
  counts: Record<ScoreResult["status"], number>;
  tasks: BatchTaskReport[];
}

export async function runSampleBatch(options: BatchRunnerOptions): Promise<BatchReport> {
  const projectRoot = resolve(options.projectRoot ?? process.cwd());
  const artifactsRoot = resolve(projectRoot, options.artifactsRoot ?? "artifacts");
  const batchId = options.batchId ?? "sample-batch-001";
  const batchDir = join(artifactsRoot, batchId);
  const tasks = await loadSweBenchSampleManifest(options.manifestPath, projectRoot);
  const taskReports: BatchTaskReport[] = [];

  await mkdir(batchDir, { recursive: true });

  for (let index = 0; index < tasks.length; index += 1) {
    const task = tasks[index];
    const runId = `${batchId}-${String(index + 1).padStart(3, "0")}`;
    const runDir = join(artifactsRoot, runId);
    const telemetryPath = join(artifactsRoot, runId, "telemetry.jsonl");
    await rm(runDir, { recursive: true, force: true });
    await appendTelemetry(telemetryPath, runId, 0, "queued", "batch task queued");
    const agentResult = await new MockAgentAdapter({ patchArtifactPath: String(task.metadata?.patchPath) }).run({
      task,
      invocation: {
        runId,
        taskId: task.id,
        adapterId: "mock-agent",
        contextBudgetTokens: 2048,
        timeoutMs: 1000
      }
    });
    await appendTelemetry(telemetryPath, runId, 1, "invoking", "mock adapter produced patch result");

    try {
      await appendTelemetry(telemetryPath, runId, 2, "evaluating", "docker evaluator started");
      const evidence = await evaluateWithDocker({
        task,
        agentResult,
        runId,
        image: options.image,
        projectRoot,
        artifactsRoot
      });
      await appendTelemetry(telemetryPath, runId, 3, "scoring", "oracle evidence scored");
      const score = scoreTask(task, runId, evidence.status, evidence.exitCode, join(artifactsRoot, runId, "oracle-evidence.json"));
      const scorePath = join(artifactsRoot, runId, "score-result.json");
      await writeJson(scorePath, score);
      await appendTelemetry(telemetryPath, runId, 4, score.status === "pass" ? "completed" : "failed", `batch task ${score.status}`);
      taskReports.push({
        runId,
        taskId: task.id,
        status: score.status,
        oracleStatus: evidence.status,
        evidencePath: join(artifactsRoot, runId, "oracle-evidence.json"),
        scorePath,
        telemetryPath
      });
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      const score = infraScore(task, runId, message, join(artifactsRoot, runId, "score-result.json"));
      const scorePath = join(artifactsRoot, runId, "score-result.json");
      await writeJson(scorePath, score);
      await appendTelemetry(telemetryPath, runId, 2, "failed", message);
      taskReports.push({
        runId,
        taskId: task.id,
        status: "infra-fail",
        evidencePath: scorePath,
        scorePath,
        telemetryPath
      });
    }
  }

  const report: BatchReport = {
    batchId,
    manifestPath: options.manifestPath,
    image: options.image,
    generatedAt: new Date().toISOString(),
    counts: countStatuses(taskReports),
    tasks: taskReports
  };
  await writeJson(join(batchDir, "batch-report.json"), report);
  return report;
}

export function countStatuses(tasks: Pick<BatchTaskReport, "status">[]): Record<ScoreResult["status"], number> {
  return tasks.reduce(
    (counts, task) => {
      counts[task.status] += 1;
      return counts;
    },
    { pass: 0, fail: 0, "infra-fail": 0, quarantined: 0 }
  );
}

function scoreTask(
  task: TaskDefinition,
  runId: string,
  oracleStatus: EvidenceStatus,
  exitCode: number | null,
  evidencePath: string
): ScoreResult {
  const oraclePassed = oracleStatus === "pass" && exitCode === task.oracle.expectedExitCode;
  return {
    runId,
    taskId: task.id,
    status: oraclePassed ? "pass" : "fail",
    evidenceRef: evidencePath,
    components: {
      oraclePassed,
      expectedExitCode: task.oracle.expectedExitCode,
      actualExitCode: exitCode ?? -1
    }
  };
}

function infraScore(task: TaskDefinition, runId: string, message: string, evidencePath: string): ScoreResult {
  return {
    runId,
    taskId: task.id,
    status: "infra-fail",
    evidenceRef: evidencePath,
    components: {
      infraFailure: true,
      messageLength: message.length
    }
  };
}

async function appendTelemetry(
  path: string,
  runId: string,
  sequence: number,
  stage: string,
  message: string
): Promise<void> {
  await mkdir(dirname(path), { recursive: true });
  await writeFile(
    path,
    `${JSON.stringify({ runId, sequence, stage, message, timestamp: new Date().toISOString() })}\n`,
    { encoding: "utf8", flag: "a" }
  );
}

async function writeJson(path: string, value: unknown): Promise<void> {
  await mkdir(dirname(path), { recursive: true });
  await writeFile(path, `${JSON.stringify(value, null, 2)}\n`, "utf8");
}
