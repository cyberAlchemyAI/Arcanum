import { mkdir, readFile, writeFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";

import type { CampaignReport, CampaignRunSummary } from "./campaign-report.ts";
import { buildCampaignReport } from "./campaign-report.ts";

export interface DashboardDataOptions {
  projectRoot?: string;
  reportPath?: string;
  outputPath?: string;
}

export interface DashboardData {
  generatedAt: string;
  summary: DashboardSummary;
  runs: DashboardRunListItem[];
  runDetails: Record<string, DashboardRunDetail>;
  evidenceGaps: CampaignReport["evidenceGaps"];
}

export interface DashboardSummary {
  totalRuns: number;
  pass: number;
  fail: number;
  infraFail: number;
  quarantined: number;
  resolved: number;
  unresolved: number;
  unknownResolution: number;
  telemetryEvents: number;
  evidenceGapCount: number;
}

export interface DashboardRunListItem {
  runId: string;
  taskId: string;
  suite: string;
  status: string;
  resolved: boolean | null;
  telemetryEvents: number;
  evidenceGapCount: number;
}

export interface DashboardRunDetail extends DashboardRunListItem {
  scorePath: string;
  scoreComponents: Record<string, unknown>;
  telemetry: CampaignRunSummary["telemetry"];
  evidenceRefs: CampaignRunSummary["evidenceRefs"];
}

export async function buildDashboardData(options: DashboardDataOptions = {}): Promise<DashboardData> {
  const projectRoot = resolve(options.projectRoot ?? process.cwd());
  const report = options.reportPath
    ? (JSON.parse(await readFile(resolve(projectRoot, options.reportPath), "utf8")) as CampaignReport)
    : await buildCampaignReport({ projectRoot });
  const data = dashboardDataFromReport(report);

  if (options.outputPath) {
    await writeJson(resolve(projectRoot, options.outputPath), data);
  }

  return data;
}

export function dashboardDataFromReport(report: CampaignReport): DashboardData {
  const runs = report.runs.map((run) => toRunListItem(run));
  return {
    generatedAt: report.generatedAt,
    summary: {
      totalRuns: report.summary.totalRuns,
      pass: report.summary.counts.pass,
      fail: report.summary.counts.fail,
      infraFail: report.summary.counts["infra-fail"],
      quarantined: report.summary.counts.quarantined,
      resolved: report.summary.resolved.true,
      unresolved: report.summary.resolved.false,
      unknownResolution: report.summary.resolved.unknown,
      telemetryEvents: report.summary.telemetryEvents,
      evidenceGapCount: report.summary.evidenceGapCount
    },
    runs,
    runDetails: Object.fromEntries(report.runs.map((run) => [run.runId, toRunDetail(run)])),
    evidenceGaps: report.evidenceGaps
  };
}

function toRunListItem(run: CampaignRunSummary): DashboardRunListItem {
  return {
    runId: run.runId,
    taskId: run.taskId,
    suite: run.suite,
    status: run.status,
    resolved: run.resolved,
    telemetryEvents: run.telemetry.eventCount,
    evidenceGapCount: run.evidenceRefs.filter((ref) => !ref.exists).length
  };
}

function toRunDetail(run: CampaignRunSummary): DashboardRunDetail {
  return {
    ...toRunListItem(run),
    scorePath: run.scorePath,
    scoreComponents: run.components,
    telemetry: run.telemetry,
    evidenceRefs: run.evidenceRefs
  };
}

async function writeJson(path: string, value: unknown): Promise<void> {
  await mkdir(dirname(path), { recursive: true });
  await writeFile(path, `${JSON.stringify(value, null, 2)}\n`, "utf8");
}
