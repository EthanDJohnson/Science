"""Tests for unit_tools.py and rocket_tools.py, plus every toolkit self-test.

Run from the project root:
    python3 -m unittest discover -s .claude/skills/conundrum/scripts/tests -v
"""
import contextlib
import importlib
import io
import math
import os
import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

import rocket_tools as R  # noqa: E402
import unit_tools as U  # noqa: E402


class Units(unittest.TestCase):
    def test_parsing_rules(self):
        self.assertAlmostEqual(U.Q("3 km/s").to("m/s"), 3000.0)           # (3 km)/s
        self.assertAlmostEqual(U.Q("1 J/(kg K)").si, 1.0)
        self.assertEqual(U.Q("1 J/(kg K)").dims, U._d(L=2, T=-2, K=-1))
        self.assertAlmostEqual(U.Q("2^-1").to("1"), 0.5)
        self.assertAlmostEqual(U.Q("(9 m^2)^(1/2)").to("m"), 3.0)
        self.assertAlmostEqual(U.Q("1 m ** 3").to("L"), 1000.0)
        self.assertAlmostEqual(U.Q("-2 m + 5 m").to("m"), 3.0)

    def test_prefixes_and_special_names(self):
        self.assertAlmostEqual(U.Q("1 GeV").to("J"), 1.602176634e-10)
        self.assertAlmostEqual(U.Q("1 MWh").to("GJ"), 3.6)
        self.assertAlmostEqual(U.Q("1 h").to("s"), 3600.0)                 # h is the hour
        self.assertAlmostEqual(U.Q("1 hPa").to("Pa"), 100.0)               # h as the hecto prefix
        self.assertEqual(U.Q("h_planck").kind, "action or angular momentum")
        self.assertAlmostEqual(U.Q("1 g").to("kg"), 1e-3)                  # g is the gram
        self.assertEqual(U.Q("g0").kind, "acceleration")
        self.assertAlmostEqual(U.Q("1 Mt").to("kg"), 1e9)                  # megatonne of mass...
        self.assertEqual(U.Q("1 MtTNT").kind, "energy")                    # ...not of TNT

    def test_dimension_errors(self):
        with self.assertRaises(U.DimensionError):
            U.Q("1 J").to("W")
        with self.assertRaises(U.DimensionError):
            U.Q("1 kg + 1 m")
        with self.assertRaises(U.DimensionError):
            float(U.Q("2 m"))
        self.assertIs(U.Q("5 kW h").expect("energy").kind, "energy")
        with self.assertRaises(KeyError):
            U.Q("3 furlongs")
        with self.assertRaises(ValueError):
            U.Q("3 km)")

    def test_cli(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = U.main(["G*Msun/c^2", "--to", "km", "--expect", "length"])
        self.assertEqual(code, 0)
        self.assertIn("1.47663 km", buf.getvalue())
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(U.main(["1 J", "--to", "W"]), 1)


class Rockets(unittest.TestCase):
    def test_photon_rocket_identities(self):
        for beta in (0.1, 0.5, 0.9, 0.999):
            self.assertAlmostEqual(R.relativistic_mass_ratio(R.C, beta * R.C), R.photon_rocket_mass_ratio(beta), places=9)

    def test_trip_profiles(self):
        flip = R.trip(4.37 * R.LY, R.G0, v_exhaust=R.C)
        self.assertIn("midpoint", flip["profile"])
        self.assertGreater(flip["earth_years"], flip["ship_years"])
        self.assertAlmostEqual(flip["mass_ratio"], math.exp(flip["rapidity_change"]), places=9)
        # a cruise speed above the flip-and-burn peak falls back to flip-and-burn
        self.assertEqual(R.trip(4.37 * R.LY, R.G0, cruise_beta=0.99)["profile"], flip["profile"])
        cruise = R.trip(4.37 * R.LY, 0.1 * R.G0, cruise_beta=0.2, v_exhaust=0.05 * R.C)
        self.assertIn("coast", cruise["profile"])
        self.assertAlmostEqual(cruise["peak_beta"], 0.2, places=12)
        self.assertGreater(cruise["earth_years"], 4.37 / 0.2)          # slower than coasting all the way
        self.assertNotIn("propellant_energy_per_kg_payload_J", cruise)  # only defined for the photon rocket

    def test_hyperbolic_inverses(self):
        ref = R.hyperbolic(R.G0, tau=3 * R.YEAR)
        for key in ("t", "x", "beta"):
            self.assertAlmostEqual(R.hyperbolic(R.G0, **{key: ref[key]})["tau"] / ref["tau"], 1.0, places=9)

    def test_invalid_inputs(self):
        for bad in (lambda: R.gamma(1.0), lambda: R.hyperbolic(-1.0, tau=1.0), lambda: R.hyperbolic(1.0),
                    lambda: R.trip(-1.0, R.G0), lambda: R.mass_ratio_for_rapidity(2 * R.C, 1.0)):
            with self.assertRaises(ValueError):
                bad()

    def test_cli_uses_units(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = R.main(["trip", "--distance", "4.37 ly", "--accel", "1 g0", "--ve", "c"])
        self.assertEqual(code, 0)
        self.assertIn("mass ratio", buf.getvalue())
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(R.main(["trip", "--distance", "4.37 ly", "--accel", "1 J"]), 1)


class ToolkitSelftests(unittest.TestCase):
    """Every calculator in the toolkit that defines selftest() must pass it, including promoted ones."""

    def test_all_selftests_pass(self):
        found = []
        for path in sorted(SCRIPTS.glob("*.py")):
            module = importlib.import_module(path.stem)
            if hasattr(module, "selftest"):
                found.append(path.stem)
                with self.subTest(tool=path.stem), contextlib.redirect_stdout(io.StringIO()):
                    self.assertTrue(module.selftest(verbose=False))
        self.assertTrue({"gr_tensors", "stats_tools", "unit_tools", "rocket_tools"} <= set(found), found)


if __name__ == "__main__":
    unittest.main()
