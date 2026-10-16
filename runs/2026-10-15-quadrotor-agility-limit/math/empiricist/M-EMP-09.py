"""M-EMP-09. Tilt required to accelerate, against a body-fixed camera's field of view.

Claims (empiricist F7, ledger row 13; load-bearing for EMP-D):
to hold altitude while accelerating laterally at a_lat a multirotor must tilt
theta = atan(a_lat/g); a body-fixed forward camera of horizontal FoV H sees its
own direction of travel only while theta <= H/2, so the threshold acceleration is
a_lat = g*tan(H/2): 1.00 g at H = 90 deg, 1.57 g at 115 deg, 4.51 g at 155 deg.
At 4 g the tilt is 76.0 deg, outside a 90 deg FoV.

Symbols: a_lat horizontal acceleration (m/s^2, >= 0), g = 9.81 m/s^2, theta tilt
from level (rad, in [0, pi/2)), H horizontal FoV (rad, in (0, pi)).
Assumptions (the lens's): rigid body, thrust along the body z axis, vertical
acceleration zero (altitude held), camera boresight along body x, level heading,
and "direction of travel" taken as the direction of the acceleration vector --
i.e. the geometry is instantaneous and ignores that the velocity direction need
not coincide with the acceleration direction.
Derivation: T cos theta = m g, T sin theta = m a_lat  =>  tan theta = a_lat/g.
"""
import math
import sys

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import finish, identity, inequality, limit, quantity, units  # noqa: E402

g = 9.81
print("inputs: g = 9.81 m/s^2; theta = atan(a_lat/g); boresight limit theta = H/2")
for H, claim in ((90.0, 1.00), (115.0, 1.57), (155.0, 4.51)):
    a_over_g = math.tan(math.radians(H / 2))
    print(f"  H = {H:5.1f} deg: threshold a_lat = {a_over_g:.4f} g = {a_over_g * g:.3f} m/s^2 "
          f"(claimed {claim} g)")
    inequality(f"abs({a_over_g:.6f} - {claim})", "<", "0.006")
    quantity(f"{a_over_g:.6f} * 9.81 m/s^2", f"{claim * g:.4f} m/s^2", rel_tol=5e-3)

for a_over_g, claim in ((4.0, 75.96), (4.2849, 76.87)):
    theta = math.degrees(math.atan(a_over_g))
    print(f"  a_lat = {a_over_g} g: tilt = {theta:.3f} deg (claimed {claim})")
    inequality(f"abs({theta:.5f} - {claim})", "<", "0.02")

# a T/W 4.4 platform holding altitude can make sqrt(4.4^2-1) g = 4.285 g, not 4 g:
# the lens's "4 g" is conservative, so the tilt it quotes is a lower bound.
print(f"T/W 4.4 altitude-holding lateral capability = {math.sqrt(4.4**2 - 1):.4f} g")
inequality(f"{math.sqrt(4.4 ** 2 - 1):.6f}", ">", "4.0")

units("9.81 m/s^2 * 1.0", "acceleration")
identity("tan(atan(x))", "x", domain={"x": (0.0, 20.0)})
identity("atan(1)", "pi/4")
# small-acceleration limit: theta ~ a/g (flat, linear) and the threshold is ~ g*H/2
limit("atan(x)/x", "x", 0, "1")
limit("tan(h/2)", "h", 0, "0", domain={"h": (0.0, 3.1)})
# as H -> 180 deg the threshold acceleration diverges: no tilt hides the travel direction
limit("tan(h/2)", "h", "pi", "oo", direction="-", domain={"h": (0.0, 3.1415)})
raise SystemExit(finish())
