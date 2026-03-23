#!/usr/bin/env node

/**
 * preprocess.mjs — Extract a clean transcript from a Claude Code session JSONL file.
 *
 * Usage:
 *   node preprocess.mjs [--cwd <path>] [--session-id <id>]
 *
 * Discovers the current session JSONL from ~/.claude/projects/ based on cwd,
 * parses it, writes the cleaned transcript to a temp file, and outputs
 * a short summary (with file path) to stdout.
 *
 * Output (stdout): JSON with stats + transcript_file path
 * Output (file):   Full transcript at .claude/tmp/skill-retro-<session-id>.json
 */

import { readFileSync, readdirSync, statSync, writeFileSync, mkdirSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { homedir } from 'node:os';

// ---------------------------------------------------------------------------
// Argument parsing
// ---------------------------------------------------------------------------

function parseArgs(argv) {
  const args = { cwd: process.cwd(), sessionId: null };
  for (let i = 2; i < argv.length; i++) {
    if (argv[i] === '--cwd' && argv[i + 1]) {
      args.cwd = resolve(argv[++i]);
    } else if (argv[i] === '--session-id' && argv[i + 1]) {
      args.sessionId = argv[++i];
    }
  }
  return args;
}

// ---------------------------------------------------------------------------
// Session file discovery
// ---------------------------------------------------------------------------

function cwdToProjectDir(cwd) {
  // Replace `/` with `-`  e.g. /Users/foo/bar → -Users-foo-bar
  return cwd.replace(/\//g, '-');
}

function findSessionFile(cwd, sessionId) {
  const projectsBase = join(homedir(), '.claude', 'projects');
  const encoded = cwdToProjectDir(cwd);
  const projectDir = join(projectsBase, encoded);

  try {
    statSync(projectDir);
  } catch {
    throw new Error(`Projects directory not found: ${projectDir}`);
  }

  if (sessionId) {
    const target = sessionId.endsWith('.jsonl') ? sessionId : `${sessionId}.jsonl`;
    const filePath = join(projectDir, target);
    try {
      statSync(filePath);
    } catch {
      throw new Error(`Session file not found: ${filePath}`);
    }
    return filePath;
  }

  // Find the most recently modified .jsonl file
  const files = readdirSync(projectDir)
    .filter((f) => f.endsWith('.jsonl'))
    .map((f) => {
      const full = join(projectDir, f);
      return { name: f, path: full, mtime: statSync(full).mtimeMs };
    })
    .sort((a, b) => b.mtime - a.mtime);

  if (files.length === 0) {
    throw new Error(`No .jsonl session files found in ${projectDir}`);
  }

  return files[0].path;
}

// ---------------------------------------------------------------------------
// Content extraction helpers
// ---------------------------------------------------------------------------

const SYSTEM_REMINDER_RE = /<system-reminder>[\s\S]*?<\/system-reminder>/g;

function truncate(str, max = 500) {
  if (str.length <= max) return str;
  return str.slice(0, max) + '...';
}

function extractContentString(content) {
  if (content == null) return '';
  if (typeof content === 'string') return content;
  if (Array.isArray(content)) {
    // tool_result content can be an array of text blocks
    return content
      .map((b) => {
        if (typeof b === 'string') return b;
        if (b.type === 'text') return b.text || '';
        return JSON.stringify(b);
      })
      .join('\n');
  }
  return JSON.stringify(content);
}

// ---------------------------------------------------------------------------
// Message processing
// ---------------------------------------------------------------------------

const SKIP_TYPES = new Set([
  'progress',
  'file-history-snapshot',
  'system',
  'queue-operation',
  'last-prompt',
]);

function processMessage(entry) {
  const parts = [];
  const meta = { skillInvocations: 0 };

  if (SKIP_TYPES.has(entry.type)) return null;

  const msg = entry.message;
  if (!msg || !msg.content) return null;

  const role = msg.role;
  if (role !== 'user' && role !== 'assistant') return null;

  const contentBlocks =
    typeof msg.content === 'string'
      ? [{ type: 'text', text: msg.content }]
      : Array.isArray(msg.content)
        ? msg.content
        : [];

  for (const block of contentBlocks) {
    if (!block || !block.type) continue;

    switch (block.type) {
      case 'text': {
        let text = block.text || '';
        if (role === 'user') {
          text = text.replace(SYSTEM_REMINDER_RE, '').trim();
          if (text) parts.push(`**User:** ${text}`);
        } else {
          if (text) parts.push(`**Assistant:** ${text}`);
        }
        break;
      }

      case 'tool_use': {
        if (block.name === 'Skill') {
          const skill = block.input?.skill || 'unknown';
          const args = block.input?.args || 'none';
          parts.push(`[SKILL INVOCATION: ${skill}] Args: ${truncate(String(args))}`);
          meta.skillInvocations++;
        } else {
          const inputStr = truncate(JSON.stringify(block.input || {}));
          parts.push(`[Tool: ${block.name}] Input: ${inputStr}`);
        }
        break;
      }

      case 'tool_result': {
        const contentStr = extractContentString(block.content);
        parts.push(
          `[Tool Result: ${block.tool_use_id}] ${truncate(contentStr)}`
        );
        break;
      }

      case 'thinking':
        // Skip thinking blocks entirely
        break;

      default:
        // Unknown block type — skip silently
        break;
    }
  }

  if (parts.length === 0) return null;

  return { text: parts.join('\n'), meta };
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

function main() {
  const args = parseArgs(process.argv);

  let sessionFile;
  try {
    sessionFile = findSessionFile(args.cwd, args.sessionId);
  } catch (err) {
    process.stderr.write(`Error: ${err.message}\n`);
    process.exit(1);
  }

  const raw = readFileSync(sessionFile, 'utf-8');
  const lines = raw.split('\n').filter((l) => l.trim());

  let sessionId = null;
  let firstTimestamp = null;
  const transcriptParts = [];
  let extractedMessages = 0;
  let totalSkillInvocations = 0;

  for (const line of lines) {
    let entry;
    try {
      entry = JSON.parse(line);
    } catch {
      // Malformed JSON line — skip gracefully
      continue;
    }

    // Capture session metadata from the first message that has it
    if (!sessionId && entry.sessionId) {
      sessionId = entry.sessionId;
    }
    if (!firstTimestamp && entry.timestamp) {
      firstTimestamp = entry.timestamp;
    }

    const result = processMessage(entry);
    if (result) {
      transcriptParts.push(result.text);
      extractedMessages++;
      totalSkillInvocations += result.meta.skillInvocations;
    }
  }

  const transcript = transcriptParts.join('\n\n');

  // Write full transcript to temp file
  const tmpDir = join(homedir(), '.claude', 'tmp');
  mkdirSync(tmpDir, { recursive: true });

  const shortId = (sessionId || 'unknown').slice(0, 8);
  const transcriptFile = join(tmpDir, `skill-retro-${shortId}.json`);

  const fullOutput = {
    session_id: sessionId,
    project_dir: args.cwd,
    timestamp: firstTimestamp,
    transcript,
    stats: {
      raw_lines: lines.length,
      extracted_messages: extractedMessages,
      skill_invocations: totalSkillInvocations,
      characters: transcript.length,
    },
  };

  writeFileSync(transcriptFile, JSON.stringify(fullOutput, null, 2), 'utf-8');

  // Output only summary + file path to stdout (keeps main agent context lean)
  const summary = {
    session_id: sessionId,
    project_dir: args.cwd,
    timestamp: firstTimestamp,
    transcript_file: transcriptFile,
    stats: fullOutput.stats,
  };

  process.stdout.write(JSON.stringify(summary, null, 2) + '\n');
}

main();
