import { test, expect } from "@playwright/test";

import { newDataDir, seedBaseline, startPreview } from "./helpers";

test("smoke: preview page mounts; variant iframe + /state resolve", async ({ page, request }) => {
  const dir = newDataDir();
  const sid = seedBaseline(dir);
  const pv = await startPreview(sid, dir);
  try {
    await page.goto(pv.url);
    await expect(page.locator("header")).toContainText(sid);

    const variant = await request.get(`http://127.0.0.1:${pv.port}/raw/variant/A`);
    expect(variant.ok()).toBeTruthy();
    expect(await variant.text()).toContain("data-od-id");

    const state = await (await request.get(`http://127.0.0.1:${pv.port}/state`)).json();
    expect(state).toHaveProperty("state");
    expect(state).toHaveProperty("head");
  } finally {
    pv.stop();
  }
});
