import type { StudioSessionStorePort } from "./ports.js";
import { createUiPrototypingStudioError } from "../domain/errors.js";
import type { HandoffBundle } from "../domain/models.js";

export interface GetHandoffBundleInput {
  sessionId: string;
}

/**
 * domainspec:
 *   concept:
 *     id: ui-prototyping-studio.GetHandoffBundle
 *     type: Query
 */
export function makeGetHandoffBundleQuery(store: StudioSessionStorePort) {
  return function getHandoffBundle(
    input: GetHandoffBundleInput,
  ): HandoffBundle {
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

    const bundle = store.getHandoffBundle(input.sessionId);
    if (!bundle) {
      throw createUiPrototypingStudioError(
        "HANDOFF_BUNDLE_NOT_READY",
        "Handoff bundle is not ready",
        {
          sessionId: input.sessionId,
        },
      );
    }

    return bundle;
  };
}
