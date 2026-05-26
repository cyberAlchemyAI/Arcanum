import { strict as assert } from "node:assert";
import test from "node:test";

import { total } from "../src/calculator.js";

test("total adds every value", () => {
  assert.equal(total([2, 3, 5]), 10);
});

test("total handles an empty list", () => {
  assert.equal(total([]), 0);
});
