#!/usr/bin/env python3
"""Refuter C7-0, part 2: equal FACTOR-OF-TWO relaxation of each limit, dodge task, and the
asymptotics that decide whether the range/thrust near-tie survives a finite relaxation.

C7's "within a factor of about two" is a statement about local elasticities.  On the dodge
bound the range elasticity is exactly 1 for all parameters while the acceleration elasticity is
provably below 1/2 and FALLS as a grows (M-DIAL-06, verified).  So any tie between them is
local only: it must widen for a finite relaxation.  Here each limit is relaxed by the same
factor of two on the verified 17-state plant, and the point-mass asymptotics are printed.

SI units.  dt = 1 ms.  Plant: Sun et al. 2022, 0.75 kg.
"""
import importlib.util
import math
import os
import sys

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(_ROOT, ".claude", "skills", "conundrum", "scripts"))
from quadrotor import platform_sun2022                                  # noqa: E402

_spec = importlib.util.spec_from_file_location(
    "simmodel", os.path.join(_HERE, "lens-simulator_model.py"))
M = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(M)
_f = importlib.util.spec_from_file_location(
    "relax", os.path.join(_HERE, "falsifier-C7-0_relaxation.py"))

G = 9.80665
BASE = dict(tau_imu=1e-3, tau_vio=20e-3, f_inner=500.0, f_outer=200.0)
q0 = platform_sun2022()
A_H0 = q0.hover()["a_max_horizontal"]
R_NEED = 0.75
S0, TAU0 = 6.0, 0.050
print(__doc__)


def dodge_disp(q, ctl, v, s, tau_lat, a_cmd, dt=1e-3):
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
    for i in range(int(round((2.5 * s / max(v, 1e-6)) / dt))):
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


def v_dodge(q, ctl, s, tau_lat, a_cmd=None, nbis=10, lo=1.0, hi=80.0):
    a_cmd = q.hover()["a_max_horizontal"] if a_cmd is None else a_cmd
    for _ in range(nbis):
        mid = 0.5 * (lo + hi)
        d, reached = dodge_disp(q, ctl, mid, s, tau_lat, a_cmd)
        if d >= R_NEED and reached:
            lo = mid
        else:
            hi = mid
    return lo


ctl0 = M.Cascade(q0, **BASE)
v_base = v_dodge(q0, ctl0, S0, TAU0)
print(f"  baseline v (s = 6 m, tau = 50 ms) = {v_base:.4f} m/s "
      f"(10-step bisection; 9-step value was 16.9199)")

print("\n" + "=" * 96)
print("EQUAL FACTOR-OF-TWO RELAXATION, one limit at a time, dodge task")
print("=" * 96)
rows = []


def add(label, vnew, note=""):
    rows.append((label, vnew, vnew / v_base - 1.0))
    print(f"  {label:48s} v = {vnew:7.3f} m/s   gain {(vnew/v_base-1)*100:+8.2f} %  {note}")


add("perception range  6 -> 12 m", v_dodge(q0, ctl0, 12.0, TAU0))
q_t = q0.variant(thrust_max=2.0 * q0.thrust_max)
add("per-rotor thrust  8.5 -> 17 N (T/W 4.62 -> 9.25)",
    v_dodge(q_t, M.Cascade(q_t, **BASE), S0, TAU0),
    f"a_h {q_t.hover()['a_max_horizontal']:.1f} m/s^2")
add("perception latency 50 -> 25 ms", v_dodge(q0, ctl0, S0, 0.025))
q_m = q0.variant(motor_tau=0.5 * q0.motor_tau)
add("motor time constant 39.1 -> 19.55 ms",
    v_dodge(q_m, M.Cascade(q_m, **BASE), S0, TAU0, a_cmd=A_H0),
    f"w_rate {M.Cascade(q_m, **BASE).w_rate:.1f} rad/s")
q_a = q0.variant(kd=tuple(0.5 * np.asarray(q0.kd, float)))
add("unmodelled drag kd  1x -> 0.5x",
    v_dodge(q_a, M.Cascade(q_a, **BASE), S0, TAU0, a_cmd=A_H0))
g = sorted([r[2] for r in rows], reverse=True)
print(f"\n  ranking: " + ", ".join(f"{lab.split()[0]} {gg*100:+.1f}%"
                                   for lab, _, gg in sorted(rows, key=lambda r: -r[2])))
print(f"  largest / second-largest gain = {g[0]/max(g[1],1e-9):.2f}")
print(f"  largest / third-largest gain  = {g[0]/max(g[2],1e-9):.2f}")
print(f"  C7's 'within a factor of about two' at a factor-2 relaxation: "
      f"{'FAILS' if g[0]/max(g[1],1e-9) > 2 else 'holds'}")

print("\n" + "=" * 96)
print("WHY THE TIE CANNOT SURVIVE: point-mass asymptotics v = s/(tau + 2 sqrt(r/a))  [D-31]")
print("=" * 96)


def v_pm(s, tau, a, r=R_NEED):
    return s / (tau + 2 * math.sqrt(r / a))


print(f"  {'a (m/s^2)':>11s} {'T/W needed':>11s} {'e_a':>8s} {'e_s':>6s} {'v_pm (m/s)':>11s}")
for fac in (1, 2, 4, 16, 1e4):
    a = A_H0 * fac
    tw = math.sqrt((a / G) ** 2 + 1)
    W = 2 * math.sqrt(R_NEED / a)
    e_a = 0.5 * W / (TAU0 + W)
    print(f"  {a:11.1f} {tw:11.2f} {e_a:+8.4f} {1.0:+6.2f} {v_pm(S0, TAU0, a):11.2f}")
print(f"  e_a = (1/2) * 2sqrt(r/a) / (tau + 2sqrt(r/a)) < 1/2 always and -> 0 as a -> oo;")
print(f"  e_s = 1 identically.  Hard cap as a -> oo: v -> s/tau = {S0/TAU0:.1f} m/s.")
print(f"  So at the measured operating point e_s/e_a = {1/(0.5*2*math.sqrt(R_NEED/A_H0)/(TAU0+2*math.sqrt(R_NEED/A_H0))):.2f} "
      f"and the ratio GROWS with every further unit of thrust.")
print("  (M-DIAL-06, verified: e_s = 1, 0 < e_a < 1/2, |e_tau| < 1 over the whole domain.)")

print("\n" + "=" * 96)
print("C7's OWN CITED SPREADS, as verified by the math checks")
print("=" * 96)
for lab, val, src in (("elasticity endpoints (range/accel/TWR)", 2.326, "M-EMP-11 verified"),
                      ("seen-course table largest/smallest", 3.992, "M-SIMULATOR-07 verified"),
                      ("ten independent speed bounds", 3.050, "M-EXAMINER-08 verified"),
                      ("dodge range vs in-vehicle rivals (max)", 7.57, "M-SIMULATOR-12"),
                      ("my 20 % relaxation, dodge", 2.23, "this refuter, part 1"),
                      ("my factor-2 relaxation, dodge", g[0] / max(g[1], 1e-9), "this script"),
                      ("my feasible-hardware relaxation", 5.26, "this refuter, part 1")):
    print(f"  {lab:42s} {val:7.3f}  {'>2' if val > 2 else '<=2'}   [{src}]")
print("\nDONE")
