#!/usr/bin/env python3
"""refcheck: verify every reference in references.json against its source, and say what was checked.

Crossref (DOI or title), OpenAlex as a second source, and plain reachability for laws and guidance
pages. It reports and never refuses (contract C39); --strict exits non-zero on any finding.
Hosted in zistgah/hecon until it moves to its home (see COMPONENTS.md).

© 1993–2026 Abhishek Choudhary. All rights reserved. AyeAI.
SPDX-License-Identifier: GPL-3.0-or-later
"""
import datetime, json, os, re, sys, urllib.parse, urllib.request
CROSSREF = os.environ.get("REFCHECK_CROSSREF", "https://api.crossref.org")
OPENALEX = os.environ.get("REFCHECK_OPENALEX", "https://api.openalex.org")
MAILTO = os.environ.get("REFCHECK_MAILTO", "ayeai.ayeam@gmail.com")
UA = {"User-Agent": "refcheck/1.0 (https://github.com/zistgah/hecon; mailto:%s)" % MAILTO}

def _get(url, timeout=25):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
        return r.status, r.read()
def _norm(s):
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", (s or "").lower())).strip()
def similarity(a, b):
    x, y = set(_norm(a).split()), set(_norm(b).split())
    return len(x & y) / float(len(x | y) or 1)

def check(ref):
    today = datetime.date.today().isoformat(); res = {"id": ref["id"], "checked_on": today}
    try:
        if ref.get("doi"):
            st, body = _get(CROSSREF + "/works/" + urllib.parse.quote(ref["doi"]))
            m = json.loads(body)["message"]; title = (m.get("title") or [""])[0]
            year = (m.get("issued", {}).get("date-parts") or [[None]])[0][0]
            sim = similarity(title, ref.get("title", "")); ok = sim >= 0.8 and (not ref.get("year") or year == ref["year"])
            res.update(state="verified" if ok else "open", source="Crossref", found_title=title, found_year=year,
                       similarity=round(sim, 3), finding="" if ok else "title or year differs from the citation")
        elif ref.get("title") and ref.get("kind") in ("article", "book", "guideline"):
            q = urllib.parse.urlencode({"query.bibliographic": ref["title"], "rows": 3})
            st, body = _get(CROSSREF + "/works?" + q)
            items = json.loads(body)["message"].get("items", [])
            best = max(items, key=lambda it: similarity((it.get("title") or [""])[0], ref["title"]), default=None)
            sim = similarity((best.get("title") or [""])[0], ref["title"]) if best else 0.0
            res.update(state="verified" if sim >= 0.85 else "open", source="Crossref search", similarity=round(sim, 3),
                       found_doi=best.get("DOI") if best else None, finding="" if sim >= 0.85 else "no matching record found")
        elif ref.get("url"):
            st, body = _get(ref["url"])
            res.update(state="reachable" if 200 <= st < 400 else "open", source="HTTP %d" % st,
                       finding="the page resolves; its wording was not compared" if 200 <= st < 400 else "unreachable")
        else:
            res.update(state="open", finding="nothing to check against")
    except Exception as e:  # network or parse failure is reported, never hidden
        res.update(state="open", finding="could not check: %s" % e.__class__.__name__)
    return res

def main(argv):
    path = argv[1] if len(argv) > 1 and not argv[1].startswith("-") else "references.json"
    data = json.load(open(path, encoding="utf-8")); results = [check(r) for r in data["references"]]
    out = os.path.join(os.path.dirname(os.path.abspath(path)), "refcheck-report.json")
    json.dump({"checked_on": datetime.date.today().isoformat(), "results": results}, open(out, "w", encoding="utf-8"), indent=1)
    counts = {}
    for r in results: counts[r["state"]] = counts.get(r["state"], 0) + 1
    print("refcheck: " + ", ".join("%s %d" % kv for kv in sorted(counts.items())) + "  (report: %s)" % os.path.basename(out))
    for r in results:
        if r["state"] != "verified": print("   %-10s %-14s %s" % (r["state"], r["id"], r.get("finding", "")))
    return 1 if ("--strict" in argv and any(r["state"] == "open" for r in results)) else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
