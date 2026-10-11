"""Tests for qft_thermal.py: every public function states its quantity and validity, out-of-range inputs are
refused, and the command line takes SI units. (The full physics self-test runs in test_calculators.py.)

Run from the project root:
    python3 -m unittest discover -s .claude/skills/conundrum/scripts/tests -p "test_qft_thermal.py" -v
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

import qft_production as qp  # noqa: E402
import qft_thermal as th  # noqa: E402


def public_functions():
    return [(name, fn) for name, fn in inspect.getmembers(th, inspect.isfunction)
            if not name.startswith("_") and fn.__module__ == th.__name__ and name not in ("main", "selftest")]


class Docstrings(unittest.TestCase):
    def test_every_public_function_states_quantity_and_validity(self):
        funcs = public_functions()
        self.assertGreater(len(funcs), 12)
        for name, fn in funcs:
            doc = inspect.getdoc(fn) or ""
            with self.subTest(function=name):
                self.assertRegex(doc, r"(?m)^Quantity: \S", f"{name} lacks a 'Quantity:' line")
                self.assertRegex(doc, r"(?m)^Valid when: \S", f"{name} lacks a 'Valid when:' line")

    def test_module_docstring_states_units_and_the_quantity_traps(self):
        self.assertIn("hbar = c = 1", th.__doc__)
        self.assertIn("Heaviside-Lorentz", th.__doc__)
        for phrase in ("NET created", "TOTAL out occupation", "Landau damping", "in-in"):
            self.assertIn(phrase, th.__doc__)


class Refusals(unittest.TestCase):
    def test_occupation_and_mode_refusals(self):
        bad = [
            lambda: th.bose_einstein([0.5], 1.0, mu=0.6),                                  # omega < mu: condensate
            lambda: th.bose_einstein([1.0], -1.0),                                         # negative temperature
            lambda: th.fermi_dirac([1.0], float("nan")),
            lambda: th.thermal_in_occupations([1.0], 0.5, mu=0.2, field="real"),           # real field has no charge
            lambda: th.thermal_in_occupations([1.0], 0.5, statistics="fermion", field="real"),   # Majorana not covered
            lambda: th.thermal_in_occupations([1.0], 0.5, statistics="anyon"),
            lambda: th.out_occupation([1.5], [0.1], [0.1], "fermion"),                     # |beta|^2 > 1 for fermions
            lambda: th.out_occupation([0.1], [-0.1], [0.0]),                               # negative occupation
            lambda: th.thermal_mode_production([0.1], [0.0], 1.0),                         # omega_in = 0
            lambda: th.thermal_number_density(lambda k: k, lambda k: k + 1, 1.0, 1.0, kmin=2.0),
            lambda: th.temperature_to_eV(-1.0),
        ]
        for i, fn in enumerate(bad):
            with self.subTest(case=i), self.assertRaises(ValueError):
                fn()

    def test_field_and_born_refusals(self):
        V = lambda K0, Kx, Ky, Kz: np.exp(-(K0 * K0 + Kx * Kx + Ky * Ky + Kz * Kz))   # noqa: E731
        bad = [
            lambda: th.thermal_pair_weight(2.0, 3.0, 1.0, 1.0),                            # spacelike K: scattering
            lambda: th.thermal_pair_weight(3.0, 0.0, 2.0, 1.0),                            # below threshold s < 4 m^2
            lambda: th.thermal_pair_weight(3.0, 0.0, 1.0, 1.0, mu=1.2),                    # boson |mu| >= m
            lambda: th.born_scalar_homogeneous_thermal(lambda t: 0.1 * np.exp(-t * t), -6, 6, 0.0, 10.0, 1.0),  # m = 0, T > 0
            lambda: th.born_scalar_homogeneous_thermal(lambda t: 0.1 * np.exp(-t * t), -6, 6, 1.0, 10.0, 1.0,
                                                       field="real", mu=0.3),             # real field with mu
            lambda: th.born_scalar_general_thermal(V, 0.0, 10.0, 4.0, 1.0),                # massless phi^2 vertex, no s_min
            lambda: th.born_scalar_general_thermal(V, 1.0, 3.0, 4.0, 1.0),                 # s_max below threshold
            lambda: th.born_yukawa_homogeneous_thermal(lambda t: t, -1.0, 1.0, 1.0, 1.5, 0.5),   # omega_max < 2m
            lambda: th.sauter_thermal_pairs_per_volume(1.0, 0.5, 2.0, 0.5, mu=1.0, fermion=False),   # scalar |mu| >= m
            lambda: th.sauter_thermal_mode(0.0, 0.3, 1.0, -0.5, 2.0, 0.5),                 # eE0 < 0 (qp refuses)
            lambda: th.frw_redshifted_temperature(1.0, 0.0, 2.0),
            lambda: th.frw_thermal_production([0.5], lambda e: 1.0, 0.0, 1 / 6, -5.0, 5.0, -1.0),   # T_in < 0
            lambda: th.pair_spectral_density_yukawa([4.0], -1.0),
        ]
        for i, fn in enumerate(bad):
            with self.subTest(case=i), self.assertRaises(ValueError):
                fn()


class Physics(unittest.TestCase):
    def test_zero_temperature_is_the_vacuum(self):
        b2 = np.array([0.02, 0.3])
        for stat in ("boson", "fermion"):
            r = th.thermal_mode_production(b2, [1.0, 2.0], 0.0, statistics=stat)
            np.testing.assert_allclose(r["net_created"], b2, rtol=0, atol=0)
            np.testing.assert_allclose(r["particles_out"], b2, rtol=0, atol=0)

    def test_mu_zero_factors_are_coth_and_tanh(self):
        w, T = np.array([0.4, 1.0, 3.0]), 0.7
        rb = th.thermal_mode_production(np.full(3, 0.1), w, T, statistics="boson", field="real")
        rf = th.thermal_mode_production(np.full(3, 0.1), w, T, statistics="fermion")
        np.testing.assert_allclose(rb["factor"], 1 / np.tanh(w / (2 * T)), rtol=1e-13)
        np.testing.assert_allclose(rf["factor"], np.tanh(w / (2 * T)), rtol=1e-13)

    def test_thermal_fermions_always_net_create(self):
        for mu in (-5.0, -0.3, 0.0, 0.9, 5.0):
            r = th.thermal_mode_production([0.2], [1.0], 0.8, mu, "fermion")
            self.assertGreater(float(r["net_created"][0]), 0.0)
            self.assertLess(float(r["net_created"][0]), 0.2)

    def test_number_density_pairs_and_zero_temperature(self):
        b2 = lambda k: np.exp(-k * k)                 # noqa: E731
        om = lambda k: np.sqrt(k * k + 1.0)            # noqa: E731
        r0 = th.thermal_number_density(b2, om, 0.0, 12.0, field="real")
        self.assertAlmostEqual(r0["net_particles_per_volume"], qp.number_density_isotropic(b2, 12.0), places=14)
        self.assertAlmostEqual(r0["pairs_per_volume"], 0.5 * r0["net_particles_per_volume"], places=15)
        rT = th.thermal_number_density(b2, om, 1.0, 12.0, field="complex")
        self.assertGreater(rT["pairs_per_volume"], rT["vacuum_pairs_per_volume"])           # stimulated
        self.assertAlmostEqual(rT["out_particles_per_volume"],
                               rT["in_particles_per_volume"] + rT["net_particles_per_volume"], places=14)

    def test_weight_branches_join_smoothly(self):
        # the Gauss-Legendre branch (kappa b < 0.05 T) and the closed-form log branch must agree at the switch
        for stat, mu in (("boson", 0.3), ("fermion", -0.7)):
            T = 1.0
            lo = th.thermal_pair_weight(3.0, 0.04999 / math.sqrt(1 - 4 / (9 - 0.04999 ** 2)), 1.0, T, mu, stat)
            hi = th.thermal_pair_weight(3.0, 0.05001 / math.sqrt(1 - 4 / (9 - 0.05001 ** 2)), 1.0, T, mu, stat)
            self.assertAlmostEqual(float(lo), float(hi), places=6)
            at_rest = th.thermal_pair_weight(3.0, 0.0, 1.0, T, mu, stat)
            sg = 1 if stat == "boson" else -1
            occ = th.bose_einstein if stat == "boson" else th.fermi_dirac
            self.assertAlmostEqual(float(at_rest), 1 + sg * float(occ(1.5, T, mu) + occ(1.5, T, -mu)), places=13)

    def test_si_temperature_and_redshift(self):
        self.assertAlmostEqual(th.temperature_to_eV(th.temperature_from_eV(0.025)), 0.025, places=15)
        self.assertAlmostEqual(th.temperature_to_eV(11604.518), 1.0, places=6)      # 1 eV = 11604.518 K
        self.assertAlmostEqual(th.frw_redshifted_temperature(2.0, 1.0, 4.0), 0.5)


class CommandLine(unittest.TestCase):
    def run_cli(self, argv):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = th.main(argv)
        return code, buf.getvalue()

    def test_mode_cli_with_SI_units(self):
        code, out = self.run_cli(["mode", "--beta2", "0.01", "--omega", "0.6 MeV", "--T", "5e9 K", "--fermion"])
        self.assertEqual(code, 0)
        self.assertIn("Pauli-blocked", out)
        self.assertIn("TOTAL out occupation", out)
        code, out = self.run_cli(["mode", "--beta2", "0.01", "--omega", "0.6 MeV", "--T", "0.4 MeV", "--mu", "0.2 MeV"])
        self.assertEqual(code, 0)
        self.assertIn("stimulated", out)

    def test_bad_units_return_1(self):
        self.assertEqual(self.run_cli(["mode", "--beta2", "0.01", "--omega", "0.6 MeV", "--T", "3 m"])[0], 1)
        self.assertEqual(self.run_cli(["sauter", "--E", "1e18 V/m", "--tau", "1e-21 m", "--T", "3e9 K"])[0], 1)

    def test_sauter_cli_with_SI_units(self):
        code, out = self.run_cli(["sauter", "--E", "1e18 V/m", "--tau", "1e-21 s", "--T", "3e9 K"])
        self.assertEqual(code, 0)
        self.assertIn("m^-3", out)
        self.assertIn("Pauli blocking", out)


if __name__ == "__main__":
    unittest.main()
