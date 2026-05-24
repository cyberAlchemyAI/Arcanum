import type { AgentInvocation, AgentResult, TaskDefinition } from "./schemas.ts";

export interface AgentRunContext {
  task: TaskDefinition;
  invocation: AgentInvocation;
}

export interface AgentAdapter {
  readonly id: string;
  run(context: AgentRunContext): Promise<AgentResult>;
}

export type MockAdapterMode = "patch" | "no-patch" | "error" | "timeout";

export interface MockAgentAdapterOptions {
  mode?: MockAdapterMode;
  patchArtifactPath?: string;
  errorMessage?: string;
}

export class MockAgentAdapter implements AgentAdapter {
  readonly id = "mock-agent";
  private readonly options: MockAgentAdapterOptions;

  constructor(options: MockAgentAdapterOptions = {}) {
    this.options = options;
  }

  async run(context: AgentRunContext): Promise<AgentResult> {
    const mode = this.options.mode ?? "patch";
    const base = {
      runId: context.invocation.runId,
      taskId: context.task.id
    };

    if (mode === "patch") {
      return {
        ...base,
        status: "patch",
        patchArtifactPath: this.options.patchArtifactPath ?? `artifacts/${context.invocation.runId}/patch.diff`
      };
    }

    if (mode === "error") {
      return {
        ...base,
        status: "error",
        errorMessage: this.options.errorMessage ?? "mock adapter error"
      };
    }

    if (mode === "timeout") {
      return {
        ...base,
        status: "timeout",
        errorMessage: this.options.errorMessage ?? "mock adapter timeout"
      };
    }

    return {
      ...base,
      status: "no-patch"
    };
  }
}
