#!/usr/bin/env node

import assert from "node:assert/strict";
import { existsSync, readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const ontologyRoot = resolve(here, "../..");
const catalogPath = resolve(here, "../../catalogs/ontology-types.json");
const fixturePath = resolve(here, "fixtures/routing-cases.json");
const catalog = JSON.parse(readFileSync(catalogPath, "utf8"));
const fixture = JSON.parse(readFileSync(fixturePath, "utf8"));
const types = new Map(
  catalog.types.map((entry) => [entry.ontology_type_id, entry]),
);

assert.equal(types.size, catalog.types.length, "ontology type IDs must be unique");
assert.equal(catalog.authority_effect, "none");
assert.deepEqual(catalog.selection_sources, [
  "explicit",
  "profile",
  "inferred",
  "user",
]);
assert.equal(catalog.ambiguity_policy.minimum_choices, 2);
assert.equal(catalog.ambiguity_policy.maximum_choices, 3);
assert.equal(catalog.ambiguity_policy.forbid_silent_default, true);

const requiredTypes = new Set([
  "knowledge-vault",
  "business-domain",
  "system-runtime",
  "business-system-bridge",
  "authority-governance",
  "architecture-property",
]);
assert.deepEqual(new Set(types.keys()), requiredTypes);

for (const entry of types.values()) {
  assert.ok(entry.label.length > 0, `${entry.ontology_type_id} needs a label`);
  assert.ok(
    entry.primary_job.length > 0,
    `${entry.ontology_type_id} needs a primary job`,
  );
  assert.ok(
    entry.model_focus.length > 0,
    `${entry.ontology_type_id} needs model focus`,
  );
  assert.ok(
    entry.clear_intent_signals.length > 0,
    `${entry.ontology_type_id} needs clear intent signals`,
  );
  assert.ok(
    entry.selection_consequence.length > 0,
    `${entry.ontology_type_id} needs a selection consequence`,
  );
}

assert.deepEqual(types.get("business-domain").derived_arguments, [
  "--branch",
  "business",
]);
assert.deepEqual(types.get("system-runtime").derived_arguments, [
  "--branch",
  "system",
]);
assert.deepEqual(types.get("architecture-property").derived_arguments, [
  "--branch",
  "system",
]);
assert.deepEqual(
  types.get("business-system-bridge").derived_arguments,
  ["--branches", "business,system", "--bridge", "business-system"],
);

const architectureFocus = new Set(
  types.get("architecture-property").model_focus,
);
for (const requiredFocus of [
  "architecture element types",
  "typed property definitions",
  "allowed relations",
  "architecture profiles",
  "observation projections",
  "explainable property findings",
]) {
  assert.ok(
    architectureFocus.has(requiredFocus),
    `architecture-property is missing ${requiredFocus}`,
  );
}

const choiceFor = (ontologyTypeId) => {
  const entry = types.get(ontologyTypeId);
  assert.ok(entry, `unknown ambiguity candidate ${ontologyTypeId}`);
  return {
    ontology_type_id: ontologyTypeId,
    label: entry.label,
    consequence: entry.selection_consequence,
  };
};

const selected = (ontologyTypeId, source, alias = null) => {
  const entry = types.get(ontologyTypeId);
  assert.ok(entry, `unknown selected ontology type ${ontologyTypeId}`);
  return {
    selected_ontology_type: ontologyTypeId,
    selection_source: source,
    selection_confidence: source === "inferred" ? "high" : "exact",
    ambiguity_candidates: [],
    user_selection_required: false,
    project_local_type_alias: alias,
    derived_arguments: entry.derived_arguments,
  };
};

const route = (testCase) => {
  const { inputs } = testCase;
  if (inputs.explicit_ontology_type) {
    return selected(inputs.explicit_ontology_type, "explicit");
  }

  if (inputs.profile) {
    assert.ok(
      inputs.profile.ontology_type,
      `${testCase.case_id} profile needs ontology_type`,
    );
    assert.ok(
      inputs.profile.ontology_type_alias,
      `${testCase.case_id} local profile needs ontology_type_alias`,
    );
    assert.equal(
      types.has(inputs.profile.ontology_type_alias),
      false,
      `${testCase.case_id} local alias must not extend the catalog`,
    );
    return selected(
      inputs.profile.ontology_type,
      "profile",
      inputs.profile.ontology_type_alias,
    );
  }

  const matchedTypeIds = new Set();
  for (const match of inputs.matched_catalog_signals) {
    const entry = types.get(match.ontology_type_id);
    assert.ok(entry, `${testCase.case_id} matched an unknown type`);
    assert.ok(
      entry.clear_intent_signals.includes(match.signal),
      `${testCase.case_id} used an undeclared intent signal`,
    );
    matchedTypeIds.add(match.ontology_type_id);
  }

  if (matchedTypeIds.size === 1) {
    return selected([...matchedTypeIds][0], "inferred");
  }

  const candidateIds =
    inputs.candidate_hints ?? [...matchedTypeIds].slice(0, 3);
  assert.ok(
    candidateIds.length >= catalog.ambiguity_policy.minimum_choices &&
      candidateIds.length <= catalog.ambiguity_policy.maximum_choices,
    `${testCase.case_id} ambiguity must offer two or three choices`,
  );
  assert.equal(
    new Set(candidateIds).size,
    candidateIds.length,
    `${testCase.case_id} ambiguity choices must be unique`,
  );

  return {
    selected_ontology_type: null,
    selection_source: null,
    selection_confidence: "low",
    ambiguity_candidates: candidateIds.map(choiceFor),
    user_selection_required: true,
    project_local_type_alias: null,
    derived_arguments: [],
  };
};

const seenCaseIds = new Set();
for (const testCase of fixture.cases) {
  assert.equal(
    seenCaseIds.has(testCase.case_id),
    false,
    `duplicate case ID ${testCase.case_id}`,
  );
  seenCaseIds.add(testCase.case_id);
  assert.equal(
    /DomainSpec|cyberAlchemy|\/home\//.test(testCase.prompt),
    false,
    `${testCase.case_id} must remain product-neutral and privacy-safe`,
  );
  assert.deepEqual(route(testCase), testCase.expected, testCase.case_id);
}

for (const requiredCase of [
  "clear-architecture-property-correction-regression",
  "clear-business-domain",
  "clear-system-runtime",
  "clear-business-system-bridge",
  "ambiguous-generic-package-ontology",
  "project-local-profile-alias",
]) {
  assert.ok(seenCaseIds.has(requiredCase), `missing case ${requiredCase}`);
}

const clearCases = fixture.cases.filter(
  (testCase) => testCase.expected.selected_ontology_type !== null,
);
assert.ok(clearCases.every((testCase) => !testCase.expected.user_selection_required));

const ambiguousCases = fixture.cases.filter(
  (testCase) => testCase.expected.selected_ontology_type === null,
);
assert.ok(ambiguousCases.length > 0, "at least one ambiguity case is required");
assert.ok(ambiguousCases.every((testCase) => testCase.expected.user_selection_required));

const markdownFiles = [
  resolve(ontologyRoot, "README.md"),
  resolve(ontologyRoot, "SKILL.md"),
  resolve(ontologyRoot, "templates/runtime-profile.md"),
  resolve(here, "README.md"),
  resolve(here, "LOCAL-OBSERVER-REPORT.md"),
  resolve(here, "REFLECTION-REPORT.md"),
];
let linkCount = 0;
for (const markdownPath of markdownFiles) {
  const markdown = readFileSync(markdownPath, "utf8");
  for (const match of markdown.matchAll(/\[[^\]]+\]\(([^)]+)\)/g)) {
    const target = match[1];
    if (
      target.startsWith("#") ||
      target.startsWith("http://") ||
      target.startsWith("https://") ||
      target.includes("{")
    ) {
      continue;
    }
    const localTarget = target.split("#")[0];
    assert.ok(
      existsSync(resolve(dirname(markdownPath), localTarget)),
      `${markdownPath} has a missing link target: ${target}`,
    );
    linkCount += 1;
  }
}

console.log(
  `PASS ontology type catalog: ${catalog.types.length} reusable types validated`,
);
console.log(
  `PASS routing fixtures: ${fixture.cases.length} cases (${clearCases.length} clear, ${ambiguousCases.length} ambiguous)`,
);
console.log(
  "PASS architecture-property regression: property routing remains distinct from business-system bridge routing",
);
console.log(
  "PASS project-local alias policy: alias preserved without extending reusable vocabulary",
);
console.log(
  `PASS Markdown links: ${linkCount} local targets resolved across ${markdownFiles.length} files`,
);
