"""M-DIAL-01. FoV-limited horizontal acceleration of a quadrotor with a body-fixed camera.

Claim (lens finding 4 / synthesis S1, candidates DIAL-F and DIAL-A):
  To accelerate horizontally at a, a quadrotor holding altitude must tilt by theta = atan(a/g).
  With a body-fixed camera whose optical axis sits phi above the body x-axis and whose vertical
  field of view is VFoV, the horizontal direction of travel leaves the camera cone once
  theta > phi + VFoV/2, hence a <= a_FoV = g*tan(phi + VFoV/2).
  Numbers claimed: phi = 30 deg, VFoV = 58 deg -> a_FoV = 16.33 m/s^2 = 1.66 g;
  level (phi = 0) -> 5.44 m/s^2 = 0.55 g; phi = 45 deg -> 34.21 m/s^2 = 3.49 g;
  thrust ceiling at T/W = 4.4 -> 42.03 m/s^2 = 4.28 g; acceleration ratio 2.57;
  dodge-speed ratio 1.49 at s = 6 m, tau = 50 ms, r = 0.5 m.

Independent derivation, SI units (m, s, m/s^2), angles in radians internally:
  Rigid body, mass m, single collective thrust T along body z, level (constant-altitude) flight.
  Vertical: T*cos(theta) = m*g.  Horizontal: T*sin(theta) = m*a  =>  a = g*tan(theta).
  Camera axis in the world frame: pitching the body nose-down by theta rotates the camera axis
  from phi above body-x to (phi - theta) relative to horizontal; the cone spans
  [phi - theta - VFoV/2, phi - theta + VFoV/2]. The horizontal travel direction (0 rad) is inside
  the cone iff phi - theta - VFoV/2 <= 0 <= phi - theta + VFoV/2, i.e.
  phi - VFoV/2 <= theta <= phi + VFoV/2. The upper branch gives a <= g*tan(phi + VFoV/2).
  Thrust ceiling at constant altitude (dossier D-33): a_T = g*sqrt((T/W)^2 - 1).
  Dodge bound (dossier D-31): v_max = s/(tau + 2*sqrt(r/a)).

Domain: 0 <= phi, 0 < VFoV, phi + VFoV/2 < pi/2 (otherwise the cap is unbounded); g, s, r, tau > 0;
T/W > 1.
"""
import math
import sys

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import identity, limit, quantity, units, finish, inequality  # noqa: E402

G = 9.81  # m/s^2

# --- the geometric criterion, derived from scratch ---------------------------------
def theta_of_a(a, g=G):
    """Tilt needed for horizontal acceleration a at constant altitude, rad."""
    return math.atan(a / g)


def in_cone(theta, phi, vfov):
    """Is the horizontal direction of travel inside the camera cone at tilt theta?"""
    lo = phi - theta - vfov / 2.0
    hi = phi - theta + vfov / 2.0
    return lo <= 0.0 <= hi


def a_fov(phi_deg, vfov_deg, g=G):
    """Largest horizontal acceleration keeping the travel direction in the cone, m/s^2."""
    half = math.radians(phi_deg + vfov_deg / 2.0)
    return g * math.tan(half)


def a_thrust(twr, g=G):
    return g * math.sqrt(twr**2 - 1.0)


def v_dodge(s, tau, r, a):
    return s / (tau + 2.0 * math.sqrt(r / a))


# numerical bisection for the cap, independent of the closed form
def a_cap_numeric(phi_deg, vfov_deg, g=G):
    phi, vfov = math.radians(phi_deg), math.radians(vfov_deg)
    lo, hi = 0.0, 1e6
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if in_cone(theta_of_a(mid, g), phi, vfov):
            lo = mid
        else:
            hi = mid
    return lo


print("inputs: g = 9.81 m/s^2; camera VFoV = 58 deg (A-20 depth camera); tilts phi = 0, 30, 45 deg")
for phi in (0.0, 30.0, 45.0):
    closed = a_fov(phi, 58.0)
    num = a_cap_numeric(phi, 58.0)
    print(f"  phi = {phi:4.1f} deg: a_FoV closed form = {closed:7.3f} m/s^2 = {closed/G:5.3f} g; "
          f"bisection on the cone test = {num:7.3f} m/s^2 (rel. diff {abs(num-closed)/closed:.2e})")

aT = a_thrust(4.4)
print(f"thrust ceiling at T/W = 4.4: a_T = {aT:.3f} m/s^2 = {aT/G:.3f} g")
a30 = a_fov(30.0, 58.0)
print(f"acceleration ratio a_T/a_FoV(30 deg) = {aT/a30:.4f}  (lens: 2.57)")
vT = v_dodge(6.0, 0.05, 0.5, aT)
vF = v_dodge(6.0, 0.05, 0.5, a30)
print(f"dodge speed s = 6 m, tau = 0.05 s, r = 0.5 m: thrust-limited {vT:.3f} m/s, "
      f"FoV-limited {vF:.3f} m/s, ratio {vT/vF:.4f}  (lens: 22.38, 15.00, 1.49)")
print(f"115 deg VFoV at 30 deg tilt: a_FoV = {a_fov(30.0, 115.0):.2f} m/s^2 "
      f"(> thrust ceiling {aT:.2f}, so FoV no longer binds)")

# --- symbolic / limit / units checks ----------------------------------------------
# a = g tan(theta) with theta = atan(a/g) is self-consistent
identity("g*tan(atan(a/g))", "a", domain={"a": (0.01, 100.0), "g": (1.0, 20.0)})
# the cone upper branch: theta <= phi + VFoV/2 maps to a <= g tan(phi + VFoV/2)
identity("atan(g*tan(p)/g)", "p", domain={"p": (0.01, 1.5), "g": (1.0, 20.0)})
# consistency of the two acceleration ceilings: with T/W = sec(theta), g*sqrt((T/W)^2-1) = g*tan(theta)
identity("g*sqrt(1/cos(t)**2 - 1)", "g*tan(t)", domain={"t": (0.0, 1.5), "g": (1.0, 20.0)})
# small-angle limit: a_FoV -> g*(phi + VFoV/2) for a narrow cone near level flight
limit("g*tan(p)/(g*p)", "p", 0, "1", domain={"g": (1.0, 20.0)})
# the cap grows without bound as the cone edge approaches the vertical
limit("g*tan(p)", "p", "pi/2", "oo", domain={"g": (1.0, 20.0)})
# a_FoV is monotone in the cone half-angle (so a wider FoV or more up-tilt always raises the cap)
inequality("g*tan(p + d)", ">", "g*tan(p)", domain={"p": (0.01, 1.0), "d": (0.01, 0.5), "g": (1.0, 20.0)})
# numbers with units
quantity("9.81 m/s^2 * 1.664279", "16.33 m/s^2", rel_tol=2e-3)
quantity("9.81 m/s^2 * 0.554309", "5.44 m/s^2", rel_tol=2e-3)
quantity("9.81 m/s^2 * 3.487414", "34.21 m/s^2", rel_tol=2e-3)
quantity("9.81 m/s^2 * 4.284857", "42.03 m/s^2", rel_tol=2e-3)
quantity("6 m / (0.05 s + 2 * (0.5 m / (16.33 m/s^2))^0.5)", "15.00 m/s", rel_tol=2e-3)
units("9.81 m/s^2 * 1.664279", "acceleration")
units("6 m / (0.05 s + 2 * (0.5 m / (16.33 m/s^2))^0.5)", "speed")

raise SystemExit(finish())
