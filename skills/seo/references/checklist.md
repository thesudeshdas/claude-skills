# checklist

Every item has an id, a default severity, and how to check it in code and live. Severity is the default; raise or lower it for the project (a missing sitemap on a 3-page site is low).

Status values: `done` · `partial` · `missing` · `n/a` (say why) · `unknown` (say what's needed to check)

## A. crawl and index

| id | item | sev | check in code | check live |
|---|---|---|---|---|
| A1 | robots.txt exists, allows what should rank, blocks nothing important (css/js, key pages) | high | `public/robots.txt`, `static/robots.txt`, `app/robots.ts` | `GET /robots.txt` |
| A2 | XML sitemap lists every indexable URL, auto-updated, referenced in robots.txt | med | `public/sitemap*.xml`, `app/sitemap.ts`, `next-sitemap`, `@astrojs/sitemap` | `GET /sitemap.xml`, `Sitemap:` line in robots |
| A3 | no accidental noindex (meta robots, `X-Robots-Tag`, env-gated staging flags leaking to prod) | high | grep `noindex`, `robots:` in metadata, headers config | meta + response headers |
| A4 | canonical URL on every indexable page, self-referencing, absolute | med | `rel="canonical"`, `alternates.canonical`, `metadataBase` | `<link rel=canonical>` |
| A5 | one host: HTTPS, http→https and www/non-www 301 to one version | high | redirect config (`next.config`, `vercel.json`, `netlify.toml`, `_redirects`) | curl `-I` the 4 variants |
| A6 | real status codes: 404 page returns 404, no soft 404s, no redirect chains | med | `not-found.tsx`, `404.html`, catch-all routes | curl a junk path |
| A7 | content present in server HTML (SSR/SSG/prerender), not only after client JS | high | framework + rendering mode; CSR-only SPA = partial at best | raw HTML has the body text |
| A8 | clean, stable URLs; consistent trailing slash; no session/tracking params in links | low | router config, `trailingSlash` | crawl links |
| A9 | internal linking: every page reachable via normal `<a href>` links, no orphan pages, nav not JS-only | med | links use `<a>`/`Link`, not `onClick` navigation | crawl from home |

## B. on-page

| id | item | sev | check in code | check live |
|---|---|---|---|---|
| B1 | unique, descriptive `<title>` per page (~50 to 60 chars, primary topic first, brand last) | high | metadata per route/template, not one global title | `<title>` across pages |
| B2 | unique meta description per page (~120 to 160 chars) | med | same as B1 | `meta[name=description]` |
| B3 | exactly one `h1` per page, logical h2/h3 order | med | grep `<h1`, heading components | count h1 |
| B4 | descriptive alt text on meaningful images, empty `alt=""` on decorative | med | `<img`/`<Image` without `alt` | scan imgs |
| B5 | descriptive link text (no "click here"), crawlable hrefs | low | grep link text | crawl |
| B6 | readable, slug-style URLs that match the content | low | route names | url list |
| B7 | real text content that matches search intent (not just a canvas/app shell) | high | landing pages have copy | view source |

## C. social cards

| id | item | sev | check in code | check live |
|---|---|---|---|---|
| C1 | Open Graph: `og:title`, `og:description`, `og:image` (1200x630, absolute URL), `og:url`, `og:type` | med | `openGraph`, `og:` tags, `opengraph-image.*` | meta tags, fetch the image |
| C2 | `twitter:card` (`summary_large_image`) + title/description/image | low | `twitter` metadata | meta tags |
| C3 | per-page OG images for shareable pages (posts, products, levels) | low | dynamic OG route / `@vercel/og` | compare pages |

## D. structured data

| id | item | sev | check in code | check live |
|---|---|---|---|---|
| D1 | `Organization` (logo, sameAs) and `WebSite` (name, url) JSON-LD on the home page | med | `application/ld+json` | Rich Results Test |
| D2 | type-specific schema where it earns a rich result: `Article`, `Product`, `SoftwareApplication`, `BreadcrumbList`, `VideoObject`, `Event`… | med | per-template JSON-LD | Rich Results Test |
| D3 | schema is valid and matches visible content | med | values come from the same data as the page | validator.schema.org |

## E. performance (core web vitals)

Targets at p75 (verify current values on web.dev): LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1

| id | item | sev | check in code | check live |
|---|---|---|---|---|
| E1 | images: modern formats, sized, `width`/`height` set, lazy below the fold, LCP image preloaded/priority | med | `next/image`, `astro:assets`, raw `<img>` | Lighthouse / PageSpeed |
| E2 | fonts: self-hosted or preconnected, `font-display: swap`, few weights | low | `next/font`, `@font-face` | Lighthouse |
| E3 | JS weight: code-split, no giant client bundles on landing pages, third-party scripts deferred | med | bundle analyzer, `"use client"` spread, script tags | Lighthouse |
| E4 | caching + compression + CDN for static assets | low | headers config, host | response headers |
| E5 | field data (CrUX) passes CWV | med | n/a | PageSpeed Insights field section, else `unknown` |

## F. mobile and accessibility overlap

| id | item | sev | check in code | check live |
|---|---|---|---|---|
| F1 | `<meta name="viewport" content="width=device-width, initial-scale=1">` | high | layout head | meta |
| F2 | responsive layout, readable font size, tap targets not cramped | med | CSS breakpoints | mobile Lighthouse |
| F3 | `<html lang="…">` set correctly | med | root layout | html tag |

## G. international (n/a for single-language sites)

| id | item | sev | check in code | check live |
|---|---|---|---|---|
| G1 | `hreflang` alternates for each locale + `x-default`, reciprocal | med | `alternates.languages`, i18n config | link tags / sitemap |
| G2 | locale in URL (subpath or subdomain), not cookie/IP-only switching | med | i18n routing | crawl |

## H. SERP appearance and brand

| id | item | sev | check in code | check live |
|---|---|---|---|---|
| H1 | favicon: square, multiple of 48px (48, 96, 144…) or SVG, stable crawlable URL, declared with `<link rel="icon">` on the home page | low | `favicon.ico`, `app/icon.*`, `<link rel="icon">` | `GET` the icon, robots doesn't block it |
| H2 | `apple-touch-icon` (180x180) | low | file + link tag | fetch |
| H3 | web app manifest (name, icons, theme_color) | low | `site.webmanifest`, `manifest.json`, `app/manifest.ts` | fetch |
| H4 | site name signal: `WebSite` JSON-LD `name` + consistent `og:site_name` | low | JSON-LD | Rich Results Test |

## I. AI search (GEO)

| id | item | sev | check in code | check live |
|---|---|---|---|---|
| I1 | deliberate AI crawler policy in robots.txt (GPTBot, ClaudeBot, PerplexityBot, Google-Extended…): allowed or blocked on purpose | low | robots.txt rules | robots |
| I2 | `llms.txt` (unofficial proposal, nice to have) | low | `public/llms.txt` | fetch |
| I3 | answer-shaped content: clear headings, direct factual answers, FAQ sections, up-to-date dates | low | content review | view page |

## J. monitoring (mostly outside the code)

| id | item | sev | check in code | check live |
|---|---|---|---|---|
| J1 | Google Search Console verified, sitemap submitted | high | verification meta/file (`google-site-verification`) | needs account: `unknown` unless verified |
| J2 | Bing Webmaster Tools | low | `msvalidate.01` | needs account |
| J3 | analytics installed (GA4, Plausible, Vercel Analytics…) | low | script/package | network tab |
| J4 | broken link / 404 monitoring | low | n/a | crawl |

## K. project-type extras (add when relevant)

- **web game / canvas app:** crawlable landing copy outside the canvas, one page per game/level with its own title + OG image, `VideoGame` or `SoftwareApplication` schema
- **mobile app with a site:** `/.well-known/assetlinks.json` (Android) and `apple-app-site-association` (iOS) for app links, smart app banner meta. App store listing (ASO) is a separate discipline; mention it, don't audit it
- **blog / content:** `Article` schema, author + dates, RSS feed, pagination, tag/category pages not thin or duplicated
- **ecommerce:** `Product` + `Offer` + reviews schema, faceted URL handling, out-of-stock handling
- **local business:** `LocalBusiness` schema, NAP consistency, Google Business Profile (off-site)

## sources to cite (open each before citing)

- seo starter guide: https://developers.google.com/search/docs/fundamentals/seo-starter-guide
- robots.txt: https://developers.google.com/search/docs/crawling-indexing/robots/intro
- sitemaps: https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview
- canonicals: https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls
- javascript seo: https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics
- title links: https://developers.google.com/search/docs/appearance/title-link
- snippets: https://developers.google.com/search/docs/appearance/snippet
- structured data: https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data
- core web vitals: https://web.dev/articles/vitals
- favicon: https://developers.google.com/search/docs/appearance/favicon-in-search
- site names: https://developers.google.com/search/docs/appearance/site-names
- hreflang: https://developers.google.com/search/docs/specialty/international/localized-versions
- open graph: https://ogp.me/
- llms.txt: https://llmstxt.org/
