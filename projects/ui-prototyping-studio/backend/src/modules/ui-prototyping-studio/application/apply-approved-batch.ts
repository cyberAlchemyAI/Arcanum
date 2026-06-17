import type { StudioSessionStorePort } from "./ports.js";
import { createUiPrototypingStudioError } from "../domain/errors.js";
import type {
  DiffSummary,
  MutationBatch,
  RevisionManifestEntry,
  StudioSession,
} from "../domain/models.js";

export interface ApplyApprovedBatchInput {
  sessionId: string;
  batchId: string;
  applyRequestedBy: string;
}

export interface ApplyApprovedBatchResult {
  session: StudioSession;
  batch: MutationBatch;
  revision: RevisionManifestEntry;
}

/**
 * domainspec:
 *   concept:
 *     id: ui-prototyping-studio.ApplyApprovedBatch
 *     type: Operation
 */
export function makeApplyApprovedBatchUseCase(store: StudioSessionStorePort) {
  return function applyApprovedBatch(
    input: ApplyApprovedBatchInput,
  ): ApplyApprovedBatchResult {
    const actor = input.applyRequestedBy.trim();
    if (actor.toLowerCase() === "system:auto") {
      throw createUiPrototypingStudioError(
        "AUTO_APPLY_FORBIDDEN",
        "Auto-apply is forbidden",
        {
          applyRequestedBy: input.applyRequestedBy,
        },
      );
    }

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

    if (session.selectionGate !== "satisfied" || !session.baseline) {
      throw createUiPrototypingStudioError(
        "BASELINE_GATE_UNSATISFIED",
        "Baseline gate must be satisfied before apply",
        {
          sessionId: session.sessionId,
          selectionGate: session.selectionGate,
          baseline: session.baseline,
        },
      );
    }

    const batch = store.getBatch(session.sessionId, input.batchId);
    if (!batch) {
      throw createUiPrototypingStudioError(
        "BATCH_NOT_FOUND",
        "Batch not found",
        {
          sessionId: session.sessionId,
          batchId: input.batchId,
        },
      );
    }

    if (batch.status !== "approved") {
      throw createUiPrototypingStudioError(
        "BATCH_APPROVAL_REQUIRED",
        "Batch must be approved before apply",
        {
          batchId: batch.batchId,
          status: batch.status,
        },
      );
    }

    if (
      session.revisionHeadId !== null &&
      batch.sourceRevisionId !== session.revisionHeadId
    ) {
      throw createUiPrototypingStudioError(
        "BATCH_STALE_FOR_HEAD",
        "Batch source revision is stale for current revision head",
        {
          sessionId: session.sessionId,
          revisionHeadId: session.revisionHeadId,
          sourceRevisionId: batch.sourceRevisionId,
        },
      );
    }

    const previousManifestCount = store.listRevisions(session.sessionId).length;
    const parentRevisionId = session.revisionHeadId ?? "rev-0000";
    const revisionId = store.allocateRevisionId(parentRevisionId);

    const appliedBatch: MutationBatch = {
      ...batch,
      status: "applied",
    };

    const unresolvedCommentIds = store
      .listComments(session.sessionId, batch.sourceRevisionId)
      .map((comment) => comment.commentId)
      .filter(
        (commentId) => !batch.generatedFromCommentIds.includes(commentId),
      );

    const revision: RevisionManifestEntry = {
      revisionId,
      parentRevisionId,
      sessionId: session.sessionId,
      variantCount: session.variantCount,
      baseline: session.baseline,
      appliedBatchId: batch.batchId,
      appliedTaskIds: batch.tasks.map((task) => task.taskId),
      unresolvedCommentIds,
      diffSummary: buildDiffSummary(batch),
      createdAt: new Date().toISOString(),
    };

    const nextSession: StudioSession = {
      ...session,
      revisionHeadId: revisionId,
      applyGate: "pending",
      state: "RevisionRecorded",
    };

    store.saveBatch(appliedBatch);
    store.appendRevision(revision);
    store.saveSession(nextSession);

    const nextManifestCount = store.listRevisions(session.sessionId).length;
    if (nextManifestCount !== previousManifestCount + 1) {
      throw createUiPrototypingStudioError(
        "VARIANT_GENERATION_COUNT_MISMATCH",
        "Successful apply must append exactly one revision manifest entry",
        {
          previousManifestCount,
          nextManifestCount,
          sessionId: session.sessionId,
        },
      );
    }

    return {
      session: nextSession,
      batch: appliedBatch,
      revision,
    };
  };
}

function buildDiffSummary(batch: MutationBatch): DiffSummary {
  let added = 0;
  let changed = 0;
  let removed = 0;

  for (const task of batch.tasks) {
    if (task.changeType === "add") {
      added += 1;
      continue;
    }
    if (task.changeType === "remove") {
      removed += 1;
      continue;
    }
    changed += 1;
  }

  return {
    added,
    changed,
    removed,
  };
}
