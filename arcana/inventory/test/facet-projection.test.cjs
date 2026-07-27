'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { spawnSync } = require('node:child_process');
const test = require('node:test');

const {
  normalizeEntry,
  updateIndex,
} = require('../lib/inventory-update.cjs');

const inventoryRoot = path.resolve(__dirname, '..');
const fixtureRoot = path.join(__dirname, 'fixtures', 'facet-projection');
const validator = path.join(inventoryRoot, 'scripts', 'validate_projection_conformance.py');

function runValidator(indexPath) {
  return spawnSync('python3', [validator, indexPath, '--json'], {
    encoding: 'utf8',
  });
}

test('independent validator accepts exact mixed legacy/faceted maps', () => {
  const result = runValidator(path.join(fixtureRoot, 'index.json'));
  assert.equal(result.status, 0, result.stderr);
  const report = JSON.parse(result.stdout);
  assert.equal(report.lookup_readiness, 'ready');
  assert.equal(report.checks.facet_admission.status, 'pass');
  assert.equal(report.checks.derived_maps.status, 'pass');
  assert.equal(report.checks.facet_admission.faceted_entry_count, 2);
});

test('validator rejects any non-exact facet map', () => {
  const temporary = fs.mkdtempSync(path.join(os.tmpdir(), 'facet-map-'));
  try {
    fs.cpSync(fixtureRoot, temporary, { recursive: true });
    const indexPath = path.join(temporary, 'index.json');
    const index = JSON.parse(fs.readFileSync(indexPath, 'utf8'));
    index.indexes.by_concept.shared = ['facet-b', 'facet-a'];
    fs.writeFileSync(indexPath, `${JSON.stringify(index, null, 2)}\n`);
    const result = runValidator(indexPath);
    assert.equal(result.status, 1);
    const report = JSON.parse(result.stdout);
    assert.match(report.checks.derived_maps.errors.join('\n'), /by_concept/);
  } finally {
    fs.rmSync(temporary, { recursive: true, force: true });
  }
});

test('updater derives facet maps in canonical entry order', () => {
  const index = JSON.parse(fs.readFileSync(path.join(fixtureRoot, 'index.json'), 'utf8'));
  const record = {
    id: 'facet-c',
    path: 'entries/example-space/research/facet-c.md',
    kind: 'entry',
    type: 'research',
    title: 'Facet C',
    summary: 'Third faceted record.',
    tags: ['known'],
    namespace: 'example-space',
    record_class: 'research',
    concepts: ['gamma', 'shared'],
  };
  const normalized = normalizeEntry(record, '2026-07-24T18:19:00Z', {
    namespaces: ['example-space'],
    recordClasses: ['research', 'review'],
  });
  const result = updateIndex(index, normalized, '2026-07-24T18:19:00Z');
  assert.deepEqual(result.index.indexes.by_namespace['example-space'], [
    'facet-a',
    'facet-b',
    'facet-c',
  ]);
  assert.deepEqual(result.index.indexes.by_record_class.research, [
    'facet-a',
    'facet-c',
  ]);
  assert.deepEqual(result.index.indexes.by_concept.shared, [
    'facet-a',
    'facet-b',
    'facet-c',
  ]);
  assert.deepEqual(result.index.indexes.by_concept.gamma, ['facet-c']);
});

test('legacy records remain absent from every facet map', () => {
  const index = JSON.parse(fs.readFileSync(path.join(fixtureRoot, 'index.json'), 'utf8'));
  for (const mapName of ['by_namespace', 'by_record_class', 'by_concept']) {
    for (const ids of Object.values(index.indexes[mapName])) {
      assert.equal(ids.includes('legacy'), false);
      assert.equal(new Set(ids).size, ids.length);
    }
  }
});

test('human represented type mismatch remains blocking', () => {
  const temporary = fs.mkdtempSync(path.join(os.tmpdir(), 'facet-human-'));
  try {
    fs.cpSync(fixtureRoot, temporary, { recursive: true });
    const humanPath = path.join(temporary, 'index.md');
    const human = fs.readFileSync(humanPath, 'utf8').replace(
      '| review | `known` | Second faceted record. |',
      '| research | `known` | Second faceted record. |',
    );
    fs.writeFileSync(humanPath, human);
    const result = runValidator(path.join(temporary, 'index.json'));
    assert.equal(result.status, 1);
    const report = JSON.parse(result.stdout);
    assert.match(report.checks.human_view.errors.join('\n'), /type mismatch/);
  } finally {
    fs.rmSync(temporary, { recursive: true, force: true });
  }
});

test('new package template declares all facet maps', () => {
  const template = JSON.parse(
    fs.readFileSync(path.join(inventoryRoot, 'templates', 'index.json'), 'utf8'),
  );
  assert.deepEqual(template.indexes.by_namespace, {});
  assert.deepEqual(template.indexes.by_record_class, {});
  assert.deepEqual(template.indexes.by_concept, {});
});
