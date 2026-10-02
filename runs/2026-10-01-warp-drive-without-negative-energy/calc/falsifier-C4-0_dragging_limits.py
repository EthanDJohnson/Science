"""Falsifier C4-0: limits on 'no felt g-force' translational dragging.

SI units unless stated; geometric (G=c=1) for M/R ratios.
1. Weak-field coefficient: lens uses kappa = 4GM/(c^2 R); Lynden-Bell, Bicak & Katz 1999
   (gr-qc/9812033 p.7) give f = 11/3 (de Donder gauge, retardation included).
2. Thin static Schwarzschild shell: DEC (|p| <= sigma) fails for R < 25M/12 (Zel'dovich limit,
   quoted by Arnfinnsson & Gron 2014, arXiv:1408.4588 p.13). Compactness C=2M/R there, interior lapse.
3. Rotational analogue (Brill-Cohen 1966): omega/Omega = 4a(2-a)/((1+a)(3-a)), a = M/(2 r_iso),
   areal R = r_iso (1+a)^2. Analogue only: shows dragging fraction < 1 until horizon (a=1).
4. Newtonian 'gravity tractor': payload in free fall towards a compact mass M at distance d that is
   pushed at acceleration A = GM/d^2. Felt acceleration = tidal only, 2 A L / d (payload length L).
   Compare mass needed vs. a shell that leaves residual felt acceleration (1-kappa) A.
"""
import math
from scipy.optimize import brentq

G = 6.67430e-11; c = 2.99792458e8; g0 = 9.80665
M_pub = 4.49e27  # kg, Fuchs et al. 2024 published mass

print("1. weak-field linear coefficient")
for R in (10.0, 20.0):
    m_geo = G * M_pub / c**2
    print(f"   R={R:5.1f} m: GM/c^2R={m_geo/R:.4f}; kappa(4M/R)={4*m_geo/R:.4f}; kappa(11M/3R, LBK 1999)={11*m_geo/(3*R):.4f}")

print("2. DEC (Zel'dovich) limit of a static thin Schwarzschild shell, R = 25M/12")
C_dec = 2.0 / (25.0 / 12.0)
print(f"   C_DEC = 2M/R = {C_dec:.4f}; interior lapse N=sqrt(1-C) = {math.sqrt(1-C_dec):.4f}; g00 ratio = {1-C_dec:.4f}")
print(f"   Buchdahl C=8/9={8/9:.4f}: lapse {math.sqrt(1-8/9):.4f}")

print("3. Brill-Cohen rotational dragging fraction (analogue) vs compactness")
def bc(a):
    return 4*a*(2-a)/((1+a)*(3-a))
def a_of_C(C):
    return brentq(lambda a: 4*a/(1+a)**2 - C, 1e-12, 1.0)
for C in (0.01, 0.335, 0.67, 8/9, C_dec, 0.99, 0.999):
    a = a_of_C(C)
    print(f"   C={C:.4f}: a=M/2r_iso={a:.4f}; drag fraction={bc(a):.4f}; weak-field 4M/3R={2*C/3:.4f}; residual 1-f={1-bc(a):.4f}")
print(f"   at horizon a=1: fraction {bc(1.0):.4f}")

print("4. gravity-tractor vs shell for 'no felt g' towing")
for A_g, L, resid_g in ((10.0, 10.0, 0.1), (100.0, 10.0, 1.0), (1.0, 10.0, 0.01)):
    A = A_g * g0
    d = 2 * L * A / (resid_g * g0)   # tidal 2AL/d = resid
    M_tr = A * d**2 / G
    kappa_need = 1 - resid_g / A_g
    # shell of interior radius >= L, area radius R = L; compactness needed at least kappa (BC analogue lower bound on C)
    C_need = brentq(lambda C: bc(a_of_C(C)) - kappa_need, 1e-9, 0.999999999)
    M_sh = C_need * c**2 * L / (2 * G)
    print(f"   A={A_g:g} g, L={L:g} m, felt<= {resid_g:g} g: tractor d={d:.3e} m, M={M_tr:.3e} kg; "
          f"shell kappa>={kappa_need:.4f} needs C~{C_need:.4f} (BC analogue) -> M~{M_sh:.3e} kg; ratio shell/tractor={M_sh/M_tr:.2e}")
    print(f"      shell C exceeds DEC limit 0.96? {C_need > C_dec}")
print("5. payload felt fraction for the run's shell (BC analogue, C=0.335 at R2): ", f"{1-bc(a_of_C(0.335)):.4f}")
