import { test, expect } from "@playwright/test";

import { cli, newDataDir, seedBaseline } from "./helpers";

test("auto: exploit picks the top self-critique score and advances head", () => {
  const dir = newDataDir();
  const sid = seedBaseline(dir);
  const cy = cli(
    ["cycle", sid, "exploit", "--objective", "make the cta clearer",
      "--candidate", "e2e/fixtures/continue.html:0.9",
      "--candidate", "e2e/fixtures/next.html:0.4"],
    dir,
  );
  expect(cy.json.staged).toBe(2);
  expect(cy.json.rejected).toBe(0);
  expect(cy.json.chosen.score).toBe(0.9);
  expect(cy.json.session.revisionHeadId).toBe(cy.json.chosen.revisionId);
});

test("auto: exploit REJECTS a structural divergence; explore ADMITS it", () => {
  const dirX = newDataDir();
  const sidX = seedBaseline(dirX);
  const ex = cli(["cycle", sidX, "exploit", "--objective", "tighten", "--candidate", "e2e/fixtures/badge.html:0.8"], dirX);
  expect(ex.json.rejected).toBe(1);
  expect(ex.json.chosen).toBeNull();

  const dirE = newDataDir();
  const sidE = seedBaseline(dirE);
  const exp = cli(["cycle", sidE, "explore", "--objective", "try a badge", "--candidate", "e2e/fixtures/badge.html:0.8"], dirE);
  expect(exp.json.rejected).toBe(0);
  expect(exp.json.chosen).not.toBeNull();
});

test("auto: an empty objective is refused (start gate)", () => {
  const dir = newDataDir();
  const sid = seedBaseline(dir);
  const r = cli(["cycle", sid, "exploit", "--candidate", "e2e/fixtures/continue.html:0.9"], dir);
  expect(r.code).not.toBe(0);
  expect(r.stdout).toContain("AUTO_OBJECTIVE_REQUIRED");
});
