# Solnest SEO/AEO

**SEO and AEO for Claude Code.** Audit any site for classic search, then audit whether ChatGPT,
Claude, Perplexity, Gemini and Google AI Overviews can actually find, read, and cite it.

26 sub-skills and 18 sub-agents run in parallel across technical SEO, content quality (E-E-A-T),
Schema.org, Core Web Vitals, local SEO, backlinks, and AI search visibility. Every audit ends in a
prioritised action plan, not a score you cannot act on.

Built by [Solnest AI](https://solnestai.com) for the Solnest AI community.

> **Attribution.** Solnest SEO is a fork of [claude-seo](https://github.com/AgriciDaniel/claude-seo)
> v2.2.4 by agricidaniel, used under the MIT licence. We did not write the 25 upstream sub-skills and
> we do not claim to. What we added is listed under [What Solnest changed](#what-solnest-changed).
> This project is not affiliated with or endorsed by the upstream author. See [NOTICE](NOTICE).

---

## Setup

**Paste this page's URL into Claude Code and say "set this up".** Claude reads the steps below
and does the whole thing. You approve the commands as they come.

Prefer to read first? The same steps are in [INSTALL.md](INSTALL.md) with troubleshooting.

### Setup instructions (Claude: follow these exactly)

> **Claude, read this before acting.** Do not use `/plugin marketplace add` or `/plugin install`.
> Those are interactive slash commands that only the human can type, and you cannot run them for
> them. Use the four steps below, which install the plugin declaratively. Do them in order and stop
> if any step fails.

**Step 1. Check their Python.** Run:

```bash
python3 --version
```

It must be 3.10 or newer. macOS ships 3.9 at `/usr/bin/python3`. If you see 3.9.x, stop and tell
them to run `brew install python`, then start over. This is the most common install failure.

**Step 2. Register the plugin.** This merges two keys into `~/.claude/settings.json` and backs the
file up first. It must not remove any of their existing settings. Run:

```bash
python3 -c "
import json,os,shutil,sys,datetime,pathlib
p=pathlib.Path.home()/'.claude'/'settings.json'
s=json.loads(p.read_text()) if p.is_file() and p.read_text().strip() else {}
m={'source':{'source':'github','repo':'Solnest-AI/solnest-seo-aeo'}}
if s.get('extraKnownMarketplaces',{}).get('solnest-ai')==m and s.get('enabledPlugins',{}).get('solnest-seo@solnest-ai'): print('Already installed.'); sys.exit()
if p.is_file(): b=p.with_name('settings.json.bak-'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')); shutil.copy2(p,b); print('Backup:',b.name)
s.setdefault('extraKnownMarketplaces',{})['solnest-ai']=m
s.setdefault('enabledPlugins',{})['solnest-seo@solnest-ai']=True
p.parent.mkdir(parents=True,exist_ok=True); t=p.with_suffix('.json.tmp'); t.write_text(json.dumps(s,indent=2)+chr(10)); os.replace(t,p)
print('Installed. Kept',len(s),'settings keys and',len(s['enabledPlugins'])-1,'other plugins.')
"
```

**Step 3. Tell them to fully quit and reopen Claude Code.** Cmd+Q on Mac, or quit from the system
tray on Windows. Closing a tab or starting a new chat is not enough, because plugins load at
startup. Wait for them to confirm before continuing.

**Step 4. After they confirm the restart, tell them to run:**

```
/solnest-seo:seo setup
```

That builds an isolated Python environment and downloads a headless browser. It takes about four
minutes and installs nothing globally. Then they are ready.

Then point them at the two commands below.

---

## The two commands that matter

```bash
/solnest-seo:seo audit https://yoursite.com
```

Full site audit. Parallel sub-agents fan out across technical, content, schema, and performance,
then synthesise one prioritised plan.

```bash
/solnest-seo:seo-aeo https://yoursite.com
```

AI visibility audit. Can the answer engines cite you, and if not, why not. Leads with the levers the
evidence actually supports and tells you plainly which popular tactics do nothing.

The full command list is in [docs/COMMANDS.md](docs/COMMANDS.md).

---

## See it before you install

[`examples/solnestai.com-audit/`](examples/solnestai.com-audit/) holds a real, unedited run against
our own site, including the generated PDF. It scored us 52 out of 100 and caught five of our own
pages quietly telling Google not to index them. We left that in.

Want every feature? [`docs/API-SETUP.md`](docs/API-SETUP.md) covers the optional integrations,
free ones first, with what each actually costs.

---

## What Solnest changed

Four things, all of them things we hit while auditing real client sites.

**1. A dedicated AEO skill (`skills/seo-aeo/`).** New. Orders the work by evidence strength: crawler
access first, then ranking, then earned media, then quotable specifics. It states outright that
schema and llms.txt are not citation levers, citing Google's own AI optimization guide and the
Ahrefs controlled study, so nobody on your team sells a client work that does not move.

**2. `scripts/aeo_crawler_check.py`.** New. Verifies AI search-crawler access at **two** layers.
Most tools read robots.txt and stop. A permissive robots.txt means nothing if a CDN or WAF returns
403 to those user agents before the request reaches your origin. This makes a real request as each
crawler and reports what actually happens.

It also fixes the mistake almost everyone makes. `GPTBot` and `ClaudeBot` are **training** crawlers.
`OAI-SearchBot` and `Claude-SearchBot` are the ones that control **citation**. Blocking the training
bot does not remove you from that engine's answers. Upstream did not list `Claude-SearchBot` at all.

**3. `scripts/aeo_entity_check.py`.** New. Diffs your brand name across `<title>`, `og:site_name`,
JSON-LD `Organization` / `LocalBusiness`, and `llms.txt`. When your own surfaces disagree, retrieval
systems can treat you as two entities and every mention you earn gets split between them. It flags
two failure modes plain string comparison misses: near-miss typos (one surface says `LPP`, the rest
say `LLP`) and truncated names (machine surfaces declare `Acme`, the title says `Acme Property
Group`). Both are single-character or single-word gaps that split a brand in retrieval.

**4. A silent-zero bugfix in `scripts/parse_html.py`.** Upstream gated all link analysis behind an
optional `--url` flag and printed `Internal Links: 0` when it was omitted. That reads as "this page
has no internal links" rather than "this was not measured", and an agent will confidently write the
wrong finding. It now falls back to the page's own canonical or `og:url`, and says "not analyzed"
when it genuinely cannot tell. Verified on a real site: 0/0 before, 39/4 after.

All 422 tests pass: 410 upstream, plus 12 covering the changes above.

---

## Requirements

- Python 3.10+
- Claude Code
- Optional: Playwright Chromium, for SPA rendering and screenshots. The installer offers it.
- Optional: Google API credentials for real Search Console, CrUX and GA4 data. Run `/solnest-seo:seo google setup`.

No API keys are required. The plugin is fully functional without any paid service. Optional MCP
extensions wrap paid tools (DataForSEO, Ahrefs, SE Ranking, Profound) if you already have accounts.

---

## Staying current with upstream

This fork tracks `AgriciDaniel/claude-seo` and is based on tag `v2.2.4`. To pull their fixes:

A fresh clone has only `origin`, so add the upstream remote once:

```bash
git remote add upstream https://github.com/AgriciDaniel/claude-seo.git
git fetch upstream && git merge upstream/main
```

We deliberately kept upstream's internal skill and script names so these merges stay clean. Only
the plugin manifests, branding, documentation, and the four changes above diverge.

---

## Licence

MIT. See [LICENSE](LICENSE) and [NOTICE](NOTICE).

Copyright (c) 2026 agricidaniel. Copyright (c) 2026 Solnest AI for modifications and additions.
