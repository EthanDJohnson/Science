"""Tests for check_env.py: what --install asks pip for, how the outcome is reported, and that nothing
is installed when every package works. pip and the network are mocked, so nothing is installed.
"""
import contextlib
import io
import json
import os
import subprocess
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import check_env  # noqa: E402

SOURCES_OK = [{"source": name, "ok": True, "detail": "HTTP 200"} for name, _ in check_env.SOURCES]
PEP668 = ("error: externally-managed-environment\n\n"
          "× This environment is externally managed\n"
          "╰─> To install Python packages system-wide, try apt install python3-xyz.\n")
OFFLINE = ("ERROR: Could not find a version that satisfies the requirement scipy (from versions: none)\n"
           "ERROR: No matching distribution found for scipy\n")


def pkgs(missing=(), broken=()):
    """check_packages() output with the named packages missing or broken."""
    out = []
    for name, required in check_env.PACKAGES:
        ok = name not in missing and name not in broken
        p = {"package": name, "ok": ok, "version": "1.0" if ok else None, "required": required}
        if name in broken:
            p["broken"] = "installed but fails to import (PanicException); pip install cffi"
        out.append(p)
    return out


def pip_result(ok, packages, reason="", tail=()):
    r = {"ok": ok, "packages": list(packages), "seconds": 5, "command": "python3 -m pip install " + " ".join(packages)}
    return r if ok else {**r, "reason": reason, "tail": list(tail)}


class PipNames(unittest.TestCase):
    def test_nothing_when_every_package_works(self):
        self.assertEqual(check_env.pip_names(pkgs()), [])

    def test_only_the_missing_ones_in_list_order(self):
        self.assertEqual(check_env.pip_names(pkgs(missing=("scipy", "sympy"))), ["sympy", "scipy"])

    def test_pypdf_brings_cffi_whether_missing_or_broken(self):
        self.assertEqual(check_env.pip_names(pkgs(missing=("pypdf",))), ["pypdf", "cffi"])
        self.assertEqual(check_env.pip_names(pkgs(broken=("pypdf",))), ["pypdf", "cffi"])

    def test_never_asks_for_anything_outside_the_fixed_list(self):
        allowed = {n for name, _ in check_env.PACKAGES for n in check_env.PIP_NAMES.get(name, [name])}
        everything = check_env.pip_names(pkgs(missing=[name for name, _ in check_env.PACKAGES]))
        self.assertEqual(set(everything), allowed)
        self.assertEqual(len(everything), len(allowed))


class PipInstall(unittest.TestCase):
    def run_pip(self, returncode=0, stdout="", stderr="", side_effect=None):
        done = subprocess.CompletedProcess([], returncode, stdout, stderr)
        with mock.patch.object(check_env.subprocess, "run", return_value=done, side_effect=side_effect) as run:
            return check_env.pip_install(["scipy"]), run

    def test_runs_this_pythons_pip_on_the_named_packages_only(self):
        result, run = self.run_pip()
        self.assertTrue(result["ok"])
        cmd = run.call_args.args[0]
        self.assertEqual(cmd[:4], [sys.executable, "-m", "pip", "install"])
        self.assertEqual([a for a in cmd[4:] if not a.startswith("-")], ["scipy"])
        self.assertNotIn("--break-system-packages", cmd)
        self.assertNotIn("--upgrade", cmd)
        self.assertEqual(run.call_args.kwargs["timeout"], check_env.PIP_TIMEOUT)

    def test_an_externally_managed_python_is_explained(self):
        result, _ = self.run_pip(1, stderr=PEP668)
        self.assertFalse(result["ok"])
        self.assertIn("PEP 668", result["reason"])
        self.assertIn("venv", result["reason"])
        self.assertIn("error: externally-managed-environment", result["tail"])

    def test_an_unreachable_index_is_explained(self):
        result, _ = self.run_pip(1, stderr=OFFLINE)
        self.assertIn("PyPI isn't reachable", result["reason"])
        self.assertEqual(result["tail"][-1], "ERROR: No matching distribution found for scipy")

    def test_a_python_without_pip(self):
        result, _ = self.run_pip(1, stderr="/usr/bin/python3: No module named pip")
        self.assertIn("pip isn't installed", result["reason"])

    def test_an_unknown_failure_keeps_pips_last_lines(self):
        result, _ = self.run_pip(1, stderr="\n".join(f"line {i}" for i in range(20)))
        self.assertEqual(result["reason"], "pip failed; its last lines follow")
        self.assertEqual(result["tail"], [f"line {i}" for i in range(12, 20)])

    def test_a_timeout_or_missing_interpreter_never_raises(self):
        result, _ = self.run_pip(side_effect=subprocess.TimeoutExpired("pip", check_env.PIP_TIMEOUT))
        self.assertFalse(result["ok"])
        self.assertIn(f"{check_env.PIP_TIMEOUT} s", result["reason"])
        result, _ = self.run_pip(side_effect=FileNotFoundError("python3"))
        self.assertFalse(result["ok"])
        self.assertIn("couldn't start", result["reason"])


class Recheck(unittest.TestCase):
    def test_reads_a_fresh_process(self):
        fresh = json.dumps({"packages": pkgs()})
        done = subprocess.CompletedProcess([], 0, fresh, "")
        with mock.patch.object(check_env.subprocess, "run", return_value=done) as run:
            self.assertEqual(check_env.recheck_packages(), pkgs())
        cmd = run.call_args.args[0]
        self.assertEqual(cmd[0], sys.executable)
        self.assertEqual(cmd[2:], ["--packages-only", "--json"])

    def test_falls_back_to_this_process(self):
        with mock.patch.object(check_env.subprocess, "run", side_effect=OSError("no")), \
                mock.patch.object(check_env, "check_packages", return_value=pkgs()) as here:
            self.assertEqual(check_env.recheck_packages(), pkgs())
        here.assert_called_once()

    def test_the_real_script_answers_it(self):
        # A real child Python on check_env.py --packages-only --json: no network, nothing installed.
        packages = check_env.recheck_packages()
        self.assertEqual([p["package"] for p in packages], [name for name, _ in check_env.PACKAGES])


class Main(unittest.TestCase):
    def run_main(self, argv, before, after=None, pip=None):
        """main() with the packages as `before` (and `after` a pip run) and every source reachable."""
        out = io.StringIO()
        with mock.patch.object(check_env, "check_packages", return_value=before), \
                mock.patch.object(check_env, "recheck_packages", return_value=before if after is None else after) as recheck, \
                mock.patch.object(check_env, "check_sources", return_value=SOURCES_OK) as sources, \
                mock.patch.object(check_env, "pip_install", return_value=pip) as install, \
                contextlib.redirect_stdout(out):
            self.assertEqual(check_env.main(argv), 0)
        return out.getvalue(), install, recheck, sources

    def test_install_does_nothing_when_every_package_works(self):
        text, install, recheck, _ = self.run_main(["--install"], pkgs())
        install.assert_not_called()
        recheck.assert_not_called()
        self.assertIn("READY: the required packages work and every source is reachable.", text)
        self.assertNotIn("INSTALLED", text)

    def test_install_installs_only_what_is_missing_and_says_so(self):
        text, install, recheck, _ = self.run_main(["--install"], pkgs(missing=("scipy",)), pkgs(),
                                                  pip_result(True, ["scipy"]))
        install.assert_called_once_with(["scipy"])
        recheck.assert_called_once()
        self.assertIn("install scipy with pip: done in 5 s", text)
        self.assertIn("INSTALLED: scipy (pip, 5 s).", text)
        self.assertIn("package scipy  ok", text)
        self.assertNotIn("ACTION", text)
        self.assertIn("READY", text)

    def test_a_failed_install_of_a_required_package_is_an_action(self):
        pip = pip_result(False, ["scipy"], "this Python is managed by the operating system (PEP 668), so ...",
                         ["error: externally-managed-environment"])
        text, *_ = self.run_main(["--install"], pkgs(missing=("scipy",)), pip=pip)
        self.assertIn("ACTION: pip could not install scipy: this Python is managed by the operating system", text)
        self.assertIn("(The command was: python3 -m pip install scipy)", text)
        self.assertIn("  pip| error: externally-managed-environment", text)
        self.assertNotIn("READY", text)

    def test_a_failed_install_of_pypdf_alone_is_only_a_note(self):
        pip = pip_result(False, ["pypdf", "cffi"], "PyPI isn't reachable from here")
        text, *_ = self.run_main(["--install"], pkgs(missing=("pypdf",)), pip=pip)
        self.assertIn("NOTE: pip could not install pypdf cffi: PyPI isn't reachable from here.", text)
        self.assertNotIn("ACTION", text)
        self.assertIn("READY", text)

    def test_a_success_that_still_fails_to_import_is_an_action(self):
        text, *_ = self.run_main(["--install"], pkgs(missing=("scipy",)), pkgs(missing=("scipy",)),
                                 pip_result(True, ["scipy"]))
        self.assertIn("ACTION: pip finished, but scipy still fail to import", text)

    def test_without_install_nothing_is_installed(self):
        text, install, recheck, _ = self.run_main([], pkgs(missing=("scipy",)))
        install.assert_not_called()
        recheck.assert_not_called()
        self.assertIn("ACTION: required packages missing: scipy. Install them with --install", text)

    def test_packages_only_skips_the_network(self):
        text, _, _, sources = self.run_main(["--packages-only"], pkgs())
        sources.assert_not_called()
        self.assertIn("READY: the required packages work.", text)
        self.assertNotIn("source ", text)

    def test_json_carries_the_install(self):
        text, *_ = self.run_main(["--install", "--json"], pkgs(missing=("scipy",)), pkgs(),
                                 pip_result(True, ["scipy"]))
        data = json.loads(text)
        self.assertEqual(data["install"]["packages"], ["scipy"])
        self.assertTrue(all(p["ok"] for p in data["packages"]))
        self.assertEqual(len(data["sources"]), len(check_env.SOURCES))


if __name__ == "__main__":
    unittest.main()
