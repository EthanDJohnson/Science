#!/usr/bin/env python3
"""M-SIMULATOR-04: the closed-form phase-margin tuning rule and the achievable rate-loop gain.

CLAIM (lens findings 3 and 4, candidate SIMULATOR-B): for the rate loop
L(s) = (w/s) e^{-s tau} / (1 + s T_m) the phase margin at the gain crossover w_c is
PM = 90 deg - (w_c tau + atan(w_c T_m)) (first term in radians, converted);
with tau = 2 ms and T_m = 39.1 ms the largest w giving PM = 40 deg is w = 39.94 rad/s with
w_c = 27.3 rad/s; the actuator pole is 1/T_m = 25.6 rad/s; setting T_m = 0 raises the
achievable gain to the 400 rad/s cap; setting tau = 0 raises it only to 43.3 rad/s
("8 per cent"); and for a pure delay the closed-form crossover is 291 rad/s where a
wrapped-phase margin reader returned up to 4000 rad/s.

SYMBOLS / DOMAIN. w > 0 rad/s loop gain (an integrator gain, units 1/s); tau >= 0 s pure
transport delay; T_m > 0 s first-order actuator time constant; w_c > 0 rad/s the frequency
where |L| = 1; PM in deg. Regime: single-loop SISO, continuous time, the half-sample ZOH lag
already folded into tau.

INDEPENDENT DERIVATION. |L(j w_c)| = w/(w_c sqrt(1 + (w_c T_m)^2)) = 1 fixes w given w_c.
arg L(j w_c) = -90 deg - w_c tau (rad -> deg) - atan(w_c T_m), so
PM = 180 deg + arg L = 90 deg - (w_c tau + atan(w_c T_m)). |L| is strictly decreasing in
w_c, so the crossover is unique and PM is strictly decreasing in w_c: bisection on w_c is
exact. Nothing from the lens's scripts is used.
"""
import sys
from math import atan, degrees, pi, radians, sqrt, tan

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import finish, identity, inequality, limit, quantity, units  # noqa: E402


def pm_deg(wc, tau, Tm):
    return 90.0 - (degrees(wc * tau) + degrees(atan(wc * Tm)))


def gain_for(wc, Tm):
    return wc * sqrt(1 + (wc * Tm) ** 2)


def solve(tau, Tm, pm_target=40.0, hi=1e6):
    """Bisect on the crossover that gives the target phase margin; return (wc, w)."""
    lo, hi = 1e-9, hi
    for _ in range(300):
        mid = 0.5 * (lo + hi)
        if pm_deg(mid, tau, Tm) > pm_target:
            lo = mid
        else:
            hi = mid
    wc = 0.5 * (lo + hi)
    return wc, gain_for(wc, Tm)


TAU_IN, TM = 0.002, 0.0391
print("=== inputs (SI) ===")
print(f"tau_in = {TAU_IN*1e3:.2f} ms (tau_imu 1 ms + half of a 500 Hz period), T_m = {TM*1e3:.1f} ms")
print(f"actuator pole 1/T_m = {1/TM:.4f} rad/s")

print("\n=== numeric check of the phase-margin formula against a direct complex evaluation ===")
import cmath  # noqa: E402

for wc in (10.0, 27.3, 100.0):
    L = (1.0 / (1j * wc)) * cmath.exp(-1j * wc * TAU_IN) / (1 + 1j * wc * TM)
    direct = 180.0 + degrees(cmath.phase(L))
    print(f"  w_c = {wc:7.2f} rad/s: formula PM = {pm_deg(wc, TAU_IN, TM):8.4f} deg, "
          f"direct arg L = {direct:8.4f} deg")

print("\n=== achievable gain at PM = 40 deg ===")
cases = {
    "baseline tau = 2 ms, T_m = 39.1 ms": (TAU_IN, TM),
    "no actuator lag (T_m = 0)": (TAU_IN, 1e-12),
    "no inner delay at all (tau = 0)": (0.0, TM),
    "tau = 1 ms (tau_imu -> 0, ZOH half-period kept)": (0.001, TM),
}
res = {}
for name, (tau, Tm) in cases.items():
    wc, w = solve(tau, Tm)
    res[name] = (wc, w)
    print(f"  {name:<46s}: w_c = {wc:9.3f} rad/s, w = {w:9.3f} rad/s, PM = {pm_deg(wc, tau, Tm):.3f} deg")

base_wc, base_w = res["baseline tau = 2 ms, T_m = 39.1 ms"]
print(f"\n  phase split at the baseline crossover: delay {degrees(base_wc*TAU_IN):.3f} deg, "
      f"lag {degrees(atan(base_wc*TM)):.3f} deg")
print(f"  gain ratio, tau = 0 vs baseline: {res['no inner delay at all (tau = 0)'][1]/base_w:.4f}")
print(f"  gain ratio, tau = 1 ms vs baseline: {res['tau = 1 ms (tau_imu -> 0, ZOH half-period kept)'][1]/base_w:.4f}")
print(f"  gain ratio, T_m = 0 vs baseline: {res['no actuator lag (T_m = 0)'][1]/base_w:.4f} "
       "(before the 400 rad/s cap)")

print("\n=== pure-delay closed form w_c = (90 - PM) in rad / tau ===")
for tau_ms in (2.0, 3.0, 4.0):
    wc = radians(90.0 - 40.0) / (tau_ms * 1e-3)
    print(f"  tau = {tau_ms:.1f} ms: w_c = w = {wc:.3f} rad/s")
print(f"  the lens's 291 rad/s corresponds to tau = {radians(50.0)/291.0*1e3:.3f} ms")

print("\n=== checks ===")
quantity(f"{1/TM:.4f} rad/s", "25.6 rad/s", rel_tol=2e-3)
quantity(f"{base_w:.4f}", "39.94", rel_tol=1e-3)                   # rad/s, dimensionless compare
quantity(f"{base_wc:.4f}", "27.3", rel_tol=2e-3)
quantity(f"{base_wc/(2*pi):.4f}", "4.3", rel_tol=5e-3)             # Hz
quantity(f"{res['no inner delay at all (tau = 0)'][1]:.4f}", "43.3", rel_tol=2e-3)
quantity(f"{res['tau = 1 ms (tau_imu -> 0, ZOH half-period kept)'][1]:.4f}", "43.3", rel_tol=2e-3)
inequality(f"{res['no actuator lag (T_m = 0)'][1]:.4f}", ">", "400")
quantity(f"{radians(50.0)/0.003:.4f}", "291", rel_tol=2e-3)
# the closed form for a pure first-order lag: w_c T_m = tan(90 deg - PM)
quantity(f"{solve(0.0, TM)[0]:.6f}", f"{tan(radians(50.0))/TM:.6f}", rel_tol=1e-6)
# algebra of the crossover relation
identity("w_c*sqrt(1 + (w_c*T)**2)", "sqrt(w_c**2 + w_c**4*T**2)")
identity("atan(w_c*T)", "pi/2 - atan(1/(w_c*T))")
# limits: no delay and no lag leaves the integrator's 90 deg margin
limit("90 - (180/pi)*(w_c*tau) - (180/pi)*atan(w_c*T)", "tau", 0,
      "90 - (180/pi)*atan(w_c*T)", domain={"tau": (0, 0.1)})
limit("(180/pi)*atan(w_c*T)", "T", 0, "0", domain={"T": (0, 0.1)})
units("1 / (0.0391 s)", "frequency")
units("27.3 s^-1 * 0.002 s", "dimensionless")
raise SystemExit(finish())
