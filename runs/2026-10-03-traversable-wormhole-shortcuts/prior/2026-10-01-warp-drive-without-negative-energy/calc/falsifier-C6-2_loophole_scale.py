"""Falsifier C6-2 (scale): what each theorem loophole of C6 would take to realise.
Units: SI unless marked; geometric (G = c = 1) only in the symbolic identity.
"""
import sympy as sp

G = 6.67430e-11      # m^3 kg^-1 s^-2
c = 2.99792458e8     # m/s
hbar = 1.054571817e-34
Msun = 1.98847e30    # kg
AU = 1.495978707e11  # m
ly = 9.4607e15       # m
rho_nuc = 2.3e17     # kg/m^3, nuclear saturation density
l_P = (hbar * G / c**3) ** 0.5
rho_P = c**5 / (hbar * G**2)

print("=== (a) de Sitter branch: recession > c across a local vacuum-energy region ===")
H, d, Gs, cs = sp.symbols("H d G c", positive=True)
rho_v = 3 * H**2 / (8 * sp.pi * Gs)                   # vacuum mass density, kg/m^3
M_in = sp.Rational(4, 3) * sp.pi * d**3 * rho_v        # mass-energy inside radius d
C_in = sp.simplify(2 * Gs * M_in / (cs**2 * d))        # compactness of that region
print("compactness 2GM/(c^2 d) of de Sitter region of radius d:", C_in)
print("at the threshold H d = c this is:", sp.simplify(C_in.subs(H, cs / d)))
# observed Lambda
Lam = 1.1056e-52  # m^-2 (Planck 2018)
H_L = c * (Lam / 3) ** 0.5
print(f"observed Lambda: H_Lambda = {H_L:.3e} s^-1, recession reaches c at d = c/H = {c/H_L:.3e} m = {c/H_L/ly:.3e} ly")
for name, dist in [("10 m bubble", 10.0), ("1 AU", AU), ("1 ly", ly), ("4.37 ly", 4.37 * ly)]:
    Hreq = c / dist
    rho = 3 * Hreq**2 / (8 * 3.141592653589793 * G)
    M = 4 / 3 * 3.141592653589793 * dist**3 * rho
    print(f"{name:12s}: H_req = {Hreq:.3e} s^-1, rho_vac = {rho:.3e} kg/m^3 "
          f"({rho/rho_nuc:.3e} x nuclear), energy density = {rho*c**2:.3e} J/m^3, "
          f"M_inside = {M:.3e} kg = {M/Msun:.3e} Msun, R_s/d = {2*G*M/(c**2*dist):.3f}")
# for comparison: highest lab energy densities
I_laser = 1e27  # W/m^2 (= 1e23 W/cm^2, record class)
print(f"record laser intensity 1e23 W/cm^2 -> energy density {I_laser/c:.3e} J/m^3")
rho10 = 3 * (c / 10.0) ** 2 / (8 * 3.141592653589793 * G) * c**2
print(f"10 m de Sitter bubble needs {rho10/(I_laser/c):.3e} times that energy density")

print()
print("=== (b) distributional / thin-shell branch ===")
M_F = 4.49e27      # kg, Fuchs et al. 2024 shell mass
for R in (10.0, 15.0, 20.0):
    sigma = M_F / (4 * 3.141592653589793 * R**2)
    print(f"R = {R:4.0f} m: surface density sigma = {sigma:.3e} kg/m^2; "
          f"wall thickness at nuclear density = {sigma/rho_nuc:.3e} m; "
          f"at Planck density = {sigma/rho_P:.3e} m (l_P = {l_P:.3e} m)")
V = 4 / 3 * 3.141592653589793 * (20.0**3 - 10.0**3)
print(f"published 10 m-thick Fuchs wall: mean density = {M_F/V:.3e} kg/m^3 = {M_F/V/rho_nuc:.3e} x nuclear")
print("a delta-function wall has rho -> infinity; any wall of thickness >= l_P is smooth, so")
print("the smooth-metric hypotheses (no singularities, completeness) of Olum and Gao-Wald hold for it.")

print()
print("=== (c) generic-condition branch: matter on the path makes it generic ===")
rho, p, E = sp.symbols("rho p E", positive=True)  # geometric units; E = -u.k > 0
# perfect fluid, Einstein eq: R_ab = 8 pi (T_ab - T g_ab/2); for null k, g_ab k^a k^b = 0
Rkk = 8 * sp.pi * (rho + p) * E**2
print("R_ab k^a k^b for perfect fluid (geo):", Rkk, "> 0 whenever rho + p > 0")
print("so a fastest path must cross no matter with rho+p>0 anywhere; a payload cavity bounded by a matter wall")
print("forces any departure->cavity->destination path to cross the wall worldtube.")
# weak-field: how compact must a lab-scale source be to leave the linear (Visser-Bassett-Liberati) regime?
for Rsrc in (10.0, 100.0):
    for C_target in (1e-6, 0.1, 0.33):
        Mreq = C_target * Rsrc * c**2 / (2 * G)
        print(f"source radius {Rsrc:5.0f} m, compactness {C_target:g}: M = {Mreq:.3e} kg = {Mreq/Msun:.3e} Msun")
M_big = 1e12  # kg, a very large engineered structure (~ 1e9 t)
print(f"a 1e12 kg structure at 10 m has compactness {2*G*M_big/(c**2*10):.3e}: deep linear regime, where NEC => Shapiro delay")
# Shapiro delay of light passing the Fuchs mass at b = 20 m between points 1 AU away each side
b = 20.0
dt = 2 * G * M_F / c**3 * __import__("math").log(4 * AU * AU / b**2)
print(f"Shapiro delay (sign +) past the Fuchs mass, b = 20 m, r1 = r2 = 1 AU: {dt:.3e} s")
