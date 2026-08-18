#!/usr/bin/env python3
"""
Verify AI search-crawler access at BOTH layers: robots.txt and the live edge.

A permissive robots.txt proves nothing if a CDN, WAF, or bot-management rule
returns 403/503 to these user agents before the request reaches the origin.
That failure mode is common and invisible to a robots.txt-only audit.

Distinguishes SEARCH crawlers (control whether you can be cited) from TRAINING
crawlers (control whether you feed the model). Blocking a training crawler does
not remove you from that engine's answers.

Usage:
    python aeo_crawler_check.py https://example.com
    python aeo_crawler_check.py https://example.com --json
"""

import argparse
import json
import os
import sys
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

_SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)
from url_safety import safe_requests_get

# role: "search" bots decide citation eligibility. "training" bots do not.
CRAWLERS = [
    ("OAI-SearchBot",  "search",   "ChatGPT",              "OAI-SearchBot/1.0; +https://openai.com/searchbot"),
    ("Claude-SearchBot", "search", "Claude",               "Mozilla/5.0 (compatible; Claude-SearchBot/1.0; +claudebot@anthropic.com)"),
    ("PerplexityBot",  "search",   "Perplexity",           "Mozilla/5.0 (compatible; PerplexityBot/1.0; +https://perplexity.ai/perplexitybot)"),
    ("Googlebot",      "search",   "Google AI Overviews",  "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"),
    ("GPTBot",         "training", "OpenAI training",      "Mozilla/5.0 (compatible; GPTBot/1.1; +https://openai.com/gptbot)"),
    ("ClaudeBot",      "training", "Anthropic training",   "Mozilla/5.0 (compatible; ClaudeBot/1.0; +claudebot@anthropic.com)"),
    ("Google-Extended", "training", "Gemini app grounding", "Mozilla/5.0 (compatible; Google-Extended/1.0)"),
]


def check(url: str) -> dict:
    parsed = urlparse(url)
    origin = f"{parsed.scheme}://{parsed.netloc}"
    robots_url = urljoin(origin, "/robots.txt")

    out = {"url": url, "origin": origin, "robots_url": robots_url,
           "robots_found": False, "robots_status": None, "crawlers": [],
           "blocking_issues": []}

    rp = RobotFileParser()
    # Fetch robots.txt with a realistic UA. Some hosts (Duda, several CDN bot
    # rules) return 403 to a default library user agent, which would otherwise
    # be misread as "this site has no robots.txt".
    robots_ua = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                 "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36")
    try:
        r = safe_requests_get(robots_url, timeout=20, allow_redirects=True,
                              headers={"User-Agent": robots_ua})
        out["robots_status"] = r.status_code
        if r.status_code == 200 and r.text.strip() and "<html" not in r.text[:200].lower():
            out["robots_found"] = True
            rp.parse(r.text.splitlines())
        elif r.status_code in (401, 403, 405, 406, 429, 503):
            out["blocking_issues"].append(
                f"robots.txt returned HTTP {r.status_code}. The file could not be read, so "
                f"crawler rules are UNKNOWN, not absent. A CDN or WAF is filtering by user agent.")
    except Exception as exc:
        out["robots_status"] = "error"
        out["robots_error"] = str(exc)[:160]

    for name, role, engine, ua in CRAWLERS:
        row = {"crawler": name, "role": role, "engine": engine,
               "robots_allowed": None, "edge_status": None, "edge_blocked": None}

        if out["robots_found"]:
            try:
                row["robots_allowed"] = rp.can_fetch(name, url)
            except Exception:
                row["robots_allowed"] = None
        elif out["robots_status"] == 404:
            # A genuine 404 means nothing is disallowed.
            row["robots_allowed"] = True
        else:
            # Unreadable robots.txt. Do not guess.
            row["robots_allowed"] = None

        try:
            resp = safe_requests_get(url, timeout=25, allow_redirects=True,
                                     headers={"User-Agent": ua})
            row["edge_status"] = resp.status_code
            row["edge_blocked"] = resp.status_code in (401, 403, 405, 406, 429, 503)
        except Exception as exc:
            row["edge_status"] = "error"
            row["edge_blocked"] = True
            row["edge_error"] = str(exc)[:120]

        if role == "search":
            if row["robots_allowed"] is False:
                out["blocking_issues"].append(
                    f"{name} is DISALLOWED in robots.txt. You cannot be cited in {engine}.")
            if row["edge_blocked"]:
                out["blocking_issues"].append(
                    f"{name} got HTTP {row['edge_status']} at the edge. "
                    f"robots.txt is not the problem; a CDN/WAF rule is blocking {engine}.")
        out["crawlers"].append(row)

    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Verify AI crawler access at robots.txt and the edge")
    ap.add_argument("url")
    ap.add_argument("--json", "-j", action="store_true")
    args = ap.parse_args()

    result = check(args.url)

    if args.json:
        print(json.dumps(result, indent=2))
        return 1 if result["blocking_issues"] else 0

    print(f"AI crawler access: {result['url']}")
    if result["robots_found"]:
        robots_line = "found and parsed"
    elif result["robots_status"] == 404:
        robots_line = "absent (HTTP 404, so nothing is disallowed)"
    else:
        robots_line = f"UNREADABLE (HTTP {result['robots_status']}) - rules unknown, not absent"
    print(f"robots.txt: {robots_line}")
    print()
    print(f"{'CRAWLER':<18} {'ROLE':<9} {'ROBOTS':<8} {'EDGE':<7} ENGINE")
    print("-" * 72)
    for c in result["crawlers"]:
        robots = {True: "allow", False: "BLOCK", None: "unknown"}[c["robots_allowed"]]
        edge = str(c["edge_status"])
        flag = "  <-- BLOCKED" if (c["edge_blocked"] and c["role"] == "search") else ""
        print(f"{c['crawler']:<18} {c['role']:<9} {robots:<8} {edge:<7} {c['engine']}{flag}")

    print()
    if result["blocking_issues"]:
        print("CITATION-BLOCKING ISSUES:")
        for i in result["blocking_issues"]:
            print(f"  ! {i}")
        return 1
    print("No citation-blocking issues. All search crawlers can reach this URL.")
    print("Note: training crawlers (GPTBot, ClaudeBot, Google-Extended) do not affect citation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
