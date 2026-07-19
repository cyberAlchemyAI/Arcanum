async (page) => {
  const url = page.url().split("#")[0].split("?")[0];
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
  await page.goto(`${url}?opening=1#CRAFT-CAUSAL-S01`);
  assert((await page.locator("section.active h1").textContent()).trim() === "What Would You Need to Build This Table?", "Opening asks the practical table question");
  assert((await page.locator("section.active .prompt").textContent()).includes("fifteen seconds"), "Opening protects private thinking time");
  assert(await page.locator("section.active .build-table-wrap").count() === 1, "Opening shows the table before offering categories");
  assert(await page.locator("section.active iframe").count() === 0, "Opening withholds Mentimeter during private thought");
  assert((await page.locator("section.active [data-reveal-index]").textContent()).includes("Open the word cloud"), "Opening action follows the pause");
  assert(await page.locator(".eyebrow, .consequence, .chapter").count() === 0, "Authoring metadata has no projected selectors");

  await page.locator("section.active [data-reveal-index]").click();
  const iframe = page.locator("section.active iframe[title^='Mentimeter word cloud']");
  assert(await iframe.count() === 1, "Mentimeter replaces the table after the audience thinks");
  assert((await iframe.getAttribute("sandbox")).includes("allow-scripts"), "Mentimeter keeps the supplied sandbox contract");
  await page.waitForTimeout(1000);
  const mentimeterFrameLoaded = page.frames().some(frame => frame.url().includes("mentimeter.com/app/presentation"));
  assert(mentimeterFrameLoaded, "Mentimeter frame loads on the opening slide");
  await page.locator("section.active [data-reveal-index]").click();
  assert(await page.locator("section.active iframe").count() === 0, "Mentimeter unmounts when the room's words return");
  assert(await page.locator("section.active .cloud-word").count() === 8, "The returned cloud retains concrete build vocabulary");
  assert((await page.locator("section.active .visible-list").textContent()).includes("materials"), "The room's words resolve into build-need groups");
  const openingTerminal = await page.locator("section.active .scene").getAttribute("aria-label");
  await page.locator("section.active .scene").focus();
  await page.keyboard.press("Space");
  assert(await page.locator("section.active .scene").getAttribute("aria-label") === openingTerminal, "Terminal Space does not reset the opening interaction");

  await page.keyboard.press("ArrowRight");
  assert((await page.locator("#counter").textContent()).trim() === "2 / 5", "ArrowRight advances from the word cloud to sketching");
  assert((await page.locator("section.active h1").textContent()).trim() === "Now Make the Sketch", "Second slide turns the build list into a sketch");
  assert(await page.locator("section.active .means-strip span").count() === 4, "Sketching begins with the room's four kinds of answers");
  assert(await page.locator("section.active .dimension-x").count() === 0, "The rough sketch withholds chosen dimensions");
  assert(await page.locator("section.active .term").count() === 0, "Schema is not named while the class is still constructing it");
  await page.locator("section.active [data-reveal-index]").click();
  assert((await page.locator("section.active .dimension-x").textContent()).includes("100 cm"), "The annotated sketch carries the selected width");
  assert((await page.locator("section.active .annotation.material").textContent()).includes("pine"), "The annotated sketch carries material and attachment choices");
  assert((await page.locator("section.active .annotation.stability").textContent()).includes("steady"), "The annotated sketch preserves a testable condition");

  await page.keyboard.press("ArrowRight");
  assert((await page.locator("#counter").textContent()).trim() === "3 / 5", "Deck advances from constructing the sketch to naming its function");
  assert((await page.locator("section.active h1").textContent()).trim() === "How Does the Sketch Relate to Schema?", "Third slide asks for the sketch-schema relation");
  assert(await page.locator("section.active .compare-panel").count() === 2, "The relation begins with a plain picture and a buildable structure");
  assert(await page.locator("section.active .term").count() === 0, "The term remains withheld during comparison");
  await page.locator("section.active [data-reveal-index]").click();
  assert((await page.locator("section.active .term").textContent()).trim() === "schema", "The completed relation earns schema");
  assert((await page.locator("section.active .prompt").textContent()).includes("acting as a schema"), "The definition names schema as a role the sketch performs");
  assert(await page.locator("section.active .schema-reason").count() === 3, "The schema reveal states selection, relation, and checking functions");

  await page.keyboard.press("ArrowRight");
  assert((await page.locator("#counter").textContent()).trim() === "4 / 5", "Deck carries the established relation into writing software");
  assert((await page.locator("section.active h1").textContent()).trim() === "What Is the Sketch for Writing Software?", "Fourth slide asks for the writing equivalent of a sketch");
  assert(await page.locator("section.active .blank-page").count() === 1, "Writing transfer begins with an unstructured output surface");
  assert((await page.locator("section.active .prompt").textContent()).includes("role of the table sketch"), "Writing question explicitly transports the table relation");
  await page.locator("section.active [data-reveal-index]").click();
  assert(await page.locator("section.active .mold-field").count() === 7, "The writing mold exposes seven intent-preserving fields");
  const moldText = (await page.locator("section.active .mold-grid").textContent()).toLowerCase();
  for (const field of ["purpose", "audience", "meaning", "evidence", "shape", "voice", "ending"]) {
    assert(moldText.includes(field), `Writing mold includes ${field}`);
  }

  await page.keyboard.press("ArrowRight");
  assert((await page.locator("#counter").textContent()).trim() === "5 / 5", "Deck reaches the boundary of the writing mold");
  assert((await page.locator("section.active h1").textContent()).trim() === "Can One Mold Write Any Text?", "Final slide challenges the universal-template assumption");
  assert(await page.locator("section.active .fixed-outline").count() === 1, "Final challenge shows one rigid outline");
  assert(await page.locator("section.active .text-type").count() === 4, "Rigid outline is tested against four different text types");
  await page.locator("section.active [data-reveal-index]").click();
  assert(await page.locator("section.active .stable-questions").count() === 1, "Adaptable mold preserves stable questions");
  assert(await page.locator("section.active .variable-shape").count() === 1, "Adaptable mold delegates body shape to text type");
  assert((await page.locator("section.active .prompt").textContent()).includes("not the final form"), "Closing statement preserves adaptability");
  assert(await page.locator("#next-slide").isDisabled(), "Presentation stops at the adaptable writing mold");

  const projectedDeckText = await page.evaluate(() => deckData.slides.flatMap(slide => slide.states.map(state => [slide.title, state.learner_prompt, ...state.visible].join(" "))).join(" ").toLowerCase());
  for (const laterTerm of ["artifact", "validation", "residue", "craft layer", "recomposition"]) {
    assert(!projectedDeckText.includes(laterTerm), `Projected deck does not introduce ${laterTerm}`);
  }
  for (const discardedStory of ["first day working from home", "bedroom desk", "desk by tomorrow"]) {
    assert(!projectedDeckText.includes(discardedStory), `Projected deck excludes discarded story: ${discardedStory}`);
  }
  assert(!projectedDeckText.includes("dashboard"), "Projected deck contains no unrelated software example");
  assert(projectedDeckText.includes("software that helps someone write"), "Projected deck contains the intended writing-software transfer");
  assert((await page.evaluate(() => deckData.formal_terms)).join(",") === "schema", "Deck vocabulary contains only schema");

  await page.locator("#notes-toggle").click();
  assert(await page.locator("#notes-toggle").getAttribute("aria-pressed") === "true", "Notes toggle exposes open state");
  assert(await page.locator("#notes-overlay").evaluate(node => node.classList.contains("open")), "Notes open in an overlay");
  await page.keyboard.press("Escape");
  assert(await page.locator("#notes-toggle").getAttribute("aria-pressed") === "false", "Escape closes notes and updates state");

  await page.goto(`${url}?hash=1#CRAFT-CAUSAL-S03`);
  assert((await page.locator("#counter").textContent()).trim() === "3 / 5", "Hash navigation opens the schema-relation slide");

  const slideIds = await page.evaluate(() => deckData.slides.map(slide => slide.id));
  const stateCount = await page.evaluate(() => deckData.slides.reduce((count, slide) => count + slide.states.length, 0));
  assert(slideIds.length === 5, "Deck contains five slides");
  assert(stateCount === 11, "Deck contains eleven interaction states");
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
      await page.goto(`${url}?matrix=${viewport.key}-${slideIndex}#${slideId}`);
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
        promptTop: slide.querySelector(".prompt").getBoundingClientRect().top,
        viewportHeight: window.innerHeight,
        mobile: vp.width <= 820
      }), viewport);
      assert(terminalMetrics.scrollWidth <= terminalMetrics.viewportWidth + 1, `${viewport.key} ${slideId} terminal has no horizontal overflow`);
      if (!terminalMetrics.mobile) assert(terminalMetrics.slideScrollHeight <= terminalMetrics.slideClientHeight + 2, `${viewport.key} ${slideId} terminal fits the presentation viewport`);
      if (terminalMetrics.mobile) assert(terminalMetrics.promptTop < terminalMetrics.viewportHeight, `${viewport.key} ${slideId} terminal keeps the prompt before the fold`);

      await page.screenshot({path: `output/playwright/${viewport.key}-schema-${String(slideIndex + 1).padStart(2, "0")}.png`, fullPage: false});
    }
  }

  assert(consoleErrors.length === 0, "Browser console has no local errors");
  return {
    checks: results.length,
    slides: slideIds.length,
    states: stateCount,
    viewports: viewports.map(item => `${item.width}x${item.height}`),
    mentimeterFrameLoaded,
    consoleErrors,
    thirdPartyConsoleErrors
  };
}
