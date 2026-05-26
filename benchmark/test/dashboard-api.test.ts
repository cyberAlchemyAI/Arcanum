import { strict as assert } from "node:assert";
import test from "node:test";

import type { CampaignReport } from "../src/campaign-report.ts";
import { dashboardDataFromReport } from "../src/dashboard-api.ts";

test("dashboard data exposes summary, run list, details, components, and telemetry", () => {
  const report: CampaignReport = {
    campaignId: "campaign",
    generatedAt: "2026-05-25T00:00:00.000Z",
    artifactsRoot: "artifacts",
    summary: {
      totalRuns: 1,
      counts: { pass: 1, fail: 0, "infra-fail": 0, quarantined: 0, unknown: 0 },
      resolved: { true: 1, false: 0, unknown: 0 },
      telemetryEvents: 2,
      evidenceGapCount: 0
    },
    runs: [
      {
        runId: "run-1",
        taskId: "task-1",
        suite: "fixture-local",
        status: "pass",
        resolved: true,
        scorePath: "artifacts/run-1/score-result.json",
        evidenceRefs: [
          { label: "score", path: "artifacts/run-1/score-result.json", exists: true },
          { label: "evidence", path: "artifacts/run-1/oracle-evidence.json", exists: true }
        ],
        components: { oraclePassed: true },
        telemetry: { path: "artifacts/run-1/telemetry.jsonl", eventCount: 2, firstStage: "queued", lastStage: "completed" }
      }
    ],
    evidenceGaps: []
  };

  const data = dashboardDataFromReport(report);

  assert.equal(data.summary.totalRuns, 1);
  assert.equal(data.summary.pass, 1);
  assert.equal(data.runs[0]?.telemetryEvents, 2);
  assert.equal(data.runDetails["run-1"]?.scoreComponents.oraclePassed, true);
  assert.equal(data.runDetails["run-1"]?.evidenceRefs.length, 2);
});
