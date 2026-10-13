---
name: seo
description: Audit a project, site or codebase for SEO and write the result as a styled HTML doc in ~/research that reuses the research skill's shared stylesheet. The doc is a checklist of every SEO area that should be considered, what is implemented (with file:line evidence), what is missing or partial, and for each gap a short how-to guide plus a copy-paste prompt to get it fixed. Covers crawl and index, on-page, social cards, structured data, performance, mobile, i18n, SERP appearance (favicon, site name), AI search and monitoring. Use when the user invokes /seo or asks for an SEO audit, SEO checklist or "what SEO are we missing".
---

# seo

Audit the target for SEO, then write one HTML file in `~/research/`. Same doc system as the research skill: content only, styling from `~/research/_assets/research.css` + `research.js`. **Never write CSS or JS in a doc.**

Shared pieces live in the research skill, read them from there:
- skeleton: `~/.claude/skills/research/assets/skeleton.html`
- components: `~/.claude/skills/research/references/components.md`
- voice: `~/.claude/skills/research/references/voice.md`
- citation check: `~/.claude/skills/research/scripts/check_sources.py`

## workflow

1. **find the target.** codebase (default: cwd), a live URL, or both. If the user gave a URL, audit it live too. If the codebase has a deployed URL in config/README/package.json `homepage`, ask once whether to include it; otherwise code only. Say which in one line
2. **scan.** run `python3 ~/.claude/skills/seo/scripts/scan.py <repo-path> [--url https://site]`. It prints stack, files found and pattern hits with `file:line`. It's a starting point, not the verdict: a hit can be dead code, a miss can be generated at runtime
3. **check every item** in [checklist](references/checklist.md):
   - confirm scan hits by reading the code (per page/route, not just once in the layout)
   - mark each item `done`, `partial`, `missing`, `n/a` (with a reason) or `unknown` (needs a live check or account access)
   - record evidence: `file:line`, a URL, or a header value. No evidence, no `done`
   - large repos: split by checklist category across 2 to 4 Explore subagents in one message; each returns item id, status, evidence, notes
4. **write the guides.** for every `missing` and `partial` item, pull the stack-specific how-to from [fixes](references/fixes.md) and fill a prompt from its templates with the real paths, framework and URLs
5. **install assets.** `bash ~/.claude/skills/research/scripts/setup.sh`
6. **write the doc** to `~/research/<yyyy-mm-dd>-seo-<project>.html` following [doc](references/doc.md). `data-type="seo"`. If the file exists for today, append `-2`
7. **rebuild the index.** `python3 ~/.claude/skills/research/scripts/index.py`
8. **check.** grep the file for `<style`, `style="`, `—`, `–`; fix hits. Run `check_sources.py <file>` and fix every `fix:` line. Re-read for voice
9. **open it and listen.** `bash ~/.claude/skills/research/scripts/serve.sh <file>.html`, `open` the URL it prints, then start a **Monitor** with command `python3 ~/.claude/skills/research/scripts/watch.py <file>.html`, description `questions on <file>`, timeout 1800000. Handle questions exactly as in the research skill's ask flow (`~/.claude/skills/research/SKILL.md`, "ask flow"): answer in chat, post with `answer.py`, confirm before any edit or side effect, re-arm silently on expiry
10. **reply** with the URL, target (code / live / both), the done/partial/missing counts and the top 3 fixes, plus "select any text in the doc and hit ask about this, i'll answer here". Under 100 words total. Details live in the doc

## rules

- **under 100 words in chat, always.** every chat reply, explanation and ask-flow answer stays under 100 words, whatever the question. Depth belongs in the doc, not chat
- **read-only audit.** never edit the audited project. The output is the doc; fixes happen when the user runs the prompts
- **honest status.** scan output alone never makes an item `done`. Anything needing Search Console, analytics or a live crawl you didn't do is `unknown`, not `missing`
- **fit the project.** mark items `n/a` when they truly don't apply (hreflang on a single-language site, Product schema on a blog). Don't pad
- **sources.** link Google Search Central or the framework's docs for each category's guidance. Guidance changes (FID became INP, HowTo rich results were dropped): anything version-specific must come from a page opened this session, never memory
- all research-skill rules apply: no animation, no inline styling, no new classes, lowercase voice, one doc per request
