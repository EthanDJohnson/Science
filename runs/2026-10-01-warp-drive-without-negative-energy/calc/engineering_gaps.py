"""Engineering facet: orders-of-magnitude gaps between warp-drive requirements and demonstrated capability.
SI units throughout. Inputs from sources quoted in research/engineering.md; shell parameters
(R1=10 m, R2=20 m, M=4.49e27 kg, v=0.04c) are UNVERIFIED leads from an earlier run, used only as
an illustration and replaced by the quantitative facet's verified values when available.
"""
import math

c = 299792458.0
G = 6.67430e-11
Mjup = 1.898e27
Msun = 1.989e30
yr = 3.15576e7

# Demonstrated capability
E_world_yr = 592.2e18          # J, EI Statistical Review 2025: 592.2 EJ primary energy 2024
v_psp = 692000e3 / 3600        # m/s, Parker Solar Probe 692,000 km/h
E_NIF_out = 8.6e6              # J fusion yield, 7 Apr 2025
E_NIF_in = 2.08e6              # J laser
sigma_nanodiamond = 460e9      # Pa yield strength (Dubrovinskaia 2016)
sigma_graphene = 130e9         # Pa intrinsic strength
P_static = 1.0e12              # Pa, static pressure beyond 1 TPa
rho_nuc = 2.3e17               # kg/m^3 nuclear saturation density (textbook value)
M_ISS = 4.2e5                  # kg (approx; NOT sourced here)

print("== Capability conversions (SI) ==")
print(f"world primary energy 2024 = {E_world_yr:.3e} J = {E_world_yr/c**2:.3e} kg of mass-energy = {E_world_yr/c**2/1e3:.2f} tonnes")
print(f"PSP speed = {v_psp/1e3:.1f} km/s = {v_psp/c:.3e} c")
print(f"NIF gain = {E_NIF_out/E_NIF_in:.2f}; yield in kg-equivalent = {E_NIF_out/c**2:.3e} kg")

# Shell illustration (UNVERIFIED lead values)
R1, R2, M, v = 10.0, 20.0, 4.49e27, 0.04 * c
V = 4 / 3 * math.pi * (R2**3 - R1**3)
rho = M / V
E_rest = M * c**2
print("\n== Illustrative 2024-shell scale (lead values, unverified) ==")
print(f"M = {M:.3e} kg = {M/Mjup:.3f} M_J = {M/Msun:.3e} M_sun")
print(f"mean density = {rho:.3e} kg/m^3 = {rho/rho_nuc:.3e} x nuclear density")
print(f"rest energy M c^2 = {E_rest:.3e} J = {E_rest/E_world_yr:.3e} world-years of primary energy")
print(f"compactness 2GM/(R2 c^2) = {2*G*M/(R2*c**2):.3e}   (G*M/c^2 = {G*M/c**2:.3e} m)")
print(f"kinetic energy 0.5 M v^2 at 0.04c (Newtonian) = {0.5*M*v**2:.3e} J = {0.5*M*v**2/E_world_yr:.3e} world-years")
p_scale = rho * c**2
print(f"rest-mass-energy density scale rho c^2 = {p_scale:.3e} Pa")
print(f"gap to nanodiamond yield strength: {math.log10(p_scale/sigma_nanodiamond):.1f} orders; to 1 TPa static: {math.log10(p_scale/P_static):.1f} orders")
print(f"mass gap vs ISS (~4.2e5 kg): {math.log10(M/M_ISS):.1f} orders")

# Experiment gaps
print("\n== Experiment gaps (ratios) ==")
print(f"GP-B frame dragging: 1-sigma/value = {7.2/37.2:.3f}; LARES2 claimed 0.2%: factor {7.2/37.2/0.002:.0f} better")
print(f"LARES+LAGEOS 2019 total systematic 2%..4% vs 0.2% target: factor {0.02/0.002:.0f}-{0.04/0.002:.0f}")
print("Archimedes target force 5e-16 N (3 mm thick, r=0.15 m samples); torque ASD 7e-13 N/sqrt(Hz) over 4e6 s")

# Glenn 2025 spark-gap claim: order-of-magnitude expected metric perturbation (OUR estimate, Newtonian-order)
print("\n== Spark-gap plasma (Glenn 2025) order-of-magnitude gap ==")
rho_E = 1.0e9          # J/m^3, energy density quoted as threshold for the reported effect
L_src = 1.0e-3         # m, assumed ~1 mm spark size (assumption, not sourced)
L_path = 0.725         # m, stated optical path length
h = 8 * math.pi * G / c**4 * rho_E * L_src**2
dpath = h * L_path
claimed = 150e-9       # m, ~140-160 nm fringe displacement reported
print(f"h ~ 8 pi G rho_E L^2 / c^4 = {h:.2e} (dimensionless); path change ~ {dpath:.2e} m; claimed ~ {claimed:.1e} m; gap = {math.log10(claimed/dpath):.1f} orders")
