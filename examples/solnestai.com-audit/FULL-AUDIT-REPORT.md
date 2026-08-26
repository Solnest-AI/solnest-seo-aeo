# SEO Audit: solnestai.com

**Date:** 2026-08-25  
**Auditor:** Solnest AI (solnest-seo plugin)  
**Scope:** All 8 URLs in sitemap.xml, crawled and parsed. Crawler access and entity checks run against the live site.

---

## Executive Summary

**Overall SEO Health Score: 52/100**

**Business type detected:** B2B AI implementation agency (service business, STR/real-estate/med-spa vertical focus)

### The headline

The site is well built and technically clean in the ways most sites fail. HTTPS is enforced, every
image has alt text, schema is present sitewide, and the robots.txt is one of the few in the wild that
correctly separates AI search crawlers from training crawlers.

It is also, right now, telling Google not to index most of itself.

### Top 5 critical issues

1. Six of eight pages declare the homepage as their canonical, instructing Google not to index them
2. Five pages share a byte-identical title tag and meta description
3. /work carries 2,789 words of portfolio content and is canonicalised away to the homepage
4. No page contains a self-contained answer block; longest paragraph on the homepage is 37 words
5. Zero percentages and zero dollar figures appear in extractable text across the site

### Top 5 quick wins

1. Set a self-referencing canonical on /about, /services, /work, /book and /webinar
2. Write unique title tags and meta descriptions for those five pages
3. Remove the duplicated brand suffix in the /webinar title
4. Add width and height to the six homepage images missing them
5. Publish real pricing figures as quotable text

---

## Scoreboard

| Category | Score | Note |
|---|---|---|
| Technical SEO | **40** | Clean foundations, one critical canonical defect |
| On-Page SEO | **38** | Five pages share one title and description |
| Content Quality | **55** | Four thin pages, two strong ones |
| Schema and Structured Data | **85** | Genuinely good, valid sitewide |
| Images | **70** | Perfect alt coverage, missing dimensions |
| AI Search Readiness | **55** | Access is perfect, nothing is quotable |

---

## Technical SEO

**Score: 40/100**

**What works**

- HTTPS enforced, clean 200 responses across all eight sitemap URLs
- robots.txt present, valid, and explicitly permissive to AI search crawlers
- sitemap.xml present and valid at /sitemap.xml with 8 URLs
- meta robots is index, follow with no X-Robots-Tag override

### Critical: Six of eight pages canonicalise to the homepage

/about, /services, /work, /book and /webinar all emit <link rel="canonical" href="https://solnestai.com">. Verified directly against raw HTML, not through a parser. A canonical pointing at a different URL tells Google the page is a duplicate and should not be indexed in its own right. These are not duplicates: /work alone holds 2,789 words of unique portfolio content.

**Fix:** Emit a self-referencing canonical on every page. /about should declare https://solnestai.com/about, and so on. This is almost certainly one shared layout component hardcoding the site root.

### Info: Core Web Vitals could not be measured

PageSpeed Insights returned a rate-limit error because no API key is configured. No field or lab data was collected, so no CWV claim is made in this report.

**Fix:** Run /solnest-seo:seo google setup to add a free Google API key, then re-run for real CrUX field data.

---

## On-Page SEO

**Score: 38/100**

**What works**

- Every page has exactly one H1
- Heading hierarchy is clean, with 24 H3s under 8 H2s on the homepage
- Homepage carries 17 internal links and a coherent structure

### Critical: Five pages share an identical title tag and meta description

/, /about, /services, /work and /book all use the title "Solnest AI - Watch What Happens When AI Meets Your Business" and the same meta description verbatim. Duplicate titles across a small site are a strong duplicate-content signal and waste the highest-value on-page ranking element on four pages.

**Fix:** Write a unique, intent-matched title and description per page. /services should target the service query, /work the proof query, /about the entity query.

### Medium: Duplicated brand suffix in the /webinar title

The title reads "Live Demo - From Zero to Automated | Solnest AI | Solnest AI", repeating the brand twice. This is the signature of a template appending a suffix to a title that already contains one.

**Fix:** Strip the brand from the page-level title or make the template suffix conditional.

---

## Content Quality

**Score: 55/100**

**What works**

- /work is substantial at 2,789 words
- The blog post is a genuine 947-word comparison piece with 4 schema blocks
- Copy is specific about verticals: short-term rentals, real estate, med spas

### High: Four pages are thin

/book is 52 words, /blog is 59, /about is 292 and /webinar is 317. /about at 292 words is well short of what an entity-establishing page needs, and it is one of the pages AI systems read to decide who a company is.

**Fix:** Prioritise /about and /services. Both are commercially important and both are currently too thin to rank or be cited.

---

## Schema and Structured Data

**Score: 85/100**

**What works**

- Organization and ProfessionalService JSON-LD present on every page
- Correct use of @id anchors such as #organization and #service
- Blog post carries 4 schema blocks including article-level markup
- Organization name is byte-identical to every other brand surface

### Low: Schema is duplicated rather than page-specific

The same Organization and ProfessionalService pair appears on all pages. That is valid and harmless, but page-type schema is missing where it would earn rich results.

**Fix:** Add Service schema on /services and FAQPage where genuine Q&A exists. Note this is a rich-results play, not an AI-citation lever.

---

## Images

**Score: 70/100**

**What works**

- Zero missing alt attributes across all 8 pages, which is unusual and good

### Medium: Six homepage images lack width and height

6 of 9 homepage images declare no intrinsic dimensions, which allows layout shift while they load and harms Cumulative Layout Shift.

**Fix:** Add explicit width and height, or use the Next.js Image component which sets them automatically.

### Low: Only one image is lazy-loaded

1 of 9 homepage images uses loading="lazy".

**Fix:** Lazy-load everything below the fold, keeping the LCP image eager.

---

## AI Search Readiness

**Score: 55/100**

**What works**

- All four search crawlers allowed in robots.txt and returning 200 at the edge: OAI-SearchBot, Claude-SearchBot, PerplexityBot, Googlebot
- The robots.txt correctly distinguishes search crawlers from training crawlers, which most sites get wrong
- Page is snippet-eligible with index, follow and no X-Robots-Tag
- Brand name is byte-identical across title, og:site_name, both JSON-LD blocks and llms.txt

### High: Nothing on the site is quotable

The homepage extracts to 479 words of main content. The longest paragraph is 37 words against a 134 to 167 word target for a self-contained answer block, and there are zero paragraphs over 40 words. Extractable text contains 0 percentages and 0 dollar figures. A model can read the page and still has nothing it can lift and attribute.

**Fix:** Add two or three genuine 130 to 160 word answer blocks containing real numbers. Published pricing is the most quotable asset available and is currently absent from extractable text.

### Critical: Canonical bug blocks AI retrieval as well as search

Google AI Overviews and AI Mode retrieve from the ordinary Search index. Pages canonicalised away are not eligible, so the canonical defect suppresses AI visibility for five pages at the same time as it suppresses ranking.

**Fix:** Fixing canonicals is the single highest-leverage action for both SEO and AI visibility. Do it first.

### Medium: Only two of eight homepage H2s are question-form

Question-shaped headings match how people phrase prompts and how retrieval segments a page.

**Fix:** Convert several H2s to the questions buyers actually ask.

---

## Page Inventory

| URL | Words | H1 | H2 | Schema | Images/missing alt | Canonical |
|---|---|---|---|---|---|---|
| / | 1921 | 1 | 8 | 2 | 9/0 | homepage (correct) |
| /about | 292 | 1 | 3 | 2 | 3/0 | **-> homepage (wrong)** |
| /services | 564 | 1 | 6 | 2 | 2/0 | **-> homepage (wrong)** |
| /work | 2789 | 1 | 12 | 2 | 2/0 | **-> homepage (wrong)** |
| /book | 52 | 1 | 0 | 2 | 2/0 | **-> homepage (wrong)** |
| /webinar | 317 | 1 | 1 | 2 | 2/0 | **-> homepage (wrong)** |
| /blog | 59 | 1 | 1 | 2 | 2/0 | self (correct) |
| /blog/best-ai-automation-agencies... | 947 | 1 | 10 | 4 | 2/0 | self (correct) |

---

## Method and Limitations

- All 8 sitemap URLs were fetched and parsed. Canonical tags were additionally verified straight from raw HTML, independent of the parser.
- Crawler access was tested with real requests using each crawler's user agent, at both robots.txt and the CDN edge.
- Core Web Vitals were **not measured**. PageSpeed Insights rate-limited without an API key, so this report makes no CWV claim.
- Backlink and Search Console data were not available. No claim is made about off-site authority or actual indexation status.
- Citability figures come from trafilatura main-content extraction, which approximates what an LLM retrieval pipeline ingests.

