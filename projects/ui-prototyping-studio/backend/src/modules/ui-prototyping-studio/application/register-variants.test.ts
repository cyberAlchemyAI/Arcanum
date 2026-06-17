import assert from "node:assert/strict";
import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { test } from "node:test";

import { isUiPrototypingStudioError } from "../domain/errors.js";
import { createFileArtifactContentStore } from "../infrastructure/file-artifact-content-store.js";
import { createFileBackedStudioSessionStore } from "../infrastructure/file-studio-session-store.js";
import { createStudioOrchestrationModule } from "./studio-orchestration-module.js";

const GOOD = `<div data-od-id="card.root"><button data-od-id="cta.primary">Go</button></div>`;
const BAD = `<div><button>Go</button></div>`;

function withModule(
  fn: (m: ReturnType<typeof createStudioOrchestrationModule>, art: ReturnType<typeof createFileArtifactContentStore>) => void,
) {
  const root = mkdtempSync(join(tmpdir(), "ups-register-"));
  try {
    const store = createFileBackedStudioSessionStore({ filePath: join(root, "studio.json") });
    const art = createFileArtifactContentStore({ rootDir: join(root, "artifacts") });
    const m = createStudioOrchestrationModule(store, {
      featureDocsRootDir: root,
      artifactContentStore: art,
    });
    fn(m, art);
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
}

function openWithPrompt(m: ReturnType<typeof createStudioOrchestrationModule>): string {
  const s = m.initializeSession({ requestedVariantCount: 1, requestedBy: "t" });
  m.submitPrompt({ sessionId: s.sessionId, prompt: "reword cta", submittedBy: "t" });
  return s.sessionId;
}

test("MR1: GOOD html is admitted, committed, and readable as real content", () => {
  withModule((m, art) => {
    const sid = openWithPrompt(m);
    const r = m.registerVariants({ sessionId: sid, variants: [{ label: "A", html: GOOD }], requestedBy: "t" });
    assert.equal(r.session.state, "VariantsReady");
    const ref = r.variants[0]!.htmlArtifactRef;
    const stored = art.readHtml(ref);
    assert.ok(stored && stored.includes("data-od-id"), "committed HTML resolves and carries data-od-id");
  });
});

test("MR1: BAD html (no data-od-id) is rejected with OD_ID_MISSING (nothing committed)", () => {
  withModule((m) => {
    const sid = openWithPrompt(m);
    try {
      m.registerVariants({ sessionId: sid, variants: [{ label: "A", html: BAD }], requestedBy: "t" });
      assert.fail("expected OD_ID_MISSING");
    } catch (e) {
      assert.ok(isUiPrototypingStudioError(e) && e.code === "OD_ID_MISSING");
    }
  });
});

test("MR1: registering identical HTML yields the same content-addressed ref (idempotent)", () => {
  withModule((m) => {
    const a = openWithPrompt(m);
    const b = openWithPrompt(m);
    const r1 = m.registerVariants({ sessionId: a, variants: [{ label: "A", html: GOOD }], requestedBy: "t" });
    const r2 = m.registerVariants({ sessionId: b, variants: [{ label: "A", html: GOOD }], requestedBy: "t" });
    assert.equal(r1.variants[0]!.htmlArtifactRef, r2.variants[0]!.htmlArtifactRef);
  });
});

test("MR1: registration without an artifact content store fails closed", () => {
  const root = mkdtempSync(join(tmpdir(), "ups-register-noport-"));
  try {
    const store = createFileBackedStudioSessionStore({ filePath: join(root, "studio.json") });
    const m = createStudioOrchestrationModule(store, { featureDocsRootDir: root }); // no artifactContentStore
    const s = m.initializeSession({ requestedVariantCount: 1, requestedBy: "t" });
    m.submitPrompt({ sessionId: s.sessionId, prompt: "x", submittedBy: "t" });
    try {
      m.registerVariants({ sessionId: s.sessionId, variants: [{ label: "A", html: GOOD }], requestedBy: "t" });
      assert.fail("expected ARTIFACT_CONTENT_PORT_UNAVAILABLE");
    } catch (e) {
      assert.ok(isUiPrototypingStudioError(e) && e.code === "ARTIFACT_CONTENT_PORT_UNAVAILABLE");
    }
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});
