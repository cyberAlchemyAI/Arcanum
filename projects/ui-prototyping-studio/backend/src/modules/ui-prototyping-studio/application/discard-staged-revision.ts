import type { ArtifactContentPort } from "./artifact-content-port.js";
import type { StudioSessionStorePort } from "./ports.js";
import { createUiPrototypingStudioError } from "../domain/errors.js";
import { discardStaged } from "./two-gate-apply.js";
import type { StudioSession } from "../domain/models.js";

export interface DiscardStagedRevisionInput {
  sessionId: string;
  requestedBy: string;
}

export interface DiscardStagedRevisionResult {
  session: StudioSession;
}

/**
 * domainspec:
 *   concept:
 *     id: ui-prototyping-studio.DiscardStagedRevision
 *     type: Operation
 *
 * MW1 — reject the accept-diff gate: drop the staged candidate with no trace and return to
 * MutationApproved (head never advanced).
 */
export function makeDiscardStagedRevisionUseCase(
  store: StudioSessionStorePort,
  artifact: ArtifactContentPort | null,
) {
  return function discardStagedRevision(
    input: DiscardStagedRevisionInput,
  ): DiscardStagedRevisionResult {
    if (!artifact) {
      throw createUiPrototypingStudioError(
        "ARTIFACT_CONTENT_PORT_UNAVAILABLE",
        "Discard requires an artifact content store",
        { sessionId: input.sessionId },
      );
    }
    const staged = store.getStagedCandidate(input.sessionId);
    if (!staged) {
      throw createUiPrototypingStudioError(
        "NO_STAGED_CANDIDATE",
        "No staged candidate to discard",
        { sessionId: input.sessionId },
      );
    }
    const session = store.getSession(input.sessionId);
    if (!session) {
      throw createUiPrototypingStudioError("SESSION_NOT_FOUND", "Session not found", {
        sessionId: input.sessionId,
      });
    }

    discardStaged(staged.stagedRef, artifact);
    store.clearStagedCandidate(session.sessionId);
    const nextSession: StudioSession = { ...session, state: "MutationApproved" };
    store.saveSession(nextSession);
    return { session: nextSession };
  };
}
