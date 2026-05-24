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
export * from "./schemas.ts";
