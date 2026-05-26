import { strict as assert } from "node:assert";
import { mkdir, mkdtemp, readFile, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";

import {
  DEFAULT_SMELLBENCH_DATASET,
  loadSmellBenchCandidateManifest,
  materializeSmellBenchCandidateManifest,
  parseSmellBenchConsoleMetrics,
  writeSmellBenchScore
} from "../src/smellbench.ts";

test("SmellBench default dataset targets hard scikit-learn classification", () => {
  assert.equal(DEFAULT_SMELLBENCH_DATASET, "CodeSmells_Scikit_architectural_hard_classification");
});

test("SmellBench manifest validator rejects missing patch file", async () => {
  const projectRoot = await mkdtemp(join(tmpdir(), "smellbench-manifest-missing-"));
  await mkdir(join(projectRoot, "fixtures"), { recursive: true });
  await writeFile(
    join(projectRoot, "fixtures", "smellbench-agent-patches.json"),
    '[{"taskId":"smellbench-hard-0001","modelNameOrPath":"codex-local-smoke","patchArtifactPath":"artifacts/smellbench-agent-smoke/smellbench-hard-0001/patch.diff"}]\n',
    "utf8"
  );

  await assert.rejects(loadSmellBenchCandidateManifest("fixtures/smellbench-agent-patches.json", projectRoot), /ENOENT/);
});

test("SmellBench manifest validator rejects empty patch file", async () => {
  const projectRoot = await mkdtemp(join(tmpdir(), "smellbench-manifest-empty-"));
  await mkdir(join(projectRoot, "fixtures"), { recursive: true });
  await mkdir(join(projectRoot, "artifacts", "smellbench-agent-smoke", "smellbench-hard-0001"), { recursive: true });
  await writeFile(join(projectRoot, "artifacts", "smellbench-agent-smoke", "smellbench-hard-0001", "patch.diff"), "\n", "utf8");
  await writeFile(
    join(projectRoot, "fixtures", "smellbench-agent-patches.json"),
    '[{"taskId":"smellbench-hard-0001","modelNameOrPath":"codex-local-smoke","patchArtifactPath":"artifacts/smellbench-agent-smoke/smellbench-hard-0001/patch.diff"}]\n',
    "utf8"
  );

  await assert.rejects(
    loadSmellBenchCandidateManifest("fixtures/smellbench-agent-patches.json", projectRoot),
    /empty/
  );
});

test("SmellBench manifest materializer writes candidate contract", async () => {
  const projectRoot = await mkdtemp(join(tmpdir(), "smellbench-manifest-contract-"));
  await mkdir(join(projectRoot, "artifacts", "smellbench-agent-smoke", "smellbench-hard-0001"), { recursive: true });
  await mkdir(
    join(
      projectRoot,
      "artifacts",
      "smellbench-contract-probe",
      "extracted",
      "ExperimentsReproductionPackage",
      "Dataset Builder",
      "result_dataset",
      "scikitlearn_1.7.2_baseline"
    ),
    { recursive: true }
  );
  await writeFile(
    join(projectRoot, "artifacts", "smellbench-agent-smoke", "smellbench-hard-0001", "patch.diff"),
    "diff --git a/a.py b/a.py\n",
    "utf8"
  );
  await writeFile(
    join(
      projectRoot,
      "artifacts",
      "smellbench-contract-probe",
      "extracted",
      "ExperimentsReproductionPackage",
      "Dataset Builder",
      "result_dataset",
      "scikitlearn_1.7.2_baseline",
      "CodeSmells_Scikit_architectural_hard_classification.csv"
    ),
    'Type,Name,Description,File,Module/Class,Line Number,Severity,scattered_modules,improper_repeats,unstable_out,unstable_in,god_public_funcs,redundant_similarity,cycle_strength,LLM_difficulty_rule\nArchitectural,Scattered Functionality,"Function, with comma",file.py,module,,medium,10.0,,,,,,,hard\n',
    "utf8"
  );

  const manifestPath = await materializeSmellBenchCandidateManifest({
    projectRoot,
    runId: "smellbench-test",
    candidates: [
      {
        taskId: "smellbench-hard-0001",
        modelNameOrPath: "codex-local-smoke",
        patchArtifactPath: "artifacts/smellbench-agent-smoke/smellbench-hard-0001/patch.diff"
      }
    ]
  });

  const manifest = JSON.parse(await readFile(manifestPath, "utf8")) as Array<Record<string, unknown>>;
  assert.equal(manifest[0]?.taskId, "smellbench-hard-0001");
  assert.equal(manifest[0]?.source, "harness-local");
  assert.equal(manifest[0]?.patchBytes, 25);
});

test("SmellBench score importer maps positive effectiveness to pass", async () => {
  const projectRoot = await mkdtemp(join(tmpdir(), "smellbench-score-pass-"));
  const officialDir = join(projectRoot, "artifacts", "run-pass", "official-or-upstream-results");
  await mkdir(join(officialDir, "logs"), { recursive: true });
  await writeFile(join(officialDir, "logs", "evaluator-stdout.txt"), "  Overall Effectiveness:    1.0000\n", "utf8");
  await writeFile(join(officialDir, "report.xlsx"), "fake\n", "utf8");

  const score = await writeSmellBenchScore({ projectRoot, runId: "run-pass", taskId: "smellbench-hard-0001" });

  assert.equal(score.status, "pass");
  assert.equal(score.resolved, true);
});

test("SmellBench score importer maps zero effectiveness to fail", async () => {
  const projectRoot = await mkdtemp(join(tmpdir(), "smellbench-score-fail-"));
  const officialDir = join(projectRoot, "artifacts", "run-fail", "official-or-upstream-results");
  await mkdir(join(officialDir, "logs"), { recursive: true });
  await writeFile(join(officialDir, "logs", "evaluator-stdout.txt"), "  Overall Effectiveness:    0.0000\n", "utf8");
  await writeFile(join(officialDir, "report.xlsx"), "fake\n", "utf8");

  const score = await writeSmellBenchScore({ projectRoot, runId: "run-fail", taskId: "smellbench-hard-0001" });

  assert.equal(score.status, "fail");
  assert.equal(score.resolved, false);
});

test("SmellBench score importer maps missing files to infra-fail", async () => {
  const projectRoot = await mkdtemp(join(tmpdir(), "smellbench-score-infra-"));

  const score = await writeSmellBenchScore({ projectRoot, runId: "run-infra", taskId: "smellbench-hard-0001" });

  assert.equal(score.status, "infra-fail");
  assert.equal(score.resolved, null);
  assert.match(score.errorMessage ?? "", /missing/);
});

test("SmellBench console parser extracts official evaluator metrics", () => {
  const metrics = parseSmellBenchConsoleMetrics(`
  Tasks Attempted:          1
  True Positives:           0
  Failed Repairs:           1
  Weighted Repair Score:    0.0000
  Overall Effectiveness:    0.0000
`);
  assert.equal(metrics.tasksAttempted, 1);
  assert.equal(metrics.failedRepairs, 1);
  assert.equal(metrics.truePositives, 0);
  assert.equal(metrics.weightedRepairScore, 0);
  assert.equal(metrics.overallEffectiveness, 0);
});
