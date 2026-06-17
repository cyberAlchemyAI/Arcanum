import type { FastifyInstance } from "fastify";
import { resolve } from "node:path";

import type { StudioSessionStorePort } from "../application/ports.js";
import { createInMemoryStudioSessionStore } from "../application/session-store.js";
import { createStudioOrchestrationModule } from "../application/studio-orchestration-module.js";
import {
  createUiPrototypingStudioError,
  isUiPrototypingStudioError,
} from "../domain/errors.js";
import type { UiPrototypingStudioErrorCode } from "../domain/errors.js";
import type {
  AnnotationTarget,
  CommentEvent,
  HandoffBundle,
  MutationBatch,
  MutationTask,
  PrototypeVariant,
  RevisionManifestEntry,
  StudioSession,
} from "../domain/models.js";
import { createFileBackedStudioSessionStore } from "../infrastructure/file-studio-session-store.js";

export interface RegisterUiPrototypingStudioRoutesOptions {
  store?: StudioSessionStorePort;
  useInMemoryStore?: boolean;
  storeFilePath?: string;
  projectRootDir?: string;
  featureDocsRootDir?: string;
}

interface InitializeSessionBody {
  requestedVariantCount?: unknown;
  requestedBy?: unknown;
}

interface SubmitPromptBody {
  prompt?: unknown;
  submittedBy?: unknown;
}

interface GenerateVariantsBody {
  requestedBy?: unknown;
}

interface SelectBaselineBody {
  selectedLabel?: unknown;
  requestedBy?: unknown;
}

interface CaptureCommentBody {
  revisionId?: unknown;
  target?: unknown;
  severity?: unknown;
  intent?: unknown;
  note?: unknown;
  createdBy?: unknown;
}

interface SynthesizeMutationBatchBody {
  sourceRevisionId?: unknown;
  requestedBy?: unknown;
}

interface ApproveMutationBatchBody {
  approvedBy?: unknown;
  approvedAt?: unknown;
}

interface ApplyApprovedBatchBody {
  applyRequestedBy?: unknown;
}

interface ExportDesignHandoffBody {
  exportProfile?: unknown;
  requestedBy?: unknown;
}

interface SessionParams {
  sessionId: string;
}

interface SessionBatchParams extends SessionParams {
  batchId: string;
}

interface DraftBatchQuerystring {
  batchId?: string;
}

interface RevisionManifestQuerystring {
  limit?: string;
  newestFirst?: string;
}

/**
 * domainspec:
 *   concept:
 *     id: ui-prototyping-studio.UIPrototypingStudioAPI
 *     type: Interface
 *   edges:
 *     - edge: exposes
 *       to: ui-prototyping-studio.InitializeSession
 *     - edge: exposes
 *       to: ui-prototyping-studio.SubmitPrompt
 *     - edge: exposes
 *       to: ui-prototyping-studio.GenerateVariants
 *     - edge: exposes
 *       to: ui-prototyping-studio.SelectOrCommitBaseline
 *     - edge: exposes
 *       to: ui-prototyping-studio.GetSessionSnapshot
 *     - edge: exposes
 *       to: ui-prototyping-studio.ListSessionVariants
 */
export function registerUiPrototypingStudioRoutes(
  app: FastifyInstance,
  options: RegisterUiPrototypingStudioRoutesOptions = {},
): void {
  const projectRootDir = options.projectRootDir ?? resolve(process.cwd(), "..");
  const featureDocsRootDir =
    options.featureDocsRootDir ??
    resolve(projectRootDir, "docs", "features", "ui-prototyping-studio");

  const store =
    options.store ??
    (options.useInMemoryStore
      ? createInMemoryStudioSessionStore()
      : createFileBackedStudioSessionStore({
          filePath:
            options.storeFilePath ??
            resolve(
              projectRootDir,
              ".data",
              "ui-prototyping-studio-session-store.json",
            ),
        }));

  const orchestration = createStudioOrchestrationModule(store, {
    featureDocsRootDir,
  });

  app.post<{ Body: InitializeSessionBody }>(
    "/api/ui-prototyping-studio/sessions",
    async (request, reply) => {
      try {
        assertWriteScope(request.headers["x-scopes"]);

        const session = orchestration.initializeSession({
          requestedVariantCount: parseOptionalVariantCount(
            request.body.requestedVariantCount,
          ),
          requestedBy: parseActor(request.body.requestedBy, "web-ui"),
        });

        return reply.status(201).send(mapSession(session));
      } catch (error) {
        return handleUiPrototypingStudioError(reply, error);
      }
    },
  );

  app.post<{ Params: SessionParams; Body: SubmitPromptBody }>(
    "/api/ui-prototyping-studio/sessions/:sessionId/prompt",
    async (request, reply) => {
      try {
        assertWriteScope(request.headers["x-scopes"]);

        const session = orchestration.submitPrompt({
          sessionId: request.params.sessionId,
          prompt: parseRequiredString(
            request.body.prompt,
            "PROMPT_REQUIRED",
            "Prompt is required",
            "prompt",
          ),
          submittedBy: parseActor(request.body.submittedBy, "web-ui"),
        });

        return reply.status(200).send(mapSession(session));
      } catch (error) {
        return handleUiPrototypingStudioError(reply, error);
      }
    },
  );

  app.post<{ Params: SessionParams; Body: GenerateVariantsBody }>(
    "/api/ui-prototyping-studio/sessions/:sessionId/variants/generate",
    async (request, reply) => {
      try {
        assertWriteScope(request.headers["x-scopes"]);

        const result = orchestration.generateVariants({
          sessionId: request.params.sessionId,
          requestedBy: parseActor(request.body.requestedBy, "web-ui"),
        });

        return reply.status(200).send({
          session: mapSession(result.session),
          variants: result.variants.map((variant) => mapVariant(variant)),
        });
      } catch (error) {
        return handleUiPrototypingStudioError(reply, error);
      }
    },
  );

  app.post<{ Params: SessionParams; Body: SelectBaselineBody }>(
    "/api/ui-prototyping-studio/sessions/:sessionId/baseline",
    async (request, reply) => {
      try {
        assertWriteScope(request.headers["x-scopes"]);

        const result = orchestration.selectOrCommitBaseline({
          sessionId: request.params.sessionId,
          selectedLabel: parseOptionalString(request.body.selectedLabel),
          requestedBy: parseActor(request.body.requestedBy, "web-ui"),
        });

        return reply.status(200).send({
          session: mapSession(result.session),
          variants: result.variants.map((variant) => mapVariant(variant)),
        });
      } catch (error) {
        return handleUiPrototypingStudioError(reply, error);
      }
    },
  );

  app.post<{ Params: SessionParams; Body: CaptureCommentBody }>(
    "/api/ui-prototyping-studio/sessions/:sessionId/comments",
    async (request, reply) => {
      try {
        assertWriteScope(request.headers["x-scopes"]);

        const comment = orchestration.captureCommentEvent({
          sessionId: request.params.sessionId,
          revisionId: parseRequiredString(
            request.body.revisionId,
            "SOURCE_REVISION_INVALID",
            "Revision ID is required",
            "revisionId",
          ),
          target: parseAnnotationTarget(request.body.target),
          severity: parseRequiredString(
            request.body.severity,
            "COMMENT_SCHEMA_INVALID",
            "Severity is required",
            "severity",
          ),
          intent: parseRequiredString(
            request.body.intent,
            "COMMENT_SCHEMA_INVALID",
            "Intent is required",
            "intent",
          ),
          note: parseRequiredString(
            request.body.note,
            "COMMENT_SCHEMA_INVALID",
            "Note is required",
            "note",
          ),
          createdBy: parseActor(request.body.createdBy, "web-ui"),
        });

        return reply.status(201).send(mapComment(comment));
      } catch (error) {
        return handleUiPrototypingStudioError(reply, error);
      }
    },
  );

  app.post<{ Params: SessionParams; Body: SynthesizeMutationBatchBody }>(
    "/api/ui-prototyping-studio/sessions/:sessionId/mutation-batches/synthesize",
    async (request, reply) => {
      try {
        assertWriteScope(request.headers["x-scopes"]);

        const result = orchestration.synthesizeMutationBatch({
          sessionId: request.params.sessionId,
          sourceRevisionId: parseRequiredString(
            request.body.sourceRevisionId,
            "SOURCE_REVISION_INVALID",
            "Source revision is required",
            "sourceRevisionId",
          ),
          requestedBy: parseActor(request.body.requestedBy, "web-ui"),
        });

        return reply.status(201).send({
          session: mapSession(result.session),
          batch: mapBatch(result.batch),
        });
      } catch (error) {
        return handleUiPrototypingStudioError(reply, error);
      }
    },
  );

  app.post<{ Params: SessionBatchParams; Body: ApproveMutationBatchBody }>(
    "/api/ui-prototyping-studio/sessions/:sessionId/mutation-batches/:batchId/approve",
    async (request, reply) => {
      try {
        assertWriteScope(request.headers["x-scopes"]);

        const result = orchestration.approveMutationBatch({
          sessionId: request.params.sessionId,
          batchId: request.params.batchId,
          approvedBy: parseRequiredString(
            request.body.approvedBy,
            "APPROVAL_METADATA_REQUIRED",
            "Approval identity is required",
            "approvedBy",
          ),
          approvedAt: parseRequiredString(
            request.body.approvedAt,
            "APPROVAL_METADATA_REQUIRED",
            "Approval timestamp is required",
            "approvedAt",
          ),
        });

        return reply.status(200).send({
          session: mapSession(result.session),
          batch: mapBatch(result.batch),
        });
      } catch (error) {
        return handleUiPrototypingStudioError(reply, error);
      }
    },
  );

  app.post<{ Params: SessionBatchParams; Body: ApplyApprovedBatchBody }>(
    "/api/ui-prototyping-studio/sessions/:sessionId/mutation-batches/:batchId/apply",
    async (request, reply) => {
      try {
        assertWriteScope(request.headers["x-scopes"]);

        const result = orchestration.applyApprovedBatch({
          sessionId: request.params.sessionId,
          batchId: request.params.batchId,
          applyRequestedBy: parseActor(request.body.applyRequestedBy, "web-ui"),
        });

        return reply.status(200).send({
          session: mapSession(result.session),
          batch: mapBatch(result.batch),
          revision: mapRevision(result.revision),
        });
      } catch (error) {
        return handleUiPrototypingStudioError(reply, error);
      }
    },
  );

  app.post<{ Params: SessionParams; Body: ExportDesignHandoffBody }>(
    "/api/ui-prototyping-studio/sessions/:sessionId/handoff/export",
    async (request, reply) => {
      try {
        assertWriteScope(request.headers["x-scopes"]);

        const result = orchestration.exportDesignHandoff({
          sessionId: request.params.sessionId,
          exportProfile: parseOptionalString(request.body.exportProfile),
          requestedBy: parseActor(request.body.requestedBy, "web-ui"),
        });

        return reply.status(200).send({
          session: mapSession(result.session),
          bundle: mapHandoffBundle(result.bundle),
        });
      } catch (error) {
        return handleUiPrototypingStudioError(reply, error);
      }
    },
  );

  app.get<{ Params: SessionParams }>(
    "/api/ui-prototyping-studio/sessions/:sessionId",
    async (request, reply) => {
      try {
        assertReadScope(request.headers["x-scopes"]);
        const session = orchestration.getSessionSnapshot({
          sessionId: request.params.sessionId,
        });

        return reply.status(200).send(mapSession(session));
      } catch (error) {
        return handleUiPrototypingStudioError(reply, error);
      }
    },
  );

  app.get<{ Params: SessionParams }>(
    "/api/ui-prototyping-studio/sessions/:sessionId/variants",
    async (request, reply) => {
      try {
        assertReadScope(request.headers["x-scopes"]);
        const variants = orchestration.listSessionVariants({
          sessionId: request.params.sessionId,
        });

        return reply.status(200).send({
          variants: variants.map((variant) => mapVariant(variant)),
        });
      } catch (error) {
        return handleUiPrototypingStudioError(reply, error);
      }
    },
  );

  app.get<{ Params: SessionParams; Querystring: DraftBatchQuerystring }>(
    "/api/ui-prototyping-studio/sessions/:sessionId/mutation-batches/draft",
    async (request, reply) => {
      try {
        assertReadScope(request.headers["x-scopes"]);
        const batch = orchestration.getDraftMutationBatch({
          sessionId: request.params.sessionId,
          batchId: parseOptionalString(request.query.batchId),
        });

        return reply.status(200).send(mapBatch(batch));
      } catch (error) {
        return handleUiPrototypingStudioError(reply, error);
      }
    },
  );

  app.get<{ Params: SessionParams; Querystring: RevisionManifestQuerystring }>(
    "/api/ui-prototyping-studio/sessions/:sessionId/revisions",
    async (request, reply) => {
      try {
        assertReadScope(request.headers["x-scopes"]);
        const entries = orchestration.listRevisionManifest({
          sessionId: request.params.sessionId,
          limit: parseOptionalPositiveInt(request.query.limit),
          newestFirst: parseOptionalBoolean(request.query.newestFirst),
        });

        return reply.status(200).send({
          entries: entries.map((entry) => mapRevision(entry)),
        });
      } catch (error) {
        return handleUiPrototypingStudioError(reply, error);
      }
    },
  );

  app.get<{ Params: SessionParams }>(
    "/api/ui-prototyping-studio/sessions/:sessionId/handoff",
    async (request, reply) => {
      try {
        assertReadScope(request.headers["x-scopes"]);
        const bundle = orchestration.getHandoffBundle({
          sessionId: request.params.sessionId,
        });

        return reply.status(200).send(mapHandoffBundle(bundle));
      } catch (error) {
        return handleUiPrototypingStudioError(reply, error);
      }
    },
  );
}

function mapComment(comment: CommentEvent) {
  return {
    commentId: comment.commentId,
    sessionId: comment.sessionId,
    revisionId: comment.revisionId,
    target: {
      ...comment.target,
    },
    severity: comment.severity,
    intent: comment.intent,
    note: comment.note,
    createdBy: comment.createdBy,
    createdAt: comment.createdAt,
  };
}

function mapSession(session: StudioSession) {
  return {
    sessionId: session.sessionId,
    prompt: session.prompt,
    variantCount: session.variantCount,
    variantLabels: session.variantLabels,
    baseline: session.baseline,
    revisionHeadId: session.revisionHeadId,
    selectionGate: session.selectionGate,
    applyGate: session.applyGate,
    integration: session.integration,
    state: session.state,
  };
}

function mapTask(task: MutationTask) {
  return {
    taskId: task.taskId,
    target: task.target,
    intent: task.intent,
    changeType: task.changeType,
    acceptanceText: task.acceptanceText,
    priority: task.priority,
  };
}

function mapBatch(batch: MutationBatch) {
  return {
    batchId: batch.batchId,
    sessionId: batch.sessionId,
    sourceRevisionId: batch.sourceRevisionId,
    status: batch.status,
    generatedFromCommentIds: [...batch.generatedFromCommentIds],
    tasks: batch.tasks.map((task) => mapTask(task)),
    approval: {
      ...batch.approval,
    },
    checksum: batch.checksum,
  };
}

function mapRevision(entry: RevisionManifestEntry) {
  return {
    revisionId: entry.revisionId,
    parentRevisionId: entry.parentRevisionId,
    sessionId: entry.sessionId,
    variantCount: entry.variantCount,
    baseline: {
      ...entry.baseline,
    },
    appliedBatchId: entry.appliedBatchId,
    appliedTaskIds: [...entry.appliedTaskIds],
    unresolvedCommentIds: [...entry.unresolvedCommentIds],
    diffSummary: {
      ...entry.diffSummary,
    },
    createdAt: entry.createdAt,
  };
}

function mapHandoffBundle(bundle: HandoffBundle) {
  return {
    sessionId: bundle.sessionId,
    revisionHeadId: bundle.revisionHeadId,
    baseline: {
      ...bundle.baseline,
    },
    variantCount: bundle.variantCount,
    storyRefs: [...bundle.storyRefs],
    requirementRefs: [...bundle.requirementRefs],
    acceptanceRefs: [...bundle.acceptanceRefs],
    uiSpecRef: bundle.uiSpecRef,
    testSpecRef: bundle.testSpecRef,
  };
}

function mapVariant(variant: PrototypeVariant) {
  return {
    sessionId: variant.sessionId,
    variantLabel: variant.variantLabel,
    htmlArtifactRef: variant.htmlArtifactRef,
    componentsUsed: variant.componentsUsed,
    rationale: variant.rationale,
    tradeoffs: variant.tradeoffs,
    risk: variant.risk,
    status: variant.status,
  };
}

function assertReadScope(rawScopes: unknown): void {
  assertScope(rawScopes, "domainspec.ui-prototyping.read", "Read");
}

function assertWriteScope(rawScopes: unknown): void {
  assertScope(rawScopes, "domainspec.ui-prototyping.write", "Write");
}

function assertScope(
  rawScopes: unknown,
  requiredScope:
    | "domainspec.ui-prototyping.read"
    | "domainspec.ui-prototyping.write",
  label: "Read" | "Write",
): void {
  const scopes = parseScopes(rawScopes);

  if (scopes.length === 0) {
    throw createUiPrototypingStudioError(
      "UPS_AUTH_REQUIRED",
      `${label} scope ${requiredScope} is required`,
      {
        requiredScope,
      },
    );
  }

  if (!scopes.includes(requiredScope)) {
    throw createUiPrototypingStudioError(
      "UPS_AUTH_FORBIDDEN",
      `${label} scope ${requiredScope} is required`,
      {
        requiredScope,
        providedScopes: scopes,
      },
    );
  }
}

function parseScopes(rawScopes: unknown): string[] {
  const values =
    typeof rawScopes === "string"
      ? [rawScopes]
      : Array.isArray(rawScopes)
        ? rawScopes.filter(
            (value): value is string => typeof value === "string",
          )
        : [];

  return values
    .join(" ")
    .split(/[\s,]+/)
    .map((value) => value.trim())
    .filter((value) => value.length > 0);
}

function parseOptionalVariantCount(rawValue: unknown): number | undefined {
  if (rawValue === undefined || rawValue === null) {
    return undefined;
  }

  if (typeof rawValue !== "number" || !Number.isInteger(rawValue)) {
    throw createUiPrototypingStudioError(
      "VARIANT_COUNT_OUT_OF_RANGE",
      "Variant count must be an integer between 1 and 3",
      {
        requestedVariantCount: rawValue,
      },
    );
  }

  return rawValue;
}

function parseRequiredString(
  rawValue: unknown,
  errorCode: UiPrototypingStudioErrorCode,
  message: string,
  field: string,
): string {
  if (typeof rawValue !== "string") {
    throw createUiPrototypingStudioError(errorCode, message, {
      field,
      value: rawValue,
    });
  }

  const normalized = rawValue.trim();
  if (normalized.length === 0) {
    throw createUiPrototypingStudioError(errorCode, message, {
      field,
      value: rawValue,
    });
  }

  return normalized;
}

function parseAnnotationTarget(rawValue: unknown): AnnotationTarget {
  if (!rawValue || typeof rawValue !== "object") {
    throw createUiPrototypingStudioError(
      "COMMENT_SCHEMA_INVALID",
      "Comment target is required",
      {
        field: "target",
      },
    );
  }

  const target = rawValue as Record<string, unknown>;
  const selector = parseRequiredString(
    target.selector,
    "COMMENT_SCHEMA_INVALID",
    "Comment target selector is required",
    "target.selector",
  );
  const elementLabel = parseRequiredString(
    target.elementLabel,
    "COMMENT_SCHEMA_INVALID",
    "Comment target element label is required",
    "target.elementLabel",
  );
  const odId =
    typeof target.odId === "string" && target.odId.trim().length > 0
      ? target.odId.trim()
      : null;

  return {
    selector,
    elementLabel,
    odId,
  };
}

function parseOptionalString(rawValue: unknown): string | undefined {
  if (typeof rawValue !== "string") {
    return undefined;
  }

  const normalized = rawValue.trim();
  return normalized.length > 0 ? normalized : undefined;
}

function parseOptionalPositiveInt(rawValue: unknown): number | undefined {
  if (typeof rawValue !== "string") {
    return undefined;
  }
  const parsed = Number(rawValue);
  if (!Number.isInteger(parsed) || parsed <= 0) {
    return undefined;
  }
  return parsed;
}

function parseOptionalBoolean(rawValue: unknown): boolean | undefined {
  if (typeof rawValue !== "string") {
    return undefined;
  }
  const normalized = rawValue.trim().toLowerCase();
  if (normalized === "true") {
    return true;
  }
  if (normalized === "false") {
    return false;
  }
  return undefined;
}

function parseActor(rawValue: unknown, fallback: string): string {
  if (typeof rawValue !== "string") {
    return fallback;
  }

  const normalized = rawValue.trim();
  return normalized.length > 0 ? normalized : fallback;
}

function handleUiPrototypingStudioError(
  reply: {
    status: (statusCode: number) => { send: (payload: unknown) => unknown };
  },
  error: unknown,
): unknown {
  if (isUiPrototypingStudioError(error)) {
    return reply.status(errorStatusCode(error.code)).send({
      code: error.code,
      message: error.message,
      details: error.details,
    });
  }

  return reply.status(500).send({
    code: "VARIANT_GENERATION_COUNT_MISMATCH",
    message: "Unexpected ui prototyping studio failure",
    details: {
      reason: String(error),
    },
  });
}

function errorStatusCode(code: UiPrototypingStudioErrorCode): number {
  switch (code) {
    case "UPS_AUTH_REQUIRED":
      return 401;
    case "UPS_AUTH_FORBIDDEN":
      return 403;
    case "SESSION_NOT_FOUND":
    case "DRAFT_BATCH_NOT_FOUND":
    case "BATCH_NOT_FOUND":
      return 404;
    case "PROMPT_NOT_SET":
    case "BASELINE_SELECTION_REQUIRED":
    case "BASELINE_GATE_UNSATISFIED":
    case "COMMENT_SET_EMPTY":
    case "BATCH_NOT_DRAFT":
    case "APPROVAL_STALE":
    case "AUTO_APPLY_FORBIDDEN":
    case "BATCH_APPROVAL_REQUIRED":
    case "HANDOFF_REVISION_REQUIRED":
    case "HANDOFF_BUNDLE_NOT_READY":
      return 409;
    case "VARIANT_COUNT_OUT_OF_RANGE":
    case "PROMPT_REQUIRED":
    case "BASELINE_LABEL_INVALID":
    case "COMMENT_SCHEMA_INVALID":
    case "SOURCE_REVISION_INVALID":
    case "APPROVAL_METADATA_REQUIRED":
    case "BATCH_STALE_FOR_HEAD":
    case "HANDOFF_REFERENCE_INCOMPLETE":
      return 422;
    case "VARIANT_GENERATION_COUNT_MISMATCH":
    default:
      return 500;
  }
}
