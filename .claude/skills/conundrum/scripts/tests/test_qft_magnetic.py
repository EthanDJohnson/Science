"""Tests for qft_magnetic.py: every public function states its quantity and validity, out-of-range inputs
are refused, and the command line takes SI units. (The full physics self-test runs in test_calculators.py.)

Run from the project root:
    python3 -m unittest discover -s .claude/skills/conundrum/scripts/tests -p "test_qft_magnetic.py" -v
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

import qft_magnetic as qm  # noqa: E402
import qft_production as qp  # noqa: E402


def public_functions():
    return [(name, fn) for name, fn in inspect.getmembers(qm, inspect.isfunction)
            if not name.startswith("_") and fn.__module__ == qm.__name__ and name not in ("main", "selftest")]


def run_cli(argv):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = qm.main(argv)
    return code, buf.getvalue()


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
        self.assertIn("hbar = c = 1", qm.__doc__)
        self.assertIn("Heaviside-Lorentz", qm.__doc__)

    def test_module_docstring_sections(self):
        for section in ("Units", "Assumptions and validity", "Python usage", "Command line",
                        "qft_magnetic.py parallel", "qft_magnetic.py selftest"):
            with self.subTest(section=section):
                self.assertIn(section, qm.__doc__)


class LandauRefusals(unittest.TestCase):
    def test_refusals(self):
        bad = [
            lambda: qm.landau_eps_perp2(0, 1.0, 0.0, False),                    # no magnetic field
            lambda: qm.landau_eps_perp2(-1, 1.0, 0.5, False),                   # negative level
            lambda: qm.landau_eps_perp2(1.5, 1.0, 0.5, False),                  # non-integer level
            lambda: qm.landau_eps_perp2(0, 1.0, 0.5, True),                     # spinor without a spin label
            lambda: qm.landau_eps_perp2(0, 1.0, 0.5, False, spin=1),            # scalar with a spin label
            lambda: qm.landau_spectrum(1.0, 0.5, True, 0),                      # no levels
            lambda: qm.parallel_n_mode(0, 1.0, 0.0, 0.5, True, spin=1),         # no electric field
            lambda: qm.parallel_n_mode(0, -1.0, 1.0, 0.5, False),               # negative mass
            lambda: qm.parallel_rates_from_modes(1.0, 1.0, 1e-7, True),         # B/E too small for a Landau sum
            lambda: qm.parallel_closed_forms(1e-4, 100.0, 1.0, True),           # series needs > max_terms terms
            lambda: qm.parallel_closed_forms(1.0, 1.0, -0.5, False),            # eB < 0
        ]
        for i, fn in enumerate(bad):
            with self.subTest(case=i), self.assertRaises(ValueError):
                fn()

    def test_lowest_spinor_level_is_spin_nondegenerate(self):
        sp = qm.landau_spectrum(1.0, 0.5, True, 4)
        self.assertEqual(list(sp["channels"]), [1, 2, 2, 2])
        self.assertEqual(sp["spin_content"][0], [(0, +1)])
        self.assertAlmostEqual(qm.landau_eps_perp2(1, 1.0, 0.5, True, spin=-1), qm.landau_eps_perp2(2, 1.0, 0.5, True, spin=+1))

    def test_massless_spinor_pair_rate_finite_decay_rate_infinite(self):
        r = qm.parallel_rates_from_modes(0.0, 1.0, 0.5, True)
        self.assertTrue(math.isfinite(r["pair_rate"]) and r["pair_rate"] > 0)
        self.assertTrue(math.isinf(r["decay_rate"]))


class FieldRefusals(unittest.TestCase):
    def test_refusals(self):
        bad = [
            lambda: qm.field_invariants([1.0, 2.0], [0.0, 0.0, 1.0]),             # not a 3-vector
            lambda: qm.field_invariants([1.0, np.nan, 0.0], [0.0, 0.0, 1.0]),     # not finite
            lambda: qm.boost_fields([1.0, 0, 0], [0, 1.0, 0], [1.0, 0, 0]),       # |v| = 1
            lambda: qm.general_rates([1.0, 0, 0], [0, 0, 1.0], 1.0, True, method="wkb"),
            lambda: qm.general_rates([1.0, 0, 0], [1.0, 0, 0], -1.0, True),        # negative mass
        ]
        for i, fn in enumerate(bad):
            with self.subTest(case=i), self.assertRaises(ValueError):
                fn()

    def test_near_null_field_boost_stays_subluminal(self):
        E = np.array([1.0, 0.0, 0.0])
        B = np.array([0.0, 1.0 - 1e-9, 0.0])           # crossed, |E| just above |B|
        inv = qm.field_invariants(E, B)
        self.assertEqual(inv["kind"], "electric")
        v = inv["boost_velocity"]
        self.assertLess(np.linalg.norm(v), 1.0)
        Ep, Bp = qm.boost_fields(E, B, v)
        self.assertAlmostEqual(np.linalg.norm(Ep) / inv["eps"], 1.0, places=5)
        self.assertLess(np.linalg.norm(Bp) / np.linalg.norm(Ep), 1e-5)

    def test_modes_and_closed_forms_agree_for_a_generic_field(self):
        E, B = [0.3, 0.0, 0.4], [0.0, 0.5, 0.2]
        for fermion in (True, False):
            a = qm.general_rates(E, B, 1.0, fermion, method="closed")
            b = qm.general_rates(E, B, 1.0, fermion, method="modes")
            self.assertAlmostEqual(a["pair_rate"] / b["pair_rate"], 1.0, places=10)
            self.assertAlmostEqual(a["decay_rate"] / b["decay_rate"], 1.0, places=10)

    def test_extreme_field_scales_are_rescaled(self):
        big = qm.field_invariants([1e160, 0, 0], [1e160, 0, 0])            # E.E would overflow
        self.assertEqual(big["kind"], "parallel-frame")
        self.assertAlmostEqual(big["eps"] / 1e160, 1.0, places=12)
        tiny = qm.general_rates([1e-170, 0, 0], [0, 0, 0], 0.0, True)      # E.E would underflow
        self.assertEqual(tiny["kind"], "electric")
        self.assertAlmostEqual(tiny["eps"] / 1e-170, 1.0, places=12)

    def test_massless_spinor_clamped_e_dot_b_is_flagged_not_zero(self):
        g = qm.general_rates([0, 0, 1e-15], [0, 0, 1.0], 0.0, True)         # w = 0 or inf: undetermined
        self.assertTrue(g["E_dot_B_clamped"])
        self.assertTrue(math.isnan(g["decay_rate"]))
        self.assertIn("reason", g)
        g = qm.general_rates([0, 0, 1e-15], [0, 0, 1.0], 1.0, True)         # massive: exp(-pi m^2/eps) = 0
        self.assertEqual(g["decay_rate"], 0.0)

    def test_magnetic_type_and_null_fields_make_nothing(self):
        for B in ([0, 2.0, 0], [0, 1.0, 0], [0.5, 0, 0]):
            g = qm.general_rates([0, 0, 0] if B[0] else [1.0, 0, 0], B, 1.0, True)
            self.assertEqual((g["pair_rate"], g["decay_rate"]), (0.0, 0.0))


class TimeDependentRefusals(unittest.TestCase):
    def test_refusals(self):
        pf, (t0, t1) = qp.sauter_kinetic_momentum([0.0], 0.5, 2.0)
        bad = [
            lambda: qm.landau_bogoliubov(pf, t0, t1, 0, 0.0, 0.25, True, spin=+1),   # massless lowest level: eps_perp = 0
            lambda: qm.landau_bogoliubov(pf, -1.0, 1.0, 0, 1.0, 0.25, False),       # field still on at the window ends
            lambda: qm.landau_sauter_n(0.0, 0, 0.0, 0.5, 2.0, 0.25, True, spin=+1),  # same, closed form
            lambda: qm.landau_sauter_n(0.0, 0, 1.0, 0.5, 2.0, 0.25, True),          # spinor without spin label
            lambda: qm.landau_sauter_pairs_per_volume(1.0, 0.5, 2.0, 1e-6, True),   # B too weak for a Landau sum
            lambda: qm.landau_sauter_pairs_per_volume(0.0, 0.5, 2.0, 0.25, True),   # m = 0
            lambda: qm.landau_lcfa_pairs_per_volume(0.0, 0.5, 2.0, 0.0, True),      # m = 0 and B = 0
        ]
        for i, fn in enumerate(bad):
            with self.subTest(case=i), self.assertRaises(ValueError):
                fn()


class SauterQuadrature(unittest.TestCase):
    def test_short_pulse_k_par_rule_refines_itself(self):
        # Independent reference: trapezoid on a uniform k_par grid (40001 points over [-400, 400]) times an
        # explicit Landau sum of qp.sauter_n_*; the old plain 96-node rule was 31% (spinor) / 25% (scalar) off here.
        for fermion, want in ((True, 2.81458421033e-3), (False, 5.45339799870e-4)):
            r = qm.landau_sauter_pairs_per_volume(1.0, 1.0, 0.1, 1.0, fermion)
            self.assertLess(abs(r["pairs_per_volume"] / want - 1), 1e-8)
            self.assertLessEqual(r["quad_rel_change"], 1e-8)

    def test_unconverged_rule_raises(self):
        with self.assertRaises(ValueError):
            qm.landau_sauter_pairs_per_volume(1.0, 1.0, 0.1, 1.0, False, n=16, n_max=32, qtol=1e-12)


class SIHelpers(unittest.TestCase):
    def test_critical_fields_and_degeneracy(self):
        me = 0.51099895e6                                   # eV
        self.assertAlmostEqual(qm.eB_from_field_SI(4.414e9) / me ** 2, 1.0, places=3)
        self.assertAlmostEqual(qm.field_B_to_SI(qm.eB_from_field_SI(1e9)), 1e9, delta=1e-3)
        self.assertAlmostEqual(qm.field_E_to_SI(qp.eE_from_field_SI(1e18)), 1e18, delta=1e3)
        self.assertAlmostEqual(qm.landau_degeneracy_SI(1.0) / 2.417989e14, 1.0, places=5)


class CommandLine(unittest.TestCase):
    def test_parallel_cli_si_units(self):
        code, out = run_cli(["parallel", "--E", "1e18 V/m", "--B", "1e9 T"])
        self.assertEqual(code, 0)
        self.assertIn("vacuum-decay rate", out)
        self.assertIn("m^-3 s^-1", out)
        code, out = run_cli(["parallel", "--E", "1e18 V/m", "--B", "1e13 gauss", "--scalar"])
        self.assertEqual(code, 0)

    def test_general_cli_magnetic_type_gives_zero(self):
        code, out = run_cli(["general", "--E", "1e18 V/m", "--B", "4e9 T", "--angle", "90"])
        self.assertEqual(code, 0)
        self.assertIn("kind = magnetic", out)

    def test_sauter_cli_short_pulse_flags_lcfa_and_reports_quadrature(self):
        code, out = run_cli(["sauter", "--E", "1e18 V/m", "--B", "1e9 T", "--tau", "1e-22 s"])
        self.assertEqual(code, 0)
        self.assertIn("NOT valid", out)
        self.assertIn("k_par rule", out)
        exact = float(out.split("after the pulse) ")[1].split(" eV^3")[0])
        self.assertAlmostEqual(exact / 1.73246e14, 1.0, places=4)     # converged value (96 nodes gave 1.19586e14)

    def test_bad_units_return_1(self):
        self.assertEqual(run_cli(["parallel", "--E", "1e18 V/m", "--B", "3 J"])[0], 1)
        self.assertEqual(run_cli(["sauter", "--E", "1e18 V/m", "--B", "1e9 T", "--tau", "3 m"])[0], 1)
        self.assertEqual(run_cli(["parallel", "--E", "1e18 V/m", "--B", "2 furlongs"])[0], 1)


if __name__ == "__main__":
    unittest.main()
