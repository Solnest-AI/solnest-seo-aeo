#!/usr/bin/env python3
"""
Check brand entity-name consistency across a site's machine-readable surfaces.

AI systems merge a brand into one entity using signals from many sources. When
your own surfaces disagree about your name, you split that entity and dilute
every mention you earn. This catches the disagreement before a retrieval system
does.

Compares the organisation name found in:
  - JSON-LD Organization / LocalBusiness  (schema.org "name")
  - Open Graph og:site_name
  - <title> tag
  - /llms.txt first heading, if the file exists

Usage:
    python aeo_entity_check.py https://example.com
    python aeo_entity_check.py https://example.com --json
"""

import argparse
import json
import os
import re
import sys
from urllib.parse import urljoin, urlparse

_SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)
from url_safety import safe_requests_get

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Error: beautifulsoup4 is required", file=sys.stderr)
    sys.exit(1)

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36")

ORG_TYPES = {"organization", "localbusiness", "corporation", "professionalservice",
             "legalservice", "realestateagent", "lodgingbusiness", "healthandbeautybusiness"}


def _walk_schema(node, found):
    """Collect 'name' from any Organization-ish node, including inside @graph."""
    if isinstance(node, list):
        for item in node:
            _walk_schema(item, found)
        return
    if not isinstance(node, dict):
        return
    if "@graph" in node:
        _walk_schema(node["@graph"], found)
    t = node.get("@type")
    types = [t] if isinstance(t, str) else (t if isinstance(t, list) else [])
    if any(isinstance(x, str) and x.lower() in ORG_TYPES for x in types):
        name = node.get("name") or node.get("legalName")
        if isinstance(name, str) and name.strip():
            found.append((", ".join(str(x) for x in types), name.strip()))
    for v in node.values():
        if isinstance(v, (dict, list)):
            _walk_schema(v, found)


def check(url: str) -> dict:
    parsed = urlparse(url)
    origin = f"{parsed.scheme}://{parsed.netloc}"
    out = {"url": url, "surfaces": {}, "mismatches": [], "notes": []}

    resp = safe_requests_get(url, timeout=30, allow_redirects=True,
                             headers={"User-Agent": UA})
    soup = BeautifulSoup(resp.text, "html.parser")

    title = soup.find("title")
    if title and title.get_text(strip=True):
        out["surfaces"]["title"] = title.get_text(strip=True)

    og = soup.find("meta", property="og:site_name")
    if og and og.get("content"):
        out["surfaces"]["og:site_name"] = og["content"].strip()

    schema_names = []
    for tag in soup.find_all("script", type="application/ld+json"):
        try:
            _walk_schema(json.loads(tag.string or "{}"), schema_names)
        except (json.JSONDecodeError, TypeError):
            continue
    for i, (types, name) in enumerate(schema_names):
        out["surfaces"][f"jsonld:{types}"] = name

    try:
        r = safe_requests_get(urljoin(origin, "/llms.txt"), timeout=20,
                              allow_redirects=True, headers={"User-Agent": UA})
        ct = r.headers.get("content-type", "")
        if r.status_code == 200 and "text/plain" in ct:
            m = re.search(r"^#\s+(.+)$", r.text, re.MULTILINE)
            if m:
                out["surfaces"]["llms.txt"] = m.group(1).strip()
        elif r.status_code == 200:
            out["notes"].append(
                f"/llms.txt returned 200 but content-type is '{ct}', likely a soft 404.")
    except Exception:
        pass

    # Compare only the surfaces that assert a bare brand name. <title> is
    # usually "Brand | Tagline", so it is treated as a containment check.
    authoritative = {k: v for k, v in out["surfaces"].items() if k != "title"}
    distinct = {}
    for k, v in authoritative.items():
        distinct.setdefault(v, []).append(k)

    if len(distinct) > 1:
        listing = "; ".join(f'"{v}" ({", ".join(ks)})' for v, ks in distinct.items())
        out["mismatches"].append(f"Brand name disagrees across surfaces: {listing}")

    if "title" in out["surfaces"] and authoritative:
        # Split the title into its segments. A brand normally occupies one whole
        # segment, either first ("Brand | Tagline") or last ("Page | Brand").
        # Plain substring matching is too weak: "Solnest" trivially matches
        # "Solnest Stays" and hides a real truncation.
        segments = [seg.strip() for seg in re.split(r"\s+[|\u2013\u2014\u00b7]\s+|\s+-\s+",
                                                   out["surfaces"]["title"]) if seg.strip()]
        seg_lower = [seg.lower() for seg in segments]
        for v in distinct:
            vl = v.lower()
            if vl in seg_lower:
                continue
            longer = [seg for seg, sl in zip(segments, seg_lower)
                      if vl in sl and len(sl) > len(vl)]
            if longer:
                out["mismatches"].append(
                    f'TRUNCATED NAME: <title> says "{longer[0]}" but the machine-readable '
                    f'surfaces declare only "{v}". Retrieval systems may treat these as two '
                    f'entities. Use the full name everywhere.')
            else:
                out["mismatches"].append(
                    f'<title> does not contain the declared brand name "{v}".')

    # Near-miss detector: same name modulo one or two characters is almost always
    # a typo rather than an intentional alternate name.
    names = list(distinct)
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = names[i], names[j]
            if a.lower() != b.lower() and abs(len(a) - len(b)) <= 2:
                sa, sb = a.lower().replace(" ", ""), b.lower().replace(" ", "")
                diff = sum(1 for x, y in zip(sa, sb) if x != y) + abs(len(sa) - len(sb))
                if 0 < diff <= 2:
                    out["mismatches"].append(
                        f'LIKELY TYPO: "{a}" vs "{b}" differ by {diff} character(s).')
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Check brand entity-name consistency")
    ap.add_argument("url")
    ap.add_argument("--json", "-j", action="store_true")
    args = ap.parse_args()

    result = check(args.url)
    if args.json:
        print(json.dumps(result, indent=2))
        return 1 if result["mismatches"] else 0

    print(f"Entity consistency: {result['url']}\n")
    if not result["surfaces"]:
        print("No brand-name surfaces found (no title, og:site_name, JSON-LD org, or llms.txt).")
        return 1
    width = max(len(k) for k in result["surfaces"])
    for k, v in result["surfaces"].items():
        print(f"  {k:<{width}}  {v}")
    for n in result["notes"]:
        print(f"\n  note: {n}")
    print()
    if result["mismatches"]:
        print("ENTITY ISSUES:")
        for m in result["mismatches"]:
            print(f"  ! {m}")
        return 1
    print("Brand name is consistent across all machine-readable surfaces.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
