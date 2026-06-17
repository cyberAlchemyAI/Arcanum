import type { StudioSessionStorePort } from "./ports.js";
import {
  buildVariantLabels,
  resolveVariantCount,
  type StudioSession,
} from "../domain/models.js";

export interface InitializeStudioSessionInput {
  requestedVariantCount?: number;
  requestedBy: string;
}

/**
 * domainspec:
 *   concept:
 *     id: ui-prototyping-studio.InitializeSession
 *     type: Operation
 */
export function makeInitializeStudioSessionUseCase(
  store: StudioSessionStorePort,
) {
  return function initializeStudioSession(
    input: InitializeStudioSessionInput,
  ): StudioSession {
    const variantCount = resolveVariantCount(input.requestedVariantCount);
    const session: StudioSession = {
      sessionId: store.allocateSessionId(),
      prompt: null,
      variantCount,
      variantLabels: buildVariantLabels(variantCount),
      baseline: null,
      revisionHeadId: null,
      selectionGate: "pending",
      applyGate: "pending",
      integration: {
        uiPhaseBridgeReady: false,
        generateTestsUiReady: false,
        uiImplementReady: false,
      },
      state: "SessionInitialized",
    };

    store.saveSession(session);
    return session;
  };
}
