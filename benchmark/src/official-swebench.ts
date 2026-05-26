import { execFile } from "node:child_process";
import { copyFile, cp, mkdir, readdir, readFile, stat, writeFile } from "node:fs/promises";
import { basename, dirname, join, relative, resolve } from "node:path";
import { promisify } from "node:util";

const execFileAsync = promisify(execFile);

export const DEFAULT_SWEBENCH_DATASET = "princeton-nlp/SWE-bench_Lite";
export const DEFAULT_SWEBENCH_SPLIT = "test";

export interface SweBenchPredictionInput {
  instanceId: string;
  modelNameOrPath: string;
  modelPatch?: string;
  patchArtifactPath?: string;
}

export interface SweBenchLiteInstanceMetadata {
  instance_id: string;
  repo: string;
  base_commit: string;
  problem_statement: string;
  [key: string]: unknown;
}

export interface SweBenchAgentSmokePrepareResult {
  instance: SweBenchLiteInstanceMetadata;
  artifactDir: string;
  checkoutDir: string;
  taskBriefPath: string;
  metadataPath: string;
  patchArtifactPath: string;
  manifestPath?: string;
}

export interface SweBenchPreflightResult {
  ok: boolean;
  docker: {
    ok: boolean;
    version?: string;
    daemonOk: boolean;
    daemonVersion?: string;
  };
  runner: {
    image: string;
    ok: boolean;
    pythonVersion?: string;
  };
  modules: {
    swebench: boolean;
    datasets: boolean;
  };
  warnings: string[];
  blockers: string[];
}

export interface OfficialSweBenchRunOptions {
  predictionsPath: string;
  runId: string;
  datasetName?: string;
  split?: string;
  maxWorkers?: number;
  runnerImage?: string;
  artifactsRoot?: string;
  projectRoot?: string;
}

export interface OfficialSweBenchDatasetProbe {
  datasetName: string;
  split: string;
  fields: string[];
  selectedInstanceIds: string[];
  totalRows: number;
}

export interface OfficialSweBenchRunResult {
  ok: boolean;
  command: string[];
  runId: string;
  datasetName: string;
  resultsDir: string;
  importedResultsDir?: string;
  stdout: string;
  stderr: string;
  exitCode: number | null;
}

export interface OfficialSweBenchScoreResult {
  status: "pass" | "fail" | "infra-fail";
  resolved: boolean | null;
  instanceId: string;
  datasetName: string;
  runId: string;
  officialResultsRef?: string;
  instanceResultsRef?: string;
  logsRef?: string;
  errorMessage?: string;
}

export async function writeSweBenchAgentPatchManifest(
  predictions: SweBenchPredictionInput[],
  outputPath = "fixtures/swebench-lite-agent-patches.json",
  projectRoot = process.cwd()
): Promise<void> {
  if (predictions.length === 0) {
    throw new Error("agent patch manifest requires at least one prediction entry");
  }
  for (const prediction of predictions) {
    if (!prediction.patchArtifactPath && !prediction.modelPatch) {
      throw new Error(`prediction ${prediction.instanceId} is missing modelPatch or patchArtifactPath`);
    }
    if (prediction.patchArtifactPath) {
      await assertNonEmptyPatchArtifact(prediction.patchArtifactPath, projectRoot);
    } else if (!prediction.modelPatch?.trim()) {
      throw new Error(`prediction ${prediction.instanceId} has an empty modelPatch`);
    }
  }
  const targetPath = resolve(projectRoot, outputPath);
  await mkdir(dirname(targetPath), { recursive: true });
  await writeFile(targetPath, `${JSON.stringify(predictions, null, 2)}\n`, "utf8");
}

export async function prepareSweBenchLiteAgentSmoke(options: {
  instanceId: string;
  runnerImage?: string;
  datasetName?: string;
  split?: string;
  projectRoot?: string;
  artifactsRoot?: string;
  manifestPath?: string;
  writeManifest?: boolean;
  modelNameOrPath?: string;
}): Promise<SweBenchAgentSmokePrepareResult> {
  const projectRoot = resolve(options.projectRoot ?? process.cwd());
  const artifactsRoot = resolve(projectRoot, options.artifactsRoot ?? "artifacts");
  const runnerImage = options.runnerImage ?? "swebench-official-runner";
  const datasetName = options.datasetName ?? DEFAULT_SWEBENCH_DATASET;
  const split = options.split ?? DEFAULT_SWEBENCH_SPLIT;
  const instance = await loadSweBenchLiteInstance(options.instanceId, datasetName, split, runnerImage, projectRoot);
  const artifactDir = join(artifactsRoot, "swebench-lite-agent-smoke", instance.instance_id);
  const checkoutDir = join(artifactDir, "repo");
  const taskBriefPath = join(artifactDir, "TASK.md");
  const metadataPath = join(artifactDir, "instance-metadata.json");
  const patchArtifactPath = join(artifactDir, "patch.diff");

  await mkdir(artifactDir, { recursive: true });
  await writeFile(metadataPath, `${JSON.stringify(redactInstanceForAgentArtifact(instance), null, 2)}\n`, "utf8");
  await writeFile(taskBriefPath, renderAgentTaskBrief(instance, patchArtifactPath, datasetName, split), "utf8");
  await ensureRepoCheckout(instance.repo, instance.base_commit, checkoutDir, projectRoot);

  if (options.writeManifest) {
    await writeSweBenchAgentPatchManifest(
      [
        {
          instanceId: instance.instance_id,
          modelNameOrPath: options.modelNameOrPath ?? "codex-local-smoke",
          patchArtifactPath: relative(projectRoot, patchArtifactPath)
        }
      ],
      options.manifestPath,
      projectRoot
    );
  }

  return {
    instance,
    artifactDir,
    checkoutDir,
    taskBriefPath,
    metadataPath,
    patchArtifactPath,
    manifestPath: options.writeManifest ? resolve(projectRoot, options.manifestPath ?? "fixtures/swebench-lite-agent-patches.json") : undefined
  };
}

export async function writeSweBenchPredictionsJsonl(
  predictions: SweBenchPredictionInput[],
  outputPath: string,
  projectRoot = process.cwd()
): Promise<void> {
  if (predictions.length === 0) {
    throw new Error("SWE-bench prediction JSONL requires at least one instance-aligned patch");
  }

  const lines = [];
  for (const prediction of predictions) {
    const modelPatch = await resolvePatch(prediction, projectRoot);
    lines.push(
      JSON.stringify({
        instance_id: prediction.instanceId,
        model_name_or_path: prediction.modelNameOrPath,
        model_patch: modelPatch
      })
    );
  }

  await mkdir(dirname(outputPath), { recursive: true });
  await writeFile(outputPath, `${lines.join("\n")}\n`, "utf8");
}

export async function loadPredictionInputs(path: string, projectRoot = process.cwd()): Promise<SweBenchPredictionInput[]> {
  const content = await readFile(resolve(projectRoot, path), "utf8");
  const parsed = JSON.parse(content) as unknown;
  if (!Array.isArray(parsed)) {
    throw new Error("SWE-bench prediction source must be a JSON array");
  }
  return parsed.map(readPredictionInput);
}

export async function preflightOfficialSweBench(runnerImage = "swebench-official-runner"): Promise<SweBenchPreflightResult> {
  const warnings = [
    "Official SWE-bench Docker evaluation can require substantial disk and memory; SWE-bench docs call out large Docker cache/storage requirements."
  ];
  const blockers: string[] = [];
  const docker = await runVersion("docker", ["--version"]);
  const dockerDaemon = await runDockerDaemonProbe();
  const runner = await probeRunnerImage(runnerImage);
  const modules = runner.ok ? await probeRunnerModules(runnerImage) : { swebench: false, datasets: false };

  if (!docker.ok) {
    blockers.push("Docker CLI is not available");
  }
  if (!dockerDaemon.ok) {
    blockers.push("Docker daemon is not accessible");
  }
  if (!runner.ok) {
    blockers.push(`Docker runner image is not available or not runnable: ${runnerImage}`);
  }
  if (!modules.swebench) {
    blockers.push(`Python module swebench is not installed or not importable in ${runnerImage}`);
  }
  if (!modules.datasets) {
    blockers.push(`Python module datasets is not installed or not importable in ${runnerImage}`);
  }

  return {
    ok: blockers.length === 0,
    docker: {
      ok: docker.ok,
      version: docker.output,
      daemonOk: dockerDaemon.ok,
      daemonVersion: dockerDaemon.output
    },
    runner,
    modules,
    warnings,
    blockers
  };
}

export async function runOfficialSweBenchEvaluation(
  options: OfficialSweBenchRunOptions
): Promise<OfficialSweBenchRunResult> {
  const projectRoot = resolve(options.projectRoot ?? process.cwd());
  const artifactsRoot = resolve(projectRoot, options.artifactsRoot ?? "artifacts");
  const datasetName = options.datasetName ?? DEFAULT_SWEBENCH_DATASET;
  const split = options.split ?? DEFAULT_SWEBENCH_SPLIT;
  const runnerImage = options.runnerImage ?? "swebench-official-runner";
  const maxWorkers = String(options.maxWorkers ?? 1);
  const resultsDir = resolve(projectRoot, "evaluation_results", options.runId);
  const importedResultsDir = join(artifactsRoot, options.runId, "official-evaluation-results");
  const harnessCommand = [
    "python",
    "-m",
    "swebench.harness.run_evaluation",
    "--dataset_name",
    datasetName,
    "--split",
    split,
    "--predictions_path",
    `/workspace/${options.predictionsPath}`,
    "--max_workers",
    maxWorkers,
    "--run_id",
    options.runId
  ];
  const command = [
    "run",
    "--rm",
    "-v",
    `${projectRoot}:/workspace`,
    "-v",
    "/var/run/docker.sock:/var/run/docker.sock",
    "-w",
    "/workspace",
    runnerImage,
    ...harnessCommand
  ];

  const started = await runProcess("docker", command, projectRoot);
  if (started.exitCode === 0) {
    await importOfficialRunArtifacts({
      projectRoot,
      resultsDir,
      importedResultsDir,
      runId: options.runId,
      stdout: started.stdout
    });
  }

  return {
    ok: started.exitCode === 0,
    command: ["docker", ...command],
    runId: options.runId,
    datasetName,
    resultsDir,
    importedResultsDir: started.exitCode === 0 ? importedResultsDir : undefined,
    stdout: started.stdout,
    stderr: started.stderr,
    exitCode: started.exitCode
  };
}

export async function probeOfficialSweBenchDataset(
  datasetName = DEFAULT_SWEBENCH_DATASET,
  split = DEFAULT_SWEBENCH_SPLIT,
  runnerImage = "swebench-official-runner",
  sampleSize = 1
): Promise<OfficialSweBenchDatasetProbe> {
  const script = [
    "import json",
    "from datasets import load_dataset",
    "ds = load_dataset(" + JSON.stringify(datasetName) + ", split=" + JSON.stringify(split) + ")",
    "rows = [ds[i] for i in range(min(" + String(sampleSize) + ", len(ds)))]",
    "print(json.dumps({'datasetName': " + JSON.stringify(datasetName) + ", 'split': " + JSON.stringify(split) + ", 'fields': list(ds.features.keys()), 'selectedInstanceIds': [r.get('instance_id') for r in rows], 'totalRows': len(ds)}))"
  ].join("\n");
  const result = await runProcess("docker", runnerCommand(runnerImage, ["python", "-c", script]), process.cwd());
  if (result.exitCode !== 0) {
    throw new Error(result.stderr || result.stdout || "failed to probe SWE-bench dataset");
  }
  return JSON.parse(result.stdout) as OfficialSweBenchDatasetProbe;
}

export async function assertInstanceInDataset(
  instanceId: string,
  datasetName = DEFAULT_SWEBENCH_DATASET,
  split = DEFAULT_SWEBENCH_SPLIT,
  runnerImage = "swebench-official-runner"
): Promise<void> {
  const script = [
    "from datasets import load_dataset",
    "import sys",
    "ds = load_dataset(" + JSON.stringify(datasetName) + ", split=" + JSON.stringify(split) + ")",
    "target = " + JSON.stringify(instanceId),
    "sys.exit(0 if any(row.get('instance_id') == target for row in ds) else 3)"
  ].join("\n");
  const result = await runProcess("docker", runnerCommand(runnerImage, ["python", "-c", script]), process.cwd());
  if (result.exitCode !== 0) {
    throw new Error(`instance_id ${instanceId} was not found in ${datasetName}/${split}`);
  }
}

export async function writeOfficialSweBenchScore(options: {
  runId: string;
  instanceId: string;
  datasetName?: string;
  artifactsRoot?: string;
  projectRoot?: string;
  officialResultsDir?: string;
  errorMessage?: string;
}): Promise<OfficialSweBenchScoreResult> {
  const projectRoot = resolve(options.projectRoot ?? process.cwd());
  const artifactsRoot = resolve(projectRoot, options.artifactsRoot ?? "artifacts");
  const runDir = join(artifactsRoot, options.runId);
  const scorePath = join(runDir, "score-result.json");
  const officialResultsDir = options.officialResultsDir ?? join(runDir, "official-evaluation-results");
  const resultsPath = await findFile(officialResultsDir, "results.json");
  const instanceResultsPath = await findFile(officialResultsDir, "instance_results.jsonl");
  const logsPath = await findLogsPath(officialResultsDir, options.instanceId);

  let score: OfficialSweBenchScoreResult;
  if (options.errorMessage || !resultsPath || !instanceResultsPath) {
    score = {
      status: "infra-fail",
      resolved: null,
      instanceId: options.instanceId,
      datasetName: options.datasetName ?? DEFAULT_SWEBENCH_DATASET,
      runId: options.runId,
      officialResultsRef: resultsPath ?? undefined,
      instanceResultsRef: instanceResultsPath ?? undefined,
      logsRef: logsPath ?? undefined,
      errorMessage: options.errorMessage ?? "official SWE-bench result files are missing"
    };
  } else {
    const resolved = await readResolvedStatus(instanceResultsPath, options.instanceId);
    score = {
      status: resolved ? "pass" : "fail",
      resolved,
      instanceId: options.instanceId,
      datasetName: options.datasetName ?? DEFAULT_SWEBENCH_DATASET,
      runId: options.runId,
      officialResultsRef: resultsPath,
      instanceResultsRef: instanceResultsPath,
      logsRef: logsPath ?? undefined
    };
  }

  await mkdir(runDir, { recursive: true });
  await writeFile(scorePath, `${JSON.stringify(score, null, 2)}\n`, "utf8");
  return score;
}

function readPredictionInput(candidate: unknown): SweBenchPredictionInput {
  if (typeof candidate !== "object" || candidate === null || Array.isArray(candidate)) {
    throw new Error("prediction input entries must be objects");
  }
  const record = candidate as Record<string, unknown>;
  const instanceId = readRequiredString(record, "instanceId");
  const modelNameOrPath = readRequiredString(record, "modelNameOrPath");
  const modelPatch = readOptionalString(record, "modelPatch");
  const patchArtifactPath = readOptionalString(record, "patchArtifactPath");
  if (!modelPatch && !patchArtifactPath) {
    throw new Error(`prediction ${instanceId} is missing modelPatch or patchArtifactPath`);
  }
  return { instanceId, modelNameOrPath, modelPatch, patchArtifactPath };
}

async function resolvePatch(prediction: SweBenchPredictionInput, projectRoot: string): Promise<string> {
  if (!prediction.instanceId || !prediction.modelNameOrPath) {
    throw new Error("SWE-bench prediction requires instanceId and modelNameOrPath");
  }
  if (prediction.modelPatch) {
    return prediction.modelPatch;
  }
  if (!prediction.patchArtifactPath) {
    throw new Error(`prediction ${prediction.instanceId} has no patchArtifactPath`);
  }
  const patch = await readFile(resolve(projectRoot, prediction.patchArtifactPath), "utf8");
  if (!patch.trim()) {
    throw new Error(`prediction ${prediction.instanceId} has an empty patch artifact`);
  }
  return patch;
}

async function loadSweBenchLiteInstance(
  instanceId: string,
  datasetName: string,
  split: string,
  runnerImage: string,
  projectRoot: string
): Promise<SweBenchLiteInstanceMetadata> {
  const script = [
    "from datasets import load_dataset",
    "import json, sys",
    "target = " + JSON.stringify(instanceId),
    "ds = load_dataset(" + JSON.stringify(datasetName) + ", split=" + JSON.stringify(split) + ")",
    "for row in ds:",
    "    if row.get('instance_id') == target:",
    "        print(json.dumps(dict(row)))",
    "        sys.exit(0)",
    "sys.exit(3)"
  ].join("\n");
  const result = await runProcess("docker", runnerCommand(runnerImage, ["python", "-c", script]), projectRoot);
  if (result.exitCode !== 0) {
    throw new Error(`instance_id ${instanceId} was not found in ${datasetName}/${split}`);
  }
  return JSON.parse(result.stdout) as SweBenchLiteInstanceMetadata;
}

async function ensureRepoCheckout(repo: string, baseCommit: string, checkoutDir: string, projectRoot: string): Promise<void> {
  if (!(await exists(join(checkoutDir, ".git")))) {
    await mkdir(dirname(checkoutDir), { recursive: true });
    const cloneResult = await runProcess("git", ["clone", `https://github.com/${repo}.git`, checkoutDir], projectRoot);
    if (cloneResult.exitCode !== 0) {
      throw new Error(cloneResult.stderr || cloneResult.stdout || `failed to clone ${repo}`);
    }
  }
  const fetchResult = await runProcess("git", ["fetch", "origin", baseCommit], checkoutDir);
  if (fetchResult.exitCode !== 0) {
    throw new Error(fetchResult.stderr || fetchResult.stdout || `failed to fetch ${baseCommit}`);
  }
  const checkoutResult = await runProcess("git", ["checkout", "--force", baseCommit], checkoutDir);
  if (checkoutResult.exitCode !== 0) {
    throw new Error(checkoutResult.stderr || checkoutResult.stdout || `failed to checkout ${baseCommit}`);
  }
}

async function assertNonEmptyPatchArtifact(patchArtifactPath: string, projectRoot: string): Promise<void> {
  const absolutePath = resolve(projectRoot, patchArtifactPath);
  const content = await readFile(absolutePath, "utf8");
  if (!content.trim()) {
    throw new Error(`patch artifact is empty: ${patchArtifactPath}`);
  }
}

function renderAgentTaskBrief(
  instance: SweBenchLiteInstanceMetadata,
  patchArtifactPath: string,
  datasetName: string,
  split: string
): string {
  return [
    `# SWE-bench Lite Agent Smoke: ${instance.instance_id}`,
    "",
    `- Dataset: ${datasetName}`,
    `- Split: ${split}`,
    `- Repo: ${instance.repo}`,
    `- Base commit: ${instance.base_commit}`,
    `- Patch artifact target: ${patchArtifactPath}`,
    "",
    "## Task",
    "",
    instance.problem_statement,
    "",
    "## Rules",
    "",
    "- Produce a real agent-authored patch from this problem statement.",
    "- Do not use the gold patch or local mirror fixtures.",
    "- Export the final diff to the patch artifact target.",
    ""
  ].join("\n");
}

function redactInstanceForAgentArtifact(instance: SweBenchLiteInstanceMetadata): Record<string, unknown> {
  const redacted = { ...instance };
  delete redacted.patch;
  delete redacted.test_patch;
  delete redacted.hints_text;
  return redacted;
}

async function probeRunnerImage(runnerImage: string): Promise<{ image: string; ok: boolean; pythonVersion?: string }> {
  const result = await runProcess("docker", runnerCommand(runnerImage, ["python", "--version"]), process.cwd());
  return {
    image: runnerImage,
    ok: result.exitCode === 0,
    pythonVersion: (result.stdout || result.stderr).trim() || undefined
  };
}

async function probeRunnerModules(runnerImage: string): Promise<{ swebench: boolean; datasets: boolean }> {
  const script = [
    "import importlib.util",
    "print('swebench=' + str(importlib.util.find_spec('swebench') is not None))",
    "print('datasets=' + str(importlib.util.find_spec('datasets') is not None))"
  ].join(";");
  const result = await runProcess("docker", runnerCommand(runnerImage, ["python", "-c", script]), process.cwd());
  return {
    swebench: result.stdout.includes("swebench=True"),
    datasets: result.stdout.includes("datasets=True")
  };
}

function runnerCommand(runnerImage: string, command: string[]): string[] {
  return [
    "run",
    "--rm",
    "-v",
    "/var/run/docker.sock:/var/run/docker.sock",
    runnerImage,
    ...command
  ];
}

async function runVersion(command: string, args: string[]): Promise<{ ok: boolean; output?: string }> {
  const result = await runProcess(command, args, process.cwd());
  return {
    ok: result.exitCode === 0,
    output: (result.stdout || result.stderr).trim()
  };
}

async function runDockerDaemonProbe(): Promise<{ ok: boolean; output?: string }> {
  const result = await runProcess("docker", ["info", "--format", "{{.ServerVersion}}"], process.cwd());
  return {
    ok: result.exitCode === 0,
    output: (result.stdout || result.stderr).trim()
  };
}

async function runProcess(command: string, args: string[], cwd: string): Promise<{ stdout: string; stderr: string; exitCode: number | null }> {
  try {
    const result = await execFileAsync(command, args, { cwd });
    return { stdout: result.stdout, stderr: result.stderr, exitCode: 0 };
  } catch (error) {
    const commandError = error as Partial<NodeJS.ErrnoException> & {
      code?: number | string;
      stdout?: string;
      stderr?: string;
    };
    return {
      stdout: commandError.stdout ?? "",
      stderr: commandError.stderr ?? commandError.message ?? "",
      exitCode: typeof commandError.code === "number" ? commandError.code : null
    };
  }
}

async function exists(path: string): Promise<boolean> {
  try {
    await stat(path);
    return true;
  } catch {
    return false;
  }
}

async function findFile(root: string, fileName: string): Promise<string | null> {
  if (!(await exists(root))) {
    return null;
  }
  const entries = await readdir(root, { withFileTypes: true });
  for (const entry of entries) {
    const path = join(root, entry.name);
    if (entry.isFile() && entry.name === fileName) {
      return path;
    }
    if (entry.isDirectory()) {
      const found = await findFile(path, fileName);
      if (found) {
        return found;
      }
    }
  }
  return null;
}

async function findLogsPath(root: string, instanceId: string): Promise<string | null> {
  if (!(await exists(root))) {
    return null;
  }
  const entries = await readdir(root, { withFileTypes: true });
  for (const entry of entries) {
    const path = join(root, entry.name);
    if (entry.isDirectory() && entry.name.includes(instanceId)) {
      return path;
    }
    if (entry.isDirectory()) {
      const found = await findLogsPath(path, instanceId);
      if (found) {
        return found;
      }
    }
  }
  return null;
}

async function importOfficialRunArtifacts(options: {
  projectRoot: string;
  resultsDir: string;
  importedResultsDir: string;
  runId: string;
  stdout: string;
}): Promise<void> {
  await mkdir(options.importedResultsDir, { recursive: true });

  if (await exists(options.resultsDir)) {
    await cp(options.resultsDir, options.importedResultsDir, { recursive: true, force: true });
  }

  const reportPath = await findCurrentSweBenchReport(options.projectRoot, options.stdout);
  if (reportPath) {
    await copyFile(reportPath, join(options.importedResultsDir, basename(reportPath)));
    await copyFile(reportPath, join(options.importedResultsDir, "results.json"));
    await writeNormalizedInstanceResults(reportPath, join(options.importedResultsDir, "instance_results.jsonl"));
  }

  const logsRoot = join(options.projectRoot, "logs", "run_evaluation", options.runId);
  if (await exists(logsRoot)) {
    await cp(logsRoot, join(options.importedResultsDir, "logs"), { recursive: true, force: true });
  }
}

async function findCurrentSweBenchReport(projectRoot: string, stdout: string): Promise<string | null> {
  const match = stdout.match(/Report written to\s+(.+\.json)/);
  if (!match?.[1]) {
    return null;
  }
  const reportPath = resolve(projectRoot, match[1].trim());
  return (await exists(reportPath)) ? reportPath : null;
}

async function writeNormalizedInstanceResults(reportPath: string, outputPath: string): Promise<void> {
  const report = JSON.parse(await readFile(reportPath, "utf8")) as Record<string, unknown>;
  const submittedIds = readStringArray(report, "submitted_ids");
  const resolvedIds = new Set(readStringArray(report, "resolved_ids"));
  const unresolvedIds = new Set(readStringArray(report, "unresolved_ids"));
  const errorIds = new Set(readStringArray(report, "error_ids"));
  const lines = submittedIds.map((instanceId) =>
    JSON.stringify({
      instance_id: instanceId,
      resolved: resolvedIds.has(instanceId),
      official_status: resolvedIds.has(instanceId)
        ? "resolved"
        : unresolvedIds.has(instanceId)
          ? "unresolved"
          : errorIds.has(instanceId)
            ? "error"
            : "unknown"
    })
  );
  await writeFile(outputPath, `${lines.join("\n")}\n`, "utf8");
}

function readStringArray(record: Record<string, unknown>, key: string): string[] {
  const value = record[key];
  if (!Array.isArray(value)) {
    return [];
  }
  return value.filter((item): item is string => typeof item === "string");
}

async function readResolvedStatus(instanceResultsPath: string, instanceId: string): Promise<boolean> {
  const content = await readFile(instanceResultsPath, "utf8");
  const records = content
    .split(/\r?\n/)
    .filter((line) => line.trim().length > 0)
    .map((line) => JSON.parse(line) as Record<string, unknown>);
  const record = records.find((item) => item.instance_id === instanceId || item.instanceId === instanceId);
  return record?.resolved === true;
}

function readRequiredString(record: Record<string, unknown>, key: string): string {
  const value = record[key];
  if (typeof value !== "string" || value.length === 0) {
    throw new Error(`${key} must be a non-empty string`);
  }
  return value;
}

function readOptionalString(record: Record<string, unknown>, key: string): string | undefined {
  const value = record[key];
  if (value === undefined) {
    return undefined;
  }
  if (typeof value !== "string" || value.length === 0) {
    throw new Error(`${key} must be a non-empty string when provided`);
  }
  return value;
}
