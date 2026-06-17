import type { ArtifactContentPort } from "./artifact-content-port.js";
import type { StudioSessionStorePort } from "./ports.js";
import { createUiPrototypingStudioError } from "../domain/errors.js";
import { diffByOdId } from "./admission.js";
import { acceptStaged } from "./two-gate-apply.js";
import { resolveCurrentHtml } from "./current-html.js";
import type {
  MutationBatch,
  RevisionManifestEntry,
  StudioSession,
} from "../domain/models.js";

export interface AcceptStagedRevisionInput {
  sessionId: string;
  acceptedAt: string;
  requestedBy: string;
}

export interface AcceptStagedRevisionResult {
  session: StudioSession;
  revision: RevisionManifestEntry;
}

/**
 * domainspec:
 *   concept:
 *     id: ui-prototyping-studio.AcceptStagedRevision
 *     type: Operation
 *
 * MW1 — gate 2B. Commit EXACTLY the staged candidate the human previewed (idempotency-at-verdict),
 * append exactly one revision carrying the honest diff + the committed candidate hash, advance head,
 * and clear the staged record. Fail-closed on hash mismatch / missing candidate (via acceptStaged).
 */
export function makeAcceptStagedRevisionUseCase(
  store: StudioSessionStorePort,
  artifact: ArtifactContentPort | null,
) {
  return function acceptStagedRevision(
    input: AcceptStagedRevisionInput,
  ): AcceptStagedRevisionResult {
    if (!artifact) {
      throw createUiPrototypingStudioError(
        "ARTIFACT_CONTENT_PORT_UNAVAILABLE",
        "Accept requires an artifact content store",
        { sessionId: input.sessionId },
      );
    }
    const staged = store.getStagedCandidate(input.sessionId);
    if (!staged) {
      throw createUiPrototypingStudioError(
        "NO_STAGED_CANDIDATE",
        "No staged candidate to accept",
        { sessionId: input.sessionId },
      );
    }
    const session = store.getSession(input.sessionId);
    if (!session) {
      throw createUiPrototypingStudioError("SESSION_NOT_FOUND", "Session not found", {
        sessionId: input.sessionId,
      });
    }
    const batch = store.getBatch(session.sessionId, staged.batchId);
    if (!batch) {
      throw createUiPrototypingStudioError("BATCH_NOT_FOUND", "Batch not found", {
        sessionId: session.sessionId,
        batchId: staged.batchId,
      });
    }

    // Read candidate + resolve current BEFORE commit (commit moves staged -> committed).
    const candidateHtml = artifact.readHtml(staged.stagedRef);
    const currentHtml = resolveCurrentHtml(session, store, artifact);
    if (candidateHtml === null || currentHtml === null) {
      throw createUiPrototypingStudioError(
        "NO_STAGED_CANDIDATE",
        "Staged candidate or current HTML is unreadable",
        { sessionId: session.sessionId },
      );
    }
    const honest = diffByOdId(currentHtml, candidateHtml);

    const committed = acceptStaged(staged.stagedRef, staged.candidateHtmlHash, artifact);

    const previousManifestCount = store.listRevisions(session.sessionId).length;
    const parentRevisionId = session.revisionHeadId ?? "rev-0000";
    const revisionId = store.allocateRevisionId(parentRevisionId);

    const unresolvedCommentIds = store
      .listComments(session.sessionId, batch.sourceRevisionId)
      .map((comment) => comment.commentId)
      .filter((commentId) => !batch.generatedFromCommentIds.includes(commentId));

    const revision: RevisionManifestEntry = {
      revisionId,
      parentRevisionId,
      sessionId: session.sessionId,
      variantCount: session.variantCount,
      baseline: session.baseline!,
      appliedBatchId: batch.batchId,
      appliedTaskIds: batch.tasks.map((task) => task.taskId),
      unresolvedCommentIds,
      diffSummary: { added: honest.added, changed: honest.changed, removed: honest.removed },
      diffSummaryHonest: honest,
      candidateHtmlHash: committed.candidateHtmlHash,
      createdAt: input.acceptedAt,
    };

    const appliedBatch: MutationBatch = { ...batch, status: "applied" };
    const nextSession: StudioSession = {
      ...session,
      revisionHeadId: revisionId,
      applyGate: "satisfied",
      state: "RevisionRecorded",
    };

    store.saveBatch(appliedBatch);
    store.appendRevision(revision);
    store.saveSession(nextSession);
    store.clearStagedCandidate(session.sessionId);

    const nextManifestCount = store.listRevisions(session.sessionId).length;
    if (nextManifestCount !== previousManifestCount + 1) {
      throw createUiPrototypingStudioError(
        "VARIANT_GENERATION_COUNT_MISMATCH",
        "Accept must append exactly one revision manifest entry",
        { previousManifestCount, nextManifestCount, sessionId: session.sessionId },
      );
    }

    return { session: nextSession, revision };
  };
}
