import { strict as assert } from "node:assert";
import { mkdir, mkdtemp, readFile, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";

import {
  DEFAULT_SWEBENCH_DATASET,
  DEFAULT_SWEBENCH_SPLIT,
  writeOfficialSweBenchScore,
  writeSweBenchAgentPatchManifest,
  writeSweBenchPredictionsJsonl
} from "../src/official-swebench.ts";

test("official SWE-bench default dataset targets Lite", () => {
  assert.equal(DEFAULT_SWEBENCH_DATASET, "princeton-nlp/SWE-bench_Lite");
  assert.equal(DEFAULT_SWEBENCH_SPLIT, "test");
});

test("prediction writer emits official SWE-bench JSONL shape", async () => {
  const dir = await mkdtemp(join(tmpdir(), "swebench-predictions-"));
  const patchPath = join(dir, "patch.diff");
  const outputPath = join(dir, "predictions.jsonl");
  await writeFile(patchPath, "diff --git a/example.py b/example.py\n", "utf8");

  await writeSweBenchPredictionsJsonl(
    [
      {
        instanceId: "sympy__sympy-20590",
        modelNameOrPath: "mock-agent",
        patchArtifactPath: patchPath
      }
    ],
    outputPath
  );

  const [line] = (await readFile(outputPath, "utf8")).trim().split("\n");
  const prediction = JSON.parse(line ?? "{}") as Record<string, unknown>;
  assert.equal(prediction.instance_id, "sympy__sympy-20590");
  assert.equal(prediction.model_name_or_path, "mock-agent");
  assert.equal(prediction.model_patch, "diff --git a/example.py b/example.py\n");
});

test("prediction writer blocks when no instance-aligned patches exist", async () => {
  const dir = await mkdtemp(join(tmpdir(), "swebench-empty-"));
  await assert.rejects(
    writeSweBenchPredictionsJsonl([], join(dir, "predictions.jsonl")),
    /requires at least one instance-aligned patch/
  );
});

test("agent patch manifest rejects missing patch artifact", async () => {
  const projectRoot = await mkdtemp(join(tmpdir(), "swebench-manifest-missing-"));

  await assert.rejects(
    writeSweBenchAgentPatchManifest(
      [
        {
          instanceId: "astropy__astropy-14365",
          modelNameOrPath: "codex-local-smoke",
          patchArtifactPath: "missing.diff"
        }
      ],
      "fixtures/swebench-lite-agent-patches.json",
      projectRoot
    ),
    /ENOENT/
  );
});

test("agent patch manifest rejects empty patch artifact", async () => {
  const projectRoot = await mkdtemp(join(tmpdir(), "swebench-manifest-empty-"));
  await writeFile(join(projectRoot, "empty.diff"), "\n", "utf8");

  await assert.rejects(
    writeSweBenchAgentPatchManifest(
      [
        {
          instanceId: "astropy__astropy-14365",
          modelNameOrPath: "codex-local-smoke",
          patchArtifactPath: "empty.diff"
        }
      ],
      "fixtures/swebench-lite-agent-patches.json",
      projectRoot
    ),
    /empty/
  );
});

test("agent patch manifest writes prediction-compatible contract", async () => {
  const projectRoot = await mkdtemp(join(tmpdir(), "swebench-manifest-contract-"));
  await mkdir(join(projectRoot, "fixtures"), { recursive: true });
  await writeFile(join(projectRoot, "patch.diff"), "diff --git a/a.py b/a.py\n", "utf8");

  await writeSweBenchAgentPatchManifest(
    [
      {
        instanceId: "astropy__astropy-14365",
        modelNameOrPath: "codex-local-smoke",
        patchArtifactPath: "patch.diff"
      }
    ],
    "fixtures/swebench-lite-agent-patches.json",
    projectRoot
  );

  const manifest = JSON.parse(
    await readFile(join(projectRoot, "fixtures", "swebench-lite-agent-patches.json"), "utf8")
  ) as Array<Record<string, unknown>>;
  assert.deepEqual(manifest, [
    {
      instanceId: "astropy__astropy-14365",
      modelNameOrPath: "codex-local-smoke",
      patchArtifactPath: "patch.diff"
    }
  ]);
});

test("official score importer maps resolved true to pass", async () => {
  const projectRoot = await mkdtemp(join(tmpdir(), "swebench-score-pass-"));
  const officialDir = join(projectRoot, "artifacts", "run-pass", "official-evaluation-results");
  await mkdir(officialDir, { recursive: true });
  await writeFile(join(officialDir, "results.json"), "{}\n", "utf8");
  await writeFile(join(officialDir, "instance_results.jsonl"), '{"instance_id":"sympy__sympy-20590","resolved":true}\n', "utf8");

  const score = await writeOfficialSweBenchScore({
    projectRoot,
    runId: "run-pass",
    instanceId: "sympy__sympy-20590"
  });

  assert.equal(score.status, "pass");
  assert.equal(score.resolved, true);
});

test("official score importer maps resolved false to fail", async () => {
  const projectRoot = await mkdtemp(join(tmpdir(), "swebench-score-fail-"));
  const officialDir = join(projectRoot, "artifacts", "run-fail", "official-evaluation-results");
  await mkdir(officialDir, { recursive: true });
  await writeFile(join(officialDir, "results.json"), "{}\n", "utf8");
  await writeFile(join(officialDir, "instance_results.jsonl"), '{"instance_id":"sympy__sympy-20590","resolved":false}\n', "utf8");

  const score = await writeOfficialSweBenchScore({
    projectRoot,
    runId: "run-fail",
    instanceId: "sympy__sympy-20590"
  });

  assert.equal(score.status, "fail");
  assert.equal(score.resolved, false);
});

test("official score importer maps missing files to infra-fail", async () => {
  const projectRoot = await mkdtemp(join(tmpdir(), "swebench-score-infra-"));

  const score = await writeOfficialSweBenchScore({
    projectRoot,
    runId: "run-infra",
    instanceId: "sympy__sympy-20590"
  });

  assert.equal(score.status, "infra-fail");
  assert.equal(score.resolved, null);
  assert.match(score.errorMessage ?? "", /missing/);
});
