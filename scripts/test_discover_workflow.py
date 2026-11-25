"""Static regressions for .github/workflows/discover.yml publication routing (ChatGPT/Codex 00:22,
ChatGPT 00:46): one UTC date and one ledger path are computed once and used for generation,
staging and announcement; the published file is never chosen by listing reference/discovery."""
import pathlib, subprocess, tempfile, unittest

import yaml

WF = pathlib.Path(__file__).resolve().parent.parent / ".github" / "workflows" / "discover.yml"


def steps():
    wf = yaml.safe_load(WF.read_text(encoding="utf-8"))
    return {s.get("name", ""): s.get("run", "") for s in wf["jobs"]["discover"]["steps"]}


class PublicationRouting(unittest.TestCase):
    def test_run_date_and_path_bound_once(self):
        st = steps()
        run, pub = st["Run discovery"], st["Publish ledger on a branch and announce in the Review thread"]
        self.assertEqual(run.count("date -u"), 1)
        self.assertNotIn("date -u", pub, "publish must reuse RUN_DATE, not re-derive the date")
        self.assertIn('--out "$f"', run)
        self.assertIn('f="$LEDGER"; d="$RUN_DATE"', pub)
        self.assertNotIn("ls reference/discovery", pub)
        self.assertIn('git add -- "$f"', pub)
        self.assertNotIn("git add reference/discovery\n", pub)

    def _route(self, existing, header_date, run_date):
        """Execute the routing lines of both steps in a scratch tree with discover.py stubbed."""
        st = steps()
        run = st["Run discovery"]
        pub = st["Publish ledger on a branch and announce in the Review thread"]
        with tempfile.TemporaryDirectory() as tmp:
            t = pathlib.Path(tmp)
            (t / "reference" / "discovery").mkdir(parents=True)
            for name in existing:
                (t / "reference" / "discovery" / name).write_text("# Discovery ledger — other run\n")
            bindir = t / "bin"; bindir.mkdir()
            # date stub: the shell's single `date -u` returns run_date
            (bindir / "date").write_text(f"#!/bin/sh\necho {run_date}\n"); (bindir / "date").chmod(0o755)
            (bindir / "python3").write_text(
                "#!/bin/sh\nwhile [ $# -gt 0 ]; do [ \"$1\" = --out ] && out=$2; shift; done\n"
                f"printf '# Discovery ledger — {header_date}\\n' > \"$out\"\n")
            (bindir / "python3").chmod(0o755)
            env_file = t / "env"
            head = run.split("if [ -n \"$INPUT_SINCE\" ]")[0]
            script = (head + "python3 scripts/discover.py --out \"$f\"\n" + run.split("fi\n", 1)[1]
                      + "set -a; . \"$GITHUB_ENV\"; set +a\n" + pub.split("# Accept the published")[0]
                      + 'echo "PICKED=$f DATE=$d"\n')
            r = subprocess.run(["bash", "-c", script], cwd=t, capture_output=True, text=True,
                               env={"PATH": f"{bindir}:/usr/bin:/bin", "GITHUB_ENV": str(env_file),
                                    "INPUT_SINCE": ""})
            return r

    def test_newer_checked_in_ledger_is_not_picked(self):
        r = self._route(["2026-11-30.md", "2099-01-01.md"], "2026-11-25", "2026-11-25")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("PICKED=reference/discovery/2026-11-25.md DATE=2026-11-25", r.stdout)

    def test_rollover_header_agrees_with_path_branch_and_announcement(self):
        """ChatGPT/Codex 00:54: run the real discover.py (fixture mode) under the workflow's own step
        text with the shell's date one day before the process's date. Header, path, branch and
        announcement must all carry the shell's date; the window must match a run whose output path
        carries no date, so only the header changed."""
        import datetime, sys
        script = pathlib.Path(__file__).resolve().parent / "discover.py"
        shell_d = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
        st = steps()
        run = st["Run discovery"]
        pub = st["Publish ledger on a branch and announce in the Review thread"]
        with tempfile.TemporaryDirectory() as tmp:
            t = pathlib.Path(tmp)
            (t / "reference" / "discovery").mkdir(parents=True)
            bindir = t / "bin"; bindir.mkdir()
            (bindir / "date").write_text(f"#!/bin/sh\necho {shell_d}\n"); (bindir / "date").chmod(0o755)
            (bindir / "python3").write_text(
                f"#!/bin/sh\nshift\nexec {sys.executable} -I {script} --channels none \"$@\"\n")
            (bindir / "python3").chmod(0o755)
            head = run.split("if [ -n \"$INPUT_SINCE\" ]")[0]
            sh = (head + "python3 scripts/discover.py --out \"$f\"\n" + run.split("fi\n", 1)[1]
                  + "set -a; . \"$GITHUB_ENV\"; set +a\n" + pub.split("# Accept the published")[0]
                  + 'echo "PICKED=$f BRANCH=claude/discovery-$d ANNOUNCE=## Discovery $d"\n')
            r = subprocess.run(["bash", "-c", sh], cwd=t, capture_output=True, text=True,
                               env={"PATH": f"{bindir}:/usr/bin:/bin", "GITHUB_ENV": str(t / "env"),
                                    "INPUT_SINCE": ""})
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertIn(f"PICKED=reference/discovery/{shell_d}.md BRANCH=claude/discovery-{shell_d} "
                          f"ANNOUNCE=## Discovery {shell_d}", r.stdout)
            self.assertNotIn("::warning::", r.stdout)
            ledger = (t / "reference" / "discovery" / f"{shell_d}.md").read_text(encoding="utf-8")
            self.assertEqual(ledger.splitlines()[0], f"# Discovery ledger — {shell_d}")
            self.assertIn(f"windows and eligibility were computed on {datetime.date.today().isoformat()}", ledger)
            undated = t / "undated.md"
            subprocess.run([sys.executable, "-I", str(script), "--channels", "none", "--out", str(undated)],
                           check=True, capture_output=True)
            window = lambda s: [ln for ln in s.splitlines() if ln.startswith("Window:")]  # noqa: E731
            self.assertEqual(window(ledger), window(undated.read_text(encoding="utf-8")))
            self.assertEqual(undated.read_text(encoding="utf-8").splitlines()[0],
                             f"# Discovery ledger — {datetime.date.today().isoformat()}")

    def test_midnight_rollover_keeps_run_date_and_warns(self):
        r = self._route([], "2026-11-26", "2026-11-25")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("PICKED=reference/discovery/2026-11-25.md DATE=2026-11-25", r.stdout)
        self.assertIn("::warning::ledger header date differs", r.stdout)


if __name__ == "__main__":
    unittest.main()
