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

## Install

**Paste one block into Claude Code and it sets itself up.** See [INSTALL.md](INSTALL.md)
for the block and the troubleshooting notes.

Prefer to do it by hand? Two slash commands:

```bash
/plugin marketplace add Solnest-AI/solnest-seo-aeo
```

```bash
/plugin install solnest-seo@solnest-ai
```

Then restart Claude Code and run `/solnest-seo:seo setup`, which builds an isolated Python
environment and downloads Playwright Chromium. It takes about four minutes and installs
nothing globally. Check it any time with `/solnest-seo:seo doctor`.

### Before you install, check your Python

```bash
python3 --version
```

You need **3.10 or newer**. macOS still ships `/usr/bin/python3` at 3.9, so if that command
prints 3.9 anything, install a current Python (`brew install python`) and then start over.
This is the single most common install failure.

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

New to this? [`docs/LESSON.md`](docs/LESSON.md) is the step-by-step walkthrough.
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

All 410 upstream tests still pass.

---

## Requirements

- Python 3.10+
- Claude Code
- Optional: Playwright Chromium, for SPA rendering and screenshots. The installer offers it.
- Optional: Google API credentials for real Search Console, CrUX and GA4 data. Run `/seo google setup`.

No API keys are required. The plugin is fully functional without any paid service. Optional MCP
extensions wrap paid tools (DataForSEO, Ahrefs, SE Ranking, Profound) if you already have accounts.

---

## Staying current with upstream

This fork tracks `AgriciDaniel/claude-seo` and is based on tag `v2.2.4`. To pull their fixes:

```bash
git fetch upstream && git merge upstream/main
```

We deliberately kept upstream's internal skill and script names so these merges stay clean. Only
the plugin manifests, branding, documentation, and the four changes above diverge.

---

## Licence

MIT. See [LICENSE](LICENSE) and [NOTICE](NOTICE).

Copyright (c) 2026 agricidaniel. Copyright (c) 2026 Solnest AI for modifications and additions.
