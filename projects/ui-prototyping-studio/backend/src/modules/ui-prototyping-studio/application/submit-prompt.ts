import type { StudioSessionStorePort } from "./ports.js";
import { createUiPrototypingStudioError } from "../domain/errors.js";
import type { StudioSession } from "../domain/models.js";

export interface SubmitStudioPromptInput {
  sessionId: string;
  prompt: string;
  submittedBy: string;
}

/**
 * domainspec:
 *   concept:
 *     id: ui-prototyping-studio.SubmitPrompt
 *     type: Operation
 */
export function makeSubmitStudioPromptUseCase(store: StudioSessionStorePort) {
  return function submitStudioPrompt(
    input: SubmitStudioPromptInput,
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

    const normalizedPrompt = input.prompt.trim();
    if (normalizedPrompt.length === 0) {
      throw createUiPrototypingStudioError(
        "PROMPT_REQUIRED",
        "Prompt is required",
      );
    }

    const nextSession: StudioSession = {
      ...session,
      prompt: normalizedPrompt,
      state: "PromptCaptured",
    };

    store.saveSession(nextSession);
    return nextSession;
  };
}
