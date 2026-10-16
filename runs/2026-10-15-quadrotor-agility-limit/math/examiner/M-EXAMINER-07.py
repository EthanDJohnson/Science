#!/usr/bin/env python3
"""M-EXAMINER-07  (examiner F10, candidates EXAMINER-A / EXAMINER-B / EXAMINER-E)

CLAIM, stated precisely
-----------------------
Same stop bound v(s, a, tau) = a*(-tau + sqrt(tau^2 + 2 s / a)) and same base point
s = 6 m, a = 39 m/s^2 (TWR 4.1), tau = 0.040 s, v0 = 20.13 m/s.  Moving one limit by its
"demonstrated attainable increment" changes v by:
   TWR 4.1 -> 12.35, i.e. a = g sqrt(TWR^2-1) from 39.0 to 120.8 m/s^2 : +66.6 per cent
   s 6 m -> 20 m                                                        : +88.6 per cent
   s 6 m -> 10 m                                                        : +31.2 per cent
   tau 40 ms -> 17 ms                                                   : +4.2 per cent
   tau -> 0 (unattainable)                                              : +7.5 per cent
and hence "latency's entire remaining headroom on this bound is under 8 per cent".

Checks: each increment recomputed from the closed form; the tau -> 0 case against the analytic
limit sqrt(2 a s)/v0 - 1; units of every input.
"""
import sys

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import finish, identity, quantity, units  # noqa: E402

G, S0, A0, T0 = 9.81, 6.0, 39.0, 0.040


def v(s=S0, a=A0, tau=T0):
    return a * (-tau + (tau**2 + 2 * s / a) ** 0.5)


def a_of_twr(twr):
    return G * (twr**2 - 1) ** 0.5


v0 = v()
print(f"base: v0 = {v0:.4f} m/s at s = {S0} m, a = {A0} m/s^2, tau = {T0*1000:.0f} ms")
print(f"a(TWR 4.1) = {a_of_twr(4.1):.3f} m/s^2, a(TWR 12.35) = {a_of_twr(12.35):.3f} m/s^2")
quantity(f"{a_of_twr(12.35):.4f} m/s^2", "120.76 m/s^2", rel_tol=2e-3)

cases = [("TWR 4.1 -> 12.35", v(a=a_of_twr(12.35)), 66.6),
         ("s 6 -> 20 m", v(s=20.0), 88.6),
         ("s 6 -> 10 m", v(s=10.0), 31.2),
         ("tau 40 -> 17 ms", v(tau=0.017), 4.2),
         ("tau -> 0", v(tau=0.0), 7.5)]
print("\nattainable-increment sensitivities:")
for name, vnew, want in cases:
    pct = 100 * (vnew / v0 - 1)
    print(f"   {name:18s} v = {vnew:7.3f} m/s  change = {pct:+.2f} per cent (claimed {want:+.1f})")
    identity(f"{pct:.1f}", f"{want:.1f}")

# the tau -> 0 case must agree with the analytic zero-delay bound
v_zero = (2 * A0 * S0) ** 0.5
print(f"\nanalytic zero-delay bound sqrt(2 a s) = {v_zero:.4f} m/s; "
      f"headroom = {100*(v_zero/v0 - 1):.2f} per cent")
quantity(f"{v_zero:.5f} m/s", f"{v(tau=0.0):.5f} m/s", rel_tol=1e-9)
identity(f"{int(100*(v_zero/v0 - 1) < 8.0)}", "1")      # "under 8 per cent"

# latency headroom is strictly smaller than either hardware move
identity(f"{int(100*(v_zero/v0 - 1) < 100*(v(s=10.0)/v0 - 1))}", "1")

units("9.81 m/s^2 * 12.31", "m/s^2")
units("2 * 39 m/s^2 * 6 m", "m^2/s^2")
units("0.017 s", "s")

raise SystemExit(finish())
