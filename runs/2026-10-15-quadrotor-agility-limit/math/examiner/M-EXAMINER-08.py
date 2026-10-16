#!/usr/bin/env python3
"""M-EXAMINER-08  (examiner F4, candidates EXAMINER-A and EXAMINER-D)

CLAIM, stated precisely
-----------------------
The lens computes ten speed bounds whose extremes are
   lowest  10.73 m/s  (bang-bang mean speed over 10.7 m at TWR 4.5)
   next    10.85 m/s  (FoV-capped stop bound, 90 deg HFoV untilted, s = 6 m)
   highest 32.72 m/s  (delay bound, tau = 40 ms, R = 5 m, m = 3)
and claims
 (i)   the span is "a factor of 3.0";
 (ii)  the demonstrated onboard-only unseen-course speeds sit at these fractions of the bounds:
       5 m/s -> 0.47 (of the lowest) and 0.15 (of the highest); 7 m/s -> 0.65 / 0.21;
       10 m/s -> 0.93 / 0.31; the seen-track peak 32.2 m/s -> 3.00 / 0.98;
 (iii) the two lowest bounds "agree to 1.1 per cent".
Each of the three extreme bounds is recomputed here from its own definition (not read off the
lens's table), then the ratios are pure arithmetic.  Units: all bounds in m/s.
"""
import sys

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import finish, identity, quantity, units  # noqa: E402

G = 9.81

# bound 1: bang-bang rest-to-rest mean speed, TWR 4.5, gate spacing 10.7 m
a_45 = G * (4.5**2 - 1) ** 0.5
low = (a_45 * 10.7) ** 0.5 / 2
# bound 2: FoV-capped zero-delay stop bound, half-angle 45 deg, s = 6 m
a_fov = G * 1.0                      # g*tan(45 deg)
fov = (2 * a_fov * 6.0) ** 0.5
# bound 3: delay bound, w_c = (pi/4)/tau, v = w_c R / m
import math
high = (math.pi / 4 / 0.040) * 5.0 / 3.0

print(f"recomputed bounds: bang-bang mean (TWR 4.5) = {low:.4f} m/s, "
      f"FoV-capped stop = {fov:.4f} m/s, delay bound = {high:.4f} m/s")
quantity(f"{low:.5f} m/s", "10.73 m/s", rel_tol=2e-3)
quantity(f"{fov:.5f} m/s", "10.85 m/s", rel_tol=2e-3)
quantity(f"{high:.5f} m/s", "32.72 m/s", rel_tol=2e-3)

span = high / low
print(f"\n(i) span = {span:.3f} (claimed 'a factor of 3.0')")
identity(f"{span:.1f}", "3.0")

print("\n(ii) demonstrated speed as a fraction of the lowest and the highest bound:")
for v, f_low, f_high in ((5.0, 0.47, 0.15), (7.0, 0.65, 0.21), (10.0, 0.93, 0.31),
                         (32.2, 3.00, 0.98)):
    r_low, r_high = v / low, v / high
    print(f"   {v:5.1f} m/s -> {r_low:.3f} of lowest (claimed {f_low}), "
          f"{r_high:.3f} of highest (claimed {f_high})")
    identity(f"{r_low:.2f}", f"{f_low:.2f}")
    identity(f"{r_high:.2f}", f"{f_high:.2f}")

rel = abs(fov - low) / ((fov + low) / 2)
print(f"\n(iii) relative gap between the two lowest bounds = {rel:.4%} (claimed 1.1 per cent)")
identity(f"{100*rel:.1f}", "1.1")

units("9.81 m/s^2 * 10.7 m", "m^2/s^2")
units("19.635 rad/s * 5 m / 3", "m/s")

raise SystemExit(finish())
