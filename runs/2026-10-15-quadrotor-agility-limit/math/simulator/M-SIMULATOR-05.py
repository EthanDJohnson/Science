#!/usr/bin/env python3
"""M-SIMULATOR-05: the delay margins of the designed rate and velocity loops.

CLAIM (lens finding 12, candidate SIMULATOR-C): L_inner(s) = (39.938/s)/(1 + 0.0391 s) has
gain crossover 27.303 rad/s, phase margin 43.13 deg and delay margin 27.57 ms, against a
2.00 ms inner budget (7.3 per cent used); L_outer(s) = 4.438/s has delay margin 354.0 ms,
matching pi/(2 w), against a 22.50 ms outer budget (6.4 per cent used).

SYMBOLS / DOMAIN. w > 0 rad/s loop gain; T_m = 0.0391 s actuator time constant; w_c > 0 the
frequency where |L| = 1; PM in deg; delay margin DM = PM(rad)/w_c in s (the extra pure delay
that would drive the phase margin to zero at the existing crossover, the standard SISO
definition, exact because a pure delay does not change |L|). Budgets: inner
tau_imu + T_inner/2 = 1 + 1 = 2.00 ms; outer tau_vio + T_outer/2 = 20 + 2.5 = 22.50 ms.

INDEPENDENT DERIVATION. Crossover from w = w_c sqrt(1 + (w_c T_m)^2); PM = 90 deg -
atan(w_c T_m); DM = PM(rad)/w_c. For the pure integrator PM = 90 deg so DM = pi/(2 w).
"""
import sys
from math import atan, degrees, pi, radians, sqrt

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import finish, identity, inequality, limit, quantity, units  # noqa: E402

W_IN, TM = 39.938, 0.0391
W_OUT = 4.438
BUDGET_IN, BUDGET_OUT = 0.002, 0.0225


def crossover(w, Tm):
    lo, hi = 1e-9, 1e7
    for _ in range(300):
        mid = 0.5 * (lo + hi)
        if mid * sqrt(1 + (mid * Tm) ** 2) < w:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


wc_in = crossover(W_IN, TM)
pm_in = 90.0 - degrees(atan(wc_in * TM))
dm_in = radians(pm_in) / wc_in
wc_out = W_OUT
pm_out = 90.0
dm_out = radians(pm_out) / wc_out

print("=== inputs (SI) ===")
print(f"L_inner = {W_IN}/(s (1 + {TM} s)); L_outer = {W_OUT}/s")
print(f"budgets: inner {BUDGET_IN*1e3:.2f} ms, outer {BUDGET_OUT*1e3:.2f} ms")

print("\n=== inner loop ===")
print(f"w_c = {wc_in:.4f} rad/s (|L| = {W_IN/(wc_in*sqrt(1+(wc_in*TM)**2)):.9f} there)")
print(f"PM = {pm_in:.4f} deg, delay margin = {dm_in*1e3:.4f} ms")
print(f"budget used = {100*BUDGET_IN/dm_in:.3f} per cent")
print(f"with the 2 ms delay already in the loop, PM = {pm_in - degrees(wc_in*BUDGET_IN):.3f} deg "
      f"and the remaining margin is {(dm_in - BUDGET_IN)*1e3:.3f} ms")

print("\n=== outer loop ===")
print(f"w_c = {wc_out:.4f} rad/s, PM = {pm_out:.1f} deg, delay margin = {dm_out*1e3:.4f} ms "
      f"(closed form pi/(2w) = {pi/(2*W_OUT)*1e3:.4f} ms)")
print(f"budget used = {100*BUDGET_OUT/dm_out:.3f} per cent")

print("\n=== checks ===")
quantity(f"{wc_in:.5f}", "27.303", rel_tol=1e-4)
quantity(f"{pm_in:.4f}", "43.13", rel_tol=1e-3)
quantity(f"{dm_in:.7f} s", "27.57 ms", rel_tol=1e-3)
quantity(f"{100*BUDGET_IN/dm_in:.4f}", "7.3", rel_tol=1e-2)      # the lens quotes one decimal
quantity(f"{dm_out:.7f} s", "354.0 ms", rel_tol=1e-3)
quantity(f"{dm_out:.9f} s", f"{pi/(2*W_OUT):.9f} s", rel_tol=1e-9)
quantity(f"{100*BUDGET_OUT/dm_out:.4f}", "6.4", rel_tol=1e-2)    # the lens quotes one decimal
inequality(f"{BUDGET_IN:.6f}", "<", f"{dm_in:.6f}")
inequality(f"{BUDGET_OUT:.6f}", "<", f"{dm_out:.6f}")
# algebra: DM of a pure integrator is pi/(2w), independent of anything else
identity("(pi/2)/w", "pi/(2*w)")
# the lag-loop margin reduces to the integrator's as T_m -> 0
limit("(pi/2 - atan(w_c*T))/w_c", "T", 0, "(pi/2)/w_c", domain={"T": (0, 1.0)})
# a faster loop has a smaller delay margin: DM is strictly decreasing in w_c
inequality("(pi/2 - atan(w_c*T))/w_c", "<", "(pi/2)/w_c", domain={"T": (0.001, 1.0), "w_c": (0.1, 100)})
units("(1.5708) / (4.438 s^-1)", "time")
units("(0.7527) / (27.303 s^-1)", "time")
raise SystemExit(finish())
