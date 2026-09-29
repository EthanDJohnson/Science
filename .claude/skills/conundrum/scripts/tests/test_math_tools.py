"""Tests for math_checks.py and math_run.py.

Run from the project root:
    python3 -m unittest discover -s .claude/skills/conundrum/scripts/tests -v
"""
import contextlib
import io
import os
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

import math_checks as mc  # noqa: E402
import math_run as mr  # noqa: E402
import sympy as sp  # noqa: E402


def quiet(fn, *args, **kwargs):
    return fn(*args, verbose=False, **kwargs)


class Checks(unittest.TestCase):
    def setUp(self):
        mc.RESULTS.clear()

    def test_identity(self):
        self.assertEqual(quiet(mc.identity, "sin(x)**2 + cos(x)**2", "1").method, "symbolic")
        passed = quiet(mc.identity, "atan(x) + atan(1/x)", "pi/2")
        self.assertEqual(passed.status, "pass")
        self.assertIn("numeric at", passed.method)                  # SymPy can't close it; the numbers can
        failed = quiet(mc.identity, "(x + 1)**2", "x**2 + 1")
        self.assertEqual(failed.status, "fail")
        self.assertIn("x", failed.counterexample)
        self.assertEqual(quiet(mc.identity, "atan(x) + atan(1/x)", "pi/2", domain={"x": (-10, -0.1)}).status, "fail")

    def test_sympy_expressions_keep_their_own_symbols(self):
        v, R, D = sp.symbols("v R Delta", positive=True)
        energy = -(v**2 / 12) * (R**2 / D + D / 12)
        self.assertTrue(quiet(mc.identity, energy, -v**2 * R**2 / (12 * D) - v**2 * D / 144))
        self.assertTrue(quiet(mc.sign, energy, "negative"))

    def test_domain_ends_are_sampled(self):
        failed = quiet(mc.inequality, "sqrt(1 - v**2)", "<", "1", domain={"v": (0, 0.9)})
        self.assertEqual(failed.status, "fail")
        self.assertEqual(failed.counterexample, {"v": "0.0"})
        self.assertTrue(quiet(mc.inequality, "sqrt(1 - v**2)", "<", "1", domain={"v": (1e-9, 0.9)}))

    def test_names_sympy_reserves_are_flagged(self):
        self.assertIn("Euler", quiet(mc.identity, "E*t", "t*exp(1)").note)
        self.assertIn("imaginary", quiet(mc.identity, "exp(I*x)", "cos(x) + I*sin(x)").note)
        self.assertEqual(quiet(mc.identity, "Energy*t", "t*Energy").note, "")

    def test_undecided_when_nothing_evaluates(self):
        self.assertEqual(quiet(mc.identity, "log(-x) + x", "log(-x) + 2*x").status, "fail")   # complex values still compare
        self.assertEqual(quiet(mc.identity, "1/(x - x)", "0").status, "undecided")

    def test_sign_and_inequality(self):
        self.assertEqual(quiet(mc.sign, "x**3 - x", "positive", domain={"x": (-2, 2)}).status, "fail")
        self.assertTrue(quiet(mc.sign, "x**2", "nonnegative", domain={"x": (-3, 3)}))    # zero at the midpoint is fine
        self.assertTrue(quiet(mc.inequality, "x**2 + 1", ">=", "2*x", domain={"x": (-10, 10)}))
        with self.assertRaises(ValueError):
            quiet(mc.inequality, "x", "=>", "1")
        with self.assertRaises(ValueError):
            quiet(mc.sign, "x", "big")

    def test_limits_and_series(self):
        self.assertTrue(quiet(mc.limit, "(sqrt(1 + x) - 1)/x", "x", 0, "1/2"))
        self.assertTrue(quiet(mc.limit, "(1 + 1/n)**n", "n", "oo", "exp(1)"))
        self.assertEqual(quiet(mc.limit, "sin(x)/x", "x", 0, "2").status, "fail")
        self.assertTrue(quiet(mc.series, "sqrt(1 + x)", "x", 0, 3, "1 + x/2 - x**2/8"))
        self.assertEqual(quiet(mc.series, "cos(x)", "x", 0, 4, "1 - x**2").status, "fail")

    def test_quantities_and_units(self):
        self.assertTrue(quiet(mc.quantity, "G*Msun/c^2", "1476.6 m", rel_tol=1e-4))
        self.assertEqual(quiet(mc.quantity, "G*Msun/c^2", "1.5 km").status, "fail")
        self.assertIn("dimensions", quiet(mc.quantity, "G*Msun/c^2", "1 s").method)
        self.assertTrue(quiet(mc.units, "0.5 * 1 kg * (3 m/s)^2", "energy"))
        self.assertTrue(quiet(mc.units, "0.5 * 1 kg * (3 m/s)^2", "J"))
        self.assertEqual(quiet(mc.units, "1 J / 1 s", "energy").status, "fail")

    def test_finish_and_command_line(self):
        quiet(mc.identity, "x", "x")
        self.assertEqual(mc.finish(verbose=False), 0)
        quiet(mc.identity, "x", "2*x")
        self.assertEqual(mc.finish(verbose=False), 1)
        with contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(mc.main(["identity", "sinh(x)**2", "cosh(x)**2 - 1"]), 0)
            self.assertEqual(mc.main(["sign", "x**3 - x", "positive", "--domain", "x=-2:2"]), 1)
        self.assertIn("FAIL x**3 - x is positive", out.getvalue())

    def test_selftest(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertTrue(mc.selftest())


class Runner(unittest.TestCase):
    def setUp(self):
        self.box = tempfile.TemporaryDirectory()
        self.root = Path(os.path.realpath(self.box.name))
        self.checks = self.root / "runs" / "s" / "math" / "constraints"
        self.checks.mkdir(parents=True)
        self.here = os.getcwd()
        os.chdir(self.root)

    def tearDown(self):
        os.chdir(self.here)
        self.box.cleanup()

    def script(self, name: str, body: str) -> str:
        (self.checks / name).write_text(body)
        return f"runs/s/math/constraints/{name}"

    def run_main(self, *argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = mr.main(list(argv))
        return code, out.getvalue(), err.getvalue()

    def test_output_is_counted_and_logged(self):
        path = self.script("M-1.py", "print('PASS a')\nprint('FAIL b')\nprint('SUMMARY: 1 pass')\n"
                                     "import sys; print('oops', file=sys.stderr); sys.exit(1)\n")
        code, out, _ = self.run_main(path)
        self.assertEqual(code, 1)
        self.assertIn("1 PASS, 1 FAIL, 0 UNDECIDED", out)
        log = (self.checks / "M-1.py.log").read_text()
        for part in ("exit:     1", "counts:   1 PASS, 1 FAIL, 0 UNDECIDED", "sympy", "--- stdout ---\nPASS a", "oops"):
            self.assertIn(part, log)

    def test_timeout(self):
        path = self.script("slow.py", "import time\nprint('PASS early', flush=True)\ntime.sleep(5)\n")
        code, out, _ = self.run_main(path, "--timeout", "1")
        self.assertEqual(code, 124)
        self.assertIn("timed out after 1 s", (self.checks / "slow.py.log").read_text())

    def test_refusals(self):
        (self.root / "loose.py").write_text("print('PASS')\n")
        evil = self.script("evil.py", "open('.claude/skills/conundrum/scripts/x.py', 'w').write('1')\n")
        (self.checks / "notes.txt").write_text("hi")
        for path, why in (("loose.py", "not under runs/"), (evil, "protected path"),
                          ("runs/s/math/constraints/notes.txt", "not a Python file")):
            with self.subTest(path=path):
                code, _, err = self.run_main(path)
                self.assertEqual(code, 2)
                self.assertIn(why, err)
        self.assertFalse((self.root / ".claude").exists())


if __name__ == "__main__":
    unittest.main()
