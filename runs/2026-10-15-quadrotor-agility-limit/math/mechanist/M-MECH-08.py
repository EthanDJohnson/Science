#!/usr/bin/env python3
"""M-MECH-08  Position error from the unmodelled aerodynamic force over a braking manoeuvre.

CLAIM (mechanist finding 8, candidate MECH-E)
  Symbols: F_err residual aerodynamic force the model misses [N]; m = 0.75 kg; a_err = F_err/m;
  v entry speed [m/s]; a_h = 42.03 m/s^2 braking acceleration; t_b = v/a_h braking duration [s];
  dx = (1/2) a_err t_b^2 the open-loop position error it integrates to [m].
  Assumptions: the residual force is constant in magnitude and direction over the manoeuvre
  (worst case), no feedback correction, braking at constant a_h, 1-D.
  Claimed: 0.352-0.365 N on 0.75 kg is 0.48 m/s^2; dx = 0.7 cm from 7 m/s, 1.4 cm from 10 m/s,
  5.4 cm from 20 m/s; a 2 N error gives 30 cm at 20 m/s.
"""
import sys

import sympy as sp

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import finish, identity, limit, quantity, units  # noqa: E402

M, A_H = 0.75, 42.034448
print(f"inputs: m = {M} kg, a_h = {A_H:.3f} m/s^2")
for F in (0.352, 0.365, 2.0):
    print(f"F_err = {F} N -> a_err = {F/M:.4f} m/s^2")
quantity(f"{0.365/M:.6f} m/s^2", "0.48 m/s^2", rel_tol=2e-2)
units("0.365 N/(0.75 kg)", "acceleration")

# closed form dx = a_err v^2/(2 a_h^2)
a_err, v, a_h, t = sp.symbols("a_err v a_h t", positive=True)
dx = sp.Rational(1, 2) * a_err * (v / a_h) ** 2
identity(dx, a_err * v**2 / (2 * a_h**2),
         domain={"a_err": (0.01, 10), "v": (1, 50), "a_h": (5, 60)})
limit(dx, "v", 0, 0)                      # no manoeuvre, no error
limit(dx, "a_h", "oo", 0)                 # instantaneous braking leaves no time to drift
units("0.4867 m/s^2 * (20 m/s)^2/(2*(42 m/s^2)^2)", "length")

for vv, want in ((7.0, "0.7 cm"), (10.0, "1.4 cm"), (20.0, "5.4 cm")):
    val = float(dx.subs({a_err: 0.365 / M, v: vv, a_h: A_H}))
    print(f"v = {vv:4.1f} m/s, F_err = 0.365 N: t_b = {vv/A_H*1e3:5.1f} ms, dx = {val*100:.3f} cm"
          f"   (lens: {want})")
    quantity(f"{val:.8f} m", want, rel_tol=5e-2)
val2 = float(dx.subs({a_err: 2.0 / M, v: 20.0, a_h: A_H}))
print(f"v = 20 m/s, F_err = 2 N: dx = {val2*100:.1f} cm   (lens: 30 cm)")
quantity(f"{val2:.8f} m", "30 cm", rel_tol=5e-2)

# scaling law: dx ~ v^2, so quadrupling the speed from 7 to 20 m/s multiplies dx by (20/7)^2
print(f"dx(20)/dx(7) = {float(dx.subs({a_err: 0.4867, v: 20, a_h: A_H})/dx.subs({a_err: 0.4867, v: 7, a_h: A_H})):.3f}"
      f"  (expect (20/7)^2 = {(20/7)**2:.3f})")
quantity(f"{float(dx.subs({a_err: 0.4867, v: 20, a_h: A_H})/dx.subs({a_err: 0.4867, v: 7, a_h: A_H})):.6f} m",
         f"{(20/7)**2:.6f} m", rel_tol=1e-9)

raise SystemExit(finish())
