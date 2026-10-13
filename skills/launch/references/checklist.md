# checklist

Every item has an id, a default severity, and how to check it. Severity is the default; raise or lower it for the project (no uptime monitor on a hobby static site is low, on a paid app it's high). `high` = launch blocker.

Status values: `done` · `partial` · `missing` · `n/a` (say why) · `you confirm` (lives outside the code, say where to look)

## project types

| type | looks like |
|---|---|
| game | phaser, pixi, three.js, kaboom, excalibur, godot (`project.godot`), unity (`ProjectSettings/`), canvas-heavy pages |
| static site | plain HTML, astro/eleventy/hugo output, blogs, landing pages, no server of its own |
| web app | next/remix/sveltekit/nuxt/vite app with accounts, data or a backend |
| mobile app | expo, react native, swift/kotlin projects |
| backend/API | express, fastify, nest, hono, django, fastapi, rails, convex, supabase functions |
| feature | a branch/PR/folder inside an existing product; the product already has the basics, check only what this change adds |

## applicability

`●` check it · `○` light check (one or two items) · blank = usually `n/a`

| category | game | static | web app | mobile | backend | feature |
|---|---|---|---|---|---|---|
| A. product analytics | ● | ○ | ● | ● | ○ | ● |
| B. errors and crashes | ● | ○ | ● | ● | ● | ● |
| C. uptime and alerts | ○ | ○ | ● | ○ | ● | |
| D. performance | ● | ● | ● | ● | ○ | ○ |
| E. accessibility | ● | ● | ● | ● | | ○ |
| F. security | ○ | ○ | ● | ● | ● | ● |
| G. privacy and legal | ● | ○ | ● | ● | ○ | ○ |
| H. feedback loop | ● | ○ | ● | ● | | ○ |
| I. rollback and release | ○ | ○ | ● | ● | ● | ● |
| J. data safety | ○ | | ● | ● | ● | ○ |
| K. devices and browsers | ● | ● | ● | ● | | ○ |
| L. sharing and discovery | ● | ● | ● | ● | | ○ |
| M. launch comms | ● | ○ | ● | ● | ○ | ● |
| N. cost guards | ○ | ○ | ● | ○ | ● | ○ |

## A. product analytics (instrumentation)

Can you answer "is anyone using it, how far do they get, where do they stop" on day one?

| id | item | sev | check |
|---|---|---|---|
| A1 | an analytics tool is installed and sends data in production (not only dev, not blocked by CSP) | high | SDK import + init call, env keys set for prod, CSP allows the endpoint |
| A2 | core events are tracked for this project type (see "events to expect") | high | grep `track(`, `capture(`, `logEvent(`, `gtag('event'`, custom event helpers; list what exists vs what's needed |
| A3 | the main funnel can be built from those events, so drop-off is visible (step 1 → step N) | high | events cover every step in order, with the same user/session id |
| A4 | events carry useful properties (level id, score, duration, platform, version) | med | event payloads |
| A5 | a stable anonymous id per player/user, linked to the account id after signup if there are accounts | med | identify/alias calls |
| A6 | retention is measurable (returning sessions, D1/D7) | med | session start event + stable id |
| A7 | a dashboard or saved funnel exists before launch, so day-one data has a home | med | `you confirm` |
| A8 | no PII in event properties (emails, names, raw IPs) unless intended and disclosed | med | event payloads |
| A9 | your own test traffic can be filtered out | low | dev flag, internal user filter, localhost check |

### events to expect

- **game:** `game_start` / session start, `level_start`, `level_complete`, `level_fail` (with reason), `game_over`, `quit` or tab hidden mid-level, tutorial steps, settings changed, time per level, purchases/ads if any. Funnel: landing → play click → first level start → level 1 done → level N
- **static site / blog:** page views, outbound clicks on key links (store, itch, socials), RSS/newsletter signups. Funnel is usually just landing → click
- **web app / mobile:** signup started/done, onboarding steps, first core action (activation), core action repeated, upgrade/paywall seen/converted, churn signals (cancel, delete). Mobile also: app open, push permission, app version
- **backend/API:** request counts and latency by route, key business events (orders, jobs done) logged or emitted
- **feature:** feature seen, feature used, feature completed, feature abandoned. Compare against a baseline metric so you know if it helped

## B. errors and crashes

| id | item | sev | check |
|---|---|---|---|
| B1 | error tracking is installed (client and server) | high | `@sentry/*`, bugsnag, rollbar, crashlytics, posthog exceptions, honeybadger |
| B2 | uncaught errors are captured: global handlers, React error boundary, unhandled promise rejections, native crashes | high | `window.onerror`, `unhandledrejection`, `ErrorBoundary`, crash SDK |
| B3 | source maps / debug symbols uploaded so stack traces are readable | med | build plugin config, CI step |
| B4 | release/version tagged on every error | med | `release:` in SDK init, app version |
| B5 | alerts on new or spiking errors reach you (email, Slack, phone) | high | `you confirm` |
| B6 | server logs are kept somewhere searchable for at least a few days | med | host log retention, log drain |
| B7 | user-facing error states tell people what to do (retry, contact) instead of a blank screen | med | error UI, 500 page |

## C. uptime and alerts

| id | item | sev | check |
|---|---|---|---|
| C1 | a health endpoint or a page that proves the app works end to end | med | `/health`, `/api/health`, `/status` routes |
| C2 | an external uptime monitor pings it | high for apps, low for static | `you confirm` (UptimeRobot, Better Stack, Checkly…) |
| C3 | alerts go to a channel you'll see at night (phone push, not just email) | med | `you confirm` |
| C4 | domain and SSL auto-renew; domain expiry date known | med | `you confirm` at registrar, host |
| C5 | scheduled jobs / cron failures alert you | low | cron config + monitor |

## D. performance

| id | item | sev | check |
|---|---|---|---|
| D1 | first load is light: total transfer and JS size checked against a budget | med | build output, bundle analyzer, Lighthouse |
| D2 | images and audio compressed, right size, lazy where possible | med | asset sizes, formats |
| D3 | games: steady frame rate on a low-end phone/laptop; no memory leak over a long session | high for games | manual test, devtools perf |
| D4 | loading state for anything slow (asset preload bar, skeletons) | low | UI |
| D5 | caching + compression for static assets | low | headers, host config |
| D6 | backend: slow queries indexed, obvious N+1s fixed, basic load tested | med | query code, `you confirm` |

## E. accessibility

| id | item | sev | check |
|---|---|---|---|
| E1 | text contrast and readable font sizes | med | CSS, Lighthouse a11y |
| E2 | keyboard works: focus visible, everything reachable, games playable without a mouse where it makes sense | med | `:focus-visible`, key handlers |
| E3 | alt text, labels on inputs and buttons, `lang` on html | med | markup |
| E4 | `prefers-reduced-motion` respected for big motion, flashes and screen shake | med | CSS/media queries, game settings |
| E5 | games: colorblind-safe cues (not color alone), subtitles/captions for spoken audio, remappable controls, volume controls | low | game settings |

## F. security

| id | item | sev | check |
|---|---|---|---|
| F1 | no secrets in the repo or client bundle (`.env` not committed, no server keys in `NEXT_PUBLIC_`/`EXPO_PUBLIC_`/`VITE_`) | high | `git ls-files`, grep for key patterns |
| F2 | auth on every private route and API; users can only read/write their own data | high | route guards, row-level security, ownership checks |
| F3 | rate limits on login, signup, forms, expensive or paid endpoints (AI calls, emails, SMS) | high | middleware, platform config |
| F4 | security headers: HTTPS only, CSP, `X-Content-Type-Options`, frame protection | med | host headers config |
| F5 | input validated on the server, uploads type/size limited | med | schema validation |
| F6 | dependencies audited for known vulns | low | `npm audit`, Dependabot |
| F7 | games with leaderboards/economy: scores and purchases validated server side, not trusted from the client | med | score submit code |

## G. privacy and legal

| id | item | sev | check |
|---|---|---|---|
| G1 | privacy policy page that matches what's actually collected (analytics, crash data, accounts) | high if collecting data | `/privacy` route or page |
| G2 | terms of service for apps with accounts, payments or user content | med | `/terms` |
| G3 | cookie/consent banner where required (EU users + non-essential cookies or tracking) | med | consent lib, or cookieless analytics |
| G4 | a way to delete an account and its data | med for apps | delete flow, `you confirm` for manual process |
| G5 | games/apps for kids: age rating, COPPA/GDPR-K rules, no ad tracking | high if kids | `you confirm` |
| G6 | licenses and credits for fonts, music, sprites, libraries; attribution where required | med | `CREDITS`, `LICENSE`, about page |
| G7 | store-required items: privacy nutrition labels (App Store), data safety form (Play) | high for mobile | `you confirm` |

## H. feedback loop

| id | item | sev | check |
|---|---|---|---|
| H1 | a visible way to report a bug or send feedback (link, form, email, Discord) | high | contact/feedback link in UI or footer |
| H2 | someone actually watches that inbox/channel during launch week | med | `you confirm` |
| H3 | bug reports include context automatically where possible (version, device, last level) | low | feedback widget, mailto body |
| H4 | a place to reply publicly (changelog, socials, Discord) for known issues | low | `you confirm` |

## I. rollback and release safety

| id | item | sev | check |
|---|---|---|---|
| I1 | you know the one action that reverts a bad deploy (host rollback, revert commit, previous build) | high | host (Vercel/Netlify instant rollback), CI, `you confirm` |
| I2 | risky features behind a flag or kill switch you can turn off without a deploy | med | feature flag lib, remote config |
| I3 | a preview/staging environment that matches prod | med | preview deploys, env config |
| I4 | version number visible somewhere (footer, settings, app about) | low | version constant |
| I5 | mobile: OTA update path for JS fixes, and a forced-update path for breaking changes | med for mobile | `expo-updates`, min version check |
| I6 | CI runs build + tests before production deploy | med | `.github/workflows`, host build checks |

## J. data safety

| id | item | sev | check |
|---|---|---|---|
| J1 | automatic DB backups on, and one restore actually tested | high for apps with data | `you confirm` |
| J2 | migrations run on a copy first, reversible or at least planned | med | migrations folder, scripts |
| J3 | games: save data is versioned, so an update doesn't wipe or corrupt saves | med for games | save key/version field, migration code |
| J4 | user uploads stored outside the app server (object storage), with limits | low | storage config |

## K. devices and browsers

| id | item | sev | check |
|---|---|---|---|
| K1 | works on a real phone (iOS Safari + Android Chrome), portrait and landscape where it matters | high | viewport meta, responsive CSS, `you confirm` |
| K2 | Safari/Firefox tested, not only Chrome | med | `you confirm` |
| K3 | slow network and offline behave sensibly (no endless spinner) | low | throttled test |
| K4 | games: touch controls on mobile, gamepad if promised, audio unlock on first tap (autoplay rules), pause on tab hidden | med for games | input handlers, `visibilitychange` |
| K5 | different screen sizes and DPIs: canvas scales, text stays sharp | med for games | resize handling, devicePixelRatio |

## L. sharing and discovery

Quick checks only. For the full audit, run `/seo`.

| id | item | sev | check |
|---|---|---|---|
| L1 | title + meta description on the main pages | med | head tags |
| L2 | Open Graph image + tags, so links look good when shared | med | `og:` tags, image file |
| L3 | favicon and app icons | low | icon files + link tags |
| L4 | `/seo` audit run (or scheduled) | low | an seo doc in `~/research/` |
| L5 | store/portal listing ready: screenshots, trailer/GIF, short + long description, tags (itch.io, Steam, App Store, Play, Product Hunt) | high for games/mobile | `you confirm` |
| L6 | press kit / media page for games (logo, screenshots, one-paragraph pitch) | low | `/press` page |

## M. launch comms

| id | item | sev | check |
|---|---|---|---|
| M1 | announcement written: blog post, changelog entry or release notes | med | changelog, blog content |
| M2 | list of where you'll post (socials, communities, newsletter, Discord) with drafts ready | low | `you confirm` |
| M3 | a way for interested people to follow (newsletter, RSS, wishlist, Discord) on the launch page | med | signup form, RSS link |
| M4 | in-product "what's new" for existing users (feature launches) | low | UI |
| M5 | launch day picked when you're around to watch the dashboards for a few hours | low | `you confirm` |

## N. cost guards

| id | item | sev | check |
|---|---|---|---|
| N1 | billing alerts set on every paid service (host, DB, AI APIs, email, maps) | high for apps | `you confirm` |
| N2 | hard spend caps or quotas where the provider supports them (AI API keys especially) | high if AI/paid APIs | `you confirm`, key config |
| N3 | free tier limits known (bandwidth, function invocations, analytics events, error quota) and what happens at the limit | med | `you confirm` |
| N4 | abuse can't run up the bill (rate limits from F3, captcha on public forms, no open proxy endpoints) | med | middleware |

## sources to cite (open each before citing)

Pick the ones that match the fixes you recommend. Prefer the tool's own docs.

- web.dev core web vitals: https://web.dev/articles/vitals
- WCAG quick reference: https://www.w3.org/WAI/WCAG22/quickref/
- game accessibility guidelines: https://gameaccessibilityguidelines.com/
- OWASP top 10: https://owasp.org/www-project-top-ten/
- MDN CSP: https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP
- Sentry docs: https://docs.sentry.io/
- PostHog docs: https://posthog.com/docs
- Plausible docs: https://plausible.io/docs
- GameAnalytics docs: https://docs.gameanalytics.com/
- Vercel instant rollback: https://vercel.com/docs/instant-rollback
- App Store privacy details: https://developer.apple.com/app-store/app-privacy-details/
- Play data safety: https://support.google.com/googleplay/android-developer/answer/10787469
- GDPR overview: https://gdpr.eu/
- FTC COPPA: https://www.ftc.gov/legal-library/browse/rules/childrens-online-privacy-protection-rule-coppa
