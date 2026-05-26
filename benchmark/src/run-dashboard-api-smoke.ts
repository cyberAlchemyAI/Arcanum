import { buildDashboardData } from "./dashboard-api.ts";

const reportPath = process.env.CAMPAIGN_REPORT_PATH ?? "artifacts/campaign-report-smoke/campaign-report.json";
const outputPath = process.env.DASHBOARD_DATA_PATH ?? "artifacts/dashboard-api-smoke/dashboard-data.json";

const data = await buildDashboardData({ reportPath, outputPath });

if (data.summary.totalRuns === 0) {
  throw new Error("dashboard data must include at least one run");
}
if (Object.keys(data.runDetails).length !== data.runs.length) {
  throw new Error("dashboard runDetails must contain one entry per run");
}
for (const run of data.runs) {
  const detail = data.runDetails[run.runId];
  if (!detail) {
    throw new Error(`missing detail for ${run.runId}`);
  }
  if (detail.evidenceRefs.length === 0) {
    throw new Error(`run ${run.runId} has no evidence refs`);
  }
}

console.log(`dashboard-api-smoke: ${data.summary.totalRuns} runs, ${data.summary.evidenceGapCount} evidence gaps`);
console.log(`  data: ${outputPath}`);
