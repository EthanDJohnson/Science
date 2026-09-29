"""Falsifier C1-0: recheck C1's load-bearing numbers and test whether the
free-field QI is the binding in-principle constraint once interacting fields
(which the QI does not govern; Olum & Graham 2003) are admitted.

Units: SI unless marked (geometric, G = c = 1, lengths in m).
"""
import math

G = 6.67430e-11        # m^3 kg^-1 s^-2
c = 2.99792458e8       # m/s
hbar = 1.054571817e-34 # J s
Msun = 1.989e30        # kg
LP = math.sqrt(hbar * G / c**3)  # m
m_per_kg = G / c**2    # geometric length per kg
eV = 1.602176634e-19   # J

print(f"L_P = {LP:.4e} m; 1 m (geometric) = {1/m_per_kg:.4e} kg")

# --- 1. QI-limited Alcubierre wall at reference case (tanh, PF convention)
v, R = 10.0, 100.0
Delta_QI = 97.7 * v * LP
E_geo = v**2 * R**2 / (18 * Delta_QI)       # m (geometric)
E_kg = E_geo / m_per_kg
print(f"Delta_QI = {Delta_QI:.3e} m; |E| = {E_kg:.3e} kg = {E_kg/Msun:.3e} Msun")

# Hubble-radius mass (Planck 2018 H0 = 67.4 km/s/Mpc)
H0 = 67.4e3 / 3.0857e22
rho_c = 3 * H0**2 / (8 * math.pi * G)
RH = c / H0
M_H = rho_c * 4 / 3 * math.pi * RH**3
print(f"Hubble-radius mass = {M_H:.3e} kg; ratio = {E_kg/M_H:.2e}")

# --- 2. Thick-wall GR floor (no QI) vs demonstrated supply
E_floor_geo = v**2 * R / 12
E_floor_kg = E_floor_geo / m_per_kg
E_floor_J = E_floor_kg * c**2
world_J = 5.92e20
bressi_J = 5.0e-15
print(f"Floor -v^2 R/12 = {E_floor_kg:.3e} kg = {E_floor_J:.3e} J; "
      f"log10(/world-yr) = {math.log10(E_floor_J/world_J):.1f}; "
      f"log10(/Bressi) = {math.log10(E_floor_J/bressi_J):.1f}")

# --- 3. Peak wall density at Delta = 1 m, v = 10c (value quoted in C5): 1.2e44 J/m^3
rho_need = 1.2e44  # J/m^3
# Interacting field of mass scale M: static negative density ~ -eps (Mc^2)^4/(hbar c)^3
hc = hbar * c
print("Mass scale needed for |rho| = 1.2e44 J/m^3 from a static interacting-field")
print("negative density -eps (Mc^2)^4/(hbar c)^3 (Olum-Graham-type, eps assumed):")
for eps in (1e-1, 1e-3, 1e-5):
    Mc2 = (rho_need * hc**3 / eps) ** 0.25
    lam = hc / Mc2  # reduced Compton length, m
    print(f"  eps={eps:.0e}: Mc^2 = {Mc2/eV/1e9:.3g} GeV; Compton length = {lam:.2e} m; "
          f"layers per 1 m wall ~ {1/lam:.1e}")

# Compare with the free-field Ford-Roman bound on the same density for a 1 m wall
# sampled over tau0 ~ Delta/(v c) (lens convention): rho >= -3 hbar/(32 pi^2 c^3 tau0^4) (SI form)
tau0 = 1.0 / (v * c)
rho_FR = 3 * hbar / (32 * math.pi**2 * c**3 * tau0**4)  # kg/m^3 ... times c^2 for J/m^3
rho_FR_J = rho_FR * c**2
print(f"Free-field FR bound at tau0 = {tau0:.2e} s: |rho| <= {rho_FR_J:.2e} J/m^3; "
      f"demand/allowed = 10^{math.log10(rho_need/rho_FR_J):.1f}")

# --- 4. RSET e-fold rough check for D = 1 km at 10c
D = 1000.0
kappa_geo = v * 1.0 / D     # ~ v max|f'| with |f'| ~ 1/D  (m^-1, geometric)
T_cruise = 4.37 / 10 * 3.156e7  # s
efolds = kappa_geo * c * T_cruise
print(f"RSET e-folds (D=1 km, kappa ~ v/D): {efolds:.2e} per {T_cruise:.2e} s cruise")
