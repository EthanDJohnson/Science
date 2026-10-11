"""Tests for qft_curved_frw.py: every public function states its quantity and validity, out-of-range inputs
are refused, the bookkeeping (particles vs pairs, whole universe vs per volume) is right, and the command line
takes SI units. (The full physics self-test runs in test_calculators.py.)

Run from the project root:
    python3 -m unittest discover -s .claude/skills/conundrum/scripts/tests -p "test_qft_curved_frw.py" -v
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

import qft_curved_frw as cf  # noqa: E402
import qft_production as qp  # noqa: E402


def public_functions():
    return [(name, fn) for name, fn in inspect.getmembers(cf, inspect.isfunction)
            if not name.startswith("_") and fn.__module__ == cf.__name__ and name not in ("main", "selftest")]


def static_a(eta):
    return 1.5


class Docstrings(unittest.TestCase):
    def test_every_public_function_states_quantity_and_validity(self):
        funcs = public_functions()
        self.assertGreater(len(funcs), 12)
        for name, fn in funcs:
            doc = inspect.getdoc(fn) or ""
            with self.subTest(function=name):
                self.assertRegex(doc, r"(?m)^Quantity: \S", f"{name} lacks a 'Quantity:' line")
                self.assertRegex(doc, r"(?m)^Valid when: \S", f"{name} lacks a 'Valid when:' line")

    def test_module_docstring_states_units(self):
        self.assertIn("hbar = c = 1", cf.__doc__)
        self.assertIn("Heaviside-Lorentz", cf.__doc__)


class Refusals(unittest.TestCase):
    def test_spectrum_and_geometry_refusals(self):
        bad = [
            lambda: cf.spatial_eigenvalue(2, [1.0]),                 # K not in {+1, 0, -1}
            lambda: cf.spatial_eigenvalue(True, [1.0]),              # a bool is not a curvature sign
            lambda: cf.spatial_eigenvalue(1, [0]),                   # closed levels start at n = 1
            lambda: cf.spatial_eigenvalue(1, [1.5]),                 # closed levels are integers
            lambda: cf.spatial_eigenvalue(-1, [-0.1]),               # open k >= 0
            lambda: cf.spatial_eigenvalue(1, [1], L=0.0),            # L > 0
            lambda: cf.closed_comoving_volume(-1.0),
            lambda: cf.closed_mode_count(0),
            lambda: cf.weyl_mode_count(-1.0, 1.0),
            lambda: cf.ricci_scalar(-1.0, 0.0, 1),                  # a <= 0
            lambda: cf.open_spectral_density([-1.0]),
        ]
        for i, fn in enumerate(bad):
            with self.subTest(case=i), self.assertRaises(ValueError):
                fn()

    def test_mode_refusals(self):
        bad = [
            lambda: cf.curved_frw_omega2(1, [1], static_a, -1.0, 0.0),                    # m < 0
            lambda: cf.curved_frw_omega2(1, [1], static_a, 1.0, float("nan")),            # xi not finite
            lambda: cf.curved_frw_omega2(1, [1], lambda e: -1.0, 1.0, 0.0)(0.0),          # a <= 0
            # massless minimally coupled closed n = 1 is a zero mode (omega = 0): no particle interpretation
            lambda: cf.curved_frw_particle_production(1, [1], static_a, 0.0, 0.0, -5.0, 5.0, a_pp=lambda e: 0.0),
            # still expanding at the window ends: no static out region
            lambda: cf.curved_frw_particle_production(-1, [0.5], lambda e: 1.0 + 0.1 * e, 1.0, 0.0, -5.0, 5.0),
            lambda: cf.conformal_tanh_beta2(1, [1], 1.0, 1.0, 2.0, 0.5),                  # a^2 < 0 in the past
            lambda: cf.conformal_tanh_beta2(-1, [0.0], 0.0, 2.0, 1.0, 0.5),               # massless k = 0
            lambda: cf.milne_beta2([0.0]),
            lambda: cf.milne_beta2_finite([0.3], 0.0, 5.0),                               # m = 0
            lambda: cf.milne_beta2_finite([0.3], 1.0, 30.0),                              # m e^eta1 too large
        ]
        for i, fn in enumerate(bad):
            with self.subTest(case=i), self.assertRaises(ValueError):
                fn()

    def test_totals_refusals(self):
        n = np.arange(1, 6, dtype=float)
        a, app, (e0, e1) = qp.frw_tanh_scale_factor(2.0, 1.0, 0.7)
        bad = [
            lambda: cf.closed_universe_totals([1.0, 3.0], [0.1, 0.1]),                    # a level is missing
            lambda: cf.closed_universe_totals(n, np.ones(5)),                             # sum not converged
            lambda: cf.closed_universe_totals(n, -np.ones(5)),                            # negative |beta|^2
            lambda: cf.closed_universe_totals(n, np.exp(-5 * n), field="majorana"),
            lambda: cf.closed_universe_totals(n, np.exp(-5 * n), a_out=0.0),
            lambda: cf.closed_universe_production(0, a, 1.0, 0.0, e0, e1),
            lambda: cf.closed_universe_production(30000, a, 1.0, 0.0, e0, e1),           # use the flat limit instead
            lambda: cf.open_universe_density(2.0, a, 1.0, 0.0, e0, e1, K=1),              # closed is discrete
            lambda: cf.open_universe_density(0.3, a, 1.0, 0.0, e0, e1, a_pp=app, nodes=16),  # spectrum not cut off
        ]
        for i, fn in enumerate(bad):
            with self.subTest(case=i), self.assertRaises(ValueError):
                fn()


class Bookkeeping(unittest.TestCase):
    def test_closed_spectrum(self):
        np.testing.assert_allclose(cf.spatial_eigenvalue(1, [1, 2, 3]), [0.0, 3.0, 8.0])
        np.testing.assert_allclose(cf.spatial_eigenvalue(-1, [0.0, 2.0], L=2.0), [0.25, 4.25])
        np.testing.assert_allclose(cf.closed_degeneracy([1, 2, 3]), [1.0, 4.0, 9.0])
        self.assertEqual(cf.closed_mode_count(3), 14)
        self.assertAlmostEqual(cf.closed_comoving_volume(2.0), 16 * math.pi ** 2)

    def test_particles_pairs_and_volumes(self):
        n = np.arange(1, 41, dtype=float)
        b2 = 1e-3 * np.exp(-n)
        real = cf.closed_universe_totals(n, b2, L=2.0, a_out=3.0)
        cplx = cf.closed_universe_totals(n, b2, L=2.0, field="complex")
        total = float(np.sum(n * n * b2))
        self.assertAlmostEqual(real["particles_total"], total, places=15)
        self.assertAlmostEqual(real["pairs_total"], total / 2, places=15)                 # real field: pairs = particles/2
        self.assertAlmostEqual(cplx["pairs_total"], cplx["particles_total"], places=15)   # complex: pairs = particles
        self.assertAlmostEqual(real["per_comoving_volume"], total / (2 * math.pi ** 2 * 8.0), places=15)
        self.assertAlmostEqual(real["per_physical_volume_out"], total / (2 * math.pi ** 2 * 216.0), places=15)
        # in-out vacuum persistence (real field: product over real modes of 1/|alpha|) vs in-in mean pairs
        self.assertAlmostEqual(real["log_vacuum_persistence"], -0.5 * float(np.sum(n * n * np.log1p(b2))), places=15)
        self.assertLess(-real["log_vacuum_persistence"], real["pairs_total"])
        self.assertAlmostEqual(cplx["log_vacuum_persistence"], 2 * real["log_vacuum_persistence"], places=15)

    def test_conformal_curvature_cancels(self):
        # xi = 1/6: omega^2 = n^2/L^2 + m^2 a^2 on S^3 of radius L, with a'' by finite differences
        w2 = cf.curved_frw_omega2(1, [1, 2, 3], lambda e: 1.0 + 0.2 * math.tanh(e), 0.5, 1 / 6, L=2.0)
        a0 = 1.0 + 0.2 * math.tanh(0.3)
        np.testing.assert_allclose(w2(0.3), np.array([1, 4, 9]) / 4.0 + 0.25 * a0 * a0, rtol=1e-14)


class CommandLine(unittest.TestCase):
    def run_main(self, argv):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = cf.main(argv)
        return code, buf.getvalue()

    def test_tanh_cli_with_SI_units(self):
        code, out = self.run_main(["tanh", "--K", "1", "--m", "1 eV", "--xi", "0.1666666667", "--A", "2", "--B", "1",
                                   "--rho", "0.7 eV", "--L", "1.97e-7 m", "--nmax", "12"])
        self.assertEqual(code, 0, out)
        self.assertIn("total particles in the whole closed universe", out)
        self.assertIn("m^-3", out)
        self.assertIn("conformal closed form", out)

    def test_bad_units_return_1(self):
        code, out = self.run_main(["tanh", "--K", "1", "--m", "3 m", "--xi", "0", "--A", "2", "--B", "1", "--rho", "0.7"])
        self.assertEqual(code, 1)
        self.assertIn("ERROR", out)
        code, _ = self.run_main(["tanh", "--K", "-1", "--m", "1", "--xi", "0", "--A", "2", "--B", "1", "--rho", "0.7",
                                 "--L", "2 kg"])
        self.assertEqual(code, 1)


if __name__ == "__main__":
    unittest.main()
