#!/usr/bin/env python3
"""Refuter 0 against C2 ("state estimation binds first through DRIFT and feature loss").

Three experiments, all SI units.

(0) REPRODUCTION CHECK of the simulator lens's plant and controller: the nominal run at
    U = 12 m/s on the 0.50 m-tolerance slalom must give the logged mean path speed
    13.053 m/s and the logged verification diagnostics.  If this fails, nothing below counts.

(1) THE DRIFT ELASTICITY the slate does not have.  The lens's loop has latency and white
    noise but no drift, and C2's own "evidence against" line concedes there is no measured
    drift in m per m.  I add a position-drift channel of rate rho (metres of estimate error
    per metre flown) and measure the largest flyable reference rate U* as a function of rho,
    in TWO reference architectures:
      GLOBAL   -- the reference is a world-frame trajectory, so the whole accumulated drift
                  d(t) = rho * (distance flown) enters the gate error.  This is the MAPPED /
                  SEEN-track regime (Swift, MonoRace), where gates have known world poses.
      RELATIVE -- the gate is perceived at look-ahead distance s_look and its target is
                  stored in the frame of the estimate AT THAT MOMENT, so the error that
                  reaches the gate is only the drift accumulated between detection and
                  passage, |d(t) - d(t - s_look/U)| <= rho * s_look.  This is the brief's
                  UNSEEN-course regime: there is no world-frame target to miss.
    Implementation: an estimate offset d(t) added to the measured position is exactly a
    reference offset -d(t) (the loop drives p_true -> p_ref - d), so the drift is injected
    through the reference wrapper and scored against the TRUE course geometry.

(2) FEATURE LOSS, costed as IMU-only coasting.  During a blur/feature-loss event the
    estimator coasts on the IMU.  I compute the velocity and position error that accrues
    against the loop's own measured tolerance from the lens's failure boundary (survives
    sigma_v = 0.50 m/s and sigma_p = 0.10 m; fails at 1.00 m/s and 0.20 m), for datasheet-
    grade accelerometer noise density and post-calibration bias.

Plant verification is the lens's 24/24 table in lens-simulator_verify.py.log; the
load-bearing rows are repeated by the reproduction check below.
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

DT = 2e-3
BASE = dict(tau_imu=1e-3, tau_vio=20e-3, f_inner=500.0, f_outer=200.0)
q0 = platform_sun2022()
LOOSE = M.Slalom(tol=0.50)
print(__doc__)

# ---------------------------------------------------------------- (0) reproduction check
dg = q0.variant(enable_drag=False, enable_h_force=False, motor_tau=0.0).diagnostics(
    dt=1e-3, t_end=2.0, rk4_dt=0.02)
ctl0 = M.Cascade(q0, **BASE)
t0 = time.time()
r0 = M.run_course(q0, ctl0, LOOSE, 12.0, dt=DT)
t_one = time.time() - t0
print("(0) REPRODUCTION CHECK")
print(f"    angular-momentum drift {dg['angular_momentum_drift']:.2e} (lens: 7.1e-15)")
print(f"    RK4 order {dg['rk4_order']:.3f} (lens: 4.005)")
print(f"    nominal U = 12 m/s: ok={r0['ok']}, mean path speed {r0['v_mean_path']:.3f} m/s "
      f"(lens logged 13.053 m/s), worst gate error {r0['worst_gate_err']:.3f} m")
ok_repro = (abs(r0['v_mean_path'] - 13.053) < 0.05) and r0['ok']
print(f"    REPRODUCES: {ok_repro}   (one run costs {t_one:.2f} s at dt = {DT*1e3:.0f} ms)")


# ---------------------------------------------------------------- (1) the drift channel
class DriftRef:
    """course.ref(t, U) with a position-drift offset subtracted from the reference.

    mode 'global'   : offset = rho * s(t) * ehat                (accumulates over the lap)
    mode 'relative' : offset = rho * (s(t) - s(t - s_look/U)) * ehat = rho * s_look * ehat
                      (re-anchored at every detection; no world-frame target)
    ehat is the horizontal direction worst for the gate score (lateral, +y).
    """

    def __init__(self, course, U, rho, mode, s_look=6.0, ehat=(0.0, 1.0, 0.0)):
        self.c, self.U, self.rho, self.mode = course, U, rho, mode
        self.s_look, self.e = s_look, np.asarray(ehat, float)
        self.t_total = course.x_end / U
        self.v0 = float(np.linalg.norm(course.dpdx(0.0) * U))
        # path length flown as a function of time (x = U t on this reference)
        self._xs = np.linspace(0.0, course.x_end * 1.8, 4001)
        sp = np.sqrt(1.0 + (course.A * course.k * np.cos(course.k * self._xs)) ** 2)
        self._s = np.concatenate([[0.0], np.cumsum(0.5 * (sp[1:] + sp[:-1])
                                                   * np.diff(self._xs))])

    def s_of_t(self, t):
        return float(np.interp(max(t, 0.0) * self.U, self._xs, self._s))

    def offset(self, t):
        if self.rho <= 0.0:
            return np.zeros(3), np.zeros(3)
        if self.mode == "global":
            d = self.rho * self.s_of_t(t)
            dd = self.rho * self.U * np.linalg.norm(self.c.dpdx(self.U * max(t, 0.0)))
        else:
            dt_blind = self.s_look / self.U
            d = self.rho * (self.s_of_t(t) - self.s_of_t(t - dt_blind))
            dd = 0.0            # saturated: constant offset once the pipeline is full
        return d * self.e, dd * self.e

    def __call__(self, t):
        p, v, a, j = self.c.ref(t, self.U)
        d, dd = self.offset(t)
        return p - d, v - dd, a, self.U * t


def max_U(rho, mode, s_look=6.0, lo=4.0, hi=22.0, iters=5):
    """Largest reference rate U that still clears every gate within the 0.50 m tolerance."""
    best = float("nan")
    # must bracket: check hi first
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        ref = DriftRef(LOOSE, mid, rho, mode, s_look=s_look)
        r = M.run_course(q0, M.Cascade(q0, **BASE), LOOSE, mid, dt=DT, ref=ref)
        if r["ok"]:
            best, lo = mid, mid
        else:
            hi = mid
    return best


print("\n(1) ELASTICITY OF ACHIEVABLE SPEED TO ESTIMATION DRIFT RATE rho (m of error per m flown)")
print("    course 98.315 m of path, 6 gates, 0.50 m tolerance; s_look = 6 m in RELATIVE mode")
print(f"    {'rho (m/m)':>10s} {'rho (%)':>8s} {'U* global':>11s} {'U* relative':>12s}")
rhos = [0.0, 0.005, 0.02, 0.05, 0.20]
res = {}
for rho in rhos:
    ug = max_U(rho, "global")
    ur = max_U(rho, "relative")
    res[rho] = (ug, ur)
    print(f"    {rho:10.4f} {rho*100:8.2f} {ug:11.3f} {ur:12.3f}")


def elast(r1, r2, u1, u2):
    if not (np.isfinite(u1) and np.isfinite(u2) and u1 > 0 and u2 > 0):
        return float("nan")
    return math.log(u2 / u1) / math.log(r2 / r1)


print("\n    elasticities d ln U* / d ln rho:")
for a, b in [(0.005, 0.02), (0.02, 0.05), (0.05, 0.20)]:
    print(f"      rho {a:.3f} -> {b:.3f}:  global {elast(a,b,res[a][0],res[b][0]):+.3f}"
          f"   relative {elast(a,b,res[a][1],res[b][1]):+.3f}")
print("    reference elasticities from the same plant (lens findings 6 and 8):")
print("      perception range +0.986 to +1.082;  VIO latency -0.105 to -0.267;"
      " motor time constant -0.212 to -1.023")

# geometric budget, closed form, as a cross-check on the simulation
print("\n    closed-form budget cross-check (error that reaches the gate):")
for rho in (0.005, 0.02, 0.05):
    print(f"      rho = {rho*100:5.2f} %/m:  global {rho*98.315:6.3f} m over the 98.315 m lap;"
          f"  relative {rho*6.0:6.3f} m over a 6 m look-ahead;  tolerance 0.500 m")
print("    ratio of the two budgets = lap length / look-ahead = "
      f"{98.315/6.0:.2f}")

# A-20's own global budget: 40 m line, goal counted reached within 5 m
print(f"\n    A-20's unseen-course demonstration allows 5 m of goal error over a 40 m line:"
      f" {5.0/40.0*100:.1f} % of distance flown.")

# ---------------------------------------------------------------- (2) feature loss costed
print("\n(2) FEATURE LOSS PRICED AS IMU-ONLY COASTING")
print("    tolerated by the lens's own failure boundary: sigma_v = 0.50 m/s, sigma_p = 0.10 m")
print("    (fails at 1.00 m/s / 0.20 m), at U = 12 m/s on the 0.50 m gate.")
cases = [("ICM-42688-P class, noise density only", 6.9e-4, 0.0),
         ("plus 5 mg residual bias", 6.9e-4, 0.05),
         ("plus 20 mg residual bias", 6.9e-4, 0.20),
         ("plus 100 mg uncalibrated bias", 6.9e-4, 0.98)]
print(f"    {'case':42s} {'dt to dv=0.5 m/s':>18s} {'dv at 0.3 s':>12s} {'dp at 0.3 s':>12s}")
for name, na, b in cases:
    # dv(t) = b t + na sqrt(t) (random walk from white accelerometer noise), dp = 0.5 b t^2
    f = lambda t: b * t + na * math.sqrt(t) - 0.5
    lo, hi = 1e-4, 1e4
    if f(hi) < 0:
        tstar = float("inf")
    else:
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if f(mid) < 0:
                lo = mid
            else:
                hi = mid
        tstar = lo
    dv03 = b * 0.3 + na * math.sqrt(0.3)
    dp03 = 0.5 * b * 0.3 ** 2 + na * 0.3 ** 1.5 / 1.5
    print(f"    {name:42s} {tstar:18.2f} {dv03:12.4f} {dp03:12.4f}")
print("    A 0.3 s coast is already long: at 500 deg/s the blur event lasts the exposure,"
      " 1-10 ms,\n    and a full feature-loss interval in [D-12]-class flight is tens of ms.")

print("\nDONE")
