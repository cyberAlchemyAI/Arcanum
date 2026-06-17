import { existsSync } from "node:fs";
import { join } from "node:path";

import type { StudioSessionStorePort } from "./ports.js";
import { createUiPrototypingStudioError } from "../domain/errors.js";
import type { HandoffBundle, StudioSession } from "../domain/models.js";

const STORY_REF = "docs/features/ui-prototyping-studio/STORIES.md";
const SPEC_REQUIREMENT_REF =
  "docs/features/ui-prototyping-studio/SPEC.md#functional-requirements-mvp";
const SPEC_ACCEPTANCE_REF =
  "docs/features/ui-prototyping-studio/SPEC.md#acceptance-criteria-mvp";
const UI_SPEC_REF = "docs/features/ui-prototyping-studio/UI-SPEC.md";
const TEST_SPEC_REF = "docs/features/ui-prototyping-studio/TEST-SPEC.md";

export interface ExportDesignHandoffInput {
  sessionId: string;
  exportProfile?: string;
  requestedBy: string;
}

export interface ExportDesignHandoffResult {
  session: StudioSession;
  bundle: HandoffBundle;
}

interface ExportDesignHandoffOptions {
  featureDocsRootDir: string;
}

/**
 * domainspec:
 *   concept:
 *     id: ui-prototyping-studio.ExportDesignHandoff
 *     type: Operation
 */
export function makeExportDesignHandoffUseCase(
  store: StudioSessionStorePort,
  options: ExportDesignHandoffOptions,
) {
  return function exportDesignHandoff(
    input: ExportDesignHandoffInput,
  ): ExportDesignHandoffResult {
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

    const revisions = store.listRevisions(session.sessionId);
    if (revisions.length === 0 || !session.revisionHeadId) {
      throw createUiPrototypingStudioError(
        "HANDOFF_REVISION_REQUIRED",
        "Handoff export requires at least one revision manifest entry",
        {
          sessionId: session.sessionId,
          revisionCount: revisions.length,
          revisionHeadId: session.revisionHeadId,
        },
      );
    }

    if (!session.baseline) {
      throw createUiPrototypingStudioError(
        "HANDOFF_REFERENCE_INCOMPLETE",
        "Handoff export requires baseline provenance",
        {
          sessionId: session.sessionId,
        },
      );
    }

    const requiredFiles = [
      "SPEC.md",
      "STORIES.md",
      "UI-SPEC.md",
      "TEST-SPEC.md",
    ];
    const missingFiles = requiredFiles.filter(
      (fileName) => !existsSync(join(options.featureDocsRootDir, fileName)),
    );

    if (missingFiles.length > 0) {
      throw createUiPrototypingStudioError(
        "HANDOFF_REFERENCE_INCOMPLETE",
        "Handoff export references are incomplete",
        {
          sessionId: session.sessionId,
          missingFiles,
        },
      );
    }

    const bundle: HandoffBundle = {
      sessionId: session.sessionId,
      revisionHeadId: session.revisionHeadId,
      baseline: session.baseline,
      variantCount: session.variantCount,
      storyRefs: [STORY_REF],
      requirementRefs: [SPEC_REQUIREMENT_REF],
      acceptanceRefs: [SPEC_ACCEPTANCE_REF],
      uiSpecRef: UI_SPEC_REF,
      testSpecRef: TEST_SPEC_REF,
    };

    const nextSession: StudioSession = {
      ...session,
      integration: {
        uiPhaseBridgeReady: true,
        generateTestsUiReady: true,
        uiImplementReady: true,
      },
      state: "RevisionRecorded",
    };

    store.saveSession(nextSession);
    store.saveHandoffBundle(bundle);

    return {
      session: nextSession,
      bundle,
    };
  };
}
