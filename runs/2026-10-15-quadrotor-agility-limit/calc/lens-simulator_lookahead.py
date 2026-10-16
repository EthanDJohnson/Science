#!/usr/bin/env python3
"""Part 2: the UNSEEN-course regime (look-ahead limited), the dodge bound with full
rotational dynamics, and the elasticity table assembled from both sweep logs.

Three experiments.

(A) THE UNSEEN COURSE.  The same plant, controller and course, but the reference is no longer
    known in advance: the controller runs pure pursuit on the part of the path within
    perception range s_look (carrot at distance s_look, feed-forward centripetal acceleration
    taken from the carrot's curvature, which is the farthest point the vehicle can be said to
    have seen).  s_look is the one candidate limit the preview runs could not test, because a
    previewed trajectory assumes infinite look-ahead.  This is the regime the brief's metric
    actually asks about.

(B) THE DODGE BOUND WITH ROTATIONAL DYNAMICS.  Falanga et al.'s perception-latency bound
    (dossier D-31) is a point-mass result and is criticised for neglecting the platform's
    rotational dynamics (RC-09).  Here the same manoeuvre is flown on the verified 17-state
    plant with the real attitude loop, motor lag and thrust limits: fly at constant speed v
    toward an obstacle first sensed at range s, wait out the latency tau, then use full lateral
    authority to clear it by r + vehicle radius.  The largest v that clears is compared with
    the point-mass bound.

(C) THE ELASTICITY TABLE, assembled from the closed-loop speeds in
    lens-simulator_sweep.py.log (quoted in this file with their source line) plus the
    look-ahead elasticity measured here.

SI units.  Seeds fixed.  dt = 2 ms (checked against 1 ms in lens-simulator_verify.py).
Verification for the plant: lens-simulator_verify.py.log, 24/24 PASS.
"""
import importlib.util
import math
import os
import sys
import time

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(_ROOT, ".claude", "skills", "conundrum", "scripts"))
from quadrotor import platform_sun2022, quat_to_rot                     # noqa: E402

_spec = importlib.util.spec_from_file_location(
    "simmodel", os.path.join(_HERE, "lens-simulator_model.py"))
M = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(M)

G = 9.80665
DT = 2e-3
LOOSE = M.Slalom(tol=0.50)
q0 = platform_sun2022()
A_H = q0.hover()["a_max_horizontal"]
T_OPT = M.time_optimal_path_time(LOOSE, A_H, np.inf)["t_opt"]
S_PATH = LOOSE.arclength()
BASE = dict(tau_imu=1e-3, tau_vio=20e-3, f_inner=500.0, f_outer=200.0)
GRID = (5.0, 7.0, 10.0, 13.0, 15.5, 17.0, 18.2)


def el(a, b, x, y):
    if not (np.isfinite(a) and np.isfinite(b) and a > 0 and b > 0):
        return float("nan")
    return math.log(b / a) / math.log(y / x)


def u_max(q, ctl, course, dt=DT, grid=GRID, refine=3, **kw):
    good, bad = None, None
    for U in grid:
        r = M.run_course(q, ctl, course, U, dt=dt, **kw)
        if r["ok"]:
            good = (U, r)
        else:
            bad = (U, r)
            break
    if good is None:
        return {"U": float("nan"), "best": None,
                "note": f"fails at U = {grid[0]} m/s ({bad[1]['failure_mode']}, "
                        f"err {bad[1]['worst_gate_err']:.3f} m)"}
    if bad is None:
        return {"U": good[0], "best": good[1], "note": "AT FAMILY CEILING"}
    a, b = good[0], bad[0]
    for _ in range(refine):
        mid = 0.5 * (a + b)
        r = M.run_course(q, ctl, course, mid, dt=dt, **kw)
        if r["ok"]:
            a, good = mid, (mid, r)
        else:
            b, bad = mid, (mid, r)
    return {"U": a, "best": good[1], "note": bad[1]["failure_mode"]}


def report(label, q, ctl, course=LOOSE, dt=DT, **kw):
    t0 = time.time()
    out = u_max(q, ctl, course, dt=dt, **kw)
    r = out["best"]
    if r is None:
        print(f"  {label:38s}  {out['note']}")
        return {"v_mean": float("nan"), "U": float("nan")}
    print(f"  {label:38s}  U*={out['U']:6.3f}  v={r['v_mean_path']:6.3f} m/s  "
          f"t={r['t_finish']:5.3f} s  frac={T_OPT/r['t_finish']:5.3f}  "
          f"err={r['worst_gate_err']:5.3f} m  pk={r['peak_rotor_thrust']:5.2f} N  "
          f"rms={r['rms_rotor_thrust']:4.2f} N  sat={r['sat_fraction']*100:4.1f}%  "
          f"[{out['note']}, {time.time()-t0:.0f}s]")
    return {"v_mean": r["v_mean_path"], "U": out["U"], "t": r["t_finish"],
            "frac": T_OPT / r["t_finish"], "err": r["worst_gate_err"],
            "pk": r["peak_rotor_thrust"], "rms": r["rms_rotor_thrust"]}


print(__doc__)
print(M.model_card(q0, LOOSE, M.Cascade(q0, **BASE)))
print(f"\n  t_opt = {T_OPT:.4f} s over {S_PATH:.3f} m; a_h = {A_H:.3f} m/s^2; "
      f"T/W = {q0.hover()['thrust_to_weight']:.4f}")
dg = q0.variant(enable_drag=False, enable_h_force=False, motor_tau=0.0).diagnostics(
    dt=1e-3, t_end=2.0, rk4_dt=0.02)
print(f"  repeated verification: angular-momentum drift {dg['angular_momentum_drift']:.2e}, "
      f"free-fall error {dg['free_fall_error']:.2e} m, RK4 order {dg['rk4_order']:.3f}")

# ------------------------------------------------------------------ (A) unseen course
print("\n" + "=" * 100)
print("(A) UNSEEN COURSE: perception range s_look, pure pursuit, gate tol 0.50 m")
print("=" * 100)
ctl = M.Cascade(q0, **BASE)
LA = {}
for sl in (3.0, 5.0, 8.0, 12.0, 20.0, 40.0):
    LA[sl] = report(f"s_look = {sl:5.1f} m", q0, ctl, mode="lookahead", s_look=sl)
print("  look-ahead elasticities d ln(v)/d ln(s_look):")
for a, b in ((3.0, 8.0), (5.0, 20.0), (8.0, 40.0), (20.0, 40.0)):
    print(f"      {a:5.1f} -> {b:5.1f} m : {el(LA[a]['v_mean'], LA[b]['v_mean'], a, b):+8.4f}")
print("  and, at a fixed s_look = 8 m, how much the OTHER limits still matter:")
for tv in (5e-3, 20e-3, 80e-3):
    LA[f"tv{tv}"] = report(f"s_look = 8 m, tau_vio = {tv*1e3:5.1f} ms", q0,
                           M.Cascade(q0, **{**BASE, "tau_vio": tv}),
                           mode="lookahead", s_look=8.0)
print(f"      VIO-latency elasticity at s_look = 8 m (5 -> 80 ms): "
      f"{el(LA['tv0.005']['v_mean'], LA['tv0.08']['v_mean'], 5e-3, 80e-3):+.4f}")

# ------------------------------------------------------------------ (B) dodge bound
print("\n" + "=" * 100)
print("(B) DODGE BOUND WITH FULL ROTATIONAL DYNAMICS vs THE POINT-MASS BOUND")
print("=" * 100)


def dodge(q, ctl, v, s, tau_lat, need, dt=1e-3, a_cmd=None):
    """Fly at speed v along +x; at t = tau_lat command full lateral acceleration.  Return the
    lateral displacement achieved by the time x has advanced by s (m)."""
    a_cmd = A_H if a_cmd is None else a_cmd
    x = np.zeros(17)
    x[0:3] = np.array([0.0, 0.0, 5.0])
    x[3:7] = np.array([1.0, 0.0, 0.0, 0.0])
    x[7:10] = np.array([v, 0.0, 0.0])
    x[13:17] = q.hover()["omega_hover"]
    hist = [x.copy()]
    k_imu = int(round(ctl.tau_imu / dt))
    n_inner = max(1, int(round((1.0 / ctl.f_inner) / dt)))
    u = x[13:17].copy()
    t = 0.0
    nmax = int(round((2.5 * s / max(v, 1e-6)) / dt))
    for i in range(nmax):
        hi = hist[max(0, len(hist) - 1 - k_imu)]
        if i % n_inner == 0:
            # hold speed along x and altitude; after the latency, full lateral command
            a_des = np.array([0.0, a_cmd if t >= tau_lat else 0.0, 0.0])
            a_des[0] += ctl.w_vel * (v - hi[7])
            a_des[2] += ctl.w_vel * (0.0 - hi[9]) + ctl.w_pos * ctl.w_vel * (5.0 - hi[2])
            T, zb = ctl.thrust_and_attitude(a_des, hi[3:7])
            om_des = ctl.rate_cmd(hi[3:7], zb)
            tau_c = ctl.torque_cmd(hi[10:13], om_des)
            f_cmd, _ = ctl.mix(T, tau_c)
            u = np.sqrt(np.maximum(f_cmd, 0.0) / q.k_thrust)
        f = lambda tt, y: q.dynamics(y, u)
        k1 = f(t, x); k2 = f(t + dt / 2, x + dt / 2 * k1)
        k3 = f(t + dt / 2, x + dt / 2 * k2); k4 = f(t + dt, x + dt * k3)
        x = x + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        x[3:7] /= np.linalg.norm(x[3:7])
        hist.append(x.copy())
        t += dt
        if x[0] >= s:
            break
    return abs(x[1]), x[0] >= s


R_OBS, R_VEH = 0.5, 0.25
NEED = R_OBS + R_VEH
print(f"  obstacle radius {R_OBS} m, vehicle radius {R_VEH} m, so the needed lateral "
      f"displacement is {NEED} m")
print(f"  {'s (m)':>7s} {'tau (ms)':>9s} {'v_sim (m/s)':>12s} {'v_pointmass (m/s)':>18s} "
      f"{'ratio':>7s}")
for s_rng, tau_l in ((6.0, 0.020), (6.0, 0.050), (6.0, 0.100), (10.0, 0.050), (3.0, 0.050)):
    lo, hi = 1.0, 40.0
    for _ in range(9):
        mid = 0.5 * (lo + hi)
        d, reached = dodge(q0, ctl, mid, s_rng, tau_l, NEED)
        if d >= NEED and reached:
            lo = mid
        else:
            hi = mid
    v_pm = s_rng / (tau_l + 2 * math.sqrt(NEED / A_H))     # Falanga form, D-31
    print(f"  {s_rng:7.1f} {tau_l*1e3:9.1f} {lo:12.3f} {v_pm:18.3f} {lo/v_pm:7.3f}")
print("  point-mass form used: v_max = s / (tau + 2 sqrt(r_need / a_max))  [D-31, A-33]")
print("  the ratio below 1 is the cost of having to ROTATE before the lateral force appears:")
print("  the rotation time is not in the point-mass bound, and the motor lag is not either.")

# ------------------------------------------------------------------ (C) elasticity table
print("\n" + "=" * 100)
print("(C) ELASTICITY TABLE   d ln(mean speed) / d ln(limit)")
print("=" * 100)
# Values quoted from lens-simulator_sweep.py.log (gate tol 0.20 m unless marked), each with
# the perturbation that produced it.  Source lines are in that log.
T020 = {            # limit value -> mean path speed (m/s), gate tol 0.20 m
    "motor_tau": {5e-3: 19.862, 10e-3: 19.862, 19.55e-3: 18.719, 39.1e-3: 16.165,
                  78.2e-3: 7.954},
    "tau_vio": {5e-3: 18.892, 10e-3: 17.419, 20e-3: 16.165, 40e-3: 14.514, 80e-3: 12.192,
                130e-3: 10.601},
    "tau_imu": {0.5e-3: 16.852, 1e-3: 16.165, 2e-3: 15.468, 5e-3: 11.249},
    "kd_scale": {0.0: 9.713, 0.5: 12.141, 1.0: 15.811},
}
T050 = {            # gate tol 0.50 m
    "motor_tau": {19.55e-3: 18.719, 39.1e-3: 19.592, 78.2e-3: 14.220},
    "thrust_max": {6.0: 16.840, 7.5: 18.943, 8.5: 19.592, 10.0: 19.600},
}
print("  gate tolerance 0.20 m (tracking-error limited regime):")
rowsA = [
    ("actuator: motor time constant", "5 -> 10 ms", el(T020["motor_tau"][5e-3],
     T020["motor_tau"][10e-3], 5e-3, 10e-3)),
    ("actuator: motor time constant", "19.55 -> 39.1 ms", el(T020["motor_tau"][19.55e-3],
     T020["motor_tau"][39.1e-3], 19.55e-3, 39.1e-3)),
    ("actuator: motor time constant", "39.1 -> 78.2 ms", el(T020["motor_tau"][39.1e-3],
     T020["motor_tau"][78.2e-3], 39.1e-3, 78.2e-3)),
    ("estimation: VIO latency", "10 -> 40 ms", el(T020["tau_vio"][10e-3],
     T020["tau_vio"][40e-3], 10e-3, 40e-3)),
    ("estimation: VIO latency", "40 -> 130 ms", el(T020["tau_vio"][40e-3],
     T020["tau_vio"][130e-3], 40e-3, 130e-3)),
    ("estimation: VIO latency", "5 -> 130 ms (whole range)", el(T020["tau_vio"][5e-3],
     T020["tau_vio"][130e-3], 5e-3, 130e-3)),
    ("estimation: IMU latency", "0.5 -> 2 ms", el(T020["tau_imu"][0.5e-3],
     T020["tau_imu"][2e-3], 0.5e-3, 2e-3)),
    ("estimation: IMU latency", "2 -> 5 ms", el(T020["tau_imu"][2e-3],
     T020["tau_imu"][5e-3], 2e-3, 5e-3)),
    ("aero: unmodelled drag kd", "0.5x -> 1x (SIGN: more drag, faster)",
     el(T020["kd_scale"][0.5], T020["kd_scale"][1.0], 0.5, 1.0)),
]
for a, b, c in rowsA:
    print(f"      {a:32s} {b:34s} {c:+8.4f}")
print("  gate tolerance 0.50 m (thrust-authority limited regime):")
rowsB = [
    ("actuator: motor time constant", "39.1 -> 78.2 ms", el(T050["motor_tau"][39.1e-3],
     T050["motor_tau"][78.2e-3], 39.1e-3, 78.2e-3)),
    ("thrust-to-weight", "6 -> 10 N per rotor", el(T050["thrust_max"][6.0],
     T050["thrust_max"][10.0], 6.0, 10.0)),
    ("thrust-to-weight", "6 -> 7.5 N per rotor", el(T050["thrust_max"][6.0],
     T050["thrust_max"][7.5], 6.0, 7.5)),
    ("thrust-to-weight", "8.5 -> 10 N per rotor", el(T050["thrust_max"][8.5],
     T050["thrust_max"][10.0], 8.5, 10.0)),
]
for a, b, c in rowsB:
    print(f"      {a:32s} {b:34s} {c:+8.4f}")
print("  perception range (measured in part A above, gate tol 0.50 m):")
for a, b in ((3.0, 8.0), (8.0, 40.0)):
    print(f"      {'perception: look-ahead s_look':32s} "
          f"{f'{a:g} -> {b:g} m':34s} {el(LA[a]['v_mean'], LA[b]['v_mean'], a, b):+8.4f}")
print("\n  hardware cross-checks from the dossier:")
print("      A-16  planner thrust-to-weight sweep on a real track: "
      "d ln(speed)/d ln(TWR) = +0.565")
print("      A-06  +40 ms of command latency raised tracking RMSE by 47 per cent (confounded "
      "with a radio link); log-log slope <= 0.51")
print("      A-33  stop-before-obstacle bound: e_s = +0.52, e_a = +0.48, e_tau = -0.037 to "
      "-0.10; dodge bound e_s = 1 exactly, e_tau = -0.08 to -0.24")
