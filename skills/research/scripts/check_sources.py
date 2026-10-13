#!/usr/bin/env python3
"""Check a research doc's citations.

Usage: check_sources.py <doc.html>

- every <sup class="ref"> link points at an id that exists in the doc
- every source in <ol class="sources"> is cited at least once (warning only)
- every external link in the sources list resolves

Exit code 1 if anything must be fixed. 401/403/429 count as "check by hand",
since many sites block scripts, not as failures.
"""
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129 Safari/537.36"


class Doc(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.refs = []          # "#s1" targets from sup.ref
        self.sources = []       # (li id, [urls])
        self._in_sources = 0
        self._in_ref = 0
        self._li = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = (a.get("class") or "").split()
        if a.get("id"):
            self.ids.add(a["id"])
        if tag == "ol" and "sources" in cls:
            self._in_sources += 1
        if tag == "sup" and "ref" in cls:
            self._in_ref += 1
        if tag == "li" and self._in_sources:
            self._li = (a.get("id"), [])
            self.sources.append(self._li)
        if tag == "a" and a.get("href"):
            href = a["href"]
            if self._in_ref and href.startswith("#"):
                self.refs.append(href[1:])
            elif self._in_sources and self._li is not None and href.startswith("http"):
                self._li[1].append(href)

    def handle_endtag(self, tag):
        if tag == "ol" and self._in_sources:
            self._in_sources -= 1
        if tag == "sup" and self._in_ref:
            self._in_ref -= 1


def check(url):
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, method=method, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=15) as r:
                return url, r.status, None
        except urllib.error.HTTPError as e:
            if method == "HEAD" and e.code in (403, 404, 405, 501):
                continue
            return url, e.code, None
        except Exception as e:  # dns, timeout, tls
            if method == "HEAD":
                continue
            return url, None, type(e).__name__
    return url, None, "unknown"


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    doc = Doc()
    doc.feed(open(sys.argv[1], encoding="utf-8").read())

    fix, warn, manual = [], [], []
    for ref in doc.refs:
        if ref not in doc.ids:
            fix.append(f"citation #{ref} points at nothing")
    cited = set(doc.refs)
    for sid, urls in doc.sources:
        if sid and sid not in cited:
            warn.append(f"source #{sid} is never cited inline")
        if not urls:
            warn.append(f"source #{sid or '?'} has no link")

    urls = sorted({u for _, us in doc.sources for u in us})
    with ThreadPoolExecutor(max_workers=8) as pool:
        for url, status, err in pool.map(check, urls):
            if status and status < 400:
                continue
            if status in (401, 403, 429):
                manual.append(f"{status} {url}")
            else:
                fix.append(f"{status or err} {url}")

    print(f"{len(doc.sources)} sources, {len(urls)} links, {len(doc.refs)} inline citations")
    for label, items in (("fix", fix), ("check by hand", manual), ("warn", warn)):
        for item in items:
            print(f"  {label}: {item}")
    if not (fix or manual or warn):
        print("  all good")
    sys.exit(1 if fix else 0)


if __name__ == "__main__":
    main()
