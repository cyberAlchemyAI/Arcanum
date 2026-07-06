import { test, expect } from "@playwright/test";

import { newDataDir, seedBaseline, seedStaged, startPreview } from "./helpers";

/**
 * BLIND — black-box naive-user contract:
 *   - the TEST BODY touches ONLY the rendered preview UI; it asserts ONLY on what a cold-start human SEES.
 *   - NO CLI in the body, NO internal JSON / hash / file / revision-count reads (that is the white-box
 *     suite's job — see governance/smoke/human-loop/auto specs).
 *   - CLI appears ONLY inside clearly-marked scaffolding helpers (seedBaseline/seedStaged/startPreview) to
 *     reach the screen the user is handed. That the studio has NO browser onboarding — a blind user cannot
 *     even start without a terminal — is itself the first ergonomic finding, recorded here, not asserted.
 */

test("blind: a cold-start user is ORIENTED by the page (plain-language next step), not left guessing", async ({ page }) => {
  const dir = newDataDir();
  const sid = seedBaseline(dir); // scaffolding → the BaselineReady screen
  const pv = await startPreview(sid, dir);
  try {
    await page.goto(pv.url);
    // the page itself tells a first-time user what just happened and what to do next
    await expect(page.locator("header")).toContainText("Baseline chosen");
    await expect(page.locator("header")).toContainText(/comment on a component/i);
  } finally {
    pv.stop();
  }
});

test("blind: the one action a naive user can complete is annotate→comment, and it confirms visibly", async ({ page }) => {
  const dir = newDataDir();
  const sid = seedBaseline(dir);
  const pv = await startPreview(sid, dir);
  try {
    await page.goto(pv.url);
    // they can SEE a variant rendered (read the button text through the frame)
    await expect(page.frameLocator('iframe[src="/raw/variant/A"]').locator('[data-od-id="cta.primary"]')).toHaveText("Go");

    // the only durable-loop-adjacent thing the browser lets them do: point at a component and comment
    await page.frameLocator("#annot").locator('[data-od-id="cta.primary"]').click();
    await expect(page.locator("#cf")).toBeVisible();
    await expect(page.locator("#cf-od")).toHaveText("cta.primary");
    await page.fill("#cf input[name=intent]", "reword");
    await page.fill("#cf input[name=note]", "say Continue");
    await page.click("#cf button[type=submit]");

    // the UI closes the loop on their action — no silent success (an ergonomic must)
    await expect(page.locator("#cf-msg")).toContainText("captured");
  } finally {
    pv.stop();
  }
});

test("blind: on a staged change the user SEES the real before/after — not a hash they must trust", async ({ page }) => {
  const dir = newDataDir();
  const sid = seedStaged(dir); // scaffolding → the RevisionApplied (staged) screen
  const pv = await startPreview(sid, dir);
  try {
    await page.goto(pv.url);
    await expect(page.getByText(/review before you accept/i)).toBeVisible();
    // the user reads the ACTUAL change in the rendered panels: "Go" → "Continue"
    await expect(page.frameLocator('iframe[src="/raw/baseline"]').locator('[data-od-id="cta.primary"]')).toHaveText("Go");
    await expect(page.frameLocator('iframe[src="/raw/staged"]').locator('[data-od-id="cta.primary"]')).toHaveText("Continue");
    // and a human-readable diff summary, not just a number
    await expect(page.locator(".pending")).toContainText(/changed/i);
  } finally {
    pv.stop();
  }
});

test("blind: the loop is now completable in-browser; EXPORT stays the one button-less terminal edge (N3)", async ({ page }) => {
  const dir = newDataDir();
  const sid = seedStaged(dir);
  const pv = await startPreview(sid, dir);
  try {
    await page.goto(pv.url);
    // N3 flipped the old dead-end: reversible verbs now have in-browser controls…
    await expect(page.getByRole("button", { name: /accept/i })).toHaveCount(1);
    await expect(page.getByRole("button", { name: /discard/i })).toHaveCount(1);
    // …but EXPORT (the one irreversible edge) has NO button — it stays terminal + --confirm by design.
    await expect(page.getByRole("button", { name: /export/i })).toHaveCount(0);
    await expect(page.locator(".pending")).toContainText("handoff export");
    await expect(page.locator(".pending")).toContainText("--confirm");
  } finally {
    pv.stop();
  }
});
