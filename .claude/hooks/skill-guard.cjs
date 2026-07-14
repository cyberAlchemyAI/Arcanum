// PreToolUse guard: steer skill authoring through the create-skill skill.
// Reads the hook payload from stdin; if the Write/Edit targets a file under
// .claude/skills/, injects context telling the agent to use create-skill.
let data = '';
process.stdin.on('data', (c) => { data += c; });
process.stdin.on('end', () => {
  let filePath = '';
  try {
    filePath = String((JSON.parse(data).tool_input || {}).file_path || '');
  } catch (e) { /* malformed payload: stay silent */ }
  const normalized = filePath.replace(/\\/g, '/').toLowerCase();
  if (normalized.includes('.claude/skills/')) {
    console.log(JSON.stringify({
      hookSpecificOutput: {
        hookEventName: 'PreToolUse',
        additionalContext: 'This file is a Claude Code skill (.claude/skills/**). Skill authoring in this repo is governed by the create-skill skill. If create-skill is not already active in this session, invoke the Skill tool with skill "create-skill" and follow its guided flow BEFORE creating or editing this file. If it is already active (or you were routed here by it), proceed.'
      }
    }));
  }
});
