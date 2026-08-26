---
name: seo-aeo
description: >
  Solnest AI visibility audit. Answers one question: can ChatGPT, Claude,
  Perplexity, Gemini and Google AI Overviews find, read, and cite this site?
  Scores AI readiness 0-100, verifies AI crawler access at the edge (not just
  robots.txt), checks brand entity consistency across the site's own machine
  surfaces, and separates what the evidence supports from what the AEO industry
  is selling. Use when the user says "AEO", "GEO", "AI visibility", "AI search",
  "get cited by ChatGPT", "why doesn't AI recommend us", "LLM SEO", or asks
  about llms.txt.
user-invocable: true
argument-hint: "[url]"
license: MIT
metadata:
  author: Solnest AI
  version: "2.2.4"
  category: seo
---

# Solnest AEO: AI Visibility Audit

## Start here: what actually moves AI citations

Do not skip this section. Most AEO advice on the internet is selling work that
the controlled studies say does nothing. Get the ordering right and you save the
client both money and disappointment.

**Google's own position** (`developers.google.com/search/docs/fundamentals/ai-optimization-guide`,
updated June 2026):

> "From Google Search's perspective, optimizing for generative AI search is
> optimizing for the search experience, and thus still SEO."

Google states plainly that you do **not** need llms.txt files, AI-specific
content rewriting, special schema, or content chunking. Its wording on llms.txt
is that such files "neither harm nor help."

| Lever | Evidence | Priority |
|---|---|---|
| **Search-crawler access** | Blocking the wrong bot removes you entirely. Binary, and free to fix. | **1. Do first** |
| **Ranking for the topic** | Google AI surfaces retrieve from the ordinary index. Seer: organic rank correlates 0.65. | **2** |
| **Earned media / brand mentions** | Muck Rack, 25M cited links: earned media = 84% of AI citations, owned = 13.7%. Ahrefs, 75k brands: branded mentions 0.664 vs backlinks 0.218. | **3. Biggest lever** |
| **Quotable specifics** (stats, quotes, named sources) | Princeton/Georgia Tech, KDD 2024. The only causal study in the field. Roughly +30% visibility. | **4** |
| Schema / JSON-LD | Ahrefs difference-in-differences, 1,885 treated pages vs 4,000 controls: **no significant lift**. Keep it for rich results, which is what it is for. | Not a citation lever |
| llms.txt | No published evidence of citation lift. Google says it neither harms nor helps. | Not a citation lever |

**How to talk to a client about this.** Never promise placement. LLMs are
non-deterministic, and the same prompt returns different brand lists to
different users. You are raising the probability of citation, not buying a slot.
Anyone guaranteeing inclusion is selling something they cannot deliver.

---

## Step 1: Crawler access, verified at the edge

This is where most sites lose before they start, and it is the single highest
value thing in this skill.

**Training crawlers and search crawlers are different bots.** Blocking the
training bot does not remove you from that engine's answers. Blocking the search
bot does.

| To be cited in | Allow this crawler | Commonly misconfigured instead |
|---|---|---|
| ChatGPT | `OAI-SearchBot` | `GPTBot` (training only) |
| Claude | `Claude-SearchBot` | `ClaudeBot` (training only) |
| Perplexity | `PerplexityBot` | |
| Google AI Overviews / AI Mode | `Googlebot` + snippets allowed | `Google-Extended` (**has no effect on AI Overviews**) |
| Gemini app grounding | `Google-Extended` | |

**Check robots.txt, then check the edge.** A permissive robots.txt proves
nothing if Cloudflare, a WAF, or a bot-management rule returns 403 to these
user agents before the request reaches the origin. This failure mode is common
and completely invisible in robots.txt.

Run the check with the bundled runtime:

```bash
claude-seo run aeo_crawler_check.py <url>
```

Also confirm the page is indexable and snippet-eligible. `noindex`, or
`max-snippet:0` / `nosnippet`, removes Google AI Overview eligibility outright.

---

## Step 2: Entity consistency

AI systems merge your brand into a single entity across sources. Inconsistent
naming splits that entity and dilutes every mention you earn.

Check that the legal or trading name is **byte-identical** across:

- `<title>` and the organization name in JSON-LD (`Organization` / `LocalBusiness`)
- `llms.txt`, if one exists
- Open Graph `og:site_name`
- Google Business Profile, and any directory listings
- The footer NAP block

Diff the machine-readable surfaces against each other:

```bash
claude-seo run aeo_entity_check.py <url>
```

The two failure modes worth knowing, both seen in the wild:

- **Truncation.** `og:site_name` and `llms.txt` declare `Acme` while the title
  says `Acme Property Group`. A retrieval system can read that as two entities.
- **Near-miss typo.** One surface carries `Acme Partners LPP` against
  `Acme Partners LLP` everywhere else. One character, and the brand splits.

---

## Step 3: Citability scoring

Delegate the scored analysis to the `seo-geo` sub-skill, which carries the full
rubric: passage citability (optimal self-contained answer blocks of roughly
134 to 167 words), question-based heading hierarchy, attribution density,
structural readability, multi-modal presence, and entity presence across
Wikipedia, Reddit, YouTube and LinkedIn.

Then apply the Solnest weighting on top when reporting:

| Band | Meaning | What to do |
|---|---|---|
| **Blocked** | A search crawler is denied at robots.txt or the edge | Nothing else matters. Fix this today. |
| **Invisible** | Crawlable, but not ranking and not mentioned anywhere | This is an SEO and PR problem, not an AEO one |
| **Readable** | Crawlable and ranking, but nothing quotable on the page | Add specifics: numbers, named sources, direct answers up top |
| **Citable** | Quotable and ranking | Now push earned media. That is the 84% |

---

## Step 4: Measure honestly

Track the trend, never the single reading. Prompt-level "rank" from any AI
visibility tool is one roll of a non-deterministic die.

Measure:

1. **Share of voice** across a fixed prompt set that matters commercially, re-run
   on a fixed schedule, always the same prompts.
2. **AI referral traffic** in analytics, segmented from organic.
3. **Branded search volume**, the closest available proxy for whether the models
   are learning who the brand is.
4. **Rankings**, because retrieval still runs through the index.

Expect nothing for six to eight weeks. Movement shows up on long-tail queries
before head terms.

**Set expectations on traffic.** Pew tracked 68,879 real Google searches and
found users clicked a result on 8% of visits where an AI summary appeared,
versus 15% without. AI sends little traffic today. What it sends converts
unusually well, because the model already did the shortlisting. Sell this as a
recommendation channel, not a traffic channel.

---

---

## Output files

Persist the audit. Chat output disappears; a client deliverable should not.

Write into the same `{domain}-audit/` directory the `seo-audit` skill uses, so the
SEO and AEO halves compose into one folder and one report:

- `{domain}-audit/AEO-REPORT.md`: the readable audit. Crawler access table, entity
  diff, citability assessment, and the evidence-ordered recommendations.
- `{domain}-audit/aeo-data.json`: structured results, in the shape below.

Create the directory if it does not exist. If a `seo-audit` run already produced
one, write alongside its files rather than overwriting anything.

```json
{
  "url": "https://example.com",
  "audited_at": "YYYY-MM-DD",
  "band": "Blocked|Invisible|Readable|Citable",
  "crawler_access": {
    "robots_readable": true,
    "blocking_issues": [],
    "crawlers": [
      {"crawler": "OAI-SearchBot", "role": "search", "engine": "ChatGPT",
       "robots_allowed": true, "edge_status": 200, "edge_blocked": false}
    ]
  },
  "entity": {
    "consistent": true,
    "surfaces": {"title": "", "og:site_name": "", "jsonld:Organization": "", "llms.txt": ""},
    "mismatches": []
  },
  "citability": {
    "extracted_words": 0,
    "longest_paragraph_words": 0,
    "blocks_over_40_words": 0,
    "percentages": 0,
    "dollar_figures": 0,
    "question_form_headings": "0/0",
    "snippet_eligible": true
  },
  "findings": [
    {"title": "", "severity": "Critical|High|Medium|Low|Info",
     "description": "", "recommendation": ""}
  ]
}
```

Both bundled scripts accept `--json`, so capture their output directly rather than
retyping their results:

```bash
claude-seo run aeo_crawler_check.py <url> --json
claude-seo run aeo_entity_check.py <url> --json
```

After writing the files, tell the user where they are. If `audit-data.json` from a
`seo-audit` run is present in the same directory, offer to merge the AEO findings
into it so they appear in the generated PDF or HTML report.

## Reporting

Lead with what is broken and free to fix (crawler access, entity splits), then
what is earned and slow (mentions, coverage). For every recommendation state how
you would know it failed. If a finding rests on a correlation rather than a
controlled study, say so in the report.

If asked to add llms.txt or bolt on FAQ schema "for AI", explain the evidence,
note that it is cheap and harmless, and put it below the levers that actually
move. Do not lead a deliverable with it.
