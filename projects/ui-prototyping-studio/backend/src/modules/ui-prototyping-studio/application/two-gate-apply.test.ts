import assert from "node:assert/strict";
import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { test } from "node:test";

import { isUiPrototypingStudioError } from "../domain/errors.js";
import { createFileArtifactContentStore } from "../infrastructure/file-artifact-content-store.js";
import { acceptStaged, discardStaged, validateAndStage } from "./two-gate-apply.js";

const SCOPE = ["cta.primary"];
const CURRENT = `<div data-od-id="card.root"><button data-od-id="cta.primary">Go</button><h2 data-od-id="card.title">T</h2></div>`;
const IN_SCOPE = CURRENT.replace(">Go<", ">Continue<");      // edits cta.primary
const OUT_OF_SCOPE = CURRENT.replace(">T<", ">Tampered<");   // edits card.title

function withArtifact(fn: (a: ReturnType<typeof createFileArtifactContentStore>) => void) {
  const root = mkdtempSync(join(tmpdir(), "ups-2gate-"));
  try { fn(createFileArtifactContentStore({ rootDir: root })); }
  finally { rmSync(root, { recursive: true, force: true }); }
}

test("M2: in-scope candidate is admitted and staged (RevisionApplied, not head)", () => {
  withArtifact((a) => {
    const r = validateAndStage(CURRENT, IN_SCOPE, SCOPE, a);
    assert.equal(r.verdict, "NOT_REJECT");
    assert.ok(r.verdict === "NOT_REJECT" && r.stagedRef.startsWith("staged:"));
    assert.ok(r.verdict === "NOT_REJECT" && a.readHtml(r.stagedRef) === IN_SCOPE);
  });
});

test("M2: out-of-scope candidate is rejected and nothing is staged", () => {
  withArtifact((a) => {
    const r = validateAndStage(CURRENT, OUT_OF_SCOPE, SCOPE, a);
    assert.equal(r.verdict, "REJECT");
  });
});

test("M2: accept commits exactly the staged hash (seen == recorded)", () => {
  withArtifact((a) => {
    const r = validateAndStage(CURRENT, IN_SCOPE, SCOPE, a);
    assert.ok(r.verdict === "NOT_REJECT");
    const committed = acceptStaged(r.stagedRef, r.candidateHtmlHash, a);
    assert.ok(committed.committedRef.startsWith("artifact:"));
    assert.equal(a.readHtml(committed.committedRef), IN_SCOPE);
    assert.equal(a.readHtml(r.stagedRef), null); // moved to head, no longer staged
  });
});

test("M2: accept with a different hash is fail-closed (CANDIDATE_HASH_MISMATCH)", () => {
  withArtifact((a) => {
    const r = validateAndStage(CURRENT, IN_SCOPE, SCOPE, a);
    assert.ok(r.verdict === "NOT_REJECT");
    try {
      acceptStaged(r.stagedRef, "0".repeat(64), a);
      assert.fail("expected mismatch");
    } catch (e) {
      assert.ok(isUiPrototypingStudioError(e) && e.code === "CANDIDATE_HASH_MISMATCH");
    }
  });
});

test("M2: discard drops the staged candidate; accept then fails", () => {
  withArtifact((a) => {
    const r = validateAndStage(CURRENT, IN_SCOPE, SCOPE, a);
    assert.ok(r.verdict === "NOT_REJECT");
    discardStaged(r.stagedRef, a);
    assert.equal(a.readHtml(r.stagedRef), null);
    try {
      acceptStaged(r.stagedRef, r.candidateHtmlHash, a);
      assert.fail("expected no-staged");
    } catch (e) {
      assert.ok(isUiPrototypingStudioError(e) && e.code === "NO_STAGED_CANDIDATE");
    }
  });
});
