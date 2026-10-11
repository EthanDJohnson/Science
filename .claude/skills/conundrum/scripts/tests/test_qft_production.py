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


class ElectricFieldRefusals(unittest.TestCase):
    def test_refusals(self):
        pf, (t0, t1) = q.sauter_kinetic_momentum([0.0], 0.5, 2.0)
        bad = [
            lambda: q.bogoliubov_fermion_efield(pf, [1.0], -1.0, 1.0),        # field still on at the window ends
            lambda: q.bogoliubov_fermion_efield(pf, [0.0], t0, t1),           # eps_perp = 0
            lambda: q.sauter_n_scalar(0.0, 0.0, 0.0, 0.5, 2.0),               # m^2 + k_perp^2 = 0
            lambda: q.sauter_n_spinor(0.0, 0.3, 1.0, -0.5, 2.0),              # eE0 < 0
            lambda: q.schwinger_n_mode(0.3, 1.0, 0.0),                        # no field
            lambda: q.schwinger_closed_forms(0.0, 1.0, True),                 # massless: closed forms diverge
            lambda: q.rates_from_modes(lambda k: np.ones_like(k), 1.0, True, 5.0),   # Pauli: n_k = 1
        ]
        for i, fn in enumerate(bad):
            with self.subTest(case=i), self.assertRaises(ValueError):
                fn()

    def test_pair_rate_and_decay_rate_differ(self):
        r = q.rates_from_modes(lambda k: q.schwinger_n_mode(k, 1.0, 10.0), 10.0, True, 40.0)
        self.assertGreater(r["decay_rate"], 1.1 * r["pair_rate"])


class CommandLine(unittest.TestCase):
    def test_tanh_cli(self):
        import contextlib
        import io
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = q.main(["tanh", "--m", "1", "--A", "2", "--B", "1", "--rho", "0.5", "--k", "0.5"])
        self.assertEqual(code, 0)
        self.assertIn("closed form", buf.getvalue())

    def test_schwinger_cli_units(self):
        import contextlib
        import io
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = q.main(["schwinger", "--E", "1.32e18 V/m"])
        self.assertEqual(code, 0)
        self.assertIn("vacuum-decay rate", buf.getvalue())
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(q.main(["schwinger", "--E", "3 J"]), 1)


if __name__ == "__main__":
    unittest.main()
