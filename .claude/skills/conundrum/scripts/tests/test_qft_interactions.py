"""Tests for qft_interactions.py: every public function states its quantity and validity, out-of-range inputs
are refused, and the command line takes SI units. (The full physics self-test runs in test_calculators.py.)

Run from the project root:
    python3 -m unittest discover -s .claude/skills/conundrum/scripts/tests -p "test_qft_interactions.py" -v
"""
import contextlib
import inspect
import io
import math
import sys
import unittest
from pathlib import Path

import numpy as np

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

import qft_interactions as qi  # noqa: E402


def public_functions():
    return [(name, fn) for name, fn in inspect.getmembers(qi, inspect.isfunction)
            if not name.startswith("_") and fn.__module__ == qi.__name__ and name not in ("main", "selftest")]


def run_cli(argv):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = qi.main(argv)
    return code, buf.getvalue()


class Docstrings(unittest.TestCase):
    def test_every_public_function_states_quantity_and_validity(self):
        funcs = public_functions()
        self.assertGreater(len(funcs), 8)
        for name, fn in funcs:
            doc = inspect.getdoc(fn) or ""
            with self.subTest(function=name):
                self.assertRegex(doc, r"(?m)^Quantity: \S", f"{name} lacks a 'Quantity:' line")
                self.assertRegex(doc, r"(?m)^Valid when: \S", f"{name} lacks a 'Valid when:' line")

    def test_module_docstring_states_units_and_traps(self):
        self.assertIn("hbar = c = 1", qi.__doc__)
        self.assertIn("Heaviside-Lorentz", qi.__doc__)
        self.assertIn("rescattering", qi.__doc__)
        self.assertIn("PHYSICAL", qi.__doc__)


class RadiativeRefusals(unittest.TestCase):
    def test_refusals(self):
        pts = qi.circle_instanton(1.0, 1.0, 256)
        bad = [
            lambda: qi.schwinger_radiative_rate(1.0, 2.0),                 # eE > m^2: not a weak field
            lambda: qi.schwinger_radiative_rate(1.0, 0.1, alpha=0.0),       # no coupling
            lambda: qi.schwinger_radiative_rate(1.0, 0.1, alpha=2.0),       # alpha > 1
            lambda: qi.schwinger_radiative_rate(1.0, 0.9, alpha=0.5),       # kappa = 4 pi alpha eE/m^2 > 1
            lambda: qi.schwinger_radiative_rate(0.0, 0.1),                  # massless: no instanton
            lambda: qi.circle_instanton(1.0, 0.1, 8),                       # too few points
            lambda: qi.circle_exchange_action_closed(0.0),                  # no regulator
            lambda: qi.worldline_exchange_action(pts, 0.01),                # a below 5 x spacing (0.0245)
            lambda: qi.worldline_exchange_action(pts, 0.2, scheme="dimreg"),
            lambda: qi.worldline_coulomb_action(pts, [0.3, 0.2]),           # too few regulators to extrapolate
        ]
        for i, fn in enumerate(bad):
            with self.subTest(case=i), self.assertRaises(ValueError):
                fn()

    def test_rate_bookkeeping(self):
        sp = qi.schwinger_radiative_rate(1.0, 0.1)
        sc = qi.schwinger_radiative_rate(1.0, 0.1, fermion=False)
        self.assertAlmostEqual(sp["all_orders"] / sp["one_loop"], math.exp(math.pi * qi.ALPHA_FS), places=14)
        self.assertAlmostEqual(sp["one_loop"] / sc["one_loop"], 2.0, places=14)   # spin factor 2s + 1
        self.assertLess(sp["one_loop"], sp["two_loop"])
        self.assertLess(sp["two_loop"], sp["all_orders"])
        self.assertIsNone(sc["next_rel"])
        self.assertAlmostEqual(1 / qi.ALPHA_FS, 137.036, places=3)

    def test_finite_part_is_scheme_independent_for_an_ellipse(self):
        th = 2 * np.pi * np.arange(2048) / 2048
        pts = np.stack([1.5 * np.cos(th), 0.7 * np.sin(th)], 1)
        av = [0.1, 0.07, 0.05, 0.035]
        p = qi.worldline_coulomb_action(pts, av)["V0"]
        g = qi.worldline_coulomb_action(pts, av, scheme="gaussian")["V0"]
        self.assertAlmostEqual(p, g, places=5)
        self.assertLess(p, -0.25)          # less round than the circle: more exchange action per e^2


class FloquetRefusals(unittest.TestCase):
    def test_refusals(self):
        bad = [
            lambda: qi.mathieu_characteristic_values(-1.0, 3),              # q < 0 not supported
            lambda: qi.mathieu_characteristic_values(1.0, 500),             # n_max too large
            lambda: qi.mathieu_band_edges(0.5, 0),                          # band 0 is A < a_0
            lambda: qi.mathieu_floquet_exponent([np.inf], 0.1),
            lambda: qi.mathieu_floquet_exponent([1.0], 1e7),                # too many steps per period
            lambda: qi.preheating_floquet([1.0], 0.0, 0.1, 10.0),           # m_phi = 0
            lambda: qi.preheating_floquet([-1.0], 1.0, 0.1, 10.0),          # k < 0
            lambda: qi.preheating_resonance_bands(1.0, 0.1, 10.0, n_bands=0),
        ]
        for i, fn in enumerate(bad):
            with self.subTest(case=i), self.assertRaises(ValueError):
                fn()

    def test_free_limit(self):
        # q = 0: Delta = cos(pi sqrt(A)) for A > 0, cosh(pi sqrt(-A)) for A < 0; no growth inside the stable range
        r = qi.mathieu_floquet_exponent([4.0, 2.0, -1.0], 0.0)
        np.testing.assert_allclose(r["half_trace"], [1.0, math.cos(math.pi * math.sqrt(2)), math.cosh(math.pi)],
                                   rtol=1e-10)
        self.assertEqual(float(r["mu"][1]), 0.0)
        self.assertAlmostEqual(float(r["mu"][2]), 1.0, places=9)   # A = -1: y ~ e^{z}

    def test_broad_resonance_bands_start_above_2q(self):
        bands = qi.preheating_resonance_bands(1.0, 1e-4, 1e5)       # q = 25
        self.assertTrue(bands)
        self.assertGreaterEqual(bands[0]["n"], 7)                   # a_n(25) < 2q for n <= 6
        self.assertGreater(bands[0]["mu_max"], 0.05)


class HartreeRefusals(unittest.TestCase):
    def test_refusals(self):
        base = dict(m_phi=1.0, g=0.1, Phi=60.0, t_end=20.0, n_modes=(32, 32))
        bad = [
            dict(base, m_phi=0.0),
            dict(base, Phi=-1.0),
            dict(base, kmax=0.5),                                   # kmax below kappa = m_phi
            dict(base, Phi=6.0, lam=500.0, t_end=5.0),              # lam L > 1: Landau pole
            dict(base, steps_per_halfperiod=20),                    # step-size resonance of the splitting
            dict(base, t_end=30.0, kmax=1.6),                       # cutoff inside the resonance band
            dict(base, m_chi=0.0, Phi=0.0, lam=0.0),                # M^2(0) = 0: no adiabatic vacuum
        ]
        for i, kw in enumerate(bad):
            with self.subTest(case=i), self.assertRaises(ValueError):
                qi.hartree_preheating(**kw)

    def test_quantities_and_conservation(self):
        r = qi.hartree_preheating(1.0, 0.1, 30.0, t_end=20.0, n_modes=(48, 64), kmax=14.0)
        for key in ("t", "phi0", "n_chi", "rho_chi", "rho_phi", "chi2_ren", "adiabaticity", "energy_drift"):
            self.assertEqual(len(r[key]), len(r["t"]))
        self.assertLess(r["energy_drift_max"], 1e-5)
        self.assertLess(r["wronskian_error"], 1e-11)
        self.assertGreater(r["n_chi"][-1], 0.0)
        self.assertAlmostEqual(r["n_chi"][-1], float(np.sum(r["W"] * r["n_k"])), places=10)


class CommandLine(unittest.TestCase):
    def test_radiative_cli_units(self):
        code, out = run_cli(["radiative", "--E", "1e17 V/m"])
        self.assertEqual(code, 0)
        self.assertIn("m^-3 s^-1", out)
        self.assertIn("exp(pi alpha) = 1.0231901", out)
        code, _ = run_cli(["radiative", "--E", "3 J"])            # not a field
        self.assertEqual(code, 1)

    def test_floquet_and_preheat_cli_units(self):
        code, out = run_cli(["floquet", "--m-phi", "1e13 GeV", "--g", "1e-4", "--Phi", "1e18 GeV", "--k", "2.5e13 GeV"])
        self.assertEqual(code, 0)
        self.assertIn("q = g^2 Phi^2/(4 m_phi^2) = 25", out)
        self.assertIn("s^-1", out)
        code, out = run_cli(["preheat", "--m-phi", "1e13 GeV", "--g", "1e-3", "--Phi", "6e15 GeV", "--t-end", "10"])
        self.assertEqual(code, 0)
        self.assertIn("PARTICLES", out)
        code, _ = run_cli(["preheat", "--m-phi", "1e13 GeV", "--g", "1e-3", "--Phi", "3 m"])   # a length, not an energy
        self.assertEqual(code, 1)


if __name__ == "__main__":
    unittest.main()
