async (page) => {
  const url = "http://127.0.0.1:4177/CRAFT-CAUSAL-CLASS-PRESENTATION.html";
  const results = [];
  const consoleErrors = [];
  const thirdPartyConsoleErrors = [];
  page.on("console", message => {
    if (message.type() !== "error") return;
    const source = message.location().url || "";
    if (source.includes("mentimeter.com")) thirdPartyConsoleErrors.push(message.text());
    else consoleErrors.push(message.text());
  });

  const assert = (condition, message) => {
    if (!condition) throw new Error(message);
    results.push(message);
  };

  await page.setViewportSize({width: 1280, height: 720});
  await page.goto(url);
  assert((await page.locator("section.active h1").textContent()).trim() === "Before We Build", "Opening title is audience-facing");
  assert((await page.locator("section.active .prompt").textContent()).trim() === "Which one would you choose for one afternoon with basic tools?", "Mentimeter vote precedes the design explanation");
  assert(await page.locator("section.active .visible-list li").count() === 0, "Opening withholds clues");
  assert(await page.locator("section.active iframe[title^='Mentimeter poll']").count() === 1, "Opening state embeds the Mentimeter poll");
  assert((await page.locator("section.active iframe").getAttribute("sandbox")).includes("allow-scripts"), "Poll iframe keeps the supplied sandbox contract");
  assert((await page.locator("section.active [data-reveal-index]").textContent()).includes("Keep the vote"), "Poll has an explicit transition into the table story");
  await page.waitForTimeout(800);
  assert(page.frames().some(frame => frame.url().includes("mentimeter.com/app/presentation")), "Mentimeter frame loads before the profiles appear");
  assert(await page.locator(".eyebrow, .consequence, .chapter").count() === 0, "Authoring metadata has no projected selectors");
  await page.locator("section.active .scene").focus();
  await page.keyboard.press("Space");
  assert((await page.locator("#counter").textContent()).trim() === "1 / 14", "Space reveal stays on slide 1");
  assert((await page.locator("section.active .scene").getAttribute("aria-label")).includes("state 2 of 4"), "Poll advances exactly once into the plain-table pause");
  assert(await page.locator("section.active iframe").count() === 0, "Poll unmounts before the table explanation begins");
  assert((await page.locator("section.active .prompt").textContent()).trim() === "What would you need to build this?", "Plain-table question follows the blind vote");
  assert((await page.locator("section.active [data-reveal-index]").textContent()).includes("Show clues"), "Table pause still withholds clues");
  await page.keyboard.press("Space");
  assert((await page.locator("section.active .visible-list").textContent()).includes("materials"), "Next reveal shows build-needs buckets");
  assert((await page.locator("section.active [data-reveal-index]").textContent()).includes("Make it concrete"), "Following reveal promises concrete choices");
  await page.keyboard.press("Space");
  assert((await page.locator("section.active .visible-list").textContent()).includes("100 x 50 x 72 cm"), "Final opening reveal shows concrete dimensions");
  await page.keyboard.press("Space");
  assert((await page.locator("section.active .scene").getAttribute("aria-label")).includes("state 4 of 4"), "Terminal Space does not reset");
  assert((await page.locator("#counter").textContent()).trim() === "1 / 14", "Terminal Space does not navigate");
  await page.keyboard.press("ArrowRight");
  assert((await page.locator("#counter").textContent()).trim() === "2 / 14", "Focused ArrowRight advances after terminal state");
  assert(await page.locator("section.active iframe").count() === 0, "Design explanation does not repeat the poll");
  assert(await page.locator("section.active .desk-profile").count() === 2, "Design explanation shows both front profiles after voting");
  assert((await page.locator("section.active [data-reveal-index]").textContent()).includes("Carry our choice forward"), "Profile comparison carries the prior vote into the causal history");
  await page.keyboard.press("ArrowLeft");
  assert((await page.locator("#counter").textContent()).trim() === "1 / 14", "Focused ArrowLeft returns to previous terminal state");

  await page.locator("#notes-toggle").click();
  assert(await page.locator("#notes-toggle").getAttribute("aria-pressed") === "true", "Notes toggle exposes open state");
  assert(await page.locator("#notes-overlay").evaluate(node => node.classList.contains("open")), "Notes open in overlay");
  await page.keyboard.press("Escape");
  assert(await page.locator("#notes-toggle").getAttribute("aria-pressed") === "false", "Escape closes notes and updates state");

  await page.goto(`${url}#CRAFT-CAUSAL-S08`);
  assert((await page.locator("#counter").textContent()).trim() === "8 / 14", "Hash navigation opens the requested slide");
  await page.locator("section.active [data-reveal-index]").click();
  const terminalLabel = await page.locator("section.active .scene").getAttribute("aria-label");
  await page.locator("section.active .scene").click({position: {x: 10, y: 10}});
  assert(await page.locator("section.active .scene").getAttribute("aria-label") === terminalLabel, "Pointer activation cannot reset a terminal state");

  const slideIds = await page.evaluate(() => deckData.slides.map(slide => slide.id));
  const metadataLeaks = await page.evaluate(() => {
    return deckData.slides.flatMap((slide, slideIndex) => {
      const projected = document.querySelectorAll("section")[slideIndex]?.querySelector(".narrative")?.textContent || "";
      const values = [slide.story_state, ...slide.states.flatMap(state => [state.consequence, state.validation_check])].filter(Boolean);
      return values.filter(value => projected.includes(value)).map(value => ({slide: slide.id, value}));
    });
  });
  assert(metadataLeaks.length === 0, "Projected narrative excludes story state, consequence, and validation metadata");
  const viewports = [
    {width: 1280, height: 720, key: "desktop-1280"},
    {width: 1366, height: 768, key: "desktop-1366"},
    {width: 390, height: 844, key: "mobile-390"},
    {width: 360, height: 800, key: "mobile-360"}
  ];

  for (const viewport of viewports) {
    await page.setViewportSize({width: viewport.width, height: viewport.height});
    for (const [slideIndex, slideId] of slideIds.entries()) {
      await page.goto(`${url}#${slideId}`);
      while (await page.locator("section.active [data-reveal-index]").count()) {
        const metrics = await page.locator("section.active").evaluate((slide, vp) => ({
          scrollWidth: document.documentElement.scrollWidth,
          viewportWidth: window.innerWidth,
          slideScrollHeight: slide.scrollHeight,
          slideClientHeight: slide.clientHeight,
          sceneTop: slide.querySelector(".scene").getBoundingClientRect().top,
          promptTop: slide.querySelector(".prompt").getBoundingClientRect().top,
          revealBottom: slide.querySelector("[data-reveal-index]")?.getBoundingClientRect().bottom || 0,
          viewportHeight: window.innerHeight,
          mobile: vp.width <= 820
        }), viewport);
        assert(metrics.scrollWidth <= metrics.viewportWidth + 1, `${viewport.key} ${slideId} has no horizontal overflow`);
        if (!metrics.mobile) assert(metrics.slideScrollHeight <= metrics.slideClientHeight + 2, `${viewport.key} ${slideId} state fits the presentation viewport`);
        if (metrics.mobile) {
          assert(metrics.sceneTop < metrics.viewportHeight, `${viewport.key} ${slideId} keeps the witness before the fold`);
          assert(metrics.promptTop < metrics.viewportHeight, `${viewport.key} ${slideId} keeps the prompt before the fold`);
          assert(metrics.revealBottom <= metrics.viewportHeight, `${viewport.key} ${slideId} keeps the primary action before the fold`);
        }
        await page.locator("section.active [data-reveal-index]").click();
      }
      const terminalMetrics = await page.locator("section.active").evaluate((slide, vp) => ({
        scrollWidth: document.documentElement.scrollWidth,
        viewportWidth: window.innerWidth,
        slideScrollHeight: slide.scrollHeight,
        slideClientHeight: slide.clientHeight,
        sceneTop: slide.querySelector(".scene").getBoundingClientRect().top,
        promptTop: slide.querySelector(".prompt").getBoundingClientRect().top,
        viewportHeight: window.innerHeight,
        mobile: vp.width <= 820
      }), viewport);
      assert(terminalMetrics.scrollWidth <= terminalMetrics.viewportWidth + 1, `${viewport.key} ${slideId} terminal has no horizontal overflow`);
      if (!terminalMetrics.mobile) assert(terminalMetrics.slideScrollHeight <= terminalMetrics.slideClientHeight + 2, `${viewport.key} ${slideId} terminal fits the presentation viewport`);
      if (terminalMetrics.mobile) {
        assert(terminalMetrics.sceneTop < terminalMetrics.viewportHeight, `${viewport.key} ${slideId} terminal keeps the witness before the fold`);
        assert(terminalMetrics.promptTop < terminalMetrics.viewportHeight, `${viewport.key} ${slideId} terminal keeps the prompt before the fold`);
      }

      const shotKey = `${viewport.key}-${String(slideIndex + 1).padStart(2, "0")}`;
      if ([0, 7, 10, 12, 13].includes(slideIndex)) {
        await page.screenshot({path: `output/playwright/${shotKey}.png`, fullPage: false});
      }
    }
  }

  assert(consoleErrors.length === 0, "Browser console has no errors");
  return {checks: results.length, slides: slideIds.length, states: 32, viewports: viewports.map(v => `${v.width}x${v.height}`), consoleErrors, thirdPartyConsoleErrors};
}
