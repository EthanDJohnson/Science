#!/usr/bin/env python3
"""Mechanism scales (SI internally; printed in km/s, kau, pc, dimensionless ratios).
1. v_c(s) = sqrt(G M / s) for M = 1.5 Msun.
2. Perspective term: |dv_p| ~ v_sys * theta, theta = s/d (rad), v_sys = 40 km/s (assumed typical
   heliocentric space velocity of disc stars; order of magnitude only). Ratio to v_c(s).
3. Fixed-km/s perturbations (inner-binary photocentre velocity 0.1 km/s; unbound dispersion 0.5 km/s)
   in units of v_c(s): grows as sqrt(s).
4. PM-noise floor in v~ units: sigma_v = 4.74047 km/s * sigma_mu[mas/yr] * sqrt(2) * d[kpc] per axis
   (two stars), for DR3 sigma_mu = 0.02 mas/yr (bright, G ~ 13) and DR4 scaled by 0.42 (ESA model, D-51).
"""
import math

G = 6.67430e-11
MSUN = 1.3271244e20 / G
AU = 1.495978707e11
PC = 3.0856775814913673e16
M = 1.5 * MSUN
vsys = 40e3
print("s[kau]  v_c[km/s]  persp ratio d=50/100/200pc   0.1km/s kick/v_c   0.5km/s/v_c   noise/v_c DR3(d=100,200pc)  DR4")
for skau in (2, 5, 10, 20, 30):
    s = skau * 1e3 * AU
    vc = math.sqrt(G * M / s)
    pr = [vsys * (s / (d * PC)) / vc for d in (50, 100, 200)]
    k1 = 100.0 / vc
    k5 = 500.0 / vc
    nz = [4740.47 * 0.02 * math.sqrt(2) * (d / 1000.0) / vc for d in (100, 200)]
    print(f"{skau:5.0f}  {vc/1e3:8.3f}   {pr[0]:.3f} / {pr[1]:.3f} / {pr[2]:.3f}            {k1:.3f}            {k5:.3f}"
          f"        {nz[0]:.3f} / {nz[1]:.3f}            {nz[0]*0.42:.3f} / {nz[1]*0.42:.3f}")
# gamma bias from a v~ broadening: if a fraction of pairs is shifted, the median moves; for a pure
# quadrature noise sigma (per axis, v~ units) on a median m0 ~ 0.52 (alpha=1.3, D-48):
m0 = 0.5134
for sig in (0.03, 0.05, 0.10):
    # Rayleigh-like quadrature approx for median of |v + n|: m^2 ~ m0^2 + 2 sig^2 * ln2 * (crude)
    m = math.sqrt(m0 ** 2 + 2 * sig ** 2 * math.log(2))
    print(f"unmodelled per-axis noise {sig:.2f} v~ units -> crude median gamma bias (m/m0)^2 = {(m/m0)**2:.3f}")
