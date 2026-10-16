#!/usr/bin/env python3
"""M-SIMULATOR-09: the h-force magnitude and the drag-limited level top speed.

CLAIMS.
(a) lens finding 10: with Sun et al. eq. 9, f_a^B = (-kd_x vx, -kd_y vy,
    -kd_z vz + kh (vx^2 + vy^2)) and kh = 0.01 kg/m, the body-z term is 4.0 N at 20 m/s,
    54 per cent of the 0.75 kg vehicle's weight.
(b) lens finding 2: "the drag-limited level top speed of the same plant is 99.1 m/s, so the
    speed cap never binds on this course (peak profile speed 28.2 m/s)".

SYMBOLS / DOMAIN. v^B = body-frame velocity in m/s; kd = (0.26, 0.28, 0.42) kg/s;
kh = 0.01 kg/m; m = 0.75 kg; T <= 34 N total thrust along body z; theta in [0, pi/2) rad
pitch from vertical; steady level flight at world velocity (V, 0, 0), V > 0 m/s, zero
acceleration, no wind.

INDEPENDENT DERIVATION. Body axes for a pitch theta about the world y axis:
z^B = (sin t, 0, cos t), x^B = (cos t, 0, -sin t), so v^B_x = V cos t, v^B_z = V sin t.
With the aerodynamic force f^B applied in the body frame, force balance in world axes is
  x: (T + f^B_z) sin t + f^B_x cos t = 0
  z: (T + f^B_z) cos t - f^B_x sin t - m g = 0
Solved on a grid in theta at T = 34 N (full thrust), taking the smallest positive V root of
the x equation and bisecting theta on the z residual. Three aero variants are compared, since
the lens does not say which it used.
"""
import sys
from math import cos, degrees, radians, sin, sqrt

import numpy as np

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import finish, identity, inequality, quantity, units  # noqa: E402

G, M = 9.80665, 0.75
T_MAX = 4 * 8.5
KDX, KDY, KDZ, KH = 0.26, 0.28, 0.42, 0.01
W = M * G

print("=== (a) the h-force ===")
for V in (10.0, 20.0, 28.2):
    fh = KH * V**2
    print(f"  V = {V:5.1f} m/s: kh V^2 = {fh:7.4f} N = {100*fh/W:6.2f} per cent of the "
          f"{W:.4f} N weight")
fh20 = KH * 20.0**2

print("\n=== (b) steady level flight at full thrust ===")


def residual_and_V(theta, variant):
    """Smallest positive V satisfying the world-x balance, and the world-z residual there."""
    Vs = np.linspace(1e-6, 400.0, 40001)
    ct, st = cos(theta), sin(theta)
    if variant == "body eq. 9":
        fx = -KDX * Vs * ct
        fz = -KDZ * Vs * st + KH * (Vs * ct) ** 2
    elif variant == "body drag only (kh = 0)":
        fx = -KDX * Vs * ct
        fz = -KDZ * Vs * st
    else:  # isotropic world-frame drag
        fx = -KDX * Vs * ct
        fz = -KDX * Vs * st
    fxw = (T_MAX + fz) * st + fx * ct
    sgn = np.sign(fxw)
    idx = np.where(np.diff(sgn) != 0)[0]
    if len(idx) == 0:
        return None, None
    i = idx[0]
    lo, hi = Vs[i], Vs[i + 1]
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if variant == "body eq. 9":
            f_x = -KDX * mid * ct
            f_z = -KDZ * mid * st + KH * (mid * ct) ** 2
        elif variant == "body drag only (kh = 0)":
            f_x, f_z = -KDX * mid * ct, -KDZ * mid * st
        else:
            f_x, f_z = -KDX * mid * ct, -KDX * mid * st
        val = (T_MAX + f_z) * st + f_x * ct
        if np.sign(val) == sgn[i]:
            lo = mid
        else:
            hi = mid
    V = 0.5 * (lo + hi)
    if variant == "body eq. 9":
        f_x = -KDX * V * ct
        f_z = -KDZ * V * st + KH * (V * ct) ** 2
    elif variant == "body drag only (kh = 0)":
        f_x, f_z = -KDX * V * ct, -KDZ * V * st
    else:
        f_x, f_z = -KDX * V * ct, -KDX * V * st
    resid = (T_MAX + f_z) * ct - f_x * st - W
    return V, resid


tops = {}
for variant in ("body eq. 9", "body drag only (kh = 0)", "isotropic world drag"):
    best = None
    thetas = np.linspace(radians(1.0), radians(89.5), 886)
    prev = None
    for th in thetas:
        V, r = residual_and_V(th, variant)
        if V is None:
            continue
        if prev is not None and np.sign(r) != np.sign(prev[1]):
            lo, hi = prev[0], th
            for _ in range(60):
                mid = 0.5 * (lo + hi)
                Vm, rm = residual_and_V(mid, variant)
                if np.sign(rm) == np.sign(prev[1]):
                    lo = mid
                else:
                    hi = mid
            th_s = 0.5 * (lo + hi)
            V_s, r_s = residual_and_V(th_s, variant)
            best = (V_s, degrees(th_s), r_s)
            break
        prev = (th, r)
    tops[variant] = best
    if best:
        print(f"  {variant:<28s}: V_top = {best[0]:8.3f} m/s at pitch {best[1]:6.2f} deg "
              f"(z residual {best[2]:.2e} N)")
    else:
        print(f"  {variant:<28s}: no level equilibrium found")

# a crude closed form for orientation: full tilt, drag opposing along world x only
v_crude = T_MAX * sqrt(1 - (W / T_MAX) ** 2) / KDX
print(f"  closed-form orientation, T sin(theta_max)/kd_x = {v_crude:.3f} m/s "
      "(no body-frame projection, no h-force)")

print("\n=== checks ===")
quantity(f"{fh20:.5f} N", "4.0 N", rel_tol=1e-4)
quantity(f"{100*fh20/W:.4f}", "54.0", rel_tol=0.01)
best_eq9 = tops["body eq. 9"]
quantity(f"{best_eq9[0]:.3f} m/s", "99.1 m/s", rel_tol=0.05)
inequality(f"{best_eq9[0]:.3f}", ">", "56.4")     # at least 2x the 28.2 m/s peak profile speed
inequality(f"{abs(best_eq9[2]):.3e}", "<", "1e-6")
# algebra: the crude cap, T sin(theta)/kd with cos(theta) = W/T
identity("T*sqrt(1 - (W/T)**2)/k", "sqrt(T**2 - W**2)/k", domain={"T": (10, 100), "W": (1, 9), "k": (0.1, 1)})
# limit: as kd -> 0 the level top speed diverges (no drag, no cap)
inequality("sqrt(T**2 - W**2)/k1", ">", "sqrt(T**2 - W**2)/k2",
           domain={"T": (10, 100), "W": (1, 9), "k1": (0.1, 0.5), "k2": (0.6, 1.0)})
units("0.01 kg/m * (20 m/s)^2", "force")
units("(34 N) / (0.26 kg/s)", "speed")
raise SystemExit(finish())
