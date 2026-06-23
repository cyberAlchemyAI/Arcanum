// UX Evidence Validator — runnable test for skill-anatomy.html (+ embedded refine x-ray)
// Spec: ./VALIDATION-SPEC.md   Evidence: arcanum/output/playwright/ux-validator/<run-id>/
// Env: BASE_URL (default http://localhost:8754), OUT (evidence dir), PW (playwright index.js path)
import { mkdirSync, writeFileSync } from 'node:fs';

const BASE = process.env.BASE_URL || 'http://localhost:8754';
const URL = BASE.replace(/\/$/, '') + '/skill-anatomy.html';
const OUT = process.env.OUT || '/tmp/ux-validator-run';
const PW = process.env.PW || '/home/vrondelli/.npm/_npx/9833c18b2d85bc59/node_modules/playwright/index.js';
const _pw = await import(PW); const { chromium } = _pw.default ?? _pw;

mkdirSync(OUT + '/screenshots', { recursive: true });
mkdirSync(OUT + '/measurements', { recursive: true });

const findings = [];
const add = (f) => findings.push(f);
const VIEWPORTS = [
  { name: 'desktop', width: 1280, height: 900, isMobile: false },
  { name: 'mobile', width: 390, height: 844, isMobile: true },
];

// --- in-browser measurement helpers (serialized into page/frame.evaluate) ---
function measureCardsInDoc() {
  // runs inside the x-ray document/frame
  // NOTE: the Stacked deck applies a 3-D transform (perspective + rotate) to .deck-inner,
  // which makes getBoundingClientRect return PROJECTED geometry. To read TRUE layout we
  // temporarily neutralise the transform and lay the planes out at natural size, measure,
  // then restore. (This runs after the screenshot, so the visual capture is untouched.)
  // Count rendered TEXT lines via a Range (element.getClientRects() on a block div is always 1 rect).
  const textLineCount = (el) => {
    if (!el) return 0;
    const r = document.createRange(); r.selectNodeContents(el);
    const pill = el.querySelector('.drill-pill'); // exclude the interactive affordance from title line count
    if (pill) r.setEndBefore(pill);
    const tops = new Set([...r.getClientRects()].filter((x) => x.width > 0).map((x) => Math.round(x.top)));
    return tops.size || 1;
  };
  const deckEl = document.querySelector('.deck');
  const deckInner = document.querySelector('.deck-inner');
  const planes = [...document.querySelectorAll('.plane')];
  const srows = [...document.querySelectorAll('.srow')];

  // Remove ONLY the 3-D transform/perspective (it distorts getBoundingClientRect).
  // Keep .plane absolute so each card keeps its true rendered width (left:34px; right:2%).
  const saved = [];
  const stash = (el) => { if (el) saved.push([el, el.getAttribute('style') || '']); };
  stash(deckEl); stash(deckInner);
  if (deckEl) { deckEl.style.perspective = 'none'; }
  if (deckInner) { deckInner.style.transform = 'none'; }
  void document.body.offsetHeight; // force reflow

  const overflow = document.documentElement.scrollWidth - document.documentElement.clientWidth;
  const deck = planes.map((p, i) => {
    const pt = p.querySelector('.pt'); const pb = p.querySelector('.pb');
    const ptr = pt ? pt.getBoundingClientRect() : null;
    const pbr = pb ? pb.getBoundingClientRect() : null;
    // does the title TEXT (first line) run horizontally under the badge?
    let collide = false, firstLineRight = 0, badgeLeft = 0;
    if (pt && pb) {
      const r = document.createRange(); r.selectNodeContents(pt);
      const rects = [...r.getClientRects()].filter((x) => x.width > 0);
      const firstLine = rects[0];
      if (firstLine && pbr) {
        firstLineRight = Math.round(firstLine.right); badgeLeft = Math.round(pbr.left);
        collide = firstLine.right > pbr.left + 1 && firstLine.top < pbr.bottom && firstLine.bottom > pbr.top;
      }
    }
    return {
      i: i + 1,
      title: pt ? pt.textContent.trim().slice(0, 40) : null,
      lines: textLineCount(pt),
      cardWidth: Math.round(p.getBoundingClientRect().width),
      firstLineRight, badgeLeft,
      fontPx: pt ? parseFloat(getComputedStyle(pt).fontSize) : 0,
      badgeCollision: collide,
    };
  });
  saved.forEach(([el, s]) => el.setAttribute('style', s)); // restore
  const strata = srows.map((rw, i) => {
    const pt = rw.querySelector('.pt');
    return {
      i: i + 1,
      title: pt ? pt.textContent.trim().slice(0, 40) : null,
      lines: textLineCount(pt),
      clipped: pt ? pt.scrollWidth > pt.clientWidth + 1 : false,
      fontPx: pt ? parseFloat(getComputedStyle(pt).fontSize) : 0,
    };
  });
  return { overflow, deck, strata };
}

function measureTapTargets() {
  const sel = '.seg button, .layer-toggles input, .tour-start, .tb-ctrls button, .trace button, button, a';
  const small = [];
  document.querySelectorAll(sel).forEach((el) => {
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) return; // hidden
    const min = Math.min(r.width, r.height);
    if (min < 24) small.push({ tag: el.tagName.toLowerCase(), label: (el.textContent || el.value || el.getAttribute('aria-label') || '').trim().slice(0, 24), w: Math.round(r.width), h: Math.round(r.height) });
  });
  return small;
}

function pageLayout() {
  const overflow = document.documentElement.scrollWidth - window.innerWidth;
  const grids = [...document.querySelectorAll('.grid-3, .grid-2')].map((g) => ({
    cls: g.className,
    cols: getComputedStyle(g).gridTemplateColumns.split(' ').filter(Boolean).length,
  }));
  return { overflow, grids, innerWidth: window.innerWidth };
}

// ---------------------------------------------------------------------------
const browser = await chromium.launch();
const consoleErrors = [];

for (const vp of VIEWPORTS) {
  const ctx = await browser.newContext({ viewport: { width: vp.width, height: vp.height }, isMobile: vp.isMobile, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  page.on('console', (m) => { if (m.type() === 'error') consoleErrors.push(`[${vp.name}] ${m.text()}`); });
  page.on('pageerror', (e) => consoleErrors.push(`[${vp.name}] PAGEERR ${e.message}`));
  await page.goto(URL, { waitUntil: 'networkidle' });

  // L0
  add({ id: 'L0.page-load', viewport: vp.name, claim: 'browser-observable', severity: 'hard_gate', status: (await page.title()) === 'Anatomy of a Skill — CyberAlchemy' ? 'pass' : 'fail', detail: await page.title() });
  const frame = page.frames().find((f) => f.url().includes('refine-skill-xray'));
  add({ id: 'L0.iframe-loaded', viewport: vp.name, claim: 'browser-observable', severity: 'hard_gate', status: frame ? 'pass' : 'fail', detail: frame ? frame.url() : 'iframe frame not found' });

  // L1 page
  const pl = await page.evaluate(pageLayout);
  add({ id: 'L1.no-horizontal-overflow', viewport: vp.name, claim: 'browser-observable', severity: 'hard_gate', status: pl.overflow <= 1 ? 'pass' : 'fail', detail: `overflow ${pl.overflow}px (inner ${pl.innerWidth})` });
  if (vp.isMobile) {
    const bad = pl.grids.filter((g) => g.cols > 1);
    add({ id: 'L1.grid-collapses-mobile', viewport: vp.name, claim: 'browser-observable', severity: 'hard_gate', status: bad.length === 0 ? 'pass' : 'fail', detail: bad.length ? `grids not collapsed: ${JSON.stringify(bad)}` : `all ${pl.grids.length} grids single-column` });
  }

  // L2 nav toggle (mobile)
  if (vp.isMobile) {
    const navHidden = await page.$eval('#primary-nav', (e) => getComputedStyle(e).display === 'none');
    await page.click('.nav-toggle');
    await page.waitForTimeout(200);
    const navShown = await page.$eval('#primary-nav', (e) => getComputedStyle(e).display !== 'none');
    const aria = await page.$eval('.nav-toggle', (e) => e.getAttribute('aria-expanded'));
    add({ id: 'L2.nav-toggle-mobile', viewport: vp.name, claim: 'browser-observable', severity: 'hard_gate', status: navHidden && navShown && aria === 'true' ? 'pass' : 'fail', detail: `hiddenInit=${navHidden} shownAfter=${navShown} aria=${aria}` });
    await page.click('.nav-toggle'); await page.waitForTimeout(100);
  }

  // page screenshot
  await page.screenshot({ path: `${OUT}/screenshots/${vp.name}-page.png` });

  // ---- enter the x-ray iframe ----
  if (frame) {
    // iframe internal overflow
    const fl = await frame.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
    add({ id: 'L1.iframe-no-overflow', viewport: vp.name, claim: 'browser-observable', severity: 'hard_gate', status: fl <= 1 ? 'pass' : 'fail', detail: `x-ray overflow ${fl}px` });

    for (const view of ['Stacked deck', 'Strata']) {
      const btn = frame.locator('.seg button', { hasText: view.split(' ')[0] }).first();
      if (await btn.count()) { await btn.click(); await frame.page().waitForTimeout(350); }
      // screenshot the x-ray region FIRST (before any measurement mutation)
      await page.locator('iframe').scrollIntoViewIfNeeded();
      await page.waitForTimeout(150);
      await page.screenshot({ path: `${OUT}/screenshots/${vp.name}-xray-${view.split(' ')[0].toLowerCase()}.png` });
      const m = await frame.evaluate(measureCardsInDoc);
      writeFileSync(`${OUT}/measurements/${vp.name}-${view.replace(/\W+/g, '-').toLowerCase()}.json`, JSON.stringify(m, null, 2));

      if (view === 'Stacked deck') {
        const overLines = m.deck.filter((c) => c.lines > 2); // ≤2 lines is acceptable in the lip; >2 gets clipped
        const collided = m.deck.filter((c) => c.badgeCollision);
        add({ id: 'L1.card-title-max-2-lines', viewport: vp.name, claim: 'browser-observable', severity: 'hard_gate', status: overLines.length === 0 ? 'pass' : 'fail', detail: overLines.length ? `${overLines.length}/${m.deck.length} titles exceed 2 lines: ${overLines.map((c) => c.i + '·' + c.title).join(', ')}` : `all ${m.deck.length} titles ≤2 lines (${m.deck.filter((c) => c.lines === 2).length} wrap to 2)` });
        add({ id: 'L1.card-title-badge-clearance', viewport: vp.name, claim: 'browser-observable', severity: 'hard_gate', status: collided.length === 0 ? 'pass' : 'fail', detail: collided.length ? `${collided.length}/${m.deck.length} titles collide with badge: ${collided.map((c) => c.i + '·' + c.title).join(', ')}` : 'no title/badge collisions' });
        const smallFont = m.deck.filter((c) => c.fontPx && c.fontPx < 12);
        add({ id: 'L3.text-legibility', viewport: vp.name, claim: 'standards-backed', severity: 'soft_flag', status: smallFont.length === 0 ? 'pass' : 'warn', detail: smallFont.length ? `${smallFont.length} titles < 12px` : `deck title font ${m.deck[0]?.fontPx}px` });
      } else {
        const clipped = m.strata.filter((c) => c.clipped);
        add({ id: 'L1.strata-title-no-clip', viewport: vp.name, claim: 'browser-observable', severity: 'hard_gate', status: clipped.length === 0 ? 'pass' : 'fail', detail: clipped.length ? `${clipped.length} strata titles clipped` : `all ${m.strata.length} strata titles fit` });
      }
    }
    add({ id: 'L2.view-toggle', viewport: vp.name, claim: 'browser-observable', severity: 'hard_gate', status: (await frame.locator('.seg button').count()) >= 2 ? 'pass' : 'fail', detail: `${await frame.locator('.seg button').count()} view buttons` });

    // L3 tap targets (advisory)
    const small = await frame.evaluate(measureTapTargets);
    add({ id: 'L3.tap-targets', viewport: vp.name, claim: 'standards-backed', severity: 'soft_flag', status: small.length === 0 ? 'pass' : 'warn', detail: small.length ? `${small.length} controls < 24×24 (WCAG 2.5.8): ${small.slice(0, 6).map((s) => `${s.label || s.tag}(${s.w}×${s.h})`).join(', ')}${small.length > 6 ? '…' : ''}` : 'all controls ≥ 24×24' });
  }
  await ctx.close();
}

add({ id: 'L0.no-console-errors', viewport: 'all', claim: 'browser-observable', severity: 'hard_gate', status: consoleErrors.length === 0 ? 'pass' : 'fail', detail: consoleErrors.length ? consoleErrors.join(' | ') : 'no console/page errors' });
await browser.close();

// ---- verdict + evidence bundle ----
const hardFails = findings.filter((f) => f.severity === 'hard_gate' && f.status === 'fail');
const softWarns = findings.filter((f) => f.severity === 'soft_flag' && f.status === 'warn');
const verdict = hardFails.length ? 'block' : softWarns.length ? 'flag' : 'pass';

writeFileSync(`${OUT}/findings.json`, JSON.stringify({ verdict, hard_fail: hardFails.length, soft_flag: softWarns.length, findings }, null, 2));
writeFileSync(`${OUT}/run-metadata.json`, JSON.stringify({ target: URL, viewports: VIEWPORTS, mode: 'validate-interface', sigil: 'ux-evidence-validator', spec: 'VALIDATION-SPEC.md' }, null, 2));
writeFileSync(`${OUT}/console-network.json`, JSON.stringify({ consoleErrors }, null, 2));
writeFileSync(`${OUT}/residue-ledger.yml`, [
  'residue:',
  '  - claim: "cards behave well / aesthetic balance"', '    class: human-study', '    status: not-automatable',
  '  - claim: "deck vs strata comprehension speed"', '    class: human-study', '    status: requires-user-test',
  '  - claim: "color contrast (axe not run)"', '    class: standards-backed', '    status: not-run',
  '',
].join('\n'));

const rows = findings.map((f) => `| ${f.id} | ${f.viewport} | ${f.severity} | ${f.status.toUpperCase()} | ${f.detail} |`).join('\n');
writeFileSync(`${OUT}/summary.md`, `# UX Validation — skill-anatomy.html

- Verdict: **${verdict.toUpperCase()}**  ·  hard-gate fails: ${hardFails.length}  ·  soft flags: ${softWarns.length}
- Target: ${URL}
- Viewports: desktop 1280×900, mobile 390×844

| check | viewport | severity | status | detail |
| --- | --- | --- | --- | --- |
${rows}
`);

console.log(JSON.stringify({ verdict, hardFails: hardFails.length, softWarns: softWarns.length, out: OUT }, null, 2));
