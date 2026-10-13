---
name: launch
description: Pre-launch readiness check for a feature, project, website, game or app, written as a styled HTML doc in ~/research that reuses the research skill's shared stylesheet. The doc is a reminder checklist of everything that should be ready before real users arrive, filtered to the project type, with what is in place (file:line evidence), what is missing or partial, and for each gap a short how-to plus a copy-paste prompt. Covers product analytics and funnels (who plays, where they drop off), error and crash tracking, uptime alerts, performance, accessibility, security, privacy and legal, feedback loop, rollback, data safety, devices, sharing and discovery, launch comms and cost guards. Use when the user invokes /launch or asks "are we ready to launch", "pre-launch checklist", "what am I forgetting before going live".
---

# launch

Check the target against the launch checklist, then write one HTML file in `~/research/`. Same doc system as the research and seo skills: content only, styling from `~/research/_assets/research.css` + `research.js`. **Never write CSS or JS in a doc.**

This is a **reminder**, not a certification. The goal is that nothing gets forgotten: no game ships without knowing where players drop off, no site ships without a way to hear about errors. Keep it fast and practical.

Shared pieces live in the research skill, read them from there:
- skeleton: `~/.claude/skills/research/assets/skeleton.html`
- components: `~/.claude/skills/research/references/components.md`
- voice: `~/.claude/skills/research/references/voice.md`
- citation check: `~/.claude/skills/research/scripts/check_sources.py`

## workflow

1. **find the target.** codebase (default: cwd), a live URL, or both. A **feature** launch inside an existing product is fine too: ask for the branch, PR or folder, and scope the check to it. Say which in one line
2. **pick the project type** from [checklist](references/checklist.md) "project types": game, static site, web app, mobile app, backend/API, feature. Mixed is fine (game + landing site). Infer it from the scan; ask only if it's truly unclear
3. **scan.** run `python3 ~/.claude/skills/launch/scripts/scan.py <repo-path> [--url https://site]`. It prints stack, guessed type, files found and pattern hits with `file:line`. It's a starting point, not the verdict
4. **check every item that applies** in [checklist](references/checklist.md):
   - use the applicability table to skip whole categories (`n/a` with a one-line reason), don't pad
   - confirm scan hits by reading the code. An analytics SDK that's installed but sends no events is `partial`
   - for analytics, list the events that exist and the events the project type needs (see "events to expect"). Missing core events is the most common gap; call it out plainly
   - mark each item `done`, `partial`, `missing`, `n/a` (with a reason) or `you confirm` (can't be seen in code: billing alerts, backups restored, support inbox watched)
   - record evidence: `file:line`, a URL, or a header value. No evidence, no `done`
   - large repos: split by category across 2 to 4 Explore subagents in one message; each returns item id, status, evidence, notes
5. **seo.** don't repeat the seo audit. Do the 4 quick seo items in category L, then point to `/seo` for the full one
6. **write the guides.** for every `missing` and `partial` item, pull the how-to from [fixes](references/fixes.md) and fill a prompt from its templates with real paths, framework and URLs
7. **install assets.** `bash ~/.claude/skills/research/scripts/setup.sh`
8. **write the doc** to `~/research/<yyyy-mm-dd>-launch-<project>.html` following [doc](references/doc.md). `data-type="launch"`. If the file exists for today, append `-2`
9. **rebuild the index.** `python3 ~/.claude/skills/research/scripts/index.py`
10. **check.** grep the file for `<style`, `style="`, `—`, `–`; fix hits. Run `check_sources.py <file>` and fix every `fix:` line. Re-read for voice
11. **open it and listen.** `bash ~/.claude/skills/research/scripts/serve.sh <file>.html`, `open` the URL it prints, then start a **Monitor** with command `python3 ~/.claude/skills/research/scripts/watch.py <file>.html`, description `questions on <file>`, timeout 1800000. Handle questions exactly as in the research skill's ask flow (`~/.claude/skills/research/SKILL.md`, "ask flow"): answer in chat, post with `answer.py`, confirm before any edit or side effect, re-arm silently on expiry
12. **reply** with the URL, project type, the done/partial/missing counts, the launch blockers (high severity gaps) and "select any text in the doc and hit ask about this, i'll answer here". Under 100 words total. Details live in the doc

## rules

- **under 100 words in chat, always.** every chat reply, explanation and ask-flow answer stays under 100 words, whatever the question. Depth belongs in the doc, not chat
- **read-only check.** never edit the checked project. The output is the doc; fixes happen when the user runs the prompts
- **fit the project.** a static blog has no rate limits to check, a game with no accounts has no auth. Mark `n/a` and move on. A short honest list beats a long padded one
- **honest status.** scan output alone never makes an item `done`. Anything that lives in a dashboard or account (alerts, billing caps, backups, store listing) is `you confirm`, never `done` unless you saw it
- **blockers first.** `high` means "don't launch without this": the user can't see usage, can't hear about errors, can't roll back, or leaks data/money. Everything else is a reminder
- **respect the project's constraints.** read the project's CLAUDE.md/README first. If it bans client JS (strict CSP), suggest server-side or log-based analytics, not a script tag
- **sources.** link the tool's or platform's own docs for each fix. Tool names, free tiers and APIs change: anything version- or price-specific must come from a page opened this session, never memory
- all research-skill rules apply: no animation, no inline styling, no new classes, lowercase voice, one doc per request
