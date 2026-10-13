# doc types

Pick one type per doc. Section lists are the default order; drop a section that would be empty, never pad one. Every type starts with the hero and a **tl;dr** section.

The `data-type` value must be one of the slugs below (they have colours in the CSS). For a new kind of doc, see "adding a type" at the bottom.

## research
use for: "look into X", "what are the options for", market/tech/library scans, "how does X work out there"

1. **tl;dr**: the answer in 2 to 4 bullets
2. **the question**: what was asked, scope, what's out of scope
3. **findings**: one `h3` per finding, each with evidence and a `sup.ref`. `.stats` for numbers, `.table-wrap` for side by side data
4. **what this means for you**: tie findings to the user's project/context. `.callout.tip`
5. **gaps and unknowns**: `ul.questions` for what couldn't be verified
6. **sources**: `ol.sources`, every link with a short note on what it supports

## approach
use for: "how should we do X", picking between ways to build something before any code

1. **tl;dr**: recommended approach in one line + why
2. **problem**: what we're solving, constraints (`dl.facts`), what good looks like
3. **options**: `.options` with one `.option` each (name, one-line summary, `ul.pros`, `ul.cons`, effort chip). Mark the recommended one `.option.pick`. 2 to 4 options
4. **comparison**: `.table-wrap` table across the criteria that matter (`td.yes` / `td.no` / `td.meh`)
5. **recommendation**: `.verdict`, then the tradeoffs you accept
6. **risks**: `.callout.risk` or a table with likelihood/impact chips
7. **open questions**: `ul.questions`

## implementation
use for: "how exactly do we build X", a concrete change to a codebase, design doc for a PR

1. **tl;dr**: what changes and the end result
2. **context**: current state, the relevant code (`file:line`), why it changes
3. **design**: data model, flow (`.flow` or a static `figure.diagram`), interfaces. Code in `pre[data-lang]`
4. **files**: `ul.files` with `.act.add` / `.act.mod` / `.act.del`
5. **steps**: `ol.steps`, each step small enough to commit on its own
6. **edge cases**: table or list
7. **testing**: how to verify, commands in `pre`
8. **rollout and rollback**: flags, migrations, how to undo
9. **risks**: `.callout.risk`

## plan
use for: roadmaps, multi-phase work, "plan out X", sprints, launches

1. **tl;dr**: goal and the end date or milestone
2. **goal**: what done looks like, success metrics (`.stats` or `dl.facts`)
3. **phases**: `ol.steps`, each with deliverables, owner, rough size chip. `.done` for finished ones
4. **milestones**: table: milestone, date/size, exit criteria
5. **dependencies**: what blocks what
6. **risks**: table with chips `.low` / `.med` / `.high`
7. **open questions**: `ul.questions`

## decision
use for: an ADR, recording a choice already made or about to be made

1. **tl;dr**: the decision in one sentence
2. **context**: the forces at play
3. **decision**: `.verdict`
4. **alternatives considered**: `.options` (no `.pick`) or `details` per alternative
5. **consequences**: `ul.pros` / `ul.cons` for what gets easier and harder
6. **status**: chip (proposed, accepted, superseded)

## debug
use for: bug investigations, root cause analysis, postmortems

1. **tl;dr**: root cause and fix in two lines
2. **symptoms**: what broke, exact error in `pre`, who/what was affected
3. **timeline**: `ol.steps` or table (time, event)
4. **investigation**: hypotheses tried, evidence for/against each (`details` per hypothesis)
5. **root cause**: `.callout.risk`, with the code `file:line`
6. **fix**: diff or code in `pre[data-lang="diff"]`
7. **prevention**: `ul.checks` for follow-ups

## explainer
use for: "explain how X works", onboarding to a system or codebase area

1. **tl;dr**: the mental model in two lines
2. **the big picture**: one static `figure.diagram` or `.flow`, then a short walk through it
3. **parts**: `h3` per component, what it does, where it lives (`code` paths)
4. **how a request flows**: `ol.steps`
5. **gotchas**: `.callout.warn`
6. **where to go next**: links/files

## comparison
use for: "X vs Y", tool/library/vendor comparisons without a build plan

1. **tl;dr**: winner per use case
2. **contenders**: `.grid` of `.card`s, one each
3. **head to head**: big `.table-wrap` table
4. **pick by situation**: "if you need A, pick X" list
5. **sources**: `ol.sources`

## audit
use for: reviewing a codebase/site/system for issues (performance, security, accessibility, quality)

1. **tl;dr**: count by severity (`.stats`) and the top fix
2. **scope**: what was checked and how
3. **findings**: table: finding, `file:line`, severity chip, fix. Or `details` per finding for long ones
4. **quick wins**: `ul.checks`
5. **longer fixes**: `ol.steps`

## adding a type

If nothing above fits, use the closest type, and tell the user in one line which type you used and that a new one could be added. To add one for real: add a section here, and a `[data-type="<slug>"] { --tc: var(--<token>); }` line in `assets/research.css` next to the others, then rerun `scripts/setup.sh`
