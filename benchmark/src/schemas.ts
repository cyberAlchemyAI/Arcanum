export type OracleType = "semantic" | "structural" | "performance" | "experimental";

export type RunStatus =
  | "queued"
  | "preparing"
  | "invoking"
  | "applying-patch"
  | "evaluating"
  | "scoring"
  | "completed"
  | "failed"
  | "quarantined";

export type EvidenceStatus = "pass" | "fail" | "timeout" | "infra-fail" | "quarantined";

export interface TaskDefinition {
  id: string;
  objective: string;
  source: {
    suite: string;
    upstreamId?: string;
  };
  repository: {
    kind: "fixture" | "docker";
    fixturePath?: string;
    repoRef?: string;
  };
  labels: string[];
  oracle: {
    type: OracleType;
    command: string;
    expectedExitCode: number;
  };
  evaluatorProfile: {
    kind: "fixture-local" | "docker" | "performance-worker";
    timeoutMs: number;
  };
  metadata?: Record<string, unknown>;
}

export interface AgentInvocation {
  runId: string;
  taskId: string;
  adapterId: string;
  contextBudgetTokens: number;
  timeoutMs: number;
}

export interface AgentResult {
  runId: string;
  taskId: string;
  status: "patch" | "no-patch" | "error" | "timeout";
  patchArtifactPath?: string;
  errorMessage?: string;
}

export interface OracleEvidence {
  runId: string;
  taskId: string;
  oracleType: OracleType;
  status: EvidenceStatus;
  command: string;
  exitCode: number | null;
  durationMs: number;
  artifacts: {
    stdoutPath?: string;
    stderrPath?: string;
  };
  metrics?: Record<string, number>;
}

export interface ScoreResult {
  runId: string;
  taskId: string;
  status: "pass" | "fail" | "infra-fail" | "quarantined";
  evidenceRef: string;
  components: Record<string, number | boolean>;
}

export interface TelemetryEvent {
  runId: string;
  sequence: number;
  stage: RunStatus;
  message: string;
  timestamp: string;
}

export interface RunAttempt {
  runId: string;
  task: TaskDefinition;
  invocation?: AgentInvocation;
  agentResult?: AgentResult;
  oracleEvidence?: OracleEvidence;
  scoreResult?: ScoreResult;
  telemetry: TelemetryEvent[];
}

export interface ValidationResult {
  ok: boolean;
  issues: string[];
}

export function validateTaskDefinition(candidate: unknown): ValidationResult {
  const issues: string[] = [];
  const task = asRecord(candidate);

  requireString(task, "id", issues);
  requireString(task, "objective", issues);
  requireStringArray(task, "labels", issues);

  const source = requireRecord(task, "source", issues);
  if (source) {
    requireString(source, "suite", issues, "source.suite");
  }

  const repository = requireRecord(task, "repository", issues);
  if (repository) {
    const kind = requireString(repository, "kind", issues, "repository.kind");
    if (kind && !["fixture", "docker"].includes(kind)) {
      issues.push("repository.kind must be fixture or docker");
    }
    if (kind === "fixture") {
      requireString(repository, "fixturePath", issues, "repository.fixturePath");
    }
    if (kind === "docker") {
      requireString(repository, "repoRef", issues, "repository.repoRef");
    }
  }

  const oracle = requireRecord(task, "oracle", issues);
  if (oracle) {
    const type = requireString(oracle, "type", issues, "oracle.type");
    if (type && !isOracleType(type)) {
      issues.push("oracle.type must be semantic, structural, performance, or experimental");
    }
    requireString(oracle, "command", issues, "oracle.command");
    requireNumber(oracle, "expectedExitCode", issues, "oracle.expectedExitCode");
  }

  const evaluatorProfile = requireRecord(task, "evaluatorProfile", issues);
  if (evaluatorProfile) {
    const kind = requireString(evaluatorProfile, "kind", issues, "evaluatorProfile.kind");
    if (kind && !["fixture-local", "docker", "performance-worker"].includes(kind)) {
      issues.push("evaluatorProfile.kind must be fixture-local, docker, or performance-worker");
    }
    requirePositiveNumber(evaluatorProfile, "timeoutMs", issues, "evaluatorProfile.timeoutMs");
  }

  return { ok: issues.length === 0, issues };
}

export function validateOracleEvidence(candidate: unknown): ValidationResult {
  const issues: string[] = [];
  const evidence = asRecord(candidate);

  requireString(evidence, "runId", issues);
  requireString(evidence, "taskId", issues);
  const oracleType = requireString(evidence, "oracleType", issues);
  if (oracleType && !isOracleType(oracleType)) {
    issues.push("oracleType must be semantic, structural, performance, or experimental");
  }

  const status = requireString(evidence, "status", issues);
  if (status && !["pass", "fail", "timeout", "infra-fail", "quarantined"].includes(status)) {
    issues.push("status must be pass, fail, timeout, infra-fail, or quarantined");
  }

  requireString(evidence, "command", issues);
  if (evidence.exitCode !== null) {
    requireNumber(evidence, "exitCode", issues);
  }
  requirePositiveNumber(evidence, "durationMs", issues);
  requireRecord(evidence, "artifacts", issues);

  return { ok: issues.length === 0, issues };
}

function asRecord(candidate: unknown): Record<string, unknown> {
  return isRecord(candidate) ? candidate : {};
}

function isRecord(candidate: unknown): candidate is Record<string, unknown> {
  return typeof candidate === "object" && candidate !== null && !Array.isArray(candidate);
}

function isOracleType(value: string): value is OracleType {
  return ["semantic", "structural", "performance", "experimental"].includes(value);
}

function requireRecord(
  record: Record<string, unknown>,
  key: string,
  issues: string[],
  label = key
): Record<string, unknown> | null {
  const value = record[key];
  if (!isRecord(value)) {
    issues.push(`${label} must be an object`);
    return null;
  }
  return value;
}

function requireString(
  record: Record<string, unknown>,
  key: string,
  issues: string[],
  label = key
): string | null {
  const value = record[key];
  if (typeof value !== "string" || value.length === 0) {
    issues.push(`${label} must be a non-empty string`);
    return null;
  }
  return value;
}

function requireNumber(record: Record<string, unknown>, key: string, issues: string[], label = key): void {
  if (typeof record[key] !== "number" || !Number.isFinite(record[key])) {
    issues.push(`${label} must be a finite number`);
  }
}

function requirePositiveNumber(
  record: Record<string, unknown>,
  key: string,
  issues: string[],
  label = key
): void {
  const value = record[key];
  if (typeof value !== "number" || !Number.isFinite(value) || value <= 0) {
    issues.push(`${label} must be a positive number`);
  }
}

function requireStringArray(record: Record<string, unknown>, key: string, issues: string[], label = key): void {
  const value = record[key];
  if (!Array.isArray(value) || value.some((item) => typeof item !== "string" || item.length === 0)) {
    issues.push(`${label} must be an array of non-empty strings`);
  }
}
