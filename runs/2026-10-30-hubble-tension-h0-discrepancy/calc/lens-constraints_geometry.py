#!/usr/bin/env python3
"""Constraints lens, calc 1: the gap, the inverse-distance-ladder (H0*r_d) budget, the theta_* budget,
CMB-side and BAO+BBN-side systematic sizes, and ages.  Cosmology units: H0 in km/s/Mpc, distances in Mpc.

Inputs (dossier IDs):
  local:  H0DN corrected 73.264 +- 0.806 [D-22]; SH0ES 73.49 +- 0.93 [D-20]
  early:  CMB-SPA 67.19 +- 0.38, Omega_m 0.3175 +- 0.0055, r_d 147.00 +- 0.24 [D-44]; Planck PR4 67.64 +- 0.52 [D-41];
          DESI DR2 BAO LCDM Omega_m 0.2975 +- 0.0086, h r_d 101.54 +- 0.73 Mpc (corr -0.92); DESI+BBN 68.50 +- 0.58 [D-45]
          Knox-Millea beta = c/(r_d H0) = 29.54 +- 0.406 [D-03]; 100 theta_* = 1.0411 +- 0.0003 [D-40]
"""
import math
import sys

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from cosmo_background import Cosmology, solve_h_from_theta, r_d_aubourg, C_KMS  # noqa: E402

print("=== A. The gap (naive, uncorrelated) ===")
local = {"H0DN corrected [D-22]": (73.264, 0.806), "SH0ES HST+JWST [D-20]": (73.49, 0.93)}
early = {"CMB-SPA [D-44]": (67.19, 0.38), "Planck PR4 [D-41]": (67.64, 0.52),
         "DESI DR2 BAO+BBN [D-45]": (68.50, 0.58), "inverse ladder flat LCDM [D-48]": (67.67, 0.685)}
for ln, (hl, sl) in local.items():
    for en, (he, se) in early.items():
        d = hl - he
        s = math.hypot(sl, se)
        print(f"{ln:24s} - {en:32s}: dH0 = {d:5.2f} km/s/Mpc = {100*d/he:4.1f}% of early, "
              f"5log10 ratio = {5*math.log10(hl/he):.3f} mag, naive {d/s:4.1f} sigma")

print("\n=== B. Inverse distance ladder: r_d required for a local H0 ===")
rd_cmb, srd_cmb = 147.00, 0.24
hrd_desi, s_hrd_desi = 101.54, 0.73
hrd_cmb = 0.6719 * rd_cmb
beta, sbeta = 29.54, 0.406
rdH_km = C_KMS / beta     # r_d * H0 in km/s
for name, hrd, shrd in [("DESI DR2 LCDM h r_d", hrd_desi, s_hrd_desi),
                        ("CMB-SPA h r_d (0.6719*147.00)", hrd_cmb, 0.0),
                        ("Knox-Millea beta (BOSS+Pantheon)", rdH_km / 100.0, rdH_km / 100.0 * sbeta / beta)]:
    print(f"{name}: h*r_d = {hrd:.2f} +- {shrd:.2f} Mpc; with r_d = 147.00 -> H0 = {100*hrd/rd_cmb:.2f} km/s/Mpc")
    for ln, (hl, sl) in local.items():
        rd_req = hrd / (hl / 100.0)
        srd = rd_req * math.hypot(shrd / hrd if hrd else 0.0, sl / hl)
        print(f"   {ln:24s}: r_d required = {rd_req:6.2f} +- {srd:4.2f} Mpc; reduction vs 147.00 = "
              f"{100*(1-rd_req/rd_cmb):4.2f}%; tension with CMB r_d = {(rd_cmb-rd_req)/math.hypot(srd, srd_cmb):.1f} sigma")

print("\n=== C. theta_* budget: r_* reduction needed when late-time LCDM is kept ===")
ob = 0.02237
Om_cmb, h_cmb = 0.3175, 0.6719
onu = 0.06 / 93.14
oc_cmb = Om_cmb * h_cmb**2 - ob - onu
c0 = Cosmology(h_cmb, ob, oc_cmb)
zs0 = c0.z_star()
DM0 = c0.D_M(zs0)
rs0 = c0.r_s(zs0)
print(f"CMB-SPA-like LCDM: omega_c = {oc_cmb:.5f}, z_* = {zs0:.2f}, r_* = {rs0:.3f} Mpc, D_M(z_*) = {DM0:.2f} Mpc, "
      f"100 theta_* = {100*rs0/DM0:.5f}")
# convergence/accuracy check of the built-in quadratures against scipy quad
dm_q = quad(lambda z: C_KMS / c0.H(z), 0, zs0, limit=500, epsabs=0, epsrel=1e-11)[0]
rs_q = quad(lambda lna: c0._rs_integrand(np.array([lna]))[0], -35.0, -math.log1p(zs0), limit=500, epsrel=1e-11)[0]
print(f"  check: D_M quad = {dm_q:.4f} (rel diff {dm_q/DM0-1:.1e}); r_* quad(from lna=-35) = {rs_q:.4f} "
      f"(rel diff {rs_q/rs0-1:.1e})")
for ln, (hl, sl) in local.items():
    h = hl / 100.0
    # (i) Omega_m fixed (BAO+SN fix Omega_m): omega_c scales with h^2
    oc_i = Om_cmb * h**2 - ob - onu
    ci = Cosmology(h, ob, oc_i)
    dm_i = ci.D_M(zs0)
    # (ii) physical omega_c fixed (CMB peak heights fix omega_c)
    cii = Cosmology(h, ob, oc_cmb)
    dm_ii = cii.D_M(zs0)
    print(f"{ln}: to keep theta_* at H0 = {hl}: r_* must fall by {100*(1-dm_i/DM0):.2f}% (Omega_m fixed at {Om_cmb}; "
          f"omega_c -> {oc_i:.4f}, +{100*(oc_i/oc_cmb-1):.1f}%) or by {100*(1-dm_ii/DM0):.2f}% (omega_c fixed; then "
          f"Omega_m = {cii.Omega_m:.3f})")

print("\n=== D. CMB-side systematic: what LCDM parameter shift gives H0_local from theta_* ===")
th = 1.0411
h_base = solve_h_from_theta(th, ob, 0.1200)
print(f"LCDM omega_b = 0.02237, omega_c = 0.1200, 100theta_* = 1.0411 -> H0 = {100*h_base:.2f} km/s/Mpc")
for ln, (hl, sl) in local.items():
    oc_need = brentq(lambda oc: solve_h_from_theta(th, ob, oc) - hl / 100.0, 0.07, 0.12)
    th_need = brentq(lambda t: solve_h_from_theta(t, ob, 0.1200) - hl / 100.0, 1.03, 1.08)
    print(f"{ln}: needs omega_c = {oc_need:.4f} (shift {oc_need-0.12:+.4f} = {(oc_need-0.12)/0.0012:+.0f} x Planck "
          f"sigma 0.0012; Omega_m = {(oc_need+ob+onu)/(hl/100)**2:.3f}) at fixed theta_*; or 100theta_* = {th_need:.4f} "
          f"({(th_need-th)/0.0003:+.0f} sigma) at fixed omega_c")

def rd_fit(omega_b, omega_cb, omega_nu=0.0006442):
    """Aubourg 2015 eq. 16 without the range guard (mild extrapolation to omega_cb ~ 0.10 is flagged in output)."""
    return 55.154 * math.exp(-72.3 * (omega_nu + 0.0006) ** 2) / (omega_cb**0.25351 * omega_b**0.12807)


print("\n=== E. BAO+BBN side: Omega_m that DESI h r_d needs for H0_local (LCDM, BBN omega_b) ===")
for ob_bbn in (0.02218, 0.02166):
    def h_of_Om(Om):
        return brentq(lambda h: h * rd_fit(ob_bbn, Om * h**2 - onu) - hrd_desi, 0.55, 0.95)
    h_desi = h_of_Om(0.2975)
    print(f"omega_b = {ob_bbn}: at DESI Omega_m = 0.2975, h r_d = 101.54 -> H0 = {100*h_desi:.2f}, "
          f"r_d = {hrd_desi/h_desi:.2f} Mpc")
    for ln, (hl, sl) in local.items():
        Om_need = brentq(lambda Om: h_of_Om(Om) - hl / 100.0, 0.22, 0.50)
        print(f"   {ln}: Omega_m needed = {Om_need:.4f} ({(Om_need-0.2975)/0.0086:+.1f} sigma from DESI 0.2975+-0.0086); "
              f"r_d = {hrd_desi/(hl/100):.2f} Mpc")
    # sensitivity d ln H0 / d ln Omega_m along the BAO+BBN constraint
    e = 1e-3
    s = (math.log(h_of_Om(0.2975 * (1 + e))) - math.log(h_of_Om(0.2975 * (1 - e)))) / (2 * e)
    print(f"   d ln H0 / d ln Omega_m along DESI h r_d = const, BBN omega_b fixed: {s:.3f}")


print("\n=== F. Ages t0 (LCDM background, radiation included) ===")
def t0_gyr(cp):
    mpc_km = 3.0856775814913673e19
    gyr_s = 3.15576e16
    f = lambda lna: 1.0 / cp.H_of_a(np.array([math.exp(lna)]))[0]
    val = quad(f, -30.0, 0.0, limit=400, epsrel=1e-10)[0]
    return val * mpc_km / gyr_s
for (h, Om, lab) in [(0.6719, 0.3175, "CMB-SPA LCDM"), (0.7326, 0.3175, "H0DN H0, Omega_m CMB"),
                     (0.7326, 0.2975, "H0DN H0, Omega_m DESI"), (0.7326, 0.30, "H0DN H0, Omega_m 0.30")]:
    cp = Cosmology(h, ob, Om * h**2 - ob - onu)
    print(f"{lab:26s}: H0 = {100*h:.2f}, Omega_m = {Om:.4f} -> t0 = {t0_gyr(cp):.3f} Gyr "
          f"(GC age 13.81 +- 0.34 Gyr [D-55]: {(t0_gyr(cp)-13.81)/math.hypot(0.25,0.23):+.1f} sigma)")
