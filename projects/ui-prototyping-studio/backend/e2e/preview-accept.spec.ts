import { test, expect } from "@playwright/test";

import { cli, newDataDir, seedStaged, startPreview } from "./helpers";

// N3: the closed loop completes IN the browser — click Accept on a staged change → head advances; then
// Revert on the recorded head → it walks back. Export is NOT a button (stays terminal --confirm).
test("N3: in-preview Accept advances head; Revert walks it back — no terminal needed", async ({ page, request }) => {
  const dir = newDataDir();
  const sid = seedStaged(dir); // a candidate is staged, head still rev-0000
  const pv = await startPreview(sid, dir);
  try {
    await page.goto(pv.url);

    const before = await (await request.get(`http://127.0.0.1:${pv.port}/state`)).json();
    expect(before.head).toBe("rev-0000"); // staged, not yet accepted

    await page.getByRole("button", { name: /accept/i }).click();
    await expect.poll(async () => (await (await request.get(`http://127.0.0.1:${pv.port}/state`)).json()).head)
      .not.toBe("rev-0000"); // head advanced via the browser Accept

    // the recorded state now offers an in-browser Revert
    await expect(page.getByRole("button", { name: /revert/i })).toHaveCount(1);
    const accepted = await (await request.get(`http://127.0.0.1:${pv.port}/state`)).json();
    await page.getByRole("button", { name: /revert/i }).click();
    await expect.poll(async () => (await (await request.get(`http://127.0.0.1:${pv.port}/state`)).json()).head)
      .not.toBe(accepted.head); // revert appended a new head (append-only walk-back)

    // append-only: two events recorded (accept + revert) — verified via the CLI read
    expect(cli(["revisions", sid], dir).json.length).toBe(2);
  } finally {
    pv.stop();
  }
});
