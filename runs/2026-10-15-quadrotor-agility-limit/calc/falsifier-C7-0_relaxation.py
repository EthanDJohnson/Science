#!/usr/bin/env python3
"""Refuter C7-0: the RELAXATION-direction sensitivities at the measured hardware operating point.

C7 (null) says the leading limits sit within a factor of about two at the operating point.
The brief defines "binds first" as the limit whose RELAXATION, holding the others fixed,
produces the largest improvement in the agility metric.  The slate's clustered elasticities are
arc elasticities taken mostly in the TIGHTENING direction and across intervals that straddle or
sit below the measured hardware value (motor_tau 39.1 -> 78.2 ms; thrust 6 -> 7.5 N against a
hardware 8.5 N; tau_vio 40 -> 130 ms against a hardware 20 ms).  This script measures the same
limits one at a time in the IMPROVING direction, at the hardware values, on the verified
17-state plant, and reports the speed gain from an equal 20 per cent relaxation of each.

Two tasks:
  (A) the dodge manoeuvre (the unseen-obstacle regime the brief's metric selects): the largest
      constant forward speed at which an obstacle first seen at range s is cleared by
      r_obs + r_veh = 0.75 m, with the real attitude loop, motor lag and per-rotor thrust
      limits.  Reproduction check against lens-simulator_lookahead.py.log first.
  (B) the seen-course preview task (the regime C7's leg (iii) uses): U*, the largest reference
      speed that still flies the 6-gate slalom at the 0.50 m tolerance, by bisection.

All SI units.  dt = 1 ms in (A), 2 ms in (B), as in the lens's own scripts.
"""
import importlib.util
import math
import os
import sys

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
BASE = dict(tau_imu=1e-3, tau_vio=20e-3, f_inner=500.0, f_outer=200.0)
q0 = platform_sun2022()
A_H0 = q0.hover()["a_max_horizontal"]
R_NEED = 0.75
print(__doc__)
print(f"  plant: m = {q0.mass} kg, motor_tau = {q0.motor_tau*1e3:.2f} ms, "
      f"f_max = {q0.thrust_max} N/rotor, T/W = {q0.hover()['thrust_to_weight']:.4f}, "
      f"a_h = {A_H0:.3f} m/s^2")
dg = q0.variant(enable_drag=False, enable_h_force=False, motor_tau=0.0).diagnostics(
    dt=1e-3, t_end=2.0, rk4_dt=0.02)
print(f"  plant re-verification: ang-mom drift {dg['angular_momentum_drift']:.2e}, "
      f"free-fall err {dg['free_fall_error']:.2e} m, RK4 order {dg['rk4_order']:.3f}")


def dodge_disp(q, ctl, v, s, tau_lat, a_cmd, dt=1e-3):
    """Lateral displacement achieved by the time x advances s, with full lateral command
    applied after tau_lat.  Mirrors lens-simulator_lookahead.py's dodge()."""
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
            a_des = np.array([0.0, a_cmd if t >= tau_lat else 0.0, 0.0])
            a_des[0] += ctl.w_vel * (v - hi[7])
            a_des[2] += ctl.w_vel * (0.0 - hi[9]) + ctl.w_pos * ctl.w_vel * (5.0 - hi[2])
            T, zb = ctl.thrust_and_attitude(a_des, hi[3:7])
            om_des = ctl.rate_cmd(hi[3:7], zb)
            f_cmd, _ = ctl.mix(T, ctl.torque_cmd(hi[10:13], om_des))
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


def v_dodge(q, ctl, s, tau_lat, a_cmd=None, nbis=9, lo=1.0, hi=60.0):
    a_cmd = q.hover()["a_max_horizontal"] if a_cmd is None else a_cmd
    for _ in range(nbis):
        mid = 0.5 * (lo + hi)
        d, reached = dodge_disp(q, ctl, mid, s, tau_lat, a_cmd)
        if d >= R_NEED and reached:
            lo = mid
        else:
            hi = mid
    return lo


def el(v1, v2, x1, x2):
    return math.log(v2 / v1) / math.log(x2 / x1)


# ---------------------------------------------------------------- (A0) reproduction check
print("\n" + "=" * 96)
print("(A0) REPRODUCTION of the lens's dodge table (lens-simulator_lookahead.py.log)")
print("=" * 96)
ctl0 = M.Cascade(q0, **BASE)
LENS = {(6.0, 0.020): 18.139, (6.0, 0.050): 16.920, (6.0, 0.100): 15.320,
        (10.0, 0.050): 29.412, (3.0, 0.050): 8.541}
print(f"  {'s (m)':>7s} {'tau (ms)':>9s} {'mine (m/s)':>11s} {'lens (m/s)':>11s} {'rel err':>9s}")
MINE = {}
for (s_, t_), vl in LENS.items():
    vm = v_dodge(q0, ctl0, s_, t_, lo=1.0, hi=40.0)
    MINE[(s_, t_)] = vm
    print(f"  {s_:7.1f} {t_*1e3:9.1f} {vm:11.3f} {vl:11.3f} "
          f"{abs(vm/vl-1)*100:8.3f} %  {'PASS' if abs(vm/vl-1) < 0.01 else 'FAIL'}")
e_s_lens = el(MINE[(3.0, 0.050)], MINE[(6.0, 0.050)], 3.0, 6.0)
print(f"  range elasticity 3 -> 6 m (lens +0.9863): {e_s_lens:+.4f}")

# ---------------------------------------------------------------- (A) equal relaxation, dodge
print("\n" + "=" * 96)
print("(A) DODGE TASK: speed gain from an equal 20 per cent RELAXATION of each limit")
print("    operating point: s = 6 m, tau_perc = 50 ms, motor_tau = 39.1 ms, f_max = 8.5 N")
print("=" * 96)
S0, TAU0 = 6.0, 0.050
v_base = MINE[(6.0, 0.050)]
print(f"  baseline v = {v_base:.4f} m/s")
rows = []


def add(label, limit_from, limit_to, vnew, note=""):
    gain = vnew / v_base - 1.0
    e = el(v_base, vnew, limit_from, limit_to)
    rows.append((label, f"{limit_from:g} -> {limit_to:g}", vnew, gain, abs(e), note))
    print(f"  {label:34s} {limit_from:9.4g} -> {limit_to:<9.4g} v = {vnew:7.3f} m/s  "
          f"gain {gain*100:+7.2f} %  |e| = {abs(e):.4f}  {note}")


# perception range +20 %
add("perception range s (m)", S0, 1.2 * S0, v_dodge(q0, ctl0, 1.2 * S0, TAU0))
# thrust limit +20 % (T/W and a_h follow)
q_t = q0.variant(thrust_max=1.2 * q0.thrust_max)
add("per-rotor thrust limit (N)", q0.thrust_max, 1.2 * q0.thrust_max,
    v_dodge(q_t, M.Cascade(q_t, **BASE), S0, TAU0),
    f"T/W {q_t.hover()['thrust_to_weight']:.3f}, a_h {q_t.hover()['a_max_horizontal']:.2f}")
# motor time constant -20 %
q_m = q0.variant(motor_tau=0.8 * q0.motor_tau)
c_m = M.Cascade(q_m, **BASE)
add("motor time constant (s)", q0.motor_tau, 0.8 * q0.motor_tau,
    v_dodge(q_m, c_m, S0, TAU0, a_cmd=A_H0), f"w_rate {c_m.w_rate:.1f} rad/s")
# perception/estimation latency -20 %
add("perception latency tau (s)", TAU0, 0.8 * TAU0, v_dodge(q0, ctl0, S0, 0.8 * TAU0))
# unmodelled aero -20 % (plant drag reduced, controller model unchanged)
q_a = q0.variant(kd=tuple(0.8 * np.asarray(q0.kd, float)))
add("unmodelled drag kd (kg/s)", 1.0, 0.8,
    v_dodge(q_a, M.Cascade(q_a, **BASE), S0, TAU0, a_cmd=A_H0),
    "limit decreases, so x2 < x1")

print("\n  ranking by speed gain from a 20 per cent relaxation:")
for lab, rng, vn, g, e, note in sorted(rows, key=lambda r: -r[3]):
    print(f"      {lab:34s} {g*100:+7.2f} %   |e| = {e:.4f}")
gains = sorted([r[3] for r in rows], reverse=True)
els = sorted([r[4] for r in rows], reverse=True)
print(f"  largest gain / second-largest gain  = {gains[0]/max(gains[1],1e-9):.2f}")
print(f"  largest gain / smallest gain        = {gains[0]/max(gains[-1],1e-9):.2f}")
print(f"  largest |e| / second-largest |e|    = {els[0]/max(els[1],1e-9):.2f}")
print(f"  C7's trigger is 'within a factor of about two': "
      f"{'FAILS (>2)' if gains[0]/max(gains[1],1e-9) > 2 else 'holds (<=2)'}")

# ---------------------------------------------------------------- (A2) feasible relaxations
print("\n" + "=" * 96)
print("(A2) FEASIBLE relaxation, each taken to what 2026 hardware actually offers")
print("=" * 96)
feas = []
for lab, v in (("range 6 -> 12 m (stereo/event depth at 12 m)", v_dodge(q0, ctl0, 12.0, TAU0)),
               ("latency 50 -> 10 ms (event camera)", v_dodge(q0, ctl0, S0, 0.010)),
               ("motor_tau 39.1 -> 5 ms (direct-drive/INDI limit)",
                v_dodge(q0.variant(motor_tau=5e-3),
                        M.Cascade(q0.variant(motor_tau=5e-3), **BASE), S0, TAU0, a_cmd=A_H0)),
               ("f_max 8.5 -> 12 N (T/W 4.62 -> 6.53)",
                v_dodge(q0.variant(thrust_max=12.0),
                        M.Cascade(q0.variant(thrust_max=12.0), **BASE), S0, TAU0)),
               ("perfect aero model (plant drag off)",
                v_dodge(q0.variant(enable_drag=False, enable_h_force=False),
                        M.Cascade(q0.variant(enable_drag=False, enable_h_force=False), **BASE),
                        S0, TAU0, a_cmd=A_H0))):
    feas.append((lab, v, v / v_base - 1))
    print(f"  {lab:50s} v = {v:7.3f} m/s  gain {(v/v_base-1)*100:+7.2f} %")
fg = sorted([f[2] for f in feas], reverse=True)
print(f"  largest / second-largest feasible gain = {fg[0]/max(fg[1],1e-9):.2f}")

# ---------------------------------------------------------------- (B) seen course
print("\n" + "=" * 96)
print("(B) SEEN-COURSE PREVIEW TASK: U* by bisection, gate tol 0.50 m "
      "(C7 leg (iii)'s own regime)")
print("=" * 96)
LOOSE = M.Slalom(tol=0.50)


def ustar(q, ctl, lo=10.0, hi=26.0, n=7, dt=2e-3):
    best = None
    for _ in range(n):
        mid = 0.5 * (lo + hi)
        try:
            r = M.run_course(q, ctl, LOOSE, mid, dt=dt)
        except Exception:
            r = {"ok": False}
        if r["ok"]:
            lo, best = mid, r
        else:
            hi = mid
    return lo, (best["v_mean_path"] if best else float("nan"))


cases = [("baseline (hardware values)", q0, M.Cascade(q0, **BASE))]
q_t2 = q0.variant(thrust_max=1.2 * q0.thrust_max)
cases.append(("thrust limit +20 %", q_t2, M.Cascade(q_t2, **BASE)))
q_m2 = q0.variant(motor_tau=0.8 * q0.motor_tau)
cases.append(("motor_tau -20 %", q_m2, M.Cascade(q_m2, **BASE)))
cases.append(("tau_vio -20 % (20 -> 16 ms)", q0,
              M.Cascade(q0, **{**BASE, "tau_vio": 16e-3})))
res = {}
print(f"  {'case':32s} {'U* (m/s)':>9s} {'mean path speed (m/s)':>22s} {'gain':>8s}")
for lab, q_, c_ in cases:
    u, vm = ustar(q_, c_)
    res[lab] = (u, vm)
    base_vm = res["baseline (hardware values)"][1]
    print(f"  {lab:32s} {u:9.3f} {vm:22.3f} {(vm/base_vm-1)*100:+7.2f} %")
print("  (bisection on U in [10, 26] m/s, 7 steps -> resolution 0.125 m/s)")
print("  NOTE: the look-ahead-limited (unseen) version of this same task could not be scored:")
print("  the lens's pure-pursuit runs fail at U = 5 m/s for EVERY s_look from 3 to 40 m, so")
print("  its look-ahead elasticity row is 'nan' in lens-simulator_lookahead.py.log.")
print("\nDONE")
