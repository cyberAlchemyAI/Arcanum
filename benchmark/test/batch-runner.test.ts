import { strict as assert } from "node:assert";
import test from "node:test";

import { countStatuses } from "../src/batch-runner.ts";

test("batch status counts separate pass, fail, infra-fail, and quarantine", () => {
  assert.deepEqual(
    countStatuses([
      { status: "pass" },
      { status: "fail" },
      { status: "infra-fail" },
      { status: "quarantined" },
      { status: "pass" }
    ]),
    {
      pass: 2,
      fail: 1,
      "infra-fail": 1,
      quarantined: 1
    }
  );
});
