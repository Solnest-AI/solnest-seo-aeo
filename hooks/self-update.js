#!/usr/bin/env node
"use strict";

// Solnest auto-update for the solnest-seo plugin (SessionStart hook).
//
// Once a day, in the background, it runs exactly what a manual update runs:
//   claude plugin marketplace update solnest-ai
//   claude plugin update solnest-seo@solnest-ai
// Claude Code only installs a new copy when plugin.json "version" went up, so a push
// to main without a version bump never ships. The new version loads the next time
// Claude Code starts. The running session keeps its copy until then.
//
// It never blocks Claude Code's start: the hook returns at once and a detached child
// does the work. It never touches the user's own files: ~/.config/claude-seo (keys and
// sign-ins), ~/.cache/claude-seo, the plugin's data folder (the Python environment and
// browser) and ~/.solnest/seo/my-instructions.md all live outside the plugin folder an
// update replaces.
//
// Shares the Solnest kill switch with every other Solnest tool (~/.solnest/):
//   ~/.solnest/paused or SOLNEST_NO_AUTOUPDATE=1  nothing updates
//   ~/.solnest/seo/last-check                     when it last ran (delete it to run again)
//   ~/.solnest/autoupdate.log                     one line per check
// Only runs from an installed copy (a path under plugins/cache/), never from a
// developer's checkout loaded with --plugin-dir.

const fs = require("fs");
const os = require("os");
const path = require("path");
const { spawn, spawnSync } = require("child_process");

const NAME = "seo";
const PLUGIN = "solnest-seo@solnest-ai";
const MARKETPLACE = "solnest-ai";
const EVERY_MS = 20 * 3600 * 1000; // once a day, with slack so a daily start always qualifies
const HOME = process.env.SOLNEST_HOME || path.join(os.homedir(), ".solnest");
const STAMP = path.join(HOME, NAME, "last-check");
const LOG = path.join(HOME, "autoupdate.log");
const ROOT = process.env.CLAUDE_PLUGIN_ROOT || path.resolve(__dirname, "..");

function log(msg) {
  try {
    fs.mkdirSync(HOME, { recursive: true });
    const d = new Date();
    const pad = (n) => String(n).padStart(2, "0");
    const when = `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ` +
      `${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`;
    fs.appendFileSync(LOG, `${when} ${NAME}: ${msg}\n`, "utf8");
  } catch (_) { /* logging never breaks anything */ }
}

function version() {
  try {
    return JSON.parse(fs.readFileSync(path.join(ROOT, ".claude-plugin", "plugin.json"), "utf8")).version || "?";
  } catch (_) {
    return "?";
  }
}

function newest(globDir, rel) {
  // newest <globDir>/<version>/<rel>, like `ls -t <globDir>/*/<rel> | head -1`
  try {
    return fs.readdirSync(globDir)
      .map((v) => path.join(globDir, v, rel))
      .filter((p) => fs.existsSync(p))
      .sort((a, b) => fs.statSync(b).mtimeMs - fs.statSync(a).mtimeMs)[0] || null;
  } catch (_) {
    return null;
  }
}

function findClaude() {
  // The same places the Solnest setups look: PATH, ~/.local/bin, then inside the desktop app.
  const win = process.platform === "win32";
  const onPath = spawnSync(win ? "where" : "which", ["claude"], { encoding: "utf8" });
  if (onPath.status === 0 && onPath.stdout.trim()) return onPath.stdout.trim().split(/\r?\n/)[0];
  for (const c of [path.join(os.homedir(), ".local", "bin", "claude"),
                   path.join(os.homedir(), ".local", "bin", "claude.exe")]) {
    if (fs.existsSync(c)) return c;
  }
  if (process.env.APPDATA) {
    const c = newest(path.join(process.env.APPDATA, "Claude", "claude-code"), "claude.exe");
    if (c) return c;
  }
  return newest(path.join(os.homedir(), "Library", "Application Support", "Claude", "claude-code"),
                path.join("claude.app", "Contents", "MacOS", "claude"));
}

function lastLine(text) {
  const lines = String(text || "").split(/\r?\n/).map((l) => l.trim()).filter(Boolean);
  return (lines[lines.length - 1] || "").slice(0, 300);
}

function child() {
  const claude = findClaude();
  if (!claude) {
    log("claude command not found, skipped");
    return;
  }
  const opts = { encoding: "utf8", timeout: 300000, env: { ...process.env, SOLNEST_AUTOUPDATE: "1", NO_COLOR: "1" },
                 shell: /\.(cmd|bat)$/i.test(claude), windowsHide: true }; // an npm install on Windows is claude.cmd
  const before = version();
  const m = spawnSync(claude, ["plugin", "marketplace", "update", MARKETPLACE], opts);
  if (m.status !== 0) {
    log(`marketplace update failed (${m.status}): ${lastLine(m.stdout + m.stderr) || m.error}`);
    return;
  }
  const u = spawnSync(claude, ["plugin", "update", PLUGIN], opts);
  const out = lastLine(u.stdout + u.stderr);
  if (u.status !== 0) {
    log(`update failed (${u.status}): ${out || u.error}`);
  } else if (/already at the latest/i.test(out)) {
    log(`up to date (v${before})`);
  } else {
    log(`v${before}: ${out} (loads the next time Claude Code starts)`);
  }
}

function main() {
  if (process.argv.includes("--child")) {
    child();
    return;
  }
  if (process.env.SOLNEST_NO_AUTOUPDATE || process.env.SOLNEST_AUTOUPDATE) return;
  if (fs.existsSync(path.join(HOME, "paused"))) return;
  if (!/[\\/]plugins[\\/]cache[\\/]/.test(ROOT)) return; // a developer's checkout
  try {
    if (Date.now() - fs.statSync(STAMP).mtimeMs < EVERY_MS) return;
  } catch (_) { /* never checked yet */ }
  try {
    fs.mkdirSync(path.dirname(STAMP), { recursive: true });
    fs.writeFileSync(STAMP, new Date().toISOString() + "\n", "utf8");
  } catch (_) {
    return; // cannot record the check: do not risk running on every start
  }
  const kid = spawn(process.execPath, [__filename, "--child"], {
    detached: true,
    stdio: "ignore",
    windowsHide: true,
    env: process.env,
  });
  kid.unref();
}

try {
  main();
} catch (_) { /* a start hook must never fail the session */ }
process.exitCode = 0;
