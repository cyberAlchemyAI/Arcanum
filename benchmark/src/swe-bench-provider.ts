import { readFile } from "node:fs/promises";
import { resolve } from "node:path";

import type { TaskDefinition } from "./schemas.ts";
import { validateTaskDefinition } from "./schemas.ts";

export interface SweBenchSampleRecord {
  id: string;
  suite: string;
  upstreamId: string;
  objective: string;
  fixturePath: string;
  patchPath: string;
  labels: string[];
  oracleCommand: string;
  expectedExitCode: number;
  timeoutMs: number;
  datasetPath: string;
  filterNote: string;
}

export async function loadSweBenchSampleManifest(path: string, projectRoot = process.cwd()): Promise<TaskDefinition[]> {
  const manifestPath = resolve(projectRoot, path);
  const records = JSON.parse(await readFile(manifestPath, "utf8")) as SweBenchSampleRecord[];
  return records.map((record) => normalizeSweBenchSample(record, path));
}

export function normalizeSweBenchSample(record: SweBenchSampleRecord, manifestPath: string): TaskDefinition {
  const task: TaskDefinition = {
    id: `swe.local.${record.id}`,
    objective: record.objective,
    source: {
      suite: record.suite,
      upstreamId: record.upstreamId
    },
    repository: {
      kind: "docker",
      repoRef: record.fixturePath,
      fixturePath: record.fixturePath
    },
    labels: record.labels,
    oracle: {
      type: "semantic",
      command: record.oracleCommand,
      expectedExitCode: record.expectedExitCode
    },
    evaluatorProfile: {
      kind: "docker",
      timeoutMs: record.timeoutMs
    },
    metadata: {
      sampleManifestPath: manifestPath,
      datasetPath: record.datasetPath,
      filterNote: record.filterNote,
      patchPath: record.patchPath,
      fixturePath: record.fixturePath
    }
  };

  const validation = validateTaskDefinition(task);
  if (!validation.ok) {
    throw new Error(`invalid normalized SWE-bench sample ${record.id}: ${validation.issues.join("; ")}`);
  }
  return task;
}
