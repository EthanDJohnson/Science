#!/usr/bin/env python3
"""M-MECH-02  Field-of-view cap on usable acceleration, and the coupled stop bound.

CLAIM (mechanist finding 2, candidate MECH-A)
  Symbols, SI: g = 9.81 m/s^2; a_x horizontal acceleration [m/s^2]; theta = atan(a_x/g) the tilt a
  planar quadrotor needs for a_x (underactuation, thrust along body z, level flight);
  phi = half-FoV + mount tilt [rad] of a body-fixed camera measured from the camera's boresight
  to the edge of the image in the pitch plane; a_u = usable braking/dodging acceleration;
  s = usable range [m]; tau_sense = sensing+compute latency [s]; v = speed [m/s].
  Assumptions: body-fixed camera, pitch/roll (not yaw) used to redirect thrust, an obstacle
  outside the image is unusable, single static obstacle, constant braking.
  Claimed: (i) theta = atan(a_x/g) gives 27.0 / 45.5 / 63.9 / 75.5 deg at 5 / 10 / 20 / 38 m/s^2;
           (ii) the direction of travel leaves the image once |a_x| > g tan(phi), so
                a_u = min(a_h, g tan(phi)) = 5.44 m/s^2 at phi = 29 deg (58 deg vertical FoV,
                level mount), 16.3 m/s^2 at phi = 59 deg (same lens tilted 30 deg up),
                44.3 m/s^2 at phi = 77.5 deg (155 deg lens);
           (iii) the coupled stop bound at s = 6 m, tau_sense = 107 ms is 7.35 m/s level-mounted
                and 11.76 m/s tilted 30 deg.
  (iii) needs a blind-time convention the analysis states only loosely ("counting half the
  rotation as latency"); both conventions are computed here and reported.
"""
import math
import sys

import sympy as sp

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import finish, identity, limit, quantity, units  # noqa: E402

G = 9.81
# Sun et al. TABLE II platform (runs/.../tools/quadrotor.py): m = 0.75 kg, l = 0.14 m,
# arm angle 56 deg from +x, J = diag(2.5, 2.1, 4.3) g m^2, f_max = 8.5 N per rotor.
M, L, BETA, JY, FMAX = 0.75, 0.14, math.radians(56.0), 2.1e-3, 8.5
A_H = G * math.sqrt((4 * FMAX / (M * G)) ** 2 - 1)          # m/s^2, thrust-limited
TAU_MAX = L * math.cos(BETA) * 2 * FMAX                     # N m, pitch torque at the rotor limit
ALPHA = TAU_MAX / JY                                        # rad/s^2
print(f"inputs: a_h = {A_H:.3f} m/s^2 (T/W = {4*FMAX/(M*G):.3f}), "
      f"tau_max = {TAU_MAX:.4f} N m, alpha_max = {ALPHA:.1f} rad/s^2")

# ---------------------------------------------------------------- (i) tilt for a_x
a_x, g_s = sp.symbols("a_x g_s", positive=True)
identity(sp.tan(sp.atan(a_x / g_s)), a_x / g_s, domain={"a_x": (0.1, 50), "g_s": (1, 20)})
for ax, want in ((5.0, 27.0), (10.0, 45.5), (20.0, 63.9), (38.0, 75.5)):
    deg = math.degrees(math.atan(ax / G))
    print(f"theta(a_x={ax} m/s^2) = {deg:.2f} deg   (lens: {want})")
    quantity(f"{deg:.6f} m", f"{want} m", rel_tol=5e-3)

# ---------------------------------------------------------------- (ii) a_u = g tan(phi)
# The flight direction (and an obstacle straight ahead) stays inside the image while the tilt
# theta = atan(a_x/g) is below phi; theta < phi  <=>  a_x < g tan(phi).
phi = sp.symbols("phi", positive=True)
identity(sp.tan(phi) * g_s, g_s * sp.tan(phi), domain={"phi": (0.01, 1.5), "g_s": (1, 20)})
limit(g_s * sp.tan(phi), "phi", 0, 0)                      # a pinhole-narrow camera allows no tilt
for phideg, want in ((29.0, 5.44), (59.0, 16.3), (77.5, 44.3)):
    au = min(A_H, G * math.tan(math.radians(phideg)))
    print(f"a_u(phi={phideg} deg) = {au:.3f} m/s^2   (lens: {want})")
    quantity(f"{au:.6f} m/s^2", f"{want} m/s^2", rel_tol=5e-3)
units("9.81 m/s^2 * 1.664", "acceleration")

# ---------------------------------------------------------------- (iii) coupled stop bound
def stop_bound(a, s, tau):
    return a * (math.sqrt(tau**2 + 2 * s / a) - tau)


def rot_time(theta_rad, alpha=ALPHA):
    """rest-to-rest bang-bang single-axis rotation, no motor lag."""
    return 2.0 * math.sqrt(theta_rad / alpha)


S, TAU_S = 6.0, 0.107
for phideg in (29.0, 59.0, 57.5, 77.5):
    au = min(A_H, G * math.tan(math.radians(phideg)))
    th = math.atan(au / G)
    trot = rot_time(th)
    v_plain = stop_bound(au, S, TAU_S)
    v_half = stop_bound(au, S, TAU_S + trot / 2)
    v_full = stop_bound(au, S, TAU_S + trot)
    print(f"phi={phideg:5.1f} deg: a_u={au:6.3f} m/s^2, theta={math.degrees(th):5.2f} deg, "
          f"tau_rot={trot*1e3:5.1f} ms -> v = {v_plain:6.3f} (tau_sense only), "
          f"{v_half:6.3f} (half rotation), {v_full:6.3f} m/s (full rotation)")

au29 = min(A_H, G * math.tan(math.radians(29.0)))
au59 = min(A_H, G * math.tan(math.radians(59.0)))
v29 = stop_bound(au29, S, TAU_S + rot_time(math.atan(au29 / G)) / 2)
v59 = stop_bound(au59, S, TAU_S + rot_time(math.atan(au59 / G)) / 2)
quantity(f"{v29:.6f} m/s", "7.35 m/s", rel_tol=1e-2)       # level mount
quantity(f"{v59:.6f} m/s", "11.76 m/s", rel_tol=1e-2)      # tilted 30 deg up
# test predictions of MECH-A: 58 / 115 / 155 deg vertical FoV, level mount
for fov, want in ((58.0, "7.4 m/s"), (115.0, "11.5 m/s"), (155.0, "17.0 m/s")):
    au = min(A_H, G * math.tan(math.radians(fov / 2)))
    vv = stop_bound(au, S, TAU_S + rot_time(math.atan(au / G)) / 2)
    print(f"FoV {fov:5.1f} deg -> a_u = {au:6.3f} m/s^2, v = {vv:6.3f} m/s   (lens: {want})")
    quantity(f"{vv:.6f} m/s", want, rel_tol=2e-2)

# the cap must be inactive when the optics are wide: a_u -> a_h
au_wide = min(A_H, G * math.tan(math.radians(85.0)))
print(f"a_u(phi=85 deg) = {au_wide:.3f} m/s^2 = a_h = {A_H:.3f} m/s^2 (cap inactive)")
quantity(f"{au_wide:.6f} m/s^2", f"{A_H:.6f} m/s^2", rel_tol=1e-9)

raise SystemExit(finish())
