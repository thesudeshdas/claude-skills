# claude skills

Claude Code skills for audits and write-ups. Each one produces a styled HTML doc in `~/research/`.

| skill | what it does | invoke |
|---|---|---|
| `research` | research, plan, decision, debug or explainer docs with a set research method and citation check. Owns the shared stylesheet, skeleton and scripts | `/research` |
| `seo` | SEO audit of a codebase and/or live URL: checklist with evidence, gaps and copy-paste fix prompts | `/seo` |
| `launch` | pre-launch readiness check (analytics, error tracking, uptime, security, privacy, rollback...) | `/launch` |

`seo` and `launch` depend on `research` (they read its stylesheet, skeleton and scripts from `~/.claude/skills/research`), so install all three.

## install

```bash
git clone git@github.com:thesudeshdas/claude-skills.git
cd claude-skills
./install.sh
```

This symlinks each folder in `skills/` into `~/.claude/skills/`. Restart Claude Code, then run `/research`, `/seo` or `/launch`. To update, `git pull`.

Requires `python3` on your PATH.
