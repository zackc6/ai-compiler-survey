# Repository maintenance

This working tree tracks `origin` on `main`. Keep coherent updates on main; create branches or pull requests only when the maintainer requests them.

Before editing a clean stale checkout, fetch and fast-forward. Preserve unrelated changes. Validate the guide and rebuild its PDF before committing the intended files.

```bash
git fetch origin main
git merge --ff-only origin/main
python3 scripts/validate_survey.py
python3 publish/build_pdf.py
git add <intended-files>
git commit -m "Survey update: <short reason>"
```

When publishing is authorized, push main directly through an authenticated route. Never force-push. If the remote has advanced, reconcile its changes first. **An explicit instruction not to push takes precedence:** prepare, validate, and commit locally, then report that publication is pending.

The GitHub connection and local Git credentials are separate. Repository write permission in the connection does not establish that a shell push can authenticate. Use the available supported route when publication is authorized; do not use a real write to test permissions.

Cite external primary sources in the guide and digests. Keep repository administration details out of the research narrative and PDF cover.
