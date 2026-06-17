import { createHash } from "node:crypto";

import type { StudioSessionStorePort } from "./ports.js";
import { createUiPrototypingStudioError } from "../domain/errors.js";
import {
  type CommentEvent,
  type MutationBatch,
  type MutationChangeType,
  type MutationTask,
  type StudioSession,
} from "../domain/models.js";

export interface SynthesizeMutationBatchInput {
  sessionId: string;
  sourceRevisionId: string;
  requestedBy: string;
}

export interface SynthesizeMutationBatchResult {
  session: StudioSession;
  batch: MutationBatch;
}

/**
 * domainspec:
 *   concept:
 *     id: ui-prototyping-studio.SynthesizeMutationBatch
 *     type: Operation
 */
export function makeSynthesizeMutationBatchUseCase(
  store: StudioSessionStorePort,
) {
  return function synthesizeMutationBatch(
    input: SynthesizeMutationBatchInput,
  ): SynthesizeMutationBatchResult {
    const session = store.getSession(input.sessionId);
    if (!session) {
      throw createUiPrototypingStudioError(
        "SESSION_NOT_FOUND",
        "Session not found",
        {
          sessionId: input.sessionId,
        },
      );
    }

    if (
      session.revisionHeadId !== null &&
      session.revisionHeadId !== input.sourceRevisionId
    ) {
      throw createUiPrototypingStudioError(
        "SOURCE_REVISION_INVALID",
        "Source revision does not match current revision head",
        {
          sessionId: session.sessionId,
          expectedRevisionId: session.revisionHeadId,
          sourceRevisionId: input.sourceRevisionId,
        },
      );
    }

    const orderedComments = store.listComments(
      session.sessionId,
      input.sourceRevisionId,
    );

    if (orderedComments.length === 0) {
      throw createUiPrototypingStudioError(
        "COMMENT_SET_EMPTY",
        "At least one comment is required to synthesize a mutation batch",
        {
          sessionId: session.sessionId,
          sourceRevisionId: input.sourceRevisionId,
        },
      );
    }

    const tasks = orderedComments.map((comment, index) =>
      toMutationTask(comment, input.sourceRevisionId, index),
    );

    const generatedFromCommentIds = orderedComments.map(
      (comment) => comment.commentId,
    );

    const checksum = buildChecksum({
      sourceRevisionId: input.sourceRevisionId,
      generatedFromCommentIds,
      tasks,
    });

    const batch: MutationBatch = {
      batchId: store.allocateBatchId(),
      sessionId: session.sessionId,
      sourceRevisionId: input.sourceRevisionId,
      status: "draft",
      generatedFromCommentIds,
      tasks,
      approval: {
        required: true,
        approvedBy: null,
        approvedAt: null,
      },
      checksum,
    };

    const nextSession: StudioSession = {
      ...session,
      applyGate: "pending",
      state: "MutationDrafted",
    };

    store.saveBatch(batch);
    store.saveSession(nextSession);

    return {
      session: nextSession,
      batch,
    };
  };
}

function toMutationTask(
  comment: CommentEvent,
  sourceRevisionId: string,
  index: number,
): MutationTask {
  const changeType = inferChangeType(comment.intent);
  const priority = inferPriority(comment.severity);

  return {
    taskId: deterministicId(
      `${sourceRevisionId}:${comment.commentId}:${comment.target.selector}:${index}`,
      "task",
    ),
    target: comment.target.selector,
    odId: comment.target.odId ?? null,
    intent: comment.intent,
    changeType,
    acceptanceText: `Apply ${comment.intent} at ${comment.target.selector}: ${comment.note}`,
    priority,
  };
}

function inferChangeType(intent: string): MutationChangeType {
  const normalized = intent.toLowerCase();
  if (normalized.includes("add") || normalized.includes("create")) {
    return "add";
  }
  if (normalized.includes("remove") || normalized.includes("delete")) {
    return "remove";
  }
  return "change";
}

function inferPriority(severity: CommentEvent["severity"]): string {
  switch (severity) {
    case "blocker":
      return "p0";
    case "high":
      return "p1";
    case "medium":
      return "p2";
    case "low":
    default:
      return "p3";
  }
}

function deterministicId(seed: string, prefix: string): string {
  return `${prefix}-${createHash("sha1").update(seed).digest("hex").slice(0, 10)}`;
}

function buildChecksum(input: {
  sourceRevisionId: string;
  generatedFromCommentIds: string[];
  tasks: MutationTask[];
}): string {
  return createHash("sha256")
    .update(
      JSON.stringify({
        sourceRevisionId: input.sourceRevisionId,
        generatedFromCommentIds: input.generatedFromCommentIds,
        tasks: input.tasks,
      }),
    )
    .digest("hex");
}
