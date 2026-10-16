#!/usr/bin/env python3
"""Falsifier C5-0, part C: does the motor-lag gain come from the PLANT or from the retuning?

In the lens's model the rate-loop gain is retuned by w_rate = min(crossover(tau_in, motor_tau),
60 rad/s), so cutting motor_tau both removes plant lag and raises the gain.  The lens's own
fixed-gain control section never ran (its sweep died on the 585 s timeout).  Here it is, at the
tight gate tolerance, with w_rate held at the baseline 39.938 rad/s:

  (C1) motor_tau 39.1 -> 19.55 -> 10 ms at FIXED gains: plant-only effect.
  (C2) installed thrust 8.5 -> 12 N at the RELAXED gain (w_rate = 60): does thrust matter once
       the bandwidth is freed?
SI units.
"""
from __future__ import annotations

import importlib.util
import math
import os
import sys
import time

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(_ROOT, ".claude", "skills", "conundrum", "scripts"))
from quadrotor import platform_sun2022  # noqa: E402

_spec = importlib.util.spec_from_file_location(
    "simmodel", os.path.join(_HERE, "lens-simulator_model.py"))
M = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(M)

DT = 2e-3
TIGHT = M.Slalom(tol=0.20)
A_H = platform_sun2022().hover()["a_max_horizontal"]
T_OPT = M.time_optimal_path_time(M.Slalom(tol=0.50), A_H, np.inf)["t_opt"]
GRID = (7.0, 10.0, 13.0, 15.5, 17.0, 18.2, 19.4, 20.6, 21.8)
BASE = dict(tau_imu=1e-3, tau_vio=20e-3, f_inner=500.0, f_outer=200.0)


def u_max(q, ctl, course, grid=GRID, refine=3):
    good, bad = None, None
    for U in grid:
        r = M.run_course(q, ctl, course, U, dt=DT)
        if r["ok"]:
            good = (U, r)
        else:
            bad = (U, r)
            break
    if good is None:
        return {"U": float("nan"), "best": None, "note": "fails at grid floor"}
    if bad is None:
        return {"U": good[0], "best": good[1], "note": "GRID CEILING"}
    a, b = good[0], bad[0]
    for _ in range(refine):
        mid = 0.5 * (a + b)
        r = M.run_course(q, ctl, course, mid, dt=DT)
        if r["ok"]:
            a, good = mid, (mid, r)
        else:
            b, bad = mid, (mid, r)
    return {"U": a, "best": good[1], "note": bad[1]["failure_mode"]}


def report(label, q, ctl):
    t0 = time.time()
    out = u_max(q, ctl, TIGHT)
    r = out["best"]
    if r is None:
        print(f"  {label:38s}  {out['note']}")
        return float("nan")
    print(f"  {label:38s} U*={out['U']:6.3f} v={r['v_mean_path']:6.3f} m/s "
          f"frac={T_OPT/r['t_finish']:5.3f} pk={r['peak_rotor_thrust']:5.2f}N "
          f"sat={r['sat_fraction']*100:4.1f}% w_r={ctl.w_rate:6.2f} "
          f"[{out['note']}, {time.time()-t0:.0f}s]")
    return r["v_mean_path"]


q0 = platform_sun2022()
WF = M.max_crossover_for_pm(2e-3, 0.0391, 40.0)
print(f"baseline rate gain held fixed at w_rate = {WF:.3f} rad/s\n")
print("(C1) FIXED gains, motor_tau swept (plant-only effect):")
v = {}
for tm in (39.1e-3, 19.55e-3, 10e-3):
    qv = q0.variant(motor_tau=tm)
    v[tm] = report(f"FIXED w_r, motor_tau = {tm*1e3:5.2f} ms", qv,
                   M.Cascade(qv, **BASE, w_rate_fixed=WF))
print(f"  fixed-gain elasticity 39.1 -> 19.55 ms: "
      f"{math.log(v[19.55e-3]/v[39.1e-3])/math.log(19.55/39.1):+.4f}; "
      f"gain {100*(v[19.55e-3]/v[39.1e-3]-1):+.2f} per cent")
print(f"  fixed-gain gain 39.1 -> 10 ms: {100*(v[10e-3]/v[39.1e-3]-1):+.2f} per cent")

print("\n(C2) thrust envelope relaxed WITH the bandwidth freed (motor_tau 10 ms, w_rate 60):")
vt = {}
for fm in (8.5, 12.0):
    qv = q0.variant(thrust_max=fm, motor_tau=10e-3)
    vt[fm] = report(f"motor_tau 10 ms, f_max = {fm:4.1f} N", qv, M.Cascade(qv, **BASE))
print(f"  gain from 8.5 -> 12 N at freed bandwidth: {100*(vt[12.0]/vt[8.5]-1):+.2f} per cent")
