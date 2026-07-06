import { defineConfig } from "@playwright/test";

// e2e for the closed loop over the `studio preview` loopback server + the CLI seam.
// No webServer: each spec launches `studio preview` itself on an ephemeral port with an
// isolated STUDIO_DATA dir (per-run isolation — the README rule). Serial (shared CLI binary).
export default defineConfig({
  testDir: "e2e",
  fullyParallel: false,
  workers: 1,
  timeout: 60_000,
  reporter: [["list"]],
  use: { headless: true },
  projects: [{ name: "chromium", use: { browserName: "chromium" } }],
});
