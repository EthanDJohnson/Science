#!/usr/bin/env python3
"""Closed-loop agility and the ELASTICITY of it to each candidate limit, one at a time.

REFERENCE FAMILY.  p_ref(t) = (U t, A sin(2 pi U t / L), z0): the course flown at a constant
rate along x.  It is C-infinity, its peak demand is |a| = A k^2 U^2 at the gates, and its own
dynamic-feasibility ceiling is U_feas = sqrt(a_h / (A k^2)) = 18.339 m/s, at which the
reference uses 100 per cent of the platform's horizontal acceleration ceiling and leaves zero
margin for feedback.  Flown at U_feas it takes 4.9075 s, i.e. 91.7 per cent of the platform's
point-mass time-optimal 4.5020 s on the same path, so the family itself costs 9 per cent of
the denominator.  (The platform's OWN time-optimal profile was also built and flown: see the
TRACKABILITY section -- its acceleration is discontinuous at every switching point and this
cascade cannot track it at ANY speed, which is a result, not a bug.)

MEASURE.  The largest U at which the closed loop passes all six gates, at two gate tolerances:
  tol = 0.50 m  -- a 1.5 m MonoRace gate minus a 0.25 m vehicle radius (dossier A-26)
  tol = 0.20 m  -- a 0.9 m gate, or the same gate with a tighter clearance demand
The loose tolerance shows WHICH limit binds; the tight one has the resolution to measure HOW
MUCH, because at the loose tolerance several conditions sit against the family ceiling.

The limit is perturbed in the PLANT (or the sensing chain); the controller keeps its nominal
model.  Bandwidth is retuned by the model's closed-form rule (largest rate-loop gain with
40 deg phase margin for L = (w/s) e^{-s tau_in}/(1 + s motor_tau)).  A fixed-gain control run
shows the sign does not come from the retuning rule.

Verification: lens-simulator_verify.py, 24/24 PASS; load-bearing rows repeated below.
SI units, seeds fixed.  dt = 2 ms for the sweep, load-bearing rows repeated at 1 ms.
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
from quadrotor import platform_sun2022                                  # noqa: E402

_spec = importlib.util.spec_from_file_location(
    "simmodel", os.path.join(_HERE, "lens-simulator_model.py"))
M = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(M)

G = 9.80665
DT = 2e-3
LOOSE = M.Slalom(tol=0.50)
TIGHT = M.Slalom(tol=0.20)
A_H = platform_sun2022().hover()["a_max_horizontal"]
T_OPT = M.time_optimal_path_time(LOOSE, A_H, np.inf)["t_opt"]
S_PATH = LOOSE.arclength()
U_FEAS = LOOSE.ref_feasible_U(A_H)
GRID = (7.0, 10.0, 13.0, 15.5, 17.0, 18.2)


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
                "note": f"fails at U = {grid[0]} m/s, mode = {bad[1]['failure_mode']}, "
                        f"gate error {bad[1]['worst_gate_err']:.3f} m"}
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


def report(label, q, ctl, course=TIGHT, dt=DT, **kw):
    t0 = time.time()
    out = u_max(q, ctl, course, dt=dt, **kw)
    r = out["best"]
    if r is None:
        print(f"  {label:40s}  {out['note']}  w_r={ctl.w_rate:6.2f}")
        return {"label": label, "v_mean": float("nan"), "U": float("nan")}
    print(f"  {label:40s}  U*={out['U']:6.3f}  v={r['v_mean_path']:6.3f} m/s  "
          f"t={r['t_finish']:5.3f} s  frac={T_OPT/r['t_finish']:5.3f}  "
          f"err={r['worst_gate_err']:5.3f} m  pk={r['peak_rotor_thrust']:5.2f} N  "
          f"rms={r['rms_rotor_thrust']:4.2f} N  sat={r['sat_fraction']*100:4.1f}%  "
          f"w_r={ctl.w_rate:6.2f}  [{out['note']}, {time.time()-t0:.0f}s]")
    return {"label": label, "U": out["U"], "v_mean": r["v_mean_path"], "t": r["t_finish"],
            "frac": T_OPT / r["t_finish"], "err": r["worst_gate_err"],
            "pk": r["peak_rotor_thrust"], "rms": r["rms_rotor_thrust"],
            "sat": r["sat_fraction"], "w_rate": ctl.w_rate, "note": out["note"]}


def el(a, b, x, y):
    if not (np.isfinite(a) and np.isfinite(b) and a > 0 and b > 0):
        return float("nan")
    return math.log(b / a) / math.log(y / x)


print(__doc__)
q0 = platform_sun2022()
print(M.model_card(q0, TIGHT))
print("\n  REPEATED VERIFICATION (all 24 rows in lens-simulator_verify.py.log):")
dg = q0.variant(enable_drag=False, enable_h_force=False, motor_tau=0.0).diagnostics(
    dt=1e-3, t_end=2.0, rk4_dt=0.02)
print(f"      angular-momentum drift {dg['angular_momentum_drift']:.2e}, free-fall error "
      f"{dg['free_fall_error']:.2e} m, RK4 order {dg['rk4_order']:.3f}")
print(f"      DENOMINATOR t_opt = {T_OPT:.4f} s over {S_PATH:.3f} m "
      f"(mean path speed {S_PATH/T_OPT:.3f} m/s); a_h = {A_H:.3f} m/s^2; "
      f"T/W = {q0.hover()['thrust_to_weight']:.4f}; U_feas = {U_FEAS:.4f} m/s")
print(f"      tuning rule (closed form): tau_in = 2 ms, T_m = 39.1 ms -> w_rate = "
      f"{M.max_crossover_for_pm(2e-3, 0.0391, 40.0):.3f} rad/s; T_m = 0 -> "
      f"{M.max_crossover_for_pm(2e-3, 0.0, 40.0):.1f} rad/s (400 rad/s cap)")

BASE = dict(tau_imu=1e-3, tau_vio=20e-3, f_inner=500.0, f_outer=200.0)
ctl0 = M.Cascade(q0, **BASE)
print("\n" + "=" * 102)
print("BASELINE, BOTH TOLERANCES (seen course, full preview -- the Swift/MonoRace regime)")
print("=" * 102)
print("  " + M.model_card(q0, TIGHT, ctl0).splitlines()[-1].strip())
base_loose = report("baseline, gate tol 0.50 m", q0, ctl0, course=LOOSE)
base_tight = report("baseline, gate tol 0.20 m", q0, ctl0, course=TIGHT)

print("\n  ALSO at gate tol 0.50 m, the two axes that bind there:")
for tm in (19.55e-3, 39.1e-3, 78.2e-3):
    qv = q0.variant(motor_tau=tm)
    report(f"tol 0.50, motor_tau = {tm*1e3:5.2f} ms", qv, M.Cascade(qv, **BASE), course=LOOSE)
L5 = {}
for fm in (6.0, 7.5, 8.5, 10.0):
    qv = q0.variant(thrust_max=fm)
    L5[fm] = report(f"tol 0.50, thrust_max = {fm:5.1f} N (T/W "
                    f"{qv.hover()['thrust_to_weight']:5.2f})", qv, M.Cascade(qv, **BASE),
                    course=LOOSE)
print(f"  tol 0.50 thrust-to-weight elasticity (6 -> 10 N): "
      f"{el(L5[6.0]['v_mean'], L5[10.0]['v_mean'], 6.0, 10.0):+.4f}  "
      f"(hardware reference A-16: +0.565)")

print("\n" + "=" * 102)
print("TRACKABILITY OF THE PLATFORM'S OWN TIME-OPTIMAL PROFILE (alpha = fraction of a_h)")
print("=" * 102)
for al in (0.10, 0.25):
    rf = M.TimeOptimalRef(LOOSE, A_H, al)
    r = M.run_course(q0, ctl0, LOOSE, 0.0, dt=DT, ref=rf)
    print(f"  alpha = {al:4.2f} (t_ref = {rf.t_total:5.3f} s): ok={r['ok']}  "
          f"worst gate error = {r['worst_gate_err']:6.3f} m  mode = {r['failure_mode']}")
print("  the time-optimal profile is bang-bang in tangential acceleration, so the required")
print("  attitude is discontinuous at every switching point: a finite-bandwidth cascade")
print("  cannot track it even at a tenth of the acceleration budget.  This is why planners")
print("  stay inside a thrust margin (dossier D-36) and why smooth references are used (D-03).")

print("\n" + "=" * 102)
print("ONE LIMIT AT A TIME, gate tol 0.20 m (plant perturbed, controller nominal, retuned)")
print("=" * 102)
rows = {"base": base_tight}

print("\n[1] ACTUATOR BANDWIDTH   motor_tau (A-03 39.1 ms thrust, A-04 33 ms rotor speed)")
for tm in (5e-3, 10e-3, 19.55e-3, 39.1e-3, 78.2e-3):
    qv = q0.variant(motor_tau=tm)
    rows[f"mt{tm}"] = report(f"motor_tau = {tm*1e3:5.2f} ms", qv, M.Cascade(qv, **BASE))

print("\n[2] ESTIMATION LATENCY, OUTER (VIO) LOOP   (A-28 17 ms, A-07 40 ms, A-22 130 ms)")
for tv in (5e-3, 10e-3, 20e-3, 40e-3, 80e-3, 130e-3):
    rows[f"tv{tv}"] = report(f"tau_vio = {tv*1e3:6.1f} ms", q0,
                             M.Cascade(q0, **{**BASE, "tau_vio": tv}))

print("\n[3] ESTIMATION LATENCY, INNER (IMU) LOOP")
for ti in (0.5e-3, 1e-3, 2e-3, 5e-3):
    rows[f"ti{ti}"] = report(f"tau_imu = {ti*1e3:5.1f} ms", q0,
                             M.Cascade(q0, **{**BASE, "tau_imu": ti}))

print("\n[4a] UNMODELLED DRAG   plant kd scaled, kh off; the controller models no aerodynamics")
for sc in (0.0, 0.5, 1.0, 2.0, 4.0):
    kd = tuple(max(sc, 1e-12) * k for k in (0.26, 0.28, 0.42))
    qv = q0.variant(kd=kd, enable_h_force=False)
    rows[f"kd{sc}"] = report(f"kd x {sc:4.1f}, kh = 0 (unmodelled)", qv, M.Cascade(qv, **BASE))

print("\n[4b] UNMODELLED TRANSLATIONAL LIFT   plant kh scaled, kd nominal.  Sun et al. eq. 9,")
print("     quoted verbatim: f_a^B = [-kd,x vx; -kd,y vy; -kd,z vz + kh(vx^2+vy^2)], kh > 0,")
print("     so this unmodelled aerodynamic term ADDS body-z force at speed (4.0 N at 20 m/s,")
print("     54 per cent of the vehicle's weight): the dominant unmodelled aerodynamic term in")
print("     the one published parameter set for this class HELPS rather than hurts.")
for sc in (0.0, 1.0, 2.0):
    qv = q0.variant(k_h=0.01 * sc, enable_h_force=sc > 0)
    rows[f"kh{sc}"] = report(f"kh x {sc:4.1f}, kd nominal (unmodelled)", qv,
                             M.Cascade(qv, **BASE))

print("\n[5] THRUST-TO-WEIGHT   per-rotor thrust_max (A-13: 4.1-4.5 on real onboard platforms)")
for fm in (6.0, 7.5, 8.5, 10.0, 12.0):
    qv = q0.variant(thrust_max=fm)
    rows[f"fm{fm}"] = report(f"thrust_max = {fm:5.1f} N (T/W "
                             f"{qv.hover()['thrust_to_weight']:5.2f})", qv,
                             M.Cascade(qv, **BASE))

print("\n" + "=" * 102)
print("ELASTICITIES   d ln(mean speed) / d ln(limit), gate tol 0.20 m")
print("=" * 102)
E = {
    "motor time constant 19.55->78.2 ms": el(rows["mt0.01955"]["v_mean"],
                                             rows["mt0.0782"]["v_mean"], 19.55e-3, 78.2e-3),
    "motor time constant 10->39.1 ms": el(rows["mt0.01"]["v_mean"],
                                          rows["mt0.0391"]["v_mean"], 10e-3, 39.1e-3),
    "motor time constant 5->10 ms": el(rows["mt0.005"]["v_mean"],
                                       rows["mt0.01"]["v_mean"], 5e-3, 10e-3),
    "VIO latency 10->40 ms": el(rows["tv0.01"]["v_mean"], rows["tv0.04"]["v_mean"],
                                10e-3, 40e-3),
    "VIO latency 40->130 ms": el(rows["tv0.04"]["v_mean"], rows["tv0.13"]["v_mean"],
                                 40e-3, 130e-3),
    "IMU latency 0.5->2 ms": el(rows["ti0.0005"]["v_mean"], rows["ti0.002"]["v_mean"],
                                0.5e-3, 2e-3),
    "unmodelled drag kd 0.5x->2x": el(rows["kd0.5"]["v_mean"], rows["kd2.0"]["v_mean"],
                                      0.5, 2.0),
    "unmodelled drag kd 1x->4x": el(rows["kd1.0"]["v_mean"], rows["kd4.0"]["v_mean"], 1.0, 4.0),
    "thrust-to-weight 7.5->10 N": el(rows["fm7.5"]["v_mean"], rows["fm10.0"]["v_mean"],
                                     7.5, 10.0),
    "thrust-to-weight 6->12 N": el(rows["fm6.0"]["v_mean"], rows["fm12.0"]["v_mean"],
                                   6.0, 12.0),
}
for k, v in E.items():
    print(f"  {k:40s} {v:+8.4f}")
print("  reference: dossier A-16, a planner thrust-to-weight sweep flown on real hardware,")
print("  d ln(lap time)/d ln(TWR) = -0.565, i.e. d ln(speed)/d ln(TWR) = +0.565.")

print("\n" + "=" * 102)
print("CONTROL: is the elasticity an artefact of the retuning rule?  (gains frozen)")
print("=" * 102)
wf = ctl0.w_rate
print(f"  rate-loop gain frozen at the baseline {wf:.3f} rad/s in every case below")
fx = {}
for tv in (10e-3, 40e-3):
    fx[f"tv{tv}"] = report(f"FIXED gains, tau_vio = {tv*1e3:5.1f} ms", q0,
                           M.Cascade(q0, **{**BASE, "tau_vio": tv}, w_rate_fixed=wf))
for tm in (19.55e-3, 78.2e-3):
    qv = q0.variant(motor_tau=tm)
    fx[f"mt{tm}"] = report(f"FIXED gains, motor_tau = {tm*1e3:5.2f} ms", qv,
                           M.Cascade(qv, **BASE, w_rate_fixed=wf))
print(f"  fixed-gain elasticity to tau_vio   : "
      f"{el(fx['tv0.01']['v_mean'], fx['tv0.04']['v_mean'], 10e-3, 40e-3):+.4f}")
print(f"  fixed-gain elasticity to motor_tau : "
      f"{el(fx['mt0.01955']['v_mean'], fx['mt0.0782']['v_mean'], 19.55e-3, 78.2e-3):+.4f}")

print("\n" + "=" * 102)
print("ACHIEVABLE RATE-LOOP BANDWIDTH vs THE DELAY AND ACTUATOR BUDGET (PM = 40 deg)")
print("=" * 102)
print(f"  {'tau_in (ms)':>12s} {'motor_tau (ms)':>15s} {'w_rate (rad/s)':>15s} "
      f"{'f (Hz)':>9s} {'binding term':>16s}")
for ti in (1e-3, 2e-3, 5e-3, 20e-3, 40e-3):
    for tm in (0.0, 5e-3, 39.1e-3):
        w = M.max_crossover_for_pm(ti, tm, 40.0)
        w0 = M.max_crossover_for_pm(ti, 0.0, 40.0)
        wd = M.max_crossover_for_pm(1e-9, tm, 40.0)
        lim = "actuator lag" if w < 0.8 * w0 else ("delay" if w < 0.8 * wd else "neither (cap)")
        print(f"  {ti*1e3:12.1f} {tm*1e3:15.1f} {w:15.2f} {w/(2*math.pi):9.2f} {lim:>16s}")
print("  pure-delay closed form: w*tau <= pi/2 - PM = 0.8727 rad at PM = 40 deg (A-32)")

print("\n" + "=" * 102
      + "\nSTEP-SIZE CHECK ON THE LOAD-BEARING NUMBERS (dt = 2 ms -> 1 ms)\n" + "=" * 102)
for lab, qv, c in (("baseline tol 0.20", q0, M.Cascade(q0, **BASE)),
                   ("tau_vio = 130 ms", q0, M.Cascade(q0, **{**BASE, "tau_vio": 130e-3})),
                   ("motor_tau = 78.2 ms", q0.variant(motor_tau=78.2e-3),
                    M.Cascade(q0.variant(motor_tau=78.2e-3), **BASE))):
    report(lab + " @ dt = 1 ms", qv, c, dt=1e-3)
