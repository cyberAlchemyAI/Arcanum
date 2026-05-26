import { buildCampaignReport, writeCampaignReportMarkdown } from "./campaign-report.ts";

const outputPath = process.env.CAMPAIGN_REPORT_PATH ?? "artifacts/campaign-report-smoke/campaign-report.json";
const markdownPath = process.env.CAMPAIGN_REPORT_MARKDOWN_PATH ?? "artifacts/campaign-report-smoke/campaign-report.md";
const report = await buildCampaignReport({
  campaignId: process.env.CAMPAIGN_ID ?? "campaign-report-smoke",
  outputPath
});
await writeCampaignReportMarkdown(markdownPath, report);

console.log(`${report.campaignId}: ${report.summary.totalRuns} runs, ${report.summary.evidenceGapCount} evidence gaps`);
console.log(`  report: ${outputPath}`);
console.log(`  markdown: ${markdownPath}`);
