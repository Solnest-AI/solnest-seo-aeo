# AI Visibility Audit: solnestai.com

**Date:** 2026-08-25  
**Auditor:** Solnest AI (solnest-seo plugin, seo-aeo skill)  
**Question this answers:** can ChatGPT, Claude, Perplexity, Gemini and Google AI Overviews find, read, and cite this site?

---

## Verdict: Readable

Crawlable, snippet-eligible, and entity-clean. A model can reach the page and knows who you are.
There is nothing on it worth quoting, and five pages are excluded from retrieval entirely.

| Band | Meaning | Status |
|---|---|---|
| Blocked | A search crawler is denied at robots.txt or the edge |  |
| Invisible | Crawlable, but not ranking and not mentioned anywhere |  |
| Readable | Crawlable and ranking, but nothing quotable on the page | **<- you are here** |
| Citable | Quotable and ranking |  |

---

## Step 1: Crawler access

robots.txt: found and parsed. Tested at robots.txt **and** with real requests at the CDN edge.

| Crawler | Role | Engine | robots.txt | Edge |
|---|---|---|---|---|
| `OAI-SearchBot` | search | ChatGPT | allow | 200 |
| `Claude-SearchBot` | search | Claude | allow | 200 |
| `PerplexityBot` | search | Perplexity | allow | 200 |
| `Googlebot` | search | Google AI Overviews | allow | 200 |
| `GPTBot` | training | OpenAI training | allow | 200 |
| `ClaudeBot` | training | Anthropic training | allow | 200 |
| `Google-Extended` | training | Gemini app grounding | allow | 200 |

**Result: pass.** All four search crawlers reach the site. Note the distinction that most sites get wrong:
`OAI-SearchBot` and `Claude-SearchBot` control citation. `GPTBot` and `ClaudeBot` are training only, and
`Google-Extended` has no effect on AI Overviews.

---

## Step 2: Entity consistency

| Surface | Declared name |
|---|---|
| `title` | Solnest AI - Watch What Happens When AI Meets Your Business |
| `og:site_name` | Solnest AI |
| `jsonld:Organization` | Solnest AI |
| `jsonld:ProfessionalService` | Solnest AI |
| `llms.txt` | Solnest AI |

**Result: pass.** Byte-identical across every surface, so retrieval systems merge these into one entity.

---

## Step 3: Citability

| Signal | Measured | Target |
|---|---|---|
| Words surviving extraction | **479 of 1921** (25%) | higher |
| Longest paragraph | **37 words** | 134-167 |
| Paragraphs over 40 words | **0** | several |
| Percentages in extractable text | **0** | some |
| Dollar figures in extractable text | **0** | some |
| Question-form H2s | 2/8 | more |
| Snippet-eligible | yes | yes |

**Result: weak.** The copy is good marketing writing: short punchy lines, one idea each, nothing over 37
words. That reads well to a human and gives a language model no self-contained block to lift.

---

## Findings

### Critical: Five pages are canonicalised to the homepage, blocking AI retrieval

Google AI Overviews and AI Mode retrieve from the ordinary Search index. /about, /services, /work, /book and /webinar all declare https://solnestai.com as canonical, so they are not eligible to be retrieved or cited. Verified against raw HTML.

**Fix:** Emit self-referencing canonicals. This is the single highest-leverage fix for both search and AI visibility.

### High: Nothing on the site is quotable

Main-content extraction yields 479 words from 1,921. The longest paragraph is 37 words against a 134 to 167 word target, with zero paragraphs over 40 words. Extractable text contains 0 percentages and 0 dollar figures. A model can read the page and has nothing to lift and attribute.

**Fix:** Add two or three genuine 130 to 160 word answer blocks with real numbers. Published pricing is the most quotable asset available and is absent from extractable text.

### Medium: Only two of eight homepage H2s are question-form

Question-shaped headings match how people phrase prompts and how retrieval segments a page.

**Fix:** Convert several H2s to the questions buyers actually ask.

### Info: AI search crawler access is correctly configured

All four search crawlers are allowed in robots.txt and return 200 at the edge. The robots.txt correctly separates search crawlers from training crawlers, which most sites get wrong.

**Fix:** No action. Keep OAI-SearchBot, Claude-SearchBot, PerplexityBot and Googlebot allowed.

### Info: Brand entity is consistent across all machine-readable surfaces

Solnest AI is byte-identical across title, og:site_name, both JSON-LD blocks and llms.txt. No entity split.

**Fix:** No action. Keep the name byte-identical when adding directory listings or a Google Business Profile.

---

## Priority order

Ordered by evidence strength, not by what is easiest to sell.

1. **Fix the canonicals.** Binary, free, and unblocks both search and AI retrieval.
2. **Rank for the topic.** Google AI surfaces retrieve from the ordinary index.
3. **Earn mentions.** Muck Rack measured earned media at 84% of AI citations across 25M links. Biggest lever, slowest.
4. **Publish quotable specifics.** The Princeton/Georgia Tech KDD 2024 study is the only causal evidence in the field, at roughly +30%.

Not levers: schema and llms.txt. Google states these are not needed for its AI features, and an Ahrefs
controlled study of 1,885 pages found no significant citation lift from structured data. Keep both for
what they are actually for.

---

## Method and limitations

- Crawler access tested with real requests using each crawler's user agent, at robots.txt and the edge.
- Citability measured with trafilatura main-content extraction, which approximates an LLM retrieval pipeline.
- No claim is made about current AI citation share. That requires repeated sampling against a fixed prompt set; a single reading of a non-deterministic system is not evidence.
- Indexation status is inferred from canonical tags, not confirmed. Search Console access would confirm it.

