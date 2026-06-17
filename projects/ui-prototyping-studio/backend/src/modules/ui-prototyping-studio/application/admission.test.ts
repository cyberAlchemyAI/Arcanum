import assert from "node:assert/strict";
import { test } from "node:test";

import { admitScope } from "./admission.js";

// TaskScope: cta.primary (A) + card.hint (B) in-scope; card.title (X), card.footer (Z) out-of-scope.
const SCOPE = ["cta.primary", "card.hint"];
const BASE = `<div class="wrap"><div class="card" data-od-id="card.root">
  <h2 class="title" data-od-id="card.title">Hello</h2>
  <button class="cta" data-od-id="cta.primary" aria-label="go">Go</button>
  <span class="hint" data-od-id="card.hint">hint</span>
  <footer class="ft" data-od-id="card.footer">f</footer>
</div></div><style>.cta{padding:8px} .title{font-size:14px}</style>`;

// GOOD — in-scope edits → NOT_REJECT
test("M1 GOOD-1: in-scope text edit on A", () => {
  const c = BASE.replace(">Go<", ">Continue<");
  assert.equal(admitScope(BASE, c, SCOPE), "NOT_REJECT");
});
test("M1 GOOD-2: in-scope CSS rule (.cta resolves only to A)", () => {
  const c = BASE.replace(".cta{padding:8px}", ".cta{padding:16px}");
  assert.equal(admitScope(BASE, c, SCOPE), "NOT_REJECT");
});
test("M1 GOOD-3: in-scope attr edit on B (card.hint)", () => {
  const c = BASE.replace('data-od-id="card.hint">hint', 'data-od-id="card.hint" title="t">hint');
  assert.equal(admitScope(BASE, c, SCOPE), "NOT_REJECT");
});

// BAD — out-of-scope / forge → REJECT
test("M1 BAD-1: out-of-scope text edit on X (card.title)", () => {
  const c = BASE.replace(">Hello<", ">Hi there<");
  assert.equal(admitScope(BASE, c, SCOPE), "REJECT");
});
test("M1 BAD-2: CSS rule spanning out-of-scope (.title resolves to X)", () => {
  const c = BASE.replace(".title{font-size:14px}", ".title{font-size:20px}");
  assert.equal(admitScope(BASE, c, SCOPE), "REJECT");
});
test("M1 BAD-3 forge: assert cta.primary on the title node", () => {
  const c = BASE.replace('class="title" data-od-id="card.title"', 'class="title" data-od-id="cta.primary"');
  assert.equal(admitScope(BASE, c, SCOPE), "REJECT");
});

// HELD-OUT
test("M1 HELD-8: out-of-scope node deletion (remove footer Z)", () => {
  const c = BASE.replace('<footer class="ft" data-od-id="card.footer">f</footer>', "");
  assert.equal(admitScope(BASE, c, SCOPE), "REJECT");
});
test("M1 HELD-2: un-anchored out-of-scope edit (wrapper class) → REJECT", () => {
  const c = BASE.replace('class="wrap"', 'class="wrap changed"');
  assert.equal(admitScope(BASE, c, SCOPE), "REJECT");
});

// discrimination: identity (no change) admits; always-reject would fail this
test("M1 identity: no change → NOT_REJECT", () => {
  assert.equal(admitScope(BASE, BASE, SCOPE), "NOT_REJECT");
});
