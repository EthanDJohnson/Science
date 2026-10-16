#!/usr/bin/env python3
"""Refuter C4-0, simulation angle.  Does a HARDWARE limit bind at the brief's operating point?

C4 claims: "No hardware limit is active ... the bounds sit 2-7x above the operating point", and
predicts "no single hardware relaxation at its *attainable* increment moves the unseen-course
metric by more than about 20 per cent".

Three tests, all on the simulator lens's own verified 17-state plant (24/24 verification rows,
lens-simulator_verify.py.log), with the controller keeping its NOMINAL model throughout:

 (A) reproduce the lens's dodge ceilings at s = 3, 6, 10 m (tau = 50 ms) before trusting them;
 (B) hardware arm 1, perception range: the attainable 6 -> 10 m sensor swap, per-cent gain
     against C4's own 20 per cent falsification threshold;
 (C) hardware arm 2, two pure-hardware caps evaluated AT the operating point:
       - usable stereo range 4.1 and 5.8 m (M-MECH-06 verified: depth noise equals a 0.1 m
         obstacle's size there for a 50 mm baseline), and
       - the lateral acceleration a body-fixed 58 deg vertical FoV at 30 deg up-tilt permits,
         a_u = g tan(29 + 30 deg) = 16.33 m/s^2 (M-MECH-02 verified),
     each compared with the measured unseen-course points 7 m/s (8/10) and 10 m/s (6/10) [A-20].
 (D) arithmetic on C4's own bound table (M-EXAMINER-08 verified anchors).

SI units.  dt = 1 ms.  Obstacle radius 0.5 m, vehicle radius 0.25 m (the lens's geometry).
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

G = 9.80665
DT = 1e-3
BASE = dict(tau_imu=1e-3, tau_vio=20e-3, f_inner=500.0, f_outer=200.0)
q0 = platform_sun2022()
A_H = q0.hover()["a_max_horizontal"]
R_OBS, R_VEH = 0.5, 0.25
NEED = R_OBS + R_VEH
print(__doc__)
print(f"platform: m = {q0.mass} kg, T/W = {q0.hover()['thrust_to_weight']:.4f}, "
      f"a_h = {A_H:.3f} m/s^2, motor_tau = {q0.motor_tau*1e3:.1f} ms")


def dodge(q, ctl, v, s, tau_lat, dt=DT, a_cmd=None):
    """Fly at v along +x; after tau_lat command lateral a_cmd.  Lateral offset reached by x = s.
    Identical to lens-simulator_lookahead.py's dodge()."""
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


def v_ceiling(q, s, tau_lat, a_cmd=None, lo=1.0, hi=40.0, nbis=11):
    ctl = M.Cascade(q, **BASE)
    for _ in range(nbis):
        mid = 0.5 * (lo + hi)
        d, reached = dodge(q, ctl, mid, s, tau_lat, a_cmd=a_cmd)
        if d >= NEED and reached:
            lo = mid
        else:
            hi = mid
    return lo


print("\n" + "=" * 92)
print("(A) REPRODUCTION of the lens's dodge ceilings (tau = 50 ms, full a_h, nominal hardware)")
print("=" * 92)
LENS = {3.0: 8.541, 6.0: 16.920, 10.0: 29.412}
rep = {}
for s in (3.0, 6.0, 10.0):
    v = v_ceiling(q0, s, 0.050)
    rep[s] = v
    print(f"  s = {s:5.1f} m: v_max = {v:7.3f} m/s   lens {LENS[s]:7.3f} m/s   "
          f"rel diff {abs(v-LENS[s])/LENS[s]*100:5.2f} %  "
          f"{'REPRODUCES' if abs(v-LENS[s])/LENS[s] < 0.02 else 'DOES NOT REPRODUCE'}")

print("\n" + "=" * 92)
print("(B) HARDWARE ARM 1 -- perception range, attainable increment 6 -> 10 m")
print("=" * 92)
e_range = math.log(rep[10.0] / rep[6.0]) / math.log(10.0 / 6.0)
gain = (rep[10.0] / rep[6.0] - 1) * 100
print(f"  elasticity d ln v / d ln s (6 -> 10 m) = {e_range:+.3f}")
print(f"  per-cent change in the metric from this ONE hardware swap = {gain:+.1f} per cent")
print(f"  C4's own falsification threshold is 'more than about 20 per cent': "
      f"{'EXCEEDED -> C4 prediction refuted' if gain > 20 else 'not exceeded'}")
e_3_6 = math.log(rep[6.0] / rep[3.0]) / math.log(2.0)
print(f"  for reference, 3 -> 6 m: elasticity {e_3_6:+.3f}, gain "
      f"{(rep[6.0]/rep[3.0]-1)*100:+.1f} per cent")

print("\n" + "=" * 92)
print("(C) HARDWARE CAPS EVALUATED AT THE OPERATING POINT (unseen course, [A-20])")
print("=" * 92)
A_U = G * math.tan(math.radians(29.0 + 30.0))
print(f"  FoV-permitted lateral acceleration a_u = g tan(59 deg) = {A_U:.3f} m/s^2 "
      f"({A_U/G:.2f} g), against a_h = {A_H:.2f} m/s^2")
rows = []
for s, a_cmd, label in ((4.1, None, "usable stereo range 4.1 m, full a_h"),
                        (5.8, None, "usable stereo range 5.8 m, full a_h"),
                        (6.0, A_U, "range 6 m, FoV-capped lateral a_u"),
                        (4.1, A_U, "range 4.1 m, FoV-capped lateral a_u")):
    v = v_ceiling(q0, s, 0.050, a_cmd=a_cmd)
    rows.append((label, v))
    print(f"  {label:42s}: v_max = {v:6.3f} m/s   "
          f"margin over 7 m/s = {v/7.0:5.2f}x,  over 10 m/s = {v/10.0:5.2f}x")
worst = min(r[1] for r in rows)
print(f"  LOWEST hardware-capped ceiling = {worst:.3f} m/s; C4 asserts every bound sits "
      f"2-7x above the operating point.")
print(f"  ratio to the 7 m/s point (8/10 success, [A-20]) = {worst/7.0:.2f}x  -> "
      f"{'inside C4 claim' if worst/7.0 >= 2.0 else 'BELOW 2x: C4 claim refuted at this point'}")
print(f"  ratio to the 10 m/s point (6/10 success, [A-20]) = {worst/10.0:.2f}x")

print("\n" + "=" * 92)
print("(D) HARDWARE ARM 2 -- thrust authority at fixed range (controller nominal-model kept)")
print("=" * 92)
for fm in (8.5, 6.0, 4.5):
    qv = q0.variant(thrust_max=fm)
    h = qv.hover()
    v = v_ceiling(qv, 6.0, 0.050, a_cmd=min(A_H, h["a_max_horizontal"]))
    print(f"  thrust_max {fm:4.1f} N/rotor (T/W {h['thrust_to_weight']:.2f}, "
          f"a_h {h['a_max_horizontal']:6.2f} m/s^2): v_max at s = 6 m = {v:6.3f} m/s")

print("\n" + "=" * 92)
print("(E) C4's OWN BOUND TABLE, read at the speed where success actually fails")
print("=" * 92)
LOWEST, HIGHEST = 10.7301, 32.7249   # M-EXAMINER-08 verified
for v_op, succ in ((5.0, "10/10"), (7.0, "8/10"), (10.0, "6/10")):
    print(f"  {v_op:5.1f} m/s ({succ}): {v_op/LOWEST:.3f} of the lowest bound, "
          f"{v_op/HIGHEST:.3f} of the highest")
print("  C4's headline reads 'a quarter to a half of EVERY limit'; at the speed where the "
      "90-per-cent")
print(f"  clause actually fails (10 m/s) the system is at {10.0/LOWEST:.2f} of the lowest bound, "
      f"i.e. {100*(1-10.0/LOWEST):.1f} per cent short of it.")
print("  The two lowest of the ten bounds are the thrust bang-bang mean (10.7301 m/s) and the "
      "FoV-capped")
print("  stop bound (10.8499 m/s) -- both HARDWARE bounds -- agreeing to 1.11 per cent "
      "[M-EXAMINER-08].")
