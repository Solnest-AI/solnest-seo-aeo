# Example output: a real audit

This is an unedited run of the plugin against [solnestai.com](https://solnestai.com), our own
site. Nothing was cleaned up for presentation, including the critical finding it caught on us.

It is here so you can see what the output actually looks like before you install anything.

## What is in this folder

| File | What it is |
|---|---|
| `FULL-AUDIT-REPORT.md` | The SEO audit. Scoreboard, findings by category, page inventory |
| `ACTION-PLAN.md` | The same findings as a phased, checkable task list |
| `AEO-REPORT.md` | The AI visibility audit. Crawler access, entity consistency, citability |
| `audit-data.json` | Structured SEO results, the input to the generated report |
| `aeo-data.json` | Structured AEO results, captured from the scripts' `--json` output |
| `Google-SEO-Report-solnestai.com-full.pdf` | The client-facing deliverable, 9 pages |
| `Google-SEO-Report-solnestai.com-full.html` | Same report as HTML, if you cannot build the PDF |

## How it was produced

```bash
/solnest-seo:seo audit https://solnestai.com
```

```bash
/solnest-seo:seo-aeo https://solnestai.com
```

Then the PDF:

```bash
claude-seo run google_report.py --type full --format both --data audit-data.json --domain solnestai.com --output-dir .
```

## What it found

**Health score: 52 out of 100.**

The critical one: six of eight pages emitted `<link rel="canonical" href="https://solnestai.com">`,
which tells Google those pages are duplicates of the homepage and should not be indexed on their
own. One of them holds 2,789 words of portfolio content. That was verified against raw HTML, not
just through the parser.

Because Google's AI surfaces retrieve from the ordinary Search index, the same defect suppressed
AI visibility for those pages at the same time. One bug, both channels.

It also found five pages sharing a byte-identical title and meta description, four thin pages, and
an AI visibility band of **Readable, not Citable**: crawlable and entity-clean, but the longest
paragraph on the homepage is 37 words against a 134 to 167 word target, with zero percentages and
zero dollar figures in extractable text.

## Honest limitations, as printed in the report

- **Core Web Vitals were not measured.** PageSpeed Insights rate-limits without an API key, so the
  report says so rather than guessing.
- **Search Console data was unavailable**, so indexation is inferred from canonical tags rather
  than confirmed.
- **No claim is made about current AI citation share.** That needs repeated sampling against a
  fixed prompt set. A single reading of a non-deterministic system is not evidence.
