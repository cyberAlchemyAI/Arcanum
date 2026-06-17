import type { StudioSessionStorePort } from "./ports.js";
import { createUiPrototypingStudioError } from "../domain/errors.js";
import type { StudioSession } from "../domain/models.js";

export interface GetStudioSessionSnapshotInput {
  sessionId: string;
}

/**
 * domainspec:
 *   concept:
 *     id: ui-prototyping-studio.GetSessionSnapshot
 *     type: Query
 *   edges:
 *     - edge: queries
 *       to: ui-prototyping-studio.StudioSession
 */
export function makeGetStudioSessionSnapshotQuery(
  store: StudioSessionStorePort,
) {
  return function getStudioSessionSnapshot(
    input: GetStudioSessionSnapshotInput,
  ): StudioSession {
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

    return session;
  };
}
