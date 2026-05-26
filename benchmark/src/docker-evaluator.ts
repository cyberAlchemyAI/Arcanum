import { execFile } from "node:child_process";
import { cp, mkdir, readFile, rm, writeFile } from "node:fs/promises";
import { dirname, isAbsolute, join, resolve } from "node:path";
import { promisify } from "node:util";

import type { AgentResult, OracleEvidence, TaskDefinition } from "./schemas.ts";

const execFileAsync = promisify(execFile);

export interface DockerEvaluatorOptions {
  task: TaskDefinition;
  agentResult: AgentResult;
  runId: string;
  image: string;
  projectRoot?: string;
  artifactsRoot?: string;
}

export async function evaluateWithDocker(options: DockerEvaluatorOptions): Promise<OracleEvidence> {
  const projectRoot = resolve(options.projectRoot ?? process.cwd());
  const artifactsRoot = resolve(projectRoot, options.artifactsRoot ?? "artifacts");
  const runDir = join(artifactsRoot, options.runId);
  const workspacePath = join(runDir, "workspace");
  const patchPath = join(runDir, "patch.diff");
  const runnerPath = join(runDir, "docker-runner.mjs");

  await mkdir(runDir, { recursive: true });
  await rm(workspacePath, { recursive: true, force: true });

  const fixturePath = readFixturePath(options.task);
  const sourcePath = resolve(projectRoot, fixturePath);
  await cp(sourcePath, workspacePath, { recursive: true });
  await persistPatch(options.agentResult, projectRoot, patchPath);
  await writeFile(runnerPath, dockerRunnerSource, "utf8");

  const startedAt = Date.now();
  const args = [
    "run",
    "--rm",
    "--network",
    "none",
    "--user",
    "0:0",
    "-v",
    `${workspacePath}:/workspace`,
    "-v",
    `${patchPath}:/patch.diff:ro`,
    "-v",
    `${runnerPath}:/runner.mjs:ro`,
    "-w",
    "/workspace",
    options.image,
    "node",
    "/runner.mjs",
    "/patch.diff",
    options.task.oracle.command
  ];

  const result = await runDocker(args, options.task.evaluatorProfile.timeoutMs);
  const stdoutPath = join(runDir, "stdout.log");
  const stderrPath = join(runDir, "stderr.log");
  await writeFile(stdoutPath, result.stdout, "utf8");
  await writeFile(stderrPath, result.stderr, "utf8");

  const status = result.timedOut
    ? "timeout"
    : result.exitCode === options.task.oracle.expectedExitCode
      ? "pass"
      : "fail";

  const evidence: OracleEvidence = {
    runId: options.runId,
    taskId: options.task.id,
    oracleType: options.task.oracle.type,
    status,
    command: options.task.oracle.command,
    exitCode: result.exitCode,
    durationMs: Math.max(1, Date.now() - startedAt),
    artifacts: {
      stdoutPath,
      stderrPath
    },
    metrics: {
      expectedExitCode: options.task.oracle.expectedExitCode,
      actualExitCode: result.exitCode ?? -1
    }
  };
  await writeFile(join(runDir, "oracle-evidence.json"), `${JSON.stringify(evidence, null, 2)}\n`, "utf8");
  return evidence;
}

function readFixturePath(task: TaskDefinition): string {
  const fixturePath = task.repository.fixturePath ?? readStringMetadata(task, "fixturePath");
  if (!fixturePath) {
    throw new Error("docker evaluator requires repository.fixturePath or metadata.fixturePath");
  }
  return fixturePath;
}

async function persistPatch(agentResult: AgentResult, projectRoot: string, targetPatchPath: string): Promise<void> {
  if (agentResult.status !== "patch" || !agentResult.patchArtifactPath) {
    throw new Error("docker evaluator requires a patch agent result");
  }
  const sourcePatchPath = isAbsolute(agentResult.patchArtifactPath)
    ? agentResult.patchArtifactPath
    : resolve(projectRoot, agentResult.patchArtifactPath);
  await mkdir(dirname(targetPatchPath), { recursive: true });
  await writeFile(targetPatchPath, await readFile(sourcePatchPath, "utf8"), "utf8");
}

async function runDocker(args: string[], timeoutMs: number): Promise<DockerCommandResult> {
  try {
    const result = await execFileAsync("docker", args, { timeout: timeoutMs });
    return {
      exitCode: 0,
      stdout: result.stdout,
      stderr: result.stderr,
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
      exitCode: typeof commandError.code === "number" ? commandError.code : null,
      stdout: commandError.stdout ?? "",
      stderr: commandError.stderr ?? commandError.message ?? "",
      timedOut: commandError.killed === true || commandError.signal === "SIGTERM"
    };
  }
}

function readStringMetadata(task: TaskDefinition, key: string): string | null {
  const value = task.metadata?.[key];
  return typeof value === "string" && value.length > 0 ? value : null;
}

const dockerRunnerSource = String.raw`
import { exec } from "node:child_process";
import { readFileSync, writeFileSync } from "node:fs";
import { promisify } from "node:util";

const execAsync = promisify(exec);
const [patchPath, oracleCommand] = process.argv.slice(2);

if (!patchPath || !oracleCommand) {
  console.error("usage: node runner.mjs <patch> <oracle-command>");
  process.exit(97);
}

const patch = readFileSync(patchPath, "utf8");
applyUnifiedPatch(patch);
const result = await runOracle(oracleCommand);
process.stdout.write(result.stdout);
process.stderr.write(result.stderr);
process.exit(result.exitCode ?? 1);

function applyUnifiedPatch(patchText) {
  const lines = patchText.split(/\r?\n/);
  let targetPath = null;
  for (const line of lines) {
    if (line.startsWith("+++ b/")) {
      targetPath = line.slice("+++ b/".length);
      break;
    }
  }
  if (!targetPath) {
    throw new Error("patch target not found");
  }

  const removeLines = [];
  const addLines = [];
  for (const line of lines) {
    if (line.startsWith("---") || line.startsWith("+++") || line.startsWith("@@") || line.startsWith("diff ") || line.startsWith("index ")) {
      continue;
    }
    if (line.startsWith("-")) {
      removeLines.push(line.slice(1));
    } else if (line.startsWith("+")) {
      addLines.push(line.slice(1));
    }
  }

  const current = readFileSync(targetPath, "utf8");
  const before = removeLines.join("\n");
  const after = addLines.join("\n");
  if (!current.includes(before)) {
    throw new Error("patch context not found in " + targetPath);
  }
  writeFileSync(targetPath, current.replace(before, after), "utf8");
}

async function runOracle(command) {
  try {
    const result = await execAsync(command);
    return { exitCode: 0, stdout: result.stdout, stderr: result.stderr };
  } catch (error) {
    return {
      exitCode: typeof error.code === "number" ? error.code : 1,
      stdout: error.stdout ?? "",
      stderr: error.stderr ?? error.message ?? ""
    };
  }
}
`;

interface DockerCommandResult {
  exitCode: number | null;
  stdout: string;
  stderr: string;
  timedOut: boolean;
}
