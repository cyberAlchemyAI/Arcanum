'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');

const {
  DEFAULT_RECORD_CLASSES,
  normalizeEntry,
} = require('../lib/inventory-update.cjs');

const fixtureRoot = path.join(__dirname, 'fixtures', 'facet-admission');
const timestamp = '2026-07-24T18:19:00Z';
const policy = {
  namespaces: ['example-space'],
  recordClasses: DEFAULT_RECORD_CLASSES,
};

function fixture(name) {
  return JSON.parse(fs.readFileSync(path.join(fixtureRoot, name), 'utf8'));
}

test('valid faceted record normalizes and byte-sorts concepts', () => {
  const normalized = normalizeEntry(fixture('valid.json'), timestamp, policy);
  assert.equal(normalized.namespace, 'example-space');
  assert.equal(normalized.record_class, 'research');
  assert.deepEqual(normalized.concepts, ['append-runtime', 'test-generation']);
  assert.equal(
    normalized.path,
    'entries/example-space/research/stable-record.md',
  );
});

test('legacy record remains valid without facet fields or path migration', () => {
  const record = fixture('legacy.json');
  const normalized = normalizeEntry(record, timestamp, policy);
  assert.equal(normalized.path, 'entries/legacy-record.md');
  assert.equal(Object.hasOwn(normalized, 'namespace'), false);
  assert.equal(Object.hasOwn(normalized, 'record_class'), false);
  assert.equal(Object.hasOwn(normalized, 'concepts'), false);
});

test('partial facet metadata blocks', () => {
  for (const omitted of ['namespace', 'record_class', 'concepts']) {
    const record = fixture('valid.json');
    delete record[omitted];
    assert.throws(
      () => normalizeEntry(record, timestamp, policy),
      /must be provided together/,
    );
  }
});

test('traversal, unknown namespace, unknown class, and path mismatch block', () => {
  const traversal = fixture('valid.json');
  traversal.namespace = '../escape';
  assert.throws(() => normalizeEntry(traversal, timestamp, policy), /path-safe token/);

  const namespace = fixture('valid.json');
  namespace.namespace = 'unknown-space';
  namespace.path = 'entries/unknown-space/research/stable-record.md';
  assert.throws(() => normalizeEntry(namespace, timestamp, policy), /not configured/);

  const recordClass = fixture('valid.json');
  recordClass.record_class = 'unknown-class';
  recordClass.path = 'entries/example-space/unknown-class/stable-record.md';
  assert.throws(() => normalizeEntry(recordClass, timestamp, policy), /not controlled/);

  const pathMismatch = fixture('valid.json');
  pathMismatch.path = 'entries/example-space/research/wrong-id.md';
  assert.throws(() => normalizeEntry(pathMismatch, timestamp, policy), /must equal/);
});

test('empty concepts and normalization collisions block', () => {
  const empty = fixture('valid.json');
  empty.concepts = [];
  assert.throws(() => normalizeEntry(empty, timestamp, policy), /non-empty array/);

  const blank = fixture('valid.json');
  blank.concepts = ['   '];
  assert.throws(() => normalizeEntry(blank, timestamp, policy), /path-safe token/);

  const duplicate = fixture('valid.json');
  duplicate.concepts = ['Test Generation', 'test-generation'];
  assert.throws(() => normalizeEntry(duplicate, timestamp, policy), /normalized duplicates/);
});

test('tags and concepts never create physical directories', () => {
  const record = fixture('valid.json');
  record.tags = ['tag/with/slash', 'another'];
  record.concepts = ['concept-one', 'concept-two'];
  const normalized = normalizeEntry(record, timestamp, policy);
  assert.equal(normalized.path, 'entries/example-space/research/stable-record.md');
  assert.equal(normalized.path.includes('concept-one'), false);
  assert.equal(normalized.path.includes('tag/with/slash'), false);
});

test('consumer policy may extend record classes without public private names', () => {
  const record = fixture('valid.json');
  record.record_class = 'custom-class';
  record.path = 'entries/example-space/custom-class/stable-record.md';
  const normalized = normalizeEntry(record, timestamp, {
    namespaces: ['example-space'],
    recordClasses: [...DEFAULT_RECORD_CLASSES, 'custom-class'],
  });
  assert.equal(normalized.record_class, 'custom-class');
});
