import assert from "node:assert/strict";
import { test } from "node:test";

import Fastify from "fastify";

import { registerUiPrototypingStudioRoutes } from "./http-routes.js";

// N1/N2 (F1): the export confirm gate lives in the CORE use-case, so the HTTP adapter inherits it.
// Proves the previously-open HTTP door now refuses without confirmation.
const WRITE = { "x-scopes": "domainspec.ui-prototyping.write" };

async function app() {
  const f = Fastify();
  registerUiPrototypingStudioRoutes(f, { useInMemoryStore: true });
  await f.ready();
  return f;
}

test("HTTP export WITHOUT confirm is refused (gate-in-core closes F1 on the network door)", async () => {
  const f = await app();
  try {
    const res = await f.inject({
      method: "POST",
      url: "/api/ui-prototyping-studio/sessions/ups-session-0001/handoff/export",
      headers: WRITE,
      payload: {},
    });
    assert.ok(res.statusCode >= 400, `expected refusal, got ${res.statusCode}`);
    assert.match(res.body, /HANDOFF_CONFIRMATION_REQUIRED/);
  } finally {
    await f.close();
  }
});

test("HTTP export WITH confirm passes the gate (then fails later on the missing session, not on confirm)", async () => {
  const f = await app();
  try {
    const res = await f.inject({
      method: "POST",
      url: "/api/ui-prototyping-studio/sessions/ups-session-0001/handoff/export",
      headers: WRITE,
      payload: { confirm: "human:op" },
    });
    // confirm gate passed → we reach the session check; never a confirmation error with confirm present
    assert.doesNotMatch(res.body, /HANDOFF_CONFIRMATION_REQUIRED/);
    assert.match(res.body, /SESSION_NOT_FOUND/);
  } finally {
    await f.close();
  }
});
