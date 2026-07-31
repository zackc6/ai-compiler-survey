# Push this survey to GitHub

Local git history is already initialized with the first commit. Creating the remote needs a one-time GitHub CLI login on this machine.

## 1. Authenticate

In PowerShell (with `gh` on PATH, or use `C:\Users\c00866834\bin\gh\bin\gh.exe`):

```powershell
$env:PATH = "C:\Users\c00866834\bin\mingit\cmd;C:\Users\c00866834\bin\gh\bin;$env:PATH"
cd C:\Users\c00866834\Desktop\ai-compiler-survey
gh auth login -h github.com -p https -w
```

Complete the device code in the browser when prompted.

If device login fails with network EOF (corporate proxy), use a Personal Access Token:

```powershell
gh auth login -h github.com -p https -t
# paste a classic PAT with `repo` scope
```

## 2. Create remote and push

```powershell
gh repo create ai-compiler-survey --public --source=. --remote=origin --push --description "Living survey of next-gen AI compilers and agentic compilation"
```

Or, if the empty repo already exists on GitHub:

```powershell
git remote add origin https://github.com/<YOUR_USER>/ai-compiler-survey.git
git push -u origin main
```

## 3. Progressive updates

After the remote exists:

1. Edit `publications/` digests and/or `docs/SURVEY.md`
2. Update `STATUS.md` checklist / changelog
3. Commit and push

```powershell
git add -A
git commit -m "Survey update: <short why>"
git push
```
