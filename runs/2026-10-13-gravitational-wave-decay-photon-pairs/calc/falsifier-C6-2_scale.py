"""Falsifier C6, refuter 2 (scale angle).

Question: is the isotropic-background kinetic rate (B&O eq. 14,
Gamma/V = (8 pi/15) G^2 rho^2 / c^7 in SI, (8 pi/15) G^2 rho^2 natural)
negligible at every scale an allowed background can reach, and what
would be *required* to make it matter?

Units: SI unless marked 'natural' (hbar = c = k_B = 1, G = 1/M_Pl^2).
"""
import math

# --- constants (SI) ---
G = 6.67430e-11
c = 2.99792458e8
hbar = 1.054571817e-34
kB = 1.380649e-23
a_rad = 7.5657e-16          # J m^-3 K^-4
T0 = 2.7255                  # K
H0 = 67.4e3 / 3.0857e22      # s^-1
eV = 1.602176634e-19
M_Pl_GeV = 1.22089e19        # GeV (G = 1/M_Pl^2)

def gamma_SI(rho):
    """pairs m^-3 s^-1 for energy density rho [J/m^3]"""
    return 8 * math.pi / 15 * G**2 * rho**2 / c**7

# 0) coefficient cross-check: B&O's substitution V w sigma^2 -> 40 pi^2/9 in eq. 8
coef_sub = 3 / (25 * math.pi) * 40 * math.pi**2 / 9
print(f"[0] 3/(25pi) * 40pi^2/9 = {coef_sub:.12f};  8pi/15 = {8*math.pi/15:.12f}; equal: {abs(coef_sub-8*math.pi/15)<1e-12}")

# 1) maximum allowed present-day background from DeltaN_eff
rho_gam = a_rad * T0**4
print(f"[1] rho_gamma(T0) = {rho_gam:.4e} J/m^3")
for dN in (0.3, 0.1, 0.05):
    rho_gw = 7/8 * (4/11)**(4/3) * dN * rho_gam
    G_ = gamma_SI(rho_gw)
    print(f"    DeltaN_eff={dN}: rho_GW={rho_gw:.3e} J/m^3, Gamma={G_:.3e} pairs m^-3 s^-1")

# 2) integrated over the present Hubble volume and a Hubble time (plasma ignored,
#    no redshift dilution: an over-estimate for late times)
rho_max = 7/8 * (4/11)**(4/3) * 0.3 * rho_gam
R_H = c / H0
V_H = 4/3 * math.pi * R_H**3
t_H = 1 / H0
N_pairs = gamma_SI(rho_max) * V_H * t_H
print(f"[2] Hubble radius {R_H:.3e} m, V_H {V_H:.3e} m^3, t_H {t_H:.3e} s")
print(f"    pairs in whole Hubble volume over a Hubble time, DeltaN_eff=0.3: {N_pairs:.3e}")
# with stimulated emission by the CMB at 25 Hz (Rayleigh-Jeans 1+2f ~ 2kT/(h f))
f25 = 25.0
stim = 1 + 2 / math.expm1(2*math.pi*hbar*f25/(kB*T0))
print(f"    CMB stimulation factor at 25 Hz: {stim:.3e}; stimulated pairs: {N_pairs*stim:.3e}")
E_pairs = N_pairs * stim * 2 * kB * T0 * 2   # each stimulated pair carries ~ 2 x 2kT? use 4kT upper bound
print(f"    energy into photons (<= 4 kT0 per stimulated pair): {E_pairs:.3e} J;  vs rho_GW V_H = {rho_max*V_H:.3e} J")

# 3) radiation era, natural units: fraction of GW energy converted per Hubble time
#    F = Gamma * E_pair / (rho_GW H), E_pair <= 4T (stimulated, w << T), x = rho_GW/rho_tot
#    F = (32 pi/15) x sqrt(pi g*/80) (T/M_Pl)^3
def F_frac(x, gstar, T_over_MPl):
    return 32*math.pi/15 * x * math.sqrt(math.pi*gstar/80) * T_over_MPl**3
# check the closed form numerically at one point against the direct expression
T = 1e-3; gstar = 106.75; x = 0.107
rho_tot = math.pi**2/30*gstar*T**4
rho_gw = x*rho_tot
Gam = 8*math.pi/15*rho_gw**2           # M_Pl = 1
H = math.sqrt(8*math.pi*rho_tot/3)
F_direct = Gam*4*T/(rho_gw*H)
print(f"[3] closed form vs direct at T=1e-3 M_Pl: {F_frac(x,gstar,T):.6e} vs {F_direct:.6e}")
# x at high T from DeltaN_eff=0.3: rho_GW/rho_gamma today 0.0691, scaled by (g_s/3.91)^(4/3), times rho_gamma/rho_tot = 2/g*
r0 = 7/8*(4/11)**(4/3)*0.3
x_hi = r0*(106.75/3.909)**(4/3)*2/106.75
print(f"    x = rho_GW/rho_tot at T > 100 GeV for DeltaN_eff=0.3: {x_hi:.4f}")
for label, T_GeV in (("BBN 1 MeV", 1e-3), ("EW 100 GeV", 1e2), ("max reheating 1.4e16 GeV (inflation bound)", 1.4e16),
                     ("1e18 GeV", 1e18), ("M_Pl", M_Pl_GeV)):
    print(f"    T = {label}: F per Hubble time = {F_frac(x_hi,106.75,T_GeV/M_Pl_GeV):.3e}")
# temperature at which F = 1 for x = x_hi and for a maximal x = 1
for xx in (x_hi, 1.0):
    Tstar = (1/(32*math.pi/15*xx*math.sqrt(math.pi*106.75/80)))**(1/3)
    print(f"    F = 1 needs T = {Tstar:.3f} M_Pl (x = {xx:.3f})")

# 4) required vs achievable for a mu-distortion at PIXIE sensitivity
#    The constraints check gives Drho/rho <= 4.3e-79 at DeltaN_eff=0.3 (r = 0.0681), scaling as r^2.
Drho_max = 4.29e-79
target_PIXIE = 3e-8/1.4      # Drho/rho ~ mu/1.4
target_FIRAS = 9e-5/1.4
for name, tgt in (("PIXIE", target_PIXIE), ("FIRAS", target_FIRAS)):
    fac = tgt/Drho_max
    print(f"[4] {name}: shortfall {fac:.2e}; required rho_GW/rho_gamma = {0.0681*math.sqrt(fac):.2e} vs allowed 0.0681")

# 5) collimated-beam corner: a beam of angular spread dth has rate ~ th^4 times the head-on scale.
#    How much angular spread converts an LVK-band 'collimated' background into the isotropic value?
#    isotropic <(1-cos)^2> / 4 (head-on) = (4/3)/4 = 1/3 ; small-angle beam <(1-cos)^2> ~ dth^4 / 4 * <...>
for dth in (1e-1, 1e-3):
    print(f"[5] beam spread {dth} rad: suppression vs isotropic ~ (dth^4/4)/(4/3) = {(dth**4/4)/(4/3):.2e}")
