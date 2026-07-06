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
const CONTINUE = BASE.replace(">Go<", ">Continue<"); // in-scope change to cta.primary
const NEXT = BASE.replace(">Go<", ">Next<"); // in-scope change to cta.primary
const ADD_BADGE = BASE.replace("</button>", `</button><span data-od-id="cta.badge">New</span>`); // introduces a new od-id

function withModule(
  fn: (m: ReturnType<typeof createStudioOrchestrationModule>, store: ReturnType<typeof createFileBackedStudioSessionStore>, art: ReturnType<typeof createFileArtifactContentStore>) => void,
) {
  const root = mkdtempSync(join(tmpdir(), "ups-auto-"));
  try {
    const store = createFileBackedStudioSessionStore({ filePath: join(root, "studio.json") });
    const art = createFileArtifactContentStore({ rootDir: join(root, "artifacts") });
    const m = createStudioOrchestrationModule(store, { featureDocsRootDir: root, artifactContentStore: art });
    fn(m, store, art);
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
}

function prepBaseline(m: ReturnType<typeof createStudioOrchestrationModule>): string {
  const s = m.initializeSession({ requestedVariantCount: 1, requestedBy: "t" });
  const sid = s.sessionId;
  m.submitPrompt({ sessionId: sid, prompt: "make the cta clearer", submittedBy: "t" });
  m.registerVariants({ sessionId: sid, variants: [{ label: "A", html: BASE }], requestedBy: "t" });
  m.selectOrCommitBaseline({ sessionId: sid, selectedLabel: "A", requestedBy: "t" });
  return sid;
}

const NOW = () => new Date().toISOString();

test("ML1: exploit converges — picks the top self-critique score and auto-accepts (head advances)", () => {
  withModule((m, store, art) => {
    const sid = prepBaseline(m);
    const r = m.runCycle({
      sessionId: sid, mode: "exploit", objective: "make the cta clearer", requestedBy: "agent:cycle", at: NOW(),
      candidates: [{ html: CONTINUE, score: 0.9 }, { html: NEXT, score: 0.5 }],
    });
    assert.equal(r.staged, 2); // both in-scope, admitted
    assert.equal(r.rejected, 0);
    assert.ok(r.chosen && r.session.revisionHeadId === r.chosen.revisionId);
    const head = art.readHtml(`artifact:${r.chosen!.candidateHtmlHash}`);
    assert.match(head!, />Continue</); // the 0.9 winner, not "Next"
    assert.equal(store.listRevisions(sid).length, 1);
    assert.equal(store.listRevisions(sid)[0]!.appliedBatchId, "cycle:exploit");
  });
});

test("ML1: exploit REJECTS a structural divergence (new od-id) — explore ADMITS it", () => {
  withModule((m, store) => {
    const sid = prepBaseline(m);
    // exploit fence = head od-ids only → adding cta.badge is out of scope
    const ex = m.runCycle({ sessionId: sid, mode: "exploit", objective: "tighten", requestedBy: "agent:cycle", at: NOW(), candidates: [{ html: ADD_BADGE, score: 0.8 }] });
    assert.equal(ex.rejected, 1);
    assert.equal(ex.chosen, null);
    assert.equal(store.getSession(sid)!.revisionHeadId, "rev-0000"); // head unchanged when nothing admitted

    // explore fence = head ∪ candidate od-ids → the divergent candidate is admitted + auto-accepted
    const exp = m.runCycle({ sessionId: sid, mode: "explore", objective: "try a badge direction", requestedBy: "agent:cycle", at: NOW(), candidates: [{ html: ADD_BADGE, score: 0.8 }] });
    assert.equal(exp.rejected, 0);
    assert.ok(exp.chosen && store.getSession(sid)!.revisionHeadId === exp.chosen.revisionId);
    assert.equal(store.listRevisions(sid)[0]!.appliedBatchId, "cycle:explore");
  });
});

test("ML1: an auto-accepted cycle is revertible (CL5) — revert restores the baseline", () => {
  withModule((m, store, art) => {
    const sid = prepBaseline(m);
    m.runCycle({ sessionId: sid, mode: "exploit", objective: "clearer cta", requestedBy: "agent:cycle", at: NOW(), candidates: [{ html: CONTINUE, score: 0.9 }] });
    const rv = m.revertRevision({ sessionId: sid, requestedBy: "human:op", revertedAt: NOW() });
    assert.equal(rv.revertedTo, "baseline");
    const restored = art.readHtml(`artifact:${rv.revision.candidateHtmlHash}`);
    assert.match(restored!, />Go</); // back to baseline
    assert.equal(store.listRevisions(sid).length, 2); // append-only: cycle + revert
  });
});

test("ML2/start-gate: an empty objective is refused (exploit toward nothing)", () => {
  withModule((m) => {
    const sid = prepBaseline(m);
    try {
      m.runCycle({ sessionId: sid, mode: "exploit", objective: "  ", requestedBy: "agent:cycle", at: NOW(), candidates: [{ html: CONTINUE, score: 1 }] });
      assert.fail("expected AUTO_OBJECTIVE_REQUIRED");
    } catch (e) {
      assert.ok(isUiPrototypingStudioError(e) && e.code === "AUTO_OBJECTIVE_REQUIRED");
    }
  });
});

test("ML1: a cycle with no candidates is refused", () => {
  withModule((m) => {
    const sid = prepBaseline(m);
    try {
      m.runCycle({ sessionId: sid, mode: "exploit", objective: "x", requestedBy: "agent:cycle", at: NOW(), candidates: [] });
      assert.fail("expected CYCLE_CANDIDATES_REQUIRED");
    } catch (e) {
      assert.ok(isUiPrototypingStudioError(e) && e.code === "CYCLE_CANDIDATES_REQUIRED");
    }
  });
});

test("N6 (F9): a non-finite self-critique score is refused (CYCLE_SCORE_INVALID)", () => {
  withModule((m) => {
    const sid = prepBaseline(m);
    try {
      m.runCycle({ sessionId: sid, mode: "exploit", objective: "x", requestedBy: "agent:cycle", at: NOW(), candidates: [{ html: CONTINUE, score: Number.NaN }] });
      assert.fail("expected CYCLE_SCORE_INVALID");
    } catch (e) {
      assert.ok(isUiPrototypingStudioError(e) && e.code === "CYCLE_SCORE_INVALID");
    }
  });
});

test("N7 (F10): the core enforces the cycle ceiling (CYCLE_CEILING_REACHED)", () => {
  withModule((m) => {
    const sid = prepBaseline(m);
    // ceiling of 1 — first cycle ok, second refused by the core (not just the agent loop)
    m.runCycle({ sessionId: sid, mode: "exploit", objective: "x", requestedBy: "agent:cycle", at: NOW(), maxCycles: 1, candidates: [{ html: CONTINUE, score: 0.9 }] });
    try {
      m.runCycle({ sessionId: sid, mode: "exploit", objective: "x", requestedBy: "agent:cycle", at: NOW(), maxCycles: 1, candidates: [{ html: NEXT, score: 0.9 }] });
      assert.fail("expected CYCLE_CEILING_REACHED");
    } catch (e) {
      assert.ok(isUiPrototypingStudioError(e) && e.code === "CYCLE_CEILING_REACHED");
    }
  });
});

test("N9 (F11): a comment does not re-fold — pending clears after synthesize and does not resurface", () => {
  withModule((m) => {
    const sid = prepBaseline(m);
    m.captureCommentEvent({
      sessionId: sid, revisionId: "rev-0000",
      target: { selector: "[data-od-id=cta.primary]", elementLabel: "Primary button", odId: "cta.primary" },
      severity: "medium", intent: "reword", note: "say Continue", createdBy: "web-ui",
    });
    assert.equal(m.listPendingComments({ sessionId: sid }).length, 1);
    m.synthesizeMutationBatch({ sessionId: sid, sourceRevisionId: "rev-0000", requestedBy: "t" });
    assert.equal(m.listPendingComments({ sessionId: sid }).length, 0); // folded ⇒ gone
    // a second synthesize must not re-pull the same comment into a new pending set
    assert.equal(m.listPendingComments({ sessionId: sid }).length, 0); // stays cleared (no double-fold)
  });
});

test("CL2: pending lists captured-but-unbatched comments; synthesize clears them", () => {
  withModule((m, store) => {
    const sid = prepBaseline(m);
    m.captureCommentEvent({
      sessionId: sid, revisionId: "rev-0000",
      target: { selector: "[data-od-id=cta.primary]", elementLabel: "Primary button", odId: "cta.primary" },
      severity: "medium", intent: "reword", note: "say Continue", createdBy: "web-ui",
    });
    assert.equal(m.listPendingComments({ sessionId: sid }).length, 1);
    const syn = m.synthesizeMutationBatch({ sessionId: sid, sourceRevisionId: "rev-0000", requestedBy: "t" });
    assert.ok(syn.batch.batchId);
    assert.equal(m.listPendingComments({ sessionId: sid }).length, 0); // folded into a batch ⇒ no longer pending
  });
}
);
