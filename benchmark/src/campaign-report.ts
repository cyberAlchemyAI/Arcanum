import { mkdir, readFile, stat, writeFile } from "node:fs/promises";
import { dirname, join, relative, resolve } from "node:path";

export type CampaignRunStatus = "pass" | "fail" | "infra-fail" | "quarantined" | "unknown";

export interface CampaignReportOptions {
  campaignId?: string;
  projectRoot?: string;
  artifactsRoot?: string;
  outputPath?: string;
  scorePaths?: string[];
}

export interface CampaignReport {
  campaignId: string;
  generatedAt: string;
  artifactsRoot: string;
  summary: {
    totalRuns: number;
    counts: Record<CampaignRunStatus, number>;
    resolved: {
      true: number;
      false: number;
      unknown: number;
    };
    telemetryEvents: number;
    evidenceGapCount: number;
  };
  runs: CampaignRunSummary[];
  evidenceGaps: EvidenceGap[];
}

export interface CampaignRunSummary {
  runId: string;
  taskId: string;
  suite: string;
  status: CampaignRunStatus;
  resolved: boolean | null;
  scorePath: string;
  evidenceRefs: EvidenceRef[];
  components: Record<string, unknown>;
  telemetry: {
    path?: string;
    eventCount: number;
    firstStage?: string;
    lastStage?: string;
  };
}

export interface EvidenceRef {
  label: string;
  path: string;
  exists: boolean;
}

export interface EvidenceGap {
  runId: string;
  label: string;
  path: string;
  reason: string;
}

const DEFAULT_SCORE_PATHS = [
  "artifacts/kernel-smoke-001/score-result.json",
  "artifacts/kernel-smoke-002/score-result.json",
  "artifacts/sample-batch-001-001/score-result.json",
  "artifacts/swebench-lite-official-smoke/score-result.json",
  "artifacts/smellbench-official-smoke/score-result.json",
  "artifacts/perfcodebench-official-smoke/score-result.json"
];

export async function buildCampaignReport(options: CampaignReportOptions = {}): Promise<CampaignReport> {
  const projectRoot = resolve(options.projectRoot ?? process.cwd());
  const artifactsRoot = resolve(projectRoot, options.artifactsRoot ?? "artifacts");
  const scorePaths = options.scorePaths ?? DEFAULT_SCORE_PATHS;
  const runs: CampaignRunSummary[] = [];
  const evidenceGaps: EvidenceGap[] = [];

  for (const scorePath of scorePaths) {
    const absoluteScorePath = resolve(projectRoot, scorePath);
    if (!(await exists(absoluteScorePath))) {
      const runId = inferRunIdFromScorePath(scorePath);
      evidenceGaps.push({
        runId,
        label: "score",
        path: scorePath,
        reason: "score artifact missing"
      });
      continue;
    }
    const score = asRecord(JSON.parse(await readFile(absoluteScorePath, "utf8")));
    const run = await summarizeScore({ projectRoot, artifactsRoot, scorePath, absoluteScorePath, score });
    runs.push(run);
    evidenceGaps.push(
      ...run.evidenceRefs
        .filter((ref) => !ref.exists)
        .map((ref) => ({
          runId: run.runId,
          label: ref.label,
          path: ref.path,
          reason: "referenced artifact missing"
        }))
    );
  }

  const report: CampaignReport = {
    campaignId: options.campaignId ?? "campaign-report-smoke",
    generatedAt: new Date().toISOString(),
    artifactsRoot: toProjectRelative(projectRoot, artifactsRoot),
    summary: {
      totalRuns: runs.length,
      counts: countStatuses(runs),
      resolved: countResolved(runs),
      telemetryEvents: runs.reduce((sum, run) => sum + run.telemetry.eventCount, 0),
      evidenceGapCount: evidenceGaps.length
    },
    runs,
    evidenceGaps
  };

  if (options.outputPath) {
    await writeJson(resolve(projectRoot, options.outputPath), report);
  }

  return report;
}

export async function writeCampaignReportMarkdown(path: string, report: CampaignReport, projectRoot = process.cwd()): Promise<void> {
  const lines = [
    `# Campaign Report: ${report.campaignId}`,
    "",
    "## Summary",
    "",
    `- Total runs: ${report.summary.totalRuns}`,
    `- Pass: ${report.summary.counts.pass}`,
    `- Fail: ${report.summary.counts.fail}`,
    `- Infra fail: ${report.summary.counts["infra-fail"]}`,
    `- Quarantined: ${report.summary.counts.quarantined}`,
    `- Telemetry events: ${report.summary.telemetryEvents}`,
    `- Evidence gaps: ${report.summary.evidenceGapCount}`,
    "",
    "## Runs",
    "",
    "| Run | Suite | Task | Status | Resolved | Evidence refs | Telemetry events |",
    "| --- | --- | --- | --- | --- | --- | --- |",
    ...report.runs.map(
      (run) =>
        `| ${run.runId} | ${run.suite} | ${run.taskId} | ${run.status} | ${String(run.resolved)} | ${run.evidenceRefs.length} | ${run.telemetry.eventCount} |`
    ),
    "",
    "## Evidence Gaps",
    "",
    report.evidenceGaps.length === 0
      ? "None."
      : report.evidenceGaps.map((gap) => `- ${gap.runId}: ${gap.label} missing at ${gap.path}`).join("\n"),
    ""
  ];
  await mkdir(dirname(resolve(projectRoot, path)), { recursive: true });
  await writeFile(resolve(projectRoot, path), `${lines.join("\n")}`, "utf8");
}

async function summarizeScore(options: {
  projectRoot: string;
  artifactsRoot: string;
  scorePath: string;
  absoluteScorePath: string;
  score: Record<string, unknown>;
}): Promise<CampaignRunSummary> {
  const runId = readString(options.score.runId) ?? inferRunIdFromScorePath(options.scorePath);
  const taskId = readString(options.score.taskId) ?? readString(options.score.instanceId) ?? "unknown";
  const evidenceRefs = await collectEvidenceRefs(options.projectRoot, options.score, options.scorePath);
  const telemetry = await readTelemetrySummary(options.projectRoot, options.artifactsRoot, runId);
  return {
    runId,
    taskId,
    suite: inferSuite(options.score, options.scorePath),
    status: normalizeStatus(options.score.status),
    resolved: readResolved(options.score),
    scorePath: toProjectRelative(options.projectRoot, options.absoluteScorePath),
    evidenceRefs,
    components: collectComponents(options.score),
    telemetry
  };
}

async function collectEvidenceRefs(
  projectRoot: string,
  score: Record<string, unknown>,
  scorePath: string
): Promise<EvidenceRef[]> {
  const refs: Array<[string, unknown]> = [
    ["score", scorePath],
    ["evidence", score.evidenceRef],
    ["officialResults", score.officialResultsRef],
    ["instanceResults", score.instanceResultsRef],
    ["logs", score.logsRef],
    ["upstreamResults", score.upstreamResultsRef],
    ["evaluatorReport", score.evaluatorReportRef],
    ["console", score.consoleRef],
    ["taskDatabase", score.taskDatabaseRef],
    ["candidateManifest", score.candidateManifestRef],
    ["workerProfile", score.workerProfileRef],
    ["rawEvidence", score.rawEvidenceRef],
    ["scoreResult", score.scoreResultRef]
  ];
  const output: EvidenceRef[] = [];
  for (const [label, value] of refs) {
    const path = readString(value);
    if (!path) {
      continue;
    }
    const absolutePath = resolveMaybeAbsolute(projectRoot, path);
    output.push({
      label,
      path: toProjectRelative(projectRoot, absolutePath),
      exists: await exists(absolutePath)
    });
  }
  return output;
}

async function readTelemetrySummary(
  projectRoot: string,
  artifactsRoot: string,
  runId: string
): Promise<CampaignRunSummary["telemetry"]> {
  const directPath = join(artifactsRoot, runId, "telemetry.jsonl");
  if (!(await exists(directPath))) {
    return { eventCount: 0 };
  }
  const events = (await readFile(directPath, "utf8"))
    .split("\n")
    .filter((line) => line.trim().length > 0)
    .map((line) => asRecord(JSON.parse(line)));
  return {
    path: toProjectRelative(projectRoot, directPath),
    eventCount: events.length,
    firstStage: readString(events[0]?.stage),
    lastStage: readString(events.at(-1)?.stage)
  };
}

function collectComponents(score: Record<string, unknown>): Record<string, unknown> {
  const components = asRecord(score.components);
  const metrics = asRecord(score.metrics);
  const runtime = asRecord(score.runtime);
  const threshold = asRecord(score.threshold);
  const output: Record<string, unknown> = { ...components };
  if (Object.keys(metrics).length > 0) {
    output.metrics = metrics;
  }
  if (Object.keys(runtime).length > 0) {
    output.runtime = runtime;
  }
  if (Object.keys(threshold).length > 0) {
    output.threshold = threshold;
  }
  return output;
}

function countStatuses(runs: CampaignRunSummary[]): Record<CampaignRunStatus, number> {
  return runs.reduce(
    (counts, run) => {
      counts[run.status] += 1;
      return counts;
    },
    { pass: 0, fail: 0, "infra-fail": 0, quarantined: 0, unknown: 0 }
  );
}

function countResolved(runs: CampaignRunSummary[]): CampaignReport["summary"]["resolved"] {
  return runs.reduce(
    (counts, run) => {
      if (run.resolved === true) {
        counts.true += 1;
      } else if (run.resolved === false) {
        counts.false += 1;
      } else {
        counts.unknown += 1;
      }
      return counts;
    },
    { true: 0, false: 0, unknown: 0 }
  );
}

function inferSuite(score: Record<string, unknown>, scorePath: string): string {
  const datasetName = readString(score.datasetName);
  if (datasetName) {
    return datasetName;
  }
  if (scorePath.includes("kernel-smoke")) {
    return "fixture-local";
  }
  if (scorePath.includes("sample-batch")) {
    return "swe-bench-local-mirror";
  }
  return "unknown";
}

function inferRunIdFromScorePath(path: string): string {
  const parts = path.split("/");
  const artifactsIndex = parts.indexOf("artifacts");
  if (artifactsIndex >= 0 && parts[artifactsIndex + 1]) {
    return parts[artifactsIndex + 1];
  }
  return "unknown";
}

function normalizeStatus(value: unknown): CampaignRunStatus {
  if (value === "pass" || value === "fail" || value === "infra-fail" || value === "quarantined") {
    return value;
  }
  return "unknown";
}

function readResolved(score: Record<string, unknown>): boolean | null {
  if (typeof score.resolved === "boolean") {
    return score.resolved;
  }
  if (score.status === "pass") {
    return true;
  }
  if (score.status === "fail") {
    return false;
  }
  return null;
}

function resolveMaybeAbsolute(projectRoot: string, path: string): string {
  return path.startsWith("/") ? path : resolve(projectRoot, path);
}

function toProjectRelative(projectRoot: string, path: string): string {
  const absolutePath = resolveMaybeAbsolute(projectRoot, path);
  return relative(projectRoot, absolutePath) || ".";
}

async function exists(path: string): Promise<boolean> {
  try {
    await stat(path);
    return true;
  } catch {
    return false;
  }
}

function asRecord(candidate: unknown): Record<string, unknown> {
  return typeof candidate === "object" && candidate !== null && !Array.isArray(candidate) ? candidate : {};
}

function readString(value: unknown): string | null {
  return typeof value === "string" && value.length > 0 ? value : null;
}

async function writeJson(path: string, value: unknown): Promise<void> {
  await mkdir(dirname(path), { recursive: true });
  await writeFile(path, `${JSON.stringify(value, null, 2)}\n`, "utf8");
}
