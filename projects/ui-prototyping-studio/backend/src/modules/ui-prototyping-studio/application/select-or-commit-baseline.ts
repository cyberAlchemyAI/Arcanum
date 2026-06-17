import type { StudioSessionStorePort } from "./ports.js";
import { createUiPrototypingStudioError } from "../domain/errors.js";
import type { PrototypeVariant, StudioSession } from "../domain/models.js";

export interface SelectOrCommitBaselineInput {
  sessionId: string;
  selectedLabel?: string;
  requestedBy: string;
}

export interface SelectOrCommitBaselineResult {
  session: StudioSession;
  variants: PrototypeVariant[];
}

/**
 * domainspec:
 *   concept:
 *     id: ui-prototyping-studio.SelectOrCommitBaseline
 *     type: Operation
 */
export function makeSelectOrCommitBaselineUseCase(
  store: StudioSessionStorePort,
) {
  return function selectOrCommitBaseline(
    input: SelectOrCommitBaselineInput,
  ): SelectOrCommitBaselineResult {
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

    const variants = store.listVariants(session.sessionId);
    if (variants.length !== session.variantCount) {
      throw createUiPrototypingStudioError(
        "VARIANT_GENERATION_COUNT_MISMATCH",
        "Baseline selection requires generated variants",
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
        "Baseline selection requires at least one generated variant",
        {
          expectedCount: session.variantCount,
          actualCount: variants.length,
        },
      );
    }

    let selectedLabel = primaryVariant.variantLabel;
    let mode: "selected" | "committed" = "committed";

    if (session.variantCount > 1) {
      const normalizedLabel = input.selectedLabel?.trim().toUpperCase();

      if (!normalizedLabel) {
        throw createUiPrototypingStudioError(
          "BASELINE_SELECTION_REQUIRED",
          "Baseline selection is required when variantCount is greater than 1",
          {
            sessionId: input.sessionId,
          },
        );
      }

      const matchedVariant = variants.find(
        (variant) => variant.variantLabel === normalizedLabel,
      );
      if (!matchedVariant) {
        throw createUiPrototypingStudioError(
          "BASELINE_LABEL_INVALID",
          "Selected baseline label is invalid",
          {
            sessionId: input.sessionId,
            selectedLabel: normalizedLabel,
            variantLabels: variants.map((variant) => variant.variantLabel),
          },
        );
      }

      selectedLabel = matchedVariant.variantLabel;
      mode = "selected";
    }

    const updatedVariants = variants.map((variant) => {
      if (variant.variantLabel !== selectedLabel) {
        return {
          ...variant,
          status: "candidate" as const,
        };
      }

      return {
        ...variant,
        status:
          mode === "committed" ? ("committed" as const) : ("selected" as const),
      };
    });

    const nextSession: StudioSession = {
      ...session,
      baseline: {
        mode,
        label: selectedLabel,
      },
      selectionGate: "satisfied",
      applyGate: "pending",
      revisionHeadId: session.revisionHeadId ?? "rev-0000",
      state: "BaselineReady",
    };

    store.saveVariants(session.sessionId, updatedVariants);
    store.saveSession(nextSession);

    return {
      session: nextSession,
      variants: updatedVariants,
    };
  };
}
