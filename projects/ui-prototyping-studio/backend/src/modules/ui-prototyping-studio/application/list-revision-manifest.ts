import type { StudioSessionStorePort } from "./ports.js";
import { createUiPrototypingStudioError } from "../domain/errors.js";
import type { RevisionManifestEntry } from "../domain/models.js";

export interface ListRevisionManifestInput {
  sessionId: string;
  limit?: number;
  newestFirst?: boolean;
}

/**
 * domainspec:
 *   concept:
 *     id: ui-prototyping-studio.ListRevisionManifest
 *     type: Query
 */
export function makeListRevisionManifestQuery(store: StudioSessionStorePort) {
  return function listRevisionManifest(
    input: ListRevisionManifestInput,
  ): RevisionManifestEntry[] {
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

    const newestFirst = input.newestFirst ?? true;
    const limit =
      typeof input.limit === "number" &&
      Number.isInteger(input.limit) &&
      input.limit > 0
        ? input.limit
        : 50;

    const entries = store.listRevisions(input.sessionId);
    const sorted = [...entries].sort((left, right) =>
      newestFirst
        ? right.createdAt.localeCompare(left.createdAt)
        : left.createdAt.localeCompare(right.createdAt),
    );

    return sorted.slice(0, limit);
  };
}
