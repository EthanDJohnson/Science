"""Tests for qft_accuracy.py: every public function states its quantity and validity, out-of-range inputs are
refused, and the command line takes SI units. (The full physics self-test runs in test_calculators.py.)

Run from the project root:
    python3 -m unittest discover -s .claude/skills/conundrum/scripts/tests -p "test_qft_accuracy.py" -v
"""
import contextlib
import inspect
import io
import sys
import unittest
from pathlib import Path

import mpmath as mp
import numpy as np

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

import qft_accuracy as qa  # noqa: E402


def public_functions():
    return [(name, fn) for name, fn in inspect.getmembers(qa, inspect.isfunction)
            if not name.startswith("_") and fn.__module__ == qa.__name__ and name not in ("main", "selftest")]


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
        self.assertIn("hbar = c = 1", qa.__doc__)
        self.assertIn("Heaviside-Lorentz", qa.__doc__)

    def test_module_docstring_sections(self):
        for section in ("Assumptions and validity range", "Python usage", "Command line"):
            self.assertIn(section, qa.__doc__)

    def test_asymptotic_and_born_results_are_labelled(self):
        self.assertIn("leading exponential x prefactor", inspect.getdoc(qa.phase_integral_beta2))
        self.assertIn("error O(V^4)", inspect.getdoc(qa.born2_scalar_mode))
        self.assertIn("pole correction", inspect.getdoc(qa.phase_integral_beta2))


class ModeSolverRefusals(unittest.TestCase):
    def test_refusals(self):
        w2, (t0, t1) = qa.tanh_model_mp(0.5, 1.0, 2.0, 1.0, 0.5)
        om2, p, ep, (s0, s1) = qa.sauter_mp(0.0, 0.3, 1.0, 0.5, 2.0)
        bad = [
            lambda: qa.bogoliubov_boson_mp(w2, t1, t0),                                   # reversed window
            lambda: qa.bogoliubov_boson_mp(lambda t: mp.mpf(-1), 0.0, 1.0),               # omega^2 < 0 at the ends
            lambda: qa.bogoliubov_boson_mp(lambda t: 1.0 + 0.0 * float(t), 0.0, 1.0),     # float, not mpmath
            lambda: qa.bogoliubov_boson_mp(w2, t0, t1, rtol=0.0, atol=0.0),               # no tolerance
            lambda: qa.bogoliubov_boson_mp(w2, t0, t1, steps=10 ** 6),                    # beyond max_steps
            lambda: qa.bogoliubov_fermion_mp(p, 0.0, s0, s1),                             # eps_perp = 0
            lambda: qa.tanh_model_mp(0.1, 1.0, 1.0, 2.0, 0.5),                            # omega^2 < 0 somewhere
            lambda: qa.tanh_model_beta2_mp(0.5, 1.0, 2.0, 1.0, 0.0),                      # rho = 0
            lambda: qa.sauter_n_mp(0.0, 0.0, 0.0, 0.5, 2.0, True),                        # m^2 + k_perp^2 = 0
            lambda: qa.sauter_mp(0.0, 0.3, 1.0, -0.5, 2.0),                               # eE0 < 0
            lambda: qa.poschl_teller_mp(1.0, 1.5, 0.5),                                   # V0 >= omega0^2
            lambda: qa.dunne_schubert_exponent(1.0, 0.0, 1.0),                            # no field
            lambda: qa.sauter_ddp_exponent(0.0, 0.0, 0.0, 0.1, 2.0),                      # m^2 + k_perp^2 = 0
            lambda: qa.sauter_ddp_exponent(0.0, 0.3, 1.0, 0.1, -2.0),                     # tau < 0
            lambda: qa.sauter_ddp_exponent([0.0, 0.5], 0.3, 1.0, 0.2, 10.0),              # array: was silently [0]
            lambda: qa.sauter_n_mp(0.0, 0.3, 1.0, 0.5, 2.0, "no"),                        # fermion must be a bool
            lambda: qa.bogoliubov_boson_mp(w2, t0, t1, steps=2 ** 14 + 1),                # 2 x steps > max_steps
        ]
        for i, fn in enumerate(bad):
            with self.subTest(case=i), self.assertRaises(ValueError):
                fn()

    def test_unresolved_is_flagged_or_refused(self):
        # window ends far from adiabatic: the end error dominates, so strict=True must refuse
        w2, _ = qa.tanh_model_mp(0.5, 1.0, 2.0, 1.0, 0.5)
        with self.assertRaises(ValueError):
            qa.bogoliubov_boson_mp(w2, -6.0, 6.0, strict=True)
        r = qa.bogoliubov_boson_mp(w2, -6.0, 6.0)
        self.assertFalse(r["resolved"])


class PhaseIntegralRefusals(unittest.TestCase):
    def test_refusals(self):
        bad = [
            lambda: qa.phase_integral_beta2(lambda t: 1 + 3 / (t * t + mp.mpf(1) / 4), (-5, 5), 4),  # pole below the t.p.
            lambda: qa.phase_integral_beta2(lambda t: t * t - 1, (-5, 5), 4),                        # real turning points
            lambda: qa.phase_integral_beta2(lambda t: 1 + t * t, (-5, 5), 0.5),                      # t.p. (i) outside box
            lambda: qa.phase_integral_beta2(lambda t: 1 + t * t, (-5, 5), 4, statistics="anyon"),
            lambda: qa.turning_points(lambda t: 1 + t * t, (5, -5), 4),                              # empty x range
            lambda: qa.phase_integral_beta2(qa.poschl_teller_mp(1.0, -0.02, 0.1)[0], (-20, 20), 17),  # bump: pole between
            lambda: qa.phase_integral_beta2(qa.tanh_model_mp(0.5, 1, 2, 1, 5.0)[0], (-0.6, 0.6), 0.4),  # 2K = 1.4 < 2
        ]
        for i, fn in enumerate(bad):
            with self.subTest(case=i), self.assertRaises(ValueError):
                fn()

    def test_flags(self):
        # small pole residue (Sauter eE0 tau^2 = 0.3): flagged, strict raises
        om2, _, _, _ = qa.sauter_mp(0.0, 0.0, 1.0, 0.012, 5.0)
        r = qa.phase_integral_beta2(om2, (-15, 15), 8, "fermion")
        self.assertFalse(r["reliable"])
        self.assertAlmostEqual(r["pole_residue"], 0.3, places=8)
        self.assertIn("UNRELIABLE", r["label"])
        with self.assertRaises(ValueError):
            qa.phase_integral_beta2(om2, (-15, 15), 8, "fermion", strict=True)
        # large residue (eE0 tau^2 = 20): reliable
        om2, _, _, _ = qa.sauter_mp(0.0, 0.3, 1.0, 0.2, 10.0)
        self.assertTrue(qa.phase_integral_beta2(om2, (-30, 30), 16)["reliable"])
        # not semiclassical (tanh, 2K = 3.5): flagged
        r = qa.phase_integral_beta2(qa.tanh_model_mp(0.5, 1, 2, 1, 2.0)[0], (-1.5, 1.5), 1.0)
        self.assertFalse(r["semiclassical"])
        self.assertIn("NOT semiclassical", r["label"])

    def test_gaussian_bump_two_pairs_default_window(self):
        # third/fourth pair at K - K1 = 18.3 is negligible: not refused, Dumlu-Dunne two-pair result vs qp (independent)
        w = 10.0
        r = qa.phase_integral_beta2(lambda t: 1 + mp.mpf("0.6") * mp.exp(-(t / w) ** 2), (-3 * w, 3 * w), 2.4 * w)
        self.assertEqual(len(r["K"]), 2)
        self.assertTrue(r["subleading_K"])
        ex = qa.qp.bogoliubov_boson(lambda t: np.array([1.0]) + 0.6 * np.exp(-(t / w) ** 2), -8 * w, 8 * w, rtol=1e-6)
        self.assertTrue(ex["resolved"][0])
        env = 4 * np.exp(-2 * r["K"][0])
        self.assertLess(abs(ex["beta2"][0] - float(r["beta2"])) / env, 0.05)   # measured 0.015 (O(1/K), K = 24.9)

    def test_landau_zener_exponent(self):
        r = qa.phase_integral_beta2(lambda t: mp.mpf(2) + (mp.mpf("0.5") * t) ** 2, (-10, 10), 10)
        self.assertAlmostEqual(r["exponent"], mp.pi * 2 / 0.5, places=10)
        self.assertEqual(len(r["turning_points"]), 1)


class BornRefusals(unittest.TestCase):
    def test_refusals(self):
        bad = [
            lambda: qa.born2_scalar_mode(lambda t: 0.1 + 0 * t, [1.0], -5.0, 5.0),            # V does not switch off
            lambda: qa.born2_scalar_mode(lambda t: 50 * np.exp(-t * t), [1.0], -8.0, 8.0),    # expansion parameter > 1
            lambda: qa.born2_scalar_mode(lambda t: np.exp(-t * t), [-1.0], -8.0, 8.0),        # omega0 < 0
            lambda: qa.born2_scalar_mode(lambda t: np.exp(-t * t), [1.0], 8.0, -8.0),         # reversed window
            lambda: qa.born2_scalar_number_density(lambda t: 0.1 * np.exp(-t * t), -8.0, 8.0, -1.0, 5.0),   # m < 0
            lambda: qa.born2_fermion_efield_mode(lambda t: 0.1 * np.tanh(t), [0.0], 0.3, 1.0, -8.0, 8.0),  # A(+-inf) != 0
            lambda: qa.born2_fermion_efield_mode(lambda t: 0.1 * np.exp(-t * t), [0.0], 0.0, 0.0, -8.0, 8.0),  # eps_perp = 0
            lambda: qa.born2_scalar_number_density(lambda t: 0.1 * np.exp(-t * t), -8.0, 8.0, 1.0, 5.0, g=-2),  # g < 0
            # omega0 tau >= 2 everywhere: Born fails although lam << 1
            lambda: qa.born2_scalar_number_density(lambda t: 0.1 * np.exp(-t * t / 2), -12.0, 12.0, 2.5, 3.0),
            lambda: qa.born2_scalar_mode(lambda t: 0.1 * np.exp(-t * t / 2), [2.0], -12.0, 12.0, strict=True),
            lambda: qa.born2_fermion_efield_mode(lambda t: 0.1 * np.exp(-t * t / 2), [0.0], 2.0, 1.0, -12.0, 12.0,
                                                 strict=True),
        ]
        for i, fn in enumerate(bad):
            with self.subTest(case=i), self.assertRaises(ValueError):
                fn()

    def test_high_frequency_modes_flagged(self):
        # Gaussian V, tau = 1, omega0 = 2: raw Born-2 is negative (-5.9e-10 vs exact 7.3e-13)
        r = qa.born2_scalar_mode(lambda t: 0.1 * np.exp(-t * t / 2), [0.5, 2.0], -12.0, 12.0)
        self.assertEqual(list(r["born_ok"]), [True, False])
        self.assertTrue(np.isnan(r["beta2_born2"][1]) and np.isnan(r["beta2_born1"][1]))
        self.assertGreater(r["b2_sq"][1], abs(r["b1"][1]) ** 2)
        f = qa.born2_fermion_efield_mode(lambda t: 0.1 * np.exp(-t * t / 2), [0.0], 3.0, 1.0, -12.0, 12.0)
        self.assertFalse(f["born_ok"][0])                  # c2 = 0 at k_par = 0; c3 flags it

    def test_born1_matches_closed_form_for_sech2(self):
        # |b1|^2 = pi^2 x^2 / sinh^2(pi w0/rho), x = eps/rho^2 (first order of the Poeschl-Teller closed form)
        eps, rho, w0 = 0.02, 0.7, np.array([0.8])
        r = qa.born2_scalar_mode(lambda t: eps / np.cosh(rho * t) ** 2, w0, -60.0, 60.0)
        x = eps / rho ** 2
        self.assertAlmostEqual(float(r["beta2_born1"][0] / (np.pi ** 2 * x * x / np.sinh(np.pi * w0[0] / rho) ** 2)), 1.0,
                               places=9)


class CommandLine(unittest.TestCase):
    def test_sauter_cli_with_si_units(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = qa.main(["sauter", "--E", "1e17 V/m", "--tau", "1e-18 s"])
        self.assertEqual(code, 0)
        out = buf.getvalue()
        self.assertIn("phase integral", out)
        self.assertIn("Dunne-Schubert", out)
        self.assertIn("skipped", out)                       # m tau ~ 800: the mp solver would need too many steps

    def test_mixed_units_refused(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(qa.main(["sauter", "--m", "1", "--E", "1e17 V/m", "--tau", "1"]), 1)
            self.assertEqual(qa.main(["sauter", "--E", "1e17 V/m", "--tau", "1"]), 1)     # m defaults to a unit string

    def test_sauter_cli_small_residue_flagged(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = qa.main(["sauter", "--m", "1", "--E", "0.012", "--tau", "5"])
        self.assertEqual(code, 0)
        self.assertIn("UNRELIABLE", buf.getvalue())

    def test_bad_unit_returns_1(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(qa.main(["sauter", "--E", "3 J", "--tau", "1e-18 s"]), 1)
            self.assertEqual(qa.main(["sauter", "--E", "1e17 V/m", "--tau", "2 m"]), 1)

    def test_born2_cli(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = qa.main(["born2", "--eps", "0.1"])
        self.assertEqual(code, 0)
        self.assertIn("Born-2", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
