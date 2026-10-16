#!/usr/bin/env python3
"""M-EXAMINER-06  (examiner F10, candidates EXAMINER-A / EXAMINER-E)

CLAIM, stated precisely
-----------------------
At the "Swift-like operating point" s = 6 m, a = 39 m/s^2, tau = 0.040 s, the stop bound
v(s, a, tau) = a*(-tau + sqrt(tau^2 + 2 s / a)) equals 20.13 m/s, and a +10 per cent move in each
limit, one at a time, changes v by:
   range   s -> 1.1 s      : +5.23 per cent
   braking a -> 1.1 a      : +4.51 per cent
   latency tau -> 0.9 tau  : +0.66 per cent
(the latency move is -10 per cent, since less delay is better).

All three are finite-difference sensitivities of the same closed-form bound, so they are exactly
computable.  I also compare them with the first-order elasticity prediction (e * 10 per cent).
"""
import sys

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import finish, identity, quantity, units  # noqa: E402

S0, A0, T0 = 6.0, 39.0, 0.040


def v(s=S0, a=A0, tau=T0):
    return a * (-tau + (tau**2 + 2 * s / a) ** 0.5)


v0 = v()
print(f"operating point: s = {S0} m, a = {A0} m/s^2, tau = {T0*1000:.0f} ms -> v = {v0:.4f} m/s")
quantity(f"{v0:.5f} m/s", "20.13 m/s", rel_tol=1e-3)
units("39 m/s^2 * 0.04 s", "m/s")
units("2 * 6 m / (39 m/s^2)", "s^2")

moves = [("range   s +10%", v(s=1.1 * S0), 5.23),
         ("braking a +10%", v(a=1.1 * A0), 4.51),
         ("latency tau -10%", v(tau=0.9 * T0), 0.66)]
print("\nfinite-difference sensitivities:")
got = {}
for name, vnew, want in moves:
    pct = 100 * (vnew / v0 - 1)
    got[name] = pct
    print(f"   {name:18s} v = {vnew:7.4f} m/s  change = {pct:+.3f} per cent (claimed {want:+.2f})")

# elasticity cross-check: W = sqrt(tau^2 + 2 s / a); e_s = (W+tau)/(2W), e_a = 1 - e_s,
# e_tau = -tau/W  (proved in M-EXAMINER-01).
W = (T0**2 + 2 * S0 / A0) ** 0.5
e_s = (W + T0) / (2 * W)
e_a = 1 - e_s
e_t = -T0 / W
print(f"\nelasticities at the point: e_s = {e_s:.4f}, e_a = {e_a:.4f}, e_tau = {e_t:.4f}")
print(f"first-order predictions for a 10 per cent move: s {10*e_s:+.2f} per cent, "
      f"a {10*e_a:+.2f} per cent, tau {-10*e_t:+.2f} per cent")

# The two large moves reproduce the lens's figures to 0.01 points.
identity(f"{got['range   s +10%']:.2f}", "5.23")
identity(f"{got['braking a +10%']:.2f}", "4.51")
# The latency move does not: exact value below.
identity(f"{got['latency tau -10%']:.2f}", "0.66")
print(f"\nlatency move, exact: {got['latency tau -10%']:+.4f} per cent; "
      f"first-order 10*|e_tau| = {-10*e_t:+.4f} per cent; lens says +0.66 per cent")

# ranking claim: range > braking >> latency (this is what F10 rests on)
rank_ok = got["range   s +10%"] > got["braking a +10%"] > 5 * got["latency tau -10%"]
identity(f"{int(rank_ok)}", "1")
print("ranking range > braking > 5x latency holds:", rank_ok)

raise SystemExit(finish())
