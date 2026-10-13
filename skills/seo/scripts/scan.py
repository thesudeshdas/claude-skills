#!/usr/bin/env python3
"""Quick SEO signal scan for a codebase and/or a live URL.

Usage: scan.py [repo-path] [--url https://example.com]

Prints the detected stack, SEO-related files that exist, and pattern hits
with file:line, plus live head tags and headers when --url is given.
It's a starting point for the audit: confirm every hit by reading the code.
"""
import json
import re
import sys
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

SKIP_DIRS = {"node_modules", ".git", ".next", "dist", "build", "out", ".output", ".vercel",
             ".netlify", "coverage", "vendor", ".expo", ".turbo", ".cache", ".svelte-kit",
             "Pods", "android", "ios", "__pycache__", ".venv", "venv"}
SRC_EXT = {".html", ".htm", ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".astro", ".vue",
           ".svelte", ".md", ".mdx", ".json", ".toml", ".txt", ".xml", ".webmanifest"}
MAX_BYTES = 400_000
UA = "Mozilla/5.0 (compatible; seo-skill-scan/1.0)"

FRAMEWORKS = [("next", "Next.js"), ("astro", "Astro"), ("nuxt", "Nuxt"), ("@remix-run/react", "Remix"),
              ("@sveltejs/kit", "SvelteKit"), ("gatsby", "Gatsby"), ("expo-router", "Expo Router"),
              ("expo", "Expo"), ("react-scripts", "CRA"), ("vite", "Vite"), ("vue", "Vue"),
              ("react", "React"), ("phaser", "Phaser"), ("pixi.js", "PixiJS"), ("three", "three.js")]

FILES = {
    "robots": ["public/robots.txt", "static/robots.txt", "robots.txt", "app/robots.ts", "app/robots.js",
               "src/app/robots.ts", "src/app/robots.js"],
    "sitemap": ["public/sitemap.xml", "static/sitemap.xml", "sitemap.xml", "app/sitemap.ts", "app/sitemap.js",
                "src/app/sitemap.ts", "src/app/sitemap.js", "next-sitemap.config.js", "next-sitemap.config.cjs"],
    "favicon": ["public/favicon.ico", "public/favicon.svg", "public/favicon.png", "static/favicon.ico",
                "favicon.ico", "app/favicon.ico", "app/icon.png", "app/icon.svg", "app/icon.tsx",
                "src/app/favicon.ico", "src/app/icon.png", "src/app/icon.svg", "assets/favicon.png"],
    "apple-touch-icon": ["public/apple-touch-icon.png", "app/apple-icon.png", "src/app/apple-icon.png",
                         "apple-touch-icon.png"],
    "manifest": ["public/site.webmanifest", "public/manifest.json", "public/manifest.webmanifest",
                 "app/manifest.ts", "app/manifest.js", "src/app/manifest.ts", "manifest.json"],
    "og-image": ["app/opengraph-image.png", "app/opengraph-image.tsx", "src/app/opengraph-image.png",
                 "src/app/opengraph-image.tsx", "public/og.png", "public/og-image.png", "public/og.jpg"],
    "not-found": ["app/not-found.tsx", "src/app/not-found.tsx", "pages/404.tsx", "pages/404.js",
                  "src/pages/404.astro", "src/pages/404.tsx", "public/404.html", "404.html", "app/+not-found.tsx"],
    "llms.txt": ["public/llms.txt", "static/llms.txt", "llms.txt"],
    "app-links": ["public/.well-known/assetlinks.json", "public/.well-known/apple-app-site-association"],
    "redirect-config": ["vercel.json", "netlify.toml", "public/_redirects", "_redirects", "next.config.js",
                        "next.config.mjs", "next.config.ts", "astro.config.mjs", "firebase.json"],
}

PATTERNS = {
    "title": r"<title[\s>]|\btitle\s*:|generateMetadata|<Head\b|react-helmet|useHead\(|useSeoMeta",
    "meta description": r"name=[\"']description|\bdescription\s*:",
    "open graph": r"og:title|og:image|openGraph\s*:",
    "twitter card": r"twitter:card|\btwitter\s*:\s*\{",
    "canonical": r"rel=[\"']canonical|\bcanonical\s*:",
    "metadataBase": r"metadataBase",
    "html lang": r"<html[^>]*\blang=",
    "viewport": r"name=[\"']viewport|\bviewport\s*[:=]",
    "json-ld": r"application/ld\+json",
    "hreflang": r"hreflang|alternates\s*:\s*\{[^}]*languages|\blanguages\s*:",
    "noindex": r"noindex|index\s*:\s*false",
    "robots meta": r"name=[\"']robots|\brobots\s*:",
    "favicon link": r"rel=[\"'](?:shortcut )?icon|apple-touch-icon",
    "search console verify": r"google-site-verification|verification\s*:\s*\{",
    "analytics": r"gtag\(|googletagmanager|plausible|@vercel/analytics|posthog|umami|fathom",
    "h1": r"<h1[\s>]",
    "font-display": r"font-display|next/font",
    "ai crawler rules": r"GPTBot|ClaudeBot|PerplexityBot|Google-Extended|CCBot",
}
IMG_NO_ALT = re.compile(r"<(?:img|Image)\b(?![^>]*\balt\s*=)[^>]*>", re.S)


def detect_stack(root):
    out = []
    for pkg in [root / "package.json", *root.glob("*/package.json")]:
        try:
            data = json.loads(pkg.read_text())
        except Exception:
            continue
        deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
        names = [label for key, label in FRAMEWORKS if key in deps]
        hp = data.get("homepage")
        out.append(f"{pkg.relative_to(root)}: {', '.join(names) or 'no known framework'}"
                   + (f" · homepage {hp}" if hp else ""))
        if "next" in deps:
            app = any((root / d).is_dir() for d in ["app", "src/app"])
            pages = any((root / d).is_dir() for d in ["pages", "src/pages"])
            out.append(f"  next router: {'app' if app else ''}{' + ' if app and pages else ''}{'pages' if pages else ''}")
        if "expo" in deps:
            app_json = root / "app.json"
            if app_json.exists() and '"output"' in app_json.read_text():
                out.append("  expo web.output set (check static vs single)")
    if not out:
        n = len(list(root.glob("*.html")))
        out.append(f"no package.json; {n} top-level html file(s)")
    return out


def walk(root):
    for p in root.rglob("*"):
        if any(part in SKIP_DIRS for part in p.relative_to(root).parts):
            continue
        if p.is_file() and p.suffix in SRC_EXT and p.stat().st_size < MAX_BYTES and "lock" not in p.name:
            yield p


def scan_code(root):
    print(f"# codebase: {root}\n\n## stack")
    for line in detect_stack(root):
        print(f"- {line}")

    # match candidates anywhere in the tree so monorepos and nested sites (web/, site/) count
    all_files = [p.relative_to(root).as_posix() for p in root.rglob("*")
                 if not any(part in SKIP_DIRS for part in p.relative_to(root).parts)]
    print("\n## files")
    for key, cands in FILES.items():
        found = [f for f in all_files if any(f == c or f.endswith("/" + c) for c in cands)]
        print(f"- {key}: {', '.join(found[:6]) if found else 'MISSING'}")

    hits = {k: [] for k in PATTERNS}
    no_alt, h1_per_file = [], {}
    for p in walk(root):
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        rel = p.relative_to(root)
        if p.suffix in (".md", ".txt"):
            continue  # docs and notes mention SEO terms; only files list cares about these
        for i, line in enumerate(text.splitlines(), 1):
            for k, pat in PATTERNS.items():
                if re.search(pat, line):
                    hits[k].append(f"{rel}:{i}")
        for m in IMG_NO_ALT.finditer(text):
            no_alt.append(f"{rel}:{text.count(chr(10), 0, m.start()) + 1}")
        c = len(re.findall(r"<h1[\s>]", text))
        if c:
            h1_per_file[str(rel)] = c

    print("\n## patterns (count · first hits)")
    for k, v in hits.items():
        print(f"- {k}: {len(v)}" + (f" · {', '.join(v[:5])}" if v else ""))
    print(f"- img/Image without alt: {len(no_alt)}" + (f" · {', '.join(no_alt[:8])}" if no_alt else ""))
    multi = {f: c for f, c in h1_per_file.items() if c > 1}
    if multi:
        print(f"- files with >1 h1: {', '.join(f'{f} ({c})' for f, c in list(multi.items())[:8])}")


class Head(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags, self.title, self._t, self.h1, self.text = [], "", False, 0, 0
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("meta", "link"):
            self.tags.append((tag, a))
        elif tag == "html" and "lang" in a:
            self.tags.append(("html", a))
        elif tag == "script" and a.get("type") == "application/ld+json":
            self.tags.append(("ld+json", a))
        elif tag == "title":
            self._t = True
        elif tag == "h1":
            self.h1 += 1
        if tag in ("script", "style"):
            self._skip += 1

    def handle_endtag(self, tag):
        if tag == "title":
            self._t = False
        if tag in ("script", "style") and self._skip:
            self._skip -= 1

    def handle_data(self, data):
        if self._t:
            self.title += data
        elif not self._skip:
            self.text += len(data.strip())


def fetch(url, method="GET"):
    req = urllib.request.Request(url, method=method, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            body = r.read(MAX_BYTES * 3).decode("utf-8", errors="ignore") if method == "GET" else ""
            return r.status, r.geturl(), dict(r.headers), body
    except urllib.error.HTTPError as e:
        return e.code, url, dict(e.headers), ""
    except Exception as e:
        return None, url, {}, str(e)


def scan_live(url):
    base = url.rstrip("/")
    print(f"\n# live: {url}")
    status, final, headers, body = fetch(url)
    print(f"- home: {status} · final url {final}")
    for h in ("x-robots-tag", "content-encoding", "cache-control", "strict-transport-security"):
        if h in {k.lower() for k in headers}:
            v = next(v for k, v in headers.items() if k.lower() == h)
            print(f"- header {h}: {v}")
    p = Head()
    p.feed(body)
    print(f"- title ({len(p.title.strip())} chars): {p.title.strip()!r}")
    for tag, a in p.tags:
        key = a.get("name") or a.get("property") or a.get("rel") or a.get("hreflang") or ""
        if tag == "html":
            print(f"- html lang: {a.get('lang')}")
        elif tag == "ld+json":
            print("- json-ld block present")
        elif tag == "meta" and re.match(r"(description|robots|viewport|og:|twitter:|google-site)", key):
            print(f"- meta {key}: {a.get('content', '')[:120]!r}")
        elif tag == "link" and re.search(r"canonical|icon|alternate|manifest", str(key)):
            print(f"- link {key}: {a.get('href')}" + (f" hreflang={a['hreflang']}" if "hreflang" in a else ""))
    print(f"- h1 count in raw html: {p.h1} · visible text chars in raw html: {p.text}"
          + ("  <- likely client-rendered shell" if p.text < 300 else ""))

    for path in ("/robots.txt", "/sitemap.xml", "/llms.txt", "/favicon.ico", "/site.webmanifest",
                 "/.well-known/assetlinks.json", "/this-page-should-404-seo-scan"):
        s, f, _, b = fetch(base + path)
        extra = ""
        if path == "/robots.txt" and s == 200:
            extra = " · " + " | ".join(l.strip() for l in b.splitlines() if l.strip() and not l.startswith("#"))[:300]
        print(f"- {path}: {s}{'' if f == base + path else f' -> {f}'}{extra}")

    host = re.sub(r"^https?://", "", base).split("/")[0]
    bare = host[4:] if host.startswith("www.") else host
    for v in (f"http://{bare}", f"http://www.{bare}", f"https://{bare}", f"https://www.{bare}"):
        s, f, _, _ = fetch(v, "HEAD")
        print(f"- variant {v}: {s} -> {f}")


def main():
    args = sys.argv[1:]
    url = None
    if "--url" in args:
        i = args.index("--url")
        url = args[i + 1]
        del args[i:i + 2]
    root = Path(args[0] if args else ".").expanduser().resolve()
    if args or not url:
        scan_code(root)
    if url:
        scan_live(url)


if __name__ == "__main__":
    main()
