#!/usr/bin/env python3
"""Constraints lens, calc 3: late-time routes.
(1) Constant-w dark energy that keeps the CMB (theta_*, omega_b, omega_c fixed) and reaches H0 = 73.264.
(2) A late 'step' in H^2 below z_t (hockey stick), tuned so the true H0 = 73.264.
For each: theta_* shift, BAO D_M/r_d and D_H/r_d residuals vs the CMB-LCDM model at representative DESI-like z,
SN Hubble-diagram shape residual (offset-free), the H0 a ladder would infer from 0.023 < z < 0.15 with SH0ES-like
cosmography (q0 = -0.55, j0 = 1), and the minimum effective w of the dark sector (NEC: w < -1 means rho+p < 0).
(3) M_B transition: G ratio needed for Delta M = -0.17 to -0.19 mag under two luminosity scalings, and lookback times.
Units: km/s/Mpc, Mpc, mag, Myr.
"""
import math
import sys

import numpy as np
from scipy.optimize import brentq

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from cosmo_background import Cosmology, solve_h_from_theta, C_KMS  # noqa: E402

TH, OB, OC = 1.0411, 0.02237, 0.1200
TARGET = 73.264
h0 = solve_h_from_theta(TH, OB, OC)
base = Cosmology(h0, OB, OC)
zs = base.z_star()
rd = base.r_d("aubourg")
ZB = [0.295, 0.51, 0.706, 0.934, 1.321, 1.484, 2.33]
ZSN = [0.023, 0.05, 0.10, 0.15, 0.30, 0.50, 0.70, 1.00]
print(f"Base CMB-LCDM: H0 = {100*h0:.2f}, Omega_m = {base.Omega_m:.4f}, r_d = {rd:.2f} Mpc, z_* = {zs:.1f}")


def ladder_H0(cp, q0=-0.55, j0=1.0):
    zz = np.linspace(0.0233, 0.15, 60)
    vals = []
    for z in zz:
        dl = cp.D_L(z)
        cosmog = C_KMS * z * (1 + 0.5 * (1 - q0) * z - (1.0 / 6.0) * (1 - q0 - 3 * q0**2 + j0) * z**2)
        vals.append(cosmog / dl)
    vals = np.array(vals)
    # SH0ES-like: equal weight in log distance -> geometric mean
    return float(np.exp(np.mean(np.log(vals))))


def describe(label, cp, w_eff_min):
    th = 100 * cp.r_s(zs) / cp.D_M(zs)
    print(f"\n{label}: true H0 = {cp.H0:.2f}, Omega_m = {cp.Omega_m:.4f}, 100theta_* = {th:.5f} "
          f"({(th-TH)/0.0003:+.1f} sigma), min w_eff(DE) = {w_eff_min:.3f} -> NEC {'VIOLATED' if w_eff_min < -1 else 'ok'}")
    print("   BAO residuals vs CMB-LCDM (same r_d): " + ", ".join(
        f"z={z}: DM {100*(cp.D_M(z)/base.D_M(z)-1):+.2f}% DH {100*(cp.D_H(z)/base.D_H(z)-1):+.2f}%" for z in ZB))
    dmu = np.array([cp.distance_modulus(z) - base.distance_modulus(z) for z in ZSN])
    ref = np.mean(dmu[4:])  # offset fixed by the z >= 0.3 SNe (M_B free)
    print("   SN shape residual (mag, offset set by z>=0.3): " + ", ".join(f"z={z}: {d-ref:+.3f}" for z, d in zip(ZSN, dmu)))
    print(f"   H0 a ladder would infer from 0.023<z<0.15 (q0=-0.55): {ladder_H0(cp):.2f} (base model: {ladder_H0(base):.2f})")


# (1) constant w
def h_of_w(w):
    return solve_h_from_theta(TH, OB, OC, w0=w)
w_need = brentq(lambda w: 100 * h_of_w(w) - TARGET, -2.0, -1.0, xtol=1e-6)
cw = Cosmology(h_of_w(w_need), OB, OC, w0=w_need)
describe(f"(1) constant w = {w_need:.3f} at fixed theta_*, omega_b, omega_c", cw, w_need)
# DESI DR2 best-fit CPL for reference (direction of H0)
hcpl = solve_h_from_theta(TH, OB, OC, w0=-0.42, wa=-1.75)
print(f"   reference: CPL (w0, wa) = (-0.42, -1.75) [D-51] at fixed theta_*: H0 = {100*hcpl:.2f} (direction: down)")


# (2) step in H^2 below z_t
def step_model(zt, amp, width=0.15):
    """rho_x(z) = amp * S(z), S = 1/(1+exp((ln(1+z)-ln(1+zt))/(width*ln(1+zt)+1e-3))); amp in omega units.
    Dark-energy closure is re-done by Cosmology, so we must ADD amp at z=0 and compensate Lambda: we use
    w0=-1 Lambda fixed at the base value by passing the base h only via omega totals (see below)."""
    lz = math.log1p(zt)
    def S(z):
        return 1.0 / (1.0 + math.exp(min(700.0, (math.log1p(z) - lz) / (width * lz + 1e-3))))
    return S


for zt in (0.01, 0.05, 0.15, 0.30):
    S = step_model(zt, 1.0)
    # choose amplitude so that H0^2 = base H0^2 + 1e4*amp*S(0); keep Lambda at the base value:
    amp = ((TARGET / 100.0) ** 2 - h0**2) / S(0.0)
    oL = base.omega_de0
    rho_x = lambda z, S=S, amp=amp: amp * S(z)
    cp = Cosmology(TARGET / 100.0, OB, OC, rho_x=rho_x)
    # Cosmology's closure puts omega_de0 = h^2 - matter - rad - rho_x(0); check it equals base Lambda
    a = np.linspace(0.3, 1.0, 400)
    zz = 1 / a - 1
    rho = np.array([oL + amp * S(z) for z in zz])
    w_eff = -1.0 - np.gradient(np.log(rho), np.log(a)) / 3.0
    print(f"\n(2) step at z_t = {zt}: omega_x amplitude = {amp:.5f}, Lambda kept: {abs(cp.omega_de0-oL) < 1e-6} "
          f"(omega_de0 {cp.omega_de0:.5f} vs {oL:.5f})")
    describe(f"(2) step in H^2 below z_t = {zt}", cp, float(w_eff.min()))

# (3) M_B / G_eff transition
print("\n(3) M_B transition (Hubble-flow SNe brighter than calibrators by |dM|)")
for dM in (0.146, 0.172, 0.188):
    lr = 10 ** (0.4 * dM)
    print(f"   |dM| = {dM:.3f} mag: luminosity ratio far/near = {lr:.4f}; G_far/G_near = {lr**(-2/3):.4f} if L ∝ G^-3/2 "
          f"(Chandrasekhar, Marra-Perivolaropoulos [D-92]); = {lr**(1/1.5):.4f} if standardised L rises with G "
          f"(Wright & Li 2018 sign; exponent ~+1.5 read roughly from their Fig. 7)")


def lookback_myr(cp, z):
    mpc_km, myr_s = 3.0856775814913673e19, 3.15576e13
    zz = np.linspace(0.0, z, 2001)
    f = 1.0 / ((1 + zz) * cp.H(zz))
    return float(np.trapezoid(f, zz)) * mpc_km / myr_s


for z in (0.005, 0.01, 0.0233, 0.15):
    print(f"   lookback time to z = {z}: {lookback_myr(base, z):.0f} Myr (n=2001); "
          f"check n=3001: {lookback_myr(base, z):.0f}; comoving distance {base.D_C(z):.1f} Mpc")
