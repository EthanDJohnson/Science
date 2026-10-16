#!/usr/bin/env python3
"""M-EXAMINER-02  (examiner F2b, candidate EXAMINER-B)

CLAIM, stated precisely
-----------------------
A quadrotor in level flight (no vertical acceleration) producing horizontal acceleration
magnitude a (m/s^2) must tilt its thrust axis from vertical by theta = atan(a/g), g = 9.81 m/s^2.
Its camera is rigidly fixed to the body, boresight along the body's forward axis, tilted up by
an angle `tilt` above that axis, with half-angle HFoV/2 of field of view.  The claim:

 (i)   theta = atan(a/g): 45.0 deg at a = 1.00 g, 63.9 deg at 2.04 g, 75.5 deg at 3.87 g;
 (ii)  the horizontal flight direction leaves the field of view when theta > HFoV/2 + tilt,
       i.e. the largest braking acceleration that keeps it in view is
       a_fov = g * tan(HFoV/2 + tilt);
 (iii) a_fov = 9.81 m/s^2 (HFoV 90 deg, tilt 0), 36.61 m/s^2 (90 deg + 30 deg tilt),
       44.25 m/s^2 (HFoV 155 deg, tilt 0)  [= 1.00 g, 3.73 g, 4.51 g];
 (iv)  the FoV-capped stop speeds at range s = 6 m, with zero delay, sqrt(2 * a_fov * s),
       are 10.85, 20.96 and 23.04 m/s.

Domain: a >= 0, g > 0, 0 < HFoV/2 + tilt < 90 deg.
"""
import sys

import sympy as sp

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import finish, identity, limit, quantity, series, units  # noqa: E402

aa, gg, th, half = sp.symbols("aa gg th half", positive=True)

# (i)-(ii): derive from force balance.  Thrust T along body z; level flight:
#   T cos(theta) = m g  (vertical),  T sin(theta) = m a  (horizontal)  =>  tan(theta) = a/g.
theta_expr = sp.atan(aa / gg)
identity(sp.tan(theta_expr), aa / gg, domain={"aa": (0.0, 100.0), "gg": (1.0, 20.0)})
# inverse direction: acceleration at which the tilt equals a given look-down budget `half`
identity(gg * sp.tan(half), sp.solve(sp.Eq(sp.atan(aa / gg), half), aa)[0],
         domain={"gg": (1.0, 20.0), "half": (0.05, 1.5)})

# small-angle limit: tilt angle ~ a/g for a << g ; a_fov ~ g * (HFoV/2 + tilt)
series(theta_expr.subs(gg, 9.81), "aa", 0, 2, sp.Rational(100, 981) * aa)
limit(sp.atan(aa / gg) / (aa / gg), "aa", 0, sp.Integer(1))

g = 9.81
print("(i) tilt angle for horizontal acceleration a:")
for mult, want in ((1.00, 45.0), (2.04, 63.9), (3.87, 75.5)):
    got = sp.deg(sp.atan(mult)).evalf()
    print(f"   a = {mult:.2f} g -> theta = {float(got):.2f} deg (claimed {want})")
    identity(f"{float(got):.1f}", f"{want:.1f}")

print("\n(iii)-(iv) FoV cutoff and capped stop speed at s = 6 m:")
cases = [("90 deg, no tilt", 90.0, 0.0, 9.81, 10.85),
         ("90 deg + 30 deg tilt", 90.0, 30.0, 36.61, 20.96),
         ("155 deg, no tilt", 155.0, 0.0, 44.25, 23.04)]
for name, hfov, tilt, a_want, v_want in cases:
    ang = sp.rad(sp.Float(hfov) / 2 + sp.Float(tilt))
    a_fov = float(g * sp.tan(ang))
    v_cap = float(sp.sqrt(2 * a_fov * 6))
    print(f"   {name:22s} half+tilt = {hfov/2 + tilt:5.1f} deg  "
          f"a_fov = {a_fov:6.2f} m/s^2 ({a_fov/g:.2f} g)  v_stop = {v_cap:6.2f} m/s "
          f"(claimed {a_want} m/s^2, {v_want} m/s)")
    quantity(f"{a_fov:.6f} m/s^2", f"{a_want} m/s^2", rel_tol=2e-3)
    quantity(f"{v_cap:.6f} m/s", f"{v_want} m/s", rel_tol=2e-3)

# units
units("9.81 m/s^2 * 1", "m/s^2")
units("2 * 36.61 m/s^2 * 6 m", "m^2/s^2")

# Caveat recorded as a check, not a refutation: a pitch rotation moves the flight direction in
# the VERTICAL field of view, so the relevant half-angle is VFoV/2, not HFoV/2.  For a D435i-class
# sensor (about 87 deg H x 58 deg V) the cutoff would be g*tan(29 deg) = 5.44 m/s^2, v = 8.08 m/s.
a_v = float(g * sp.tan(sp.rad(29)))
print(f"\ncaveat: with VFoV 58 deg (half 29 deg) instead, a_fov = {a_v:.2f} m/s^2, "
      f"v_stop(6 m) = {float(sp.sqrt(2*a_v*6)):.2f} m/s")

raise SystemExit(finish())
