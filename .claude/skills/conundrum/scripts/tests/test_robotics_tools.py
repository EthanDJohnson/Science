"""Tests for rigid_body.py and control_tools.py, the dynamics-and-control calculators.

The modules' own selftest() functions check them against published equations and closed
forms, and test_calculators.py runs every selftest in the toolkit. These tests cover what a
selftest does not: the API contracts, the errors the modules must refuse, and one end-to-end
closed-loop run (Acrobot swing-up handing over to an LQR balance controller) that exercises
both modules together the way a run's simulator lens would.

Run from the project root:
    python3 -m unittest discover -s .claude/skills/conundrum/scripts/tests -v
"""
import math
import os
import sys
import unittest

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import control_tools as C  # noqa: E402
import rigid_body as RB  # noqa: E402


def wrap(a):
    return (a + math.pi) % (2 * math.pi) - math.pi


def state_error(x, x_star):
    """Error with the first two coordinates treated as angles on a circle."""
    x, x_star = np.asarray(x, dtype=float), np.asarray(x_star, dtype=float)
    return np.concatenate([wrap(x[:2] - x_star[:2]), x[2:] - x_star[2:]])


class LinkConventions(unittest.TestCase):
    def test_inertia_is_about_the_centre_of_mass(self):
        rod = RB.Link.rod(mass=3.0, length=2.0)
        self.assertAlmostEqual(rod.com, 1.0)
        self.assertAlmostEqual(rod.izz, 3.0 * 4.0 / 12.0)
        self.assertAlmostEqual(rod.izz_pivot, 3.0 * 4.0 / 3.0)
        point = RB.Link.point_mass(mass=2.0, length=1.5)
        self.assertAlmostEqual(point.izz, 0.0)
        self.assertAlmostEqual(point.izz_pivot, 2.0 * 1.5 ** 2)

    def test_from_pivot_inertia_round_trips(self):
        lk = RB.Link.from_pivot_inertia(mass=2.0, length=1.0, com=0.4, izz_pivot=0.5)
        self.assertAlmostEqual(lk.izz_pivot, 0.5)
        self.assertAlmostEqual(lk.izz, 0.5 - 2.0 * 0.16)

    def test_impossible_values_are_refused(self):
        with self.assertRaises(ValueError):
            RB.Link(mass=-1.0, length=1.0, com=0.5, izz=0.1)
        with self.assertRaises(ValueError):
            RB.Link(mass=1.0, length=1.0, com=-0.5, izz=0.1)
        with self.assertRaises(ValueError):      # below the parallel-axis floor m d^2
            RB.Link.from_pivot_inertia(mass=1.0, length=1.0, com=0.5, izz_pivot=0.2)


class ChainProperties(unittest.TestCase):
    def setUp(self):
        self.ch = RB.acrobot()

    def test_mass_matrix_is_symmetric_positive_definite(self):
        rng = np.random.default_rng(0)
        for q in rng.uniform(-math.pi, math.pi, (20, 2)):
            M = self.ch.mass_matrix(q)
            self.assertLess(float(np.max(np.abs(M - M.T))), 1e-12)
            self.assertGreater(float(np.min(np.linalg.eigvalsh(M))), 0.0)

    def test_geometry(self):
        pts = self.ch.joint_positions([0.0, 0.0])          # hanging straight down
        np.testing.assert_allclose(pts[0], [0.0, 0.0], atol=1e-12)
        np.testing.assert_allclose(pts[1], [0.0, -1.0], atol=1e-12)
        np.testing.assert_allclose(pts[2], [0.0, -2.0], atol=1e-12)
        pts = self.ch.joint_positions([math.pi, 0.0])       # straight up
        np.testing.assert_allclose(pts[2], [0.0, 2.0], atol=1e-12)
        # q is relative: bending the elbow by pi folds link 2 back onto link 1
        pts = self.ch.joint_positions([0.0, math.pi])
        np.testing.assert_allclose(pts[2], [0.0, 0.0], atol=1e-12)

    def test_energy_at_the_two_equilibria(self):
        hanging = self.ch.energy([0.0, 0.0], [0.0, 0.0])
        self.assertAlmostEqual(hanging, -self.ch.upright_energy(), places=9)
        self.assertGreater(self.ch.upright_energy(), 0.0)
        # kinetic energy is positive for any non-zero velocity
        self.assertGreater(self.ch.kinetic([0.3, 0.4], [1.0, -2.0]), 0.0)

    def test_wrong_shapes_are_refused(self):
        with self.assertRaises(ValueError):
            self.ch.mass_matrix([0.0])
        with self.assertRaises(ValueError):
            self.ch.coriolis([0.0, 0.0], [0.0])
        with self.assertRaises(ValueError):
            self.ch.forward_dynamics([0.0, 0.0], [0.0, 0.0], [0.0, 0.0])   # one actuator
        with self.assertRaises(ValueError):
            RB.Chain([], gravity=9.81)

    def test_actuation_matrix_follows_the_links(self):
        self.assertEqual(self.ch.m_actuated, 1)
        np.testing.assert_allclose(self.ch.B, [[0.0], [1.0]])
        both = RB.double_pendulum()
        self.assertEqual(both.m_actuated, 2)
        np.testing.assert_allclose(both.B, np.eye(2))

    def test_equilibrium_torque_refuses_an_unholdable_pose(self):
        # The Acrobot's shoulder is passive, so only poses with the first link vertical can
        # be held. Returning a least-squares "nearly" would be the dangerous answer.
        np.testing.assert_allclose(self.ch.equilibrium_torque([math.pi, 0.0]),
                                   [0.0], atol=1e-9)
        with self.assertRaises(ValueError):
            self.ch.equilibrium_torque([0.5, 0.0])

    def test_cart_pole_is_refused_rather_than_approximated(self):
        with self.assertRaises(NotImplementedError):
            RB.cartpole_chain()


class ModelChecks(unittest.TestCase):
    def test_passivity_identity_holds(self):
        ch = RB.acrobot()
        rng = np.random.default_rng(1)
        for q, v in zip(rng.uniform(-3, 3, (10, 2)), rng.uniform(-3, 3, (10, 2))):
            self.assertLess(ch.passivity_residual(q, v), 1e-5)

    def test_energy_is_conserved_without_damping_and_lost_with_it(self):
        ch = RB.acrobot()
        free = RB.simulate(ch, lambda t, x: [0.0], [0.7, -0.4, 0.0, 0.0], 10.0, 1e-3)
        self.assertLess(free.energy_drift, 1e-9)
        damped = RB.acrobot(damping=0.5)
        lossy = RB.simulate(damped, lambda t, x: [0.0], [0.7, -0.4, 0.0, 0.0], 10.0, 1e-3)
        self.assertLess(lossy.energy[-1], lossy.energy[0] - 1e-2)

    def test_rk4_converges_at_fourth_order(self):
        ch = RB.acrobot()
        conv = RB.convergence_order(ch, [0.7, -0.4, 0.0, 0.0], 2.0, 4e-3)
        self.assertGreater(conv["order"], 3.5)
        self.assertLess(conv["order"], 4.6)
        self.assertLess(conv["errors"][-1], conv["errors"][0])

    def test_cross_check_separates_agreement_from_disagreement(self):
        ch = RB.acrobot()
        rng = np.random.default_rng(2)
        states = rng.uniform(-2, 2, (15, 4))
        zeros = [np.zeros(1) for _ in states]
        same = RB.cross_check(ch.state_dynamics(), ch.state_dynamics_reference(),
                              states, zeros)
        self.assertLess(same["max_rel"], 1e-7)
        worse = RB.cross_check(ch.state_dynamics(), RB.acrobot(m2=1.2).state_dynamics(),
                               states, zeros)
        self.assertGreater(worse["max_rel"], 1e-3)
        self.assertIsNotNone(worse["worst_state"])

    def test_compiled_and_reference_paths_agree(self):
        fast = RB.acrobot()
        slow = RB.Chain(fast.links, gravity=fast.gravity, compile=False)
        for q, v in [([0.3, -0.7], [1.1, -0.4]), ([2.0, 1.0], [-2.0, 0.5])]:
            np.testing.assert_allclose(fast.mass_matrix(q), slow.mass_matrix(q), atol=1e-10)
            np.testing.assert_allclose(fast.coriolis(q, v) @ np.array(v),
                                       slow.coriolis(q, v) @ np.array(v), atol=1e-6)
            np.testing.assert_allclose(fast.gravity_torque(q), slow.gravity_torque(q),
                                       atol=1e-10)


class Simulation(unittest.TestCase):
    def test_torque_limit_clips_and_is_reported(self):
        ch = RB.acrobot()
        traj = RB.simulate(ch, lambda t, x: [100.0], [0.0, 0.0, 0.0, 0.0], 1.0, 1e-3,
                           torque_limit=2.0)
        self.assertLessEqual(float(np.max(np.abs(traj.u))), 2.0 + 1e-12)
        self.assertGreater(traj.saturated_fraction, 0.9)
        free = RB.simulate(ch, lambda t, x: [1.0], [0.0, 0.0, 0.0, 0.0], 1.0, 1e-3,
                           torque_limit=2.0)
        self.assertEqual(free.saturated_fraction, 0.0)

    def test_noise_reaches_the_controller_and_not_the_plant(self):
        ch = RB.acrobot()
        seen = []

        def controller(t, x):
            seen.append(np.array(x, dtype=float))
            return [0.0]
        traj = RB.simulate(ch, controller, [0.0, 0.0, 0.0, 0.0], 0.1, 1e-3,
                           noise={"q": 0.01, "qdot": 0.01}, rng=5)
        # the controller saw corrupted angles ...
        self.assertGreater(float(np.std([s[0] for s in seen])), 1e-3)
        # ... while the plant, with zero torque from rest, never moved
        self.assertLess(float(np.max(np.abs(traj.x))), 1e-12)

    def test_divergence_is_flagged_not_silent(self):
        ch = RB.acrobot()
        traj = RB.simulate(ch, lambda t, x: [1e7 * (1 + x[0] ** 2)],
                           [0.0, 0.0, 0.0, 0.0], 5.0, 1e-2)
        self.assertTrue(traj.diverged)
        self.assertTrue(np.all(np.isfinite(traj.x)))

    def test_stop_condition_ends_the_run_early(self):
        ch = RB.acrobot()
        traj = RB.simulate(ch, lambda t, x: [0.0], [1.0, 0.0, 0.0, 0.0], 10.0, 1e-3,
                           stop=lambda t, x: t > 1.0)
        self.assertLess(traj.t[-1], 1.1)

    def test_bad_inputs_are_refused(self):
        ch = RB.acrobot()
        with self.assertRaises(ValueError):
            RB.simulate(ch, lambda t, x: [0.0], [0.0, 0.0], 1.0, 1e-3)
        with self.assertRaises(ValueError):
            RB.simulate(ch, lambda t, x: [0.0], [0.0] * 4, 1.0, -1e-3)


class Linearisation(unittest.TestCase):
    def test_upright_is_an_equilibrium_and_hanging_is_stable(self):
        ch = RB.acrobot()
        f = ch.state_dynamics()
        A_up, B_up, info_up = C.linearize(f, [math.pi, 0.0, 0.0, 0.0], [0.0])
        self.assertLess(info_up["residual"], 1e-9)
        self.assertEqual(info_up["unstable_modes"], 2)
        A_dn, _, info_dn = C.linearize(f, [0.0, 0.0, 0.0, 0.0], [0.0])
        self.assertLess(info_dn["residual"], 1e-9)
        self.assertEqual(info_dn["unstable_modes"], 0)
        self.assertLess(info_up["step_sensitivity"], 1e-5)

    def test_a_non_equilibrium_point_is_flagged(self):
        ch = RB.acrobot()
        _, _, info = C.linearize(ch.state_dynamics(), [0.7, 0.2, 0.0, 0.0], [0.0])
        self.assertGreater(info["residual"], 1e-3)

    def test_acrobot_is_controllable_at_upright_but_ill_conditioned(self):
        ch = RB.acrobot()
        A, B, _ = C.linearize(ch.state_dynamics(), [math.pi, 0.0, 0.0, 0.0], [0.0])
        ctrb = C.controllability(A, B)
        self.assertTrue(ctrb["controllable"])
        self.assertEqual(ctrb["rank"], 4)
        # one actuator for two degrees of freedom: controllable, and badly conditioned
        self.assertGreater(ctrb["condition"], 100.0)


class Synthesis(unittest.TestCase):
    def test_weight_validation(self):
        A = np.array([[0.0, 1.0], [0.0, 0.0]])
        B = np.array([[0.0], [1.0]])
        with self.assertRaises(ValueError):
            C.lqr(A, B, np.eye(3), np.eye(1))
        with self.assertRaises(ValueError):
            C.lqr(A, B, np.eye(2), np.zeros((1, 1)))        # R must be positive definite
        with self.assertRaises(ValueError):
            C.lqr(A, B, -np.eye(2), np.eye(1))              # Q must be semidefinite
        with self.assertRaises(ValueError):
            C.lqr(A, B, np.eye(2), np.eye(2))               # R has the wrong shape

    def test_scaling_q_and_r_together_leaves_the_gain_alone(self):
        A = np.array([[0.0, 1.0], [2.0, 0.0]])
        B = np.array([[0.0], [1.0]])
        a = C.lqr(A, B, np.eye(2), np.eye(1))
        b = C.lqr(A, B, 1000.0 * np.eye(2), 1000.0 * np.eye(1))
        np.testing.assert_allclose(a["K"], b["K"], rtol=1e-8)

    def test_margins_report_both_sides_of_the_gain_margin(self):
        A = np.array([[0.0, 1.0], [2.0, 0.0]])
        B = np.array([[0.0], [1.0]])
        out = C.lqr(A, B, np.eye(2), np.eye(1))
        m = C.state_feedback_margins(A, B, out["K"])
        self.assertEqual(m["gain_margin_up"], math.inf)
        self.assertLessEqual(m["gain_margin_down"], 0.5 + 1e-9)
        self.assertGreaterEqual(m["phase_margin_deg"], 59.9)
        self.assertGreater(m["delay_margin"], 0.0)

    def test_multi_input_margins_are_refused(self):
        A = np.eye(2) * -1.0
        B = np.eye(2)
        with self.assertRaises(ValueError):
            C.state_feedback_margins(A, B, np.eye(2))

    def test_roa_simulated_needs_an_angle_aware_error(self):
        # A pendulum that always ends upright, reported one turn around. With a plain
        # subtraction that reads as a failure; with a wrapping error it reads as success.
        x_star = np.array([math.pi, 0.0])

        def step(x0, t_end):
            return np.array([math.pi + 2 * math.pi, 0.0])
        plain = C.roa_simulated(step, x_star, [np.array([1.0, 0.0])], 0.01, 1.0)
        self.assertEqual(plain["min"], 0.0)
        aware = C.roa_simulated(
            step, x_star, [np.array([1.0, 0.0])], 0.01, 1.0,
            error=lambda x, s: np.array([wrap(x[0] - s[0]), x[1] - s[1]]))
        self.assertGreater(aware["max"], 0.0)

    def test_sampled_regions_say_they_are_not_certified(self):
        roa = C.roa_sample(lambda x, u: np.array([-x[0] + x[0] ** 3]), [0.0], [[1.0]],
                           rho_max=4.0, samples=20, levels=200)
        self.assertFalse(roa["certified"])
        self.assertIn("not certified", roa["note"])
        self.assertAlmostEqual(roa["rho"], 1.0, delta=0.05)


class RobustnessSweep(unittest.TestCase):
    def test_interval_widens_as_trials_shrink(self):
        few = C.robustness_sweep(lambda p: True, [{"i": i} for i in range(5)])
        many = C.robustness_sweep(lambda p: True, [{"i": i} for i in range(500)])
        self.assertEqual(few["rate"], 1.0)
        self.assertEqual(many["rate"], 1.0)
        self.assertLess(few["interval"][0], many["interval"][0])
        self.assertLess(few["interval"][0], 0.6)      # 5 for 5 proves very little

    def test_failures_are_listed_with_their_conditions(self):
        out = C.robustness_sweep(lambda p: p["m"] < 1.15,
                                 [{"m": m} for m in (0.9, 1.0, 1.1, 1.2, 1.3)])
        self.assertEqual(out["successes"], 3)
        self.assertEqual([f["perturbation"]["m"] for f in out["failures"]], [1.2, 1.3])


class AcrobotEndToEnd(unittest.TestCase):
    """Swing-up to balance on the Acrobot, using both modules as a simulator lens would.

    This is the reproduction target of Spong's energy-based swing-up with partial feedback
    linearisation plus an LQR catch. It is a regression test on the toolkit, not a claim
    about Spong's own parameters: the plant here is two uniform rods (1 m and 2 m).
    """

    @classmethod
    def setUpClass(cls):
        cls.ch = RB.acrobot(l2=2.0, lc2=1.0, I2=4.0 / 12.0)
        cls.x_up = np.array([math.pi, 0.0, 0.0, 0.0])
        A, B, info = C.linearize(cls.ch.state_dynamics(), cls.x_up, np.zeros(1))
        cls.A, cls.B, cls.info = A, B, info
        cls.out = C.lqr(A, B, np.diag([10.0, 10.0, 1.0, 1.0]), np.eye(1))

    def controller(self, rho=8.0, alpha=1.6, ke=0.035, k1=250.0, limit=None):
        """Spong swing-up with a collocated-PFL inner loop, handing over to LQR."""
        ch, x_up = self.ch, self.x_up
        K, S = self.out["K"], self.out["S"]
        E_d = ch.upright_energy()
        k2 = 2.0 * math.sqrt(k1)
        state = {"mode": "swingup", "t_switch": None}

        def u(t, x):
            e = state_error(x, x_up)
            if state["mode"] == "swingup" and float(e @ S @ e) < rho:
                state["mode"], state["t_switch"] = "lqr", t
            if state["mode"] == "lqr":
                return -K @ e
            q, qd = x[:2], x[2:]
            M = ch.mass_matrix(q)
            bias = ch.gravity_torque(q) - ch.coriolis(q, qd) @ qd
            e_tilde = ch.energy(q, qd) - E_d
            q2_ref = -(2 * alpha / math.pi) * math.atan(ke * qd[0] * e_tilde)
            qdd2 = -k1 * (wrap(q[1]) - q2_ref) - k2 * qd[1]
            return np.array([(M[1, 1] - M[1, 0] * M[0, 1] / M[0, 0]) * qdd2
                             - bias[1] + M[1, 0] / M[0, 0] * bias[0]])
        return u, state

    def test_upright_is_unstable_and_the_lqr_stabilises_it(self):
        self.assertEqual(self.info["unstable_modes"], 2)
        self.assertTrue(self.out["stable"])
        self.assertLess(self.out["are_residual"], 1e-7)

    def test_the_balance_basin_is_small_and_has_a_sharp_edge(self):
        """The measured region of attraction, and that it is an edge rather than a fade."""
        K = self.out["K"]

        def step(x0, t_end):
            return RB.simulate(self.ch, lambda t, x: -K @ state_error(x, self.x_up),
                               x0, t_end, 2e-3).x[-1]
        roa = C.roa_simulated(step, self.x_up,
                              [np.array([1.0, 0.0, 0.0, 0.0]),
                               np.array([0.0, 1.0, 0.0, 0.0])],
                              tolerance=0.02, t_end=6.0, bracket=(1e-3, 1.0),
                              error=state_error)
        shoulder = roa["per_direction"][0]["alpha"]
        self.assertGreater(shoulder, 0.005)      # a basin exists
        self.assertLess(shoulder, 0.5)           # and it is narrow: degrees, not radians
        # the elbow direction tolerates more than the shoulder direction
        self.assertGreater(roa["per_direction"][1]["alpha"], shoulder)
        # sharp edge: just inside recovers, well outside diverges
        inside = step(self.x_up + 0.9 * shoulder * np.array([1.0, 0, 0, 0]), 6.0)
        outside = step(self.x_up + 3.0 * shoulder * np.array([1.0, 0, 0, 0]), 6.0)
        self.assertLess(float(np.max(np.abs(state_error(inside, self.x_up)))), 0.02)
        self.assertGreater(float(np.max(np.abs(state_error(outside, self.x_up)))), 0.5)

    def test_energy_pumping_raises_the_energy_towards_the_upright_value(self):
        u, _ = self.controller(rho=0.0)          # never hand over; pump only
        traj = RB.simulate(self.ch, u, [0.05, 0.0, 0.0, 0.0], 50.0, 4e-3)
        E_d = self.ch.upright_energy()
        self.assertLess(traj.energy[0], -0.9 * E_d)            # starts near hanging
        self.assertGreater(float(traj.energy.max()), 0.98 * E_d)   # reaches the target
        self.assertFalse(traj.diverged)

    def test_swing_up_hands_over_to_lqr_and_balances(self):
        u, state = self.controller()
        traj = RB.simulate(self.ch, u, [0.05, 0.0, 0.0, 0.0], 60.0, 4e-3)
        self.assertEqual(state["mode"], "lqr", "the swing-up never entered the LQR basin")
        self.assertIsNotNone(state["t_switch"])
        self.assertLess(state["t_switch"], 60.0)
        final = float(np.max(np.abs(state_error(traj.x[-1], self.x_up))))
        self.assertLess(final, 1e-6, f"balanced to only {final} rad")
        self.assertFalse(traj.diverged)

    def test_the_handover_time_does_not_depend_on_the_step_size(self):
        """A result that moves with the integrator step is an artefact, not a result."""
        times = []
        for dt in (4e-3, 1e-3):
            u, state = self.controller()
            RB.simulate(self.ch, u, [0.05, 0.0, 0.0, 0.0], 60.0, dt)
            times.append(state["t_switch"])
        self.assertIsNotNone(times[0])
        self.assertIsNotNone(times[1])
        self.assertAlmostEqual(times[0], times[1], delta=0.05)

    def test_a_torque_limit_below_the_demand_breaks_the_swing_up(self):
        """The peak torque the swing-up needs is a real requirement, not a preference."""
        u, state = self.controller()
        traj = RB.simulate(self.ch, u, [0.05, 0.0, 0.0, 0.0], 60.0, 4e-3)
        peak = float(np.max(np.abs(traj.u)))
        self.assertGreater(peak, 5.0)
        tight, tight_state = self.controller()
        limited = RB.simulate(self.ch, tight, [0.05, 0.0, 0.0, 0.0], 60.0, 4e-3,
                              torque_limit=0.2 * peak)
        self.assertGreater(limited.saturated_fraction, 0.0)
        self.assertNotEqual(tight_state["mode"], "lqr")


if __name__ == "__main__":
    unittest.main()
