import type { StudioSessionStorePort } from "./ports.js";
import { createUiPrototypingStudioError } from "../domain/errors.js";
import type { MutationBatch, StudioSession } from "../domain/models.js";

export interface ApproveMutationBatchInput {
  sessionId: string;
  batchId: string;
  approvedBy: string;
  approvedAt: string;
}

export interface ApproveMutationBatchResult {
  session: StudioSession;
  batch: MutationBatch;
}

/**
 * domainspec:
 *   concept:
 *     id: ui-prototyping-studio.ApproveMutationBatch
 *     type: Operation
 */
export function makeApproveMutationBatchUseCase(store: StudioSessionStorePort) {
  return function approveMutationBatch(
    input: ApproveMutationBatchInput,
  ): ApproveMutationBatchResult {
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

    const batch = store.getBatch(input.sessionId, input.batchId);
    if (!batch) {
      throw createUiPrototypingStudioError(
        "BATCH_NOT_FOUND",
        "Batch not found",
        {
          sessionId: input.sessionId,
          batchId: input.batchId,
        },
      );
    }

    if (batch.status !== "draft") {
      throw createUiPrototypingStudioError(
        "BATCH_NOT_DRAFT",
        "Batch must be in draft status before approval",
        {
          batchId: batch.batchId,
          status: batch.status,
        },
      );
    }

    const approvedBy = input.approvedBy.trim();
    const approvedAt = input.approvedAt.trim();
    const approvedAtEpoch = Date.parse(approvedAt);
    if (
      approvedBy.length === 0 ||
      approvedAt.length === 0 ||
      Number.isNaN(approvedAtEpoch)
    ) {
      throw createUiPrototypingStudioError(
        "APPROVAL_METADATA_REQUIRED",
        "Approval identity and timestamp are required",
        {
          approvedBy: input.approvedBy,
          approvedAt: input.approvedAt,
        },
      );
    }

    if (
      session.revisionHeadId !== null &&
      batch.sourceRevisionId !== session.revisionHeadId
    ) {
      throw createUiPrototypingStudioError(
        "APPROVAL_STALE",
        "Approval is stale against the current revision head",
        {
          sessionId: session.sessionId,
          revisionHeadId: session.revisionHeadId,
          sourceRevisionId: batch.sourceRevisionId,
        },
      );
    }

    const nextBatch: MutationBatch = {
      ...batch,
      status: "approved",
      approval: {
        required: true,
        approvedBy,
        approvedAt,
      },
    };

    const nextSession: StudioSession = {
      ...session,
      applyGate: "satisfied",
      state: "MutationApproved",
    };

    store.saveBatch(nextBatch);
    store.saveSession(nextSession);

    return {
      session: nextSession,
      batch: nextBatch,
    };
  };
}
