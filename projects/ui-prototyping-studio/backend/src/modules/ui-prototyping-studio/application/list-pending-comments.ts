import type { StudioSessionStorePort } from "./ports.js";
import { createUiPrototypingStudioError } from "../domain/errors.js";
import type { CommentEvent } from "../domain/models.js";

export interface ListPendingCommentsInput {
  sessionId: string;
}

/**
 * domainspec:
 *   concept:
 *     id: ui-prototyping-studio.ListPendingComments
 *     type: Query
 *
 * CL2 — the agent-pickup drain. "Pending" = comments on the current head revision that have NOT yet
 * been folded into any mutation batch (`generatedFromCommentIds`). The agent reads these on its turn
 * (or via `studio watch`), synthesizes + proposes a candidate, and stages it. Idempotent by comment id:
 * once a comment is in a batch, it stops being pending, so re-draining never double-processes.
 */
export function makeListPendingCommentsQuery(store: StudioSessionStorePort) {
  return function listPendingComments(
    input: ListPendingCommentsInput,
  ): CommentEvent[] {
    const session = store.getSession(input.sessionId);
    if (!session) {
      throw createUiPrototypingStudioError("SESSION_NOT_FOUND", "Session not found", {
        sessionId: input.sessionId,
      });
    }
    const revisionId = session.revisionHeadId ?? "rev-0000";
    const comments = store.listComments(session.sessionId, revisionId);
    const batched = new Set(
      store
        .listBatches(session.sessionId)
        .flatMap((batch) => batch.generatedFromCommentIds),
    );
    return comments.filter((comment) => !batched.has(comment.commentId));
  };
}
