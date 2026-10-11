"""Tests for qft_plane_wave.py: every public function states its quantity and validity, out-of-range inputs
are refused, and the command line takes SI units. (The full physics self-test runs in test_calculators.py.)

Run from the project root:
    python3 -m unittest discover -s .claude/skills/conundrum/scripts/tests -p "test_qft_plane_wave.py" -v
"""
import contextlib
import inspect
import io
import math
import re
import sys
import unittest
from pathlib import Path

import numpy as np

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

import qft_plane_wave as pw  # noqa: E402
import qft_production as qp  # noqa: E402


def public_functions():
    return [(name, fn) for name, fn in inspect.getmembers(pw, inspect.isfunction)
            if not name.startswith("_") and fn.__module__ == pw.__name__ and name not in ("main", "selftest")]


def plus(prof):
    return lambda U: np.multiply.outer(prof(np.asarray(U, dtype=float)), np.diag([1.0, -1.0]))


SQUARE = plus(lambda U: 0.25 * ((U >= -1.0) & (U <= 1.0)))      # A0 = 0.5, a = 1
IDENTITY = lambda U: np.multiply.outer(1.0 * ((np.asarray(U, float) >= -1) & (np.asarray(U, float) <= 1)), np.eye(2))  # noqa: E731
CROSS = lambda U: np.multiply.outer(0.0025 * ((np.asarray(U, float) >= -1) & (np.asarray(U, float) <= 1)),  # noqa: E731
                                    np.array([[0.0, 1.0], [1.0, 0.0]]))
L_BOX = 16 * math.pi


class Docstrings(unittest.TestCase):
    def test_every_public_function_states_quantity_and_validity(self):
        funcs = public_functions()
        self.assertGreater(len(funcs), 10)
        for name, fn in funcs:
            doc = inspect.getdoc(fn) or ""
            with self.subTest(function=name):
                self.assertRegex(doc, r"(?m)^Quantity: \S", f"{name} lacks a 'Quantity:' line")
                self.assertRegex(doc, r"(?m)^Valid when: \S", f"{name} lacks a 'Valid when:' line")

    def test_module_docstring_states_units(self):
        self.assertIn("hbar = c = 1", pw.__doc__)
        self.assertIn("Heaviside-Lorentz", pw.__doc__)

    def test_module_docstring_has_required_sections(self):
        for header in ("Units (read this first)", "Assumptions and validity range", "Python usage",
                       "Command line (from the project root)"):
            with self.subTest(section=header):
                self.assertRegex(pw.__doc__, r"(?m)^" + re.escape(header) + r"\s*$")
        for formula in ("Tr beta^dag beta", "alpha alpha^dag - beta beta^dag = 1", "e^{-icV}", "omega_k^2 = k^2 + m^2"):
            with self.subTest(formula=formula):
                self.assertIn(formula, pw.__doc__)

    def test_import_adds_no_cwd_relative_path_and_runs_nothing(self):
        # importing must not depend on the working directory, and must only define things (no computation, no
        # output): re-import in a fresh interpreter from another directory and check stdout and sys.path
        import subprocess
        # (qft_production, imported first, may add its own entries: only qft_plane_wave's are checked here)
        code = ("import sys, os; sys.path.insert(0, %r); import qft_production, unit_tools; "
                "sys.path[:] = [p for p in sys.path if os.path.isabs(p) or not p]; "
                "import qft_plane_wave as pw; "
                "print([p for p in sys.path if p and not os.path.isabs(p)]); "
                "print(len(pw._BM_A))") % str(SCRIPTS)
        out = subprocess.run([sys.executable, "-c", code], cwd="/", capture_output=True, text=True, timeout=60)
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertEqual(out.stdout.split(), ["[]", "7"])
        self.assertAlmostEqual(sum(pw._BM_A), 1.0, places=14)       # S6 is consistent: sum a = sum b = 1
        self.assertAlmostEqual(sum(pw._BM_B), 1.0, places=14)


class LatticeRefusals(unittest.TestCase):
    def test_refusals(self):
        pat = pw.pattern_potential(0.3, 8, 3.0, 6.0, L_BOX, 1.0)
        t0, t1 = pat["window"]
        V = pat["V"]
        bad = [
            lambda: pw.lattice_bogoliubov(V, L_BOX, 35, 1.0, t0, t1),                      # odd N
            lambda: pw.lattice_bogoliubov(V, L_BOX, 6, 1.0, t0, t1),                       # N < 8
            lambda: pw.lattice_bogoliubov(V, -1.0, 36, 1.0, t0, t1),                       # L <= 0
            lambda: pw.lattice_bogoliubov(V, L_BOX, 36, 1.0, t1, t0),                      # reversed window
            lambda: pw.lattice_bogoliubov(V, L_BOX, 36, 1.0, -6.0, 6.0),                   # pattern on at the window ends
            lambda: pw.lattice_bogoliubov(lambda t, z: 0 * z, L_BOX, 36, 0.0, -5.0, 5.0),  # m = 0: omega(k=0) = 0
            lambda: pw.lattice_bogoliubov(lambda t, z: 0.1 * np.exp(-t * t) * (np.abs(z) < 1.0), L_BOX, 36, 1.0,
                                          -9.0, 9.0),                                   # not band-limited
            lambda: pw.lattice_bogoliubov(V, L_BOX, 36, 1.0, t0, t1, steps=1),             # steps < 2
            lambda: pw.lattice_born(V, L_BOX, 36, 0.0, t0, t1),                             # Born needs m > 0
            lambda: pw.lattice_born(lambda t, z: 0.1 + 0 * z, L_BOX, 36, 1.0, -5.0, 5.0),  # V not 0 at the ends
            lambda: pw.lattice_bogoliubov(V, L_BOX, 36, 1.0, t0, t1, check_N=36),         # N-check must use N2 > N
            lambda: pw.lattice_bogoliubov(V, L_BOX, 36, 1.0, t0, t1, check_N=49),         # ... and even N2
        ]
        for i, fn in enumerate(bad):
            with self.subTest(case=i), self.assertRaises(ValueError):
                fn()

    def test_truncated_null_band_is_flagged(self):
        # null pattern, eps = 0.3 m^2, T = 10/m: N = 36 misses the leakage at k ~ 2 m (2e-11 vs 7.4e-7 converged);
        # the N-check must call it unresolved and not zero
        pat = pw.pattern_potential(0.3, 8, 1.0, 10.0, L_BOX, 1.0)
        r = pw.lattice_bogoliubov(pat["V"], L_BOX, 36, 1.0, *pat["window"], rtol=1e-3, steps=256)
        self.assertEqual(r["N_check"], 48)
        self.assertFalse(r["resolved"])
        self.assertFalse(r["consistent_with_zero"])
        self.assertGreater(r["total_N_check"], 100 * r["total"])

    def test_null_band_at_floor_is_not_certified_zero(self):
        # null pattern, eps = 0.3 m^2, T = 40/m: the leakage sits at k ~ 4.5 m, so N = 36 and N = 48 both read
        # roundoff (2.3e-26, 2.8e-26), while N = 72 gives 2.1e-18 and the converged yield is 3.0e-13 (N = 144; an
        # independent k-space ODE solver reported 3.04e-13). One 4N/3 rerun must not certify a zero: the N-check
        # escalates to 2N = 72, which leaves the floor.
        pat = pw.pattern_potential(0.3, 8, 1.0, 40.0, L_BOX, 1.0)
        r = pw.lattice_bogoliubov(pat["V"], L_BOX, 36, 1.0, *pat["window"], steps=256, rtol=1e-4)
        self.assertFalse(r["consistent_with_zero"])
        self.assertFalse(r["resolved"])
        self.assertEqual([n for n, _, _ in r["N_ladder"]], [48, 72])
        self.assertEqual(r["N_check"], 72)
        self.assertGreater(r["total_N_check"], 1e3 * r["total_floor"])

    def test_pattern_refusals_and_kinds(self):
        bad = [
            lambda: pw.pattern_potential(0.3, 2.5, 1.0, 6.0, L_BOX, 1.0),     # q not a box harmonic
            lambda: pw.pattern_potential(1.2, 8, 0.5, 6.0, L_BOX, 1.0),       # subluminal with m^2 + V < 0 somewhere
            lambda: pw.pattern_potential(0.3, 0, 0.0, 6.0, L_BOX, 1.0),       # homogeneous needs omega
            lambda: pw.pattern_potential(0.3, 8, 1.0, -6.0, L_BOX, 1.0),      # T <= 0
            lambda: pw.pattern_potential(0.3, 8, 1.0, 6.0, L_BOX, 1.0, ends=5.0),   # Gaussian not off at the ends
        ]
        for i, fn in enumerate(bad):
            with self.subTest(case=i), self.assertRaises(ValueError):
                fn()
        kinds = {v: pw.pattern_potential(0.3, 8, v, 6.0, L_BOX, 1.0)["kind"] for v in (0.5, 1.0, 3.0)}
        self.assertEqual(kinds, {0.5: "subluminal", 1.0: "null", 3.0: "superluminal"})
        self.assertEqual(pw.pattern_potential(0.3, 8, 1.0, 6.0, L_BOX, 1.0)["s"], 0.0)     # null: K^2 = 0 exactly


class BornRefusalsAndIdentity(unittest.TestCase):
    def test_refusals(self):
        Vt = lambda K0, Kz: np.exp(-(K0 - 3) ** 2 - (Kz - 1) ** 2)     # noqa: E731
        bad = [
            lambda: pw.pair_spectral_density_1p1([5.0], 0.0),           # massless 1+1: collinear singular
            lambda: pw.born_pairs_1p1(Vt, 1.0, 4.0, 2.0),              # s_max below threshold
            lambda: pw.born_pairs_1p1(Vt, 0.0, 20.0, 2.0),             # m = 0
            lambda: pw.born_pairs_1p1(Vt, 1.0, 20.0, -1.0),            # y_max <= 0
        ]
        for i, fn in enumerate(bad):
            with self.subTest(case=i), self.assertRaises(ValueError):
                fn()

    def test_1p1_density_is_minus_4pi_mass_derivative_of_3p1(self):
        # rho_1+1(s; m^2) = -4 pi d/dm^2 [beta/(16 pi)] (integrating the 1+1 density over transverse momenta)
        s, m2, d = np.array([5.0, 9.0, 40.0]), 1.0, 1e-5
        r3 = lambda mm2: qp.pair_spectral_density_scalar(s, math.sqrt(mm2))     # noqa: E731
        deriv = (r3(m2 + d) - r3(m2 - d)) / (2 * d)
        np.testing.assert_allclose(pw.pair_spectral_density_1p1(s, 1.0), -4 * math.pi * deriv, rtol=1e-8)
        self.assertEqual(float(pw.pair_spectral_density_1p1([3.9], 1.0)[0]), 0.0)                # below threshold


class GibbonsRefusals(unittest.TestCase):
    def test_refusals(self):
        k = np.array([0.3, 0.1])
        bad = [
            lambda: pw.gibbons_jacobi(SQUARE, -2.0, [-3.0], breaks=(-1, 1)),                     # U < U_a
            lambda: pw.gibbons_jacobi(SQUARE, 0.0, [1.5], breaks=(-1, 1)),                       # U_a inside the wave
            lambda: pw.gibbons_jacobi(SQUARE, -2.0, [4.0], breaks=(-1, 1)),                      # beyond the caustic
            lambda: pw.gibbons_jacobi(lambda U: np.multiply.outer(np.ones_like(np.asarray(U, float)),
                                                                  np.array([[0.0, 1.0], [0.0, 0.0]])), -1.0, [0.0]),  # H not symmetric
            lambda: pw.gibbons_mode(0.0, 0.0, 0.1, 0.2, k, -1.0, 1.0, SQUARE, -2.0, (-1, 1)),    # c < 0
            lambda: pw.gibbons_mode(0.0, 0.0, 0.1, 0.2, [1.0, 2.0, 3.0], 1.0, 1.0, SQUARE, -2.0, (-1, 1)),   # k not 2D
            lambda: pw.gibbons_packet(SQUARE, -1.25, 1.25, 1.0, 1.0, [0.5, 0.3], 1.0, breaks=(-1, 1), n_grid=16),  # too coarse
            lambda: pw.gibbons_packet(SQUARE, -1.25, 1.25, 0.0, 1.0, [0.5, 0.3], 1.0, breaks=(-1, 1)),      # c = 0
            lambda: pw.square_pulse_geodesic(0.5, 0.0, [0.0], [1.0, 0.0]),                       # a <= 0
            lambda: pw.velocity_memory(SQUARE, [1.0], -2.0, 2.0, breaks=(-1, 1)),                # X0 not 2D
            lambda: pw.kg_residual_brinkmann(lambda *a: a[0], SQUARE, 0.0, 0.0, 0.0, 0.0, 1.0, d=0.0),  # d <= 0
            lambda: pw.gibbons_mode(0.9, 0.0, 0.1, 0.2, k, 1.0, 1.0, IDENTITY, -2.0, (-1, 1)),   # past a DOUBLE caustic
            lambda: pw.gibbons_packet(IDENTITY, -2.0, 1.0, 1.0, 1.0, [0.5, 0.3], 1.0, breaks=(-1, 1)),  # same
            lambda: pw.gibbons_jacobi(SQUARE, -2.0, [1.5], breaks=(-1, 1), min_scale=1e-6),       # needs > max_steps
            lambda: pw.gibbons_packet_spacelike(SQUARE, -1.0, 1.0, 1.0, 0.5, 1.0, [1.0, 1.0], 2.0),   # c0 - 5 sigma_c < 0
            lambda: pw.gibbons_packet_spacelike(SQUARE, -0.5, 1.0, 6.0, 1.0, 1.0, [1.0, 1.0], 2.0),   # H != 0 before U1
            lambda: pw.gibbons_packet_spacelike(CROSS, -1.0, 1.0, 6.0, 1.0, 1.0, [1.0, 1.0], 2.0),    # not diagonal
        ]
        for i, fn in enumerate(bad):
            with self.subTest(case=i), self.assertRaises(ValueError):
                fn()

    def test_narrow_pulse_first_order_memory(self):
        # width 1e-3 (fixed quadrature panels of 0.25 used to return -5e-5): Simpson on the adaptive RK4 grid
        Hn = plus(lambda U: 0.1 / 1e-3 * np.exp(-0.5 * ((U - 0.0123) / 1e-3) ** 2))
        vm = pw.velocity_memory(Hn, [1.0, 0.0], -2.0, 2.0)
        self.assertAlmostEqual(vm["velocity_first_order"][0] / (-0.1 * math.sqrt(2 * math.pi)), 1.0, places=8)
        self.assertAlmostEqual(vm["velocity"][0], -0.2506, places=3)        # weak: exact ~ first order

    def test_double_caustic_is_found(self):
        jac = pw.gibbons_jacobi(IDENTITY, -2.0, [1.0], breaks=(-1, 1), allow_caustic=True)
        self.assertAlmostEqual(jac["first_caustic"], math.pi / 2 - 1, delta=1e-3)     # det P = cos^2(U + 1) >= 0

    def test_classical_memory_allows_caustics(self):
        # geodesics cross caustics: velocity_memory works past the first zero of det P where modes are refused
        vm = pw.velocity_memory(SQUARE, [0.5, 0.3], -2.0, 4.0, breaks=(-1, 1))
        ck = pw.square_pulse_geodesic(0.5, 1.0, [4.0], [0.5, 0.3])
        np.testing.assert_allclose(vm["velocity"], ck["dX_dU"][0], atol=1e-11)

    def test_mode_is_plane_wave_before_the_wave(self):
        k, c, m = np.array([0.4, -0.2]), 0.8, 1.0
        U, V, x, y = -1.5, 0.3, 0.7, -0.4
        phi = pw.gibbons_mode(U, V, x, y, k, c, m, SQUARE, -2.0, (-1, 1))
        ref = np.exp(1j * (k[0] * x + k[1] * y - c * V - (k @ k + m * m) * (U + 2.0) / (4 * c)))
        self.assertAlmostEqual(abs(phi - ref), 0.0, places=12)


class CommandLine(unittest.TestCase):
    def run_cli(self, argv):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = pw.main(argv)
        return code, buf.getvalue()

    def test_pattern_cli_si_units(self):
        # m = 0.511 MeV, T = 7.7e-21 s = 6.0/m, L = 1.94e-11 m = 16 pi/m: superluminal v = 2.5 (resolved at N = 36)
        code, out = self.run_cli(["pattern", "--m", "0.511 MeV", "--eps", "0.3", "--nq", "8", "--v", "2.5",
                                  "--T", "7.73e-21 s", "--L", "1.94e-11 m"])
        self.assertEqual(code, 0, out)
        self.assertIn("superluminal pattern", out)
        self.assertIn("Tr beta^dag beta", out)
        self.assertIn("resolved = True", out)
        self.assertIn("N-check: N = 48", out)

    def test_pattern_cli_flags_truncated_null_band(self):
        code, out = self.run_cli(["pattern", "--eps", "0.3", "--nq", "8", "--v", "1", "--T", "10", "--L", "50.265"])
        self.assertEqual(code, 0, out)
        self.assertIn("NOT converged in the number of modes", out)
        self.assertNotIn("zero to the floor", out)

    def test_pattern_cli_null_never_says_zero(self):
        # the T = 40/m null case that a single 4N/3 rerun used to certify as 'zero to the floor'
        code, out = self.run_cli(["pattern", "--eps", "0.3", "--nq", "8", "--v", "1", "--T", "40", "--L", "50.265",
                                  "--N", "36"])
        self.assertEqual(code, 0, out)
        self.assertNotIn("zero to the floor", out)
        self.assertIn("N = 72 gives", out)
        self.assertIn("NOT converged in the number of modes", out)

    def test_pattern_cli_refuses_bare_m_with_si_times(self):
        code, out = self.run_cli(["pattern", "--m", "2", "--eps", "0.3", "--nq", "8", "--v", "1",
                                  "--T", "2.9e-20 s", "--L", "1.94e-11 m"])
        self.assertEqual(code, 1)
        self.assertIn("bare number", out)
        code, out = self.run_cli(["pattern", "--m", "nan", "--eps", "0.3", "--nq", "8", "--v", "1", "--T", "6", "--L", "50"])
        self.assertEqual(code, 1)
        self.assertIn("m must be finite", out)

    def test_bad_unit_returns_1(self):
        code, out = self.run_cli(["pattern", "--m", "0.511 MeV", "--eps", "0.3", "--nq", "8", "--v", "1",
                                  "--T", "3 kg", "--L", "1.94e-11 m"])
        self.assertEqual(code, 1)
        self.assertIn("ERROR", out)
        code, _ = self.run_cli(["pattern", "--eps", "0.3", "--nq", "8", "--v", "1", "--T", "6", "--L", "3 furlongs"])
        self.assertEqual(code, 1)

    def test_gibbons_cli(self):
        code, out = self.run_cli(["gibbons", "--A0", "0.5", "--a", "1"])
        self.assertEqual(code, 0)
        self.assertIn("negative-frequency weight", out)


if __name__ == "__main__":
    unittest.main()
