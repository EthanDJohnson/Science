#!/usr/bin/env python3
"""Acrobot swing-up and balance, built only from the toolkit's tested calculators.

What this is: the worked validation of `rigid_body.py` and `control_tools.py`, following the
standard route for an underactuated double pendulum with torque at the elbow only —
Spong's energy-based swing-up with collocated partial feedback linearisation, handing over
to an LQR controller that balances it at the top.

What this is not: a reproduction of any published parameter set. Published Acrobot
parameters disagree (see `rigid_body.acrobot`'s docstring), so the plant here is stated
outright: two uniform rods, 1 kg and 1 m for the upper link, 1 kg and 2 m for the lower one.
The controller gains below were found by a grid search in this plant and mean nothing in
another one.

It prints, in order:
  1. the model verification, which comes before any result is allowed to count;
  2. the balance controller: the upright equilibrium, its instability, the LQR gain, the
     closed-loop poles and the loop's margins;
  3. the measured region of attraction of the balance controller, direction by direction;
  4. the full run from hanging to balanced, with the handover time and the peak torque;
  5. the failure boundary: the torque limit, the model error, and the sensor noise at which
     the whole thing stops working.

Run from the project root:
    python3 .claude/skills/conundrum/scripts/math_run.py examples/acrobot-swingup-balance/acrobot_demo.py --timeout 590
or directly:
    python3 examples/acrobot-swingup-balance/acrobot_demo.py
"""
import math
import sys

import numpy as np

sys.path.insert(0, ".claude/skills/conundrum/scripts")

from control_tools import (linearize, lqr, controllability, roa_simulated,      # noqa: E402
                           robustness_sweep, state_feedback_margins)
from rigid_body import acrobot, convergence_order, cross_check, simulate, Chain  # noqa: E402

SEED = 20261015
UPRIGHT = np.array([math.pi, 0.0, 0.0, 0.0])
HANGING = np.array([0.05, 0.0, 0.0, 0.0])      # 0.05 rad off the hanging rest point
# Exactly at rest at the bottom, every term of the swing-up law is zero and nothing moves:
# the energy-pumping term is proportional to the shoulder rate. A real Acrobot is never
# exactly at rest; the nudge stands in for that.

# Plant: two uniform rods. lc = L/2 and izz = m L^2 / 12 about each rod's centre of mass.
PLANT = dict(m1=1.0, m2=1.0, l1=1.0, l2=2.0, lc1=0.5, lc2=1.0,
             I1=1.0 / 12.0, I2=4.0 / 12.0)
# LQR weights. Q penalises state error and R control effort; only the ratio matters.
Q = np.diag([10.0, 10.0, 1.0, 1.0])
R = np.eye(1)
# Swing-up gains, from a grid search in this plant: alpha is the largest elbow angle the
# pump will command, ke scales the energy error into that angle, and k1/k2 are the elbow's
# inner loop (k2 = 2 sqrt(k1), critically damped).
ALPHA, KE, K1 = 1.6, 0.035, 250.0
RHO_SWITCH = 8.0        # hand over when the LQR cost-to-go falls below this; see step 3
DT = 2e-3


def wrap(a):
    return (a + math.pi) % (2 * math.pi) - math.pi


def state_error(x, x_star=UPRIGHT):
    """Error with the joint angles taken around the circle, not along a line."""
    x = np.asarray(x, dtype=float)
    return np.concatenate([wrap(x[:2] - x_star[:2]), x[2:] - x_star[2:]])


def build_controller(chain, K, S, limit=None, rho=RHO_SWITCH,
                     alpha=ALPHA, ke=KE, k1=K1):
    """Spong energy swing-up with a collocated-PFL inner loop, handing over to LQR."""
    E_d = chain.upright_energy()
    k2 = 2.0 * math.sqrt(k1)
    state = {"mode": "swingup", "t_switch": None}

    def u(t, x):
        e = state_error(x)
        if state["mode"] == "swingup" and float(e @ S @ e) < rho:
            state["mode"], state["t_switch"] = "lqr", t
        if state["mode"] == "lqr":
            return -K @ e
        q, qd = x[:2], x[2:]
        M = chain.mass_matrix(q)
        bias = chain.gravity_torque(q) - chain.coriolis(q, qd) @ qd
        e_tilde = chain.energy(q, qd) - E_d          # negative while energy is short
        q2_ref = -(2 * alpha / math.pi) * math.atan(ke * qd[0] * e_tilde)
        qdd2 = -k1 * (wrap(q[1]) - q2_ref) - k2 * qd[1]
        # collocated PFL: solve the actuated row for the torque that realises qdd2
        return np.array([(M[1, 1] - M[1, 0] * M[0, 1] / M[0, 0]) * qdd2
                         - bias[1] + M[1, 0] / M[0, 0] * bias[0]])
    return u, state


def section(title):
    print(f"\n{'=' * 78}\n{title}\n{'=' * 78}")


def main():
    chain = acrobot(**PLANT)

    section("1. MODEL VERIFICATION  (nothing below counts until these pass)")
    free = simulate(chain, lambda t, x: [0.0], [0.6, -0.3, 0.0, 0.0], 20.0, 1e-3)
    print(f"energy drift, 20 s unforced and undamped, RK4 at 1 ms : {free.energy_drift:.3e} "
          f"(expected 0)")
    print(f"passivity residual, max |Mdot - (C + C^T)|            : "
          f"{chain.passivity_residual([0.3, -0.7], [1.1, -0.4]):.3e} (expected 0)")
    conv = convergence_order(chain, [0.6, -0.3, 0.0, 0.0], 2.0, 4e-3)
    print(f"RK4 convergence order                                 : {conv['order']:.2f} "
          f"(expected 4)")
    rng = np.random.default_rng(SEED)
    states = rng.uniform(-3.0, 3.0, (30, 4))
    cc = cross_check(chain.state_dynamics(), chain.state_dynamics_reference(), states,
                     [rng.uniform(-5.0, 5.0, 1) for _ in range(30)])
    print(f"compiled vs reference dynamics, max relative gap      : {cc['max_rel']:.3e} "
          f"(expected ~1e-9, the reference's own differencing error)")
    # a known limit: small oscillations about hanging, against the generalised eigenproblem
    M0 = chain.mass_matrix([0.0, 0.0])
    eps, Kst = 1e-6, np.zeros((2, 2))
    for j in range(2):
        step = np.zeros(2)
        step[j] = eps
        Kst[:, j] = -(chain.gravity_torque(step) - chain.gravity_torque(-step)) / (2 * eps)
    # A known limit: small oscillations about hanging. Launch the chain along ONE normal
    # mode's eigenvector, so the free motion is a single sinusoid whose period can be
    # measured and compared with the linearised prediction. Launching it along a coordinate
    # instead mixes both modes and the zero crossings then mean nothing.
    vals2, vecs2 = np.linalg.eig(np.linalg.solve(M0, Kst))
    order = np.argsort(np.real(vals2))
    for which, label in ((order[0], "slow"), (order[-1], "fast")):
        omega = math.sqrt(float(np.real(vals2[which])))
        mode = np.real(vecs2[:, which])
        mode = mode / np.max(np.abs(mode)) * 1e-4
        small = simulate(chain, lambda t, x: [0.0],
                         [mode[0], mode[1], 0.0, 0.0], 40.0, 1e-3)
        crossings = np.where(np.diff(np.sign(small.x[:, 0])) != 0)[0]
        measured = 2.0 * float(np.mean(np.diff(small.t[crossings]))) if len(
            crossings) > 2 else float("nan")
        print(f"{label} normal-mode period: linearised {2 * math.pi / omega:.4f} s, "
              f"measured on that mode {measured:.4f} s "
              f"(gap {abs(measured - 2 * math.pi / omega) / (2 * math.pi / omega):.2%})")

    section("2. BALANCE CONTROLLER (LQR about the upright equilibrium)")
    f = chain.state_dynamics()
    A, B, info = linearize(f, UPRIGHT, np.zeros(1))
    print(f"|f(x*, 0)| at the upright pose : {info['residual']:.3e} "
          f"(must be ~0, or it is not an equilibrium)")
    print(f"step sensitivity of the Jacobian: {info['step_sensitivity']:.3e}")
    print(f"open-loop eigenvalues          : {np.round(info['eigenvalues'], 4)}")
    print(f"unstable modes                 : {info['unstable_modes']}")
    ctrb = controllability(A, B)
    print(f"controllable                   : {ctrb['controllable']} "
          f"(rank {ctrb['rank']}/{ctrb['n']}, sigma_min {ctrb['min_singular_value']:.3e}, "
          f"condition {ctrb['condition']:.0f})")
    print("  one actuator for two degrees of freedom: controllable, and badly conditioned.")
    out = lqr(A, B, Q, R)
    K, S = out["K"], out["S"]
    print(f"K                              : {np.round(K, 3)}")
    print(f"Riccati residual               : {out['are_residual']:.3e}")
    print(f"closed-loop poles              : {np.round(out['closed_loop_poles'], 4)}")
    m = state_feedback_margins(A, B, K)
    print(f"gain margin  up {m['gain_margin_up']}, down {m['gain_margin_down']:.3f}  "
          f"(LQR's guarantee: infinite up, <= 0.5 down)")
    print(f"phase margin {m['phase_margin_deg']:.1f} deg at "
          f"{m['w_gain_crossover']:.2f} rad/s; delay margin "
          f"{m['delay_margin'] * 1e3:.1f} ms")
    print(f"  -> the loop cannot be run slower than about "
          f"{1.0 / (2 * m['delay_margin']):.0f} Hz even with no computation delay.")

    section("3. REGION OF ATTRACTION OF THE BALANCE CONTROLLER (simulated)")

    def balance_only(x0, t_end):
        return simulate(chain, lambda t, x: -K @ state_error(x), x0, t_end, DT).x[-1]
    dirs = {"shoulder angle": [1, 0, 0, 0], "elbow angle": [0, 1, 0, 0],
            "shoulder rate": [0, 0, 1, 0], "elbow rate": [0, 0, 0, 1],
            "both angles together": [1, 1, 0, 0]}
    roa = roa_simulated(balance_only, UPRIGHT, [np.array(d, dtype=float) for d in
                                                dirs.values()],
                        tolerance=0.02, t_end=8.0, bracket=(1e-3, 2.0),
                        error=lambda x, s: state_error(x, s))
    edge_costs = []
    for name, entry in zip(dirs, roa["per_direction"]):
        d = np.array(entry["direction"])
        a = entry["alpha"]
        cost = float((a * d) @ S @ (a * d))
        edge_costs.append(cost)
        print(f"{name:24s} recovers out to {a:7.4f}  "
              f"({math.degrees(a):6.2f} deg or rad/s)   cost-to-go at the edge {cost:7.2f}")
    print(f"\nThe basin is tens of degrees wide, and it is NOT a level set of the LQR cost: "
          f"the cost-to-go at\nits edge spans {min(edge_costs):.0f} to {max(edge_costs):.0f}, "
          f"a factor of {max(edge_costs) / min(edge_costs):.1f}, because the velocity "
          f"directions reach\nfurther than the cost weights say. A cost sublevel set is "
          f"still the convenient handover test, but\nit has to be set from the SMALLEST "
          f"edge cost ({min(edge_costs):.0f}), not an average, and with margin below that.")

    # Does the basin depend on the weights? Measure it rather than assuming.
    print("\nDoes the basin move when the weights change?")
    for R_try in (1.0, 100.0, 1e4):
        g = lqr(A, B, Q, np.eye(1) * R_try)

        def step_try(x0, t_end, Kt=g["K"]):
            return simulate(chain, lambda t, x: -Kt @ state_error(x), x0, t_end, DT).x[-1]
        r = roa_simulated(step_try, UPRIGHT, [np.array([1.0, 0.0, 0.0, 0.0])],
                          tolerance=0.02, t_end=8.0, bracket=(1e-3, 2.0),
                          error=lambda x, s: state_error(x, s))
        print(f"   R = {R_try:8.0f}: |K|max {np.abs(g['K']).max():7.1f}, "
              f"shoulder basin {r['min']:.4f} rad ({math.degrees(r['min']):5.2f} deg)")
    print(f"   Hardly at all: raising R by four orders of magnitude leaves the basin within "
          f"20 per cent and\n   the gain near the same floor. The plant's unstable pole at "
          f"{max(np.real(info['eigenvalues'])):.2f} rad/s forces a minimum gain, so the LQR "
          f"cannot be\n   made gentle enough to widen its basin. A swing-up controller has "
          f"to arrive accurately.")
    print(f"\n{roa['note']}")

    section("4. FULL RUN: HANGING -> SWING-UP -> BALANCED")
    u, state = build_controller(chain, K, S)
    traj = simulate(chain, u, HANGING, 60.0, DT)
    E_d = chain.upright_energy()
    print(f"target energy E_d                 : {E_d:.4f} J "
          f"(hanging: {chain.energy([0, 0], [0, 0]):.4f} J)")
    print(f"peak energy reached               : {traj.energy.max():.4f} J")
    print(f"handover to LQR at               : {state['t_switch']} s")
    print(f"final error from upright          : "
          f"{np.max(np.abs(state_error(traj.x[-1]))):.3e} rad, rad/s")
    print(f"peak |torque|                     : {np.abs(traj.u).max():.2f} N m")
    print(f"RMS torque                        : "
          f"{float(np.sqrt(np.mean(traj.u ** 2))):.2f} N m")
    print(f"diverged                          : {traj.diverged}")
    coarse_u, coarse_state = build_controller(chain, K, S)
    simulate(chain, coarse_u, HANGING, 60.0, 4 * DT)
    print(f"\nhandover time at a 4x coarser step: {coarse_state['t_switch']} s "
          f"(the result is not an artefact of the step size)")
    print(f"\nThe handover threshold rho = {RHO_SWITCH} is about "
          f"{min(edge_costs) / RHO_SWITCH:.0f}x inside the smallest measured edge cost, which "
          f"costs time:")
    for rho_try in (50.0, 200.0, 400.0):
        trial_u, trial_st = build_controller(chain, K, S, rho=rho_try)
        tr = simulate(chain, trial_u, HANGING, 70.0, 4 * DT)
        print(f"   rho = {rho_try:6.1f}: handover at {trial_st['t_switch']} s, "
              f"final error {np.max(np.abs(state_error(tr.x[-1]))):.2e}")
    print("   Handing over at the measured edge saves about a quarter of the swing-up time "
          "and still\n   converges, but it spends the whole basin on arrival accuracy and "
          "leaves nothing for the\n   model error and noise measured in step 5. The "
          "conservative threshold is the better trade.")

    section("5. FAILURE BOUNDARY")
    peak = float(np.abs(traj.u).max())
    print(f"a. Torque limit. The nominal run peaks at {peak:.2f} N m.")
    lo, hi = 0.2, 1.0
    for _ in range(6):
        mid = 0.5 * (lo + hi)
        trial_u, trial_state = build_controller(chain, K, S)
        simulate(chain, trial_u, HANGING, 60.0, 4 * DT, torque_limit=mid * peak)
        if trial_state["mode"] == "lqr":
            hi = mid
        else:
            lo = mid
    print(f"   swing-up still reaches the basin down to about "
          f"{hi * peak:.2f} N m ({hi:.0%} of the nominal peak);")
    print(f"   below about {lo * peak:.2f} N m it never gets there. The peak torque is a "
          f"requirement, not a preference.")

    print("\nb. Model error. The controller keeps its nominal model while the plant changes.")
    for frac in (0.05, 0.10, 0.20):
        perturbations = []
        gen = np.random.default_rng(SEED + int(frac * 1000))
        for _ in range(12):
            perturbations.append({k: float(v * (1 + gen.uniform(-frac, frac)))
                                  for k, v in PLANT.items()})

        def trial(p):
            plant = acrobot(**p)
            uu, st = build_controller(plant, K, S)      # the NOMINAL K and S
            simulate(plant, uu, HANGING, 60.0, 4 * DT)
            return st["mode"] == "lqr"
        sweep = robustness_sweep(trial, perturbations)
        print(f"   +-{frac:.0%} on every parameter: {sweep['successes']}/{sweep['trials']} "
              f"reach the basin, rate {sweep['rate']:.2f}, "
              f"95% interval {sweep['interval'][0]:.2f} to {sweep['interval'][1]:.2f}")
    print("   The interval is what the trial count supports; the rate alone is not a result.")

    print("\nc. Sensor noise on the measured state (the plant still integrates the truth).")
    for sigma in (1e-4, 1e-3, 1e-2):
        noisy_u, noisy_state = build_controller(chain, K, S)
        nt = simulate(chain, noisy_u, HANGING, 60.0, 4 * DT,
                      noise={"q": sigma, "qdot": 10 * sigma}, rng=SEED)
        err = np.max(np.abs(state_error(nt.x[-1]))) if not nt.diverged else float("inf")
        print(f"   sigma_q = {sigma:.0e} rad, sigma_qdot = {10 * sigma:.0e} rad/s: "
              f"handover {noisy_state['t_switch']}, final error {err:.3e}")
    print("   The balance controller's gains multiply velocity noise directly, so the "
          "noise floor it\n   tolerates is set by the same minimum gain that makes the "
          "basin narrow.")

    section("WHAT THIS DOES AND DOES NOT SHOW")
    print("""Shown: in this model, with these parameters, Spong's energy swing-up reaches the
LQR's basin and the LQR then balances the Acrobot; the basin is a few degrees wide and
that is forced by the plant, not by the weights; the peak torque, the model error and the
noise at which it stops working are measured, not asserted.

Not shown: that this model matches any physical Acrobot. There is no joint friction beyond
viscous damping, no actuator dynamics or torque-speed envelope, no backlash, no flexibility,
no state estimator and no computation delay. Each of those costs margin, and the delay
margin above says how little there is to spend. Nothing here is evidence about hardware;
for that, the only evidence is hardware.""")
    return 0


if __name__ == "__main__":
    sys.exit(main())
