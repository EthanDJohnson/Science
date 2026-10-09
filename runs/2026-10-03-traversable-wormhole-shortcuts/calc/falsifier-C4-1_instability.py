"""Falsifier C4-1 (evidence angle): how the published ghost-scalar (Ellis) instability
and the published phantom-EFT cutoff bear on C4's Ellis shortcut.

Inputs (sources quoted in verdicts/C4-1.md):
 - Gonzalez, Guzman & Sarbach 2009 (arXiv:0806.0608) Table I: e-folding time of the single
   unstable mode, tau_unstable = T * r_throat / c, T = 0.846 for the massless (Ellis) member
   (gamma1 = 0), T -> 0.590 for large gamma1. Time measured as proper time at the throat
   (= coordinate time for Phi = 0).
 - Morris-Thorne lateral tidal criterion at an Ellis throat (Phi = 0, b = b0^2/r):
   gamma^2 v^2 xi / b0^2 <= g  ->  b0 >= gamma v sqrt(xi/g)  (this reproduces C4's 4.5 km at 10 km/s).
 - Cline, Jeon & Moore 2004 (hep-ph/0311312): Lorentz-violating cutoff Lambda < 3 MeV.
Units: SI throughout; energies in eV where stated.
"""
import math

c = 2.99792458e8      # m/s
G = 6.67430e-11       # m^3 kg^-1 s^-2
hbar = 1.054571817e-34
lP = math.sqrt(hbar * G / c**3)
eV = 1.602176634e-19
T_ellis = 0.846       # Gonzalez et al. Table I, gamma1 = 0
g = 9.80665

def tau_e(b0):
    return T_ellis * b0 / c

print("== 1. e-folding time of the Ellis unstable mode (Gonzalez et al. T = 0.846) ==")
for b0 in [1.0, 505.0, 4.5e3, 1.0e7]:
    print(f"b0 = {b0:9.3e} m : tau_e = {tau_e(b0):.3e} s")

print("\n== 2. Lifetime of an unattended static throat seeded only by Planck-scale fluctuations ==")
for b0 in [1.0, 505.0, 4.5e3]:
    N = math.log(b0 / lP)
    print(f"b0 = {b0:9.3e} m : N = ln(b0/lP) = {N:.1f} e-folds -> lifetime ~ {N*tau_e(b0):.3e} s = {N*T_ellis:.1f} b0/c")

print("\n== 3. Payload seed and e-folds used during the crossing ==")
def eps_payload(m, b0):
    # perturbation amplitude ~ payload energy / throat energy scale b0 c^4/G
    return G * m / (c**2 * b0)

cases = [
    ("C4 sub-hyp (a): b0=505 m, 10 km/s, transit 0.16 s (C4 text)", 505.0, 0.16, 70.0),
    ("C4 sub-hyp (a): b0=4.5 km, 10 km/s, transit 1.4 s (C4 text)", 4.5e3, 1.4, 70.0),
    ("C4 Ellis b0=1 m, T_thru=6.64e-8 s (observers at 10 m)", 1.0, 6.64e-8, 1.0),
]
for name, b0, t, m in cases:
    N_used = t / tau_e(b0)
    N_avail = math.log(1.0 / eps_payload(m, b0))
    print(f"{name}\n   e-folds during transit = {N_used:.3e} ; e-folds before O(1) growth from payload seed (m={m} kg) = {N_avail:.1f}"
          f" ; amplification exp(N_used) {'overflows (>1e300)' if N_used > 690 else f'= {math.exp(N_used):.2e}'}")

print("\n== 4. Tidal-limited human crossing of an Ellis throat (1 g over 2 m): e-folds vs speed ==")
xi = 2.0
for beta in [3.3356e-5, 1e-3, 0.01, 0.03, 0.1, 0.5, 0.9, 0.99]:
    v = beta * c
    gam = 1 / math.sqrt(1 - beta**2)
    b0 = gam * v * math.sqrt(xi / g)
    # coordinate time to cross proper length l = -b0..+b0 at speed v measured by static observers
    t_cross = 2 * b0 / v
    N_used = t_cross / tau_e(b0)
    N_avail = math.log(1.0 / eps_payload(70.0, b0))
    print(f"v = {beta:8.3e} c : b0 >= {b0:.3e} m, crossing 2b0/v = {t_cross:.3e} s, e-folds used = {N_used:.3e}, "
          f"payload seed allows {N_avail:.1f} -> {'passes' if N_used < N_avail else 'throat collapses first'}")
print("   (e-folds used = 2/(0.846 v/c) = 2.364 c/v, independent of b0)")
beta_min = 2 / T_ellis / math.log(1.0 / eps_payload(70.0, 1e7))
print(f"   minimum speed for a 70 kg payload at b0 ~ 1e7 m: v > {beta_min:.3f} c (order of magnitude)")

print("\n== 5. Phantom-EFT cutoff (Cline, Jeon & Moore: Lambda < 3 MeV) vs throat energy-density scale ==")
hbarc = hbar * c  # J m
Lam = 3e6 * eV
for b0 in [1.0, 1e3, 1e7, 1e8]:
    rho = c**4 / (8 * math.pi * G * b0**2)   # |rho| scale at an Ellis throat, J/m^3
    rho14 = (rho * hbarc**3) ** 0.25 / eV
    print(f"b0 = {b0:9.3e} m : |rho| = {rho:.3e} J/m^3, rho^(1/4) = {rho14:.3e} eV, rho/Lambda^4 = {(rho14*eV/Lam)**4:.3e}")
rho1 = c**4 / (8 * math.pi * G)
b_min = math.sqrt(rho1 * hbarc**3 / Lam**4)
print(f"b0 at which rho^(1/4) = 3 MeV : {b_min:.3e} m ; cutoff length hbar c / Lambda = {hbarc/Lam:.3e} m")
