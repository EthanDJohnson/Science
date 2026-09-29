"""Tests for gr_tensors.py. Run from the project root:

    python3 -m unittest discover -s .claude/skills/conundrum/scripts/tests -v
"""
import math
import os
import sys
import unittest
import warnings

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import numpy as np  # noqa: E402
import sympy as sp  # noqa: E402

from gr_tensors import (C, G_NEWTON, M_SUN, Spacetime, _boosted_fluid, classify_stress_energy,  # noqa: E402
                        horizons_1p1, metrics, qi, selftest, to_si)

Q = sp.symbols("q", positive=True)
GAUSS = sp.Lambda(Q, sp.exp(-(Q**2)))


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

    def test_closed_form_adm_inverse_is_the_inverse(self):
        for st, _ in (metrics.alcubierre(), metrics.van_den_broeck()):
            self.assertEqual(sp.simplify(st.g * st.ginv), sp.eye(4))

    def test_eulerian_observer_is_unit_timelike(self):
        st, _ = metrics.alcubierre()
        n = st.eulerian_observer()
        self.assertEqual(sp.simplify((n.T * st.g * n)[0, 0]), -1)

    def test_rejects_non_square_metric(self):
        t, x = sp.symbols("t x")
        with self.assertRaises(ValueError):
            Spacetime(sp.Matrix([[1, 0, 0]]), [t, x])


class EnergyDensity(unittest.TestCase):
    def test_hamiltonian_constraint_matches_einstein_tensor_for_van_den_broeck(self):
        st, s = metrics.van_den_broeck()
        fns = {s["f"]: GAUSS, s["B"]: sp.Lambda(Q, 1 + 2 * sp.exp(-4 * Q**2))}
        for p in [(0.0, 0.3, 0.2, -0.1), (0.2, -0.4, 0.5, 0.3)]:
            adm = st.evaluate(st.energy_density(), p, {s["v"]: 1.3}, fns)
            full = st.evaluate(st.energy_density(method="einstein"), p, {s["v"]: 1.3}, fns)
            self.assertAlmostEqual(adm, full, delta=1e-9 * max(1.0, abs(full)))

    def test_riemann_contracts_to_ricci(self):
        st, s = metrics.alcubierre()
        rm, ric = st.riemann(), st.ricci()
        point, params, fns = (0.0, 0.4, 0.5, 0.1), {s["v"]: 1.2}, {s["f"]: GAUSS}
        for b, d in [(0, 0), (0, 1), (1, 1), (2, 3)]:
            contracted = sum(rm[a][b][a][d] for a in range(4))
            self.assertAlmostEqual(st.evaluate(contracted, point, params, fns),
                                   st.evaluate(ric[b, d], point, params, fns), places=10)


class EnergyConditions(unittest.TestCase):
    def test_ordinary_fluid_satisfies_everything(self):
        r = classify_stress_energy(_boosted_fluid(rho=1.0, p=0.2, beta=0.5))
        self.assertEqual(r["type"], "I")
        self.assertTrue(all(r[k] for k in ("nec", "wec", "sec", "dec")))
        self.assertAlmostEqual(r["rho_rest"], 1.0, places=9)

    def test_negative_density_dust_fails_nec_and_wec(self):
        r = classify_stress_energy(np.diag([-1.0, 0.0, 0.0, 0.0]))
        self.assertFalse(r["nec"])
        self.assertFalse(r["wec"])

    def test_boosted_negative_density_is_not_a_false_pass(self):
        t = _boosted_fluid(rho=-1.0, p=3.0, beta=0.9)
        self.assertGreater(t[0, 0], 0)  # the moving observer sees positive density...
        r = classify_stress_energy(t)
        self.assertFalse(r["wec"])      # ...but the WEC still fails
        self.assertTrue(r["nec"])

    def test_alcubierre_wall_is_type_iv_and_violates_nec(self):
        st, s = metrics.alcubierre()
        r = st.energy_conditions((0.0, 0.4, 0.5, 0.1), {s["v"]: 1.0}, {s["f"]: GAUSS})
        self.assertTrue(r["type"].startswith("IV"))
        self.assertFalse(r["nec"])

    def test_region_scan_counts_violations(self):
        st, s = metrics.alcubierre()
        pts = [(0.0, x, y, 0.2) for x in (-0.6, 0.0, 0.6) for y in (0.3, 0.7)] + [(0.0, 4.0, 4.0, 4.0)]
        scan = st.scan_energy_conditions(pts, {s["v"]: 1.0}, {s["f"]: GAUSS})
        self.assertEqual(scan["points"], len(pts))
        self.assertGreaterEqual(scan["violations"]["nec"], 5)
        self.assertLess(scan["worst"]["nec_min"][0], 0)


class Numerics(unittest.TestCase):
    def test_unassigned_symbols_are_reported(self):
        st, _ = metrics.alcubierre()
        with self.assertRaises(ValueError) as ctx:
            st.compile(st.energy_density())  # v and f left unassigned
        self.assertIn("v", str(ctx.exception))

    def test_compile_is_cached_and_accepts_free_parameters(self):
        st, s = metrics.alcubierre()
        rho = st.energy_density()
        f1 = st.compile(rho, functions={s["f"]: GAUSS}, free=[s["v"]])
        f2 = st.compile(rho, functions={s["f"]: GAUSS}, free=[s["v"]])
        self.assertIs(f1, f2)
        p = (0.0, 0.3, 0.4, 0.1)
        self.assertAlmostEqual(f1(*p, 3.0) / f1(*p, 1.0), 9.0, places=9)

    def test_top_hat_energy_matches_radial_reference(self):
        # For spherically symmetric f, E = -(v^2/12) * int_0^inf f'(r)^2 r^2 dr.
        st, s = metrics.alcubierre()
        top = metrics.alcubierre_top_hat(s)
        params = {s["v"]: 1.0, s["R"]: 1.0, s["sigma"]: 8.0}
        e3d = st.integrate_on_slice(st.energy_density(), 0.0, [(-1.8, 1.8)] * 3, 96, params, {s["f"]: top})
        r = sp.symbols("r", positive=True)
        fprime = sp.lambdify(r, sp.diff(top(r), r).subs(params), "numpy")
        rr = np.linspace(1e-6, 4, 200001)
        e1d = -(1.0 / 12) * np.trapezoid(fprime(rr) ** 2 * rr**2, rr)
        self.assertAlmostEqual(e3d, e1d, delta=1e-4 * abs(e1d))

    def test_integrate_parts_splits_signs(self):
        st, s = metrics.alcubierre()
        parts = st.integrate_parts(st.energy_density(), 0.0, [(-4, 4)] * 3, 40, {s["v"]: 1.0}, {s["f"]: GAUSS})
        self.assertAlmostEqual(parts["positive"], 0.0, places=12)
        self.assertAlmostEqual(parts["total"], parts["negative"], places=12)
        mk, m = metrics.minkowski()
        mixed = mk.integrate_parts(m["x"], 0.0, [(-1, 1)] * 3, 20)
        self.assertAlmostEqual(mixed["total"], 0.0, places=12)
        self.assertAlmostEqual(mixed["positive"], -mixed["negative"], places=12)
        self.assertGreater(mixed["positive"], 0.0)

    def test_nan_points_are_dropped_and_reported(self):
        mk, m = metrics.minkowski()
        x, y, z = m["x"], m["y"], m["z"]
        density = 1 / sp.sqrt(x**2 + y**2 + z**2)
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            parts = mk.integrate_parts(density, 0.0, [(-1.5, 1.5)] * 3, 3)  # odd n puts a point at 0
        self.assertEqual(parts["nan_points"], 1)
        self.assertTrue(any("NaN" in str(w.message) for w in caught))
        self.assertTrue(math.isfinite(parts["total"]))

    def test_precision_check_flags_cancellation(self):
        mk, m = metrics.minkowski()
        expr = sp.sqrt(1 + sp.Float("1e-20") * m["x"] ** 2) - 1
        report = mk.precision_check(expr, [(0.0, 1.0, 0.0, 0.0)])
        self.assertGreater(report["max_rel_error"], 0.5)
        hp = report["values"][0][2]
        self.assertAlmostEqual(hp / 5e-21, 1.0, places=6)


class Helpers(unittest.TestCase):
    def test_lorentzian_average(self):
        self.assertAlmostEqual(qi.lorentzian_average(lambda t: np.full_like(t, 2.5), 1.0), 2.5, places=12)
        # int (1/(1+t^2)) (1/pi)/(1+t^2) dt = 1/2
        self.assertAlmostEqual(qi.lorentzian_average(lambda t: 1 / (1 + t**2), 1.0), 0.5, places=6)

    def test_ford_roman_units_agree(self):
        tau = 1e-15
        si = qi.ford_roman_si(tau)
        geo = qi.ford_roman_geometric(C * tau)
        self.assertAlmostEqual(to_si.energy_density_j_per_m3(geo) / si, 1.0, places=9)

    def test_solar_mass_hawking_temperature(self):
        m_geo = G_NEWTON * M_SUN / C**2
        self.assertAlmostEqual(to_si.hawking_temperature_k(1 / (4 * m_geo)) / 6.17e-8, 1.0, places=2)

    def test_horizon_finder_on_a_superluminal_profile(self):
        v = 2.0
        u = lambda xi: -v * (1 - np.exp(-(xi**2)))  # noqa: E731
        hz = horizons_1p1(u, np.linspace(-3, 3, 3001))
        self.assertEqual(len(hz), 2)  # front and back walls
        xh = math.sqrt(-math.log(1 - 1 / v))
        self.assertAlmostEqual(abs(hz[0]["x"]), xh, places=8)
        self.assertAlmostEqual(hz[0]["kappa"], 2 * v * xh * math.exp(-xh**2), places=5)


class Units(unittest.TestCase):
    def test_si_conversions(self):
        self.assertAlmostEqual(to_si.energy_joules(1.0), C**4 / G_NEWTON)
        self.assertAlmostEqual(to_si.mass_kg(1.0) / 1.3466e27, 1.0, places=3)  # c^2/G in kg/m
        self.assertAlmostEqual(to_si.energy_density_j_per_m3(2.0), 2 * C**4 / G_NEWTON)
        self.assertTrue(math.isclose(to_si.energy_joules(1.0), to_si.mass_kg(1.0) * C**2))


if __name__ == "__main__":
    unittest.main()
