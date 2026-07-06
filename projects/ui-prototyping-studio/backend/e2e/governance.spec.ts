import { test, expect } from "@playwright/test";
import { readFileSync } from "node:fs";

import { cli, newDataDir, seedBaseline } from "./helpers";

// The load-bearing governance suite (CLI seam — no browser). Each test FAILS if the
// reversibility guarantee breaks (see refinement-runs/.../stages/08-toygame.md).

function seedWithRevision(dir: string): { sid: string; cycle: ReturnType<typeof cli> } {
  const sid = seedBaseline(dir);
  const cycle = cli(["cycle", sid, "exploit", "--objective", "make the cta clearer", "--candidate", "e2e/fixtures/continue.html:0.9"], dir);
  return { sid, cycle };
}

test("governance: handoff export without --confirm is refused (exit 3); --confirm exports", () => {
  const dir = newDataDir();
  const { sid } = seedWithRevision(dir);

  const refused = cli(["handoff", "export", sid], dir);
  expect(refused.code).toBe(3);
  expect(refused.json?.refused).toBe("HANDOFF_CONFIRMATION_REQUIRED");

  const confirmed = cli(["handoff", "export", sid, "--confirm"], dir);
  expect(confirmed.code).toBe(0);
  expect(confirmed.json?.bundle?.revisionHeadId).toBeTruthy();
});

test("governance: revert restores the pre-accept baseline html", () => {
  const dir = newDataDir();
  const { sid, cycle } = seedWithRevision(dir);

  const headHtml = readFileSync(cycle.json.openPath, "utf8");
  expect(headHtml).toContain("Continue"); // the cycle auto-accepted "Continue"

  const rv = cli(["revert", sid], dir);
  const restored = readFileSync(rv.json.openPath, "utf8");
  expect(restored).toContain("Go");
  expect(restored).not.toContain("Continue");
});

test("governance: an auto-accept is revertible and append-only (log grows, never rewinds)", () => {
  const dir = newDataDir();
  const { sid } = seedWithRevision(dir);

  expect(cli(["revisions", sid], dir).json.length).toBe(1);
  cli(["revert", sid], dir);
  expect(cli(["revisions", sid], dir).json.length).toBe(2); // appended, not rewound
});
