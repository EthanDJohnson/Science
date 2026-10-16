#!/usr/bin/env python3
"""M-SIMULATOR-06: when the delay, not the actuator lag, caps the rate loop.

CLAIM (lens finding 4, candidate SIMULATOR-B): "the binding term is the actuator pole at
1/0.0391 = 25.6 rad/s, not the delay ... The delay only takes over above tau_in of about
5 ms with a 5 ms actuator, or about 20 ms with no actuator lag."

STATEMENT CHECKED. Two readings, since the lens does not define "takes over":
(R1) the delay's phase lag at the PM = 40 deg crossover exceeds the lag's:
     w_c tau > atan(w_c T_m), i.e. each term takes half of the 50 deg budget at the
     threshold tau*(T_m);
(R2) the delay alone restricts the achievable gain to at or below the baseline value
     w = 39.938 rad/s obtained with tau = 2 ms and T_m = 39.1 ms, i.e.
     tau* = radians(50 deg)/39.938.

SYMBOLS / DOMAIN. tau >= 0 s inner-loop delay; T_m >= 0 s actuator time constant;
w_c > 0 rad/s crossover at PM = 40 deg; everything else as in M-SIMULATOR-04.

INDEPENDENT DERIVATION. From PM = 90 deg - (w_c tau + atan(w_c T_m)) = 40 deg, at the
threshold of R1 both terms equal 25 deg, so w_c = tan(25 deg)/T_m and
tau* = radians(25 deg) T_m/tan(25 deg). For R2, with T_m = 0 the gain equals the crossover
and w = radians(50 deg)/tau.
"""
import sys
from math import atan, degrees, radians, sqrt, tan

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import finish, identity, inequality, quantity, units  # noqa: E402

PM, TM_BASE, TAU_BASE = 40.0, 0.0391, 0.002
budget = radians(90.0 - PM)


def solve(tau, Tm):
    lo, hi = 1e-9, 1e7
    for _ in range(300):
        mid = 0.5 * (lo + hi)
        if 90.0 - degrees(mid * tau) - degrees(atan(mid * Tm)) > PM:
            lo = mid
        else:
            hi = mid
    wc = 0.5 * (lo + hi)
    return wc, wc * sqrt(1 + (wc * Tm) ** 2)


wc_base, w_base = solve(TAU_BASE, TM_BASE)
print("=== inputs (SI) ===")
print(f"PM target {PM} deg, total phase budget {degrees(budget):.1f} deg")
print(f"baseline tau = {TAU_BASE*1e3} ms, T_m = {TM_BASE*1e3} ms -> w_c = {wc_base:.4f} rad/s, "
      f"w = {w_base:.4f} rad/s")
print(f"phase split there: delay {degrees(wc_base*TAU_BASE):.3f} deg vs lag "
      f"{degrees(atan(wc_base*TM_BASE)):.3f} deg -> ratio {degrees(atan(wc_base*TM_BASE))/degrees(wc_base*TAU_BASE):.1f}")
print(f"actuator pole 1/T_m = {1/TM_BASE:.4f} rad/s; crossover/pole = {wc_base*TM_BASE:.4f}")

print("\n=== reading R1: equal phase contributions ===")
for Tm_ms in (5.0, 10.0, 39.1):
    Tm = Tm_ms * 1e-3
    wc_star = tan(radians(25.0)) / Tm
    tau_star = radians(25.0) / wc_star
    # confirm by solving with that tau
    wc_chk, _ = solve(tau_star, Tm)
    print(f"  T_m = {Tm_ms:5.1f} ms: w_c* = {wc_star:8.3f} rad/s, tau* = {tau_star*1e3:7.3f} ms "
          f"(re-solved w_c = {wc_chk:8.3f} rad/s)")
tau_star_5ms = radians(25.0) / (tan(radians(25.0)) / 0.005)

print("\n=== reading R2: delay alone matched to the baseline achievable gain ===")
tau_r2 = budget / w_base
print(f"  tau* with no actuator lag = {degrees(budget):.1f} deg in rad / {w_base:.3f} rad/s "
      f"= {tau_r2*1e3:.3f} ms")
for tau_ms in (5.0, 14.5, 20.0, 21.85):
    _, w = solve(tau_ms * 1e-3, 1e-12)
    print(f"  tau = {tau_ms:6.2f} ms, no lag: achievable w = {w:9.3f} rad/s "
          f"({'below' if w < w_base else 'above'} the 39.938 rad/s baseline)")

print("\n=== sensitivity of the achievable gain, one term at a time ===")
for tau_ms in (0.0, 1.0, 2.0, 5.0, 10.0, 20.0):
    _, w = solve(tau_ms * 1e-3, TM_BASE)
    print(f"  tau = {tau_ms:5.1f} ms, T_m = 39.1 ms: w = {w:8.3f} rad/s")
for Tm_ms in (0.0, 5.0, 10.0, 19.55, 39.1, 78.2):
    _, w = solve(TAU_BASE, max(Tm_ms, 1e-9) * 1e-3)
    print(f"  T_m = {Tm_ms:5.2f} ms, tau = 2 ms: w = {w:9.3f} rad/s")

print("\n=== checks ===")
quantity(f"{tau_star_5ms*1e3:.4f}", "5.0", rel_tol=0.07)        # R1 with a 5 ms actuator, "about 5 ms"
quantity(f"{tau_r2*1e3:.4f}", "20.0", rel_tol=0.10)             # R2 with no lag, "about 20 ms"
quantity(f"{1/TM_BASE:.4f}", "25.6", rel_tol=2e-3)
inequality(f"{degrees(atan(wc_base*TM_BASE)):.4f}", ">", f"{degrees(wc_base*TAU_BASE):.4f}")
# R1 threshold in closed form: tau* = radians(25 deg) * T_m / tan(25 deg), linear in T_m
import sympy as sp  # noqa: E402

T_ = sp.Symbol("T_m", positive=True)
identity((sp.pi / 180 * 25) * T_ / sp.tan(sp.pi / 180 * 25),
         T_ * sp.Rational(25, 180) * sp.pi / sp.tan(sp.pi * sp.Rational(25, 180)))
# the lag's phase at any frequency is below the pure-delay phase of an equal time constant
inequality("atan(w*T)", "<", "w*T", domain={"w": (0.1, 100), "T": (0.001, 0.1)})
units("(0.43633) / (93.26 s^-1)", "time")
units("0.0391 s * 25.5754 s^-1", "dimensionless")
raise SystemExit(finish())
