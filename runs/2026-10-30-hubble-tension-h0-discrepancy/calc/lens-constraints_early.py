#!/usr/bin/env python3
"""Constraints lens, calc 2: background-level H0 reach of early-time variants at fixed 100 theta_* = 1.0411.
Variants: axion-like EDE (Poulin fluid, n = 3), Delta N_eff, varying electron mass m_e.
Two closures for the late universe: (a) physical omega_c fixed; (b) Omega_m fixed at 0.3175 (BAO/SN-like),
omega_c = Omega_m h^2 - omega_b - omega_nu solved jointly with h.
Plus a crude damping-scale diagnostic theta_D / theta_* (fully ionised plasma above z_*, diffusion integral of
Hu & White 1997), used only as a RATIO between models, with Delta N_eff = +0.13 (1 sigma of ACT DR6 [D-52]) as yardstick.
Cosmology units: H0 km/s/Mpc, distances Mpc.  Convergence: r_D integral at n and 1.5n nodes.
"""
import math
import sys

import numpy as np
from scipy.optimize import brentq

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from cosmo_background import Cosmology, solve_h_from_theta, C_KMS, RHO_CRIT100, MPC_M  # noqa: E402

TH = 1.0411
OB = 0.02237
OC0 = 0.1200
ONU = 0.06 / 93.14
OM_FIX = 0.3175
TARGET = 73.264
SIGMA_T = 6.6524587e-29  # m^2
M_P = 1.67262192e-27     # kg
YP = 0.245


def h_fixed_oc(oc=OC0, z_star=None, **kw):
    return solve_h_from_theta(TH, OB, oc, z_star=z_star, **kw)


def h_fixed_Om(Om=OM_FIX, z_star_fn=None, **kw):
    """Joint solve: h such that 100 theta_* = TH with omega_c = Om h^2 - OB - ONU (bracketed root in h)."""
    def g(h):
        oc = Om * h * h - OB - ONU
        cp = Cosmology(h, OB, oc, **kw)
        zs = z_star_fn(oc) if z_star_fn else cp.z_star()
        return 100.0 * cp.theta_star(zs) - TH
    h = brentq(g, 0.55, 0.95, xtol=1e-9)
    return h, Om * h * h - OB - ONU


def theta_D_over_theta(cp, zs, me_ratio=1.0, n=400):
    """r_D / r_* at recombination; k_D^-2 = int deta * lambda_c /(6(1+R)) * [R^2/(1+R) + 16/15],
    lambda_c = comoving Thomson mean free path for a fully ionised H+He plasma; sigma_T ∝ m_e^-2."""
    ne0 = (1.0 - YP / 2.0) * cp.omega_b * RHO_CRIT100 / M_P   # m^-3 today (ionised)
    sig = SIGMA_T / me_ratio**2
    lna1 = -math.log1p(zs)
    x = np.linspace(-20.0, lna1, n)
    a = np.exp(x)
    H = cp.H_of_a(a)                                           # km/s/Mpc
    deta = C_KMS / (a * H)                                     # Mpc per unit ln a
    lam_c = 1.0 / (ne0 * a**-3 * sig * a) / MPC_M              # comoving mfp in Mpc
    R = cp.R_baryon(a)
    integrand = deta * lam_c / (6.0 * (1.0 + R)) * (R**2 / (1.0 + R) + 16.0 / 15.0)
    kD_m2 = np.trapezoid(integrand, x)
    rD = math.pi * math.sqrt(kD_m2)
    return rD / cp.r_s(zs)


# ---- baseline LCDM
hb = h_fixed_oc()
cb = Cosmology(hb, OB, OC0)
zsb = cb.z_star()
base_ratio = theta_D_over_theta(cb, zsb)
conv = theta_D_over_theta(cb, zsb, n=600) / base_ratio - 1
print(f"LCDM baseline: H0 = {100*hb:.3f}, r_* = {cb.r_s(zsb):.3f} Mpc, r_D/r_* = {base_ratio:.5f} "
      f"(n=400 vs 600 rel. diff {conv:.1e})")

rows = []


def report(label, cp, zs, me_ratio=1.0):
    rs = cp.r_s(zs)
    d = theta_D_over_theta(cp, zs, me_ratio) / base_ratio - 1
    rows.append((label, 100 * cp.h, cp.Omega_m, cp.omega_c, rs, d))
    print(f"  {label:44s} H0 = {100*cp.h:6.2f}  Omega_m = {cp.Omega_m:.4f}  omega_c = {cp.omega_c:.4f}  "
          f"r_* = {rs:7.3f} Mpc  d(theta_D/theta_*) = {100*d:+.2f}%")
    return d


print("\n=== yardstick: Delta N_eff = +0.13 (1 sigma ACT DR6), omega_c fixed ===")
h = h_fixed_oc(N_eff=3.046 + 0.13)
d_yard = report("N_eff = 3.176, omega_c fixed", Cosmology(h, OB, OC0, N_eff=3.176), zsb)
print(f"  yardstick: 1 sigma(N_eff) <-> {100*d_yard:+.3f}% in theta_D/theta_*")

print("\n=== EDE (n = 3, z_c = 3500), H0 from theta_* ===")
for f in (0.0, 0.05, 0.07, 0.10, 0.12, 0.15, 0.20):
    ede = dict(f=f, z_c=3500.0, n=3) if f > 0 else None
    h1 = h_fixed_oc(ede=ede)
    report(f"f_EDE = {f:.2f}, omega_c fixed", Cosmology(h1, OB, OC0, ede=ede), zsb)
    h2, oc2 = h_fixed_Om(ede=ede)
    report(f"f_EDE = {f:.2f}, Omega_m fixed", Cosmology(h2, OB, oc2, ede=ede), Cosmology(h2, OB, oc2).z_star())
for zc in (1500.0, 3500.0, 10000.0):
    g = lambda f: h_fixed_Om(ede=dict(f=f, z_c=zc, n=3))[0] * 100 - TARGET
    try:
        fneed = brentq(g, 0.01, 0.25, xtol=1e-5)
        print(f"  f_EDE needed for H0 = {TARGET} (Omega_m fixed, z_c = {zc:.0f}): {fneed:.3f}")
    except ValueError as e:
        print(f"  z_c = {zc:.0f}: not reached for f < 0.6 ({e})")
    g1 = lambda f: h_fixed_oc(ede=dict(f=f, z_c=zc, n=3)) * 100 - TARGET
    try:
        print(f"  f_EDE needed (omega_c fixed, z_c = {zc:.0f}): {brentq(g1, 0.005, 0.12, xtol=1e-5):.3f}")
    except ValueError:
        print(f"  f_EDE needed (omega_c fixed, z_c = {zc:.0f}): not reached for f < 0.6")

print("\n=== Delta N_eff ===")
for Ne in (2.86, 3.046, 3.12, 3.30, 3.60, 4.0):
    h1 = h_fixed_oc(N_eff=Ne)
    report(f"N_eff = {Ne:.3f}, omega_c fixed", Cosmology(h1, OB, OC0, N_eff=Ne), zsb)
    # z_eq fixed: omega_m scaled by (1 + 0.2271 N_eff)/(1 + 0.2271*3.046)
    s = (1 + 0.22711 * Ne) / (1 + 0.22711 * 3.046)
    oc_eq = (OB + OC0 + ONU) * s - OB - ONU
    h3 = h_fixed_oc(oc=oc_eq, N_eff=Ne)
    report(f"N_eff = {Ne:.3f}, z_eq fixed", Cosmology(h3, OB, oc_eq, N_eff=Ne), zsb)
for lab, fn in [("omega_c fixed", lambda Ne: h_fixed_oc(N_eff=Ne)),
                ("z_eq fixed", lambda Ne: h_fixed_oc(oc=(OB + OC0 + ONU) * (1 + 0.22711 * Ne) / (1 + 0.22711 * 3.046) - OB - ONU, N_eff=Ne)),
                ("Omega_m fixed", lambda Ne: h_fixed_Om(N_eff=Ne)[0])]:
    try:
        Nn = brentq(lambda Ne: fn(Ne) * 100 - TARGET, 3.046, 8.0, xtol=1e-4)
        print(f"  N_eff needed for H0 = {TARGET} ({lab}): {Nn:.2f}  -> {(Nn-2.86)/0.13:.1f} sigma above ACT DR6 2.86 +- 0.13")
    except ValueError:
        print(f"  N_eff needed ({lab}): not reached below 8")

print("\n=== varying m_e (z_*, z_drag ∝ m_e; sigma_T ∝ m_e^-2) ===")
for dm in (0.0, 0.01, 0.02, 0.04, 0.06, 0.08):
    zs = zsb * (1 + dm)
    h1 = h_fixed_oc(z_star=zs)
    report(f"dm_e/m_e = {dm:+.2f}, omega_c fixed", Cosmology(h1, OB, OC0), zs, 1 + dm)
    h2, oc2 = h_fixed_Om(z_star_fn=lambda oc, dm=dm: Cosmology(0.7, OB, oc).z_star() * (1 + dm))
    report(f"dm_e/m_e = {dm:+.2f}, Omega_m fixed", Cosmology(h2, OB, oc2), Cosmology(h2, OB, oc2).z_star() * (1 + dm), 1 + dm)
for lab, fn in [("omega_c fixed", lambda dm: h_fixed_oc(z_star=zsb * (1 + dm))),
                ("Omega_m fixed", lambda dm: h_fixed_Om(z_star_fn=lambda oc: Cosmology(0.7, OB, oc).z_star() * (1 + dm))[0])]:
    try:
        dn = brentq(lambda dm: fn(dm) * 100 - TARGET, 0.0, 0.10, xtol=1e-6)
        print(f"  dm_e/m_e needed for H0 = {TARGET} ({lab}): {100*dn:.2f}%")
    except ValueError:
        print(f"  dm_e/m_e needed ({lab}): not reached below 30%")

print("\n=== varying m_e along the scaling direction: omega_b, omega_c ∝ (1+dm)^2, z_* ∝ (1+dm) ===")


def h_scaling(dm):
    return solve_h_from_theta(TH, OB * (1 + dm) ** 2, OC0 * (1 + dm) ** 2, z_star=zsb * (1 + dm))


for dm in (0.02, 0.04, 0.06, 0.08):
    hs = h_scaling(dm)
    report(f"dm_e/m_e = {dm:+.2f}, omega_i ∝ m_e^2", Cosmology(hs, OB * (1 + dm) ** 2, OC0 * (1 + dm) ** 2),
           zsb * (1 + dm), 1 + dm)
dn = brentq(lambda dm: h_scaling(dm) * 100 - TARGET, 0.0, 0.15, xtol=1e-6)
cs = Cosmology(h_scaling(dn), OB * (1 + dn) ** 2, OC0 * (1 + dn) ** 2)
print(f"  dm_e/m_e needed for H0 = {TARGET} (omega_i ∝ m_e^2): {100*dn:.2f}%; then omega_b = {cs.omega_b:.5f} "
      f"(BBN D/H omega_b ~0.0217-0.0222 [D-46]), Omega_m = {cs.Omega_m:.4f}")
d = report("  -> that solution", cs, zsb * (1 + dn), 1 + dn)
print(f"  damping shift = {d/d_yard:+.1f} yardsticks")

print("\nSummary rows (label, H0, Omega_m, omega_c, r_*, d theta_D/theta_* in units of the 1-sigma N_eff yardstick):")
for r in rows:
    print(f"  {r[0]:44s} {r[1]:6.2f} {r[2]:.4f} {r[3]:.4f} {r[4]:7.3f}  {r[5]/d_yard:+6.1f} yardsticks")
