import { existsSync, readFileSync } from "node:fs";
import { isAbsolute, resolve } from "node:path";

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
  /**
   * N1 — export is the one IRREVERSIBLE edge (downstream consumption). The human confirmation lives HERE,
   * in the core use-case, so EVERY adapter (CLI, HTTP) inherits it — not only the CLI (closes F1, restores
   * ARCHITECTURE §4 "gates live in the core, never in the adapter"). Must be a non-empty confirming actor.
   */
  confirmedBy?: string;
}

export interface ExportDesignHandoffResult {
  session: StudioSession;
  bundle: HandoffBundle;
}

interface ExportDesignHandoffOptions {
  featureDocsRootDir: string;
}

interface HandoffExportRefs {
  profileId?: string;
  storyRefs: string[];
  requirementRefs: string[];
  acceptanceRefs: string[];
  uiSpecRef: string;
  testSpecRef: string;
  sourceRefs: string[];
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
    // N1 (gate-in-core): the irreversible edge requires an explicit human confirmation. Enforced here so no
    // adapter can reach export unconfirmed (the HTTP route previously bypassed the CLI-only `--confirm`).
    if (!input.confirmedBy || input.confirmedBy.trim().length === 0) {
      throw createUiPrototypingStudioError(
        "HANDOFF_CONFIRMATION_REQUIRED",
        "Export is the one irreversible edge — an explicit human confirmation is required",
        { sessionId: input.sessionId },
      );
    }
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

    const refs = resolveExportRefs(input.exportProfile, options.featureDocsRootDir);
    const missingRefs = refsForExistenceCheck(refs).filter(
      (ref) => !existsSync(resolveRefPath(options.featureDocsRootDir, ref)),
    );

    const bundle: HandoffBundle = {
      sessionId: session.sessionId,
      revisionHeadId: session.revisionHeadId,
      baseline: session.baseline,
      variantCount: session.variantCount,
      exportProfile: refs.profileId ?? input.exportProfile,
      storyRefs: refs.storyRefs,
      requirementRefs: refs.requirementRefs,
      acceptanceRefs: refs.acceptanceRefs,
      uiSpecRef: refs.uiSpecRef,
      testSpecRef: refs.testSpecRef,
      sourceRefs: refs.sourceRefs,
      missingRefs,
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

function defaultExportRefs(): HandoffExportRefs {
  return {
    storyRefs: [STORY_REF],
    requirementRefs: [SPEC_REQUIREMENT_REF],
    acceptanceRefs: [SPEC_ACCEPTANCE_REF],
    uiSpecRef: UI_SPEC_REF,
    testSpecRef: TEST_SPEC_REF,
    sourceRefs: [],
  };
}

function resolveExportRefs(
  exportProfile: string | undefined,
  featureDocsRootDir: string,
): HandoffExportRefs {
  const defaults = defaultExportRefs();
  if (!exportProfile) return defaults;

  const profilePath = isAbsolute(exportProfile)
    ? exportProfile
    : resolve(featureDocsRootDir, exportProfile);
  if (!existsSync(profilePath)) {
    return { ...defaults, profileId: exportProfile };
  }

  const parsed = JSON.parse(readFileSync(profilePath, "utf8")) as Record<string, unknown>;
  return {
    profileId: optionalString(parsed.profileId) ?? exportProfile,
    storyRefs: stringList(parsed.storyRefs, defaults.storyRefs),
    requirementRefs: stringList(parsed.requirementRefs, defaults.requirementRefs),
    acceptanceRefs: stringList(parsed.acceptanceRefs, defaults.acceptanceRefs),
    uiSpecRef: optionalString(parsed.uiSpecRef) ?? defaults.uiSpecRef,
    testSpecRef: optionalString(parsed.testSpecRef) ?? defaults.testSpecRef,
    sourceRefs: stringList(parsed.sourceRefs, defaults.sourceRefs),
  };
}

function stringList(value: unknown, fallback: string[]): string[] {
  if (!Array.isArray(value)) return [...fallback];
  const strings = value.filter((item): item is string => typeof item === "string" && item.trim().length > 0);
  return strings.length ? strings : [...fallback];
}

function optionalString(value: unknown): string | undefined {
  return typeof value === "string" && value.trim().length > 0 ? value : undefined;
}

function refsForExistenceCheck(refs: HandoffExportRefs): string[] {
  return [
    ...refs.storyRefs,
    ...refs.requirementRefs,
    ...refs.acceptanceRefs,
    refs.uiSpecRef,
    refs.testSpecRef,
    ...refs.sourceRefs,
  ].filter((ref) => !/^https?:\/\//.test(ref));
}

function resolveRefPath(rootDir: string, ref: string): string {
  const [pathOnly] = ref.split("#", 1);
  return isAbsolute(pathOnly ?? "") ? (pathOnly ?? "") : resolve(rootDir, pathOnly ?? "");
}
