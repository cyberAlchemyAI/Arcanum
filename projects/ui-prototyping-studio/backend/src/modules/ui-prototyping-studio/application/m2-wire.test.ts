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
const OUT_SCOPE = BASE.replace(">T<", ">Tampered<"); // edits card.title (out of scope)

function withModule(
  fn: (m: ReturnType<typeof createStudioOrchestrationModule>, store: ReturnType<typeof createFileBackedStudioSessionStore>) => void,
) {
  const root = mkdtempSync(join(tmpdir(), "ups-mw1-"));
  try {
    const store = createFileBackedStudioSessionStore({ filePath: join(root, "studio.json") });
    const art = createFileArtifactContentStore({ rootDir: join(root, "artifacts") });
    const m = createStudioOrchestrationModule(store, { featureDocsRootDir: root, artifactContentStore: art });
    fn(m, store);
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
}

function prep(m: ReturnType<typeof createStudioOrchestrationModule>): { sid: string; bid: string } {
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
  return { sid, bid };
}

test("MW1: in-scope candidate is admitted + staged (RevisionApplied, head not advanced)", () => {
  withModule((m) => {
    const { sid, bid } = prep(m);
    const r = m.applyAndStage({ sessionId: sid, batchId: bid, candidateHtml: IN_SCOPE, requestedBy: "human:op" });
    assert.equal(r.verdict, "NOT_REJECT");
    assert.equal(r.session.state, "RevisionApplied");
    assert.equal(r.session.revisionHeadId, null); // head NOT advanced at stage
    assert.ok(r.verdict === "NOT_REJECT" && r.diff.changed >= 1); // honest diff measured a change
  });
});

test("MW1: accept commits the staged candidate, advances head, records the honest diff", () => {
  withModule((m, store) => {
    const { sid, bid } = prep(m);
    m.applyAndStage({ sessionId: sid, batchId: bid, candidateHtml: IN_SCOPE, requestedBy: "human:op" });
    const acc = m.acceptStagedRevision({ sessionId: sid, acceptedAt: new Date().toISOString(), requestedBy: "human:op" });
    assert.equal(acc.session.state, "RevisionRecorded");
    assert.ok(acc.session.revisionHeadId && acc.session.revisionHeadId !== "rev-0000");
    assert.ok(acc.revision.diffSummaryHonest && acc.revision.diffSummaryHonest.changed >= 1);
    assert.ok(acc.revision.candidateHtmlHash);
    assert.equal(store.getStagedCandidate(sid), null); // staged cleared
    assert.equal(store.listRevisions(sid).length, 1); // exactly one revision
  });
});

test("MW1: out-of-scope candidate is rejected; nothing staged; head unchanged", () => {
  withModule((m, store) => {
    const { sid, bid } = prep(m);
    const r = m.applyAndStage({ sessionId: sid, batchId: bid, candidateHtml: OUT_SCOPE, requestedBy: "human:op" });
    assert.equal(r.verdict, "REJECT");
    assert.equal(store.getStagedCandidate(sid), null);
    assert.equal(store.getSession(sid)!.revisionHeadId, null);
  });
});

test("MW1: discard drops the staged candidate; accept then fails NO_STAGED_CANDIDATE", () => {
  withModule((m, store) => {
    const { sid, bid } = prep(m);
    m.applyAndStage({ sessionId: sid, batchId: bid, candidateHtml: IN_SCOPE, requestedBy: "human:op" });
    const d = m.discardStagedRevision({ sessionId: sid, requestedBy: "human:op" });
    assert.equal(d.session.state, "MutationApproved");
    assert.equal(store.getStagedCandidate(sid), null);
    try {
      m.acceptStagedRevision({ sessionId: sid, acceptedAt: new Date().toISOString(), requestedBy: "human:op" });
      assert.fail("expected NO_STAGED_CANDIDATE");
    } catch (e) {
      assert.ok(isUiPrototypingStudioError(e) && e.code === "NO_STAGED_CANDIDATE");
    }
  });
});

test("MW1: auto-apply actor is forbidden", () => {
  withModule((m) => {
    const { sid, bid } = prep(m);
    try {
      m.applyAndStage({ sessionId: sid, batchId: bid, candidateHtml: IN_SCOPE, requestedBy: "system:auto" });
      assert.fail("expected AUTO_APPLY_FORBIDDEN");
    } catch (e) {
      assert.ok(isUiPrototypingStudioError(e) && e.code === "AUTO_APPLY_FORBIDDEN");
    }
  });
});
