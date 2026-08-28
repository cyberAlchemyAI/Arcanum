#!/usr/bin/env node
'use strict';
/*
 * Append one row to
 * <repo-root>/.arcanum/observability/subagents-strategy/subagents-dispatch.yaml.
 *
 *   node append-dispatch.cjs [--check | --schema-check | --consume] <record.tmp.json>
 *
 * <record.json> is a UTF-8 JSON file (a file arg, not stdin, so shell encoding
 * — e.g. PowerShell's UTF-16 pipes — can't corrupt the payload).
 *
 * SCHEMA — subagents-strategy schema v0.7.0 (`agent_name` and the exact
 * identity-prefixed `initial_prompt` became mandatory; `output_mode` was added
 * for review at v0.6.1 and group `role` was removed at v0.6.0). Two row kinds,
 * both appended by this script
 * (two appends, one place):
 *
 *   DISPATCH ROW — keyed by `dispatch_id`. Required: dispatch_id,
 *     schema_version ("0.7.0" exactly), dispatch_type
 *     (research|code|review|plan|suggestion|experiment), goal, context, max_loops (1..5),
 *     final_approver, groups[] (each group: group_id, agents[] — NO group
 *     `role` field; each agent: agent_name, role
 *     explorer|synthesizer|skeptic|writer|auditor, model, token_budget,
 *     initial_prompt beginning with `You are {agent_name}.`). Optional: meta (true), parent_dispatch_id,
 *     anti_bias_global, working_folder (REQUIRED for LIVE types research/review/experiment; never vault/),
 *     invoked_by (tooling extension, not part of the core schema),
 *     connections[] ({from,to,type,loop_cap?}).
 *   CLOSE ROW — keyed by `close_of`. Required: exit_reason
 *     (resolved|loop_ceiling_reached|dissent_irreconcilable|user_abort|error)
 *     and agents_spawned ({planned_total, total, not_launched, tree,
 *     loops_used}). `total` is the number actually launched; `tree` sums to
 *     `total`; `total + not_launched` equals `planned_total`. Optional:
 *     feedback_prompts[] (verbatim feedback-edge asks),
 *     invoked_by (tooling extension, not part of the core schema).
 *
 * NOT ENFORCED here (deliberate — sheet-design rules owned by the strategist
 * and the human confirm gate): dispatch_id YYYY-MM-DD-<slug> format;
 * no-self-approval (final_approver never a working-group member); the
 * layers>1 not-on-a-zig-zag/feedback-endpoint corollary; the semantic
 * four-test anti-bias decision rule (axis vocabulary /
 * clone / spread / evidence — gate-checked on the sheet). The anti_bias_global
 * required-when->=2-groups-fan-out conditional IS enforced here (2026-06-12
 * in-place amendment).
 *
 * `created`/`closed` are STAMPED by the appender (never supplied by the
 * caller). `invoked_by` is taken from the record when present, otherwise
 * resolved via `git config user.email` (fail-soft: warning + null).
 * `project_dir` is a control key (repo-root fallback), never emitted.
 *
 * VALIDATION SPLIT (grandfathering):
 *   - The INCOMING record is validated STRICTLY against the v0.7.0 schema
 *     before append: required fields, closed enums, conditional fields
 *     (working_folder on research; anti_bias/angle at n >= 2;
 *     anti_bias_global when >= 2 groups have >= 2 agents; n ==
 *     agents.length; loop_cap only on zig-zag/feedback; connection endpoints
 *     declared), and unknown-key rejection — keys in the removed
 *     table (success_metric, constraints, created) get a removed-by-v0.5.2
 *     error; old ledger-row-only keys (status, top-level anti_bias, top-level
 *     agents, corpus, topic_slug, session) get a pre-v0.5.2-ledger-row error.
 *     Exit 2.
 *   - The EXISTING ledger passes only the STRUCTURAL SELF-CHECK below
 *     (zero-dep, line-based — the file is machine-written in a known shape):
 *     every non-comment line is the `dispatches:` key, a `  - key: <json>`
 *     row start, or a `    key: <json>` continuation; every value parses as
 *     JSON; rows start with dispatch_id or close_of; ids are unique. Rows
 *     written under pre-v0.5.2 schemas are grandfathered historical artifacts
 *     and are NEVER re-validated semantically — old keys keep passing. On
 *     structural corruption the appender refuses to append (exit 1) so
 *     corruption surfaces at the next write instead of accumulating silently.
 *
 * Emission style: scalar fields as block keys; `groups`/`connections`
 * (dispatch row) and `agents_spawned`/`feedback_prompts` (close row) as JSON
 * flow values ("JSON columns") — valid YAML, appendable with no YAML parser;
 * JSON.stringify escapes the newlines inside initial_prompt, which is the
 * point. Idempotent: a dispatch_id/close_of already present is a no-op.
 *
 * With --consume, the input is deleted after a successful append or idempotent
 * no-op. Consumption is allowed only for *.tmp.json files below
 * <repo-root>/.arcanum/runtime/subagents-strategy/. Invalid records and failed
 * appends remain available for diagnosis.
 *
 * The registry is APPEND-ONLY: a dispatch row is never edited after the fact;
 * closing a dispatch is the appended close row, never an edit.
 */
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { execFileSync, execSync } = require('child_process');

const args = process.argv.slice(2);
const consume = args.includes('--consume');
const checkOnly = args.includes('--check');
const schemaCheckOnly = args.includes('--schema-check');
const positional = args.filter((arg) => !['--consume', '--check', '--schema-check'].includes(arg));
if (positional.length !== 1 || [consume, checkOnly, schemaCheckOnly].filter(Boolean).length !== 1) {
  console.error('usage: node append-dispatch.cjs [--check | --schema-check | --consume] <record.tmp.json>');
  process.exit(2);
}
const src = path.resolve(positional[0]);

let rec;
let sourceBytes;
try {
  sourceBytes = fs.readFileSync(src);
  rec = JSON.parse(sourceBytes.toString('utf8').replace(/^\uFEFF/, ''));
} // strip UTF-8 BOM
catch (e) { console.error('cannot read/parse record:', e.message); process.exit(2); }
if (rec === null || typeof rec !== 'object' || Array.isArray(rec)) {
  console.error('record must be a JSON object'); process.exit(2);
}

const J = (v) => JSON.stringify(v);   // valid YAML scalar / flow value
const isStr = (v) => typeof v === 'string';
const isNonEmptyStr = (v) => isStr(v) && v.trim() !== '';
const isObj = (v) => v !== null && typeof v === 'object' && !Array.isArray(v);

// ---------------------------------------------------------------- schema
const SCHEMA_VERSION = '0.7.0';   // mandatory pool identity and exact prompt prefix
const DISPATCH_TYPES = ['research', 'code', 'review', 'plan', 'suggestion', 'experiment'];
// LIVE (review 2026-06-12; experiment 2026-06-14, owner decisions); others
// RESERVED (code, plan, suggestion) — recorded but not yet dispatchable.
// Group `role` was removed from the row schema at v0.6.0: a group's
// function is read off its agents' roles, its workflow position off its connections.
const AGENT_ROLES = ['explorer', 'synthesizer', 'skeptic', 'writer', 'auditor'];
const CONNECTION_TYPES = ['sequential', 'zig-zag', 'feedback'];
const OUTPUT_MODES = ['inline', 'persisted'];
const EXIT_REASONS = ['resolved', 'loop_ceiling_reached', 'dissent_irreconcilable', 'user_abort', 'error'];

const DISPATCH_KEYS = new Set([
  'dispatch_id', 'schema_version', 'dispatch_type', 'goal', 'context',
  'max_loops', 'final_approver', 'groups',                       // required
  'meta', 'parent_dispatch_id', 'anti_bias_global', 'output_mode', 'working_folder',
  'invoked_by', 'connections', 'execution_projection_sha256',    // optional
  'project_dir',                                                 // control key, not emitted
]);
const CLOSE_KEYS = new Set([
  'close_of', 'exit_reason', 'agents_spawned',                   // required
  'feedback_prompts', 'invoked_by',                              // optional
  'project_dir',                                                 // control key, not emitted
]);
// Keys in the removed table — rejected with an explicit
// removed-by-v0.5.2 message. (`created`/`closed` are stamped by the appender,
// never caller-supplied.)
const REMOVED_KEYS = new Set(['success_metric', 'constraints', 'created']);
// Old ledger-row-only keys (pre-v0.5.2 ledger format; not in the removed
// table — e.g. `anti_bias`/`agents` live at group level in v0.5.2, never top
// level). Rejected with a pre-v0.5.2-ledger-row message.
const LEGACY_LEDGER_KEYS = new Set([
  'status', 'anti_bias', 'agents', 'corpus', 'topic_slug', 'session',
]);
const GROUP_KEYS = new Set(['group_id', 'agents', 'n', 'robot_talks', 'layers', 'anti_bias', 'predicted_disagreements']);
const AGENT_KEYS = new Set(['role', 'model', 'token_budget', 'initial_prompt', 'agent_name', 'angle']);
const CONN_KEYS = new Set(['from', 'to', 'type', 'loop_cap']);
const SPAWN_KEYS = new Set(['planned_total', 'total', 'not_launched', 'tree', 'loops_used']);

function validateDispatch(rec) {
  const errs = [];
  for (const k of Object.keys(rec)) {
    if (DISPATCH_KEYS.has(k)) continue;
    if (REMOVED_KEYS.has(k)) errs.push(`"${k}" was removed by schema v0.5.2 — drop it from the record`);
    else if (LEGACY_LEDGER_KEYS.has(k)) errs.push(`"${k}" is a pre-v0.5.2 ledger-row key, not in the v0.5.2 schema — drop it from the record`);
    else errs.push(`unknown key "${k}" on a dispatch record`);
  }
  if (!isNonEmptyStr(rec.dispatch_id)) errs.push('dispatch_id is required and must be a non-empty string');
  if (rec.schema_version !== SCHEMA_VERSION) errs.push(`schema_version must be exactly "${SCHEMA_VERSION}" (got ${J(rec.schema_version)})`);
  if (!DISPATCH_TYPES.includes(rec.dispatch_type)) errs.push(`dispatch_type must be one of ${DISPATCH_TYPES.join(' | ')} (got ${J(rec.dispatch_type)})`);
  if (!isNonEmptyStr(rec.goal)) errs.push('goal is required and must be a non-empty string');
  if (!isNonEmptyStr(rec.context)) errs.push('context is required and must be a non-empty string (subagents never see the parent conversation)');
  if (!Number.isInteger(rec.max_loops) || rec.max_loops < 1 || rec.max_loops > 5) errs.push(`max_loops must be an integer in 1..5 (got ${J(rec.max_loops)})`);
  if (!isNonEmptyStr(rec.final_approver)) errs.push('final_approver is required and must be a non-empty string');
  if (rec.meta !== undefined && rec.meta !== true) errs.push('meta, when present, must be boolean true (omit it otherwise)');
  if (rec.parent_dispatch_id !== undefined && rec.parent_dispatch_id !== null && !isNonEmptyStr(rec.parent_dispatch_id)) errs.push('parent_dispatch_id must be a non-empty string (or null / omitted)');
  if (rec.anti_bias_global !== undefined && !isNonEmptyStr(rec.anti_bias_global)) errs.push('anti_bias_global, when present, must be a non-empty string');
  if (rec.invoked_by !== undefined && !isNonEmptyStr(rec.invoked_by)) errs.push('invoked_by, when present, must be a non-empty string (email)');
  if (rec.project_dir !== undefined && !isNonEmptyStr(rec.project_dir)) errs.push('project_dir, when present, must be a non-empty string');
  if (rec.execution_projection_sha256 !== undefined &&
      (!isStr(rec.execution_projection_sha256) || !/^[a-f0-9]{64}$/.test(rec.execution_projection_sha256))) {
    errs.push('execution_projection_sha256, when present, must be a lowercase SHA-256');
  }

  if (rec.dispatch_type === 'review') {
    if (!OUTPUT_MODES.includes(rec.output_mode)) {
      errs.push(`output_mode is required when dispatch_type is "review" and must be one of ${OUTPUT_MODES.join(' | ')} (got ${J(rec.output_mode)})`);
    } else if (rec.output_mode === 'inline' && rec.working_folder !== undefined) {
      errs.push('working_folder must be absent when review output_mode is "inline"');
    } else if (rec.output_mode === 'persisted' && rec.working_folder === undefined) {
      errs.push('working_folder is required when review output_mode is "persisted"');
    }
  } else {
    if (rec.output_mode !== undefined) errs.push('output_mode is allowed only when dispatch_type is "review"');
    if ((rec.dispatch_type === 'research' || rec.dispatch_type === 'experiment') && rec.working_folder === undefined) {
      errs.push(`working_folder is required when dispatch_type is "${rec.dispatch_type}"`);
    }
  }
  if (rec.working_folder !== undefined) {
    if (!isNonEmptyStr(rec.working_folder)) errs.push('working_folder must be a non-empty string');
    else {
      // Normalize before the vault guard: strip leading "./" / ".\", match
      // case-insensitively, and reject bare "vault" as well as vault/ prefixes.
      const raw = rec.working_folder;
      const portable = raw.split('\\').join('/');
      const segments = portable.split('/');
      if (raw.includes('\\')) errs.push('working_folder must use portable forward slashes');
      if (path.posix.isAbsolute(portable) || path.win32.isAbsolute(raw) || /^[A-Za-z]:/.test(raw)) {
        errs.push('working_folder must be project-relative, never absolute');
      }
      if (segments.includes('..')) errs.push('working_folder must not contain parent traversal (..)');
      const normalized = path.posix.normalize(portable.replace(/^\.\//, ''));
      if (/^vault(?:\/|$)/i.test(normalized)) errs.push(`working_folder must never point into vault/ ("Never vault/**") — got ${J(rec.working_folder)}`);
    }
  }

  const groupIds = new Set();
  if (!Array.isArray(rec.groups) || rec.groups.length === 0) {
    errs.push('groups is required and must be a non-empty array');
  } else {
    rec.groups.forEach((g, gi) => {
      const gw = `groups[${gi}]`;
      if (!isObj(g)) { errs.push(`${gw} must be an object`); return; }
      for (const k of Object.keys(g)) if (!GROUP_KEYS.has(k)) errs.push(`${gw}: unknown key "${k}"`);
      if (!isNonEmptyStr(g.group_id)) errs.push(`${gw}.group_id is required and must be a non-empty string`);
      else if (groupIds.has(g.group_id)) errs.push(`${gw}.group_id ${J(g.group_id)} duplicates an earlier group — group ids must be unique`);
      else groupIds.add(g.group_id);
      const agents = Array.isArray(g.agents) && g.agents.length > 0 ? g.agents : null;
      if (!agents) errs.push(`${gw}.agents is required and must be a non-empty array`);
      if (g.n !== undefined) {
        if (!Number.isInteger(g.n) || g.n < 1) errs.push(`${gw}.n must be an integer >= 1 (got ${J(g.n)})`);
        else if (agents && g.n !== agents.length) errs.push(`${gw}.n (${g.n}) must equal agents.length (${agents.length})`);
      }
      if (g.robot_talks !== undefined && typeof g.robot_talks !== 'boolean') errs.push(`${gw}.robot_talks must be a boolean`);
      if (g.layers !== undefined && (!Number.isInteger(g.layers) || g.layers < 1)) errs.push(`${gw}.layers must be an integer >= 1 (got ${J(g.layers)})`);
      const fanout = agents !== null && agents.length >= 2;
      if (fanout && !isNonEmptyStr(g.anti_bias)) errs.push(`${gw}.anti_bias is required when the group has >= 2 agents`);
      if (fanout && !Array.isArray(g.predicted_disagreements)) errs.push(`${gw}.predicted_disagreements is required when the group has >= 2 agents`);
      if (!fanout && g.anti_bias !== undefined && !isNonEmptyStr(g.anti_bias)) errs.push(`${gw}.anti_bias, when present, must be a non-empty string`);
      if (agents) agents.forEach((a, ai) => {
        const aw = `${gw}.agents[${ai}]`;
        if (!isObj(a)) { errs.push(`${aw} must be an object`); return; }
        for (const k of Object.keys(a)) if (!AGENT_KEYS.has(k)) errs.push(`${aw}: unknown key "${k}"`);
        if (!AGENT_ROLES.includes(a.role)) errs.push(`${aw}.role must be one of ${AGENT_ROLES.join(' | ')} (got ${J(a.role)})`);
        if (!isNonEmptyStr(a.model)) errs.push(`${aw}.model is required and must be a non-empty string`);
        if (!Number.isInteger(a.token_budget) || a.token_budget <= 0) errs.push(`${aw}.token_budget is required and must be a positive integer — no unlimited default`);
        if (!isNonEmptyStr(a.initial_prompt)) errs.push(`${aw}.initial_prompt is required and must be a non-empty string`);
        if (!isNonEmptyStr(a.agent_name)) {
          errs.push(`${aw}.agent_name is required and must be a non-empty string`);
        } else if (isNonEmptyStr(a.initial_prompt)) {
          const identityPrefix = `You are ${a.agent_name}.`;
          const instructionBody = a.initial_prompt.startsWith(identityPrefix + '\n\n')
            ? a.initial_prompt.slice(identityPrefix.length + 2).trim()
            : '';
          if (!instructionBody) {
            errs.push(`${aw}.initial_prompt must start exactly with ${J(identityPrefix)} followed by a blank line`);
          }
        }
        if (fanout && !isNonEmptyStr(a.angle)) errs.push(`${aw}.angle is required when the group has >= 2 agents`);
        if (!fanout && a.angle !== undefined && !isNonEmptyStr(a.angle)) errs.push(`${aw}.angle, when present, must be a non-empty string`);
      });
    });
    const fanoutGroups = rec.groups.filter((g) => isObj(g) && Array.isArray(g.agents) && g.agents.length >= 2).length;
    if (fanoutGroups >= 2 && !isNonEmptyStr(rec.anti_bias_global)) {
      errs.push(`anti_bias_global is required when >= 2 groups have >= 2 agents (${fanoutGroups} fan-out groups declared)`);
    }
  }

  if (rec.connections !== undefined) {
    if (!Array.isArray(rec.connections)) errs.push('connections must be an array of {from, to, type, loop_cap?}');
    else rec.connections.forEach((c, ci) => {
      const cw = `connections[${ci}]`;
      if (!isObj(c)) { errs.push(`${cw} must be an object`); return; }
      for (const k of Object.keys(c)) if (!CONN_KEYS.has(k)) errs.push(`${cw}: unknown key "${k}" — connections are exactly {from, to, type, loop_cap?}`);
      for (const end of ['from', 'to']) {
        if (!isNonEmptyStr(c[end])) errs.push(`${cw}.${end} is required and must be a group_id string`);
        else if (!groupIds.has(c[end])) errs.push(`${cw}.${end} ${J(c[end])} does not reference a declared group_id`);
      }
      if (!CONNECTION_TYPES.includes(c.type)) errs.push(`${cw}.type must be one of ${CONNECTION_TYPES.join(' | ')} (got ${J(c.type)})`);
      if (c.loop_cap !== undefined) {
        if (c.type === 'sequential') errs.push(`${cw}: loop_cap must be ABSENT on a sequential connection`);
        else if (!Number.isInteger(c.loop_cap) || c.loop_cap <= 0) errs.push(`${cw}.loop_cap must be a positive integer (got ${J(c.loop_cap)})`);
      }
    });
  }
  return errs;
}

function validateClose(rec) {
  const errs = [];
  if (rec.dispatch_id !== undefined) errs.push('a close record must use close_of, not dispatch_id');
  for (const k of Object.keys(rec)) {
    if (k === 'dispatch_id' || CLOSE_KEYS.has(k)) continue;
    if (REMOVED_KEYS.has(k)) errs.push(`"${k}" was removed by schema v0.5.2 — drop it from the record`);
    else if (LEGACY_LEDGER_KEYS.has(k)) errs.push(`"${k}" is a pre-v0.5.2 ledger-row key, not in the v0.5.2 schema — drop it from the record`);
    else errs.push(`unknown key "${k}" on a close record`);
  }
  if (!isNonEmptyStr(rec.close_of)) errs.push('close_of must be a non-empty string');
  if (!EXIT_REASONS.includes(rec.exit_reason)) errs.push(`exit_reason must be one of ${EXIT_REASONS.join(' | ')} (got ${J(rec.exit_reason)})`);
  const s = rec.agents_spawned;
  if (!isObj(s)) {
    errs.push('agents_spawned is required and must be an object: {planned_total, total, not_launched, tree, loops_used}');
  } else {
    for (const k of Object.keys(s)) if (!SPAWN_KEYS.has(k)) errs.push(`agents_spawned: unknown key "${k}"`);
    if (!Number.isInteger(s.planned_total) || s.planned_total < 0) errs.push('agents_spawned.planned_total must be a non-negative integer');
    if (!Number.isInteger(s.total) || s.total < 0) errs.push('agents_spawned.total must be a non-negative integer');
    if (!Number.isInteger(s.not_launched) || s.not_launched < 0) errs.push('agents_spawned.not_launched must be a non-negative integer');
    if (!isObj(s.tree)) errs.push('agents_spawned.tree must be an object (keyed by role-category, helpers in their own bucket)');
    else {
      const counts = Object.values(s.tree);
      if (counts.some((value) => !Number.isInteger(value) || value < 0)) {
        errs.push('every agents_spawned.tree count must be a non-negative integer');
      } else if (Number.isInteger(s.total) && counts.reduce((sum, value) => sum + value, 0) !== s.total) {
        errs.push('agents_spawned.tree counts must sum exactly to agents_spawned.total');
      }
    }
    if (!Number.isInteger(s.loops_used) || s.loops_used < 0) errs.push('agents_spawned.loops_used is required and must be a non-negative integer (loop iterations used are a component of agents_spawned)');
    if (Number.isInteger(s.planned_total) && Number.isInteger(s.total) && Number.isInteger(s.not_launched) &&
        s.total + s.not_launched !== s.planned_total) {
      errs.push('agents_spawned.total + agents_spawned.not_launched must equal agents_spawned.planned_total');
    }
  }
  if (rec.feedback_prompts !== undefined &&
      (!Array.isArray(rec.feedback_prompts) || rec.feedback_prompts.some((p) => !isStr(p)))) {
    errs.push('feedback_prompts must be an array of strings (the verbatim feedback-edge asks)');
  }
  if (rec.invoked_by !== undefined && !isNonEmptyStr(rec.invoked_by)) errs.push('invoked_by, when present, must be a non-empty string (email)');
  if (rec.project_dir !== undefined && !isNonEmptyStr(rec.project_dir)) errs.push('project_dir, when present, must be a non-empty string');
  return errs;
}

// A record is either a dispatch row (`dispatch_id` + groups) or a close row
// (`close_of` + exit_reason + agents_spawned). Close rows exist because the
// registry is append-only: the original row is never updated on close.
const isClose = rec.close_of != null;
const errs = isClose ? validateClose(rec) : validateDispatch(rec);
if (errs.length > 0) {
  console.error(`invalid ${isClose ? 'close' : 'dispatch'} record (schema v${SCHEMA_VERSION}):`);
  for (const e of errs) console.error('  - ' + e);
  process.exit(2);
}

const projectDir = path.resolve(
  process.env.ARCANUM_PROJECT_DIR ||
  process.env.CODEX_PROJECT_DIR ||
  process.env.CLAUDE_PROJECT_DIR ||
  rec.project_dir ||
  process.cwd()
);
const file = path.join(
  projectDir,
  '.arcanum',
  'observability',
  'subagents-strategy',
  'subagents-dispatch.yaml'
);
const sheetSha256 = crypto.createHash('sha256').update(sourceBytes).digest('hex');

function assertConsumableSource() {
  if (!consume) return;
  const tempRoot = path.join(projectDir, '.arcanum', 'runtime', 'subagents-strategy');
  const relative = path.relative(tempRoot, src);
  const outside = relative === '..' || relative.startsWith('..' + path.sep) || path.isAbsolute(relative);
  if (outside || !src.endsWith('.tmp.json')) {
    console.error('--consume requires a *.tmp.json file below ' + tempRoot);
    process.exit(2);
  }
}

function consumeSource() {
  if (!consume) return;
  fs.unlinkSync(src);
  console.log('consumed temporary record', src);
}

assertConsumableSource();

if (schemaCheckOnly) {
  console.log(JSON.stringify({
    status: 'pass',
    mode: 'schema-check',
    record_kind: isClose ? 'close' : 'dispatch',
    schema_version: SCHEMA_VERSION,
    sheet_sha256: sheetSha256,
    ledger: file,
  }));
  process.exit(0);
}

if (checkOnly || (consume && !isClose)) {
  const readiness = path.join(__dirname, 'validate-readiness.cjs');
  try {
    const output = execFileSync(process.execPath, [readiness, src], {
      cwd: projectDir,
      env: Object.assign({}, process.env, { ARCANUM_PROJECT_DIR: projectDir }),
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'pipe'],
    });
    if (checkOnly) process.stdout.write(output);
  } catch (error) {
    if (error.stdout) process.stdout.write(String(error.stdout));
    if (error.stderr) process.stderr.write(String(error.stderr));
    process.exit(Number.isInteger(error.status) ? error.status : 2);
  }
  if (checkOnly) process.exit(0);
}

// invoked_by: record value wins; otherwise resolve from git; fail-soft to null.
function resolveInvokedBy() {
  if (rec.invoked_by !== undefined) return rec.invoked_by;
  try {
    const email = execSync('git config user.email', { cwd: projectDir, stdio: ['ignore', 'pipe', 'ignore'] })
      .toString('utf8').trim();
    if (email) return email;
  } catch (_) { /* fall through */ }
  console.log('warning: invoked_by not in record and `git config user.email` unavailable — recording invoked_by: null.');
  return null;
}

const header =
  '# subagents-dispatch.yaml — Arcanum registry of subagent dispatches (one row per dispatch,\n' +
  '# plus one close row per dispatch — append-only, never edited in place).\n' +
  '# Written by the Subagent Strategy registrar. `groups`/`connections` (dispatch rows) and\n' +
  '# `agents_spawned`/`feedback_prompts` (close rows) are JSON columns.\n' +
  'dispatches:\n';

class RegistrationError extends Error {
  constructor(message, code = 2) { super(message); this.code = code; }
}

function isWithin(root, target) {
  const relative = path.relative(root, target);
  return relative === '' || (!relative.startsWith('..' + path.sep) && relative !== '..' && !path.isAbsolute(relative));
}

function nearestExisting(candidate) {
  let current = path.resolve(candidate);
  while (!fs.existsSync(current)) {
    const parent = path.dirname(current);
    if (parent === current) break;
    current = parent;
  }
  return current;
}

function assertGovernedPaths() {
  const realProject = fs.realpathSync(projectDir);
  const ledgerParent = path.dirname(file);
  const existingParent = fs.realpathSync(nearestExisting(ledgerParent));
  if (!isWithin(realProject, existingParent)) throw new RegistrationError('ledger path escapes the real project root through a symlink or junction');
  fs.mkdirSync(ledgerParent, { recursive: true });
  if (!isWithin(realProject, fs.realpathSync(ledgerParent))) throw new RegistrationError('ledger directory resolves outside the real project root');

  if (consume) {
    const tempRoot = path.join(projectDir, '.arcanum', 'runtime', 'subagents-strategy');
    fs.mkdirSync(tempRoot, { recursive: true });
    if (!isWithin(fs.realpathSync(tempRoot), fs.realpathSync(src))) {
      throw new RegistrationError('temporary record resolves outside its governed runtime root');
    }
  }
}

const sleepCell = new Int32Array(new SharedArrayBuffer(4));
const lockPath = file + '.lock';
let lockOwned = false;
function processAlive(pid) {
  if (!Number.isInteger(pid) || pid <= 0) return false;
  try { process.kill(pid, 0); return true; } catch (error) { return error.code === 'EPERM'; }
}
function acquireLock() {
  const deadline = Date.now() + 15000;
  while (Date.now() < deadline) {
    try {
      const fd = fs.openSync(lockPath, 'wx');
      fs.writeFileSync(fd, JSON.stringify({ pid: process.pid, created_at: new Date().toISOString() }));
      fs.closeSync(fd);
      lockOwned = true;
      return;
    } catch (error) {
      if (error.code !== 'EEXIST') throw error;
      try {
        const stat = fs.statSync(lockPath);
        const lock = JSON.parse(fs.readFileSync(lockPath, 'utf8'));
        if (Date.now() - stat.mtimeMs > 30000 && !processAlive(lock.pid)) {
          fs.unlinkSync(lockPath);
          continue;
        }
      } catch (_) { /* another process may be replacing a stale lock */ }
      Atomics.wait(sleepCell, 0, 0, 25);
    }
  }
  throw new RegistrationError(`timed out acquiring ledger lock ${lockPath}`, 1);
}
function releaseLock() {
  if (!lockOwned) return;
  lockOwned = false;
  try { fs.unlinkSync(lockPath); } catch (_) { /* already gone */ }
}
process.once('exit', releaseLock);

function appendDurably(text) {
  const fd = fs.openSync(file, 'a');
  try { fs.writeSync(fd, text, null, 'utf8'); fs.fsyncSync(fd); }
  finally { fs.closeSync(fd); }
}

function checkLedger(text) {
  const dispatchRows = new Map(), closeRows = new Map(), rows = [];
  const fail = (n, why) => { throw new RegistrationError(`ledger structural check failed at ${file}:${n}: ${why}`, 1); };
  const sourceLines = text.split('\n');
  let sawTop = false, current = null;
  for (let i = 0; i < sourceLines.length; i++) {
    const line = sourceLines[i].replace(/\r$/, '');
    if (line === '' || line.startsWith('#')) continue;
    if (line === 'dispatches:') {
      if (sawTop) fail(i + 1, 'duplicate "dispatches:" key');
      sawTop = true; continue;
    }
    const match = /^(  - |    )([A-Za-z_][A-Za-z0-9_]*):(?: (.*))?$/.exec(line);
    if (!match) fail(i + 1, 'unrecognized line shape');
    if (!sawTop) fail(i + 1, 'row content before the "dispatches:" key');
    let value;
    if (match[3] === undefined || match[3] === '') {
      const block = [];
      let j = i + 1;
      while (j < sourceLines.length) {
        const continuation = sourceLines[j].replace(/\r$/, '');
        if (continuation === '') { j++; continue; }
        if (/^\s*/.exec(continuation)[0].length <= 4) break;
        block.push(continuation.trim()); j++;
      }
      if (block.length === 0) fail(i + 1, `value of "${match[2]}" is empty`);
      try { value = JSON.parse(block.join('\n').replace(/,\s*([}\]])/g, '$1')); }
      catch (_) { fail(i + 1, `multiline value of "${match[2]}" is not valid historical JSON/YAML flow syntax`); }
      i = j - 1;
    } else {
      try { value = JSON.parse(match[3]); }
      catch (_) { fail(i + 1, `value of "${match[2]}" is not valid JSON`); }
    }
    if (match[1] === '  - ') {
      current = { [match[2]]: value, __line: i + 1 };
      rows.push(current);
      if (match[2] === 'dispatch_id') {
        if (dispatchRows.has(value)) fail(i + 1, `duplicate dispatch_id ${J(value)}`);
        dispatchRows.set(value, current);
      } else if (match[2] === 'close_of') {
        if (closeRows.has(value)) fail(i + 1, `duplicate close_of ${J(value)}`);
        closeRows.set(value, current);
      } else fail(i + 1, `row must start with dispatch_id or close_of, got "${match[2]}"`);
    } else {
      if (!current) fail(i + 1, 'continuation field appears before a row');
      if (Object.prototype.hasOwnProperty.call(current, match[2])) fail(i + 1, `duplicate row field "${match[2]}"`);
      current[match[2]] = value;
    }
  }
  return { dispatchRows, closeRows, rows };
}

function validateCloseAgainstDispatch(dispatchRow) {
  if (!dispatchRow) throw new RegistrationError(`close_of ${J(rec.close_of)} has no matching dispatch row`);
  const groups = Array.isArray(dispatchRow.groups) ? dispatchRow.groups : [];
  const expectedAgents = groups.reduce((sum, group) => sum + (Array.isArray(group.agents) ? group.agents.length : 0), 0);
  if (rec.agents_spawned.planned_total !== expectedAgents) {
    throw new RegistrationError(`agents_spawned.planned_total (${rec.agents_spawned.planned_total}) must equal the registered strategy agent count (${expectedAgents})`);
  }
  if (rec.exit_reason === 'resolved' &&
      (rec.agents_spawned.total !== expectedAgents || rec.agents_spawned.not_launched !== 0)) {
    throw new RegistrationError('resolved close requires every registered agent to be launched and not_launched to be zero');
  }
  if (Number.isInteger(dispatchRow.max_loops) && rec.agents_spawned.loops_used > dispatchRow.max_loops) {
    throw new RegistrationError(`agents_spawned.loops_used exceeds registered max_loops ${dispatchRow.max_loops}`);
  }
}

try {
  assertGovernedPaths();
  acquireLock();
  try { fs.writeFileSync(file, header, { flag: 'wx' }); } catch (error) { if (error.code !== 'EEXIST') throw error; }
  const existing = fs.readFileSync(file, 'utf8');
  const nl = existing.length > 0 && !existing.endsWith('\n') ? '\n' : '';
  const { dispatchRows, closeRows } = checkLedger(existing);

  if (isClose) {
    const prior = closeRows.get(rec.close_of);
    if (prior) {
      if (prior.close_sha256 !== sheetSha256) throw new RegistrationError(`close_of ${J(rec.close_of)} already exists with different content; temporary record preserved`);
      console.log('already closed with identical content:', rec.close_of, '— no row appended.');
      consumeSource();
    } else {
      validateCloseAgainstDispatch(dispatchRows.get(rec.close_of));
      const output = [
        '  - close_of: ' + J(rec.close_of),
        '    closed: ' + J(new Date().toISOString()),
        '    close_sha256: ' + J(sheetSha256),
        '    invoked_by: ' + J(resolveInvokedBy()),
        '    exit_reason: ' + J(rec.exit_reason),
        '    agents_spawned: ' + J(rec.agents_spawned),
      ];
      if (rec.feedback_prompts !== undefined) output.push('    feedback_prompts: ' + J(rec.feedback_prompts));
      appendDurably(nl + output.join('\n') + '\n');
      console.log('closed dispatch', rec.close_of, '->', file);
      consumeSource();
    }
  } else {
    const prior = dispatchRows.get(rec.dispatch_id);
    if (prior) {
      if (prior.sheet_sha256 !== sheetSha256) throw new RegistrationError(`dispatch_id ${J(rec.dispatch_id)} already exists with different sheet bytes; temporary record preserved`);
      console.log('already registered with identical sheet:', rec.dispatch_id, '— no row appended.');
      consumeSource();
    } else {
      const output = [
        '  - dispatch_id: ' + J(rec.dispatch_id),
        '    schema_version: ' + J(rec.schema_version),
        '    created: ' + J(new Date().toISOString()),
        '    sheet_sha256: ' + J(sheetSha256),
        '    invoked_by: ' + J(resolveInvokedBy()),
        '    dispatch_type: ' + J(rec.dispatch_type),
        '    goal: ' + J(rec.goal),
        '    context: ' + J(rec.context),
        '    max_loops: ' + J(rec.max_loops),
        '    final_approver: ' + J(rec.final_approver),
      ];
      if (rec.meta === true) output.push('    meta: ' + J(true));
      if (rec.parent_dispatch_id != null) output.push('    parent_dispatch_id: ' + J(rec.parent_dispatch_id));
      if (rec.anti_bias_global != null) output.push('    anti_bias_global: ' + J(rec.anti_bias_global));
      if (rec.output_mode != null) output.push('    output_mode: ' + J(rec.output_mode));
      if (rec.working_folder != null) output.push('    working_folder: ' + J(rec.working_folder));
      if (rec.execution_projection_sha256 != null) output.push('    execution_projection_sha256: ' + J(rec.execution_projection_sha256));
      output.push('    groups: ' + J(rec.groups));
      if (rec.connections !== undefined) output.push('    connections: ' + J(rec.connections));
      appendDurably(nl + output.join('\n') + '\n');
      const agentCount = rec.groups.reduce((total, group) => total + group.agents.length, 0);
      console.log('registered dispatch', rec.dispatch_id, '->', file, `(${agentCount} agents across ${rec.groups.length} groups)`);
      consumeSource();
    }
  }
} catch (error) {
  console.error(error.message || String(error));
  process.exitCode = Number.isInteger(error.code) ? error.code : 1;
} finally {
  releaseLock();
}
