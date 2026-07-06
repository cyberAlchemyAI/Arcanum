import { test, expect } from "@playwright/test";

import { cli, newDataDir, seedBaseline, startPreview } from "./helpers";

// CL1: click a component in the trusted annotate wrapper → postMessage → parent comment form →
// POST /comment → the write reaches the core (studio pending shows it).
test("human loop: annotate click → comment form → POST /comment → pending=1", async ({ page }) => {
  const dir = newDataDir();
  const sid = seedBaseline(dir);
  const pv = await startPreview(sid, dir);
  try {
    await page.goto(pv.url);

    // click the CTA inside the sandboxed-but-script-allowed annotate frame
    const frame = page.frameLocator("#annot");
    await frame.locator("[data-od-id=cta\\.primary]").click();

    // the trusted click→postMessage opened the parent comment form, prefilled with the od-id
    await expect(page.locator("#cf")).toBeVisible();
    await expect(page.locator("#cf-od")).toHaveText("cta.primary");

    await page.fill("#cf input[name=intent]", "reword");
    await page.fill("#cf input[name=note]", "say Continue");
    await page.click("#cf button[type=submit]");
    await expect(page.locator("#cf-msg")).toContainText("captured");

    // the browser→studio write landed in the core
    const pending = cli(["pending", sid], dir);
    expect(pending.json.length).toBe(1);
    expect(pending.json[0].target.odId).toBe("cta.primary");
  } finally {
    pv.stop();
  }
});
