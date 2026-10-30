#!/usr/bin/env python3
"""Constraints lens, calc 4: (A) local-void requirement vs LCDM cosmic variance (Eisenstein-Hu 1998 no-wiggle P(k),
sigma8-normalised, top-hat spheres), with linear and Bernardeau-1992 nonlinear delta; Copernican offset bound.
(B) Null / reframe: error inflation needed for 2-sigma consistency; non-Cepheid local classes vs CMB-SPA and H0DN.
Units: km/s/Mpc, Mpc and h^-1 Mpc as labelled.  Convergence: sigma(R) with n and 1.5n k-nodes.
"""
import math

import numpy as np

# ---------------- (A) void
h, Om, ob, s8, ns = 0.6719, 0.3175, 0.02237, 0.8137, 0.9679   # CMB-SPA [D-44]
om = Om * h * h
fb = ob / om
theta = 2.7255 / 2.7


def T_nw(k_h):
    """EH98 no-wiggle transfer function, k in h/Mpc (eqs. 26, 28-31)."""
    s = 44.5 * math.log(9.83 / om) / math.sqrt(1 + 10 * ob**0.75)          # Mpc
    aG = 1 - 0.328 * math.log(431 * om) * fb + 0.38 * math.log(22.3 * om) * fb**2
    k = k_h * h                                                           # 1/Mpc
    Geff = Om * h * (aG + (1 - aG) / (1 + (0.43 * k * s) ** 4))
    q = k_h * theta**2 / Geff
    L0 = np.log(2 * math.e + 1.8 * q)
    C0 = 14.2 + 731 / (1 + 62.5 * q)
    return L0 / (L0 + C0 * q * q)


def W(x):
    return 3 * (np.sin(x) - x * np.cos(x)) / x**3


def sig2_raw(R, n):
    lk = np.linspace(math.log(1e-5), math.log(50.0), n)
    k = np.exp(lk)
    P = k**ns * T_nw(k) ** 2
    return np.trapezoid(k**3 * P * W(k * R) ** 2, lk) / (2 * math.pi**2)


for n in (4000, 6000):
    A = s8**2 / sig2_raw(8.0, n)
    print(f"n = {n}: " + ", ".join(f"sigma(R={R} Mpc/h) = {math.sqrt(A*sig2_raw(R, n)):.4f}" for R in (8, 50, 100, 150, 300, 450)))
A = s8**2 / sig2_raw(8.0, 6000)
f = Om**0.55
gap_frac = 73.264 / 67.19 - 1
d_lin = -3 * gap_frac / f
d_nl = (1 - 2 * gap_frac / f) ** 1.5 - 1        # Bernardeau 1992: dH/H = -(f/2)[(1+d)^(2/3)-1]
print(f"f = Omega_m^0.55 = {f:.3f}; needed dH/H = {100*gap_frac:.2f}% -> delta_lin = {d_lin:.3f}, delta_NL(Bernardeau) = {d_nl:.3f}")
for R in (50, 100, 150, 300, 450):
    sg = math.sqrt(A * sig2_raw(R, 6000))
    sH = f * sg / 3
    print(f"  R = {R:3d} h^-1 Mpc ({R/h:5.0f} Mpc, edge z ~ {R/h*67.19/299792.458:.3f}): sigma_delta = {sg:.4f}, "
          f"sigma(dH/H) top-hat = {100*sH:.2f}% = {67.19*sH:.2f} km/s/Mpc; needed delta_lin is {abs(d_lin)/sg:.1f} sigma")
print("  (the void must extend past the Hubble-flow sample edge z = 0.15, i.e. R >~ 640 Mpc = 430 h^-1 Mpc, "
      "or the SN Hubble diagram shows the edge [D-11])")
for vmax in (370.0, 100.0):
    for Rv in (300.0, 640.0):
        d = vmax / (73.264 - 67.19)
        print(f"  Copernican: |v| < {vmax:.0f} km/s and dH = 6.07 -> offset from void centre < {d:.0f} Mpc; "
              f"for R = {Rv:.0f} Mpc random-position probability (d/R)^3 = {(d/Rv)**3:.1e}")

# ---------------- (B) null and reframe
print("\n(B) error inflation for 2-sigma consistency")
for ln, hl, sl in [("H0DN corrected", 73.264, 0.806), ("SH0ES", 73.49, 0.93)]:
    for en, he, se in [("CMB-SPA", 67.19, 0.38), ("BAO+BBN", 68.50, 0.58)]:
        need = (hl - he) / 2.0
        sl_need = math.sqrt(max(need**2 - se**2, 0))
        print(f"  {ln} vs {en}: need total sigma {need:.2f}; local sigma would have to be {sl_need:.2f} "
              f"(x{sl_need/sl:.1f}) or an unmodelled common shift of {hl-he-2*math.hypot(sl, se):.2f} km/s/Mpc")

print("\nnon-Cepheid local classes (symmetrised errors; stat+sys in quadrature; treated as independent - an approximation)")
cls = {"TDCOSMO-2026 time delays [D-31]": (71.1, 2.35), "masers Stiskalek 2026 (stat only) [D-32]": (71.6, 3.7),
       "GWTC-5 sirens [D-33]": (71.7, 8.45), "SBF Jensen 2025 [D-29]": (73.8, math.hypot(0.7, 2.3)),
       "CCHP TRGB 2025 [D-24]": (70.39, math.sqrt(1.22**2 + 1.33**2 + 0.70**2))}


def comb(keys):
    x = np.array([cls[k][0] for k in keys]); s = np.array([cls[k][1] for k in keys])
    w = 1 / s**2
    m = np.sum(w * x) / np.sum(w); sm = 1 / math.sqrt(np.sum(w))
    chi_self = float(np.sum(w * (x - m) ** 2))
    return m, sm, chi_self, len(keys)


sets = {"one-step (TD+masers+sirens)": list(cls)[:3],
        "one-step + SBF (no SN, no Cepheid)": list(cls)[:4],
        "one-step + SBF + CCHP TRGB (no Cepheid)": list(cls)}
for name, keys in sets.items():
    m, sm, chi, n = comb(keys)
    print(f"  {name}: {m:.2f} +- {sm:.2f}; chi2/dof about own mean {chi:.2f}/{n-1}; "
          f"vs CMB-SPA 67.19+-0.38: {(m-67.19)/math.hypot(sm,0.38):.1f} sigma; vs H0DN 73.264+-0.806: "
          f"{(m-73.264)/math.hypot(sm,0.806):+.1f} sigma; vs BAO+BBN 68.50+-0.58: {(m-68.50)/math.hypot(sm,0.58):.1f} sigma")
