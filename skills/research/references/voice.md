# voice

Every visible word in a research doc follows this. Taken from the GrowthX teach editor and humanizer, plus the user's lowercase style.

## casing and punctuation

- **all lowercase**, including headings, the `<title>`, names (jack, john), places (america) and the first word of a sentence. Acronyms stay uppercase (AI, API, CSS, PR, DB, URL)
- keep official casing for code, file paths, commands, identifiers, package names, error messages and brand/product names with special casing (macOS, GitHub, SwiftUI, iOS, npm, Next.js, Convex)
- no trailing full stop at the end of a paragraph, list item, caption or standalone sentence. Periods between sentences inside the same block are fine: "this does X. that does Y"
- no em dashes (—), en dashes (–) or ` -- ` used as dashes. Use a comma, colon, period or parentheses
- straight quotes only. Contractions are fine (it's, don't, you'll)

## voice

- **a smart friend explaining over chai.** warm, direct, a bit playful. Talk to the reader as "you"
- **plain words first.** say "the server tries again" before naming "retries". Explain a term the first time it shows up
- **short and specific.** mix short sentences with longer ones. One concrete detail (a file name, a number, a real error) beats a general claim
- **lead with the answer.** the tl;dr and the first line of every section state the conclusion, then the reasoning
- at most one light aside per section, only where it helps the idea stick
- bold a term once, where it's first explained. Never bold every list item's opening words

## kill these tells

1. **not X but Y.** "it's not just a cache, it's a strategy". State the point directly. Keep a contrast only when the reader actually believes the X half
2. **one-line closers.** "that's the real win." "let that sink in." Cut any line that repeats what the paragraph just said
3. **deep-sounding sayings.** "at its core", "the real question is", "X is the language of Y". Replace with the specific claim
4. **run-ups.** "let's dive in", "here's the thing", "honestly?". Make the point instead
5. **arguing with no one.** "to be clear", "you might think…but", "a tempting approach would be". Drop unless a real reader holds that view
6. **forced triads.** lists of three that exist to sound complete. Keep three only when there are three real items
7. **AI words.** additionally, crucial, delve, enhance, robust (figurative), seamless, leverage, pivotal, showcase, underscore, landscape, tapestry, testament, vibrant, meticulous, key (adjective)
8. **inflation.** "marks a pivotal shift", "sets the stage for", "the future looks bright". Keep the fact, drop the significance
9. **stacked hedges.** "could potentially possibly". One qualifier max, only when the doubt is real
10. **wrapper leftovers.** "great question", "I hope this helps", "in this document we will". Never

## facts

- never invent facts, numbers, names, links or quotes. If you didn't verify it, say it's unverified or leave it out
- every external claim in a research doc gets a source. Use `<sup class="ref"><a href="#s1">1</a></sup>` and list it in the sources section
- keep the user's real data (file paths, error text, IDs, numbers) character for character

## final check before saving

read the doc top to bottom once more and search for: capital letters outside code/acronyms/brands, `—`, `–`, trailing `.` before `</p>` / `</li>`, and the tells above
