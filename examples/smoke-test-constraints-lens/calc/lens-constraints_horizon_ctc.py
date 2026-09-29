#!/usr/bin/env python3
"""lens-constraints: causal structure of a superluminal Alcubierre bubble, and chronology.

Units: geometric (G = c = 1, lengths in metres) unless marked SI.

 1. Horizon: in the bubble frame xi = x - v t, null rays obey dxi/dt = v (f - 1) + n_x with |n| = 1.
    Wherever v (1 - f) > 1 every causal direction has dxi/dt < 0.  The sphere f(r_h) = 1 - 1/v exists
    only for v > 1.  Surface gravity of the on-axis horizon kappa = v |f'(r_h)|; thin-wall closed form
    (derived here for the tanh profile, f' = -2 sigma f (1-f)):  kappa = 2 sigma (1 - 1/v).
 2. The half-space xi > r_h can never be reached from xi <= r_h (every point of the plane xi = r_h has
    dxi/dt <= 0 for all causal directions, since f is monotone in r).  Fraction of the wall's negative
    Eulerian energy lying there = stress-energy that must be pre-arranged ahead of the ship.
 3. Hawking-type temperature T = hbar c kappa / (2 pi k_B) (SI), and the time scale 1/(c kappa).
 4. Chronology: superluminal signal speed u in its launch frame; a return leg launched from a frame moving
    at w relative to the first arrives before departure iff w > 2u/(1+u^2) (tachyonic antitelephone;
    derived here with the relativistic velocity addition).
Run: python3 runs/smoke-constraints/calc/lens-constraints_horizon_ctc.py
"""
import math
import sys

sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
import sympy as sp
from gr_tensors import C, G_NEWTON, HBAR, metrics

K_B = 1.380649e-23                  # J/K (exact SI)
L_P = math.sqrt(HBAR * G_NEWTON / C**3)
T_PLANCK = math.sqrt(HBAR * C**5 / G_NEWTON) / K_B
print(__doc__.split(" 1.")[0])
print(f"k_B = {K_B} J/K, L_P = {L_P:.4e} m, T_Planck = {T_PLANCK:.3e} K")

st, s = metrics.alcubierre()
top = metrics.alcubierre_top_hat(s)
rr = sp.symbols("rr", positive=True)


def profile(Rv, sv):
    fexpr = top(rr).subs({s["R"]: Rv, s["sigma"]: sv})
    return sp.lambdify(rr, fexpr, "numpy"), sp.lambdify(rr, sp.diff(fexpr, rr), "numpy")


def bisect(fun, lo, hi, it=200):
    flo = fun(lo)
    for _ in range(it):
        mid = 0.5 * (lo + hi)
        fm = fun(mid)
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return 0.5 * (lo + hi)


# ------------------------------------------------------------------ 1. horizon and surface gravity (toy R = 1 m, sigma = 8/m)
print("\n== 1. Horizon radius and surface gravity, R = 1 m, sigma = 8 /m (toy) and thin-wall formula")
ff, fp = profile(1.0, 8.0)
rgrid = np.linspace(1e-6, 4, 20001)
print(f"   f(0) = {ff(1e-9):.6f}; f'(r) <= 0 on (0, 4R] (f monotone; zeros only from float underflow/saturation): "
      f"{bool(np.all(fp(rgrid) <= 0))}, max f' = {np.max(fp(rgrid)):.1e}")
for vv in (0.5, 0.99, 1.01, 1.5, 2.0, 5.0, 10.0):
    target = 1 - 1 / vv
    if target <= 0:
        print(f"   v = {vv:5.2f}: 1 - 1/v = {target:+.3f} <= 0 -> no horizon (subluminal bubble; every point can signal forward)")
        continue
    rh = bisect(lambda r: ff(r) - target, 1e-6, 6.0)
    kap = vv * abs(fp(rh))
    print(f"   v = {vv:5.2f}: f(r_h) = {target:.4f}, r_h = {rh:.5f} m, kappa = v|f'(r_h)| = {kap:.5f} /m, "
          f"thin-wall 2 sigma (1-1/v) = {2 * 8.0 * target:.5f} /m")

# ------------------------------------------------------------------ 2. energy fraction ahead of the causal plane xi = r_h
print("\n== 2. Share of the wall's negative Eulerian energy in the unreachable half-space xi > r_h")
print("   rho = -(v^2/32 pi) f'(r)^2 sin^2(theta); angular weight g(mu0) = int_mu0^1 (1-mu^2) dmu = 2/3 - mu0 + mu0^3/3")


def fraction(Rv, sv, vv):
    ff, fp = profile(Rv, sv)
    rh = bisect(lambda r: ff(r) - (1 - 1 / vv), 1e-9 * Rv, Rv + 60.0 / sv)
    r = np.linspace(1e-9, Rv + 60.0 / sv, 2_000_001)
    w = fp(r) ** 2 * r**2
    mu0 = np.clip(rh / r, 0.0, 1.0)
    g = np.where(r > rh, 2.0 / 3.0 - mu0 + mu0**3 / 3.0, 0.0)
    return rh, np.trapezoid(w * g, r) / np.trapezoid(w * 4.0 / 3.0, r)


for Rv, sv in ((1.0, 8.0), (100.0, 2.0), (100.0, 200.0)):
    for vv in (1.01, 2.0, 10.0):
        rh, fr = fraction(Rv, sv, vv)
        print(f"   R = {Rv:6.1f} m, Delta = 2/sigma = {2 / sv:6.3f} m, v = {vv:5.2f}: r_h = {rh:.5f} m, share = {fr:.3e}")
print("   (share falls roughly as (Delta/R)^2; it is never zero, so some stress-energy must sit where the ship cannot reach)")

# ------------------------------------------------------------------ 3. temperatures and time scales (thin wall)
print("\n== 3. Horizon temperature T = hbar c kappa/(2 pi k_B) and time scale 1/(c kappa), kappa = 2 sigma (1-1/v)")
qi_delta_lp = {2.0: 93.31, 10.0: 109.9}   # Delta_max/L_P at alpha = 0.1, N = 1 from lens-constraints_qi_wall.py
for vv in (1.01, 2.0, 10.0):
    for label, delta in (("Delta = 1 m", 1.0), ("Delta = 1 mm", 1e-3),
                         ("QI-limited Delta", qi_delta_lp.get(vv, 93.31) * L_P)):
        sv = 2.0 / delta
        kap = 2 * sv * (1 - 1 / vv)
        T = HBAR * C * kap / (2 * math.pi * K_B)
        print(f"   v = {vv:5.2f}, {label:16s} ({delta:.3e} m): kappa = {kap:.3e} /m, T = {T:.3e} K "
              f"(T/T_Planck = {T / T_PLANCK:.1e}), 1/(c kappa) = {1 / (C * kap):.3e} s")
print("   (QI-limited Delta for v = 1.01 uses the v = 2 value as a stand-in)")

# ------------------------------------------------------------------ 4. chronology: antitelephone threshold
print("\n== 4. Two superluminal legs close a causal loop when the second launch frame moves at w > 2u/(1+u^2)")
for u in (1.01, 1.5, 2.0, 5.0, 10.0, 100.0):
    w = 2 * u / (1 + u * u)
    # numeric check: send A->B at speed u in S (distance 1), reply at speed u in S' (velocity -u in S')
    L = 1.0
    ww = w + 0.01 * (1 - w)                # 1% of the way from w_crit to c
    u_ret = (-u + ww) / (1 - u * ww)       # return-leg velocity seen in S
    t_back = L / u - L / u_ret if u_ret > 0 else float("nan")
    print(f"   u = {u:6.2f} c: w_crit = {w:.5f} c; with w = {ww:.5f} c the reply arrives at t = {t_back:+.4f} (units of L/c; < 0 = before departure)")
