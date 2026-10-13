#!/usr/bin/env python3
"""Quick launch-readiness signal scan for a codebase and/or a live URL.

Usage: scan.py [repo-path] [--url https://example.com]

Prints the detected stack, a guessed project type, launch-related files that
exist, and pattern hits with file:line (analytics events, error tracking,
flags, legal pages, secrets...), plus live headers when --url is given.
It's a starting point for the check: confirm every hit by reading the code.
"""
import json
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

SKIP_DIRS = {"node_modules", ".git", ".next", "dist", "build", "out", ".output", ".vercel",
             ".netlify", "coverage", "vendor", ".expo", ".turbo", ".cache", ".svelte-kit",
             "Pods", "android", "ios", "__pycache__", ".venv", "venv", "Library", "Temp", ".godot"}
SRC_EXT = {".html", ".htm", ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".astro", ".vue",
           ".svelte", ".json", ".toml", ".yml", ".yaml", ".py", ".gd", ".cs", ".swift", ".kt",
           ".rb", ".go", ".css", ".webmanifest", ".env", ".sql"}
MAX_BYTES = 400_000
UA = "Mozilla/5.0 (compatible; launch-skill-scan/1.0)"

TYPES = {
    "game": ["phaser", "pixi.js", "three", "kaboom", "kaplay", "excalibur", "@babylonjs/core", "playcanvas",
             "matter-js", "planck"],
    "mobile app": ["expo", "react-native"],
    "web app": ["next", "@remix-run/react", "@sveltejs/kit", "nuxt", "@tanstack/react-router",
                "react-router-dom", "convex", "@supabase/supabase-js", "firebase", "prisma", "drizzle-orm"],
    "backend/API": ["express", "fastify", "@nestjs/core", "hono", "koa", "@trpc/server"],
    "static site": ["astro", "@11ty/eleventy", "gatsby", "vitepress", "@docusaurus/core"],
}
PY_BACKEND = ["django", "fastapi", "flask"]

FILES = {
    "privacy page": ["privacy", "privacy-policy"],
    "terms page": ["terms", "tos", "terms-of-service"],
    "404 page": ["404", "not-found", "+not-found"],
    "health route": ["health", "healthz", "status"],
    "changelog": ["CHANGELOG", "changelog", "releases"],
    "credits/licenses": ["CREDITS", "credits", "LICENSE", "ATTRIBUTION"],
    "press kit": ["press", "presskit"],
    "ci workflows": [".github/workflows"],
    "host config": ["vercel.json", "netlify.toml", "_headers", "_redirects", "firebase.json", "fly.toml",
                    "render.yaml", "wrangler.toml", "Dockerfile", "eas.json", "app.json"],
    "migrations": ["migrations", "prisma/migrations", "drizzle", "supabase/migrations"],
    "sentry config": ["sentry.client.config", "sentry.server.config", "sentry.properties",
                      "instrumentation.ts", "instrumentation-client.ts"],
    "service worker / manifest": ["sw.js", "service-worker", "manifest.json", "site.webmanifest"],
    "feed / rss": ["feed.xml", "rss.xml", "atom.xml"],
}

PATTERNS = {
    # A. analytics
    "analytics sdk": r"posthog|plausible|umami|fathom|@vercel/analytics|amplitude|mixpanel|segment|"
                     r"gameanalytics|googletagmanager|gtag\(|firebase/analytics|@react-native-firebase/analytics|"
                     r"cloudflareinsights|aptabase|telemetrydeck",
    "event calls": r"\b(?:track|capture|logEvent|trackEvent|addProgressionEvent|addDesignEvent)\s*\(|"
                   r"gtag\(\s*['\"]event|plausible\(\s*['\"]",
    "identify": r"\.identify\(|\.alias\(|setUserId\(",
    "progression words": r"level_?(?:start|complete|fail|end)|game_?over|onLevel(?:Start|Complete)|"
                         r"tutorial_|session_?start",
    # B. errors
    "error tracking sdk": r"@sentry/|sentry_sdk|bugsnag|rollbar|crashlytics|honeybadger|posthog\.captureException",
    "global error handlers": r"window\.onerror|addEventListener\(\s*['\"](?:error|unhandledrejection)|"
                             r"ErrorBoundary|componentDidCatch|process\.on\(\s*['\"]uncaught|global-error",
    "release tag": r"\brelease\s*:|SENTRY_RELEASE|appVersion|APP_VERSION",
    # C. uptime
    "health handler": r"['\"/]health(?:z|check)?['\"/]",
    # F. security
    "rate limit": r"rate.?limit|ratelimit|@upstash/ratelimit|express-rate-limit|throttle",
    "security headers": r"Content-Security-Policy|X-Content-Type-Options|X-Frame-Options|frame-ancestors|"
                        r"Strict-Transport-Security|helmet\(",
    "auth": r"getServerSession|auth\(\)|clerk|next-auth|@auth/|supabase\.auth|lucia|requireAuth|"
            r"isAuthenticated|row level security|enable row level",
    "validation": r"\bzod\b|from ['\"]zod|yup|valibot|joi\b|pydantic",
    "captcha": r"turnstile|recaptcha|hcaptcha",
    # G. privacy
    "consent": r"cookie.?consent|cookiebot|klaro|onetrust|consent\s*\(|cookieless",
    "account deletion": r"delete.?account|deleteUser|account.?deletion",
    # H. feedback
    "feedback path": r"mailto:|feedback|report.?a.?bug|discord\.gg|tally\.so|forms\.gle|canny",
    # I. rollback / release
    "feature flags": r"feature.?flag|isFeatureEnabled|getFeatureFlag|useFeatureFlag|launchdarkly|growthbook|"
                     r"statsig|unleash|remote.?config",
    "ota updates": r"expo-updates|Updates\.checkForUpdate|codepush",
    "version shown": r"\bversion\b.*(?:footer|about|settings)|__APP_VERSION__|process\.env\.npm_package_version",
    # J. data safety
    "save data": r"localStorage\.setItem|AsyncStorage\.setItem|indexedDB|saveGame|save_game|SAVE_KEY",
    "save version": r"saveVersion|SAVE_VERSION|save_version|schemaVersion|migrateSave",
    # K. devices
    "viewport meta": r"name=[\"']viewport",
    "visibility pause": r"visibilitychange|document\.hidden|onPause|AppState",
    "touch input": r"touchstart|pointerdown|onTouch|input\.addPointer|activePointers",
    "audio unlock": r"AudioContext|\.resume\(\)|unlock(?:Audio)?|sound\.locked",
    "device pixel ratio": r"devicePixelRatio|resolution\s*:|Scale\.(?:FIT|RESIZE)",
    "reduced motion": r"prefers-reduced-motion|reduceMotion|reducedMotion",
    # L. sharing
    "og tags": r"og:title|og:image|openGraph\s*:",
    # N. cost
    "paid apis": r"openai|@anthropic-ai|anthropic|replicate|resend|sendgrid|twilio|stripe|mapbox|"
                 r"googleapis|elevenlabs",
}

SECRET_PATTERNS = {
    "private key": r"-----BEGIN (?:RSA |EC )?PRIVATE KEY-----",
    "aws key": r"AKIA[0-9A-Z]{16}",
    "stripe live key": r"sk_live_[0-9a-zA-Z]{10,}",
    "openai/anthropic key": r"sk-(?:ant-|proj-)?[A-Za-z0-9_-]{20,}",
    "secret in public env": r"(?:NEXT_PUBLIC|EXPO_PUBLIC|VITE|PUBLIC|REACT_APP)_[A-Z_]*(?:SECRET|PRIVATE|SERVICE_ROLE)",
}


def load_pkgs(root):
    pkgs = []
    for pkg in [root / "package.json", *root.glob("*/package.json"), *root.glob("apps/*/package.json")]:
        try:
            data = json.loads(pkg.read_text())
        except Exception:
            continue
        deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
        pkgs.append((pkg.relative_to(root), data, deps))
    return pkgs


def guess_types(root, pkgs):
    found = []
    for _, _, deps in pkgs:
        for t, keys in TYPES.items():
            hits = [k for k in keys if k in deps]
            if hits:
                found.append(f"{t} ({', '.join(hits)})")
    if (root / "project.godot").exists():
        found.append("game (godot)")
    if (root / "ProjectSettings").is_dir():
        found.append("game (unity)")
    for req in ("requirements.txt", "pyproject.toml"):
        f = root / req
        if f.exists():
            txt = f.read_text(errors="ignore").lower()
            hits = [k for k in PY_BACKEND if k in txt]
            if hits:
                found.append(f"backend/API ({', '.join(hits)})")
    if not found:
        html = [p for p in root.rglob("*.html") if not any(s in p.parts for s in SKIP_DIRS)]
        canvas = any("<canvas" in p.read_text(errors="ignore") for p in html[:50])
        found.append(f"static site ({len(html)} html files)" + (", has <canvas>: maybe a game" if canvas else ""))
    return found


def walk(root):
    for p in root.rglob("*"):
        if any(part in SKIP_DIRS for part in p.relative_to(root).parts):
            continue
        if p.is_file() and (p.suffix in SRC_EXT or p.name.startswith(".env")) \
                and p.stat().st_size < MAX_BYTES and "lock" not in p.name:
            yield p


def git_tracked_env(root):
    try:
        out = subprocess.run(["git", "-C", str(root), "ls-files"], capture_output=True, text=True, timeout=10)
    except Exception:
        return None
    if out.returncode != 0:
        return None
    return [f for f in out.stdout.splitlines()
            if re.search(r"(^|/)\.env(\.|$)", f) and not re.search(r"example|sample|template", f)]


def scan_code(root):
    print(f"# codebase: {root}\n\n## stack")
    pkgs = load_pkgs(root)
    for rel, data, deps in pkgs:
        print(f"- {rel}: {len(deps)} deps · version {data.get('version', 'none')}")
    if not pkgs:
        print("- no package.json")
    print("\n## guessed type (confirm by reading)")
    for t in guess_types(root, pkgs):
        print(f"- {t}")

    for name in ("CLAUDE.md", "README.md", "AGENTS.md"):
        if (root / name).exists():
            print(f"- read {name} for constraints (CSP, hosting, no-JS rules)")

    all_files = [p.relative_to(root).as_posix() for p in root.rglob("*")
                 if not any(part in SKIP_DIRS for part in p.relative_to(root).parts)]
    print("\n## files")
    for key, cands in FILES.items():
        found = [f for f in all_files
                 if any(re.search(rf"(^|/){re.escape(c)}(/|\.|$)", f) for c in cands)]
        print(f"- {key}: {', '.join(found[:6]) if found else 'MISSING'}")

    tracked = git_tracked_env(root)
    if tracked is None:
        print("- tracked .env files: unknown (not a git repo)")
    else:
        print(f"- tracked .env files: {', '.join(tracked) if tracked else 'none'}")

    hits = {k: [] for k in PATTERNS}
    secrets = {k: [] for k in SECRET_PATTERNS}
    for p in walk(root):
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        rel = p.relative_to(root)
        for i, line in enumerate(text.splitlines(), 1):
            if len(line) > 2000 and p.suffix in (".js", ".mjs", ".cjs", ".css"):
                continue  # minified bundles
            for k, pat in PATTERNS.items():
                if re.search(pat, line, re.I if k not in ("event calls",) else 0):
                    hits[k].append(f"{rel}:{i}")
            for k, pat in SECRET_PATTERNS.items():
                if re.search(pat, line):
                    secrets[k].append(f"{rel}:{i}")

    print("\n## patterns (count · first hits)")
    for k, v in hits.items():
        print(f"- {k}: {len(v)}" + (f" · {', '.join(v[:6])}" if v else ""))
    print("\n## possible secrets (verify; never print values)")
    any_secret = False
    for k, v in secrets.items():
        if v:
            any_secret = True
            print(f"- {k}: {len(v)} · {', '.join(v[:6])}")
    if not any_secret:
        print("- none matched")


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
    low = {k.lower(): v for k, v in headers.items()}
    for h in ("content-security-policy", "strict-transport-security", "x-content-type-options",
              "x-frame-options", "referrer-policy", "permissions-policy", "cache-control", "server"):
        print(f"- header {h}: {low.get(h, 'MISSING')[:200]}")
    for k, pat in (("analytics in html", PATTERNS["analytics sdk"]),
                   ("error sdk in html", PATTERNS["error tracking sdk"]),
                   ("og tags", PATTERNS["og tags"]), ("viewport", PATTERNS["viewport meta"]),
                   ("feedback link", r"mailto:|feedback|discord\.gg")):
        print(f"- {k}: {'yes' if re.search(pat, body, re.I) else 'no'}")
    for path in ("/privacy", "/terms", "/health", "/api/health", "/this-page-should-404-launch-scan"):
        s, f, _, _ = fetch(base + path)
        print(f"- {path}: {s}{'' if f == base + path else f' -> {f}'}")


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
