# Git remote notes

This working tree already tracks `origin` on `main`. **Always push `main` directly** — no feature branches, no PRs (living survey). See `.cursor/skills/survey/SKILL.md` → “Git: push main only”.

```bash
git checkout main
git add -A
git commit -m "Survey update: <short why>"
git push origin main
```

Do not create `cursor/*` branches or open GitHub PRs unless the maintainer explicitly asks. Do not embed this survey’s own repository URL or name into digests, PDF covers, or prediction text — cite external primary sources only.
