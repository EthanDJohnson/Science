"""M-DIAL-02. Thrust-to-weight saturation set by a body-fixed camera cone.

Claim (lens finding 10, candidate DIAL-F): using a = g*tan(theta) and T/W = sec(theta), the
thrust-to-weight above which extra thrust cannot be spent without swinging the direction of travel
out of the camera cone is T/W_sat = sec(phi + VFoV/2), with values 1.14 (level, 58 deg VFoV),
1.94 (30 deg tilt, 58 deg), 3.63 (45 deg tilt, 58 deg), 1.86 (115 deg VFoV level) and
22.93 (115 deg VFoV at 30 deg tilt).

Independent derivation (SI; angles in degrees on input):
  Constant-altitude flight: T*cos(theta) = m*g  =>  T/W = T/(m*g) = sec(theta).
  The cone criterion of M-DIAL-01 caps theta at theta_max = phi + VFoV/2.
  sec is increasing on [0, pi/2), so T/W <= sec(theta_max). Dimensionless quantity.
Domain: 0 <= phi, VFoV > 0, phi + VFoV/2 < 90 deg.
"""
import math
import sys

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import identity, limit, inequality, finish  # noqa: E402

G = 9.81


def twr_sat(phi_deg, vfov_deg):
    return 1.0 / math.cos(math.radians(phi_deg + vfov_deg / 2.0))


cases = [("level, 58 deg VFoV", 0.0, 58.0, 1.14),
         ("30 deg tilt, 58 deg VFoV", 30.0, 58.0, 1.94),
         ("45 deg tilt, 58 deg VFoV", 45.0, 58.0, 3.63),
         ("level, 115 deg VFoV", 0.0, 115.0, 1.86),
         ("30 deg tilt, 115 deg VFoV", 30.0, 115.0, 22.93)]
print("T/W_sat = sec(phi + VFoV/2), dimensionless")
for name, phi, vfov, claimed in cases:
    got = twr_sat(phi, vfov)
    print(f"  {name:28s}: {got:8.4f}  (lens: {claimed})  rel. diff {abs(got-claimed)/claimed:.3%}")

# cross-check through the acceleration ceiling instead of through sec: T/W from a_FoV
for name, phi, vfov, claimed in cases:
    a = G * math.tan(math.radians(phi + vfov / 2.0))
    twr = math.sqrt(1.0 + (a / G) ** 2)            # invert a = g sqrt((T/W)^2 - 1)
    print(f"  via a_FoV = {a:9.3f} m/s^2 -> T/W = {twr:8.4f}  ({name})")

# every onboard-only platform in the dossier is T/W 4.1-4.5; compare with the 30 deg-tilt cap
print(f"unused thrust factor at T/W 4.1-4.5 against T/W_sat = {twr_sat(30.0, 58.0):.3f}: "
      f"{4.1/twr_sat(30.0, 58.0):.2f}x to {4.5/twr_sat(30.0, 58.0):.2f}x  (lens: 2-4x)")

identity("sqrt(1 + tan(t)**2)", "1/cos(t)", domain={"t": (0.0, 1.5)})
identity("1/cos(t)", "sqrt(1 + (g*tan(t)/g)**2)", domain={"t": (0.0, 1.5), "g": (1.0, 20.0)})
# hover limit: zero usable acceleration means T/W_sat -> 1
limit("1/cos(t)", "t", 0, "1")
# saturation diverges as the cone edge reaches the vertical
limit("1/cos(t)", "t", "pi/2", "oo")
# monotone in the cone half-angle
inequality("1/cos(t + d)", ">", "1/cos(t)", domain={"t": (0.0, 1.0), "d": (0.01, 0.5)})
# T/W_sat is dimensionless by construction: check the identity T/W = sec(theta) from force balance
identity("(m*g/cos(t))/(m*g)", "1/cos(t)", domain={"t": (0.0, 1.5), "m": (0.2, 1.5), "g": (1.0, 20.0)})

raise SystemExit(finish())
