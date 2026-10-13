# components

Every class below already exists in `~/research/_assets/research.css`. Never write a `<style>` block or `style=""` attribute, and never invent a class. If something can't be built from these, use plain semantic HTML (p, ul, table, h3) and it will still look right.

`research.js` builds the topbar, theme toggle, doc switcher (topbar "docs" menu, or press `/`), progress bar, toc, copy buttons, newer/older links and footer. The doc list comes from `_assets/docs.js`, written by `index.py`. Don't write any of those.

## page frame
see `assets/skeleton.html`. Sections:
```html
<section class="block">
  <h2>findings</h2>            <!-- becomes a toc entry; data-toc="short label" to shorten -->
  <p>…</p>
</section>
```
`<div class="stack">` = vertical group with 12px gap. `<span class="sec-num">01</span>` = optional mono label above an h2.

## text
`<p class="lede">` intro · `<span class="grad">word</span>` serif gradient accent (one per page, in the h1) · `.muted` · `.mono` · `.eyebrow` small caps label · `<blockquote>…<cite>…</cite></blockquote>`

## tl;dr
```html
<div class="tldr"><ul><li>…</li></ul></div>
```

## callouts
```html
<div class="callout"><span class="eyebrow">note</span><p>…</p></div>
```
modifiers: `.tip` (violet) · `.warn` (amber) · `.risk` (red) · `.win` (green). default is blue note

## chips
`<span class="chip">2 days</span>` · `.ok` `.warn` `.bad` `.info` · severity: `.low` `.med` `.high`
type badge: `<span class="type" data-type="plan">plan</span>`

## stats
```html
<div class="stats"><div class="stat"><b>42ms</b><span>p95 latency</span></div></div>
```

## cards
```html
<div class="grid"><div class="card"><h3>…</h3><p>…</p></div></div>
```
`a.card` for a clickable card

## options + verdict (approach, decision, comparison)
```html
<div class="options">
  <div class="option pick">
    <h3>option a: …</h3><p>…</p>
    <ul class="pros"><li>…</li></ul>
    <ul class="cons"><li>…</li></ul>
    <div class="meta"><span class="chip">effort: s</span></div>
  </div>
</div>
<div class="verdict"><span class="eyebrow">recommendation</span><p>go with a</p><p>because …</p></div>
```

## steps (plan, implementation, flows)
```html
<ol class="steps">
  <li class="done"><strong>step title</strong><p>…</p></li>
  <li><strong>step title</strong><p>…</p><div class="meta"><span class="chip">1 day</span></div></li>
</ol>
```
checklist: `<ul class="checks"><li class="done">…</li><li>…</li></ul>`

## files
```html
<ul class="files">
  <li><span class="act add">add</span><code>convex/levels.ts</code><span>what it does</span></li>
  <li><span class="act mod">mod</span><code>src/game.ts</code><span>…</span></li>
  <li><span class="act del">del</span><code>old.ts</code><span>…</span></li>
</ul>
```

## tables
```html
<div class="table-wrap"><table>
  <thead><tr><th>…</th></tr></thead>
  <tbody><tr><td class="yes">yes</td><td class="no">no</td><td class="meh">partly</td></tr></tbody>
</table></div>
```

## key facts
```html
<dl class="facts"><dt>deadline</dt><dd>…</dd></dl>
```

## code
```html
<pre data-lang="ts"><code>…escaped code…</code></pre>
```
escape `<`, `>`, `&` inside code. Inline: `<code>`

## open questions
`<ul class="questions"><li>…</li></ul>`

## collapsible
```html
<details><summary>hypothesis 2: stale cache</summary><div class="body"><p>…</p></div></details>
```

## sources
```html
<ol class="sources">
  <li id="s1"><a href="https://…">page title</a> <span class="muted">what it supports</span></li>
</ol>
```
cite inline: `<sup class="ref"><a href="#s1">1</a></sup>`

## static diagrams (no animation, ever)
simple chain:
```html
<div class="flow"><span>client</span><i>→</i><span>convex</span><i>→</i><span>db</span></div>
```
anything bigger: inline `<svg>` inside `<figure class="diagram">…<figcaption>…</figcaption></figure>`. Use `currentColor` and `var(--brand-text)`, `var(--muted)`, `var(--hairline-2)` for strokes/fills so it works in both themes. No `<animate>`, no CSS keyframes, no JS-driven motion. Only add a diagram when it explains something prose can't
