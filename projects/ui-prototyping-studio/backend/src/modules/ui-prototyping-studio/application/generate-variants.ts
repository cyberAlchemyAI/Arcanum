import type { StudioSessionStorePort } from "./ports.js";
import { createUiPrototypingStudioError } from "../domain/errors.js";
import {
  buildVariantLabels,
  type PrototypeVariant,
  type StudioSession,
} from "../domain/models.js";

export interface GenerateStudioVariantsInput {
  sessionId: string;
  requestedBy: string;
}

export interface GenerateStudioVariantsResult {
  session: StudioSession;
  variants: PrototypeVariant[];
}

/**
 * domainspec:
 *   concept:
 *     id: ui-prototyping-studio.GenerateVariants
 *     type: Operation
 */
export function makeGenerateStudioVariantsUseCase(
  store: StudioSessionStorePort,
) {
  return function generateStudioVariants(
    input: GenerateStudioVariantsInput,
  ): GenerateStudioVariantsResult {
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

    if (!session.prompt || session.prompt.trim().length === 0) {
      throw createUiPrototypingStudioError(
        "PROMPT_NOT_SET",
        "Prompt must be submitted before variant generation",
        {
          sessionId: input.sessionId,
        },
      );
    }

    const labels = buildVariantLabels(session.variantCount);
    const variants: PrototypeVariant[] = labels.map((label, index) => ({
      sessionId: session.sessionId,
      variantLabel: label,
      htmlArtifactRef: `/artifacts/ui-prototyping-studio/${session.sessionId}/${label.toLowerCase()}.html`,
      componentsUsed: [
        "StudioHeader",
        "VariantCanvas",
        index % 2 === 0 ? "SessionControlsPanel" : "SessionStateIndicator",
      ],
      rationale: `Variant ${label} emphasizes ${index % 2 === 0 ? "clarity" : "density"} for prompt intent.`,
      tradeoffs: `Variant ${label} balances exploration breadth with deterministic controls.`,
      risk: `Variant ${label} may require follow-up tuning after baseline selection.`,
      status: session.variantCount === 1 ? "committed" : "candidate",
    }));

    if (variants.length !== session.variantCount) {
      throw createUiPrototypingStudioError(
        "VARIANT_GENERATION_COUNT_MISMATCH",
        "Generated variant count does not match requested variant count",
        {
          expectedCount: session.variantCount,
          actualCount: variants.length,
        },
      );
    }

    const primaryVariant = variants[0];
    if (!primaryVariant) {
      throw createUiPrototypingStudioError(
        "VARIANT_GENERATION_COUNT_MISMATCH",
        "Generated variants are missing a primary baseline candidate",
        {
          expectedCount: session.variantCount,
          actualCount: variants.length,
        },
      );
    }

    const nextSession: StudioSession = {
      ...session,
      state: "VariantsReady",
      baseline:
        session.variantCount === 1
          ? {
              mode: "committed",
              label: primaryVariant.variantLabel,
            }
          : null,
      selectionGate: session.variantCount === 1 ? "satisfied" : "pending",
    };

    store.saveVariants(session.sessionId, variants);
    store.saveSession(nextSession);

    return {
      session: nextSession,
      variants,
    };
  };
}
