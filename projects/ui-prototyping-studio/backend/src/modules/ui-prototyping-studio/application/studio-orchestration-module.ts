import { makeApplyApprovedBatchUseCase } from "./apply-approved-batch.js";
import { makeApproveMutationBatchUseCase } from "./approve-mutation-batch.js";
import { makeCaptureCommentEventUseCase } from "./capture-comment-event.js";
import { makeExportDesignHandoffUseCase } from "./export-design-handoff.js";
import { makeGenerateStudioVariantsUseCase } from "./generate-variants.js";
import { makeRegisterStudioVariantsUseCase } from "./register-variants.js";
import { makeApplyAndStageUseCase } from "./apply-and-stage.js";
import { makeAcceptStagedRevisionUseCase } from "./accept-staged-revision.js";
import { makeDiscardStagedRevisionUseCase } from "./discard-staged-revision.js";
import type { ArtifactContentPort } from "./artifact-content-port.js";
import { makeGetDraftMutationBatchQuery } from "./get-draft-mutation-batch.js";
import { makeGetHandoffBundleQuery } from "./get-handoff-bundle.js";
import { makeGetStudioSessionSnapshotQuery } from "./get-session-snapshot.js";
import { makeInitializeStudioSessionUseCase } from "./initialize-session.js";
import { makeListRevisionManifestQuery } from "./list-revision-manifest.js";
import { makeListStudioSessionVariantsQuery } from "./list-session-variants.js";
import type { StudioSessionStorePort } from "./ports.js";
import { makeSelectOrCommitBaselineUseCase } from "./select-or-commit-baseline.js";
import { makeSubmitStudioPromptUseCase } from "./submit-prompt.js";
import { makeSynthesizeMutationBatchUseCase } from "./synthesize-mutation-batch.js";

interface CreateStudioOrchestrationModuleOptions {
  featureDocsRootDir: string;
  /** MR1 — injected by the composition root (CLI) so application stays free of infrastructure. */
  artifactContentStore?: ArtifactContentPort;
}

/**
 * domainspec:
 *   concept:
 *     id: ui-prototyping-studio.StudioOrchestrationModule
 *     type: Interface
 */
export function createStudioOrchestrationModule(
  store: StudioSessionStorePort,
  options: CreateStudioOrchestrationModuleOptions,
) {
  return {
    initializeSession: makeInitializeStudioSessionUseCase(store),
    submitPrompt: makeSubmitStudioPromptUseCase(store),
    generateVariants: makeGenerateStudioVariantsUseCase(store),
    registerVariants: makeRegisterStudioVariantsUseCase(store, options.artifactContentStore ?? null),
    selectOrCommitBaseline: makeSelectOrCommitBaselineUseCase(store),
    captureCommentEvent: makeCaptureCommentEventUseCase(store),
    synthesizeMutationBatch: makeSynthesizeMutationBatchUseCase(store),
    approveMutationBatch: makeApproveMutationBatchUseCase(store),
    applyApprovedBatch: makeApplyApprovedBatchUseCase(store),
    applyAndStage: makeApplyAndStageUseCase(store, options.artifactContentStore ?? null),
    acceptStagedRevision: makeAcceptStagedRevisionUseCase(store, options.artifactContentStore ?? null),
    discardStagedRevision: makeDiscardStagedRevisionUseCase(store, options.artifactContentStore ?? null),
    exportDesignHandoff: makeExportDesignHandoffUseCase(store, {
      featureDocsRootDir: options.featureDocsRootDir,
    }),
    getSessionSnapshot: makeGetStudioSessionSnapshotQuery(store),
    listSessionVariants: makeListStudioSessionVariantsQuery(store),
    getDraftMutationBatch: makeGetDraftMutationBatchQuery(store),
    listRevisionManifest: makeListRevisionManifestQuery(store),
    getHandoffBundle: makeGetHandoffBundleQuery(store),
  };
}
