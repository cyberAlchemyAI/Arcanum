import assert from "node:assert/strict";
import { test } from "node:test";

import {
  canonicalHash,
  canonicalizeHtml,
  parseHtml,
} from "./canonicalize.js";

test("M0c: canonicalization is idempotent", () => {
  const html = `<div class="card"  data-od-id="cta.primary" >
     <button   class='cta'>Go</button>
  </div>`;
  const once = canonicalizeHtml(html);
  const twice = canonicalizeHtml(once);
  assert.equal(once, twice);
});

test("M0c: attribute order is normalized (sorted)", () => {
  const a = canonicalizeHtml(`<button data-od-id="x" class="cta" aria-label="go">Go</button>`);
  const b = canonicalizeHtml(`<button class="cta" aria-label="go" data-od-id="x">Go</button>`);
  assert.equal(a, b);
  assert.match(a, /aria-label="go" class="cta" data-od-id="x"/);
});

test("M0c: whitespace is collapsed", () => {
  const a = canonicalizeHtml(`<p>hello     world</p>`);
  const b = canonicalizeHtml(`<p>hello world</p>`);
  assert.equal(a, b);
});

test("M0c: data-od-id is preserved", () => {
  const tree = parseHtml(`<button data-od-id="cta.primary">Go</button>`);
  const el = tree[0];
  assert.ok(el && el.type === "element");
  assert.equal(el.attrs.get("data-od-id"), "cta.primary");
});

test("M0c: void elements and style raw text handled", () => {
  const out = canonicalizeHtml(`<img src="a.png"><style> .cta { padding: 8px } </style>`);
  assert.match(out, /<img src="a.png">/);
  assert.match(out, /<style>\.cta \{ padding: 8px \}<\/style>/);
});

test("M0c: hash is stable across equivalent inputs", () => {
  const h1 = canonicalHash(`<div  class="x"><span>hi</span></div>`);
  const h2 = canonicalHash(`<div class="x">\n  <span>hi</span>\n</div>`);
  assert.equal(h1, h2);
});
