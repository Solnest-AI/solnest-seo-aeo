# Optional API Setup

**You do not need any of this.** The plugin runs a full SEO and AI visibility audit with zero API
keys and zero accounts. Everything on this page is optional, and every item is listed with what it
actually costs.

Start with the free Google key. It takes about five minutes and unlocks the one thing the base
audit genuinely cannot do, which is measure real Core Web Vitals from actual Chrome users.

## What you get at each step

| Step | Cost | Unlocks |
|---|---|---|
| Nothing | Free | Full SEO audit, AI visibility audit, schema, sitemaps, images, local, content |
| Google API key | Free | Real Core Web Vitals, CrUX field data, 25-week trends |
| Google service account | Free | Search Console, URL inspection, indexation status, Indexing API |
| GA4 property ID | Free | Organic traffic, top landing pages, device and country splits |
| Google Ads token | Free | Keyword Planner search volume |
| Bing Webmaster | Free | Bing data, IndexNow instant submission |
| Unlighthouse | Free | Multi-page Lighthouse audits |
| Everything else | Paid | Backlinks, live SERP data, AI citation tracking |

---

## 1. Google API key (free, 5 minutes)

This is the highest-value step. Do this one even if you skip the rest.

1. Go to [console.cloud.google.com](https://console.cloud.google.com) and create a project, or pick
   an existing one.
2. Go to **APIs & Services > Library** and enable both:
   - **PageSpeed Insights API**
   - **Chrome UX Report API**
3. Go to **APIs & Services > Credentials > Create Credentials > API key**.
4. Optional but sensible: click **Restrict key** and allow only those two APIs.

Then save it. This command takes the key with hidden input, so it never lands in your terminal
history or in a chat transcript:

```bash
mkdir -p ~/.config/claude-seo && chmod 700 ~/.config/claude-seo && python3 -c "
import json,getpass,os,pathlib
k=getpass.getpass('Paste your Google API key (hidden): ').strip()
p=pathlib.Path.home()/'.config/claude-seo/google-api.json'
cfg=json.loads(p.read_text()) if p.is_file() else {}
cfg['api_key']=k
fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_TRUNC,0o600)
os.write(fd,(json.dumps(cfg,indent=2)+chr(10)).encode()); os.close(fd)
print('Saved to',p)
"
```

Check it worked:

```bash
~/.claude/plugins/cache/solnest-ai/solnest-seo/*/bin/claude-seo run google_auth.py --tier
```

You should see **Tier 0**, which unlocks `pagespeed`, `crux`, `crux-history`, `youtube` and `nlp`.

> **A Gemini API key will not work here.** Keys from Google AI Studio are scoped to the Generative
> Language API and return HTTP 403 for PageSpeed and CrUX. You need a key from a Cloud project with
> those two APIs enabled. If you already have a Gemini key, keep it: it works for the image
> generation extension further down.

---

## 2. Google service account (free, 10 minutes)

This is what tells you whether your pages are **actually indexed**, rather than inferring it from
your markup. If an audit ever flags a canonical or indexing problem, this is how you confirm it.

1. In the same project, go to **IAM & Admin > Service Accounts > Create Service Account**.
2. Create it, then open it, go to **Keys > Add Key > Create new key > JSON**, and download the file.
3. Move it somewhere private and lock it down:

   ```bash
   mkdir -p ~/.config/claude-seo && mv ~/Downloads/your-service-account.json ~/.config/claude-seo/service-account.json && chmod 600 ~/.config/claude-seo/service-account.json
   ```

4. Open that JSON and copy the `client_email` value. It looks like an email address.
5. In **Google Search Console > Settings > Users and permissions > Add user**, paste that email.
   Choose **Owner** if you want the Indexing API, otherwise **Full**.
6. Point the config at the file:

   ```bash
   python3 -c "
   import json,pathlib
   p=pathlib.Path.home()/'.config/claude-seo/google-api.json'
   cfg=json.loads(p.read_text()) if p.is_file() else {}
   cfg['service_account_path']=str(pathlib.Path.home()/'.config/claude-seo/service-account.json')
   cfg['default_property']='https://yoursite.com/'
   p.write_text(json.dumps(cfg,indent=2)+chr(10))
   print('Tier 1 configured')
   "
   ```

Set `default_property` to exactly how the property appears in Search Console, including the
trailing slash, or `sc-domain:yoursite.com` for a domain property.

Also enable **Google Search Console API** and **Web Search Indexing API** in the API Library.

You are now **Tier 1**: `gsc`, `inspect`, `sitemaps`, `index`.

---

## 3. GA4 traffic (free, 2 minutes)

1. Enable **Google Analytics Data API** in the API Library.
2. In **GA4 > Admin > Property Access Management**, add the same `client_email` as **Viewer**.
3. Copy your numeric property ID from **Admin > Property Settings**.

```bash
python3 -c "
import json,pathlib
p=pathlib.Path.home()/'.config/claude-seo/google-api.json'
cfg=json.loads(p.read_text()); cfg['ga4_property_id']='123456789'
p.write_text(json.dumps(cfg,indent=2)+chr(10)); print('Tier 2 configured')
"
```

**Tier 2**: `ga4`, `ga4-pages`.

---

## 4. Keyword volume (free, but approval takes days)

Real Keyword Planner search volume needs a **Google Ads developer token**, requested from your Ads
account under **Tools > API Center**. Approval is not instant.

Add `ads_developer_token` and `ads_customer_id` to the same config file for **Tier 3**:
`keywords`, `volume`.

Most people skip this. If you just want volume data, a DataForSEO account is faster.

---

## 5. Bing Webmaster and IndexNow (free)

Bing powers ChatGPT's search results, so this is more relevant than it used to be. IndexNow pushes
new URLs to Bing instantly instead of waiting for a crawl.

Get a free API key from [Bing Webmaster Tools](https://www.bing.com/webmasters) under
**Settings > API access**, then add it to `~/.claude/settings.json`:

```json
{
  "env": {
    "BING_WEBMASTER_API_KEY": "your-key",
    "INDEXNOW_KEY": "optional-indexnow-key"
  }
}
```

---

## 6. Unlighthouse (free, no key)

Multi-page Lighthouse audits across your whole site instead of one URL at a time. Needs Node 18+.

```bash
bash ~/.claude/plugins/cache/solnest-ai/solnest-seo/*/extensions/unlighthouse/install.sh
```

---

## 7. Image generation (free tier)

If you have a **Gemini API key** from [aistudio.google.com](https://aistudio.google.com), the
`banana` extension generates OG images, social previews, and blog heroes. This is the one place a
Gemini key is the right key.

---

## 8. Paid integrations

Only worth it if you are running client work at volume. All are bring-your-own-account.

| Extension | What it adds | Rough cost |
|---|---|---|
| **DataForSEO** | Live SERPs, keyword volume, backlinks, AI visibility | Pay per call, cheap to start |
| **Ahrefs** | Backlink index, organic keywords | Ahrefs plan with API access |
| **SE Ranking** | AI share of voice across ChatGPT, Gemini, Perplexity, AI Overviews | Subscription |
| **Profound** | LLM citation tracking with time series | Enterprise |
| **Firecrawl** | Full-site crawling for large audits | Free tier, then paid |

Each ships an installer. Swap in the extension name:

```bash
bash ~/.claude/plugins/cache/solnest-ai/solnest-seo/*/extensions/dataforseo/install.sh
```

Valid names: `ahrefs`, `banana`, `bing-webmaster`, `dataforseo`, `firecrawl`, `profound`,
`seranking`, `unlighthouse`.

---

## Checking what you have

Easiest way is to just ask Claude: "what Google SEO credential tier am I on?"

To run it directly, the launcher lives inside the installed plugin:

```bash
~/.claude/plugins/cache/solnest-ai/solnest-seo/*/bin/claude-seo run google_auth.py --tier
```

```bash
~/.claude/plugins/cache/solnest-ai/solnest-seo/*/bin/claude-seo run google_auth.py --check
```

`--tier` prints which tier you reached and what the next one needs. `--check` lists every API and
whether your credentials reach it.

The audit adapts to whatever is configured. With no credentials it still runs and simply reports
which measurements it could not take, rather than guessing at them.

---

## Keeping credentials safe

- Everything lives in `~/.config/claude-seo/`, created `0700`, with files written `0600`.
- Nothing is committed, transmitted anywhere except to Google's own endpoints, or logged.
- Never paste a key into a chat window, including into Claude. Use the hidden-input commands above.
- If you think a key leaked, delete it in the Cloud Console and create a new one. Rotating is free.
