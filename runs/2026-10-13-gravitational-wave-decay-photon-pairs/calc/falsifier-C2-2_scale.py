"""Falsifier C2, refuter 2 (scale angle).

Scale attack on C2 ("an outgoing GW's photon-pair production converges within a few
wavelengths of its source; no lifetime, no path depletion, nothing observable").

Units: SI throughout unless stated. Kinetic cross sections from the slate
(sigma(RL->gg) = (4 pi/5) G_nat^2 s, sigma(RR) = 0, natural units; C6 / M-MECHANIST-01),
converted with G_nat = hbar G / c^3.

Parts
 A. Worst-case (head-on, max-helicity, pattern-peak) upper bound on pairs made beyond R by
    a single outgoing shell: needs NO wave-optics or toy assumption, only energy density
    falling as 1/r^2 and the local kinetic rate <= its head-on maximum.
 B. Ray-geometry bound: gravitons at r come from an emitting region of radius a, so their
    mutual angle is <= 2a/r; gives the R^-5 tail.
 C. Required vs achievable: fractional energy loss beyond R vs standard-siren 1e-2.
 D. Residual "lifetime" of a wave from cross-fusion with the ambient isotropic GW background
    (multi-directional; outside C2's self-decay scope but in vacuum).
 E. Lensing multi-image overlap for a burst: time delay vs duration; wave-optics parameter.
 F. Dimensional estimate (k = 1, labelled): conversion on the static field of compact objects
    passed within lambda/2pi along the path.
"""
import sympy as sp
import math

G = 6.67430e-11; c = 2.99792458e8; hbar = 1.054571817e-34; Msun = 1.98892e30
AU = 1.495978707e11; pc = 3.0856775814913673e16; Mpc = 1e6 * pc
kB = 1.380649e-23

# ---------- symbolic derivation of the worst-case bound ----------
r, R, E, T, K, Gs, cs = sp.symbols('r R E T K G c', positive=True)
rho = E / (4 * sp.pi * r**2 * cs * T)               # shell energy density, J/m^3
rate_V = K * Gs**2 * rho**2 / cs**7                 # pairs m^-3 s^-1, hbar-free kinetic form
dP_dr = rate_V * 4 * sp.pi * r**2 * cs * T / cs     # shell volume x dt = dr/c
P_beyond = sp.simplify(sp.integrate(dP_dr, (r, R, sp.oo)))
print("A. symbolic P(>R) =", P_beyond)
# head-on max of n1 n2 sigma(1-cos) c with rho1+rho2 = rho: (8 pi/5) G^2 rho^2/c^7
K_headon = sp.Rational(8, 5) * sp.pi
K_bound = K_headon * sp.Rational(5, 2)              # x pattern peak/mean 2.5 (face-on quadrupole)
print("   K_headon = 8pi/5 =", float(K_headon), "; K_bound (x2.5 pattern) =", float(K_bound),
      "= 4 pi ?", sp.simplify(K_bound - 4 * sp.pi) == 0)
P_bound_expr = sp.simplify(P_beyond.subs(K, K_bound))
print("   P(>R) <= ", P_bound_expr, "  [ (G E/c^4)^2 / (c T R) ]")

# cross-check the head-on coefficient against M-MECHANIST-03's closed form
w, h = sp.symbols('omega h', positive=True)
rho_lin = cs**2 * w**2 * h**2 / (32 * sp.pi * Gs)    # one linearly polarised beam, energy density
# two beams each rho_lin head-on, linear pols: M-MECHANIST-03 Gamma = w^4 h^4 (1-cos)^2/(1280 pi c^3)
mech = w**4 * h**4 * 4 / (1280 * sp.pi * cs**3)
# kinetic with sigma_lin = (2 pi/5) G_nat^2 s (azimuth-averaged, linear): (4 pi/5) G^2 rho1 rho2 (1-cos)^2/c^7
mine = sp.Rational(4, 5) * sp.pi * Gs**2 * rho_lin**2 * 4 / cs**7
print("   cross-check vs M-MECHANIST-03 (head-on, linear): ratio =", sp.simplify(mine / mech))

# ---------- numbers: GW150914 (B&O inputs) ----------
f = 150.0; omega = 2 * math.pi * f; sigma_w = 200.0; Tdur = 1 / sigma_w
lam = c / f; lbar = c / omega
for Emsun in (2.0, 3.0):
    Ej = Emsun * Msun * c**2
    L1 = G * Ej / c**4
    print(f"\nGW150914, E = {Emsun} Msun c^2 = {Ej:.3e} J; GE/c^4 = {L1:.3e} m; cT = {c*Tdur:.3e} m;"
          f" lambda = {lam:.3e} m; c/omega = {lbar:.3e} m")
    a = 2 * lbar   # emitting-region radius assumed <= 2 c/omega (merger: ~3.3 GM/c^2 = c/omega)
    for name, Rv in [("c/omega", lbar), ("lambda", lam), ("10 lambda", 10 * lam), ("1 AU", AU),
                     ("1 pc", pc), ("410 Mpc", 410 * Mpc)]:
        Pb = L1**2 / (c * Tdur * Rv)                      # Part A worst case
        Pg = L1**2 / (c * Tdur) * a**4 / (5 * Rv**5) if Rv >= a else float('nan')   # Part B
        frac = 2 * hbar * omega * Pb / Ej                 # Part C energy fraction (unstimulated)
        frac_st = frac * 7.57e8                           # with CMB 1+2f at 150 Hz (upper)
        print(f"  R = {name:9s} {Rv:.3e} m: A worst-case P(>R) <= {Pb:.2e} pairs;"
              f" B ray-geometry (a = 2c/w) <= {Pg:.2e}; C energy fraction <= {frac:.1e}"
              f" (x(1+2f): {frac_st:.1e})")

# Part C: required vs achievable
Ej = 2 * Msun * c**2
frac_410 = 2 * hbar * omega * (G * Ej / c**4)**2 / (c * Tdur * lam) / Ej * 7.57e8
print(f"\nC. worst-case fraction of GW energy lost beyond lambda (stimulated, any distance): {frac_410:.1e};"
      f" standard-siren sensitivity ~1e-2 -> shortfall {1e-2/frac_410:.1e}")

# ---------- Part D: cross-fusion with ambient isotropic background ----------
# per wave graviton: Gamma = n_bg <sigma(1-cos)> c, helicity average 1/2, s = 2 w w'(1-cos),
# <(1-cos)^2>_iso = 4/3  ->  Gamma = (16 pi/15) hbar G^2 w rho_bg / c^7
Tcmb = 2.7255
a_rad = 4 * 5.670374419e-8 / c
rho_gam = a_rad * Tcmb**4
fnu = 7 / 8 * (4 / 11)**(4 / 3)
th = sp.symbols('theta')
avg = sp.integrate((1 - sp.cos(th))**2 * sp.sin(th) / 2, (th, 0, sp.pi))
print(f"\nD. <(1-cos)^2>_iso = {avg}; rho_gamma = {rho_gam:.3e} J/m^3")
tH = 4.35e17
for lab, rbg in [("DeltaNeff=0.3", 0.3 * fnu * rho_gam), ("LVK Omega~1.7e-8 (h^2-free, indicative)", 1.7e-8 * 7.8e-10)]:
    Gam = 16 * math.pi / 15 * hbar * G**2 * omega * rbg / c**7
    print(f"  {lab}: rho_bg = {rbg:.2e} J/m^3, Gamma = {Gam:.2e} s^-1, lifetime = {1/Gam:.2e} s"
          f" ({1/Gam/tH:.1e} t_H); x(1+2f)=7.57e8 -> lifetime {1/(Gam*7.57e8):.1e} s;"
          f" loss over t_H (stim) = {Gam*7.57e8*tH:.1e}")

# ---------- Part E: lensing overlap ----------
for M in (1.0, 1e11):
    dt = 4 * G * M * Msun / c**3
    print(f"\nE. lens M = {M:.0e} Msun: 4GM/c^3 = {dt:.2e} s vs burst T = {Tdur:.1e} s; w*4GM/c^3 = {omega*dt:.2e}")

theta_E = 1e-5   # rad, generous galaxy-lens image separation (~2 arcsec)
print(f"E. continuous source, two overlapping lensed images at theta <= {theta_E:.0e} rad:"
      f" (1-cos)^2 / head-on 4 = {(1-math.cos(theta_E))**2/4:.1e} of the head-on rate")

# ---------- Part F: static field of compact objects along the path (dimensional, k = 1) ----------
EP = math.sqrt(hbar * c**5 / G)
N_hw = Ej * hbar * omega / EP**2               # N (hbar w / E_P)^2
rs = 2 * G * Msun / c**2
Omega_star = 3e-3; rho_c = 8.5e-27
n_co = Omega_star * rho_c / Msun
tau = n_co * math.pi * lbar**2 * 410 * Mpc
print(f"\nF. N(hbar w/E_P)^2 = {N_hw:.2e}; (r_s w/c)^2 (1 Msun) = {(rs*omega/c)**2:.2e};"
      f" n_compact <= {n_co:.2e} m^-3; optical depth within c/w over 410 Mpc = {tau:.2e};"
      f" pairs ~ {N_hw*(rs*omega/c)**2*tau:.1e} (k = 1, dimensional)")
