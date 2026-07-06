import assert from "node:assert/strict";
import { mkdtempSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import test from "node:test";

import { makeApplyApprovedBatchUseCase } from "./apply-approved-batch.js";
import { makeApproveMutationBatchUseCase } from "./approve-mutation-batch.js";
import { makeCaptureCommentEventUseCase } from "./capture-comment-event.js";
import { makeExportDesignHandoffUseCase } from "./export-design-handoff.js";
import { makeGenerateStudioVariantsUseCase } from "./generate-variants.js";
import { makeGetDraftMutationBatchQuery } from "./get-draft-mutation-batch.js";
import { makeGetHandoffBundleQuery } from "./get-handoff-bundle.js";
import { makeGetStudioSessionSnapshotQuery } from "./get-session-snapshot.js";
import { makeInitializeStudioSessionUseCase } from "./initialize-session.js";
import { makeListRevisionManifestQuery } from "./list-revision-manifest.js";
import { makeSelectOrCommitBaselineUseCase } from "./select-or-commit-baseline.js";
import { createInMemoryStudioSessionStore } from "./session-store.js";
import { makeSubmitStudioPromptUseCase } from "./submit-prompt.js";
import { makeSynthesizeMutationBatchUseCase } from "./synthesize-mutation-batch.js";
import { isUiPrototypingStudioError } from "../domain/errors.js";

test("UPS-CON-001 UPS-OP-001 ui-prototyping-studio InitializeSession defaults variantCount to 3 and enforces 1..3", () => {
  const context = createTestContext();

  const defaultSession = context.initializeSession({
    requestedBy: "test-suite",
  });

  assert.equal(defaultSession.variantCount, 3);
  assert.deepEqual(defaultSession.variantLabels, ["A", "B", "C"]);
  assert.equal(defaultSession.selectionGate, "pending");
  assert.equal(defaultSession.applyGate, "pending");
  assert.equal(defaultSession.state, "SessionInitialized");

  assert.throws(
    () =>
      context.initializeSession({
        requestedVariantCount: 4,
        requestedBy: "test-suite",
      }),
    (error) => {
      assert.ok(isUiPrototypingStudioError(error));
      assert.equal(error.code, "VARIANT_COUNT_OUT_OF_RANGE");
      return true;
    },
  );
});

test("UPS-ST-001 ui-prototyping-studio SubmitPrompt transitions SessionInitialized to PromptCaptured", () => {
  const context = createTestContext();
  const session = context.initializeSession({
    requestedVariantCount: 3,
    requestedBy: "test-suite",
  });

  const updated = context.submitPrompt({
    sessionId: session.sessionId,
    prompt: "Generate a dashboard with KPI cards",
    submittedBy: "test-suite",
  });

  assert.equal(updated.state, "PromptCaptured");
  assert.equal(updated.prompt, "Generate a dashboard with KPI cards");
});

test("UPS-CON-002 UPS-OP-002 UPS-ST-002 ui-prototyping-studio GenerateVariants emits exact variant count and metadata contract", () => {
  const context = createTestContext();
  const session = context.initializeSession({
    requestedVariantCount: 3,
    requestedBy: "test-suite",
  });

  context.submitPrompt({
    sessionId: session.sessionId,
    prompt: "Landing page for product onboarding",
    submittedBy: "test-suite",
  });

  const result = context.generateVariants({
    sessionId: session.sessionId,
    requestedBy: "test-suite",
  });

  assert.equal(result.session.state, "VariantsReady");
  assert.equal(result.variants.length, 3);
  assert.deepEqual(
    result.variants.map((variant) => variant.variantLabel),
    ["A", "B", "C"],
  );

  for (const variant of result.variants) {
    assert.ok(variant.componentsUsed.length > 0);
    assert.ok(variant.rationale.length > 0);
    assert.ok(variant.tradeoffs.length > 0);
    assert.ok(variant.risk.length > 0);
  }
});

test("UPS-CON-003 UPS-OP-003 UPS-ST-003 ui-prototyping-studio multi-variant branch requires explicit baseline selection", () => {
  const context = createTestContext();
  const session = context.initializeSession({
    requestedVariantCount: 3,
    requestedBy: "test-suite",
  });

  context.submitPrompt({
    sessionId: session.sessionId,
    prompt: "Workspace app shell",
    submittedBy: "test-suite",
  });

  const generation = context.generateVariants({
    sessionId: session.sessionId,
    requestedBy: "test-suite",
  });

  assert.equal(generation.session.selectionGate, "pending");

  assert.throws(
    () =>
      context.selectOrCommitBaseline({
        sessionId: session.sessionId,
        requestedBy: "test-suite",
      }),
    (error) => {
      assert.ok(isUiPrototypingStudioError(error));
      assert.equal(error.code, "BASELINE_SELECTION_REQUIRED");
      return true;
    },
  );

  const baseline = context.selectOrCommitBaseline({
    sessionId: session.sessionId,
    selectedLabel: "B",
    requestedBy: "test-suite",
  });

  assert.equal(baseline.session.state, "BaselineReady");
  assert.equal(baseline.session.selectionGate, "satisfied");
  assert.equal(baseline.session.baseline?.mode, "selected");
  assert.equal(baseline.session.baseline?.label, "B");
});

test("UPS-OP-004 UPS-ST-004 ui-prototyping-studio single-variant branch uses committed baseline", () => {
  const context = createTestContext();
  const session = context.initializeSession({
    requestedVariantCount: 1,
    requestedBy: "test-suite",
  });

  context.submitPrompt({
    sessionId: session.sessionId,
    prompt: "Simple profile card",
    submittedBy: "test-suite",
  });

  const generation = context.generateVariants({
    sessionId: session.sessionId,
    requestedBy: "test-suite",
  });

  assert.equal(generation.variants.length, 1);
  assert.equal(generation.session.selectionGate, "satisfied");
  assert.equal(generation.session.baseline?.mode, "committed");
  assert.equal(generation.session.baseline?.label, "A");

  const baseline = context.selectOrCommitBaseline({
    sessionId: session.sessionId,
    requestedBy: "test-suite",
  });

  assert.equal(baseline.session.state, "BaselineReady");
  assert.equal(baseline.session.baseline?.mode, "committed");
  assert.equal(baseline.session.baseline?.label, "A");
});

test("UPS-CON-004 UPS-OP-005 UPS-ST-005 ui-prototyping-studio CaptureCommentEvent enforces gate/schema and transitions to CommentsCaptured", () => {
  const context = createTestContext();
  const session = prepareBaselineReadySession(context, 3);

  const notReadySession = context.initializeSession({
    requestedVariantCount: 3,
    requestedBy: "test-suite",
  });

  assert.throws(
    () =>
      context.captureCommentEvent({
        sessionId: notReadySession.sessionId,
        revisionId: "rev-0000",
        target: {
          selector: "#hero",
          elementLabel: "Hero",
        },
        severity: "high",
        intent: "Improve readability",
        note: "Increase heading contrast.",
        createdBy: "test-suite",
      }),
    (error) => {
      assert.ok(isUiPrototypingStudioError(error));
      assert.equal(error.code, "BASELINE_GATE_UNSATISFIED");
      return true;
    },
  );

  assert.throws(
    () =>
      context.captureCommentEvent({
        sessionId: session.sessionId,
        revisionId: "rev-0000",
        target: {
          selector: "#hero",
          elementLabel: "Hero",
        },
        severity: "critical",
        intent: "Improve readability",
        note: "Increase heading contrast.",
        createdBy: "test-suite",
      }),
    (error) => {
      assert.ok(isUiPrototypingStudioError(error));
      assert.equal(error.code, "COMMENT_SCHEMA_INVALID");
      return true;
    },
  );

  const comment = context.captureCommentEvent({
    sessionId: session.sessionId,
    revisionId: "rev-0000",
    target: {
      selector: "#hero",
      elementLabel: "Hero",
    },
    severity: "high",
    intent: "Improve readability",
    note: "Increase heading contrast.",
    createdBy: "test-suite",
  });

  assert.equal(comment.revisionId, "rev-0000");
  assert.equal(comment.target.selector, "#hero");

  const snapshot = context.getSessionSnapshot({
    sessionId: session.sessionId,
  });
  assert.equal(snapshot.state, "CommentsCaptured");
});

test("UPS-CON-005 UPS-OP-006 UPS-QRY-003 UPS-ST-006 ui-prototyping-studio synthesis remains deterministic and approval opens apply gate", () => {
  const context = createTestContext();
  const session = prepareBaselineReadySession(context, 3);

  assert.throws(
    () =>
      context.synthesizeMutationBatch({
        sessionId: session.sessionId,
        sourceRevisionId: "rev-0000",
        requestedBy: "test-suite",
      }),
    (error) => {
      assert.ok(isUiPrototypingStudioError(error));
      assert.equal(error.code, "COMMENT_SET_EMPTY");
      return true;
    },
  );

  context.captureCommentEvent({
    sessionId: session.sessionId,
    revisionId: "rev-0000",
    target: {
      selector: "#hero",
      elementLabel: "Hero",
    },
    severity: "high",
    intent: "Increase contrast",
    note: "Boost heading contrast ratio.",
    createdBy: "test-suite",
  });

  context.captureCommentEvent({
    sessionId: session.sessionId,
    revisionId: "rev-0000",
    target: {
      selector: "#summary",
      elementLabel: "Summary card",
    },
    severity: "medium",
    intent: "Add spacing",
    note: "Increase vertical rhythm.",
    createdBy: "test-suite",
  });

  const first = context.synthesizeMutationBatch({
    sessionId: session.sessionId,
    sourceRevisionId: "rev-0000",
    requestedBy: "test-suite",
  });
  const second = context.synthesizeMutationBatch({
    sessionId: session.sessionId,
    sourceRevisionId: "rev-0000",
    requestedBy: "test-suite",
  });

  assert.notEqual(first.batch.batchId, second.batch.batchId);
  assert.equal(first.batch.checksum, second.batch.checksum);
  assert.deepEqual(
    first.batch.tasks.map((task) => task.taskId),
    second.batch.tasks.map((task) => task.taskId),
  );

  const draft = context.getDraftMutationBatch({
    sessionId: session.sessionId,
    batchId: first.batch.batchId,
  });
  assert.equal(draft.status, "draft");

  assert.throws(
    () =>
      context.approveMutationBatch({
        sessionId: session.sessionId,
        batchId: first.batch.batchId,
        approvedBy: "",
        approvedAt: "",
      }),
    (error) => {
      assert.ok(isUiPrototypingStudioError(error));
      assert.equal(error.code, "APPROVAL_METADATA_REQUIRED");
      return true;
    },
  );

  const approved = context.approveMutationBatch({
    sessionId: session.sessionId,
    batchId: first.batch.batchId,
    approvedBy: "qa-reviewer",
    approvedAt: "2026-05-08T00:00:00.000Z",
  });

  assert.equal(approved.batch.status, "approved");
  assert.equal(approved.session.applyGate, "satisfied");
  assert.equal(approved.session.state, "MutationApproved");
});

test("UPS-CON-006 UPS-CON-007 UPS-OP-008 UPS-QRY-004 UPS-ST-008 ui-prototyping-studio apply requires manual actor and appends one revision", () => {
  const context = createTestContext();
  const session = prepareBaselineReadySession(context, 3);
  const draft = prepareApprovedBatch(context, session.sessionId);

  assert.throws(
    () =>
      context.applyApprovedBatch({
        sessionId: session.sessionId,
        batchId: draft.batchId,
        applyRequestedBy: "system:auto",
      }),
    (error) => {
      assert.ok(isUiPrototypingStudioError(error));
      assert.equal(error.code, "AUTO_APPLY_FORBIDDEN");
      return true;
    },
  );

  const applied = context.applyApprovedBatch({
    sessionId: session.sessionId,
    batchId: draft.batchId,
    applyRequestedBy: "test-suite",
  });

  assert.equal(applied.batch.status, "applied");
  assert.equal(applied.session.state, "RevisionRecorded");
  assert.equal(applied.session.revisionHeadId, applied.revision.revisionId);
  assert.equal(applied.revision.parentRevisionId, "rev-0000");

  const revisions = context.listRevisionManifest({
    sessionId: session.sessionId,
    newestFirst: true,
  });
  assert.equal(revisions.length, 1);
  assert.equal(revisions[0]?.revisionId, applied.revision.revisionId);
});

test("UPS-CON-008 UPS-CON-009 UPS-CON-010 UPS-OP-009 UPS-OP-010 UPS-QRY-005 UPS-ST-009 ui-prototyping-studio handoff export and retrieval require revision evidence", () => {
  const context = createTestContext();
  const session = prepareBaselineReadySession(context, 1);

  assert.throws(
    () =>
      context.getHandoffBundle({
        sessionId: session.sessionId,
      }),
    (error) => {
      assert.ok(isUiPrototypingStudioError(error));
      assert.equal(error.code, "HANDOFF_BUNDLE_NOT_READY");
      return true;
    },
  );

  assert.throws(
    () =>
      context.exportDesignHandoff({
        sessionId: session.sessionId,
        requestedBy: "test-suite",
        confirmedBy: "test-suite", // N1: confirm passes so this reaches the revision-required check it tests
      }),
    (error) => {
      assert.ok(isUiPrototypingStudioError(error));
      assert.equal(error.code, "HANDOFF_REVISION_REQUIRED");
      return true;
    },
  );

  const approvedDraft = prepareApprovedBatch(context, session.sessionId);
  context.applyApprovedBatch({
    sessionId: session.sessionId,
    batchId: approvedDraft.batchId,
    applyRequestedBy: "test-suite",
  });

  const exported = context.exportDesignHandoff({
    sessionId: session.sessionId,
    requestedBy: "test-suite",
    confirmedBy: "test-suite", // N1: export is the one irreversible edge — confirmation required
    exportProfile: "mvp",
  });
  assert.equal(exported.bundle.storyRefs.length, 1);
  assert.equal(exported.bundle.requirementRefs.length, 1);
  assert.equal(exported.bundle.acceptanceRefs.length, 1);
  assert.equal(
    exported.bundle.uiSpecRef,
    "docs/features/ui-prototyping-studio/UI-SPEC.md",
  );
  assert.equal(
    exported.bundle.testSpecRef,
    "docs/features/ui-prototyping-studio/TEST-SPEC.md",
  );

  const handoff = context.getHandoffBundle({
    sessionId: session.sessionId,
  });
  assert.equal(handoff.revisionHeadId, exported.bundle.revisionHeadId);

  const snapshot = context.getSessionSnapshot({
    sessionId: session.sessionId,
  });
  assert.equal(snapshot.integration.uiPhaseBridgeReady, true);
  assert.equal(snapshot.integration.generateTestsUiReady, true);
  assert.equal(snapshot.integration.uiImplementReady, true);
});

test("ui-prototyping-studio handoff export can use a target-specific profile", () => {
  const featureDocsRootDir = mkdtempSync(join(tmpdir(), "ups-handoff-profile-"));
  writeFileSync(
    join(featureDocsRootDir, "troqar-profile.json"),
    JSON.stringify({
      profileId: "troqar-product-architecture",
      storyRefs: ["projects/body-war/docs/features/troqar-product-architecture/SPEC.md"],
      requirementRefs: ["projects/body-war/docs/features/troqar-product-architecture/UI-SPEC.md#requirements"],
      acceptanceRefs: ["projects/body-war/docs/features/troqar-product-architecture/TEST-SPEC.md#acceptance"],
      uiSpecRef: "projects/body-war/docs/features/troqar-product-architecture/UI-SPEC.md",
      testSpecRef: "projects/body-war/docs/features/troqar-product-architecture/TEST-SPEC.md",
      sourceRefs: ["projects/body-war/docs/features/troqar-product-architecture/VISUAL-DEFINITIONS.md"],
    }),
    "utf8",
  );
  const context = createTestContext(featureDocsRootDir);
  const session = prepareBaselineReadySession(context, 1);
  const approvedDraft = prepareApprovedBatch(context, session.sessionId);
  context.applyApprovedBatch({
    sessionId: session.sessionId,
    batchId: approvedDraft.batchId,
    applyRequestedBy: "test-suite",
  });

  const exported = context.exportDesignHandoff({
    sessionId: session.sessionId,
    requestedBy: "test-suite",
    confirmedBy: "test-suite",
    exportProfile: "troqar-profile.json",
  });

  assert.equal(exported.bundle.exportProfile, "troqar-product-architecture");
  assert.equal(
    exported.bundle.uiSpecRef,
    "projects/body-war/docs/features/troqar-product-architecture/UI-SPEC.md",
  );
  assert.equal(
    exported.bundle.testSpecRef,
    "projects/body-war/docs/features/troqar-product-architecture/TEST-SPEC.md",
  );
  assert.deepEqual(exported.bundle.sourceRefs, [
    "projects/body-war/docs/features/troqar-product-architecture/VISUAL-DEFINITIONS.md",
  ]);
});

function prepareBaselineReadySession(
  context: ReturnType<typeof createTestContext>,
  variantCount: 1 | 2 | 3,
) {
  const session = context.initializeSession({
    requestedVariantCount: variantCount,
    requestedBy: "test-suite",
  });

  context.submitPrompt({
    sessionId: session.sessionId,
    prompt: "Prepare deterministic workflow",
    submittedBy: "test-suite",
  });

  context.generateVariants({
    sessionId: session.sessionId,
    requestedBy: "test-suite",
  });

  if (variantCount > 1) {
    context.selectOrCommitBaseline({
      sessionId: session.sessionId,
      selectedLabel: "B",
      requestedBy: "test-suite",
    });
  } else {
    context.selectOrCommitBaseline({
      sessionId: session.sessionId,
      requestedBy: "test-suite",
    });
  }

  return session;
}

function prepareApprovedBatch(
  context: ReturnType<typeof createTestContext>,
  sessionId: string,
) {
  context.captureCommentEvent({
    sessionId,
    revisionId: "rev-0000",
    target: {
      selector: "#primary",
      elementLabel: "Primary panel",
    },
    severity: "high",
    intent: "Improve hierarchy",
    note: "Promote primary action clarity.",
    createdBy: "test-suite",
  });

  const draft = context.synthesizeMutationBatch({
    sessionId,
    sourceRevisionId: "rev-0000",
    requestedBy: "test-suite",
  });

  const approved = context.approveMutationBatch({
    sessionId,
    batchId: draft.batch.batchId,
    approvedBy: "qa-reviewer",
    approvedAt: "2026-05-08T00:00:00.000Z",
  });

  return approved.batch;
}

function createTestContext(featureDocsRootOverride?: string) {
  const store = createInMemoryStudioSessionStore();
  const featureDocsRootDir = featureDocsRootOverride ?? resolve(
    process.cwd(),
    "..",
    "provenance",
    "legacy-domainspec-spec",
  );

  return {
    initializeSession: makeInitializeStudioSessionUseCase(store),
    submitPrompt: makeSubmitStudioPromptUseCase(store),
    generateVariants: makeGenerateStudioVariantsUseCase(store),
    selectOrCommitBaseline: makeSelectOrCommitBaselineUseCase(store),
    captureCommentEvent: makeCaptureCommentEventUseCase(store),
    synthesizeMutationBatch: makeSynthesizeMutationBatchUseCase(store),
    approveMutationBatch: makeApproveMutationBatchUseCase(store),
    applyApprovedBatch: makeApplyApprovedBatchUseCase(store),
    exportDesignHandoff: makeExportDesignHandoffUseCase(store, {
      featureDocsRootDir,
    }),
    getSessionSnapshot: makeGetStudioSessionSnapshotQuery(store),
    getDraftMutationBatch: makeGetDraftMutationBatchQuery(store),
    listRevisionManifest: makeListRevisionManifestQuery(store),
    getHandoffBundle: makeGetHandoffBundleQuery(store),
  };
}
