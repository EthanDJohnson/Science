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
        for header in ("Python usage", "Command line", "Assumptions and validity", "Quantity:", "Valid when:"):
            self.assertIn(header, qi.__doc__)

    def test_lcfa_validity_is_stated_for_weak_fields(self):
        # The LCFA needs eE0 L^2 >> (m^2/eE0)^2 as well as >> 1; the old "O(1/(eE0 L^2))" claim alone was wrong.
        for fn in (qi.lcfa_rates_per_area, qi.sauter_step_lcfa_closed_form):
            self.assertIn("pi m^4/(4 eE0^3 L^2) << 1", inspect.getdoc(fn))
        self.assertIn("(m^2/eE0)^2", qi.__doc__)


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
            lambda: qi.klein_zone([-1.0], 1.0, 2.0, -2.0),                        # k_perp < 0
            lambda: qi.rates_from_n(lambda o, k: np.full_like(o, np.nan), 2.0, -2.0, 1.0, True),       # NaN n
            lambda: qi.rates_from_n(lambda o, k: np.full_like(o, 0.1), 2.0, -2.0, 1.0, True, eE_max=0.0),   # eE_max = 0
            lambda: qi.rates_from_n(lambda o, k: np.full_like(o, 0.1), 2.0, -2.0, 1.0, True, eE_max=-1.0),  # eE_max < 0
            lambda: qi.sauter_step_rates(1.0, 1.0, 2.0, True, 4, 4, strict=True),  # coarse quadrature (2.6% change)
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


class Precision(unittest.TestCase):
    def test_closed_form_rates_flag_unresolved_quadrature(self):
        self.assertFalse(qi.sauter_step_rates(1.0, 1.0, 2.0, True, 4, 4)["resolved"])
        self.assertTrue(qi.sauter_step_rates(1.0, 1.0, 2.0, True)["resolved"])

    def test_ck_eq47_all_heights(self):
        # F(arcsin al, 1/al) sat on its branch point: about half of all heights raised TypeError (e.g. dV = 20, 2000).
        vs = np.concatenate([1.0 + np.geomspace(1e-6, 5e-2, 25), np.linspace(1.1, 3.0, 40)[:-1], np.geomspace(3.0, 1e3, 40)])
        w = np.array([qi.klein_step_decay_rate_scalar(1.0, 2.0 * v) for v in vs])
        self.assertTrue(np.all(np.isfinite(w)) and np.all(w > 0))
        self.assertTrue(np.all(np.diff(w) > 0))                                    # grows with the step height
        # near threshold the closed form must not lose digits: w ~ (v - m)^2/(4 pi) (independently: a 40-digit
        # mpmath double quadrature of ln(1 + n) gave 7.9577484809e-14 at v - m = 1e-6)
        self.assertAlmostEqual(qi.klein_step_decay_rate_scalar(1.0, 2.0 * (1 + 1e-6)) / 7.9577484809e-14, 1.0, delta=1e-8)
        for v in (1.0001, 1.01, 2.5, 10.0, 100.0, 1000.0):                         # vs quadrature of ln(1 + n): ~3e-7
            q = qi.rates_from_n(lambda o, k: qi.klein_step_n_scalar(o, k, 1.0, 2 * v), v, -v, 1.0, False)["decay_rate"]
            with self.subTest(v=v):
                self.assertLess(abs(q / qi.klein_step_decay_rate_scalar(1.0, 2 * v) - 1), 2e-6)
        self.assertGreater(qi.klein_step_rates(1.0, 2000.0, False)["decay_rate"], 0.0)

    def test_lcfa_window_independent(self):
        # A window 200x wider than the field used to miss the peak (0.27 x the right answer, unflagged).
        f = lambda z: 2.0 * np.exp(-z * z)                                          # noqa: E731
        ref = qi.lcfa_rates_per_area(f, -8.0, 8.0, 1.0, True)
        for half in (200.0, 1e5):
            r = qi.lcfa_rates_per_area(f, -half, half, 1.0, True)
            with self.subTest(half=half):
                self.assertTrue(r["resolved"])
                self.assertAlmostEqual(r["pair_rate"] / ref["pair_rate"], 1.0, delta=1e-9)
                self.assertAlmostEqual(r["decay_rate"] / ref["decay_rate"], 1.0, delta=1e-9)
        # Lorentzian (1/z^2 tail) on +-3000 L: the old fixed 800-node rule returned 1.5e-16 instead of 3.0e-2.
        g = lambda z: 3.778 / (1 + (z / 0.518) ** 2)                                # noqa: E731
        self.assertAlmostEqual(qi.lcfa_rates_per_area(g, -1554.0, 1554.0, 1.0, True)["pair_rate"]
                               / qi.lcfa_rates_per_area(g, -26.0, 26.0, 1.0, True)["pair_rate"], 1.0, delta=1e-8)

    def test_solver_survives_overflowing_coarse_pass_and_does_not_false_converge(self):
        # Window +-600 = 400 L: a 4-step pass overflowed (old: ValueError "n < ~1e-600"), and 4 vs 8 steps sampled only
        # the plateaus, agreeing on the SHARP-step n = 0.52 (true 0.0226). Now: renormalised, started at >= 16 steps
        # across the field.
        V, (z0, z1), _ = qi.sauter_step_potential(1.0, 1.5, ends=400)
        r = qi.klein_mode_spinor(V, z0, z1, [0.2], [0.1], 1.0, steps=4)
        self.assertTrue(bool(r["resolved"][0]))
        self.assertAlmostEqual(float(r["n"][0]) / float(qi.sauter_step_n_spinor(0.2, 0.1, 1.0, 1.0, 1.5)), 1.0, delta=1e-5)

    def test_underflowing_n_keeps_ln_n(self):
        # n = 4.6e-440: 'n' underflows to 0.0 but ln_n is exact, flux_error is finite, and no numpy warning leaks.
        import warnings
        V, (z0, z1), _ = qi.sauter_step_potential(0.004, 300.0, ends=10)
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            r = qi.klein_mode_scalar(V, z0, z1, [0.0], [0.0], 1.0, steps=4000, rtol=1e-6)
        ref = float(qi.sauter_step_n_scalar(0.0, 0.0, 1.0, 0.004, 300.0, log=True))
        self.assertAlmostEqual(ref, -1011.6064, delta=1e-3)
        self.assertLess(abs(float(r["ln_n"][0]) - ref), 1e-4)
        self.assertTrue(bool(r["resolved"][0]) and np.isfinite(r["flux_error"][0]))
        self.assertEqual(float(qi.sauter_step_n_scalar(0.0, 0.0, 1.0, 0.004, 300.0)), 0.0)


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

    def test_profile_cli_every_shape(self):
        for shape in ("sauter", "gauss"):
            with self.subTest(shape=shape):
                code, out = self.run_cli(["profile", "--shape", shape, "--E", "2.6e18 V/m", "--L", "5e-13 m", "--n", "6"])
                self.assertEqual(code, 0, out)
                self.assertIn("resolved True", out)
                self.assertRegex(out, r"exact/LCFA = 0\.[56]")      # 0.584 (gauss), 0.638 (sauter)
        with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
            self.run_cli(["profile", "--shape", "lorentz", "--E", "2.6e18 V/m", "--L", "5e-13 m"])   # removed: 1/z^2 tail

    def test_bad_units_return_1(self):
        self.assertEqual(self.run_cli(["sauter", "--E", "3 J", "--L", "1e-12 m"])[0], 1)          # energy, not a field
        self.assertEqual(self.run_cli(["sauter", "--E", "1e18 V/m", "--L", "2 s"])[0], 1)         # time, not a length


if __name__ == "__main__":
    unittest.main()
