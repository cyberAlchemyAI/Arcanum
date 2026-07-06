import assert from "node:assert/strict";
import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { test } from "node:test";

import { isUiPrototypingStudioError } from "../domain/errors.js";
import { createFileArtifactContentStore } from "../infrastructure/file-artifact-content-store.js";
import { createFileBackedStudioSessionStore } from "../infrastructure/file-studio-session-store.js";
import { createStudioOrchestrationModule } from "./studio-orchestration-module.js";

const BASE = `<div data-od-id="card.root"><button data-od-id="cta.primary">Go</button><h2 data-od-id="card.title">T</h2></div>`;
const IN_SCOPE = BASE.replace(">Go<", ">Continue<"); // edits cta.primary (in scope)

function withModule(
  fn: (m: ReturnType<typeof createStudioOrchestrationModule>, store: ReturnType<typeof createFileBackedStudioSessionStore>, art: ReturnType<typeof createFileArtifactContentStore>) => void,
) {
  const root = mkdtempSync(join(tmpdir(), "ups-cl5-"));
  try {
    const store = createFileBackedStudioSessionStore({ filePath: join(root, "studio.json") });
    const art = createFileArtifactContentStore({ rootDir: join(root, "artifacts") });
    const m = createStudioOrchestrationModule(store, { featureDocsRootDir: root, artifactContentStore: art });
    fn(m, store, art);
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
}

/** Prep through one accepted revision (head = rev with cta.primary reworded to "Continue"). */
function prepAccepted(m: ReturnType<typeof createStudioOrchestrationModule>): { sid: string } {
  const s = m.initializeSession({ requestedVariantCount: 1, requestedBy: "t" });
  const sid = s.sessionId;
  m.submitPrompt({ sessionId: sid, prompt: "reword cta", submittedBy: "t" });
  m.registerVariants({ sessionId: sid, variants: [{ label: "A", html: BASE }], requestedBy: "t" });
  m.captureCommentEvent({
    sessionId: sid,
    revisionId: "rev-0000",
    target: { selector: "[data-od-id=cta.primary]", elementLabel: "Primary button", odId: "cta.primary" },
    severity: "medium",
    intent: "reword",
    note: "say Continue",
    createdBy: "t",
  });
  const syn = m.synthesizeMutationBatch({ sessionId: sid, sourceRevisionId: "rev-0000", requestedBy: "t" });
  const bid = syn.batch.batchId;
  m.approveMutationBatch({ sessionId: sid, batchId: bid, approvedBy: "t", approvedAt: new Date().toISOString() });
  m.applyAndStage({ sessionId: sid, batchId: bid, candidateHtml: IN_SCOPE, requestedBy: "human:op" });
  m.acceptStagedRevision({ sessionId: sid, acceptedAt: new Date().toISOString(), requestedBy: "human:op" });
  return { sid };
}

test("CL5: revert undoes one step — head HTML equals the pre-accept (baseline) HTML", () => {
  withModule((m, store, art) => {
    const { sid } = prepAccepted(m);
    const head1 = store.getSession(sid)!.revisionHeadId!;
    const acceptedHtml = art.readHtml(`artifact:${store.listRevisions(sid).find((r) => r.revisionId === head1)!.candidateHtmlHash}`);
    assert.match(acceptedHtml!, />Continue</); // sanity: accept applied

    const rv = m.revertRevision({ sessionId: sid, requestedBy: "agent:cycle", revertedAt: new Date().toISOString() });
    assert.equal(rv.revertedTo, "baseline");
    // head moved FORWARD (new revision id), content went BACK to baseline ("Go")
    assert.notEqual(rv.session.revisionHeadId, head1);
    const restored = art.readHtml(`artifact:${rv.revision.candidateHtmlHash}`);
    assert.match(restored!, />Go</);
    assert.doesNotMatch(restored!, />Continue</);
  });
});

test("CL5: revert is append-only — the manifest shows BOTH events and never shrinks", () => {
  withModule((m, store) => {
    const { sid } = prepAccepted(m);
    assert.equal(store.listRevisions(sid).length, 1);
    m.revertRevision({ sessionId: sid, requestedBy: "agent:cycle", revertedAt: new Date().toISOString() });
    const after = store.listRevisions(sid);
    assert.equal(after.length, 2); // appended, not rewound
    assert.ok(after.some((r) => r.appliedBatchId.startsWith("revert:")));
  });
});

test("CL5: a revert is itself revertible — revert twice restores the accepted content", () => {
  withModule((m, store, art) => {
    const { sid } = prepAccepted(m);
    const acceptedRev = store.listRevisions(sid)[0]!;
    m.revertRevision({ sessionId: sid, requestedBy: "agent:cycle", revertedAt: new Date().toISOString() }); // -> baseline ("Go")
    // revert again, explicitly targeting the original accepted revision -> restores "Continue"
    const rv2 = m.revertRevision({ sessionId: sid, targetRevisionId: acceptedRev.revisionId, requestedBy: "agent:cycle", revertedAt: new Date().toISOString() });
    const restored = art.readHtml(`artifact:${rv2.revision.candidateHtmlHash}`);
    assert.match(restored!, />Continue</);
    assert.equal(store.listRevisions(sid).length, 3); // three append-only events
  });
});

test("CL5: revert with no recorded revision fails NO_REVISION_TO_REVERT", () => {
  withModule((m) => {
    const s = m.initializeSession({ requestedVariantCount: 1, requestedBy: "t" });
    try {
      m.revertRevision({ sessionId: s.sessionId, requestedBy: "agent:cycle", revertedAt: new Date().toISOString() });
      assert.fail("expected NO_REVISION_TO_REVERT");
    } catch (e) {
      assert.ok(isUiPrototypingStudioError(e) && e.code === "NO_REVISION_TO_REVERT");
    }
  });
});

test("CL5: revert to an unknown revision fails REVISION_NOT_FOUND", () => {
  withModule((m) => {
    const { sid } = prepAccepted(m);
    try {
      m.revertRevision({ sessionId: sid, targetRevisionId: "rev-9999", requestedBy: "agent:cycle", revertedAt: new Date().toISOString() });
      assert.fail("expected REVISION_NOT_FOUND");
    } catch (e) {
      assert.ok(isUiPrototypingStudioError(e) && e.code === "REVISION_NOT_FOUND");
    }
  });
});

test("N4 (F5): revert --to a revision with no committed content ERRORS, not a silent baseline restore", () => {
  withModule((m, store) => {
    const { sid } = prepAccepted(m);
    // forge a legacy-style revision with no candidateHtmlHash (as applyApprovedBatch would record)
    const head = store.getSession(sid)!.revisionHeadId!;
    const legacyId = store.allocateRevisionId(head);
    store.appendRevision({
      revisionId: legacyId, parentRevisionId: head, sessionId: sid,
      variantCount: store.getSession(sid)!.variantCount, baseline: store.getSession(sid)!.baseline!,
      appliedBatchId: "legacy", appliedTaskIds: [], unresolvedCommentIds: [],
      diffSummary: { added: 0, changed: 0, removed: 0 }, createdAt: new Date().toISOString(),
    });
    try {
      m.revertRevision({ sessionId: sid, targetRevisionId: legacyId, requestedBy: "human:op", revertedAt: new Date().toISOString() });
      assert.fail("expected REVISION_NOT_FOUND (no committed content)");
    } catch (e) {
      assert.ok(isUiPrototypingStudioError(e) && e.code === "REVISION_NOT_FOUND");
    }
  });
});
