export interface HarnessSkeleton {
  name: string;
  status: "skeleton";
  kernel: "benchmark-run";
}

export const harnessSkeleton: HarnessSkeleton = {
  name: "agentic-tech-debt-optimization-harness",
  status: "skeleton",
  kernel: "benchmark-run"
};

export * from "./agent-adapter.ts";
export * from "./batch-runner.ts";
export * from "./campaign-report.ts";
export * from "./dashboard-api.ts";
export * from "./docker-evaluator.ts";
export * from "./official-swebench.ts";
export * from "./run-kernel.ts";
export * from "./schemas.ts";
export * from "./swe-bench-provider.ts";
