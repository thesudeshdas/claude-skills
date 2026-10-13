# sources

Where to look and how much to trust what you find. **A wrong source is worse than no source.**

## tiers

Trust depends on the claim. A vendor's docs are tier A for "how does their API work" and tier C for "is their product better than X".

**tier A: primary, trust first**
- official docs, specs, standards, RFCs, API references for the thing itself
- source code, and its issues, PRs and discussions (what the code does and what maintainers say)
- release notes, changelogs, migration guides (what changed, current version)
- peer-reviewed papers and the original preprint for research claims
- official pricing and status pages, filings, government and standards-body data
- the user's own codebase, logs and data

**tier B: credible secondary, verify key claims**
- engineering blogs from teams describing their own production use
- well-known practitioners writing from first-hand experience, with specifics
- reputable tech press and analysts, with dates
- conference talks and their slides
- maintained, high-quality community resources (MDN, well-kept wikis, awesome lists as pointers only)

**tier C: signal, never sole evidence**
- forum threads, Reddit, Hacker News, X, Discord, Stack Overflow answers (good for "what do people actually hit", weak for facts. Engagement is not accuracy)
- vendor marketing and comparison pages written by one of the products compared
- tutorials and listicles without first-hand detail, aggregator and directory sites

**avoid**
- SEO content farms, AI-generated roundups, pages that rephrase other pages without adding anything
- undated pages for anything time-sensitive
- anything you only saw as a search snippet

## freshness

- APIs, libraries, pricing, model capabilities, tools: prefer sources from the last 12 months, and check the changelog for anything newer than your source
- concepts, algorithms, architecture patterns: age matters less, prefer the original source
- always record the source's date in notes. If a page has no date, say so

## where to look

| question type | start here | then |
|---|---|---|
| how does library/API X work | official docs, API reference | GitHub repo source, issues, changelog |
| is X broken / known bug | GitHub issues and PRs (`gh search issues`), changelog | Stack Overflow, forum threads |
| what changed in version N | release notes, migration guide | PRs and the diff |
| which tool/library should we use | official docs of each, GitHub (activity, issues, releases) | engineering blogs with production use, then forums for pain points |
| what do people think / real experience | Hacker News, Reddit, X, GitHub discussions | first-hand blog posts |
| how does our code do X | the codebase (grep, read, `git log`, `git blame`) | internal docs, then upstream library docs |
| academic / ML research | arXiv, Semantic Scholar, the paper's own repo | citing papers, author talks |
| market, pricing, companies | official pricing pages, filings, company announcements | reputable press and analysts |
| UI/UX patterns | live products, platform guidelines (Apple HIG, Material) | design case studies |
| security | vendor advisories, CVE entries, the fix commit | security researcher write-ups |

## tools, in order

1. **codebase tools** for anything about the user's code: grep, read, `git log`
2. **web search + web fetch** (built in) for most web research. Search finds, fetch confirms
3. **`gh`** for GitHub: `gh search repos|issues|code`, `gh api repos/<o>/<r>/releases`, `gh issue view`. More reliable than scraping github.com
4. **package registries** for versions and activity: `npm view <pkg>`, PyPI JSON (`https://pypi.org/pypi/<pkg>/json`)
5. **MCP search tools** (Exa, Firecrawl, Tavily, arXiv, Context7…) only if they're installed in this session. Don't assume they are

## recording a source

For every source you cite, keep: url, title, tier, date, and the specific claim it supports. In the doc, that becomes one `ol.sources` entry with a short "what it supports" note.
