import { strict as assert } from "node:assert";
import { mkdir, mkdtemp, readFile, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";

import { buildCampaignReport, writeCampaignReportMarkdown } from "../src/campaign-report.ts";

test("campaign report links scores to evidence and telemetry", async () => {
  const projectRoot = await mkdtemp(join(tmpdir(), "campaign-report-"));
  await mkdir(join(projectRoot, "artifacts", "run-1"), { recursive: true });
  await writeFile(join(projectRoot, "artifacts", "run-1", "oracle-evidence.json"), "{}\n", "utf8");
  await writeFile(
    join(projectRoot, "artifacts", "run-1", "score-result.json"),
    JSON.stringify(
      {
        runId: "run-1",
        taskId: "fixture.refactor.001",
        status: "pass",
        evidenceRef: "artifacts/run-1/oracle-evidence.json",
        components: { oraclePassed: true }
      },
      null,
      2
    ) + "\n",
    "utf8"
  );
  await writeFile(
    join(projectRoot, "artifacts", "run-1", "telemetry.jsonl"),
    [
      JSON.stringify({ runId: "run-1", sequence: 0, stage: "queued" }),
      JSON.stringify({ runId: "run-1", sequence: 1, stage: "completed" })
    ].join("\n") + "\n",
    "utf8"
  );

  const report = await buildCampaignReport({
    projectRoot,
    campaignId: "test-campaign",
    outputPath: "artifacts/report/campaign-report.json",
    scorePaths: ["artifacts/run-1/score-result.json"]
  });

  assert.equal(report.summary.totalRuns, 1);
  assert.equal(report.summary.counts.pass, 1);
  assert.equal(report.summary.telemetryEvents, 2);
  assert.equal(report.summary.evidenceGapCount, 0);
  assert.equal(report.runs[0]?.evidenceRefs.find((ref) => ref.label === "evidence")?.exists, true);

  const persisted = JSON.parse(await readFile(join(projectRoot, "artifacts", "report", "campaign-report.json"), "utf8"));
  assert.equal(persisted.campaignId, "test-campaign");

  await writeCampaignReportMarkdown("artifacts/report/campaign-report.md", report, projectRoot);
  const markdown = await readFile(join(projectRoot, "artifacts", "report", "campaign-report.md"), "utf8");
  assert.match(markdown, /Campaign Report: test-campaign/);
  assert.match(markdown, /run-1/);
});

test("campaign report keeps missing evidence visible", async () => {
  const projectRoot = await mkdtemp(join(tmpdir(), "campaign-report-gap-"));
  await mkdir(join(projectRoot, "artifacts", "run-gap"), { recursive: true });
  await writeFile(
    join(projectRoot, "artifacts", "run-gap", "score-result.json"),
    JSON.stringify(
      {
        runId: "run-gap",
        taskId: "fixture.refactor.002",
        status: "fail",
        evidenceRef: "artifacts/run-gap/missing-evidence.json",
        components: { oraclePassed: false }
      },
      null,
      2
    ) + "\n",
    "utf8"
  );

  const report = await buildCampaignReport({
    projectRoot,
    scorePaths: ["artifacts/run-gap/score-result.json"]
  });

  assert.equal(report.summary.counts.fail, 1);
  assert.equal(report.summary.evidenceGapCount, 1);
  assert.equal(report.evidenceGaps[0]?.label, "evidence");
});
