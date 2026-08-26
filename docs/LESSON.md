# Lesson: Install the Solnest SEO and AEO Plugin for Claude Code

**By the end of this lesson:** You can audit any website for classic Google SEO and for AI search visibility from inside Claude Code, and you will know which fixes actually move the needle.

**What you need:** Claude Code (desktop app or terminal), Python 3.10 or newer, and a website you want to audit

---

## Overview

- The plugin adds 26 SEO skills and 18 specialist agents to Claude Code, free and with no API keys
- Two audits: a full technical and content SEO audit, and a separate AI visibility audit for ChatGPT, Claude, Perplexity, Gemini, and Google AI Overviews
- Installation is one block you paste into Claude Code, plus one restart
- The AI visibility side ranks fixes by what the research actually supports, so you stop paying for work that does nothing

---

## Step 1: Check Your Python Version

- In Claude Code, ask it to run `python3 --version`
- Confirm the version is 3.10 or newer

**Tip:** This is the number one reason the install fails. macOS still ships Python 3.9 at `/usr/bin/python3`. If you see 3.9, install a current version with `brew install python`, then start this lesson over.

---

## Step 2: Install the Plugin

- Copy the block below and paste it into Claude Code as a message
- Let Claude run the steps and approve the commands it asks to run

```
Set up the Solnest SEO/AEO plugin for me. Do these four steps in order and stop
if any of them fails.

STEP 1. Check my Python. Run:  python3 --version
It must be 3.10 or newer. macOS ships 3.9 at /usr/bin/python3, so if you see
3.9.x, STOP and tell me to run `brew install python` first, then start over.

STEP 2. Register the plugin. Back up ~/.claude/settings.json first, then merge in
these two keys without removing any of my existing settings:
extraKnownMarketplaces."solnest-ai" = {"source":{"source":"github","repo":"Solnest-AI/solnest-seo-aeo"}}
enabledPlugins."solnest-seo@solnest-ai" = true

STEP 3. Tell me to fully quit and reopen Claude Code.

STEP 4. After I confirm I restarted, tell me to run:  /solnest-seo:seo setup
```

**Tip:** The install only adds two settings and writes a timestamped backup first. Your existing plugins and settings are left alone.

**Tip:** The full paste block, with troubleshooting and an uninstall command, is in `INSTALL.md` at github.com/Solnest-AI/solnest-seo-aeo.

---

## Step 3: Restart Claude Code

- Quit the application completely, then reopen it
- Desktop app: quit from the menu bar on Mac, or the system tray on Windows
- Terminal: type `exit`, then reopen Claude

**Tip:** Closing a tab or starting a new chat is not enough. Plugins load when the app starts, so it has to be a full quit.

---

## Step 4: Build the Runtime

- Run `/solnest-seo:seo setup`
- Approve the install prompts and let it finish

**Tip:** This takes about four minutes. It builds an isolated Python environment and downloads a headless browser so the plugin can read JavaScript-rendered sites. Nothing is installed globally on your machine.

**Tip:** Run `/solnest-seo:seo doctor` any time to confirm the runtime is healthy. The shorter `/seo doctor` usually works too, but the full form always resolves, which matters if you have another SEO plugin installed.

**Tip:** If setup says it needs Python 3.10 even though you installed it, your app is not seeing your shell PATH. Add `"env": {"CLAUDE_SEO_PYTHON": "/opt/homebrew/bin/python3"}` to `~/.claude/settings.json`, using the path that `which python3` returns, then restart.

---

## Step 5: Run a Full SEO Audit

- Run `/solnest-seo:seo audit` followed by your site URL
- Let the specialist agents finish and read the prioritized action plan

**Tip:** The audit spawns multiple agents in parallel across technical SEO, content quality, schema, and performance, so a full site takes minutes instead of hours.

**Tip:** You can also target a single page with `/solnest-seo:seo page` and a URL.

---

## Step 6: Run an AI Visibility Audit

- Run `/solnest-seo:seo-aeo` followed by your site URL
- Read the crawler access results first, then the entity check, then the citability score

**Tip:** Plain English works too. Asking "why doesn't ChatGPT recommend my business" routes to the same skill.

**Tip:** The entity check compares your brand name across your title tag, Open Graph, structured data, and llms.txt. A one-character difference between those surfaces can split your brand into two entities as far as an AI system is concerned.

---

## Step 7: Fix the Findings in the Right Order

- Fix crawler access first. It is binary and free
- Then work on ranking for the topic, because Google AI surfaces retrieve from the normal search index
- Then invest in earned media and brand mentions, which is the biggest lever and the slowest
- Then make your pages quotable with specific numbers, named sources, and direct answers near the top
- Treat schema and llms.txt as housekeeping, not as citation levers

**Tip:** Training crawlers and search crawlers are different bots. `OAI-SearchBot` controls whether ChatGPT can cite you. `GPTBot` is training only, and blocking it does not remove you from ChatGPT answers. Same split for `Claude-SearchBot` versus `ClaudeBot`. `Google-Extended` has no effect on Google AI Overviews at all.

**Tip:** Check crawler access at your CDN, not just in robots.txt. A permissive robots.txt means nothing if Cloudflare or a firewall rule is returning 403 to those crawlers before they reach your site. The plugin tests both layers with real requests.

**Tip:** Google published in June 2026 that llms.txt files, AI-specific rewriting, special schema, and content chunking are not needed for its AI features. A controlled study of 1,885 pages that added structured data found no meaningful lift in AI citations. Set client expectations accordingly.

---

## Confirmation Check

- `/solnest-seo:seo doctor` reports the runtime is ready
- `/solnest-seo:seo audit` returns a prioritized action plan for your site
- `/solnest-seo:seo-aeo` reports whether each AI search crawler can reach your site and whether your brand name is consistent

---

## Key Takeaway

- Two commands cover both jobs: `/solnest-seo:seo audit` for Google, and `/solnest-seo:seo-aeo` for AI search visibility
- Getting cited by AI is mostly ordinary SEO plus being talked about elsewhere. Fix crawler access, rank for the topic, earn mentions, and publish things worth quoting. The file-based tricks being sold right now are not what moves it

---

## Need Help?

Post in the Community tab with a screenshot of where you are stuck. Tag @Ryan and I will help you work through it.
