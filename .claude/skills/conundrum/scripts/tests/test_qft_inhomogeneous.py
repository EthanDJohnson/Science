"""Tests for qft_inhomogeneous.py: every public function states its quantity and validity, out-of-range
inputs are refused, and the command line takes SI units. (The full physics self-test runs in test_calculators.py.)

Run from the project root:
    python3 -m unittest discover -s .claude/skills/conundrum/scripts/tests -p "test_qft_inhomogeneous.py" -v
"""
import contextlib
import inspect
import io
import sys
import unittest
from pathlib import Path

import numpy as np

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

import qft_inhomogeneous as qi  # noqa: E402


def public_functions():
    return [(name, fn) for name, fn in inspect.getmembers(qi, inspect.isfunction)
            if not name.startswith("_") and fn.__module__ == qi.__name__ and name not in ("main", "selftest")]


class Docstrings(unittest.TestCase):
    def test_every_public_function_states_quantity_and_validity(self):
        funcs = public_functions()
        self.assertGreater(len(funcs), 15)
        for name, fn in funcs:
            doc = inspect.getdoc(fn) or ""
            with self.subTest(function=name):
                self.assertRegex(doc, r"(?m)^Quantity: \S", f"{name} lacks a 'Quantity:' line")
                self.assertRegex(doc, r"(?m)^Valid when: \S", f"{name} lacks a 'Valid when:' line")

    def test_module_docstring_states_units_and_traps(self):
        self.assertIn("hbar = c = 1", qi.__doc__)
        self.assertIn("Heaviside-Lorentz", qi.__doc__)
        self.assertIn("Klein zone", qi.__doc__.replace("KLEIN ZONE", "Klein zone"))
        self.assertIn("vacuum-decay", qi.__doc__)


class Refusals(unittest.TestCase):
    def test_closed_form_refusals(self):
        bad = [
            lambda: qi.sauter_step_n_spinor(0.0, 0.0, 1.0, -1.0, 2.0),            # eE0 < 0
            lambda: qi.sauter_step_n_scalar(0.0, 0.0, 1.0, 1.0, 0.0),             # L = 0
            lambda: qi.sauter_step_n_scalar(0.0, -0.3, 1.0, 1.0, 2.0),            # k_perp < 0
            lambda: qi.sauter_step_n_spinor(0.0, 0.0, -1.0, 1.0, 2.0),            # m < 0
            lambda: qi.klein_step_n_spinor(0.0, 0.0, 1.0, 0.0),                   # no step
            lambda: qi.klein_step_decay_rate_scalar(0.0, 4.0),                    # massless: CK eq. 47 needs m > 0
            lambda: qi.klein_zone([0.0], 1.0, 2.0, 2.0),                          # V_left = V_right
            lambda: qi.sauter_step_potential(1.0, 2.0, ends=3.0),                 # window too short
            lambda: qi.sauter_step_lcfa_closed_form(0.0, 1.0, 2.0, True),         # LCFA needs m > 0
            lambda: qi.lcfa_rates_per_area(lambda z: z, 1.0, -1.0, 1.0, True),    # reversed window
        ]
        for i, fn in enumerate(bad):
            with self.subTest(case=i), self.assertRaises(ValueError):
                fn()

    def test_solver_refusals(self):
        V, (z0, z1), _ = qi.sauter_step_potential(1.0, 1.5)
        bad = [
            lambda: qi.klein_mode_scalar(V, z1, z0, [0.0], [0.0], 1.0),                    # reversed window
            lambda: qi.klein_mode_spinor(V, -2.0, 2.0, [0.0], [0.0], 1.0),                 # field still on at the ends
            lambda: qi.klein_mode_scalar(V, z0, z1, [0.0], [0.0], 1.0, steps=1),           # too few steps
            lambda: qi.potential_from_field(lambda z: z, 0.0, 1.0, n=10),                  # grid too coarse
            lambda: qi.rates_from_n(lambda o, k: np.full_like(o, 1.5), 1.5, -1.5, 1.0, True),   # Pauli: n > 1
            lambda: qi.rates_numeric(lambda z: 0.0 * np.asarray(z), -1.0, 1.0, 1.0, True),       # no step at all
            lambda: qi.klein_mode_spinor(V, z0, z1, [0.0], [0.0], 1.0, max_eps_end=0.9),   # meaningless plane-wave ends
        ]
        for i, fn in enumerate(bad):
            with self.subTest(case=i), self.assertRaises(ValueError):
                fn()

    def test_strict_refuses_unresolved(self):
        V, (z0, z1), _ = qi.sauter_step_potential(1.0, 1.5)
        with self.assertRaises(ValueError):
            qi.klein_mode_scalar(V, z0, z1, [0.2], [0.1], 1.0, steps=2, max_steps=4, rtol=1e-12, strict=True)


class Physics(unittest.TestCase):
    def test_outside_klein_zone_is_zero_not_transmission(self):
        # omega above the zone (over-barrier): the formula would give a transmission probability; n must be 0.
        self.assertEqual(float(qi.sauter_step_n_spinor(5.0, 0.0, 1.0, 1.0, 1.5)), 0.0)
        V, (z0, z1), _ = qi.sauter_step_potential(1.0, 1.5)
        r = qi.klein_mode_scalar(V, z0, z1, [5.0, 0.0], [0.0, 0.0], 1.0)
        self.assertFalse(bool(r["in_klein_zone"][0]))
        self.assertEqual(float(r["n"][0]), 0.0)
        self.assertGreater(float(r["n"][1]), 0.0)

    def test_below_threshold_rates_vanish(self):
        for fermion in (True, False):
            r = qi.sauter_step_rates(1.0, 1.0, 0.9, fermion)
            self.assertTrue(r["zone_empty"])
            self.assertEqual(r["pair_rate"], 0.0)
            self.assertEqual(r["decay_rate"], 0.0)

    def test_sharp_bosonic_step_pair_rate_is_infinite(self):
        r = qi.klein_step_rates(1.0, 4.0, fermion=False)
        self.assertEqual(r["pair_rate"], float("inf"))
        self.assertGreater(r["decay_rate"], 0.0)

    def test_numeric_rates_report_weighted_errors(self):
        V, (z0, z1), _ = qi.sauter_step_potential(1.0, 1.5)
        r = qi.rates_numeric(V, z0, z1, 1.0, True, n_omega=6, n_k=6, eE_max=1.0)
        self.assertTrue(r["resolved"])
        self.assertLess(r["pair_relerr"], 1e-6)
        self.assertGreater(r["pair_rate"], 0.0)

    def test_pair_and_decay_rates_order(self):
        rf = qi.sauter_step_rates(1.0, 3.0, 3.0, True)
        rb = qi.sauter_step_rates(1.0, 3.0, 3.0, False)
        self.assertGreater(rf["decay_rate"], rf["pair_rate"])
        self.assertLess(rb["decay_rate"], rb["pair_rate"])


class CommandLine(unittest.TestCase):
    def run_cli(self, argv):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = qi.main(argv)
        return code, buf.getvalue()

    def test_sauter_cli_si_units(self):
        code, out = self.run_cli(["sauter", "--E", "1.32e18 V/m", "--L", "1 pm"])
        self.assertEqual(code, 0)
        self.assertIn("pair-number rate", out)
        self.assertIn("m^-2 s^-1", out)
        self.assertIn("vacuum-decay rate", out)

    def test_below_threshold_cli(self):
        code, out = self.run_cli(["sauter", "--E", "1.32e18 V/m", "--L", "3e-13 m", "--scalar"])
        self.assertEqual(code, 0)
        self.assertIn("NO pairs", out)

    def test_mode_cli(self):
        code, out = self.run_cli(["mode", "--E", "1.32e18 V/m", "--L", "1e-12 m", "--omega", "0 eV", "--kperp", "100 keV"])
        self.assertEqual(code, 0)
        self.assertIn("closed form", out)
        self.assertIn("ODE", out)

    def test_bad_units_return_1(self):
        self.assertEqual(self.run_cli(["sauter", "--E", "3 J", "--L", "1e-12 m"])[0], 1)          # energy, not a field
        self.assertEqual(self.run_cli(["sauter", "--E", "1e18 V/m", "--L", "2 s"])[0], 1)         # time, not a length


if __name__ == "__main__":
    unittest.main()
