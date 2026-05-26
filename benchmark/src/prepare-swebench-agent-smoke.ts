import { mkdir } from "node:fs/promises";
import { dirname } from "node:path";

import { prepareSweBenchLiteAgentSmoke } from "./official-swebench.ts";

const instanceId = process.env.SWEBENCH_INSTANCE_ID ?? "astropy__astropy-14365";
const runnerImage = process.env.SWEBENCH_RUNNER_IMAGE ?? "swebench-official-runner";
const manifestPath = process.env.SWEBENCH_PREDICTION_SOURCE ?? "fixtures/swebench-lite-agent-patches.json";
const writeManifest = process.env.SWEBENCH_WRITE_MANIFEST === "1";

if (writeManifest) {
  await mkdir(dirname(manifestPath), { recursive: true });
}

const result = await prepareSweBenchLiteAgentSmoke({
  instanceId,
  runnerImage,
  manifestPath,
  writeManifest,
  modelNameOrPath: "codex-local-smoke"
});

console.log(`prepared SWE-bench Lite agent smoke for ${result.instance.instance_id}`);
console.log(`  task brief: ${result.taskBriefPath}`);
console.log(`  checkout: ${result.checkoutDir}`);
console.log(`  patch artifact: ${result.patchArtifactPath}`);
if (result.manifestPath) {
  console.log(`  manifest: ${result.manifestPath}`);
} else {
  console.log("  manifest: not written; set SWEBENCH_WRITE_MANIFEST=1 after patch.diff exists");
}
