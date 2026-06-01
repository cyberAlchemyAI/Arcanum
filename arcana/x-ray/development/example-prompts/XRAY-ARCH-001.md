# Experiment Prompt: XRAY-ARCH-001

Use `x-ray` in `architecture` mode.

Target context:

```text
Inventory sync architecture:

The storefront sends stock change events to an event intake service. The intake service validates event shape and writes accepted events to the inventory update queue. A worker consumes the queue, updates the inventory database, and publishes cache invalidation messages. The admin dashboard reads inventory from the database and shows sync status. External dependencies include the storefront event source, the message broker, the database, and the cache system. Failed validation events are written to a review log.
```

Expected evidence:

- mode: `architecture`
- components, boundaries, flows, internal dependencies, external dependencies
- `pattern.dependency-boundary` or similar library pattern where appropriate
- clear assumptions and open questions
- L0 HTML/SVG output or a complete HTML page model
