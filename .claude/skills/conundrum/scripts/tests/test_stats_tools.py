"""Tests for stats_tools.py against independent references (mpmath ships with sympy).

Run from the project root:
    python3 -m unittest discover -s .claude/skills/conundrum/scripts/tests -v
"""
import math
import os
import sys
import unittest

import mpmath as mp

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import stats_tools as S  # noqa: E402

mp.mp.dps = 40


class AgainstMpmath(unittest.TestCase):
    def test_gaussian_tails_and_inverse(self):
        for z in (0.1, 1.0, 3.0, 5.0, 8.0, 20.0):
            self.assertAlmostEqual(S.sigma_to_p(z) / float(mp.erfc(z / mp.sqrt(2)) / 2), 1.0, places=11)
        for p in (0.4, 0.05, 2.8665157e-7, 1e-30, 1e-200):
            self.assertAlmostEqual(S.sigma_to_p(S.p_to_sigma(p)) / p, 1.0, places=10)
        self.assertAlmostEqual(S.p_to_sigma(0.05, two_sided=True), 1.959964, places=5)

    def test_poisson_tail(self):
        for n, b in ((1, 0.5), (10, 3.0), (50, 30.0), (400, 300.0), (3, 20.0)):
            ref = float(mp.gammainc(n, 0, b, regularized=True))
            self.assertAlmostEqual(S.poisson_p_value(n, b) / ref, 1.0, places=10, msg=(n, b))
        self.assertEqual(S.poisson_p_value(0, 5.0), 1.0)

    def test_chi2_survival(self):
        for x, k in ((0.5, 3), (3.841459, 1), (20.0, 10), (100.0, 50), (400.0, 300)):
            ref = float(mp.gammainc(k / 2, x / 2, mp.inf, regularized=True))
            self.assertAlmostEqual(S._chi2_sf(x, k) / ref, 1.0, places=10, msg=(x, k))


class Behaviour(unittest.TestCase):
    def test_selftest_passes(self):
        self.assertTrue(S.selftest(verbose=False))

    def test_invalid_p_is_rejected(self):
        for bad in (0.0, 1.0, -0.1):
            with self.assertRaises(ValueError):
                S.p_to_sigma(bad)

    def test_look_elsewhere_raises_p(self):
        p_local = S.sigma_to_p(3.0)
        self.assertAlmostEqual(S.sidak_global_p(p_local, 1), p_local, places=15)
        self.assertAlmostEqual(S.sidak_global_p(1e-9, 1000) / 1e-6, 1.0, places=5)   # ~ n p for small p
        self.assertGreater(S.gross_vitells_global_p(3.0, upcrossings_ref=5.0), p_local)

    def test_asimov_limits(self):
        self.assertAlmostEqual(S.asimov_z(1.0, 1e6), 1e-3, places=6)            # s/sqrt(b) for s << b
        self.assertLess(S.asimov_z(10, 100, sigma_b=10), S.asimov_z(10, 100))  # background uncertainty hurts
        self.assertAlmostEqual(S.asimov_z(10, 100, sigma_b=1e-9), S.asimov_z(10, 100), places=5)

    def test_bayes_helpers_round_trip(self):
        bf = S.min_bayes_factor(0.05)
        self.assertAlmostEqual(bf["max_odds_against_null"], 1 / bf["sellke"])
        prior = S.prior_needed(bf["max_odds_against_null"])
        self.assertAlmostEqual(S.posterior_probability(prior, bf["max_odds_against_null"]), 0.5)
        self.assertLess(bf["gaussian"], bf["sellke"])

    def test_weighted_mean_consistency(self):
        agree = S.weighted_mean([10.0, 10.2, 9.9], [0.2, 0.2, 0.3])
        self.assertEqual(agree["scale_factor"], 1.0)
        clash = S.weighted_mean([1.0, 3.0], [0.5, 0.5])
        self.assertGreater(clash["scale_factor"], 2.0)
        self.assertLess(clash["p_consistent"], 0.01)
        self.assertAlmostEqual(clash["error_scaled"], clash["error"] * clash["scale_factor"])


class Disagreements(unittest.TestCase):
    """The tools an anomaly question needs: tensions, method groups and systematic floors."""

    def test_tension_matches_an_independent_gaussian_tail(self):
        t = S.tension(888.1, 2.0, 877.8, 0.3)
        z = 10.3 / math.sqrt(2.0**2 + 0.3**2)
        self.assertAlmostEqual(t["z"], z, places=12)
        self.assertAlmostEqual(t["p_two_sided"] / float(mp.erfc(z / mp.sqrt(2))), 1.0, places=10)
        self.assertAlmostEqual(t["difference"], 10.3, places=12)
        # Symmetric in its arguments, and the side of an asymmetric error that faces the other value is used.
        self.assertAlmostEqual(S.tension(877.8, 0.3, 888.1, 2.0)["z"], t["z"], places=12)
        jparc = S.total_error(1.7, (4.0, 3.6))
        above = S.tension(877.2, jparc, 887.7, 2.2)["sigma"]
        below = S.tension(877.2, jparc, 870.0, 2.2)["sigma"]
        self.assertAlmostEqual(above, math.hypot(jparc[0], 2.2), places=12)
        self.assertAlmostEqual(below, math.hypot(jparc[1], 2.2), places=12)
        with self.assertRaises(ValueError):
            S.tension(1.0, 0.0, 2.0, 0.0)

    def test_total_error_keeps_symmetric_inputs_symmetric(self):
        self.assertAlmostEqual(S.total_error(3.0, 4.0), 5.0, places=12)
        self.assertIsInstance(S.total_error(3.0, 4.0), float)
        self.assertEqual(len(S.total_error(3.0, (4.0, 0.0))), 2)

    def test_grouped_chi2_splits_the_pooled_chi2_exactly(self):
        beam = ([887.7, 888.4, 889.2], [2.2, 2.9, 4.8])
        bottle = ([877.75, 878.5, 877.7, 880.2], [0.33, 0.8, 0.7, 1.2])
        g = S.grouped_chi2({"beam": beam, "bottle": bottle})
        self.assertAlmostEqual(g["within_chi2"] + g["between_chi2"], g["pooled"]["chi2"], places=9)
        self.assertEqual(g["within_dof"] + g["between_dof"], g["pooled"]["dof"])
        # Between two groups the between-group chi2 is the squared tension of the group means.
        t = S.tension(g["groups"]["beam"]["mean"], g["groups"]["beam"]["error"],
                      g["groups"]["bottle"]["mean"], g["groups"]["bottle"]["error"])
        self.assertAlmostEqual(g["between_chi2"], t["z"] ** 2, places=9)
        self.assertAlmostEqual(g["between_z"], t["z"], places=6)
        ref = float(mp.gammainc(0.5, g["between_chi2"] / 2, mp.inf, regularized=True))
        self.assertAlmostEqual(g["p_between"] / ref, 1.0, places=9)
        with self.assertRaises(ValueError):
            S.grouped_chi2({"only": beam})

    def test_exposure_with_a_systematic_floor(self):
        # No floor: the old statistics-only answer.
        self.assertAlmostEqual(S.exposure_to_reach(2.0), 6.25, places=12)
        self.assertAlmostEqual(S.exposure_to_reach(delta=4.0, sigma_stat=2.0), 6.25, places=12)
        # With a floor: the answer reaches the target exactly, and is dearer than without it.
        k = S.exposure_to_reach(delta=10.3, sigma_stat=1.7, sigma_sys=1.0, sigma_other=0.3)
        self.assertAlmostEqual(S.z_after_exposure(10.3, 1.7, 1.0, k, sigma_other=0.3), 5.0, places=9)
        self.assertGreater(k, S.exposure_to_reach(delta=10.3, sigma_stat=1.7))
        # Above the ceiling delta / sqrt(sys^2 + other^2), no amount of data is enough.
        self.assertEqual(S.exposure_to_reach(delta=10.3, sigma_stat=1.7, sigma_sys=4.0), math.inf)
        self.assertLess(S.z_after_exposure(10.3, 1.7, 4.0, 1e12), 5.0)
        self.assertAlmostEqual(S.precision_needed(10.3, 5.0), 2.06, places=12)
        with self.assertRaises(ValueError):
            S.exposure_to_reach(delta=10.0, sigma_sys=1.0)
        with self.assertRaises(ValueError):
            S.exposure_to_reach()


class DisagreementEdgeCases(unittest.TestCase):
    def test_grouped_chi2_accepts_iterators(self):
        as_lists = S.grouped_chi2({"a": ([1.0, 3.0], [1.0, 1.0]), "b": ([5.0], [1.0])})
        as_iters = S.grouped_chi2({"a": (iter([1.0, 3.0]), iter([1.0, 1.0])), "b": (iter([5.0]), iter([1.0]))})
        self.assertEqual(as_iters["groups"]["a"]["n"], 2)
        self.assertAlmostEqual(as_iters["between_chi2"], as_lists["between_chi2"], places=12)
        self.assertAlmostEqual(as_iters["pooled"]["mean"], as_lists["pooled"]["mean"], places=12)

    def test_between_z_stays_finite_far_out_in_the_tail(self):
        two = S.grouped_chi2({"a": ([0.0], [1.0]), "b": ([60.0], [1.0])})
        self.assertAlmostEqual(two["between_z"], math.sqrt(two["between_chi2"]), places=9)   # 60 / sqrt(2)
        # Three groups: 2 degrees of freedom, a p-value of about e^-3600, far below the smallest float.
        three = S.grouped_chi2({"a": ([0.0], [1.0]), "b": ([60.0], [1.0]), "c": ([120.0], [1.0])})
        self.assertEqual(three["p_between"], 0.0)
        log_p = mp.log(mp.gammainc(1, three["between_chi2"] / 2, mp.inf, regularized=True))
        exact = mp.findroot(lambda z: mp.log(mp.erfc(z / mp.sqrt(2))) - log_p, 80)
        self.assertAlmostEqual(three["between_z"] / float(exact), 1.0, places=6)
        for k, x in ((3, 3000.0), (7, 5000.0)):   # the tail formula against mpmath at other dof
            ref = float(mp.log(mp.gammainc(k / 2, x / 2, mp.inf, regularized=True)))
            self.assertAlmostEqual(S._log_chi2_sf_tail(x, k) / ref, 1.0, places=5)

    def test_asymmetric_errors_are_refused_where_they_cannot_be_used(self):
        with self.assertRaisesRegex(ValueError, "symmetric errors"):
            S.weighted_mean([877.75, 878.5], [S.total_error(0.28, (0.22, 0.16)), 0.8])
        with self.assertRaisesRegex(ValueError, "separate arguments"):
            S.total_error([1.7, 4.0])



if __name__ == "__main__":
    unittest.main()
