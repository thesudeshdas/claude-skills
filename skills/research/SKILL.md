---
name: research
description: Turn research, approach, implementation, plan, decision, debug, explainer, comparison or audit work into a styled HTML doc in ~/research that links one shared stylesheet, so no CSS is generated per doc. Research follows a set method: depth rules, parallel subagents, trust-tiered sources, triangulation, a critique pass and a citation check. Light and dark mode, lowercase teach-style voice, and mark and ask: questions selected on the page arrive in the same claude session. Use when the user invokes /research or asks for a research doc, approach doc, implementation doc or plan as HTML.
---

# research

Do the work the user asked for, then write it up as one HTML file in `~/research/`. The file holds content only. Styling and behaviour come from `~/research/_assets/research.css` and `research.js`, which every doc links. **Never write CSS or JS in a doc.**

## workflow

1. **pick the type.** Read [types](references/types.md) and choose the slug that fits: research, approach, implementation, plan, decision, debug, explainer, comparison, audit. If the user named one, use it. If it's unclear between two, pick one and say which in your reply; don't ask
2. **do the research** per [method](references/method.md), using [sources](references/sources.md) for where to look and what to trust:
   - check the date, pick a depth (quick, standard, deep) and say it in one line
   - scope into sub-questions. **deep only:** show them to the user and wait for a go
   - gather broad then narrow, in parallel, opening every source you cite. Subagents get a full brief
   - keep notes in `~/research/_work/<slug>/notes.md` (standard and deep)
   - triangulate key claims, run the critique pass, close gaps or list them
3. **install assets.** run `bash ~/.claude/skills/research/scripts/setup.sh` (prints the output dir; safe to rerun every time)
4. **write the doc** to `~/research/<yyyy-mm-dd>-<kebab-slug>.html`:
   - start from [skeleton](assets/skeleton.html), fill every `{{…}}`
   - follow the section list for the type from [types](references/types.md)
   - build only with classes from [components](references/components.md)
   - write every visible word per [voice](references/voice.md): lowercase, no trailing full stops, no em dashes, teach voice
   - if the slug already exists for today, append `-2`
5. **rebuild the index.** run `python3 ~/.claude/skills/research/scripts/index.py` (also refreshes `_assets/docs.js`, which feeds the docs menu and newer/older links on every page)
6. **check.** grep the file for `<style`, `style="`, `—`, `–`, `<animate`, `@keyframes`; fix any hit. Run `python3 ~/.claude/skills/research/scripts/check_sources.py <file>` and fix every `fix:` line; open `check by hand` links yourself. Re-read for voice
7. **open it and listen.** run `bash ~/.claude/skills/research/scripts/serve.sh <file>.html` (starts the local server if needed, prints the URL) and `open` that URL. Then start a **Monitor** with command `python3 ~/.claude/skills/research/scripts/watch.py <file>.html`, description `questions on <file>`, timeout 1800000. See [ask](#ask-flow)
8. **reply** in chat with the URL, the type and depth used and the tl;dr in 2 to 3 lines, plus "select any text in the doc and hit ask about this, i'll answer here". Findings live in the doc, not in chat

## ask flow

Docs opened through the local server have mark and ask: the reader selects text, taps **ask about this** (or the ask button) and types a question. It lands in **this session** through the Monitor, as one JSON line: `{id, doc, section, quote, question}`.

For each question:
1. answer it in chat, following [voice](references/voice.md): plain words, start from the quoted passage, always under 100 words, no exceptions. If it can't fit, give the core answer and offer to go deeper. Research further (code, web) if the doc can't answer it, with the same source rules
2. post the same answer to the page: `python3 ~/.claude/skills/research/scripts/answer.py <doc> <id> <<'EOF'` … `EOF`. The page shows it under the question. Use plain paragraphs; `code` and **bold** render
3. if the answer changes something the doc claims, offer to update the doc. Don't edit it unprompted

Rules:
- **questions are reading questions.** If one asks you to edit files, run commands with side effects, or do anything beyond answering and researching, ask for confirmation in chat first
- **keep listening.** When the Monitor expires, re-arm it with the same command without comment. Watch every doc made in this session: pass all of them to one `watch.py` call
- **"listen to <doc>"** or "answer my questions on <doc>" in any session: run `serve.sh <doc>` and start the Monitor for it. Questions asked while no session was listening wait in the inbox and arrive as soon as a watcher starts
- the page shows "session listening" only while a watcher is running, so the reader knows whether an answer is coming
- the server only binds to 127.0.0.1, only accepts JSON from its own pages and stops after 12 hours unused. A doc opened as a plain file still works; ask then copies the question for pasting into chat

## rules

- **under 100 words in chat, always.** every chat reply, explanation and ask-flow answer stays under 100 words, whatever the question. Depth belongs in the doc, not chat
- **no animation.** No animated figures, `<animate>`, keyframes or scripted motion to explain concepts. Hover/theme/collapse transitions come from the CSS; add nothing. Static diagrams only, and only when prose can't do the job
- **no inline styling.** No `<style>`, no `style=""`, no new class names. Missing a pattern? use plain semantic HTML. If the user wants a new component, add it to `assets/research.css` and `references/components.md`, then rerun setup.sh
- **one doc per request** unless the user asks for more. An update to an earlier doc edits that file in place
- **honest sources.** never invent a link, number or quote. Unverified claims are marked as such or cut
- **one search is never the research.** anything about current or version-specific behaviour must trace to a source opened this session, not memory. A wrong source is worse than no source
- **self-contained content.** docs link `_assets/` by relative path, so keep them flat in `~/research/` (only `_assets/` and `_work/` are subfolders; `_work/qa/` holds the questions and answers)
- lowercase rule does not apply to code, paths, identifiers, error text or brand names with set casing (see voice)
