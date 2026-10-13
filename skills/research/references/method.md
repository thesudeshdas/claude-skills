# method

How to do the research before writing anything. Read [sources](sources.md) alongside this.

## 0. date first

Check today's date (`date +%F`) before the first search. Put the current year into queries about anything that changes ("2026", "latest"), and never assume last year's state of a tool, price or API.

## 1. pick a depth

Set effort by these rules. Don't guess: over-researching a simple question and under-researching a broad one are both failures.

| depth | when | searches | subagents | outline checkpoint |
|---|---|---|---|---|
| **quick** | one fact, one API behaviour, "does X support Y" | 3 to 10 | none | no |
| **standard** | comparisons, "how should we do X", most approach/implementation/plan docs | 10 to 25 | 0 to 4, one per option or sub-question | no |
| **deep** | broad topics, market scans, critical decisions, "research everything about X" | 25+ | 4 to 8, clearly divided | yes |

If the user says "quick" or "deep", use that. Otherwise pick from the table and say the depth in one line when you start.

## 2. scope

Write down, for yourself:
- the actual question in one sentence, and what a good answer lets the user do
- 2 to 6 sub-questions that together answer it
- for comparisons and scans, the **items × fields** grid: what's being compared (items) and what you need to know about each (fields: pricing, limits, maturity, fit for this project…)
- what's out of scope

**deep only:** show the user the sub-questions (and grid, if any) as a short list and wait for a go or edits before searching. Quick and standard go straight on.

## 3. gather

- **broad, then narrow.** Start with short, general queries to see what exists, then focus. Long, very specific first queries tend to return nothing
- **one search is never the research.** Every sub-question gets at least two queries from different angles
- **open the source.** A search snippet is not evidence. Fetch the page before you cite it
- **match the source to the question.** Use the "where to look" table in [sources](sources.md)
- **run in parallel.** Fire independent searches and fetches in the same turn
- **codebase questions:** read the code first (grep, read, `git log`) and cite `file:line`. Web research only fills in what the code can't tell you

### subagents (standard and deep)

Split work by sub-question or by item, never so two agents cover the same ground. Launch them in one message so they run together. Every brief includes:

1. **objective:** the one sub-question, and why it matters to the main question
2. **context:** what the user is working on, constraints already known, today's date
3. **sources:** where to look and which tiers to trust (paste the relevant part of [sources](sources.md))
4. **boundaries:** what's out of scope and what other agents are covering
5. **output format:** findings as bullets, each with claim, source URL or `file:line`, source tier, date of source, and confidence (high, med, low). Plus a list of what couldn't be found

A brief like "research X" is too thin. Agents with thin briefs duplicate work and drift.

## 4. keep notes on disk (standard and deep)

Keep a scratch file at `~/research/_work/<slug>/notes.md` while gathering: one line per source (url, title, tier, date, what it supports) and findings under each sub-question. Subagent results get appended there too. This survives context compaction on long runs and becomes the sources section later. Quick depth can skip it.

## 5. triangulate

- every **key claim** (anything the recommendation rests on) needs 2 independent sources, or 1 tier A source. Two blogs copying the same press release count as one
- when sources disagree, prefer the higher tier and the newer date, and say so in the doc. Don't silently pick one
- version-specific or "current" behaviour must come from a source opened this session, never from memory. If you state something from memory, mark it unverified
- numbers (prices, limits, benchmarks, stars) need a source and a date

## 6. critique

Before writing, reread your findings as a skeptic:
- what would a practitioner who has used this in production push back on
- which sub-question has the thinnest evidence
- is anything resting only on vendor marketing, SEO pages or one forum post
- did anything important change recently (changelog, deprecation, pricing change)

If a key gap shows up, run a targeted round of follow-up searches (at most 2 rounds), then write. Gaps you can't close go in the doc's open questions or gaps section, stated plainly.

## 7. check citations

After writing the doc, run:

```sh
python3 ~/.claude/skills/research/scripts/check_sources.py ~/research/<file>.html
```

It flags sources that don't resolve and `<sup class="ref">` links that point at a missing source. Fix every hit. Then spot-check: each key claim's citation actually says what the doc claims it says. Drop or mark unverified any claim whose source doesn't hold up.

## when to stop

Stop gathering when every sub-question has an answer that meets the triangulation bar, or is listed as a gap after the critique rounds. More sources past that point don't improve the doc.
