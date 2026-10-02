"""Falsifier C5-2 (scale angle): Lentz soliton energy, compactness, densities and fields.

SI units unless marked geo (G = c = 1, lengths in m).
Inputs quoted from Lentz arXiv:2006.07125:
  Eq. (23): E_tot ~ C v_s^2 R^2 / w  (geo), C "of order unity"
  p.6/p.12: R = 100 m, w = 1 m -> E_tot ~ (few) x 1e-1 M_sun v_s  (printed linear in v_s; Eq. 23 is v_s^2)
  p.11: v_s = N^z(0,0)  (soliton speed = central shift)
  p.10: DEC shown only for N_i N^i < 1; horizons form at higher speed.
"""
import math

G = 6.67430e-11
c = 2.99792458e8
Msun = 1.98847e30
mu0 = 4e-7 * math.pi
eps0 = 8.8541878128e-12
kg_per_m_geo = c**2 / G  # kg per geometric metre of mass

R = 100.0   # m, payload/central radius
w = 1.0     # m, wall thickness
v = 10.0    # v_s in units of c

print("== 1. Lentz energy at R=100 m, w=1 m, v_s=10 ==")
for label, few in (("few=2", 0.2), ("few=5", 0.5)):
    for law, fac in (("v^2 (Eq.23, proceedings)", v**2), ("v (CQG printed)", v)):
        M = few * fac * Msun
        print(f"  {label}, {law}: E/c^2 = {M/Msun:.3g} M_sun = {M:.3e} kg = {M*c**2:.3e} J")

# Eq. 23 with C as a free form factor, geo
print("\n== 2. Eq.23 directly: E_geo = C v^2 R^2/w ==")
for C in (1.0,):
    Egeo = C * v**2 * R**2 / w
    print(f"  C={C}: E_geo = {Egeo:.3e} m -> {Egeo*kg_per_m_geo:.3e} kg = {Egeo*kg_per_m_geo/Msun:.3g} M_sun")
C_implied = 0.2 * Msun / (kg_per_m_geo * 1.0 * R**2 / w)  # at v=1, few=2
C_implied5 = 0.5 * Msun / (kg_per_m_geo * 1.0 * R**2 / w)
print(f"  form factor implied by Lentz's 'few x 0.1 M_sun' at v=1: C = {C_implied:.4f} - {C_implied5:.4f}")

print("\n== 3. Compactness 2GE/(c^4 R) if the claimed energy were positive and gravitated ==")
for M in (2 * Msun, 5 * Msun, 20 * Msun, 50 * Msun):
    Rs = 2 * G * M / c**2
    print(f"  M = {M/Msun:5.1f} M_sun: r_s = {Rs/1e3:8.2f} km; r_s/R = {Rs/R:8.1f}; Buchdahl 8/9 exceeded by x{(Rs/R)/(8/9):.0f}")
print("  Scaling law (geo): 2E/R = 2 C v^2 (R/w)")
for C in (C_implied, C_implied5, 1.0):
    comp = 2 * C * v**2 * R / w
    Rw_max = 1.0 / (2 * C * v**2)
    print(f"   C={C:.4f}: 2E/R at v=10 = {comp:.3g}; sub-horizon needs R/w < {Rw_max:.3g} (wall thicker than payload radius by x{1/Rw_max:.3g})")
for vv in (1.0, 1.5, 2.0):
    print(f"   C={C_implied:.4f}, v={vv}: 2E/R = {2*C_implied*vv**2*R/w:.3g}")

print("\n== 4. ADM mass of a flat-slice (h_ij = delta_ij) metric ==")
print("  M_ADM = (1/16pi) lim oint (d_j h_ij - d_i h_jj) dS^i = 0 exactly, since every d h = 0.")
print("  => total gravitating mass 0, while Lentz claims E_tot = 2-50 M_sun of positive density.")

print("\n== 5. Wall energy density and equivalent fields (20-50 M_sun case) ==")
Vwall = 4 * math.pi * R**2 * w
for M in (20 * Msun, 50 * Msun):
    u = M * c**2 / Vwall
    rho_m = M / Vwall
    B = math.sqrt(2 * mu0 * u)
    E = math.sqrt(2 * u / eps0)
    geo = 8 * math.pi * G * u / c**4
    lcurv = 1 / math.sqrt(geo)
    print(f"  M={M/Msun:.0f} M_sun: wall volume {Vwall:.3e} m^3; u = {u:.3e} J/m^3; rho = {rho_m:.3e} kg/m^3")
    print(f"     vs nuclear 2.3e17 kg/m^3: x{rho_m/2.3e17:.2e}")
    print(f"     B-equivalent = {B:.3e} T (magnetar 1e11 T: x{B/1e11:.1e}; Schwinger B_c 4.41e9 T: x{B/4.41e9:.1e}; lab 1.2e3 T: x{B/1.2e3:.1e})")
    print(f"     E-equivalent = {E:.3e} V/m (Schwinger 1.32e18 V/m: x{E/1.32e18:.1e})")
    print(f"     curvature length 1/sqrt(8 pi G u/c^4) = {lcurv:.3f} m (vs wall w = {w} m)")

print("\n== 6. Practice: energy gap ==")
NIF = 8.6e6
world_yr = 5.9e20
for M in (20 * Msun, 50 * Msun):
    Ej = M * c**2
    print(f"  {Ej:.3e} J: log10 over NIF 8.6 MJ = {math.log10(Ej/NIF):.2f}; over world-year 5.9e20 J = {math.log10(Ej/world_yr):.2f}")
