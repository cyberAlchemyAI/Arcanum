import assert from "node:assert/strict";
import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { test } from "node:test";

import { createFileArtifactContentStore } from "../infrastructure/file-artifact-content-store.js";

function withStore(fn: (store: ReturnType<typeof createFileArtifactContentStore>) => void) {
  const root = mkdtempSync(join(tmpdir(), "ups-artifact-"));
  try {
    fn(createFileArtifactContentStore({ rootDir: root }));
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
}

test("M0b: stage → read returns the staged html + a content hash", () => {
  withStore((store) => {
    const html = `<button data-od-id="cta.primary">Go</button>`;
    const staged = store.stageHtml(html);
    assert.ok(staged.stagedRef.startsWith("staged:"));
    assert.equal(staged.hash.length, 64);
    assert.equal(store.readHtml(staged.stagedRef), html);
  });
});

test("M0b: commit promotes staged → committed; staged ref no longer resolves", () => {
  withStore((store) => {
    const html = `<div data-od-id="card.root">x</div>`;
    const staged = store.stageHtml(html);
    const committedRef = store.commitHtml(staged.stagedRef);
    assert.ok(committedRef.startsWith("artifact:"));
    assert.equal(store.readHtml(committedRef), html);
    assert.equal(store.readHtml(staged.stagedRef), null); // moved, not copied
  });
});

test("M0b: discard drops a staged candidate with no trace", () => {
  withStore((store) => {
    const staged = store.stageHtml(`<p>draft</p>`);
    store.discardStagedHtml(staged.stagedRef);
    assert.equal(store.readHtml(staged.stagedRef), null);
  });
});

test("M0b: commit of an unknown/discarded staged ref throws NO_STAGED_CANDIDATE", () => {
  withStore((store) => {
    assert.throws(() => store.commitHtml("staged:deadbeef"), /NO_STAGED_CANDIDATE/);
  });
});
