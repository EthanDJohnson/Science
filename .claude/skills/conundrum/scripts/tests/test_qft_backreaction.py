"""Tests for qft_backreaction.py: every public function states its quantity and validity, out-of-range inputs
are refused, and the command line takes SI units. (The full physics self-test runs in test_calculators.py.)

Run from the project root:
    python3 -m unittest discover -s .claude/skills/conundrum/scripts/tests -p "test_qft_backreaction.py" -v
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

import qft_backreaction as br  # noqa: E402


def public_functions():
    return [(name, fn) for name, fn in inspect.getmembers(br, inspect.isfunction)
            if not name.startswith("_") and fn.__module__ == br.__name__ and name not in ("main", "selftest")]


def run_cli(argv):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = br.main(argv)
    return code, buf.getvalue()


class Docstrings(unittest.TestCase):
    def test_every_public_function_states_quantity_and_validity(self):
        funcs = public_functions()
        self.assertGreaterEqual(len(funcs), 9)
        for name, fn in funcs:
            doc = inspect.getdoc(fn) or ""
            with self.subTest(function=name):
                self.assertRegex(doc, r"(?m)^Quantity: \S", f"{name} lacks a 'Quantity:' line")
                self.assertRegex(doc, r"(?m)^Valid when: \S", f"{name} lacks a 'Valid when:' line")

    def test_module_docstring_states_units_and_traps(self):
        self.assertIn("hbar = c = 1", br.__doc__)
        self.assertIn("Heaviside-Lorentz", br.__doc__)
        self.assertIn("transient", br.__doc__)          # polarization 'pairs' while the field is on
        self.assertIn("CANONICAL momentum", br.__doc__)  # the gauge-invariance trap


class SolverRefusals(unittest.TestCase):
    def test_bad_inputs(self):
        k = np.linspace(-5, 5, 41)
        bad = [
            lambda: br.qed2_backreaction(0.0, 1.0, 1.0, 1.0),                         # m = 0
            lambda: br.qed2_backreaction(1.0, -1.0, 1.0, 1.0),                        # e < 0
            lambda: br.qed2_backreaction(1.0, 1.0, 1.0, -1.0),                        # t_end < t0
            lambda: br.qed2_backreaction(1.0, 1.0, 1.0, 1.0, "majorana"),             # unknown field
            lambda: br.qed2_backreaction(1.0, 1.0, 1.0, 1.0, dk=2.0),                 # grid coarser than m
            lambda: br.qed2_backreaction(1.0, 1.0, 1.0, 1.0, k_max=10.0, dk=0.5, dt=1.0),   # omega_max dt > 1.5
            lambda: br.qed2_backreaction(1.0, 1.0, 1.0, 1.0, k_nodes=k),              # nodes without weights
            lambda: br.qed2_backreaction(1.0, 1.0, 1.0, 1.0, E_ext=3.0),              # E_ext not callable
            lambda: br.qed2_backreaction(1.0, 1.0, float("nan"), 1.0),                # non-finite field
        ]
        for i, fn in enumerate(bad):
            with self.subTest(case=i), self.assertRaises(ValueError):
                fn()

    def test_ring_longer_than_causal_time_is_refused_unless_asked(self):
        # uniform grid dk = 0.5 is a ring of length 4 pi: pairs meet their images after t = pi/dk = 6.28
        with self.assertRaises(ValueError):
            br.qed2_backreaction(1.0, 1.0, 0.1, 8.0, k_max=8.0, dk=0.5)
        r = br.qed2_backreaction(1.0, 1.0, 0.1, 8.0, k_max=8.0, dk=0.5, finite_ring=True)
        self.assertAlmostEqual(r["ring_length"], 4 * math.pi)

    def test_pairs_leaving_the_grid_are_refused(self):
        # strong constant field, no back-reaction: produced pairs accelerate off a narrow grid
        with self.assertRaises(ValueError):
            br.qed2_backreaction(1.0, 1.0, 2.0, 6.0, backreaction=False, k_max=4.0, dk=0.1)

    def test_energy_drift_is_refused(self):
        with self.assertRaises(ValueError):
            br.qed2_backreaction(1.0, 1.0, 1.0, 3.0, k_max=10.0, dk=0.25, dt=0.14, drift_tol=1e-12)


class ClosedFormRefusals(unittest.TestCase):
    def test_bad_inputs(self):
        bad = [
            lambda: br.schwinger_boson_mass(0.0),
            lambda: br.vacuum_susceptibility(-1.0, 1.0, 1.0),                    # advanced side: Re s < 0
            lambda: br.vacuum_susceptibility(1.0, 0.0, 1.0),                     # m = 0
            lambda: br.dielectric_constant(1.0, 1.0, "photon"),
            lambda: br.screened_sauter_field(0.0, 1.0, 1.0, 1e-3, -1.0),          # tau < 0
            lambda: br.screened_sauter_field(100.0, 1.0, 1.0, 1e-3, 1.0),         # |t| > 40 tau
            lambda: br.pair_rates_constant_field(1.0, 0.0),                      # no field
            lambda: br.adiabatic_polarization_pairs(-1.0, 0.1),
            lambda: br.oscillation_period([0, 1, 2, 3], [1, 1, 1, 1]),           # no crossings
            lambda: br.oscillation_period([0, 1, 2, 3], [1, -1, 1, -1], direction="down"),
        ]
        for i, fn in enumerate(bad):
            with self.subTest(case=i), self.assertRaises(ValueError):
                fn()


class Quantities(unittest.TestCase):
    def test_pair_rate_and_decay_rate_differ(self):
        f, s = br.pair_rates_constant_field(1.0, 3.0, "spinor"), br.pair_rates_constant_field(1.0, 3.0, "scalar")
        self.assertGreater(f["decay_rate"], 1.1 * f["pair_rate"])
        self.assertLess(s["decay_rate"], 0.95 * s["pair_rate"])

    def test_static_limit_of_susceptibility(self):
        for field, c in (("spinor", 6.0), ("scalar", 12.0)):
            self.assertAlmostEqual(br.dielectric_constant(2.0, 1.0, field), 1 + 1 / (c * math.pi * 4.0), places=14)
            self.assertAlmostEqual(br.vacuum_susceptibility(1e-3, 2.0, 1.0, field).real,
                                   1 / (c * math.pi * 4.0), places=8)

    def test_massless_limit_of_susceptibility(self):
        # chi_F -> e^2/(pi s^2) for m -> 0: the photon mass mu^2 = e^2/pi
        s = 2.0
        self.assertAlmostEqual(br.vacuum_susceptibility(s, 1e-4, 1.0, "spinor").real * math.pi * s * s, 1.0, places=6)

    def test_backreaction_off_keeps_the_field(self):
        r = br.qed2_backreaction(1.0, 1.0, 0.5, 4.0, backreaction=False, k_max=8.0, dk=0.25)
        self.assertTrue(np.allclose(r["E_steps"], 0.5))
        self.assertGreater(r["pairs"][-1], 0.0)

    def test_oscillation_period_of_a_cosine(self):
        t = np.linspace(0, 30, 3001)
        self.assertAlmostEqual(br.oscillation_period(t, np.cos(2.0 * t))["period"], math.pi, places=5)
        self.assertAlmostEqual(br.oscillation_period(t, np.cos(2.0 * t), direction="any")["period"], math.pi, places=5)


class CommandLine(unittest.TestCase):
    def test_qed2_cli_natural_units(self):
        code, out = run_cli(["qed2", "--m", "1", "--e", "1", "--E0", "1", "--t", "4"])
        self.assertEqual(code, 0)
        self.assertIn("pairs per length", out)

    def test_qed2_cli_si_units(self):
        code, out = run_cli(["qed2", "--m", "0.511 MeV", "--e", "0.511 MeV", "--E0", "0.511 MeV", "--t", "1e-21 s"])
        self.assertEqual(code, 0)
        self.assertIn("m^-1", out)

    def test_rate_cli_si_units(self):
        code, out = run_cli(["rate", "--m", "0.511 MeV", "--eE", "0.25 MeV^2"])
        self.assertEqual(code, 0)
        self.assertIn("vacuum-decay rate", out)
        self.assertIn("m^-1 s^-1", out)

    def test_bad_units_return_1(self):
        self.assertEqual(run_cli(["qed2", "--m", "3 m", "--e", "0.3 MeV", "--E0", "1 MeV"])[0], 1)   # a length
        self.assertEqual(run_cli(["qed2", "--m", "1", "--e", "0.3 MeV", "--E0", "1"])[0], 1)        # mixed units
        self.assertEqual(run_cli(["rate", "--m", "0.511 MeV", "--eE", "3 J"])[0], 1)                # not energy^2


if __name__ == "__main__":
    unittest.main()
