#!/usr/bin/env python3
"""Idealizer lens: the scaling laws applied to the brief's reference sources (SI units throughout).

Laws (derived and checked in lens-idealizer_coeff.py, lens-idealizer_outgoing.py):
  (a) B&O in-state total, real-sign isotropic top hat:  P = (4/25) G^2 E^2 w sigma / c^10          [pairs]
      profile-free form:                                P = (12 pi/25) G^2 w int L(t)^2 dt / c^10  [pairs]
      B&O 'rate' (eq. 8):                               dP/dt = (3/(25 pi)) G^2 E^2 w sigma^2 / c^10
  (b) physical-pattern factor (tool gw_coherent_fusion table, top hat): circular binary 0.562, linear quadrupole
      0.3125, pure circular 0 (exact).
  (c) outgoing wave, yield beyond radius r: R(kr) ~ 0.07 (kr)^-3 x P_B&O (scalar toy, kinetic proxy).
  (d) isotropic incoherent background: Gamma = (8 pi/15) G^2 rho^2 / c^7  [pairs m^-3 s^-1], hbar-free.
  (e) CMB final-state stimulation (if it applied): x (1 + 2 f_gamma), f_gamma = 1/(exp(hbar w/kT) - 1).
"""
import math

G = 6.67430e-11
c = 2.99792458e8
hbar = 1.054571817e-34
kB = 1.380649e-23
Msun = 1.98892e30
eV = 1.602176634e-19
T_CMB = 2.7255
Mpc = 3.0857e22
AU = 1.495978707e11
yr = 3.15576e7


def P_tophat(E, w, sig):
    return 4 / 25 * G**2 * E**2 * w * sig / c**10


def rate_BO(E, w, sig):
    return 3 / (25 * math.pi) * G**2 * E**2 * w * sig**2 / c**10


def fgam(w):
    return 1 / math.expm1(hbar * w / (kB * T_CMB))


print("=== GW150914-like merger, B&O inputs (f = 150 Hz, sigma_w = 200 s^-1) ===")
w = 2 * math.pi * 150.0
sig = 200.0
for Em in (2.0, 3.0):
    E = Em * Msun * c**2
    P = P_tophat(E, w, sig)
    print(f"E = {Em} Msun c^2 = {E:.3e} J: B&O in-state total P = {P:.3e} pairs; B&O rate = {rate_BO(E, w, sig):.3e} "
          f"pairs/s; T_eff = 4pi/(3 sigma) = {4*math.pi/(3*sig)*1e3:.2f} ms")
    print(f"   x circular-binary factor 0.562 -> {0.562*P:.3e} pairs; energy in photons = "
          f"{0.562*P*2*hbar*w:.3e} J; fraction of E_GW = {0.562*P*2*hbar*w/E:.3e}")
    f = fgam(w)
    print(f"   CMB stimulation 1+2f = {1+2*f:.3e} (hbar w = {hbar*w/eV:.3e} eV) -> {0.562*P*(1+2*f):.3e} pairs "
          f"(energy {0.562*P*(1+2*f)*2*hbar*w:.3e} J)")
# profile-free version with the peak luminosity held for a nominal 5 ms
Lp = 3.6e49
for tdur in (5e-3, 10e-3):
    Pl = 12 * math.pi / 25 * G**2 * w * Lp**2 * tdur / c**10
    print(f"profile-free: L = {Lp:.2e} W held {tdur*1e3:.0f} ms -> P = {Pl:.3e} pairs (in-state ideal)")
lam = c / 150.0
print(f"reduced wavelength c/w = {c/w/1e3:.1f} km; GM/c^2 (65 Msun) = {G*65*Msun/c**2/1e3:.1f} km -> "
      f"the B&O production region r ~ 1/w is {c/w/(G*65*Msun/c**2):.2f} GM/c^2: the merger itself")
P = P_tophat(2 * Msun * c**2, w, sig)
for name, r in (("r = lambda", lam), ("r = 10 lambda", 10 * lam), ("r = 1 AU", AU), ("r = 410 Mpc", 410 * Mpc)):
    x = w * r / c
    print(f"outgoing wave, yield beyond {name:12s} (kr = {x:.3g}): {0.07*x**-3:.3e} x P = {0.07*x**-3*P:.3e} pairs")

print("\n=== Inspirals: profile-free in-state ideal P = (12 pi/25) G^2/c^10 int w L^2 dt (quadrupole chirp) ===")


def inspiral_P(Mc, f_lo, f_hi, n=4000):
    """int w L^2 dt = int w L dE over the chirp, E_orb = -(1/2)(G Mc Omega)^{2/3} Mc, w = 2 Omega."""
    tot = 0.0
    O_lo, O_hi = math.pi * f_lo, math.pi * f_hi
    for i in range(n):
        O = O_lo * (O_hi / O_lo)**((i + 0.5) / n)
        dO = O * math.log(O_hi / O_lo) / n
        L = 32 / 5 * c**5 / G * (G * Mc * O / c**3)**(10 / 3)
        dE = (1 / 3) * (G * Mc)**(2 / 3) * Mc * O**(-1 / 3) * dO
        tot += 2 * O * L * dE
    return 12 * math.pi / 25 * G**2 / c**10 * tot


for name, Mc, flo, fhi in (("GW170817 (Mc = 1.188 Msun), 30 Hz - 1.6 kHz", 1.188, 30, 1600),
                           ("GW150914 inspiral (Mc = 28 Msun), 35 - 68 Hz", 28.0, 35, 68),
                           ("Galactic WD binary (Mc = 0.3 Msun) at 6.2 mHz, per year", 0.3, None, None)):
    if flo is not None:
        print(f"{name}: P = {inspiral_P(Mc*Msun, flo, fhi):.3e} pairs (whole chirp; dominated by the top frequency)")
    else:
        O = math.pi * 6.2e-3
        L = 32 / 5 * c**5 / G * (G * Mc * Msun * O / c**3)**(10 / 3)
        Pyr = 12 * math.pi / 25 * G**2 * 2 * O * L**2 * yr / c**10
        print(f"{name}: L_GW = {L:.3e} W, P = {Pyr:.3e} pairs per year")

print("\n=== Stochastic background: Gamma = (8 pi/15) G^2 rho^2 / c^7 ===")
H0 = 67.4e3 / Mpc
rho_c = 3 * H0**2 * c**2 / (8 * math.pi * G)
for name, rho in (("DeltaN_eff = 0.3 bound (rho = 2.8e-15 J/m^3)", 2.8e-15),
                  ("LVK Omega_GW = 2.8e-9 (25 Hz, flat; as total)", 2.8e-9 * rho_c)):
    Gam = 8 * math.pi / 15 * G**2 * rho**2 / c**7
    w25 = 2 * math.pi * 25
    frac = Gam * 2 * hbar * w25 / H0 / rho
    print(f"{name}: Gamma = {Gam:.3e} pairs m^-3 s^-1; GW energy fraction lost per Hubble time at 25 Hz = {frac:.3e}")
print(f"rho_crit c^2 = {rho_c:.3e} J/m^3")
