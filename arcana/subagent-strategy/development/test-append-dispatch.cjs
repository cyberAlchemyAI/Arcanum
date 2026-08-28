#!/usr/bin/env node
'use strict';
/*
 * Test battery for the Arcanum append-dispatch.cjs (schema v0.7.0).
 *
 *   node arcana/subagent-strategy/development/test-append-dispatch.cjs
 *
 * Zero-dependency, self-contained. Every case runs the appender as a child
 * process against a FRESH TEMP DIRECTORY used as the project root. Records
 * are written below the runtime temp root and passed with --consume. The real
 * repository ledger is NEVER touched.
 */
const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawnSync } = require('child_process');

const APPENDER = path.join(__dirname, '..', 'scripts', 'append-dispatch.cjs');
if (!fs.existsSync(APPENDER)) { console.error('appender not found:', APPENDER); process.exit(1); }

const roots = [];
function freshRoot() {
  const d = fs.mkdtempSync(path.join(os.tmpdir(), 'append-dispatch-test-'));
  roots.push(d);
  return d;
}
function ledgerPath(root) {
  return path.join(root, '.arcanum', 'observability', 'subagents-strategy', 'subagents-dispatch.yaml');
}
function readLedger(root) {
  const p = ledgerPath(root);
  return fs.existsSync(p) ? fs.readFileSync(p, 'utf8') : '';
}

let seq = 0;
// Run the appender against `root` with `record`, with optional extra env.
function run(root, record, extraEnv) {
  const tempRoot = path.join(root, '.arcanum', 'runtime', 'subagents-strategy');
  fs.mkdirSync(tempRoot, { recursive: true });
  const tmp = path.join(tempRoot, `rec-${++seq}.tmp.json`);
  fs.writeFileSync(tmp, JSON.stringify(record));
  const env = Object.assign({}, process.env, { ARCANUM_PROJECT_DIR: root }, extraEnv || {});
  const r = spawnSync(process.execPath, [APPENDER, '--consume', tmp], { env, encoding: 'utf8' });
  return {
    status: r.status,
    stdout: r.stdout || '',
    stderr: r.stderr || '',
    tempExists: fs.existsSync(tmp),
  };
}

let pass = 0, fail = 0, skip = 0;
const failures = [];
function check(name, cond, detail) {
  if (cond) { pass++; console.log('  PASS  ' + name); }
  else {
    fail++; failures.push(name);
    console.log('  FAIL  ' + name + (detail ? '\n        ' + String(detail).split('\n').join('\n        ') : ''));
  }
}
function note(name, why) { skip++; console.log('  SKIP  ' + name + ' — ' + why); }

// expects exit 2 and (optionally) a stderr pattern
function expectReject(name, root, record, pattern) {
  const r = run(root, record);
  const ok = r.status === 2 && (!pattern || pattern.test(r.stderr));
  check(name, ok, `exit=${r.status}\nstderr=${r.stderr.trim()}`);
}

// ---------------------------------------------------------------- fixtures
function validDispatch(over) {
  return Object.assign({
    dispatch_id: '2026-06-12-battery-main',
    schema_version: '0.7.0',
    dispatch_type: 'research',
    goal: 'Prove the v0.7.0 appender end to end.',
    context: 'Synthetic record produced by the test battery. Runs against a temp ledger, never the real one.',
    max_loops: 2,
    final_approver: 'parent',
    anti_bias_global: 'optimism vs skepticism',
    working_folder: 'research/battery-topic/',
    invoked_by: 'tester@example.com',
    groups: [
      {
        group_id: 'explorers', n: 2,
        anti_bias: 'methodology (static reading vs dynamic probing)',
        predicted_disagreements: [{ between: [0, 1], question: 'Will static reading or dynamic probing expose the decisive defect?' }],
        agents: [
          { agent_name: 'Abramsky, Samson', role: 'explorer', model: 'claude-sonnet-4-6', token_budget: 800,
            angle: 'static-reading side', initial_prompt: 'You are Abramsky, Samson.\n\nExplore statically.\nSecond line proves stringify newline escaping.' },
          { agent_name: 'Hewitt, Carl', role: 'explorer', model: 'claude-opus-4-8', token_budget: 800,
            angle: 'dynamic-probing side', initial_prompt: 'You are Hewitt, Carl.\n\nExplore dynamically.' },
        ],
      },
      {
        group_id: 'synthesizer',
        agents: [
          { agent_name: 'Shannon, Claude', role: 'writer', model: 'claude-opus-4-8', token_budget: 4000, initial_prompt: 'You are Shannon, Claude.\n\nSynthesize the explorers\' returns.' },
        ],
      },
    ],
    connections: [
      { from: 'explorers', to: 'synthesizer', type: 'sequential' },
      { from: 'synthesizer', to: 'explorers', type: 'feedback', loop_cap: 1 },
    ],
  }, over);
}
function validClose(over) {
  return Object.assign({
    close_of: '2026-06-12-battery-main',
    exit_reason: 'resolved',
    agents_spawned: validSpawn(),
    feedback_prompts: ['Verbatim feedback ask sent back to the explorers.'],
    invoked_by: 'tester@example.com',
  }, over);
}

function validSpawn(over) {
  return Object.assign({
    planned_total: 3,
    total: 3,
    not_launched: 0,
    tree: { explorer: 2, writer: 1, helpers: 0 },
    loops_used: 1,
  }, over);
}
// Drop a key from a fresh valid record.
function without(base, key) { const r = Object.assign({}, base); delete r[key]; return r; }
// A record with TWO fan-out groups (explorers n=2 + reviewers n=2) — the
// anti_bias_global conditional's trigger shape (constitution §9, D2).
function twoFanout(over) {
  const r = validDispatch(Object.assign({ dispatch_id: '2026-06-12-battery-two-fanout' }, over));
  r.groups.push({
    group_id: 'reviewers', n: 2,
    anti_bias: 'attack-vector (precedent-kill vs non-vacuity)',
    predicted_disagreements: [{ between: [0, 1], question: 'Does precedent-kill or non-vacuity control the verdict?' }],
    agents: [
      { agent_name: 'Sattler, Christian', role: 'skeptic', model: 'claude-opus-4-8', token_budget: 1000, angle: 'precedent-kill gate', initial_prompt: 'You are Sattler, Christian.\n\nAttack precedent.' },
      { agent_name: 'Popper, Karl', role: 'skeptic', model: 'claude-opus-4-8', token_budget: 1000, angle: 'non-vacuity gate', initial_prompt: 'You are Popper, Karl.\n\nAttack vacuity.' },
    ],
  });
  return r;
}

// =====================================================================
console.log('\n[1] valid full v0.7.0 row appends; emitted lines pass the self-check on a second append');
{
  const root = freshRoot();
  const r1 = run(root, validDispatch());
  check('1a valid dispatch row appends (exit 0)', r1.status === 0, r1.stderr || r1.stdout);
  const text = readLedger(root);
  check('1b row start emitted', /^  - dispatch_id: "2026-06-12-battery-main"$/m.test(text), text);
  check('1c schema_version block key', /^    schema_version: "0\.7\.0"$/m.test(text), text);
  check('1d invoked_by taken from record', /^    invoked_by: "tester@example\.com"$/m.test(text), text);
  check('1e created stamped by appender', /^    created: "\d{4}-\d{2}-\d{2}T/m.test(text), text);
  check('1f exact temporary sheet digest emitted', /^    sheet_sha256: "[a-f0-9]{64}"$/m.test(text), text);
  check('1g successful dispatch temp consumed', r1.tempExists === false, r1.stdout);
  check('1h groups emitted as JSON column', /^    groups: \[\{"group_id":"explorers"/m.test(text), text);
  check('1i connections emitted as JSON column', /^    connections: \[\{"from":"explorers"/m.test(text), text);
  {
    const marker = 'Second line proves stringify newline escaping';
    const hits = text.split('\n').filter((l) => l.includes(marker));
    check('1j newline inside initial_prompt is escaped (groups JSON column is ONE physical line)',
      hits.length === 1 && hits[0].startsWith('    groups: '), text);
  }
  // second append over the same ledger — the self-check must accept the emitted row
  const r2 = run(root, validDispatch({ dispatch_id: '2026-06-12-battery-second' }));
  check('1k second append passes self-check over the first emitted row (exit 0)', r2.status === 0, r2.stderr || r2.stdout);
  check('1l both rows present', /battery-main/.test(readLedger(root)) && /battery-second/.test(readLedger(root)));
}

console.log('\n[2] each missing required dispatch field is rejected (exit 2)');
{
  const root = freshRoot();
  const fieldPattern = {
    dispatch_id: /dispatch_id is required/,
    schema_version: /schema_version must be exactly "0\.7\.0"/,
    dispatch_type: /dispatch_type must be one of/,
    goal: /goal is required/,
    context: /context is required/,
    max_loops: /max_loops must be an integer in 1\.\.5/,
    final_approver: /final_approver is required/,
    groups: /groups is required/,
  };
  for (const f of Object.keys(fieldPattern)) {
    expectReject(`2 missing ${f}`, root, without(validDispatch(), f), fieldPattern[f]);
  }
  // required fields inside group / agent
  expectReject('2 group missing group_id', root, validDispatch({ groups: [{ agents: [{ role: 'writer', model: 'm', token_budget: 1, initial_prompt: 'p' }] }] }), /group_id is required/);
  expectReject('2 agent missing token_budget', root, validDispatch({ groups: [{ group_id: 'g', agents: [{ role: 'writer', model: 'm', initial_prompt: 'p' }] }], connections: [] }), /token_budget is required/);
  expectReject('2 agent missing initial_prompt', root, validDispatch({ groups: [{ group_id: 'g', agents: [{ role: 'writer', model: 'm', token_budget: 1 }] }], connections: [] }), /initial_prompt is required/);
  const missingIdentity = validDispatch();
  delete missingIdentity.groups[0].agents[0].agent_name;
  expectReject('2 agent missing agent_name', root, missingIdentity, /agent_name is required/);
  const wrongIdentityPrefix = validDispatch();
  wrongIdentityPrefix.groups[0].agents[0].initial_prompt = 'You are Hewitt, Carl.\n\nExplore statically.';
  expectReject('2 initial_prompt identity mismatch', root, wrongIdentityPrefix, /initial_prompt must start exactly with "You are Abramsky, Samson\."/);
  const emptyInstructionBody = validDispatch();
  emptyInstructionBody.groups[0].agents[0].initial_prompt = 'You are Abramsky, Samson.\n\n';
  expectReject('2 initial_prompt requires bounded instructions after identity', root, emptyInstructionBody, /followed by a blank line/);
  check('2z ledger untouched by rejected records', readLedger(root) === '');
}

console.log('\n[3] wrong schema_version rejected');
{
  const root = freshRoot();
  expectReject('3a schema_version "0.3.0"', root, validDispatch({ schema_version: '0.3.0' }), /schema_version must be exactly "0\.7\.0"/);
  expectReject('3b schema_version 0.6.0 as number', root, validDispatch({ schema_version: 0.6 }), /schema_version/);
  expectReject('3c old schema_version "0.5.2" now rejected', root, validDispatch({ schema_version: '0.5.2' }), /schema_version must be exactly "0\.7\.0"/);
}

console.log('\n[4] bad enum values rejected');
{
  const root = freshRoot();
  expectReject('4a dispatch_type "audit"', root, validDispatch({ dispatch_type: 'audit' }), /dispatch_type must be one of/);
  const g = validDispatch();
  g.groups[1].role = 'synthesize';
  expectReject('4b group `role` is now an unknown key (removed v0.6.0)', root, g, /unknown key "role"/);
  const a = validDispatch();
  a.groups[1].agents[0].role = 'reviewer';
  expectReject('4c agent role "reviewer"', root, a, /role must be one of explorer/);
  // the rejection message must enumerate the full v0.6.0 role vocab, incl. synthesizer
  expectReject('4c2 role error lists synthesizer in the enum', root, a, /explorer \| synthesizer \| skeptic \| writer \| auditor/);
  // synthesizer is a LIVE role (model change: writer split into synthesizer+writer) — must be accepted
  const syn = validDispatch({ dispatch_id: '2026-06-12-battery-synthesizer-role' });
  syn.groups[1].agents[0].role = 'synthesizer';
  const rSyn = run(root, syn);
  check('4c3 synthesizer with a pool-admitted identity is accepted',
    rSyn.status === 0, rSyn.stderr || rSyn.stdout);
  expectReject('4d exit_reason "success"', root, validClose({ exit_reason: 'success' }), /exit_reason must be one of resolved/);
  expectReject('4e agents_spawned missing tree', root, validClose({ agents_spawned: validSpawn({ tree: undefined }) }), /agents_spawned\.tree/);
  expectReject('4f agents_spawned non-numeric total', root, validClose({ agents_spawned: validSpawn({ total: 'three', tree: {} }) }), /agents_spawned\.total/);
  expectReject('4g close row missing loops_used', root, validClose({ agents_spawned: validSpawn({ loops_used: undefined }) }), /agents_spawned\.loops_used is required/);
  expectReject('4h negative loops_used', root, validClose({ agents_spawned: validSpawn({ loops_used: -1 }) }), /agents_spawned\.loops_used is required and must be a non-negative integer/);
}

console.log('\n[5] pre-v0.5.2 keys rejected with the right per-provenance message');
{
  const root = freshRoot();
  // keys in constitution §7's removed table — removed-by-v0.5.2 message
  const removed = { success_metric: { type: 'closure' }, constraints: ['x'], created: '2026-06-12T00:00:00Z' };
  for (const [k, v] of Object.entries(removed)) {
    expectReject(`5 removed key ${k}`, root, validDispatch({ [k]: v }), new RegExp(`"${k}" was removed by schema v0\\.5\\.2`));
  }
  // old ledger-row-only keys (not in §7's table) — pre-v0.5.2-ledger-row message
  const legacy = { status: 'dispatched', anti_bias: { axis: 'x' }, agents: [{ role: 'explorer' }],
    corpus: 'research/audits', topic_slug: 'slug', session: 's1' };
  for (const [k, v] of Object.entries(legacy)) {
    expectReject(`5 legacy ledger key ${k}`, root, validDispatch({ [k]: v }), new RegExp(`"${k}" is a pre-v0\\.5\\.2 ledger-row key, not in the v0\\.5\\.2 schema`));
  }
}

console.log('\n[6] missing angle / anti_bias in a 2-agent group rejected');
{
  const root = freshRoot();
  const noAngle = validDispatch();
  delete noAngle.groups[0].agents[0].angle;
  expectReject('6a missing angle on one agent of a 2-agent group', root, noAngle, /angle is required when the group has >= 2 agents/);
  const noAxis = validDispatch();
  delete noAxis.groups[0].anti_bias;
  expectReject('6b missing anti_bias on a 2-agent group', root, noAxis, /anti_bias is required when the group has >= 2 agents/);
  // control: a 1-agent group needs neither (the base fixture's synthesizer already proves it in [1])
}

console.log('\n[7] n mismatch with agents.length rejected');
{
  const root = freshRoot();
  const r = validDispatch();
  r.groups[0].n = 3;
  expectReject('7a n=3 with 2 agents', root, r, /must equal agents\.length/);
  expectReject('7b n=0', root, (() => { const x = validDispatch(); x.groups[0].n = 0; return x; })(), /n must be an integer >= 1/);
}

console.log('\n[8] connection referencing an undeclared group_id rejected');
{
  const root = freshRoot();
  const r = validDispatch();
  r.connections.push({ from: 'ghosts', to: 'synthesizer', type: 'sequential' });
  expectReject('8 from "ghosts" undeclared', root, r, /does not reference a declared group_id/);
}

console.log('\n[9] loop_cap on a sequential connection rejected');
{
  const root = freshRoot();
  const r = validDispatch();
  r.connections[0].loop_cap = 2; // explorers -> synthesizer is sequential
  expectReject('9 loop_cap on sequential', root, r, /loop_cap must be ABSENT on a sequential connection/);
}

console.log('\n[10] working_folder rules');
{
  const root = freshRoot();
  expectReject('10a research without working_folder', root, without(validDispatch(), 'working_folder'), /working_folder is required when dispatch_type is "research"/);
  expectReject('10b working_folder under vault/', root, validDispatch({ working_folder: 'vault/discovery/x/' }), /must never point into vault\//);
  // hardened vault guard (normalized): leading ./ or .\, case-insensitive, bare "vault"
  expectReject('10d "./vault/x" rejected (leading ./ stripped)', root, validDispatch({ working_folder: './vault/x' }), /must never point into vault\//);
  expectReject('10e "Vault/x" rejected (case-insensitive)', root, validDispatch({ working_folder: 'Vault/x' }), /must never point into vault\//);
  expectReject('10f "vault\\x" rejected (backslash separator)', root, validDispatch({ working_folder: 'vault\\x' }), /must never point into vault\//);
  expectReject('10g bare "vault" rejected', root, validDispatch({ working_folder: 'vault' }), /must never point into vault\//);
  const rv = run(root, validDispatch({ dispatch_id: '2026-06-12-battery-vaulted', working_folder: 'vaulted/x/' }));
  check('10h "vaulted/x/" accepted — no vault-guard false positive', rv.status === 0, rv.stderr || rv.stdout);
  // a non-research type does not require working_folder (reserved-type note, still appends)
  expectReject('10c reserved code type is blocked by readiness', root,
    validDispatch({ dispatch_id: '2026-06-12-battery-code', dispatch_type: 'code', working_folder: undefined }), /has no live owner/);
  // experiment is LIVE (2026-06-14) — requires working_folder like research/review, no FORECAST note
  expectReject('10i experiment without working_folder rejected (LIVE type)', root, validDispatch({ dispatch_id: '2026-06-12-battery-exp-nf', dispatch_type: 'experiment', working_folder: undefined }), /working_folder is required when dispatch_type is "experiment"/);
  expectReject('10i experiment remains blocked without a live owner', root,
    validDispatch({ dispatch_id: '2026-06-12-battery-experiment', dispatch_type: 'experiment' }), /has no live owner/);
  expectReject('10j review without output_mode rejected', root, validDispatch({ dispatch_id: '2026-06-12-battery-review-no-mode', dispatch_type: 'review' }), /output_mode is required when dispatch_type is "review"/);
  expectReject('10k inline review with working_folder rejected', root, validDispatch({ dispatch_id: '2026-06-12-battery-review-inline-folder', dispatch_type: 'review', output_mode: 'inline' }), /working_folder must be absent when review output_mode is "inline"/);
  const ri = run(root, validDispatch({ dispatch_id: '2026-06-12-battery-review-inline', dispatch_type: 'review', output_mode: 'inline', working_folder: undefined }));
  check('10l inline review without working_folder appends and emits output_mode', ri.status === 0 && /^    output_mode: "inline"$/m.test(readLedger(root)), ri.stderr || ri.stdout);
  expectReject('10m persisted review without working_folder rejected', root, validDispatch({ dispatch_id: '2026-06-12-battery-review-persisted-no-folder', dispatch_type: 'review', output_mode: 'persisted', working_folder: undefined }), /working_folder is required when review output_mode is "persisted"/);
  const rp = run(root, validDispatch({ dispatch_id: '2026-06-12-battery-review-persisted', dispatch_type: 'review', output_mode: 'persisted' }));
  check('10n persisted review with working_folder appends', rp.status === 0, rp.stderr || rp.stdout);
  expectReject('10o output_mode on non-review rejected', root, validDispatch({ dispatch_id: '2026-06-12-battery-research-mode', output_mode: 'persisted' }), /output_mode is allowed only when dispatch_type is "review"/);
}

console.log('\n[11] close rows');
{
  const root = freshRoot();
  run(root, validDispatch()); // seed the dispatch row
  const r1 = run(root, validClose());
  check('11a valid close row appends (exit 0)', r1.status === 0, r1.stderr || r1.stdout);
  const text = readLedger(root);
  check('11b close row block keys emitted', /^  - close_of: "2026-06-12-battery-main"$/m.test(text) && /^    exit_reason: "resolved"$/m.test(text) && /^    closed: "\d{4}/m.test(text), text);
  check('11c agents_spawned emitted as JSON column', /^    agents_spawned: \{"planned_total":3,"total":3,"not_launched":0,"tree":\{"explorer":2,"writer":1,"helpers":0\},"loops_used":1\}$/m.test(text), text);
  check('11d feedback_prompts emitted as JSON column', /^    feedback_prompts: \["Verbatim feedback ask sent back to the explorers\."\]$/m.test(text), text);
  expectReject('11e close row with unknown key rejected', root, validClose({ close_of: '2026-06-12-battery-second', bogus: 1 }), /unknown key "bogus" on a close record/);
  expectReject('11f close row with dispatch_id rejected', root, Object.assign(validClose(), { dispatch_id: 'x' }), /must use close_of, not dispatch_id/);
  expectReject('11g close row with caller-supplied closed rejected', root, validClose({ closed: '2026-01-01T00:00:00Z' }), /unknown key "closed"/);
  const r2 = run(root, validClose({ close_of: 'never-dispatched', feedback_prompts: undefined }));
  check('11h close without matching dispatch row is rejected and preserved',
    r2.status === 2 && r2.tempExists && /has no matching dispatch row/.test(r2.stderr), r2.stderr || r2.stdout);
  // self-check still passes over the emitted close rows
  const r3 = run(root, validDispatch({ dispatch_id: '2026-06-12-battery-after-close' }));
  check('11i ledger with close rows still passes self-check', r3.status === 0, r3.stderr || r3.stdout);
}

console.log('\n[12] idempotency');
{
  const root = freshRoot();
  run(root, validDispatch());
  const before = readLedger(root);
  const r1 = run(root, validDispatch());
  check('12a same dispatch_id is a no-op', r1.status === 0 && /already registered/.test(r1.stdout) && readLedger(root) === before, r1.stdout);
  run(root, validClose());
  const mid = readLedger(root);
  const r2 = run(root, validClose());
  check('12b same close_of is a no-op', r2.status === 0 && /already closed/.test(r2.stdout) && readLedger(root) === mid, r2.stdout);
  const dispatchMismatch = run(root, validDispatch({ goal: 'Different bytes under the same dispatch id.' }));
  check('12c same dispatch_id with different bytes is blocked and preserved',
    dispatchMismatch.status === 2 && dispatchMismatch.tempExists && /different sheet bytes/.test(dispatchMismatch.stderr), dispatchMismatch.stderr);
  const closeMismatch = run(root, validClose({ feedback_prompts: ['Different close evidence.'] }));
  check('12d same close_of with different content is blocked and preserved',
    closeMismatch.status === 2 && closeMismatch.tempExists && /different content/.test(closeMismatch.stderr), closeMismatch.stderr);
}

console.log('\n[13] grandfathering: old-shape rows pass the structural self-check');
{
  const root = freshRoot();
  const file = ledgerPath(root);
  fs.mkdirSync(path.dirname(file), { recursive: true });
  // a real OLD-shape row, exactly as the pre-v0.5.2 appender emitted it
  fs.writeFileSync(file,
    '# subagents-dispatch.yaml — registry of subagent dispatches (one row per dispatch).\n' +
    '# Written by the register-dispatch skill. `agents` and `anti_bias` are JSON columns.\n' +
    'dispatches:\n' +
    '  - dispatch_id: "repo-genesis-backbone"\n' +
    '    corpus: "research/audits"\n' +
    '    created: "2026-06-12T18:00:00.000Z"\n' +
    '    status: "dispatched"\n' +
    '    goal: "Identify the invariant skeleton every component must instantiate."\n' +
    '    success_metric: {"type":"exploratory"}\n' +
    '    max_loops: 1\n' +
    '    anti_bias:\n' +
    '      {\n' +
    '        "axis": "corpus",\n' +
    '        "pairs": ["Adamek (domainspec) vs Baez (arcanum)"],\n' +
    '      }\n' +
    '    agents:\n' +
    '      [\n' +
    '        {"seq":"00","layer":"L0","role":"explorer","model":"sonnet","mode":"single","name":"Abramsky, Samson","angle":"model-extraction"},\n' +
    '      ]\n');
  const r = run(root, validDispatch());
  check('13a append over an old-shape row succeeds (exit 0)', r.status === 0, r.stderr || r.stdout);
  const text = readLedger(root);
  check('13b old row untouched and new row appended', /repo-genesis-backbone/.test(text) && /battery-main/.test(text));
  const r2 = run(root, validClose({ close_of: 'repo-genesis-backbone', feedback_prompts: undefined }));
  check('13c old-shape row without topology cannot claim a semantic close',
    r2.status === 2 && /registered strategy agent count/.test(r2.stderr), r2.stderr || r2.stdout);
}

console.log('\n[14] invoked_by resolution');
{
  // (a) taken from record when present — already asserted in 1d; re-assert isolated:
  const rootA = freshRoot();
  run(rootA, validDispatch({ invoked_by: 'explicit@example.com' }));
  check('14a invoked_by from record wins', /^    invoked_by: "explicit@example\.com"$/m.test(readLedger(rootA)));

  const gitOk = spawnSync('git', ['--version'], { encoding: 'utf8' }).status === 0;
  // env that blinds git to global/system config, so only repo-local config counts
  function isolatedGitEnv(root) {
    const empty = path.join(root, 'empty-gitconfig');
    fs.writeFileSync(empty, '');
    return { GIT_CONFIG_GLOBAL: empty, GIT_CONFIG_SYSTEM: empty, GIT_CONFIG_NOSYSTEM: '1' };
  }
  if (!gitOk) {
    note('14b resolved from git config when absent', 'git unavailable on PATH');
    note('14c fail-soft null when neither', 'git unavailable on PATH');
  } else {
    // (b) absent from record -> resolved from the temp repo's git config user.email
    const rootB = freshRoot();
    const envB = isolatedGitEnv(rootB);
    spawnSync('git', ['init', '-q', rootB], { encoding: 'utf8', env: Object.assign({}, process.env, envB) });
    spawnSync('git', ['-C', rootB, 'config', 'user.email', 'battery@example.com'], { encoding: 'utf8', env: Object.assign({}, process.env, envB) });
    const rB = run(rootB, without(validDispatch(), 'invoked_by'), envB);
    check('14b resolved from git config user.email when absent',
      rB.status === 0 && /^    invoked_by: "battery@example\.com"$/m.test(readLedger(rootB)), rB.stderr || readLedger(rootB));
    // (c) absent from record, no repo, no global config -> warning + null
    const rootC = freshRoot();
    const envC = isolatedGitEnv(rootC);
    const rC = run(rootC, without(validDispatch(), 'invoked_by'), envC);
    check('14c fail-soft: warning emitted and invoked_by null',
      rC.status === 0 && /warning: invoked_by not in record/.test(rC.stdout) && /^    invoked_by: null$/m.test(readLedger(rootC)),
      rC.stderr || rC.stdout + '\n' + readLedger(rootC));
  }
}

console.log('\n[15] corrupt ledger refused (exit 1)');
{
  const root = freshRoot();
  const file = ledgerPath(root);
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, 'dispatches:\n  - dispatch_id: "ok-row"\n    goal: not-valid-json\n');
  const r = run(root, validDispatch());
  check('15 structurally corrupt ledger refused with exit 1', r.status === 1 && /ledger structural check failed/.test(r.stderr), `exit=${r.status} stderr=${r.stderr.trim()}`);
}

console.log('\n[16] anti_bias_global conditional (>= 2 fan-out groups) enforced');
{
  const root = freshRoot();
  expectReject('16a two fan-out groups without anti_bias_global', root,
    without(twoFanout(), 'anti_bias_global'), /anti_bias_global is required when >= 2 groups have >= 2 agents/);
  const r1 = run(root, twoFanout());
  check('16b two fan-out groups with anti_bias_global appends (exit 0)', r1.status === 0, r1.stderr || r1.stdout);
  const r2 = run(root, without(validDispatch({ dispatch_id: '2026-06-12-battery-one-fanout' }), 'anti_bias_global'));
  check('16c one fan-out group without anti_bias_global appends (exit 0)', r2.status === 0, r2.stderr || r2.stdout);
  // 16d: the conditional counts GROUPS WITH >= 2 AGENTS, not groups.length —
  // one fan-out group + three singletons must not trigger it.
  const manySingletons = without(validDispatch({ dispatch_id: '2026-06-12-battery-many-singletons' }), 'anti_bias_global');
  const singletonIdentities = ['Mac Lane, Saunders', 'Turing, Alan', 'Spivak, David'];
  for (let i = 0; i < singletonIdentities.length; i++) {
    const id = `solo-${i}`;
    const agentName = singletonIdentities[i];
    manySingletons.groups.push({ group_id: id,
      agents: [{ agent_name: agentName, role: 'writer', model: 'claude-opus-4-8', token_budget: 1,
        initial_prompt: `You are ${agentName}.\n\nWrite the bounded return.` }] });
  }
  const r3 = run(root, manySingletons);
  check('16d one fan-out + three singleton groups without anti_bias_global appends (exit 0)', r3.status === 0, r3.stderr || r3.stdout);
  // 16e: a malformed sibling group must not crash or spuriously fire the conditional —
  // expect a clean exit 2 on the agents-array error, with NO anti_bias_global error.
  const malformedSibling = without(validDispatch({ dispatch_id: '2026-06-12-battery-malformed-sibling' }), 'anti_bias_global');
  malformedSibling.groups.push({ group_id: 'broken', agents: 'broken' });
  const r4 = run(root, malformedSibling);
  check('16e malformed sibling group: clean exit 2 on agents error, no spurious anti_bias_global error',
    r4.status === 2 && /agents is required and must be a non-empty array/.test(r4.stderr) && !/anti_bias_global/.test(r4.stderr),
    `exit=${r4.status}\nstderr=${r4.stderr.trim()}`);
}

console.log('\n[17] temporary-record consumption is safe and failure-preserving');
{
  const root = freshRoot();
  const invalid = run(root, without(validDispatch(), 'goal'));
  check('17a invalid temporary record is preserved for diagnosis',
    invalid.status === 2 && invalid.tempExists === true,
    `exit=${invalid.status} stdout=${invalid.stdout} stderr=${invalid.stderr}`);

  const outside = path.join(root, 'outside.tmp.json');
  fs.writeFileSync(outside, JSON.stringify(validDispatch()));
  const env = Object.assign({}, process.env, { ARCANUM_PROJECT_DIR: root });
  const result = spawnSync(process.execPath, [APPENDER, '--consume', outside], { env, encoding: 'utf8' });
  check('17b --consume refuses a path outside the governed runtime temp root',
    result.status === 2 && fs.existsSync(outside) && /requires a \*\.tmp\.json file below/.test(result.stderr),
    `exit=${result.status} stdout=${result.stdout} stderr=${result.stderr}`);

  const checkRoot = freshRoot();
  const checkTempRoot = path.join(checkRoot, '.arcanum', 'runtime', 'subagents-strategy');
  fs.mkdirSync(checkTempRoot, { recursive: true });
  const checkTemp = path.join(checkTempRoot, 'check.tmp.json');
  fs.writeFileSync(checkTemp, JSON.stringify(validDispatch()));
  const checkEnv = Object.assign({}, process.env, { ARCANUM_PROJECT_DIR: checkRoot });
  const checked = spawnSync(process.execPath, [APPENDER, '--check', checkTemp], { env: checkEnv, encoding: 'utf8' });
  check('17c --check validates without ledger mutation or temp consumption',
    checked.status === 0 && fs.existsSync(checkTemp) && !fs.existsSync(ledgerPath(checkRoot)) &&
      /"mode":"confirmation-readiness"/.test(checked.stdout) && /"sheet_sha256":"[a-f0-9]{64}"/.test(checked.stdout),
    `exit=${checked.status} stdout=${checked.stdout} stderr=${checked.stderr}`);
}

console.log('\n[18] traversal and semantic close hardening');
{
  const root = freshRoot();
  expectReject('18a parent traversal in working_folder is rejected', root,
    validDispatch({ working_folder: 'research/../outside/' }), /parent traversal/);
  expectReject('18b absolute Windows working_folder is rejected', root,
    validDispatch({ working_folder: 'C:\\outside' }), /portable forward slashes|project-relative/);
  run(root, validDispatch());
  expectReject('18c close planned total must match registered topology', root,
    validClose({ agents_spawned: validSpawn({ planned_total: 2, total: 2, tree: { explorer: 1, writer: 1 }, loops_used: 0 }) }), /registered strategy agent count/);
  expectReject('18d close tree must sum to total', root,
    validClose({ agents_spawned: validSpawn({ tree: { explorer: 1, writer: 1 }, loops_used: 0 }) }), /sum exactly/);
  expectReject('18e close loop count cannot exceed registered max_loops', root,
    validClose({ agents_spawned: validSpawn({ loops_used: 3 }) }), /exceeds registered max_loops/);
  const linkRoot = freshRoot();
  const outsideRoot = freshRoot();
  fs.mkdirSync(path.join(linkRoot, '.arcanum'), { recursive: true });
  try {
    fs.symlinkSync(outsideRoot, path.join(linkRoot, '.arcanum', 'observability'), process.platform === 'win32' ? 'junction' : 'dir');
    const escaped = run(linkRoot, validDispatch({ dispatch_id: 'junction-escape' }));
    check('18f ledger junction/symlink escape is blocked',
      escaped.status === 2 && escaped.tempExists && /escapes the real project root/.test(escaped.stderr), escaped.stderr);
  } catch (error) {
    note('18f ledger junction/symlink escape is blocked', `link creation unavailable: ${error.code || error.message}`);
  }
}

// ---------------------------------------------------------------- summary
for (const d of roots) { try { fs.rmSync(d, { recursive: true, force: true }); } catch (_) { /* best effort */ } }
console.log(`\n${pass} passed, ${fail} failed, ${skip} skipped`);
if (failures.length) { console.log('failing cases:\n  - ' + failures.join('\n  - ')); process.exit(1); }
process.exit(0);
