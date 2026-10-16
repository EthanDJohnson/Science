#!/usr/bin/env python3
"""Falsifier C5-0: is the ACTUATOR ENVELOPE active at the MEASURED hardware values?

C5 claims thrust authority (5a) and the constant-altitude torque ceiling (5b) bind first on a
seen course at 15-20 m/s, and that the motor time constant (5c) is eliminated.

Part A  -- arithmetic on the simulator lens's OWN logged rows
          (calc/lens-simulator_sweep.py.log), recomputing every elasticity at the MEASURED
          hardware value (f_max = 8.5 N per rotor, T/W 4.6227; motor_tau = 39.1 ms) and in the
          RELAXATION direction the brief's definition of "binds first" requires.

Part B  -- the row the lens never printed.  Its own script has a section [5] THRUST-TO-WEIGHT
          at the tight gate tolerance (0.20 m), but the run died on the 585 s timeout
          (exit 124) before reaching it, so every thrust number in C5 comes from the LOOSE
          (0.50 m) tolerance, which the lens itself says only "shows WHICH limit binds" and
          lacks the resolution to say how much.  Here I run that missing section, plus the
          motor_tau rows at the same tolerance as a reproduction check, with the speed grid
          extended above the nominal reference-family ceiling so the thrust arm is not
          censored by it.

All SI units.  Plant, controller and course are the lens's own module, unmodified.
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

G = 9.80665
DT = 2e-3
LOOSE = M.Slalom(tol=0.50)
TIGHT = M.Slalom(tol=0.20)
S_PATH = LOOSE.arclength()
A_H = platform_sun2022().hover()["a_max_horizontal"]
T_OPT = M.time_optimal_path_time(LOOSE, A_H, np.inf)["t_opt"]


def el(v1, v2, x1, x2):
    return math.log(v2 / v1) / math.log(x2 / x1)


print("=" * 96)
print("PART A: elasticities at the MEASURED values, from the lens's own logged speeds")
print("=" * 96)
print(f"  path {S_PATH:.3f} m, t_opt {T_OPT:.4f} s, a_h {A_H:.3f} m/s^2")
print("  measured hardware: f_max = 8.5 N/rotor (T/W 4.6227), motor_tau = 39.1 ms  [A-03, A-13]")
print()
# rows copied verbatim from calc/lens-simulator_sweep.py.log
loose_thrust = {6.0: 16.840, 7.5: 18.943, 8.5: 19.592, 10.0: 19.600}   # v_mean, tol 0.50
loose_Ustar = {6.0: 15.500, 7.5: 17.450, 8.5: 18.050, 10.0: 18.050}
tight_tau = {5.0: 19.862, 10.0: 19.862, 19.55: 18.719, 39.1: 16.165, 78.2: 7.954}  # tol 0.20
tight_Ustar = {5.0: 18.200, 10.0: 18.200, 19.55: 17.150, 39.1: 14.875, 78.2: 7.375}

print("  (A1) thrust, tol 0.50 m -- the arc C5 quotes vs the arc at the measured value")
print(f"      6.0 -> 7.5 N  (both BELOW the installed 8.5 N): e = "
      f"{el(loose_thrust[6.0], loose_thrust[7.5], 6.0, 7.5):+.4f}   <- C5's +0.527")
print(f"      8.5 -> 10.0 N (relaxing the INSTALLED limit):   e = "
      f"{el(loose_thrust[8.5], loose_thrust[10.0], 8.5, 10.0):+.4f}")
print(f"      gain from +17.6 per cent of installed thrust: "
      f"{100*(loose_thrust[10.0]/loose_thrust[8.5]-1):+.3f} per cent of mean speed, "
      f"U* {loose_Ustar[8.5]:.3f} -> {loose_Ustar[10.0]:.3f} m/s "
      f"(delta {loose_Ustar[10.0]-loose_Ustar[8.5]:+.3f})")
print()
print("  (A2) motor time constant, tol 0.20 m -- the arc C5 quotes vs the arc at the measured value")
print(f"      5 -> 10 ms   (both FAR BELOW the measured 39.1 ms): e = "
      f"{el(tight_tau[5.0], tight_tau[10.0], 5.0, 10.0):+.4f}   <- C5's 'exactly 0.000'")
print(f"      39.1 -> 19.55 ms (halving the MEASURED lag):        e = "
      f"{el(tight_tau[39.1], tight_tau[19.55], 39.1, 19.55):+.4f}")
print(f"      39.1 -> 10 ms:                                     e = "
      f"{el(tight_tau[39.1], tight_tau[10.0], 39.1, 10.0):+.4f}")
print(f"      gain from halving the measured lag: "
      f"{100*(tight_tau[19.55]/tight_tau[39.1]-1):+.2f} per cent of mean speed")
print(f"      gain from 39.1 -> 10 ms:            "
      f"{100*(tight_tau[10.0]/tight_tau[39.1]-1):+.2f} per cent "
      f"(U* {tight_Ustar[39.1]:.3f} -> {tight_Ustar[10.0]:.3f}, reported AT FAMILY CEILING,"
      f" so a LOWER bound)")
print()
ratio = abs(el(tight_tau[39.1], tight_tau[19.55], 39.1, 19.55)) / abs(
    el(loose_thrust[8.5], loose_thrust[10.0], 8.5, 10.0))
print(f"  (A3) at the measured values, |e(motor_tau)| / e(installed thrust) = {ratio:.1f}")
print()
print("  (A4) is the envelope even touched at the tight tolerance?  lens's own baseline rows:")
print("      tol 0.50 baseline: U*=18.050, sat=32.0 per cent, peak 8.46 of 8.5 N -> envelope ACTIVE")
print("      tol 0.20 baseline: U*=14.875, sat= 0.0 per cent, peak 7.32 of 8.5 N -> envelope IDLE")
print(f"      reference-family ceiling at nominal T/W: U_feas = {LOOSE.ref_feasible_U(A_H):.4f} m/s;"
      f" the tol-0.50 baseline U* = 18.050 is {100*18.050/LOOSE.ref_feasible_U(A_H):.1f} per cent of it,")
print(f"      and the family's own demand there is |a| = {3.0*(2*math.pi/30.0)**2*18.050**2:.2f} m/s^2 = "
      f"{100*3.0*(2*math.pi/30.0)**2*18.050**2/A_H:.1f} per cent of a_h BY CONSTRUCTION.")
print()
print("  (A5) the hardware anchor A-16 (planner T/W sweep): 2.5 -> 3.6 on a platform of T/W ~4,")
print("       'planner bound deliberately below the platform limit' [dossier A-16, D-36] --")
print("       so the +0.565 anchor is an elasticity to a COMMANDED bound, not to installed thrust.")
print(f"       e(lap) = {el(7.14, 5.81, 2.5, 3.6):+.4f} recomputed from the dossier's two lap times.")
print()

print("=" * 96)
print("PART B: the missing section [5] at gate tol 0.20 m (plant perturbed, controller nominal)")
print("=" * 96)
BASE = dict(tau_imu=1e-3, tau_vio=20e-3, f_inner=500.0, f_outer=200.0)
GRID2 = (7.0, 10.0, 13.0, 15.5, 17.0, 18.2, 19.4, 20.6, 21.8)


def u_max(q, ctl, course, grid=GRID2, refine=3):
    good, bad = None, None
    for U in grid:
        r = M.run_course(q, ctl, course, U, dt=DT)
        if r["ok"]:
            good = (U, r)
        else:
            bad = (U, r)
            break
    if good is None:
        return {"U": float("nan"), "best": None,
                "note": f"fails at U = {grid[0]}, mode {bad[1]['failure_mode']}"}
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


def report(label, q, ctl, course=TIGHT):
    t0 = time.time()
    out = u_max(q, ctl, course)
    r = out["best"]
    uf = course.ref_feasible_U(q.hover()["a_max_horizontal"])
    if r is None:
        print(f"  {label:34s}  {out['note']}")
        return {"v": float("nan"), "U": float("nan")}
    print(f"  {label:34s} U*={out['U']:6.3f} v={r['v_mean_path']:6.3f} m/s "
          f"t={r['t_finish']:5.3f}s frac={T_OPT/r['t_finish']:5.3f} "
          f"err={r['worst_gate_err']:5.3f}m pk={r['peak_rotor_thrust']:5.2f}N "
          f"sat={r['sat_fraction']*100:4.1f}% w_r={ctl.w_rate:6.2f} "
          f"U_feas={uf:5.2f} [{out['note']}, {time.time()-t0:.0f}s]")
    return {"v": r["v_mean_path"], "U": out["U"], "sat": r["sat_fraction"],
            "pk": r["peak_rotor_thrust"], "note": out["note"]}


q0 = platform_sun2022()
res = {}
print("\n  reproduction checks (these rows exist in the lens's log; must match):")
res["base"] = report("f_max 8.5 N, tau 39.1 ms (base)", q0, M.Cascade(q0, **BASE))
qv = q0.variant(motor_tau=19.55e-3)
res["tau19"] = report("tau 19.55 ms, f_max 8.5 N", qv, M.Cascade(qv, **BASE))
qv = q0.variant(motor_tau=10e-3)
res["tau10"] = report("tau 10 ms, f_max 8.5 N", qv, M.Cascade(qv, **BASE))
print("\n  NEW: relaxing the INSTALLED thrust envelope at the tight tolerance:")
for fm in (10.0, 12.0):
    qv = q0.variant(thrust_max=fm)
    res[f"f{fm}"] = report(f"f_max {fm:4.1f} N (T/W {qv.hover()['thrust_to_weight']:4.2f}),"
                           f" tau 39.1", qv, M.Cascade(qv, **BASE))
print("\n  control: both relaxed together")
qv = q0.variant(thrust_max=12.0, motor_tau=10e-3)
res["both"] = report("f_max 12 N + tau 10 ms", qv, M.Cascade(qv, **BASE))

print("\n" + "=" * 96)
print("VERDICT ARITHMETIC (tol 0.20 m, measured values as the base point)")
print("=" * 96)
b = res["base"]["v"]
for k, lab, x1, x2 in (("f10.0", "installed thrust 8.5 -> 10 N", 8.5, 10.0),
                       ("f12.0", "installed thrust 8.5 -> 12 N", 8.5, 12.0),
                       ("tau19", "motor_tau 39.1 -> 19.55 ms", 39.1, 19.55),
                       ("tau10", "motor_tau 39.1 -> 10 ms", 39.1, 10.0),
                       ("both", "both", 1.0, 1.0)):
    v = res[k]["v"]
    if not np.isfinite(v):
        continue
    gain = 100 * (v / b - 1)
    e = el(b, v, x1, x2) if x1 != x2 else float("nan")
    print(f"  {lab:32s} v = {v:6.3f} m/s  gain {gain:+6.2f} per cent   e = {e:+.4f}"
          f"   [{res[k]['note']}, sat {100*res[k]['sat']:.1f} per cent, pk {res[k]['pk']:.2f} N]")
print()
print("  C5 (5a) requires that relaxing the installed thrust envelope at the measured value")
print("  produce the largest gain.  Compare the two columns above.")
