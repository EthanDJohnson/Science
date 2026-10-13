"""Tests for qft_second_order.py: every public function states its quantity and validity, out-of-range inputs
are refused, and the command line takes SI units. (The full physics self-test runs in test_calculators.py.)

Run from the project root:
    python3 -m unittest discover -s .claude/skills/conundrum/scripts/tests -p "test_qft_second_order.py" -v
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

import qft_second_order as q  # noqa: E402


def public_functions():
    return [(name, fn) for name, fn in inspect.getmembers(q, inspect.isfunction)
            if not name.startswith("_") and fn.__module__ == q.__name__ and name not in ("main", "selftest")]


def cm_kinematics(theta=1.1, s=3.0):
    E = 0.5 * math.sqrt(s)
    q1, q2 = np.array([E, 0, 0, E]), np.array([E, 0, 0, -E])
    n = np.array([math.sin(theta), 0.0, math.cos(theta)])
    k1, k2 = np.concatenate([[E], E * n]), np.concatenate([[E], -E * n])
    return q1, q2, k1, k2


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
        self.assertIn("hbar = c = 1", q.__doc__)
        self.assertIn("Heaviside-Lorentz", q.__doc__)


class AmplitudeRefusals(unittest.TestCase):
    def test_refusals(self):
        q1, q2, k1, k2 = cm_kinematics()
        E1, E2 = q.graviton_polarization(q1, "R"), q.graviton_polarization(q2, "L")
        e1, e2 = q.photon_polarization(k1, 1), q.photon_polarization(k2, -1)
        bad_eps = E1.copy()
        bad_eps[0, 0] = 1.0                                                     # not transverse/traceless
        off_shell = q1 * np.array([1.0, 1.0, 1.0, 0.9])
        q1c, q2c, k1c, k2c = cm_kinematics(theta=0.0)                           # photon along graviton 1: t = 0
        bad = [
            lambda: q.amplitude_gg_to_photons(off_shell, E1, q2, E2, k1, e1, k2, e2),          # off-shell graviton
            lambda: q.amplitude_gg_to_photons(q1, bad_eps, q2, E2, k1, e1, k2, e2),            # not TT
            lambda: q.amplitude_gg_to_photons(q1, E1, q2, E2, 1.1 * k1, e1, k2, e2),            # momentum not conserved
            lambda: q.amplitude_gg_to_photons(q1, E1, q2, E2, k1, e1 + np.array([1, 0, 0, 0]), k2, e2),  # e.k != 0
            lambda: q.amplitude_gg_to_photons(q1, E1, q1, E1, q1, e1, q1, e1),                 # collinear: s = 0
            lambda: q.amplitude_gg_to_photons(q1c, E1, q2c, E2, k1c, q.photon_polarization(k1c, 1), k2c,
                                              q.photon_polarization(k2c, 1)),                   # t = 0 exactly
            lambda: q.amplitude_gg_to_scalars(q1, E1, q2, E2, k1, k2, m=0.5),                  # k^2 != m^2
            lambda: q.amplitude_gg_to_scalars(q1, E1, q2, E2, k1, k2, m=-1.0),
            lambda: q.amplitude_gg_to_photons(q1, E1, q2, E2, k1, e1, k2, e2, G=0.0),
            lambda: q.graviton_polarization(q1, "vector"),
            lambda: q.photon_polarization(k1, 0),
            lambda: q.compton_amplitude("electron", k1, q1, E1, k1, q1, E1),
            lambda: q.compton_amplitude("scalar", -k2, q1, E1, -k2, q1, E1),                    # zero momentum transfer
        ]
        # photon-graviton Compton (theta = 1): non-transverse photon polarisations and negative energies are refused
        Pin, Kin = np.array([1.0, 0, 0, -1.0]), np.array([1.0, 0, 0, 1.0])
        Kout = np.array([1.0, math.sin(1.0), 0, math.cos(1.0)])
        Pout = Pin + Kin - Kout
        Gi, Go = q.graviton_polarization(Kin, 2), q.graviton_polarization(Kout, 2)
        ei, eo = q.photon_polarization(Pin, 1), q.photon_polarization(Pout, 1)
        bad += [
            lambda: q.compton_amplitude("photon", Pin, Kin, Gi, Pout, Kout, Go, np.array([1.0, 0, 0, 0]), eo),
            lambda: q.compton_amplitude("photon", Pin, Kin, Gi, Pout, Kout, Go, ei + np.array([0.5, 0, 0, 0]), eo),
            lambda: q.compton_amplitude("photon", Pin, Kin, Gi, Pout, Kout, Go, ei, eo + np.array([0.5, 0, 0, 0])),
            lambda: q.compton_amplitude("scalar", -Pin, -Kin, Gi, -Pout, -Kout, Go),            # negative energies
        ]
        for i, fn in enumerate(bad):
            with self.subTest(case=i), self.assertRaises(ValueError):
                fn()

    def test_cross_section_refusals(self):
        bad = [
            lambda: q.helicity_amplitudes_cm(1.0, 0.0),                    # exactly forward
            lambda: q.helicity_amplitudes_cm(1.0, 1.0, final="graviton"),
            lambda: q.sigma_total(1.0, "R", "L", "scalar", m=0.6),         # below threshold s < 4 m^2
            lambda: q.sigma_total(1.0, "R", "L", "photon", m=0.1),         # massive photon
            lambda: q.sigma_total(1.0, "R", "L", n_theta=4),               # quadrature too coarse
            lambda: q.sigma_total(1.0, "R", "L", "scalar", field="majorana"),
            lambda: q.dsigma_domega_cm(-1.0, 1.0),
            lambda: q.sigma_total_massless_closed_form(0.0),
            lambda: q.compton_scalar_lab_dsigma(1.0, 1.0, 0.0),            # massless target at rest
            lambda: q.sigma_total(1.0, "R", "R", "scalar", m=1e-5),        # m^2/s < 1e-8: same-helicity roundoff
            lambda: q.sigma_same_helicity_scalar_closed_form(1.0, 0.0),
            lambda: q.sigma_same_helicity_scalar_closed_form(1.0, 0.6),    # below threshold
        ]
        for i, fn in enumerate(bad):
            with self.subTest(case=i), self.assertRaises(ValueError):
                fn()


class WaveAndBeamRefusals(unittest.TestCase):
    def test_refusals(self):
        q1, q2, _, _ = cm_kinematics()
        bad = [
            lambda: q.gw_plane_wave(1.0, 0.5, [0, 0, 1]),                  # strain not perturbative
            lambda: q.gw_plane_wave(-1.0, 1e-3, [0, 0, 1]),
            lambda: q.gw_plane_wave(1.0, 1e-3, [0, 0, 0]),
            lambda: q.beams_pair_rate(1.0, 1e-3, 1.0, 1e-3, 0.0),          # collinear: theta = 0
            lambda: q.beams_pair_rate(1.0, 1e-3, 1.0, 1e-3, 4.0),          # theta > pi
            lambda: q.beams_pair_rate(1.0, 1e-3, 1.0, 1e-3, 0.1, final="scalar", m=0.5),   # below threshold
            lambda: q.beams_pair_rate_SI(-1.0, 1e-21, 1.0),
            lambda: q.second_order_metric(q1, q.graviton_polarization(q1, "R"), q1, q.graviton_polarization(q1, "L")),
            lambda: q.newton_G_natural(0.0),
            lambda: q.beams_pair_rate(1.0, 1e-3, 1.0, 1e-3, 1e-13),        # K0^2/s = 4e26 > 1e24: untested
        ]
        for i, fn in enumerate(bad):
            with self.subTest(case=i), self.assertRaises(ValueError):
                fn()

    def test_quantities_are_consistent(self):
        # pairs vs particles, and the documented G-independence of the rate at fixed strain
        r1 = q.beams_pair_rate(1.0, 1e-3, 1.0, 1e-3, 2.0, "R", "L", G=1.0)
        r2 = q.beams_pair_rate(1.0, 1e-3, 1.0, 1e-3, 2.0, "R", "L", G=5.0)
        self.assertAlmostEqual(r1["particle_rate"] / r1["pair_rate"], 2.0, places=12)
        self.assertAlmostEqual(r2["pair_rate"] / r1["pair_rate"], 1.0, places=10)
        # same-helicity waves make no photon pairs at tree level
        r3 = q.beams_pair_rate(1.0, 1e-3, 1.0, 1e-3, 2.0, "R", "R")
        self.assertLess(r3["pair_rate"], 1e-20 * r1["pair_rate"])

    def test_extreme_kinematics_match_closed_forms(self):
        # frequency ratio 1e-10 (LIGO x PTA) and nearly collinear waves: once wrong by up to 1e22 without warning
        for w2, th, pols in ((1e-10, 1.0, (("R", "L"), ("plus", "cross"))), (1.0, 1e-7, (("R", "L"), ("plus", "plus")))):
            for pa, pb in pols:
                with self.subTest(w2=w2, theta=th, pols=(pa, pb)):
                    r = q.beams_pair_rate(1.0, 1e-3, w2, 2e-3, th, pa, pb)
                    fl = 2 * math.sin(th / 2) ** 2
                    want = q.sigma_total_massless_closed_form(2 * w2 * fl, pa, pb) * r["n1"] * r["n2"] * fl
                    self.assertAlmostEqual(r["pair_rate"] / want, 1.0, places=11)
                    self.assertAlmostEqual(r["s"] / (2 * w2 * fl), 1.0, places=14)

    def test_light_scalar_same_helicity(self):
        # the m^4 same-helicity piece, peaked within 2 m^2/s of the axis: graded panels vs the analytic integral
        for m in (0.01, 0.003):
            with self.subTest(m=m):
                got = q.sigma_total(1.0, "R", "R", "scalar", m)
                self.assertAlmostEqual(got / q.sigma_same_helicity_scalar_closed_form(1.0, m), 1.0, places=8)
        self.assertAlmostEqual(q.sigma_same_helicity_scalar_closed_form(1.0, 0.01, field="complex")
                               / q.sigma_same_helicity_scalar_closed_form(1.0, 0.01), 2.0, places=13)

    def test_amplitude_anchor(self):
        # |M| <= 8 pi G s for photons (O(kappa^2 s)), attained as t -> -s
        amps = q.helicity_amplitudes_cm(2.0, 0.3, final="photon", G=1.0)
        self.assertLessEqual(max(abs(a) for a in amps.values()), 8 * math.pi * 2.0)
        self.assertGreater(max(abs(a) for a in amps.values()), 0.9 * 8 * math.pi * 2.0)


class CommandLine(unittest.TestCase):
    def test_beams_cli_with_SI_units(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = q.main(["beams", "--omega", "1 kHz", "--h", "1e-21", "--theta", "180"])
        self.assertEqual(code, 0)
        out = buf.getvalue()
        self.assertIn("PAIRS per m^3 per s", out)
        rate = float(out.split("plane waves): ")[1].split()[0])
        # linear polarisations, head-on: w^4 h^4 (1 - cos th)^2/(1280 pi c^3), w = 1000 rad/s
        self.assertAlmostEqual(rate / (1e12 * 1e-84 * 4 / (1280 * math.pi * 299792458.0 ** 3)), 1.0, places=4)

    def test_omega_in_hz_prints_note(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            q.main(["beams", "--omega", "1 kHz", "--h", "1e-21", "--theta", "90"])
        self.assertIn("ANGULAR frequency", buf.getvalue())

    def test_compton_cli_in_units_of_m(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            self.assertEqual(q.main(["compton", "--omega", "0.3", "--theta", "40"]), 0)
        val = float(buf.getvalue().split("= ")[1].split()[0])
        self.assertAlmostEqual(val / q.compton_scalar_lab_dsigma(0.3, math.radians(40), 1.0), 1.0, places=6)

    def test_bad_unit_returns_1(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(q.main(["beams", "--omega", "3 J", "--h", "1e-21", "--theta", "90"]), 1)
            self.assertEqual(q.main(["beams", "--f", "1 kHz", "--h", "0.5", "--theta", "90"]), 1)

    def test_amplitudes_cli(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = q.main(["amplitudes", "--theta", "60", "--final", "scalar", "--m", "0.3"])
        self.assertEqual(code, 0)
        self.assertIn("sigma_tot", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
