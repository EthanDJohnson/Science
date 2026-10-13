"""Tests for qft_spinor_born.py: every public function states its quantity and validity, out-of-range inputs
are refused, and the command line takes SI units. (The full physics self-test runs in test_calculators.py.)

Run from the project root:
    python3 -m unittest discover -s .claude/skills/conundrum/scripts/tests -p "test_qft_spinor_born.py" -v
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

import qft_spinor_born as sb  # noqa: E402


def public_functions():
    return [(name, fn) for name, fn in inspect.getmembers(sb, inspect.isfunction)
            if not name.startswith("_") and fn.__module__ == sb.__name__ and name not in ("main", "selftest")]


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
        self.assertIn("hbar = c = 1", sb.__doc__)
        self.assertIn("Heaviside-Lorentz", sb.__doc__)

    def test_module_docstring_has_required_sections(self):
        for section in ("Units (read this first)", "Conventions", "Assumptions and validity range", "Python usage",
                        "Command line"):
            with self.subTest(section=section):
                self.assertIn(section, sb.__doc__)
        for formula in ("beta (1 + 2 m^2/s)/(6 pi)", "rhoV = beta^3/(24 pi)", "rho0 = m^2 s beta^3/(36 pi)"):
            with self.subTest(formula=formula):
                self.assertIn(formula, sb.__doc__)


class SpectralDensities(unittest.TestCase):
    def test_refusals(self):
        bad = [
            lambda: sb.vector_spectral_density([4.0], -1.0),                 # negative mass
            lambda: sb.vector_spectral_density([4.0], 1.0, "majorana"),      # unknown field
            lambda: sb.im_vacuum_polarization([9.0], 1.0, alpha=0.0),        # no coupling
            lambda: sb.dirac_stress_spectral_densities([4.0], 0.5, "weyl"),  # massive Weyl
            lambda: sb.dirac_stress_spectral_densities([4.0], 0.0, "photon"),
            lambda: sb.em_weight(1.0, 0.0, 0.0, 0.0, np.ones(3)),            # potential needs 4 components
        ]
        for i, fn in enumerate(bad):
            with self.subTest(case=i), self.assertRaises(ValueError):
                fn()

    def test_below_threshold_is_zero_and_weyl_is_half_dirac(self):
        self.assertEqual(float(sb.vector_spectral_density([3.9], 1.0)[0]), 0.0)
        r2d, _ = sb.dirac_stress_spectral_densities([7.0])
        r2w, r0w = sb.dirac_stress_spectral_densities([7.0], 0.0, "weyl")
        self.assertAlmostEqual(float(r2w[0] / r2d[0]), 0.5, places=14)
        self.assertEqual(float(r0w[0]), 0.0)

    def test_em_weight_is_lorentz_invariant(self):
        rng = np.random.default_rng(3)
        A = rng.normal(size=4) + 1j * rng.normal(size=4)
        K = np.array([3.0, 0.4, -0.7, 1.1])
        y = 0.9
        L = np.eye(4)
        L[0, 0] = L[3, 3] = math.cosh(y)
        L[0, 3] = L[3, 0] = math.sinh(y)
        Kb = L @ K
        Ab = np.linalg.inv(L).T @ A          # lower-index vectors transform with the inverse transpose
        self.assertAlmostEqual(float(sb.em_weight(*K, A)), float(sb.em_weight(*Kb, Ab)), places=10)


class BornRefusals(unittest.TestCase):
    def test_qed_refusals(self):
        sech2 = lambda t: 0.05 / np.cosh(t) ** 2                          # noqa: E731
        A = lambda K0, Kz: np.zeros(np.shape(K0) + (4,))                  # noqa: E731
        bad = [
            lambda: sb.born_qed_homogeneous(sech2, -2.0, 2.0, 1.0, 30.0),             # field still on at the window ends
            lambda: sb.born_qed_homogeneous(sech2, -20.0, 20.0, 0.0, 30.0),           # massless: non-perturbative at small k
            lambda: sb.born_qed_homogeneous(sech2, -20.0, 20.0, 1.0, 1.5),            # omega_max below 2m
            lambda: sb.born_qed_homogeneous(lambda t: 0.0 * t, -5.0, 5.0, 1.0, 30.0),  # no field at all
            lambda: sb.born_qed_homogeneous(lambda t: 0.4 / np.cosh(t) ** 2, -20.0, 20.0, 1.0, 30.0),  # estimate 1.8
            lambda: sb.sauter_born_pairs_per_volume(1.0, 0.4, 1.0),                  # R2 = 2 eE0 tau^2 = 0.8
            lambda: sb.sauter_exact_pairs_per_volume(1.0, 20.0, 1.0),                # grid would not resolve n_k
            lambda: sb.born_mode_efield([0.0], [0.0], 1.0, lambda Om: 50.0 + 0 * Om),  # first-order n_k > 0.1
            lambda: sb.born_qed_planar(A, 1.0, 3.0, 4.0),                            # s_max below threshold
            lambda: sb.born_qed_general(lambda *K: np.zeros(np.shape(K[0]) + (4,)), 1.0, 10.0, -1.0),
            lambda: sb.born_qed_general(lambda *K: np.zeros(np.shape(K[0]) + (4,)), 1.0, 10.0, 1.0, n_s=1),  # grid
            lambda: sb.born_qed_planar(A, 1.0, 10.0, 4.0, n_y=8.5),                    # non-integer grid
            lambda: sb.sauter_born_pairs_per_volume(1.0, 0.05, 1.0, n=1),            # grid too small
            lambda: sb.born_qed_homogeneous(sech2, -20.0, 20.0, 1.0, 30.0, n_omega=20.5),   # non-integer grid
            lambda: sb.born_qed_homogeneous(sech2, -np.inf, 20.0, 1.0, 30.0),       # infinite window
            lambda: sb.born_mode_efield([0.1], [0.1], 1.0, lambda Om: np.nan * Om),  # non-finite transform
            lambda: sb.born_mode_efield([0.05], [0.1], 1.0, lambda Om: 0.01 + 0 * Om, "scalar", eA_max=0.02),  # k_par small
        ]
        for i, fn in enumerate(bad):
            with self.subTest(case=i), self.assertRaises(ValueError):
                fn()

    def test_multiphoton_trap_is_refused_but_check_false_reports_the_estimate(self):
        g = lambda t: 0.02 * np.exp(-t * t / 8.0)                         # Gaussian E, m tau = 2       # noqa: E731
        with self.assertRaises(ValueError):
            sb.born_qed_homogeneous(g, -28.0, 28.0, 1.0, 30.0)
        r = sb.born_qed_homogeneous(g, -28.0, 28.0, 1.0, 30.0, check=False)
        self.assertGreater(r["R2"], 1.0)
        self.assertGreater(r["error_estimate"], 0.5)
        self.assertGreater(r["pairs_per_volume"], 0.0)

    def test_noise_limited_transform_is_refused(self):
        # Gaussian eE0 exp(-t^2/2T^2), m T = 5, window +-7T (ends 2e-11 of peak, so the ends check passes): the true
        # |eE~(2m)| ~ exp(-50) of int|eE| is below the transform's roundoff and the window-edge step; the numerical
        # yield was 3.3e-34 against the analytic 6.4e-57, with error_estimate 3e-5. It must be refused.
        g = lambda t: 1e-5 * np.exp(-t * t / 50.0)                        # noqa: E731
        with self.assertRaisesRegex(ValueError, "noise floor"):
            sb.born_qed_homogeneous(g, -35.0, 35.0, 1.0, 30.0)
        r = sb.born_qed_homogeneous(g, -35.0, 35.0, 1.0, 30.0, check=False)
        self.assertGreater(r["noise_error"], 1.0)

    def test_truncated_spectrum_and_coarse_grid_are_refused(self):
        sauter = lambda t: 0.05 / np.cosh(t / 0.2) ** 2                   # noqa: E731
        with self.assertRaisesRegex(ValueError, "omega_max"):              # yield 42x too small at omega_max = 2.2
            sb.born_qed_homogeneous(sauter, -10.0, 10.0, 1.0, 2.2)
        r = sb.born_qed_homogeneous(sauter, -10.0, 10.0, 1.0, 40.0)
        self.assertAlmostEqual(r["pairs_per_volume"] / sb.sauter_born_pairs_per_volume(1.0, 0.05, 0.2), 1.0, places=8)
        for key in ("noise_error", "tail_fraction", "grid_error"):
            self.assertLess(r[key], 1e-6)
        line = lambda t: 0.01 * np.exp(-t * t / 1800.0) * np.cos(3 * t)   # narrow line: n_omega = 200 is 0.4% off
        with self.assertRaisesRegex(ValueError, "n_omega"):
            sb.born_qed_homogeneous(line, -240.0, 240.0, 1.0, 10.0)

    def test_long_window_is_refused_not_oom(self):
        g = lambda t: 1e-3 * np.exp(-t * t / 8e6) * np.cos(3 * t)         # T = 2000: was OOM-killed  # noqa: E731
        with self.assertRaisesRegex(ValueError, "too large"):
            sb.born_qed_homogeneous(g, -16000.0, 16000.0, 1.0, 10.0)

    def test_sauter_R2_matches_its_closed_form(self):
        # R2 = 2 eE0 tau^2 for sech^2 (the dA^2 and E transforms share their poles); T_rms = pi tau/sqrt(12)
        r = sb.born_qed_homogeneous(lambda t: 0.05 / np.cosh(t / 1.5) ** 2, -30.0, 30.0, 1.0, 30.0)
        self.assertAlmostEqual(r["R2"] / (2 * 0.05 * 1.5 ** 2), 1.0, places=3)
        self.assertAlmostEqual(r["T_rms"] / (math.pi * 1.5 / math.sqrt(12.0)), 1.0, places=4)

    def test_gravity_and_frw_refusals(self):
        h = lambda t: np.zeros(len(t))                                     # noqa: E731

        def htt(a):
            return lambda t: a * np.exp(-np.asarray(t)[:, None, None] ** 2) * np.diag([0.0, 1.0, -1.0, 0.0])
        bad = [
            lambda: sb.born_dirac_metric_homogeneous(h, -1.0, 1.0, 5.0),               # h not 4x4
            lambda: sb.born_dirac_metric_homogeneous(lambda t: np.zeros((len(t), 4, 4)), -1.0, 1.0, 1.0, 1.0),  # omega_max < 2m
            lambda: sb.born_dirac_metric_planar(lambda K0, Kz: np.zeros(np.shape(K0) + (4, 4)), 10.0, 4.0, 0.5, "weyl"),
            lambda: sb.frw_dirac_tanh_n([0.5], 1.0, 0.2, 0.3, 0.8),                  # a(eta) < 0 somewhere
            lambda: sb.frw_dirac_tanh_n([0.0], 1.0, 1.3, 0.3, 0.8),                  # k = 0
            lambda: sb.frw_dirac_production([0.5], lambda e: 1.0 + 0.1 * e, 1.0, -5.0, 5.0),   # still expanding
            lambda: sb.frw_dirac_production([0.5], lambda e: -1.0, 1.0, -5.0, 5.0),            # a < 0
            lambda: sb.born_dirac_metric_homogeneous(htt(0.1), -0.3, 0.3, 30.0),     # window cut: was 1400x too large
            lambda: sb.born_dirac_metric_homogeneous(htt(100.0), -8.0, 8.0, 30.0),   # |h| = 100: not first order
            lambda: sb.born_dirac_metric_homogeneous(htt(0.1), -np.inf, 8.0, 30.0),  # infinite window
            lambda: sb.born_dirac_metric_homogeneous(htt(0.1), -8.0, 8.0, 30.0, n_omega=8),
            lambda: sb.born_dirac_metric_general(lambda *K: np.zeros(np.shape(K[0]) + (4, 4)), 10.0, 2.0, n_k=2),
        ]
        for i, fn in enumerate(bad):
            with self.subTest(case=i), self.assertRaises(ValueError):
                fn()

    def test_metric_homogeneous_reports_h_max_and_check_false(self):
        h = lambda t: 0.2 * np.exp(-np.asarray(t)[:, None, None] ** 2) * np.diag([0.0, 1.0, -1.0, 0.0])   # noqa: E731
        r = sb.born_dirac_metric_homogeneous(h, -8.0, 8.0, 30.0, check=False)
        self.assertAlmostEqual(r["h_max"], 0.2, places=6)        # max over the time quadrature nodes
        r2 = sb.born_dirac_metric_homogeneous(lambda t: 0.5 * h(t), -8.0, 8.0, 30.0)
        self.assertAlmostEqual(r["pairs_per_volume"] / r2["pairs_per_volume"], 4.0, places=9)
        self.assertLess(r2["noise_error"], 1e-6)

    def test_particles_are_twice_pairs_and_yield_scales_exactly_as_E0_squared(self):
        r = sb.born_qed_homogeneous(lambda t: 0.05 / np.cosh(t) ** 2, -20.0, 20.0, 1.0, 30.0)
        r2 = sb.born_qed_homogeneous(lambda t: 0.025 / np.cosh(t) ** 2, -20.0, 20.0, 1.0, 30.0)
        self.assertAlmostEqual(r["particles_per_volume"], 2 * r["pairs_per_volume"], places=20)
        self.assertAlmostEqual(r["pairs_per_volume"] / r2["pairs_per_volume"], 4.0, places=9)   # O(E^2) exactly


class CommandLine(unittest.TestCase):
    def run_cli(self, args):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = sb.main(args)
        return code, buf.getvalue()

    def test_sauter_cli_si_units(self):
        code, out = self.run_cli(["sauter", "--E", "1e16 V/m", "--tau", "1e-21 s"])
        self.assertEqual(code, 0)
        self.assertIn("pairs per m^3", out)
        self.assertIn("exact/Born", out)

    def test_bad_units_return_1(self):
        self.assertEqual(self.run_cli(["sauter", "--E", "3 J", "--tau", "1e-21 s"])[0], 1)
        self.assertEqual(self.run_cli(["sauter", "--E", "1e16 V/m", "--tau", "2 m"])[0], 1)
        self.assertEqual(self.run_cli(["spectral", "--sqrts", "1.5 kg", "--m", "0.511 MeV"])[0], 1)

    def test_spectral_and_frw_cli(self):
        code, out = self.run_cli(["spectral", "--sqrts", "1.5 MeV", "--m", "0.511 MeV"])
        self.assertEqual(code, 0)
        self.assertIn("Im Pi", out)
        code, out = self.run_cli(["frw", "--m", "1", "--A", "1.3", "--B", "0.3", "--rho", "0.8", "--k", "0.5"])
        self.assertEqual(code, 0)
        self.assertIn("closed form", out)


if __name__ == "__main__":
    unittest.main()
