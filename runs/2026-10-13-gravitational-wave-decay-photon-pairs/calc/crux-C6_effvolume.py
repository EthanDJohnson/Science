"""Crux C6: what B&O's eq.8 <-> eq.14 identity implies, and cross-checks of verdict numbers.

Natural units for coefficients; SI for GW150914 numbers (B&O inputs D-27: f = 150 Hz,
sigma_w = 200 rad/s, E_rel = 2 Msun c^2).

1. Identity: eq.8 dP/dt = 3 G^2 N^2 w^3 sigma^2/(25 pi) equals the kinetic isotropic rate
   (8 pi/15) G^2 rho^2 V with rho = N w / V  iff  V = 40 pi^2/(9 w sigma^2)  (natural units),
   i.e. V_eff = 40 pi^2 c^3/(9 w sigma^2) (SI). Print V_eff, equivalent radius, k*R_eq.
2. Sawyer identity mu/H = 6 (rho_GW/rho_tot)(H/omega)  (symbolic check).
3. Whole-universe yield check (verdict C6-2): 2.78e-109 m^-3 s^-1 x 1.08e79 m^3 x 4.58e17 s.
4. Merger rate density at which per-event near-source yields equal the sustained ensemble
   rate per volume (LVK-limited 1.6e-115 pairs m^-3 s^-1, candidates C6), using per-event
   yields 2.9e-6 pairs (eq.8 x T_eff, C4) and 9.3e-3 k pairs (C5 linear channel, k uncomputed).
"""
import math
import sympy as sp

c = 2.99792458e8
f = 150.0
w = 2 * math.pi * f
sigma = 200.0

# 1. identity
Gs, N, ws, ss, V = sp.symbols('G N w sigma V', positive=True)
eq8 = 3 * Gs**2 * N**2 * ws**3 * ss**2 / (25 * sp.pi)
kin = sp.Rational(8, 15) * sp.pi * Gs**2 * (N * ws / V)**2 * V
Vsol = sp.solve(sp.Eq(eq8, kin), V)[0]
print("1 V_eff (natural units) =", sp.simplify(Vsol), " ; V*w*sigma^2 =", sp.simplify(Vsol * ws * ss**2))
Veff = 40 * math.pi**2 * c**3 / (9 * w * sigma**2)
Req = (3 * Veff / (4 * math.pi)) ** (1 / 3)
print(f"1 GW150914: V_eff = {Veff:.3e} m^3 ; R_eq = {Req:.3e} m ; c/sigma = {c/sigma:.3e} m ; "
      f"R_eq/(c/sigma) = {Req/(c/sigma):.3f} ; k*R_eq = w R_eq/c = {w*Req/c:.2f}")
lam = c / f
print(f"1 lambda = {lam:.3e} m ; R_eq/lambda = {Req/lam:.3f}")

# 2. Sawyer identity
H, rg, rt, om = sp.symbols('H rho_GW rho_tot omega', positive=True)
Gsub = 3 * H**2 / (8 * sp.pi * rt)
mu = 16 * sp.pi * Gsub * rg / om
print("2 mu/H =", sp.simplify(mu / H), " (expect 6 rho_GW H/(rho_tot omega))")

# 3. whole universe
y = 2.78e-109 * 1.08e79 * 4.58e17
print(f"3 pairs per Hubble volume per Hubble time at DeltaN_eff=0.3: {y:.2e}")

# 4. crossover merger rate density
Gpc = 3.0857e25
yr = 3.15576e7
conv = Gpc**3 * yr  # (m^-3 s^-1) -> (Gpc^-3 yr^-1)
ens = 1.6e-115
for label, P in [("eq8 x T_eff (C4)", 2.9e-6), ("C5 linear, per unit k", 9.3e-3)]:
    Rx = ens / P * conv
    print(f"4 crossover merger rate for {label}: {Rx:.2e} Gpc^-3 yr^-1 (divide by k for C5)")
ens_max = 2.78e-109
for label, P in [("eq8 x T_eff (C4)", 2.9e-6)]:
    print(f"4 same at DeltaN_eff=0.3 ceiling: {ens_max / P * conv:.2e} Gpc^-3 yr^-1")
