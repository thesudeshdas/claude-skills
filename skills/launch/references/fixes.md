# fixes

How to close each gap, and the prompt templates the doc hands to the user. Tool names below are common picks, not endorsements: check the tool's current docs (and pricing/free tier) before recommending, they drift.

## tool cheat sheet

| need | small/free-friendly options | notes |
|---|---|---|
| product analytics (events, funnels, retention) | PostHog, Amplitude, Mixpanel | funnels + retention built in. PostHog also does errors, flags and session replay |
| simple page analytics | Plausible, Umami, Fathom, Vercel Web Analytics, Cloudflare Web Analytics | cookieless, often no consent banner needed. Page views + custom events, weak on funnels |
| game analytics | GameAnalytics, PostHog, Unity Analytics | GameAnalytics has progression events (start/complete/fail) built in |
| no client JS allowed (strict CSP) | host/server logs, Cloudflare analytics (edge), Plausible/Umami events sent from a server or proxy | a static site can still count page views from the host's request logs |
| error tracking | Sentry, PostHog error tracking, Bugsnag, Crashlytics (mobile) | upload source maps in the build |
| uptime | UptimeRobot, Better Stack, Checkly, Cronitor (for cron) | point it at a real page, not just `/` |
| feature flags / kill switch | PostHog, LaunchDarkly, GrowthBook, Statsig, remote config, an env var | an env var + redeploy is a fine kill switch for small projects |
| feedback | mailto link, Tally/Google form, Discord, Canny, in-app widget | include version + device in the body |
| consent | cookieless analytics (avoid needing it), or a CMP like Cookiebot / Klaro | |
| rollback | Vercel/Netlify instant rollback, `git revert` + redeploy, EAS update rollback | write the exact command in the doc |

## stack notes

- **Next.js:** analytics/error SDKs init in `instrumentation.ts` / `instrumentation-client.ts` or a client provider in the root layout. Sentry has a `withSentryConfig` wrapper for source maps
- **Vite / plain SPA:** init in `main.ts` before render; error boundary around the root
- **Expo / React Native:** `expo-updates` for OTA, `sentry-expo`/`@sentry/react-native`, analytics SDK with app version + platform
- **Phaser / canvas games:** wrap the analytics calls in one `track(event, props)` helper called from scene lifecycle (`create`, level end, game over). Listen to `visibilitychange` to log quits mid-level and pause the game
- **static HTML with no JS:** analytics from host logs or edge; error tracking mostly n/a; feedback via mailto; rollback via the host
- **backend:** structured JSON logs, request id per request, health route that touches the DB

## guide shape for each gap

Inside the doc, every `missing`/`partial` item gets a `details` block:

1. **why it matters**: one or two lines, in launch terms ("on day one you won't know if anyone got past level 1"). Cite a source when it's a claim
2. **what to do here**: steps specific to this repo's stack and paths, with a short code sample in `pre[data-lang]`
3. **how to verify**: a command, URL or dashboard check (fire the event locally and see it in the live view, throw a test error, curl the health route)
4. **prompt**: a filled template below in `pre data-lang="prompt"` (the copy button comes from research.js)

## prompt templates

Fill every `<…>` with real values. Prompts are in normal sentence case (they go to an agent, not into the doc's prose voice), but keep them short.

### generic
```
In <repo path>, a <framework/engine> project, add <item> before launch. Current state: <what exists, file:line>. Requirements: <bullets from the checklist row>. Don't change unrelated files. When done, show me how to verify it: <verify step>.
```

### analytics events + funnel (A1 to A6)
```
In <repo>, a <type> built with <stack>, set up product analytics with <tool> so I can see usage and drop-off from day one. Create one small track(event, props) helper and call it at these points: <event list with where each fires, e.g. level_start in GameScene.create at src/scenes/Game.ts:40>. Every event includes <common props: version, platform, level_id, session id>. Use a stable anonymous id<, and identify the user after signup>. Skip tracking on localhost/dev. Make sure it works with our CSP <current CSP or "no CSP">. Then list every event with its properties and the funnel I should build: <step 1 → step N>.
```

### error tracking (B1 to B4)
```
In <repo>, add error tracking with <tool> for <client/server/both>. Capture uncaught errors, unhandled promise rejections<, and React render errors with an error boundary at <root component>>. Tag every event with release <version source> and environment. Upload source maps in the <build/CI step> without serving them publicly. Add a temporary way to throw a test error so I can confirm it shows up, then tell me where to set up an alert for new issues.
```

### uptime + health (C1 to C3)
```
In <repo>, add a <route> health endpoint that returns 200 only if <the app and its DB/critical dependency> work, and 503 otherwise, with no secrets in the response. Then give me the exact settings to monitor it with <uptime tool>: URL, interval, expected status, and alert to <channel>.
```

### security pass (F1 to F5)
```
Do a pre-launch security pass on <repo> (<stack>). Check: secrets committed or exposed to the client (<public env prefix>), auth on every route in <routes/api folder>, users only accessing their own data, rate limits on <endpoints>, server-side input validation, and security headers in <host config>. Report findings as a list with file:line and severity first; only fix after I approve.
```

### privacy + legal pages (G1 to G4)
```
Draft a privacy policy page for <product> at <route/file>. Facts to cover, nothing else: we collect <analytics tool + what>, <error tool + what>, <account data if any>, stored by <providers>, kept for <period>, users can delete via <method>, contact <email>. Plain language, short. Mark anything I need a lawyer to check. Link it from <footer/settings>.
```

### rollback + flags (I1 to I3)
```
For <repo> deployed on <host>, write a ROLLBACK note in <docs path> with the exact steps to revert production to the previous version in under 2 minutes, and how to roll back <DB migrations / mobile OTA> if relevant. Then put <risky feature> behind a kill switch using <flag tool or env var> so I can turn it off without a deploy.
```

### game save safety (J3)
```
In <repo>, game saves are stored in <storage, file:line>. Add a version field to the save format and a migration step on load so future updates can change the format without wiping progress. If a save can't be parsed, back it up under a separate key and start fresh instead of crashing. Show me how to test it with an old save.
```

### devices pass (K1 to K5)
```
In <repo>, check the <game/site> for mobile and cross-browser launch issues: viewport meta, canvas scaling and devicePixelRatio, touch input, audio unlock on first interaction, pause on visibilitychange, Safari-specific APIs. List problems with file:line first; fix only after I approve.
```

### cost guards (N1 to N4)
```
List every paid or metered service <repo> uses (look at dependencies, env vars and config): <known list>. For each, tell me the free tier limit, what happens when it's hit, and where to set a billing alert or hard cap, with links to the provider's docs. Then check which public endpoints could be abused to run up cost, with file:line.
```

## outside the code (for section "before you hit publish")

- set alerts: errors (new issue, spike), uptime (down 2+ min), billing (each paid service)
- build the funnel and a launch-day dashboard in the analytics tool, fire a test event end to end
- confirm backups exist and try one restore
- check domain + SSL renewal dates
- prepare the store/portal listing and the announcement drafts
- block a few hours on launch day to watch dashboards and the feedback inbox
