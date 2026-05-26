import { exec } from "node:child_process";
import { cp, mkdir, readFile, rm, writeFile } from "node:fs/promises";
import { dirname, isAbsolute, join, resolve } from "node:path";
import { promisify } from "node:util";

import type { AgentAdapter } from "./agent-adapter.ts";
import type {
  AgentInvocation,
  AgentResult,
  OracleEvidence,
  RunAttempt,
  RunStatus,
  ScoreResult,
  TaskDefinition,
  TelemetryEvent
} from "./schemas.ts";
import { validateTaskDefinition } from "./schemas.ts";

const execAsync = promisify(exec);

export interface RunKernelOptions {
  task: TaskDefinition;
  invocation: AgentInvocation;
  adapter: AgentAdapter;
  projectRoot?: string;
  artifactsRoot?: string;
}

export async function runBenchmarkKernel(options: RunKernelOptions): Promise<RunAttempt> {
  const projectRoot = resolve(options.projectRoot ?? process.cwd());
  const artifactsRoot = resolve(projectRoot, options.artifactsRoot ?? "artifacts");
  const runDir = join(artifactsRoot, options.invocation.runId);
  const telemetry = new TelemetryRecorder(options.invocation.runId, runDir);
  const attempt: RunAttempt = {
    runId: options.invocation.runId,
    task: options.task,
    invocation: options.invocation,
    telemetry: []
  };

  await rm(runDir, { recursive: true, force: true });
  await mkdir(runDir, { recursive: true });

  try {
    const taskValidation = validateTaskDefinition(options.task);
    if (!taskValidation.ok) {
      throw new KernelInfraError(`invalid task definition: ${taskValidation.issues.join("; ")}`);
    }
    if (options.task.repository.kind !== "fixture" || options.task.evaluatorProfile.kind !== "fixture-local") {
      throw new KernelInfraError("L0 run kernel only supports fixture repositories with fixture-local evaluators");
    }

    await record(telemetry, attempt, "queued", "run queued");
    await record(telemetry, attempt, "preparing", "fixture workspace prepared");
    const workspacePath = await prepareFixtureWorkspace(options.task, projectRoot, runDir);

    await record(telemetry, attempt, "invoking", "agent adapter invoked");
    const agentResult = await options.adapter.run({ task: options.task, invocation: options.invocation });
    attempt.agentResult = agentResult;
    await writeJson(join(runDir, "agent-result.json"), agentResult);

    if (agentResult.status !== "patch" || !agentResult.patchArtifactPath) {
      const scoreResult = scoreAgentFailure(options.task, agentResult, runDir);
      attempt.scoreResult = scoreResult;
      await writeJson(join(runDir, "score-result.json"), scoreResult);
      await record(telemetry, attempt, "failed", `agent returned ${agentResult.status}`);
      return attempt;
    }

    await record(telemetry, attempt, "applying-patch", "patch artifact persisted and applied");
    const patchPath = await persistPatchArtifact(agentResult, projectRoot, runDir);
    const applyResult = await runCommand(`patch --batch -p1 -i "${patchPath}"`, workspacePath, options.task.evaluatorProfile.timeoutMs);
    if (applyResult.exitCode !== 0) {
      const evidence = await makeEvidence(options.task, options.invocation.runId, "fail", "patch", applyResult, runDir);
      const scoreResult = scoreEvidence(options.task, evidence, join(runDir, "oracle-evidence.json"), {
        patchApplied: false,
        agentFailure: true
      });
      attempt.oracleEvidence = evidence;
      attempt.scoreResult = scoreResult;
      await writeJson(join(runDir, "oracle-evidence.json"), evidence);
      await writeJson(join(runDir, "score-result.json"), scoreResult);
      await record(telemetry, attempt, "failed", "patch application failed");
      return attempt;
    }

    await record(telemetry, attempt, "evaluating", "oracle command executed");
    const oracleResult = await runCommand(options.task.oracle.command, workspacePath, options.task.evaluatorProfile.timeoutMs);
    const evidenceStatus = oracleResult.timedOut
      ? "timeout"
      : oracleResult.exitCode === options.task.oracle.expectedExitCode
        ? "pass"
        : "fail";
    const evidence = await makeEvidence(
      options.task,
      options.invocation.runId,
      evidenceStatus,
      options.task.oracle.command,
      oracleResult,
      runDir
    );
    attempt.oracleEvidence = evidence;
    await writeJson(join(runDir, "oracle-evidence.json"), evidence);

    await record(telemetry, attempt, "scoring", "oracle evidence scored");
    const scoreResult = scoreEvidence(options.task, evidence, join(runDir, "oracle-evidence.json"), {
      patchApplied: true,
      agentFailure: false
    });
    attempt.scoreResult = scoreResult;
    await writeJson(join(runDir, "score-result.json"), scoreResult);

    await record(telemetry, attempt, scoreResult.status === "pass" ? "completed" : "failed", `run ${scoreResult.status}`);
    return attempt;
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    const scoreResult = scoreInfraFailure(options.task, options.invocation.runId, message, runDir);
    attempt.scoreResult = scoreResult;
    await writeJson(join(runDir, "score-result.json"), scoreResult);
    await record(telemetry, attempt, "failed", message);
    return attempt;
  }
}

async function prepareFixtureWorkspace(task: TaskDefinition, projectRoot: string, runDir: string): Promise<string> {
  const fixturePath = task.repository.fixturePath;
  if (!fixturePath) {
    throw new KernelInfraError("fixture task is missing repository.fixturePath");
  }
  const sourcePath = resolve(projectRoot, fixturePath);
  const workspacePath = join(runDir, "workspace");
  await cp(sourcePath, workspacePath, { recursive: true });
  return workspacePath;
}

async function persistPatchArtifact(agentResult: AgentResult, projectRoot: string, runDir: string): Promise<string> {
  if (!agentResult.patchArtifactPath) {
    throw new KernelInfraError("patch result is missing patchArtifactPath");
  }
  const sourcePatchPath = isAbsolute(agentResult.patchArtifactPath)
    ? agentResult.patchArtifactPath
    : resolve(projectRoot, agentResult.patchArtifactPath);
  const targetPatchPath = join(runDir, "patch.diff");
  const patch = await readFile(sourcePatchPath, "utf8");
  await writeFile(targetPatchPath, patch, "utf8");
  return targetPatchPath;
}

async function runCommand(command: string, cwd: string, timeoutMs: number): Promise<CommandResult> {
  const startedAt = Date.now();
  try {
    const result = await execAsync(command, { cwd, timeout: timeoutMs, windowsHide: true });
    return {
      command,
      exitCode: 0,
      stdout: result.stdout,
      stderr: result.stderr,
      durationMs: Math.max(1, Date.now() - startedAt),
      timedOut: false
    };
  } catch (error) {
    const commandError = error as Partial<NodeJS.ErrnoException> & {
      code?: number | string;
      stdout?: string;
      stderr?: string;
      killed?: boolean;
      signal?: NodeJS.Signals;
    };
    return {
      command,
      exitCode: typeof commandError.code === "number" ? commandError.code : null,
      stdout: commandError.stdout ?? "",
      stderr: commandError.stderr ?? (commandError.message ?? ""),
      durationMs: Math.max(1, Date.now() - startedAt),
      timedOut: commandError.killed === true || commandError.signal === "SIGTERM"
    };
  }
}

async function makeEvidence(
  task: TaskDefinition,
  runId: string,
  status: OracleEvidence["status"],
  command: string,
  result: CommandResult,
  runDir: string
): Promise<OracleEvidence> {
  const stdoutPath = join(runDir, "stdout.log");
  const stderrPath = join(runDir, "stderr.log");
  await writeFile(stdoutPath, result.stdout, "utf8");
  await writeFile(stderrPath, result.stderr, "utf8");
  return {
    runId,
    taskId: task.id,
    oracleType: task.oracle.type,
    status,
    command,
    exitCode: result.exitCode,
    durationMs: result.durationMs,
    artifacts: {
      stdoutPath,
      stderrPath
    },
    metrics: {
      expectedExitCode: task.oracle.expectedExitCode,
      actualExitCode: result.exitCode ?? -1
    }
  };
}

function scoreEvidence(
  task: TaskDefinition,
  evidence: OracleEvidence,
  evidencePath: string,
  components: Record<string, number | boolean>
): ScoreResult {
  const oraclePassed = evidence.status === "pass" && evidence.exitCode === task.oracle.expectedExitCode;
  return {
    runId: evidence.runId,
    taskId: task.id,
    status: evidence.status === "timeout" ? "fail" : oraclePassed ? "pass" : "fail",
    evidenceRef: evidencePath,
    components: {
      oraclePassed,
      expectedExitCode: task.oracle.expectedExitCode,
      actualExitCode: evidence.exitCode ?? -1,
      ...components
    }
  };
}

function scoreAgentFailure(task: TaskDefinition, agentResult: AgentResult, runDir: string): ScoreResult {
  return {
    runId: agentResult.runId,
    taskId: task.id,
    status: "fail",
    evidenceRef: join(runDir, "agent-result.json"),
    components: {
      agentFailure: true,
      patchProduced: false
    }
  };
}

function scoreInfraFailure(task: TaskDefinition, runId: string, message: string, runDir: string): ScoreResult {
  return {
    runId,
    taskId: task.id,
    status: "infra-fail",
    evidenceRef: join(runDir, "score-result.json"),
    components: {
      infraFailure: true,
      messageLength: message.length
    }
  };
}

async function record(
  recorder: TelemetryRecorder,
  attempt: RunAttempt,
  stage: RunStatus,
  message: string
): Promise<void> {
  const event = await recorder.append(stage, message);
  attempt.telemetry.push(event);
}

async function writeJson(path: string, value: unknown): Promise<void> {
  await mkdir(dirname(path), { recursive: true });
  await writeFile(path, `${JSON.stringify(value, null, 2)}\n`, "utf8");
}

class TelemetryRecorder {
  private readonly runId: string;
  private readonly runDir: string;
  private sequence = 0;

  constructor(runId: string, runDir: string) {
    this.runId = runId;
    this.runDir = runDir;
  }

  async append(stage: RunStatus, message: string): Promise<TelemetryEvent> {
    const event = {
      runId: this.runId,
      sequence: this.sequence++,
      stage,
      message,
      timestamp: new Date().toISOString()
    };
    await mkdir(this.runDir, { recursive: true });
    await writeFile(join(this.runDir, "telemetry.jsonl"), `${JSON.stringify(event)}\n`, {
      encoding: "utf8",
      flag: "a"
    });
    return event;
  }
}

class KernelInfraError extends Error {}

interface CommandResult {
  command: string;
  exitCode: number | null;
  stdout: string;
  stderr: string;
  durationMs: number;
  timedOut: boolean;
}
