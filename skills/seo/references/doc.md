# doc structure

Start from the research skeleton. Set `<span class="type" data-type="seo">seo</span>`, `<meta name="research:type" content="seo">`, and `research:project` to the project name. Title like "seo audit: <project>" (lowercase). Build only with classes from the research components reference.

Sections, in order. Drop one only if it would be empty.

1. **tl;dr**
   - `.stats`: done, partial, missing, unknown counts (n/a left out)
   - `.tldr` list: the top 3 fixes by impact, one line each
2. **scope**
   - `dl.facts`: target (path and/or URL), stack + rendering mode, pages/routes checked, how (code read, scan.py, live fetch), date
   - one line on what wasn't checked and why (no Search Console access, no live URL…)
3. **scorecard**: one `.table-wrap` table, one row per category (A to K): category, done/total, worst open severity chip
4. **checklist**: one `h3` per category, then a `.table-wrap` table with columns: id, item, status, evidence, severity
   - status cell: `td.yes` done · `td.meh` partial · `td.no` missing · plain `td` with `n/a` or `unknown` + short reason
   - evidence: `<code>file:line</code>`, URL, or header value. Empty only for missing
   - severity: `.chip.high` / `.chip.med` / `.chip.low`
5. **fix guides**: one `details` per missing/partial item, sorted high → low severity. Summary: `<id> <item>` plus a severity chip. Body per the "guide shape" in fixes.md, ending with the prompt in `<pre data-lang="prompt"><code>…</code></pre>`
6. **quick wins**: `ul.checks` of fixes that take under ~15 min
7. **outside the code**: `ul.checks` for Search Console, Bing, backlinks etc. Mark `.done` only if verified
8. **sources**: `ol.sources` with the Google/framework pages actually cited, cite inline with `sup.ref`

Escape `<`, `>`, `&` inside `pre`/`code`. Prompts can contain capitals and periods (they're code-like payloads), the rest follows the lowercase voice.
