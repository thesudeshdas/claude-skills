# fixes

How to close each gap, by stack, and the prompt templates the doc hands to the user. Always check the framework's current docs before quoting an API: these names were right when written and can drift.

## stack cheat sheet

| need | Next.js (app router) | Next.js (pages) | Astro | Vite/CRA SPA | static HTML |
|---|---|---|---|---|---|
| title/description | `export const metadata` / `generateMetadata` | `next/head` | `<head>` in layout, props per page | `react-helmet-async` or `@unhead/react` + prerender | `<head>` per file |
| canonical | `alternates.canonical` + `metadataBase` | `<link rel="canonical">` | `Astro.url` → link tag | prerender + helmet | link tag |
| robots.txt | `app/robots.ts` | `public/robots.txt` | `public/robots.txt` | `public/robots.txt` | root file |
| sitemap | `app/sitemap.ts` | `next-sitemap` | `@astrojs/sitemap` | `vite-plugin-sitemap` / build script | hand or generator |
| OG image | `opengraph-image.tsx` (ImageResponse) | `@vercel/og` API route | static file or `astro-og-canvas` | static file | static file |
| icons | `app/icon.png`, `app/apple-icon.png`, `app/favicon.ico` | `public/` + `<link>` | `public/` + `<link>` | `public/` + `<link>` | root + `<link>` |
| manifest | `app/manifest.ts` | `public/site.webmanifest` | `public/` | `public/` | root |
| JSON-LD | `<script type="application/ld+json">` in the page component | same via `next/head` | `<script type="application/ld+json" set:html={…}>` | same, prerendered | inline script |
| SSR/prerender | default (server components) | `getStaticProps` | default static | `vite-plugin-ssr`/Vike, `react-snap`, or move to a framework | already static |

Expo web / React Native Web: treat as SPA. Use `expo-router` static rendering (`web.output: "static"`) and `<Head>` from `expo-router/head`.

## guide shape for each gap

Inside the doc, every `missing`/`partial` item gets a `details` block:

1. **why it matters**: one or two lines, cite a source
2. **what to do here**: steps specific to this repo's stack and paths, with a short code sample in `pre[data-lang]`
3. **how to verify**: a command, URL or tool (curl, Rich Results Test, Lighthouse, view-source)
4. **prompt**: a filled template below in `pre data-lang="prompt"` (the copy button comes from research.js)

## prompt templates

Fill every `<…>` with real values. Prompts are in normal sentence case (they go to an agent, not into the doc's prose voice), but keep them short.

### generic
```
In <repo path>, a <framework + version> project, add <item>. Current state: <what exists, file:line>. Requirements: <bullets from the checklist row>. Don't change unrelated files. When done, show me how to verify it: <verify step>.
```

### metadata (B1, B2, A4, C1, C2)
```
In <repo>, add per-page SEO metadata using <API, e.g. Next.js generateMetadata>. Set metadataBase to <prod URL>. Each route in <list of routes> needs a unique title (<=60 chars, "<Page> | <Brand>"), a meta description (120-160 chars), a self-referencing canonical, Open Graph (title, description, 1200x630 image, url, type) and twitter:card summary_large_image. Pull values from <data source> where pages are dynamic. Then list each route with its final title and description so I can review the copy.
```

### robots + sitemap (A1, A2, I1)
```
In <repo>, add robots.txt and an XML sitemap using <framework mechanism>. The sitemap must include every indexable route (<static routes>, plus dynamic ones from <data source>) with lastmod. robots.txt should allow all, disallow <private paths>, <allow|block> AI crawlers (GPTBot, ClaudeBot, PerplexityBot, Google-Extended), and point to <prod URL>/sitemap.xml. Make sure non-production deployments send noindex instead.
```

### structured data (D1, D2, H4)
```
In <repo>, add JSON-LD structured data. Home page: Organization (name <name>, url, logo <logo URL>, sameAs <social URLs>) and WebSite (name, url). <Template> pages: <schema type> using fields from <data source>. Render it server-side in the page's HTML. Afterwards give me one URL per template to test in Google's Rich Results Test.
```

### rendering (A7)
```
<repo> is a client-rendered <framework> app, so crawlers see an empty shell. Propose the smallest change that serves real HTML for <public routes>: options are prerendering at build, SSG, or SSR. Pick one for this stack, explain the tradeoff in 3 lines, then implement it for <routes> and show me the raw HTML diff before/after.
```

### icons + manifest (H1, H2, H3)
```
In <repo>, set up site icons from <source logo file>: favicon.ico (48x48), a square PNG or SVG icon at a multiple of 48px, apple-touch-icon 180x180, and a web manifest (name <name>, short_name, theme_color <hex>, icons 192 and 512). Use <framework mechanism>. Make sure the home page HTML declares them with link tags and robots.txt doesn't block them.
```

### performance (E1 to E3)
```
In <repo>, fix the Core Web Vitals issues on <page>: <specific findings, e.g. LCP image not prioritized at file:line, 3 font weights, 400KB client bundle>. Keep visuals identical. Report before/after Lighthouse mobile scores for LCP, CLS and INP (or TBT as a lab proxy).
```

### content (B3, B4, B7)
```
Review <routes/files> in <repo> for on-page SEO: exactly one h1 per page, logical h2/h3 order, alt text on meaningful images (empty alt on decorative ones), and enough crawlable text explaining <what the product is> for someone searching "<target query>". Suggest copy changes as a list first; only edit after I approve.
```

## off-site and manual steps (for section "outside the code")

- verify the domain in Google Search Console (DNS TXT is easiest), submit the sitemap, check page indexing + core web vitals reports
- same for Bing Webmaster Tools (can import from Search Console)
- request indexing for the home page after launch
- backlinks, directories, launch posts, Google Business Profile for local businesses
