#!/usr/bin/env python3
"""M-SIMULATOR-01: the course's path length and the point-mass time-optimal traversal time.

CLAIM (lens finding 2): for the slalom path y(x) = A sin(2 pi x / L) m with A = 3 m,
L = 30 m, 0 <= x <= 90 m, flown at constant altitude by a point mass whose horizontal
acceleration obeys the isotropic bound |a_horiz| <= a_h = 44.260 m/s^2, the path length is
S = 98.315 m, the minimum traversal time is t_opt = 4.5020 s, the mean path speed is
S/t_opt = 21.838 m/s, and the peak speed on the optimal profile is 28.2 m/s.

SYMBOLS / DOMAIN. x, y in m (path is in the horizontal plane, altitude fixed); s = arc length
in m; kappa(s) = path curvature in 1/m, kappa >= 0; v(s) = path speed in m/s, v > 0;
a_h > 0 in m/s^2 is the bound on the magnitude of the horizontal acceleration vector, so
a_t^2 + (kappa v^2)^2 <= a_h^2 where a_t = dv/dt is the tangential component.

INDEPENDENT DERIVATION. On a FIXED path the time-optimal speed profile is the one that is
pointwise maximal subject to (i) the centripetal limit v <= sqrt(a_h/kappa) (the velocity
limit curve) and (ii) the tangential reachability |dv/ds| * v = a_t <= sqrt(a_h^2 -
(kappa v^2)^2).  The profile is obtained by a forward integration from the start state and a
backward integration from the end state, both clipped to the limit curve, then taking the
pointwise minimum (standard velocity-limit-curve / forward-backward construction; the
sinusoid's limit curve has no interior non-differentiable "singular" island beyond the
curvature maxima, which the clipping already handles).  Written from scratch here; nothing is
imported from the lens's scripts.
"""
import sys

import numpy as np

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import finish, identity, quantity, units  # noqa: E402

G = 9.80665                      # m/s^2
MASS = 0.75                      # kg
THRUST_PER_ROTOR = 8.5           # N
A_MAX = 4 * THRUST_PER_ROTOR / MASS                  # m/s^2, total specific thrust
A_H = np.sqrt(A_MAX**2 - G**2)                       # m/s^2, horizontal ceiling at level flight
AMP, LAM, XEND = 3.0, 30.0, 90.0                     # m, m, m


def path_arrays(n):
    """Arc length, curvature and dx-grid for the sinusoid slalom."""
    x = np.linspace(0.0, XEND, n)
    k = 2 * np.pi / LAM
    yp = AMP * k * np.cos(k * x)
    ypp = -AMP * k**2 * np.sin(k * x)
    speedfac = np.sqrt(1 + yp**2)
    ds = 0.5 * (speedfac[1:] + speedfac[:-1]) * np.diff(x)       # trapezoid arc length
    s = np.concatenate([[0.0], np.cumsum(ds)])
    kappa = np.abs(ypp) / speedfac**3
    return s, kappa, ds


def optimal_time(s, kappa, ds, a, v_start, v_end, vcap=1e4):
    """Forward-backward velocity-limit-curve profile; returns (time, profile)."""
    with np.errstate(divide="ignore"):
        vlim = np.where(kappa > 1e-12, np.sqrt(a / np.maximum(kappa, 1e-30)), vcap)
    vlim = np.minimum(vlim, vcap)
    n = len(s)
    fwd = np.empty(n)
    fwd[0] = min(v_start, vlim[0])
    for i in range(n - 1):
        at = np.sqrt(max(a**2 - (kappa[i] * fwd[i] ** 2) ** 2, 0.0))
        fwd[i + 1] = min(vlim[i + 1], np.sqrt(fwd[i] ** 2 + 2 * at * ds[i]))
    bwd = np.empty(n)
    bwd[-1] = min(v_end, vlim[-1])
    for i in range(n - 2, -1, -1):
        at = np.sqrt(max(a**2 - (kappa[i + 1] * bwd[i + 1] ** 2) ** 2, 0.0))
        bwd[i] = min(vlim[i], np.sqrt(bwd[i + 1] ** 2 + 2 * at * ds[i]))
    v = np.minimum(fwd, bwd)
    t = np.sum(2 * ds / (v[:-1] + v[1:]))
    return t, v


print("=== inputs (SI) ===")
print(f"mass {MASS} kg, 4 x {THRUST_PER_ROTOR} N -> a_max = {A_MAX:.5f} m/s^2, g = {G} m/s^2")
print(f"a_h = sqrt(a_max^2 - g^2) = {A_H:.5f} m/s^2")
print(f"path y = {AMP} sin(2 pi x / {LAM}) m, x in [0, {XEND}] m")

print("\n=== path length convergence ===")
for n in (2001, 20001, 200001):
    s, kappa, ds = path_arrays(n)
    print(f"  n = {n:>7d}: S = {s[-1]:.6f} m, kappa_max = {kappa.max():.6f} 1/m")
s, kappa, ds = path_arrays(200001)
S = s[-1]
kappa_peak = AMP * (2 * np.pi / LAM) ** 2            # at the sine peaks, where y' = 0
v_limit_min = np.sqrt(A_H / kappa_peak)
print(f"  analytic kappa at a crest = A k^2 = {kappa_peak:.6f} 1/m -> v_lim = {v_limit_min:.4f} m/s")

print("\n=== time-optimal profile ===")
for n in (20001, 200001):
    sn, kn, dn = path_arrays(n)
    t_fly, v_fly = optimal_time(sn, kn, dn, A_H, 1e4, 1e4)
    t_rest, v_rest = optimal_time(sn, kn, dn, A_H, 0.0, 0.0)
    print(f"  n = {n:>7d}: flying-start t = {t_fly:.5f} s (mean {sn[-1]/t_fly:.4f} m/s, "
          f"peak {v_fly.max():.3f} m/s); rest-to-rest t = {t_rest:.5f} s "
          f"(mean {sn[-1]/t_rest:.4f} m/s)")
t_fly, v_fly = optimal_time(s, kappa, ds, A_H, 1e4, 1e4)
t_rest, v_rest = optimal_time(s, kappa, ds, A_H, 0.0, 0.0)

print("\n=== known limits the solver must reproduce ===")
# straight path, rest to rest: t = 2 sqrt(S/a)
nstr = 100001
x = np.linspace(0, 100.0, nstr)
ds_str = np.diff(x)
t_str, _ = optimal_time(x, np.zeros(nstr), ds_str, A_H, 0.0, 0.0)
closed_str = 2 * np.sqrt(100.0 / A_H)
print(f"  straight 100 m rest-to-rest: {t_str:.6f} s vs 2 sqrt(S/a) = {closed_str:.6f} s")
# circular cruise: v = sqrt(a R)
R = 7.6
ncirc = 100001
arc = np.linspace(0, 2 * np.pi * R, ncirc)
t_cir, v_cir = optimal_time(arc, np.full(ncirc, 1.0 / R), np.diff(arc), A_H, 1e4, 1e4)
print(f"  circular cruise R = {R} m: v = {v_cir.mean():.6f} m/s vs sqrt(a R) = {np.sqrt(A_H*R):.6f} m/s")

print("\n=== checks ===")
quantity(f"{S:.6f} m", "98.315 m", rel_tol=2e-4)
quantity(f"{t_fly:.6f} s", "4.5020 s", rel_tol=1e-3)
quantity(f"{S/t_fly:.6f} m/s", "21.838 m/s", rel_tol=1e-3)
quantity(f"{v_fly.max():.6f} m/s", "28.2 m/s", rel_tol=5e-3)
print(f"NOTE: rest-to-rest would give {t_rest:.5f} s, 12 per cent slower; the lens's 4.5020 s is "
      "the flying-start value, consistent with its closed-loop runs starting on the reference.")
quantity(f"{v_limit_min:.6f} m/s", f"{v_fly.min():.6f} m/s", rel_tol=2e-3)
quantity(f"{t_str:.6f} s", f"{closed_str:.6f} s", rel_tol=1e-5)
quantity(f"{v_cir.mean():.6f} m/s", f"{np.sqrt(A_H*R):.6f} m/s", rel_tol=1e-5)
# the two closed forms the limits use, symbolically (sympy symbols: S and Q are reserved names)
import sympy as sp  # noqa: E402

S_, a_, R_ = sp.symbols("S_len a_acc R_rad", positive=True)
identity(2 * sp.sqrt(S_ / a_), 2 * S_ / sp.sqrt(S_ * a_))
identity(sp.sqrt(a_ * R_), sp.sqrt(a_ / (1 / R_)))
units("(44.26 m/s^2 / (0.1316 m^-1))^(1/2)", "speed")
units("(98.315 m) / (21.838 m/s)", "time")
raise SystemExit(finish())
