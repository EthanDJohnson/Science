"""Tests for gr_tensors.py. Run from the project root:

    python3 -m unittest discover -s .claude/skills/conundrum/scripts/tests -v
"""
import math
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import numpy as np  # noqa: E402
import sympy as sp  # noqa: E402

from gr_tensors import C, G_NEWTON, Spacetime, metrics, selftest, to_si  # noqa: E402


class SelfTest(unittest.TestCase):
    def test_selftest_passes(self):
        self.assertTrue(selftest(verbose=False))


class Construction(unittest.TestCase):
    def test_from_adm_matches_alcubierre_line_element(self):
        st, s = metrics.alcubierre()
        v, f, rs = s["v"], s["f"], s["r_s"]
        expected = sp.Matrix([[-1 + v**2 * f(rs) ** 2, -v * f(rs), 0, 0],
                              [-v * f(rs), 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
        self.assertEqual(sp.simplify(st.g - expected), sp.zeros(4, 4))

    def test_eulerian_observer_is_unit_timelike(self):
        st, _ = metrics.alcubierre()
        n = st.eulerian_observer()
        self.assertEqual(sp.simplify((n.T * st.g * n)[0, 0]), -1)

    def test_rejects_non_square_metric(self):
        t, x = sp.symbols("t x")
        with self.assertRaises(ValueError):
            Spacetime(sp.Matrix([[1, 0, 0]]), [t, x])


class Numerics(unittest.TestCase):
    def test_unassigned_symbols_are_reported(self):
        st, s = metrics.alcubierre()
        with self.assertRaises(ValueError) as ctx:
            st.compile(st.energy_density())  # v and f left unassigned
        self.assertIn("v", str(ctx.exception))

    def test_top_hat_energy_matches_radial_reference(self):
        # For spherically symmetric f, E = -(v^2/12) * int_0^inf f'(r)^2 r^2 dr.
        st, s = metrics.alcubierre()
        top = metrics.alcubierre_top_hat(s)
        params = {s["v"]: 1.0, s["R"]: 1.0, s["sigma"]: 8.0}
        e3d = st.integrate_on_slice(st.energy_density(), t=0.0, bounds=[(-1.8, 1.8)] * 3, n=96,
                                    params=params, functions={s["f"]: top})
        r = sp.symbols("r", positive=True)
        fprime = sp.lambdify(r, sp.diff(top(r), r).subs(params), "numpy")
        rr = np.linspace(1e-6, 4, 200001)
        e1d = -(1.0 / 12) * np.trapezoid(fprime(rr) ** 2 * rr**2, rr)
        self.assertAlmostEqual(e3d, e1d, delta=1e-4 * abs(e1d))

    def test_energy_scales_as_v_squared(self):
        st, s = metrics.alcubierre()
        gauss = sp.Lambda(sp.symbols("q", positive=True), sp.exp(-sp.symbols("q", positive=True) ** 2))
        rho = st.energy_density()
        e1 = st.integrate_on_slice(rho, 0.0, [(-4, 4)] * 3, 48, {s["v"]: 1.0}, {s["f"]: gauss})
        e3 = st.integrate_on_slice(rho, 0.0, [(-4, 4)] * 3, 48, {s["v"]: 3.0}, {s["f"]: gauss})
        self.assertAlmostEqual(e3 / e1, 9.0, places=6)


class Units(unittest.TestCase):
    def test_si_conversions(self):
        self.assertAlmostEqual(to_si.energy_joules(1.0), C**4 / G_NEWTON)
        self.assertAlmostEqual(to_si.mass_kg(1.0) / 1.3466e27, 1.0, places=3)  # c^2/G in kg/m
        self.assertAlmostEqual(to_si.energy_density_j_per_m3(2.0), 2 * C**4 / G_NEWTON)
        self.assertTrue(math.isclose(to_si.energy_joules(1.0), to_si.mass_kg(1.0) * C**2))


if __name__ == "__main__":
    unittest.main()
