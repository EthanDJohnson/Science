"""Tests for qft_production.py: every public function states its quantity and validity, and
out-of-range inputs are refused. (The full physics self-test runs in test_calculators.py.)

Run from the project root:
    python3 -m unittest discover -s .claude/skills/conundrum/scripts/tests -v
"""
import inspect
import sys
import unittest
from pathlib import Path

import numpy as np

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

import qft_production as q  # noqa: E402


def public_functions():
    return [(name, fn) for name, fn in inspect.getmembers(q, inspect.isfunction)
            if not name.startswith("_") and fn.__module__ == q.__name__ and name not in ("main", "selftest")]


class Docstrings(unittest.TestCase):
    def test_every_public_function_states_quantity_and_validity(self):
        funcs = public_functions()
        self.assertGreater(len(funcs), 8)
        for name, fn in funcs:
            doc = inspect.getdoc(fn) or ""
            with self.subTest(function=name):
                self.assertRegex(doc, r"(?m)^Quantity: \S", f"{name} lacks a 'Quantity:' line")
                self.assertRegex(doc, r"(?m)^Valid when: \S", f"{name} lacks a 'Valid when:' line")

    def test_module_docstring_states_units(self):
        self.assertIn("hbar = c = 1", q.__doc__)
        self.assertIn("Heaviside-Lorentz", q.__doc__)


class Refusals(unittest.TestCase):
    def test_mode_solver_refusals(self):
        w2, (t0, t1) = q.tanh_model_omega2([0.5], 1.0, 2.0, 1.0, 0.5)
        bad = [
            lambda: q.bogoliubov_boson(w2, t1, t0),                                    # reversed window
            lambda: q.bogoliubov_boson(lambda t: np.array([-1.0]), 0.0, 1.0),          # omega^2 < 0 at the ends
            lambda: q.bogoliubov_boson(w2, -1.0, 1.0),                                 # ends not adiabatic
            lambda: q.tanh_model_omega2([0.1], 1.0, 1.0, 2.0, 0.5),                    # omega^2 < 0 somewhere
            lambda: q.tanh_model_beta2([0.5], 1.0, 2.0, 1.0, 0.0),                     # rho = 0
            lambda: q.sudden_jump_beta2(-1.0, 2.0),
            lambda: q.number_density_isotropic(lambda k: k, -1.0),
        ]
        for i, fn in enumerate(bad):
            with self.subTest(case=i), self.assertRaises(ValueError):
                fn()

    def test_strict_refuses_below_floor(self):
        w2, (t0, t1) = q.tanh_model_omega2([0.5], 1.0, 2.0, 1.0, 0.07)
        with self.assertRaises(ValueError):
            q.bogoliubov_boson(w2, t0, t1, strict=True)


class CommandLine(unittest.TestCase):
    def test_tanh_cli(self):
        import contextlib
        import io
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = q.main(["tanh", "--m", "1", "--A", "2", "--B", "1", "--rho", "0.5", "--k", "0.5"])
        self.assertEqual(code, 0)
        self.assertIn("closed form", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
