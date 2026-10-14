"""Crux C2: numbers that separate C2 from its rivals (SI units unless marked).

1. Ambient cross-fusion lifetime of a 150 Hz graviton (re-check of verdicts C2-0/1/2):
   Gamma_1 = (16 pi/15) G^2 (hbar w) rho_b / c^7.
2. Worst-case self-fusion tail (verdict C2-2 bound A): P(>R) <= (G E/c^4)^2/(c T R),
   so dP/dR = (G E/c^4)^2/(c T R^2); compare with the ambient per-length rate
   dP/dR = N0 Gamma_1 / c to get the R beyond which the ambient term must dominate
   even against the worst-case self term.
3. C5 linear channel: coefficient k needed for P_lin = k * 9.3e-3 pairs (M-EXAMINER-09,
   GW150914) to deplete 1e-2 of the wave energy (standard-siren reach).
4. Bound A at R = c/w and R = lambda relative to B&O's per-packet total 2.9e-6 pairs
   (M-IDEALIZER-09): caps the share any C3/C4 retarded total can have outside r ~ c/w.
"""
import math

G = 6.67430e-11
c = 2.99792458e8
hbar = 1.054571817e-34
Msun = 1.98892e30
pc = 3.0857e16
Mpc = 1e6 * pc

f = 150.0
w = 2 * math.pi * f
E = 2.0 * Msun * c**2          # B&O E_rel [D-27]
T = 1.50e6 / c                 # cT = 1.50e6 m as in verdict C2-2 (T = 5 ms)
lam = c / f
N0 = E / (hbar * w)
print(f"N0 = {N0:.3e} gravitons (D-42 quotes 3.6e78)")

# 1. ambient lifetimes
for label, rho in [("DeltaN_eff=0.3 ceiling [D-33]", 2.84e-15),
                   ("NANOGrav-level [C2-0]", 6.1e-18),
                   ("LVK upper limit [C2-0]", 2.2e-18)]:
    g1 = (16 * math.pi / 15) * G**2 * hbar * w * rho / c**7
    frac = g1 * 410 * Mpc / c
    print(f"[1] {label}: Gamma_1 = {g1:.3e} 1/s, lifetime = {1/g1:.3e} s, "
          f"fraction over 410 Mpc = {frac:.3e}")
    # 2. crossover against worst-case self tail
    A = (G * E / c**4) ** 2 / (c * T)       # pairs * m
    amb = N0 * g1 / c                        # pairs per m
    Rx = math.sqrt(A / amb)
    print(f"[2]   worst-case crossover R_x(bound A) = {Rx:.3e} m = {Rx/pc:.3e} pc "
          f"= {Rx/lam:.3e} wavelengths")

# 3. C5 k threshold
P_lin_over_k = 9.3e-3
P_needed = 1e-2 * N0 / 2.0   # each pair removes ~2 hbar w (two photons of ~w each)
print(f"[3] pairs needed for 1e-2 energy loss = {P_needed:.3e}; k needed = {P_needed/P_lin_over_k:.3e}")

# 4. bound A vs B&O per-packet total
A = (G * E / c**4) ** 2 / (c * T)
P_BO = 2.9e-6
for label, R in [("c/w", c / w), ("lambda", lam), ("10 lambda", 10 * lam)]:
    print(f"[4] bound A P(>{label}) = {A/R:.3e} pairs = {A/R/P_BO:.3f} x B&O total 2.9e-6")
