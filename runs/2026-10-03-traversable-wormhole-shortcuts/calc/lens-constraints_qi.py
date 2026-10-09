"""Constraints lens: quantum-inequality (QI/QEI) constraints on throats, with their validity domains.
Units: SI unless marked; geometric (G = c = 1, metres) where marked; hbar enters via l_P^2 = hbar G / c^3.
1  Single-scale bound for a static Ellis throat: static observers are geodesic (Phi = 0) and see a
   constant rho = -1/(8 pi b0^2) forever, so the Lorentzian average equals rho. Sampling time
   tau0 = f * (curvature radius) = f b0 (curvature radius b0 from lens-constraints_ec_table.py).
   Ford-Roman: <rho> >= -3 l_P^2/(32 pi^2 tau0^4); Fewster-Eveson (Lorentzian): -27 l_P^2/(2048 pi^2 tau0^4).
2  Thin band (Ford-Roman 1996 type): static density rho ~ -1/(8 pi r0 Delta) in a band of thickness Delta,
   tau0 = f Delta  =>  Delta^3 <= 3 r0 l_P^2/(4 pi f^4) (FR constant); compare dossier Q-21 form (r0/(8 f^4 l_P))^(1/3) l_P.
3  Species count: if N free fields each saturate the bound, N_min = |rho_req| / |bound per field|.
   Compare with the Bekenstein-like species bound N < (M_pl/Lambda)^2 [K-22].
4  Validity domain for MMP/MM: magnetic length l_B = r_e sqrt(2/q) (q flux quanta, LLL), with the extremal magnetic RN relation r_e = sqrt(pi) q l_P / g4 (Heaviside-Lorentz, hbar = c = 1; linear in q as MMP state r_e ~ q),
   so the flat-space QI applies only for tau0 << l_B.
"""
import math
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from gr_tensors import qi, to_si, PLANCK_LENGTH as LP, C, G_NEWTON, HBAR

print(f"l_P = {LP:.4e} m")
print("=== 1. Single-scale throat bound (static geodesic observer at an Ellis throat) ===")
for f in (0.01, 0.1):
    bmax_fr = math.sqrt(3 / (4 * math.pi)) * LP / f**2
    bmax_fe = math.sqrt(27 / (256 * math.pi)) * LP / f**2
    # numerical check with the toolkit: at b0 = bmax_fr the bound equals |rho|
    rho = -1 / (8 * math.pi * bmax_fr**2)
    bound = qi.ford_roman_geometric(f * bmax_fr)
    print(f"f={f}: b0_max(Ford-Roman) = {bmax_fr/LP:.4e} l_P = {bmax_fr:.4e} m; b0_max(Fewster-Eveson) = {bmax_fe/LP:.4e} l_P = {bmax_fe:.4e} m; check rho/bound at b0_max = {rho/bound:.6f}")
# a constant density has Lorentzian average equal to itself (toolkit check)
import numpy as np
print("lorentzian_average of a constant -1.0:", qi.lorentzian_average(lambda tau: -np.ones_like(tau), 1.0))
f = 0.01
for b0 in (1.0, 1.5e7):
    rho_si = to_si.energy_density_j_per_m3(-1 / (8 * math.pi * b0**2))
    bound_si = qi.ford_roman_si(f * b0 / C)
    print(f"b0 = {b0:.3g} m: required rho = {rho_si:.4e} J/m^3; FR bound at tau0 = f b0/c = {f*b0/C:.3e} s: {bound_si:.4e} J/m^3; ratio = {rho_si/bound_si:.3e}")

print("\n=== 2. Thin-band bound ===")
for r0, lab in ((1.0, "1 m"), (1.5e7, "1.5e7 m (MM tidal minimum)"), (9.4607e15, "1 ly")):
    d_fr = (3 * r0 * LP**2 / (4 * math.pi * f**4)) ** (1 / 3)
    d_q21 = (r0 / (8 * f**4 * LP)) ** (1 / 3) * LP
    print(f"r0 = {lab}: Delta_max (FR constant) = {d_fr:.3e} m = {d_fr/LP:.3e} l_P; dossier Q-21 form = {d_q21:.3e} m; ratio Delta/r0 = {d_fr/r0:.3e}")

print("\n=== 3. Species count needed to saturate the QI with N free fields (f = 0.01, single scale) ===")
coef = 2048 * math.pi * f**4 / 216   # N_min = coef (b0/l_P)^2  [from 1/(8 pi b0^2) vs 3 l_P^2 /(32 pi^2 f^4 b0^4) ... per field]
coef = (1 / (8 * math.pi)) / (3 / (32 * math.pi**2 * f**4))   # N_min = coef * (b0/l_P)^2 with the Ford-Roman constant
print(f"N_min = {coef:.4e} (b0/l_P)^2  (Ford-Roman constant)")
for b0, lab in ((1e-18, "1e-18 m"), (2e-19 * 1e3, "2e-16 m"), (1.0, "1 m"), (1.5e7, "1.5e7 m")):
    print(f"b0 = {lab}: N_min = {coef*(b0/LP)**2:.3e}")
for Nmax, lab in ((1e32, "TeV cutoff, N < 1e32"),):
    bmax = math.sqrt(Nmax / coef) * LP
    print(f"{lab}: largest throat with N <= Nmax: b0 <= {bmax:.3e} m")

print("\n=== 4. Magnetic length in MMP/MM throats vs QI sampling time ===")
for g4 in (0.1, 0.30282212, 1.0):   # 0.3028 = e in Heaviside-Lorentz units
    for re in (1.5e7, 2e-19):
        q = re * g4 / (math.sqrt(math.pi) * LP)
        lB = re * math.sqrt(2 / q)
        print(f"g4={g4}, r_e={re:.2e} m: q = {q:.3e}, l_B = {lB:.3e} m = {lB/LP:.3f} l_P; tau0 = 0.01 r_e = {0.01*re:.2e} m >> l_B: {0.01*re > lB}")
