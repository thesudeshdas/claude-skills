# doc structure

Start from the research skeleton. Set `<span class="type" data-type="launch">launch</span>`, `<meta name="research:type" content="launch">`, and `research:project` to the project name. Title like "launch check: <project>" (lowercase). Build only with classes from the research components reference.

Sections, in order. Drop one only if it would be empty.

1. **tl;dr**
   - `.stats`: done, partial, missing, you confirm counts (n/a left out)
   - `.tldr` list: the launch blockers (high severity gaps), one line each. If there are none, say so and list the top 3 reminders
2. **scope**
   - `dl.facts`: target (path, branch and/or URL), project type, stack, how (code read, scan.py, live fetch), date
   - one line listing the categories marked n/a for this type and why
3. **what you'll see on day one**: a short paragraph plus a `.table-wrap` table of the analytics events: event, where it fires (`file:line` or "missing"), status. Then the funnel as `.flow` or `ol.steps` (landing → … → goal), marking steps that can't be measured yet. This is the section the user cares about most, keep it concrete
4. **scorecard**: one `.table-wrap` table, one row per category that applies: category, done/total, worst open severity chip
5. **checklist**: one `h3` per category that applies, then a `.table-wrap` table with columns: id, item, status, evidence, severity
   - status cell: `td.yes` done · `td.meh` partial · `td.no` missing · plain `td` with `n/a` or `you confirm` + short reason
   - evidence: `<code>file:line</code>`, URL, or header value. Empty only for missing
   - severity: `.chip.high` / `.chip.med` / `.chip.low`
6. **fix guides**: one `details` per missing/partial item, sorted high → low severity. Summary: `<id> <item>` plus a severity chip. Body per the "guide shape" in fixes.md, ending with the prompt in `<pre data-lang="prompt"><code>…</code></pre>`
7. **quick wins**: `ul.checks` of fixes that take under ~15 min
8. **before you hit publish**: `ul.checks` of the `you confirm` items and the manual steps from fixes.md ("outside the code"). Mark `.done` only if verified
9. **sources**: `ol.sources` with the pages actually cited, cite inline with `sup.ref`

Escape `<`, `>`, `&` inside `pre`/`code`. Prompts can contain capitals and periods (they're code-like payloads), the rest follows the lowercase voice.
