#!/usr/bin/env python3
"""Falsifier C2-2 (scale angle): the dimensionless stress load the 2024 warp shell puts on its
matter, compared with what any known matter can bear; its scale invariance; its dependence on
compactness C and on the edge-smoothing span.

Units: SI (Pa = J/m^3, kg, m). Ratios are dimensionless (stress / energy density eps = rho c^2).
Input metric: the run's toolkit rebuild tools/warp_shell.py (zero shift; the shift adds only
O(beta) momentum flux, so the static stresses are the load-bearing part).
"""
import math
import sys

import numpy as np

sys.path.insert(0, "runs/2026-10-01-warp-drive-without-negative-energy/tools")
from warp_shell import build_shell, G, C  # noqa: E402

trap = np.trapezoid if hasattr(np, "trapezoid") else np.trapz


def loads(s, frac=0.01):
    """Stress-load ratios of a built shell.
    peak_aniso: max |p_t - p_r| / eps over points with eps > frac * eps_peak
    peak_abs  : max max(|p_r|,|p_t|) / eps over the same points
    mean_aniso: volume-weighted <|p_t - p_r|> / <eps> (proper volume ignored, factor ~1.2)
    virial    : int (p_r + 2 p_t) dV / int eps dV
    DEC_min   : min (eps - max|p|) / eps_peak over all matter points
    """
    r, e, pr, pt = s.r, s.eps, s.p_r, s.p_t
    sel = e > frac * s.eps_peak
    an = np.abs(pt - pr)
    w = 4 * math.pi * r ** 2
    mat = np.maximum(np.abs(e), np.maximum(np.abs(pr), np.abs(pt))) > 1e-12 * s.eps_peak
    dec = (e - np.maximum(np.abs(pr), np.abs(pt)))[mat].min() / s.eps_peak
    return dict(
        peak_aniso=float((an[sel] / e[sel]).max()),
        peak_abs=float((np.maximum(np.abs(pr), np.abs(pt))[sel] / e[sel]).max()),
        mean_aniso=float(trap(w * an, r) / trap(w * e, r)),
        virial=float(trap(w * (pr + 2 * pt), r) / trap(w * e, r)),
        DEC_min=float(dec),
        pt_max=float(pt.max()), eps_peak=float(s.eps_peak))


M0, R1, R2 = 4.49e27, 10.0, 20.0
print("=== A. Published shell (M = 4.49e27 kg, R1 = 10 m, R2 = 20 m), toolkit default smoothing ===")
s0 = build_shell(M0, R1, R2)
L0 = loads(s0)
C0 = 2 * G * M0 / (C ** 2 * R2)
print(f"compactness C = 2GM/(c^2 R2) = {C0:.4f}")
for k, v in L0.items():
    print(f"  {k:11s} = {v:.4g}")

print("\n=== B. Scale invariance at fixed C (M, R1, R2 all x L) ===")
for Lf in (1.0, 10.0, 1e3, 1e6):
    s = build_shell(M0 * Lf, R1 * Lf, R2 * Lf)
    Lq = loads(s)
    print(f"  L = {Lf:8.0e}: R2 = {R2*Lf:9.3e} m, eps_peak = {Lq['eps_peak']:.3e} Pa, "
          f"peak_aniso = {Lq['peak_aniso']:.4f}, mean_aniso = {Lq['mean_aniso']:.4f}, virial = {Lq['virial']:.4f}")

print("\n=== C. Compactness sweep at R1 = 10 m, R2 = 20 m (default smoothing) ===")
rows = []
for Cc in (1e-4, 1e-3, 1e-2, 0.05, 0.1, 0.2, 1 / 3, 0.5):
    M = Cc * C ** 2 * R2 / (2 * G)
    s = build_shell(M, R1, R2)
    Lq = loads(s)
    rows.append((Cc, Lq))
    print(f"  C = {Cc:7.4g}: peak_aniso = {Lq['peak_aniso']:.4e} ({Lq['peak_aniso']/Cc:.3f} C), "
          f"mean_aniso = {Lq['mean_aniso']:.4e} ({Lq['mean_aniso']/Cc:.3f} C), virial = {Lq['virial']:.4e}")
k_peak = rows[0][1]["peak_aniso"] / rows[0][0]
k_mean = rows[0][1]["mean_aniso"] / rows[0][0]
print(f"  weak-field coefficients: peak_aniso ~ {k_peak:.3f} C, mean_aniso ~ {k_mean:.3f} C")

print("\n=== D. Edge-smoothing span (span_P; span_rho = 1.72 span_P), published M, R1, R2 ===")
for sp in (0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 1.0, 1.5, 2.0):
    s = build_shell(M0, R1, R2, span_P=sp)
    Lq = loads(s)
    print(f"  span_P = {sp:4.2f} m: max|p|/eps = {Lq['peak_abs']:.3f}, DEC_min/eps_peak = {Lq['DEC_min']:+.4f}, "
          f"DEC {'holds' if Lq['DEC_min'] >= 0 else 'FAILS'}")

print("\n=== E. Strength / energy-density of known matter (dimensionless, scale-free) ===")
c2 = C ** 2
mats = {
    "graphene, intrinsic 130 GPa, 2267 kg/m^3 [D-44, search-summary]": 130e9 / (2267 * c2),
    "nanodiamond yield 460 GPa, 3510 kg/m^3 [D-44]": 460e9 / (3510 * c2),
    "1 TPa static (DAC) taken over diamond 3510 kg/m^3 [D-44]": 1e12 / (3510 * c2),
}
# Neutron-star crust: bcc Coulomb crystal shear modulus mu = 0.1194 n_i (Z e)^2 / (4 pi eps0 a),
# a = (3/(4 pi n_i))^(1/3); breaking stress = 0.1 mu (Horowitz & Kadau 2009: breaking strain
# ~0.1, defined as maximum stress over shear modulus). Neutron-drip point: 118Kr, rho = 4.3e14 kg/m^3.
e2_4pie0 = 2.307077e-28  # J m
mu_u = 1.66053907e-27
for label, rho, Z, A in (("NS outer crust at drip (118Kr, 4.3e14 kg/m^3)", 4.3e14, 36, 118),
                         ("NS inner crust, illustrative (Z = 40, A_cell = 1000, 8e16 kg/m^3)", 8e16, 40, 1000)):
    n_i = rho / (A * mu_u)
    a = (3 / (4 * math.pi * n_i)) ** (1 / 3)
    mu = 0.1194 * n_i * Z ** 2 * e2_4pie0 / a
    print(f"  {label}: mu = {mu:.3e} Pa, mu/eps = {mu/(rho*c2):.3e}, v_T = {math.sqrt(mu/(rho*c2)):.3e} c")
    mats[f"NS crust breaking stress 0.1 mu, {label}"] = 0.1 * mu / (rho * c2)
for k, v in mats.items():
    print(f"  {k}: sigma_max/eps = {v:.3e}")

print("\n=== F. Gaps: required (published shell) vs best capacity, in orders of magnitude ===")
best = max(mats.values())
best_selfbound = mats["graphene, intrinsic 130 GPa, 2267 kg/m^3 [D-44, search-summary]"]
for name, req in (("peak |p_t - p_r|/eps", L0["peak_aniso"]), ("mean anisotropy", L0["mean_aniso"])):
    print(f"  {name} = {req:.3e}: gap vs NS crust {math.log10(req/best):.2f} orders; "
          f"vs graphene {math.log10(req/best_selfbound):.2f} orders")

print("\n=== G. Shift cap reachable if the matter's strength ratio is the limit ===")
# beta_crit / C = 0.072 at C = 1/3 (M-CONSTRAINTS-13) rising to 0.082 at C = 0.083 (lens data);
# use 0.08 C as a generous weak-field value (linear law beta_max ~ k C Delta/R2 of the idealizer).
for name, cap in (("NS crust (best known, not self-bound)", best),
                  ("graphene (best self-bound)", best_selfbound)):
    C_allow = cap / k_peak
    beta = 0.08 * C_allow
    print(f"  {name}: C_allowed = {C_allow:.2e} -> beta_cap ~ {beta:.2e} c = {beta*C:.3e} m/s"
          f" (mean-load basis: C = {cap/k_mean:.2e}, beta ~ {0.08*cap/k_mean*C:.3e} m/s)")
print(f"  published shell needs beta_cap 0.0239 c = {0.0239*C:.3e} m/s at C = {C0:.3f}")
