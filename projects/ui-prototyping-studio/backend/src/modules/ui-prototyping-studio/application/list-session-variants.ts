import type { StudioSessionStorePort } from "./ports.js";
import { createUiPrototypingStudioError } from "../domain/errors.js";
import type { PrototypeVariant } from "../domain/models.js";

export interface ListStudioSessionVariantsInput {
  sessionId: string;
}

/**
 * domainspec:
 *   concept:
 *     id: ui-prototyping-studio.ListSessionVariants
 *     type: Query
 *   edges:
 *     - edge: queries
 *       to: ui-prototyping-studio.PrototypeVariant
 */
export function makeListStudioSessionVariantsQuery(
  store: StudioSessionStorePort,
) {
  return function listStudioSessionVariants(
    input: ListStudioSessionVariantsInput,
  ): PrototypeVariant[] {
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

    return store.listVariants(input.sessionId);
  };
}
