import { strict as assert } from "node:assert";
import test from "node:test";

import { harnessSkeleton } from "../src/index.ts";

test("benchmark harness skeleton is importable", () => {
  assert.equal(harnessSkeleton.name, "agentic-tech-debt-optimization-harness");
  assert.equal(harnessSkeleton.status, "skeleton");
  assert.equal(harnessSkeleton.kernel, "benchmark-run");
});
