import { execFile } from "node:child_process";
import { copyFile, cp, mkdir, readdir, readFile, rm, stat, writeFile } from "node:fs/promises";
import { basename, dirname, join, resolve } from "node:path";
import { promisify } from "node:util";

const execFileAsync = promisify(execFile);

export const DEFAULT_SMELLBENCH_DATASET = "CodeSmells_Scikit_architectural_hard_classification";
export const DEFAULT_SMELLBENCH_RUN_ID = "smellbench-official-smoke";
export const DEFAULT_SMELLBENCH_EVALUATOR_DIR =
  "artifacts/smellbench-contract-probe/extracted/ExperimentsReproductionPackage/Code Smell Evaluator";
export const DEFAULT_SMELLBENCH_HARD_CSV =
  "artifacts/smellbench-contract-probe/extracted/ExperimentsReproductionPackage/Dataset Builder/result_dataset/scikitlearn_1.7.2_baseline/CodeSmells_Scikit_architectural_hard_classification.csv";

const DEFAULT_BASELINE_ALL_REPORT =
  "artifacts/smellbench-contract-probe/extracted/ExperimentsReproductionPackage/Code Smell Evaluator/input_reports/CodeSmells_Scikit_architectural_all_classification.csv";
const DEFAULT_ANALYZER_SRC =
  "artifacts/smellbench-contract-probe/extracted/ExperimentsReproductionPackage/python_smells_detector/src";
const DEFAULT_ANALYZER_CONFIG =
  "artifacts/smellbench-contract-probe/extracted/ExperimentsReproductionPackage/python_smells_detector/code_quality_config.yaml";
const DEFAULT_DATASET_BUILDER_DIR =
  "artifacts/smellbench-contract-probe/extracted/ExperimentsReproductionPackage/Dataset Builder";
const DEFAULT_ANALYZER_DEPS = "/tmp/smellbench-analyzer-pydeps";
const DEFAULT_EVALUATOR_DEPS = "/tmp/smellbench-eval-pydeps";

export interface SmellBenchCandidateInput {
  taskId: string;
  modelNameOrPath: string;
  patchArtifactPath: string;
}

export interface SmellBenchCandidateManifestEntry extends SmellBenchCandidateInput {
  patchBytes: number;
  source: "harness-local";
}

export interface SmellBenchOfficialRunResult {
  ok: boolean;
  command: string[];
  runId: string;
  taskId: string;
  datasetName: string;
  upstreamResultsDir: string;
  stdoutPath?: string;
  stderrPath?: string;
  evaluatorReportPath?: string;
  exitCode: number | null;
}

export interface SmellBenchScoreResult {
  status: "pass" | "fail" | "infra-fail";
  resolved: boolean | null;
  taskId: string;
  datasetName: string;
  runId: string;
  upstreamResultsRef?: string;
  evaluatorReportRef?: string;
  consoleRef?: string;
  taskDatabaseRef?: string;
  candidateManifestRef?: string;
  metrics?: {
    tasksAttempted?: number;
    failedRepairs?: number;
    truePositives?: number;
    weightedRepairScore?: number;
    overallEffectiveness?: number;
  };
  derivation?: string;
  errorMessage?: string;
}

export async function loadSmellBenchCandidateManifest(
  path = "fixtures/smellbench-agent-patches.json",
  projectRoot = process.cwd()
): Promise<SmellBenchCandidateInput[]> {
  const parsed = JSON.parse(await readFile(resolve(projectRoot, path), "utf8")) as unknown;
  if (!Array.isArray(parsed) || parsed.length === 0) {
    throw new Error("SmellBench candidate manifest must be a non-empty JSON array");
  }
  const entries = parsed.map(readCandidateInput);
  for (const entry of entries) {
    await assertHarnessLocalPatch(entry, projectRoot);
  }
  return entries;
}

export async function assertSmellBenchTaskExists(options: {
  taskId: string;
  hardCsvPath?: string;
  projectRoot?: string;
}): Promise<Record<string, string>> {
  const projectRoot = resolve(options.projectRoot ?? process.cwd());
  const csvPath = resolve(projectRoot, options.hardCsvPath ?? DEFAULT_SMELLBENCH_HARD_CSV);
  const records = parseCsv(await readFile(csvPath, "utf8"));
  const rowIndex = taskIdToOneBasedIndex(options.taskId);
  const row = records[rowIndex - 1];
  if (!row) {
    throw new Error(`SmellBench task ${options.taskId} was not found in ${csvPath}`);
  }
  if ((row.LLM_difficulty_rule ?? "").trim().toLowerCase() !== "hard") {
    throw new Error(`SmellBench task ${options.taskId} is not from the hard split`);
  }
  return row;
}

export async function materializeSmellBenchCandidateManifest(options: {
  candidates: SmellBenchCandidateInput[];
  runId?: string;
  projectRoot?: string;
  artifactsRoot?: string;
}): Promise<string> {
  const projectRoot = resolve(options.projectRoot ?? process.cwd());
  const runId = options.runId ?? DEFAULT_SMELLBENCH_RUN_ID;
  const runDir = resolve(projectRoot, options.artifactsRoot ?? "artifacts", runId);
  const manifestPath = join(runDir, "candidate-manifest.json");
  const entries: SmellBenchCandidateManifestEntry[] = [];
  for (const candidate of options.candidates) {
    await assertSmellBenchTaskExists({ taskId: candidate.taskId, projectRoot });
    const patchPath = resolve(projectRoot, candidate.patchArtifactPath);
    const patchStats = await stat(patchPath);
    entries.push({
      ...candidate,
      patchBytes: patchStats.size,
      source: "harness-local"
    });
  }
  await mkdir(runDir, { recursive: true });
  await writeFile(manifestPath, `${JSON.stringify(entries, null, 2)}\n`, "utf8");
  return manifestPath;
}

export async function runOfficialSmellBenchSmoke(options: {
  candidates: SmellBenchCandidateInput[];
  runId?: string;
  projectRoot?: string;
  artifactsRoot?: string;
  evaluatorDir?: string;
  baselineAllReport?: string;
}): Promise<SmellBenchOfficialRunResult> {
  if (options.candidates.length !== 1) {
    throw new Error("SmellBench smoke requires exactly one pinned candidate");
  }

  const projectRoot = resolve(options.projectRoot ?? process.cwd());
  const runId = options.runId ?? DEFAULT_SMELLBENCH_RUN_ID;
  const runDir = resolve(projectRoot, options.artifactsRoot ?? "artifacts", runId);
  const upstreamResultsDir = join(runDir, "official-or-upstream-results");
  const evaluatorSourceDir = resolve(projectRoot, options.evaluatorDir ?? DEFAULT_SMELLBENCH_EVALUATOR_DIR);
  const evaluatorRunDir = join(upstreamResultsDir, "evaluator");
  const inputReportsDir = join(upstreamResultsDir, "input_reports");
  const inputDatabaseDir = join(upstreamResultsDir, "input_solutions_database");
  const logsDir = join(upstreamResultsDir, "logs");
  const candidate = options.candidates[0]!;
  const agentSlug = slugify(candidate.modelNameOrPath);
  const oldReportPath = join(inputReportsDir, "CodeSmells_Scikit_architectural_all_classification.csv");
  const newReportPath = join(inputReportsDir, `code_quality_report_${agentSlug}_architectural_all_classification.csv`);
  const dbPath = join(inputDatabaseDir, `tasks_state_${agentSlug}.db`);
  const stdoutPath = join(logsDir, "evaluator-stdout.txt");
  const stderrPath = join(logsDir, "evaluator-stderr.txt");
  const baselineAllReport = resolve(projectRoot, options.baselineAllReport ?? DEFAULT_BASELINE_ALL_REPORT);

  await assertSmellBenchTaskExists({ taskId: candidate.taskId, projectRoot });
  await assertHarnessLocalPatch(candidate, projectRoot);
  await rm(upstreamResultsDir, { recursive: true, force: true });
  await mkdir(inputReportsDir, { recursive: true });
  await mkdir(inputDatabaseDir, { recursive: true });
  await mkdir(logsDir, { recursive: true });
  await cp(evaluatorSourceDir, evaluatorRunDir, { recursive: true, force: true });
  await rm(join(evaluatorRunDir, "evaluation_reports"), { recursive: true, force: true });
  await rm(join(evaluatorRunDir, "input_reports"), { recursive: true, force: true });
  await rm(join(evaluatorRunDir, "input_solutions_database"), { recursive: true, force: true });
  await mkdir(join(evaluatorRunDir, "evaluation_reports"), { recursive: true });

  await copyFile(baselineAllReport, oldReportPath);
  const generatedReport = await runPostPatchAnalysisAndClassification({
    projectRoot,
    upstreamResultsDir,
    logsDir,
    agentSlug,
    candidate
  });
  await copyFile(generatedReport.classifiedReportPath, newReportPath);
  await writeCandidateTaskStateDb({
    dbPath,
    candidate,
    summary:
      "Harness-local SmellBench smoke candidate. The smoke runs post-patch PyExamine analysis and Dataset Builder classification before invoking the upstream evaluator for one pinned candidate.",
    changedFiles: candidate.patchArtifactPath
  });

  const command = ["python3", "main.py", "--old", oldReportPath, "--new", newReportPath, "--db", dbPath];
  const result = await runProcess(command[0]!, command.slice(1), evaluatorRunDir, {
    PYTHONPATH: ["/tmp/smellbench-eval-pydeps", process.env.PYTHONPATH].filter(Boolean).join(":"),
    MPLCONFIGDIR: "/tmp/smellbench-mpl-cache"
  });
  await writeFile(stdoutPath, result.stdout, "utf8");
  await writeFile(stderrPath, result.stderr, "utf8");

  const evaluatorReportPath = await findNewestFile(join(evaluatorRunDir, "evaluation_reports"), ".xlsx");
  if (evaluatorReportPath) {
    await copyFile(evaluatorReportPath, join(upstreamResultsDir, basename(evaluatorReportPath)));
  }

  await writeFile(
    join(upstreamResultsDir, "input-derivation.json"),
    `${JSON.stringify(
      {
        oldReportPath,
        newReportPath,
        dbPath,
        postFixReportDerivation: "generated by running PyExamine on the candidate checkout and classifying with Dataset Builder",
        pyExamineRawReportPath: generatedReport.rawReportPath,
        classifiedReportPath: generatedReport.classifiedReportPath,
        candidatePatchArtifactPath: candidate.patchArtifactPath,
        evaluatorCommand: command
      },
      null,
      2
    )}\n`,
    "utf8"
  );

  return {
    ok: result.exitCode === 0,
    command,
    runId,
    taskId: candidate.taskId,
    datasetName: DEFAULT_SMELLBENCH_DATASET,
    upstreamResultsDir,
    stdoutPath,
    stderrPath,
    evaluatorReportPath: evaluatorReportPath ? join(upstreamResultsDir, basename(evaluatorReportPath)) : undefined,
    exitCode: result.exitCode
  };
}

export async function writeSmellBenchScore(options: {
  runId: string;
  taskId: string;
  projectRoot?: string;
  artifactsRoot?: string;
  upstreamResultsDir?: string;
  candidateManifestPath?: string;
  errorMessage?: string;
}): Promise<SmellBenchScoreResult> {
  const projectRoot = resolve(options.projectRoot ?? process.cwd());
  const runDir = resolve(projectRoot, options.artifactsRoot ?? "artifacts", options.runId);
  const scorePath = join(runDir, "score-result.json");
  const upstreamResultsDir = options.upstreamResultsDir ?? join(runDir, "official-or-upstream-results");
  const stdoutPath = join(upstreamResultsDir, "logs", "evaluator-stdout.txt");
  const dbPath = await findFile(upstreamResultsDir, `tasks_state_${slugify("codex-local-smoke")}.db`);
  const evaluatorReportPath = await findNewestFile(upstreamResultsDir, ".xlsx");
  const manifestPath = options.candidateManifestPath ?? join(runDir, "candidate-manifest.json");

  let score: SmellBenchScoreResult;
  if (options.errorMessage || !(await exists(stdoutPath)) || !evaluatorReportPath) {
    score = {
      status: "infra-fail",
      resolved: null,
      taskId: options.taskId,
      datasetName: DEFAULT_SMELLBENCH_DATASET,
      runId: options.runId,
      upstreamResultsRef: (await exists(upstreamResultsDir)) ? upstreamResultsDir : undefined,
      evaluatorReportRef: evaluatorReportPath ?? undefined,
      consoleRef: (await exists(stdoutPath)) ? stdoutPath : undefined,
      taskDatabaseRef: dbPath ?? undefined,
      candidateManifestRef: (await exists(manifestPath)) ? manifestPath : undefined,
      derivation: "missing evaluator output",
      errorMessage: options.errorMessage ?? "SmellBench evaluator output files are missing"
    };
  } else {
    const metrics = parseSmellBenchConsoleMetrics(await readFile(stdoutPath, "utf8"));
    const resolved = (metrics.overallEffectiveness ?? 0) > 0;
    score = {
      status: resolved ? "pass" : "fail",
      resolved,
      taskId: options.taskId,
      datasetName: DEFAULT_SMELLBENCH_DATASET,
      runId: options.runId,
      upstreamResultsRef: upstreamResultsDir,
      evaluatorReportRef: evaluatorReportPath,
      consoleRef: stdoutPath,
      taskDatabaseRef: dbPath ?? undefined,
      candidateManifestRef: (await exists(manifestPath)) ? manifestPath : undefined,
      metrics,
      derivation: "status is pass only when upstream evaluator console metrics report overall effectiveness greater than zero"
    };
  }

  await mkdir(runDir, { recursive: true });
  await writeFile(scorePath, `${JSON.stringify(score, null, 2)}\n`, "utf8");
  return score;
}

export async function writeSmellBenchOracleEvidence(options: {
  runId: string;
  score: SmellBenchScoreResult;
  projectRoot?: string;
  artifactsRoot?: string;
}): Promise<string> {
  const projectRoot = resolve(options.projectRoot ?? process.cwd());
  const runDir = resolve(projectRoot, options.artifactsRoot ?? "artifacts", options.runId);
  const evidencePath = join(runDir, "oracle-evidence.json");
  const evidence = {
    oracle: "SmellBench",
    taskId: options.score.taskId,
    status: options.score.status,
    resolved: options.score.resolved,
    rawEvidence: {
      upstreamResultsRef: options.score.upstreamResultsRef,
      evaluatorReportRef: options.score.evaluatorReportRef,
      consoleRef: options.score.consoleRef,
      taskDatabaseRef: options.score.taskDatabaseRef
    },
    metrics: options.score.metrics,
    derivation: options.score.derivation
  };
  await writeFile(evidencePath, `${JSON.stringify(evidence, null, 2)}\n`, "utf8");
  return evidencePath;
}

async function runPostPatchAnalysisAndClassification(options: {
  projectRoot: string;
  upstreamResultsDir: string;
  logsDir: string;
  agentSlug: string;
  candidate: SmellBenchCandidateInput;
}): Promise<{ rawReportPath: string; classifiedReportPath: string }> {
  const analysisDir = join(options.upstreamResultsDir, "post-patch-analysis");
  const analyzerRawDir = join(analysisDir, "raw_datasets");
  const datasetBuilderRunDir = join(analysisDir, "dataset-builder");
  const checkoutDir = resolve(options.projectRoot, "artifacts", "smellbench-agent-smoke", options.candidate.taskId, "repo");
  const rawReportPath = join(analyzerRawDir, `code_quality_report_${options.agentSlug}.csv`);
  const classifiedReportPath = join(
    datasetBuilderRunDir,
    "result_dataset",
    `code_quality_report_${options.agentSlug}_architectural_all_classification.csv`
  );

  if (!(await exists(checkoutDir))) {
    throw new Error(`candidate checkout is missing for post-patch analysis: ${checkoutDir}`);
  }

  await mkdir(analyzerRawDir, { recursive: true });
  await cp(resolve(options.projectRoot, DEFAULT_DATASET_BUILDER_DIR), datasetBuilderRunDir, { recursive: true, force: true });
  await rm(join(datasetBuilderRunDir, "result_dataset"), { recursive: true, force: true });
  await rm(join(datasetBuilderRunDir, "raw_datasets"), { recursive: true, force: true });
  await mkdir(join(datasetBuilderRunDir, "raw_datasets"), { recursive: true });
  await mkdir(join(datasetBuilderRunDir, "result_dataset"), { recursive: true });

  const analyzerScript = [
    "import sys",
    "from code_quality_analyzer.main import analyze_project",
    "sys.argv = [",
    "  'analyze_code_quality',",
    `  ${JSON.stringify(checkoutDir)},`,
    "  '--config',",
    `  ${JSON.stringify(resolve(options.projectRoot, DEFAULT_ANALYZER_CONFIG))},`,
    "  '--output',",
    `  ${JSON.stringify(rawReportPath)},`,
    "  '--type',",
    "  'architectural',",
    "]",
    "analyze_project()"
  ].join("\n");
  const analyzerResult = await runProcess("python3", ["-c", analyzerScript], options.projectRoot, {
    PYTHONPATH: [DEFAULT_ANALYZER_DEPS, resolve(options.projectRoot, DEFAULT_ANALYZER_SRC), process.env.PYTHONPATH]
      .filter(Boolean)
      .join(":")
  });
  await writeFile(join(options.logsDir, "pyexamine-stdout.txt"), analyzerResult.stdout, "utf8");
  await writeFile(join(options.logsDir, "pyexamine-stderr.txt"), analyzerResult.stderr, "utf8");
  if (analyzerResult.exitCode !== 0) {
    throw new Error(analyzerResult.stderr || analyzerResult.stdout || "post-patch PyExamine analysis failed");
  }
  if (!(await exists(rawReportPath))) {
    throw new Error(`post-patch PyExamine report was not created: ${rawReportPath}`);
  }

  const datasetFileName = basename(rawReportPath);
  await copyFile(rawReportPath, join(datasetBuilderRunDir, "raw_datasets", datasetFileName));
  const classifyResult = await runProcess(
    "python3",
    ["main.py", "classify_dataset", datasetFileName, "--repo-root", checkoutDir, "--difficulty", "all"],
    datasetBuilderRunDir,
    {
      PYTHONPATH: [datasetBuilderRunDir, DEFAULT_EVALUATOR_DEPS, process.env.PYTHONPATH].filter(Boolean).join(":")
    }
  );
  await writeFile(join(options.logsDir, "dataset-builder-stdout.txt"), classifyResult.stdout, "utf8");
  await writeFile(join(options.logsDir, "dataset-builder-stderr.txt"), classifyResult.stderr, "utf8");
  if (classifyResult.exitCode !== 0) {
    throw new Error(classifyResult.stderr || classifyResult.stdout || "post-patch Dataset Builder classification failed");
  }
  if (!(await exists(classifiedReportPath))) {
    throw new Error(`classified post-patch report was not created: ${classifiedReportPath}`);
  }

  return { rawReportPath, classifiedReportPath };
}

export function parseSmellBenchConsoleMetrics(stdout: string): SmellBenchScoreResult["metrics"] {
  return {
    tasksAttempted: readNumber(stdout, /Tasks Attempted:\s+([0-9.]+)/),
    failedRepairs: readNumber(stdout, /Failed Repairs:\s+([0-9.]+)/),
    truePositives: readNumber(stdout, /True Positives:\s+([0-9.]+)/),
    weightedRepairScore: readNumber(stdout, /Weighted Repair Score:\s+([0-9.-]+)/),
    overallEffectiveness: readNumber(stdout, /Overall Effectiveness:\s+([0-9.-]+)/)
  };
}

function readCandidateInput(candidate: unknown): SmellBenchCandidateInput {
  if (typeof candidate !== "object" || candidate === null || Array.isArray(candidate)) {
    throw new Error("SmellBench candidate entries must be objects");
  }
  const record = candidate as Record<string, unknown>;
  return {
    taskId: readRequiredString(record, "taskId"),
    modelNameOrPath: readRequiredString(record, "modelNameOrPath"),
    patchArtifactPath: readRequiredString(record, "patchArtifactPath")
  };
}

async function assertHarnessLocalPatch(candidate: SmellBenchCandidateInput, projectRoot: string): Promise<void> {
  if (!candidate.patchArtifactPath.startsWith("artifacts/smellbench-agent-smoke/")) {
    throw new Error(`SmellBench patch must point to harness-local artifact path: ${candidate.patchArtifactPath}`);
  }
  for (const forbidden of ["tasks_state", "input_solutions_database", "input_reports/code_quality_report_"]) {
    if (candidate.patchArtifactPath.includes(forbidden)) {
      throw new Error(`SmellBench patch path points at forbidden benchmark output: ${candidate.patchArtifactPath}`);
    }
  }
  const patch = await readFile(resolve(projectRoot, candidate.patchArtifactPath), "utf8");
  if (!patch.trim()) {
    throw new Error(`SmellBench patch artifact is empty: ${candidate.patchArtifactPath}`);
  }
}

async function writeCandidateTaskStateDb(options: {
  dbPath: string;
  candidate: SmellBenchCandidateInput;
  summary: string;
  changedFiles: string;
}): Promise<void> {
  const script = [
    "import sqlite3, sys",
    "db_path, summary, changed_files = sys.argv[1:4]",
    "conn = sqlite3.connect(db_path)",
    "cur = conn.cursor()",
    "cur.execute('CREATE TABLE task_state (task_id TEXT, status TEXT, summary TEXT, changed_files TEXT, task_solve_score REAL, attempts INTEGER)')",
    "cur.execute('INSERT INTO task_state VALUES (?, ?, ?, ?, ?, ?)', ('custom-0001', 'done', summary, changed_files, 0.0, 1))",
    "conn.commit()",
    "conn.close()"
  ].join("\n");
  const result = await runProcess("python3", ["-c", script, options.dbPath, options.summary, options.changedFiles], process.cwd());
  if (result.exitCode !== 0) {
    throw new Error(result.stderr || result.stdout || "failed to create SmellBench task_state database");
  }
}

function parseCsv(content: string): Record<string, string>[] {
  const rows = parseCsvRows(content);
  const header = rows.shift();
  if (!header) {
    return [];
  }
  return rows
    .filter((row) => row.some((cell) => cell.length > 0))
    .map((row) => Object.fromEntries(header.map((key, index) => [key, row[index] ?? ""])));
}

function parseCsvRows(content: string): string[][] {
  const rows: string[][] = [];
  let row: string[] = [];
  let cell = "";
  let quoted = false;

  for (let index = 0; index < content.length; index += 1) {
    const char = content[index];
    const next = content[index + 1];
    if (char === '"' && quoted && next === '"') {
      cell += '"';
      index += 1;
    } else if (char === '"') {
      quoted = !quoted;
    } else if (char === "," && !quoted) {
      row.push(cell);
      cell = "";
    } else if ((char === "\n" || char === "\r") && !quoted) {
      if (char === "\r" && next === "\n") {
        index += 1;
      }
      row.push(cell);
      rows.push(row);
      row = [];
      cell = "";
    } else {
      cell += char;
    }
  }
  if (cell.length > 0 || row.length > 0) {
    row.push(cell);
    rows.push(row);
  }
  return rows;
}

function taskIdToOneBasedIndex(taskId: string): number {
  const match = taskId.match(/(\d+)$/);
  if (!match?.[1]) {
    throw new Error(`SmellBench task id does not end in a numeric row index: ${taskId}`);
  }
  return Number(match[1]);
}

function readNumber(content: string, regex: RegExp): number | undefined {
  const match = content.match(regex);
  if (!match?.[1]) {
    return undefined;
  }
  return Number(match[1]);
}

function readRequiredString(record: Record<string, unknown>, key: string): string {
  const value = record[key];
  if (typeof value !== "string" || value.length === 0) {
    throw new Error(`${key} must be a non-empty string`);
  }
  return value;
}

function slugify(value: string): string {
  return value.toLowerCase().replace(/[^a-z0-9._-]+/g, "-").replace(/^-|-$/g, "");
}

async function runProcess(
  command: string,
  args: string[],
  cwd: string,
  env?: NodeJS.ProcessEnv
): Promise<{ stdout: string; stderr: string; exitCode: number | null }> {
  try {
    const result = await execFileAsync(command, args, { cwd, env: { ...process.env, ...env } });
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

async function findNewestFile(root: string, suffix: string): Promise<string | null> {
  if (!(await exists(root))) {
    return null;
  }
  const entries = await readdir(root, { withFileTypes: true });
  const candidates: Array<{ path: string; mtimeMs: number }> = [];
  for (const entry of entries) {
    const path = join(root, entry.name);
    if (entry.isDirectory()) {
      const nested = await findNewestFile(path, suffix);
      if (nested) {
        const nestedStats = await stat(nested);
        candidates.push({ path: nested, mtimeMs: nestedStats.mtimeMs });
      }
    } else if (entry.isFile() && entry.name.endsWith(suffix)) {
      const fileStats = await stat(path);
      candidates.push({ path, mtimeMs: fileStats.mtimeMs });
    }
  }
  candidates.sort((left, right) => right.mtimeMs - left.mtimeMs);
  return candidates[0]?.path ?? null;
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
