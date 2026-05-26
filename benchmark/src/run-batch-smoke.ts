import { runSampleBatch } from "./batch-runner.ts";

const image = process.env.BENCHMARK_DOCKER_IMAGE ?? "test-nestjs-app:latest";
const report = await runSampleBatch({
  manifestPath: "fixtures/swe-bench-local-sample.json",
  image,
  batchId: "sample-batch-001"
});

console.log(`${report.batchId}: pass=${report.counts.pass} fail=${report.counts.fail} infra-fail=${report.counts["infra-fail"]} quarantined=${report.counts.quarantined}`);
console.log(`  report: artifacts/${report.batchId}/batch-report.json`);

if (report.counts.pass < 1 || report.counts.fail > 0 || report.counts["infra-fail"] > 0) {
  process.exitCode = 1;
}
