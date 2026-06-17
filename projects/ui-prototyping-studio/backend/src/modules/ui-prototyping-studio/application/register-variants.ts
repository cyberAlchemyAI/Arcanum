import type { ArtifactContentPort } from "./artifact-content-port.js";
import type { StudioSessionStorePort } from "./ports.js";
import { createUiPrototypingStudioError } from "../domain/errors.js";
import { canonicalizeHtml } from "../domain/canonicalize.js";
import {
  buildVariantLabels,
  type PrototypeVariant,
  type StudioSession,
  type VariantLabel,
} from "../domain/models.js";

export interface RegisterVariantInput {
  label: VariantLabel;
  html: string;
}

export interface RegisterStudioVariantsInput {
  sessionId: string;
  variants: RegisterVariantInput[];
  requestedBy: string;
}

export interface RegisterStudioVariantsResult {
  session: StudioSession;
  variants: PrototypeVariant[];
}

/** True when the canonical HTML carries at least one `data-od-id` attribute. */
function hasOdId(canonicalHtml: string): boolean {
  return /data-od-id\s*=\s*"/i.test(canonicalHtml);
}

/**
 * domainspec:
 *   concept:
 *     id: ui-prototyping-studio.RegisterVariants
 *     type: Operation
 *
 * MR1 — the real `variants register` path (DEC-MUTATION-EXEC-015 substrate). Claude Code
 * supplies generated variant HTML; the core canonicalizes it (M0c), ENFORCES `data-od-id`
 * presence server-side (DEC-F2's "good mirror" — identity is unenforceable but od-id presence
 * is), commits it content-addressed via the ArtifactContentPort (M0b), and points the
 * variant's htmlArtifactRef at real content. Unblocks preview/annotation/mutation and harness M2.
 */
export function makeRegisterStudioVariantsUseCase(
  store: StudioSessionStorePort,
  artifact: ArtifactContentPort | null,
) {
  return function registerStudioVariants(
    input: RegisterStudioVariantsInput,
  ): RegisterStudioVariantsResult {
    if (!artifact) {
      throw createUiPrototypingStudioError(
        "ARTIFACT_CONTENT_PORT_UNAVAILABLE",
        "Variant registration requires an artifact content store",
        { sessionId: input.sessionId },
      );
    }

    const session = store.getSession(input.sessionId);
    if (!session) {
      throw createUiPrototypingStudioError("SESSION_NOT_FOUND", "Session not found", {
        sessionId: input.sessionId,
      });
    }
    if (!session.prompt || session.prompt.trim().length === 0) {
      throw createUiPrototypingStudioError(
        "PROMPT_NOT_SET",
        "Prompt must be submitted before variant registration",
        { sessionId: input.sessionId },
      );
    }

    const expectedLabels = buildVariantLabels(session.variantCount);
    const suppliedLabels = input.variants.map((variant) => variant.label);
    const uniqueSupplied = new Set(suppliedLabels);
    if (
      uniqueSupplied.size !== suppliedLabels.length ||
      suppliedLabels.length !== expectedLabels.length ||
      !expectedLabels.every((label) => uniqueSupplied.has(label))
    ) {
      throw createUiPrototypingStudioError(
        "VARIANT_GENERATION_COUNT_MISMATCH",
        "Registered variant labels must match the session's variant labels exactly",
        { expected: expectedLabels, supplied: suppliedLabels },
      );
    }

    // Canonicalize + gate ALL before any commit (fail-closed: no partial writes).
    const prepared = expectedLabels.map((label, index) => {
      const supplied = input.variants.find((variant) => variant.label === label)!;
      const canonical = canonicalizeHtml(supplied.html);
      if (!hasOdId(canonical)) {
        throw createUiPrototypingStudioError(
          "OD_ID_MISSING",
          `Variant ${label} HTML has no data-od-id; annotatable components must be stamped`,
          { sessionId: input.sessionId, label },
        );
      }
      return { label, canonical, index };
    });

    const variants: PrototypeVariant[] = prepared.map(({ label, canonical, index }) => {
      const staged = artifact.stageHtml(canonical);
      const committedRef = artifact.commitHtml(staged.stagedRef);
      return {
        sessionId: session.sessionId,
        variantLabel: label,
        htmlArtifactRef: committedRef,
        componentsUsed: [],
        rationale: `Variant ${label} registered by ${input.requestedBy}.`,
        tradeoffs: "",
        risk: "",
        status: session.variantCount === 1 ? "committed" : "candidate",
      } satisfies PrototypeVariant;
    });

    const primaryVariant = variants[0]!;
    const nextSession: StudioSession = {
      ...session,
      state: "VariantsReady",
      baseline:
        session.variantCount === 1
          ? { mode: "committed", label: primaryVariant.variantLabel }
          : null,
      selectionGate: session.variantCount === 1 ? "satisfied" : "pending",
    };

    store.saveVariants(session.sessionId, variants);
    store.saveSession(nextSession);

    return { session: nextSession, variants };
  };
}
