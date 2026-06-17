import type { StudioSessionStorePort } from "./ports.js";
import { createUiPrototypingStudioError } from "../domain/errors.js";
import type { MutationBatch } from "../domain/models.js";

export interface GetDraftMutationBatchInput {
  sessionId: string;
  batchId?: string;
}

/**
 * domainspec:
 *   concept:
 *     id: ui-prototyping-studio.GetDraftMutationBatch
 *     type: Query
 */
export function makeGetDraftMutationBatchQuery(store: StudioSessionStorePort) {
  return function getDraftMutationBatch(
    input: GetDraftMutationBatchInput,
  ): MutationBatch {
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

    const batch = store.getDraftBatch(input.sessionId, input.batchId);
    if (!batch) {
      throw createUiPrototypingStudioError(
        "DRAFT_BATCH_NOT_FOUND",
        "Draft mutation batch not found",
        {
          sessionId: input.sessionId,
          batchId: input.batchId,
        },
      );
    }

    return batch;
  };
}
