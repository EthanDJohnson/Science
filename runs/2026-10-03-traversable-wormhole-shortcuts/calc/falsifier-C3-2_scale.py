"""Falsifier C3-2 (scale): how big can a self-consistent, free-field-supported
achronal-ANEC-violating throat be, and what would a violation have to supply?

All SI unless marked. Geometric = G = c = 1.
"""
import math

G = 6.67430e-11       # m^3 kg^-1 s^-2
c = 2.99792458e8      # m/s
hbar = 1.054571817e-34  # J s
lP = math.sqrt(hbar * G / c**3)   # m
mP = math.sqrt(hbar * c / G)      # kg
EP = mP * c**2                    # J
print(f"l_P = {lP:.4e} m, m_P = {mP:.4e} kg, E_P = {EP:.4e} J")

# ---------------------------------------------------------------
# 1. Required ANEC deficit on the radial throat geodesic (Ellis throat radius a)
#    Geometric: G_kk = -2 a^2/(l^2+a^2)^2 for k = d_t + d_l, so
#    int G_kk dl = -pi/a  ->  int T_kk dlambda = -1/(8a)  (k^t = 1).
#    Check by numeric quadrature, then SI: -c^4/(8 G a)  [J/m^2].
# ---------------------------------------------------------------
def anec_geom_numeric(a, n=200000, Lmax_factor=2000.0):
    Lmax = Lmax_factor * a
    h = 2 * Lmax / n
    s = 0.0
    for i in range(n + 1):
        l = -Lmax + i * h
        w = 0.5 if i in (0, n) else 1.0
        s += w * (-2 * a**2 / (l**2 + a**2) ** 2)
    s *= h
    return s / (8 * math.pi)

a_test = 1.0
num = anec_geom_numeric(a_test)
print("\n=== 1. Required ANEC (Ellis) ===")
print(f"numeric int T_kk dlambda (geometric, a=1 m) = {num:.6f} 1/m ; analytic -1/(8a) = {-1/8:.6f} 1/m")
for a in (1.0, 1.0e3, 1.5e7):
    req = c**4 / (8 * G * a)
    print(f"a = {a:.3e} m: required |ANEC| = c^4/(8 G a) = {req:.4e} J/m^2")

# ---------------------------------------------------------------
# 2. What one free field can supply at the single scale a (flat-space QI,
#    sampling time tau0 = f a / c, valid only for tau0 << curvature radius).
#    Ford-Roman Lorentzian QI: rho_bar >= -3 hbar c/(32 pi^2 (c tau0)^4).
#    Required throat density |rho| = c^4/(8 pi G a^2) (Ellis, at throat).
#    N_min = |rho_req| / |rho_QI| ; reproduces the run's 4.19e-8 (a/l_P)^2.
# ---------------------------------------------------------------
print("\n=== 2. Species needed to saturate the QI at single scale a ===")
def Nmin(a, f):
    rho_req = c**4 / (8 * math.pi * G * a**2)
    rho_qi = 3 * hbar * c / (32 * math.pi**2 * (f * a) ** 4)
    return rho_req / rho_qi
for f in (0.01, 0.1):
    coeff = Nmin(lP, f)  # N_min / (a/l_P)^2
    print(f"f = {f}: N_min = {coeff:.4e} (a/l_P)^2")
    for a in (1e-30, 1e-18, 1.0, 1.5e7):
        print(f"   a = {a:.1e} m: N_min = {Nmin(a, f):.3e}")

# ---------------------------------------------------------------
# 3. Combine with the species bound (Dvali): with N species the gravity
#    cutoff length is l_* = sqrt(N) l_P; semiclassical control needs a >> l_*.
#    QI saturation gives a <= sqrt(N/coeff) l_P = l_* / sqrt(coeff).
#    So a / l_* <= 1/sqrt(coeff), independent of N.
# ---------------------------------------------------------------
print("\n=== 3. Throat size in units of the species cutoff length sqrt(N) l_P ===")
for f in (0.01, 0.1):
    coeff = Nmin(lP, f)
    ratio = 1 / math.sqrt(coeff)
    print(f"f = {f}: a_max / (sqrt(N) l_P) = {ratio:.4e}; curvature (l_*/a)^2 >= {coeff:.3e}")
for N in (1, 100, 1e32):
    for f in (0.01, 0.1):
        coeff = Nmin(lP, f)
        amax = math.sqrt(N / coeff) * lP
        print(f"   N = {N:.0e}, f = {f}: a_max = {amax:.3e} m")

# ---------------------------------------------------------------
# 4. Few-quantum (Urban-Olum-type, vacuum + 2-particle admixture) state
#    back-reacting O(1) curvature over length L needs energy ~ c^4 L/G inside L.
#    If carried by O(1) quanta, each has reduced wavelength hbar c / E = l_P^2/L.
# ---------------------------------------------------------------
print("\n=== 4. Energy to self-source O(1) curvature at scale L, and quantum wavelength ===")
for L in (1e-30, 1e-15, 1.0, 1.5e7):
    E = c**4 * L / G
    lam = hbar * c / E
    print(f"L = {L:.1e} m: E ~ c^4 L/G = {E:.3e} J ({E/c**2:.3e} kg); "
          f"single-quantum reduced wavelength = {lam:.3e} m = {lam/lP:.3e} l_P; "
          f"quanta of wavelength L needed = {(L/lP)**2:.3e}")

# ---------------------------------------------------------------
# 5. Payload ceiling for the single-scale free-field throat: positive
#    payload energy must stay below the throat mass scale a c^2/(2G)
#    (order of magnitude; Q-28 reading). With a_max(N, f):
# ---------------------------------------------------------------
print("\n=== 5. Payload ceiling m < a_max c^2/(2G) ===")
for f in (0.01, 0.1):
    coeff = Nmin(lP, f)
    k = (1 / math.sqrt(coeff)) * lP * c**2 / (2 * G)   # kg per sqrt(N)
    print(f"f = {f}: m_max = {k:.3e} sqrt(N) kg")
    for N in (100, 1e32):
        print(f"   N = {N:.0e}: m_max = {k*math.sqrt(N):.3e} kg")
    for m in (1.0, 70.0):
        print(f"   N needed for m = {m} kg: {(m/k)**2:.3e}")
# single quantum through a 7.9e-31 m throat
a1 = math.sqrt(100 / Nmin(lP, 0.01)) * lP
Eq = hbar * c / a1
print(f"N=100, f=0.01 throat a = {a1:.3e} m: one quantum with wavelength a carries {Eq:.3e} J "
      f"= {Eq/EP:.3e} E_P; throat mass-energy scale a c^4/(2G) = {a1*c**4/(2*G):.3e} J; ratio = {Eq/(a1*c**4/(2*G)):.3e}")

# ---------------------------------------------------------------
# 6. Ford-Roman thin-band escape for a = 1 m (run values recomputed):
#    band width w <= (3 a/(4 pi f^4 l_P))^(1/3) l_P, density c^4/(8 pi G a w).
# ---------------------------------------------------------------
print("\n=== 6. Thin band for a = 1 m, f = 0.01 ===")
a = 1.0; f = 0.01
w = (3 * a / (4 * math.pi * f**4 * lP)) ** (1 / 3) * lP
rho_b = c**4 / (8 * math.pi * G * a * w)
Eneg = rho_b * 4 * math.pi * a**2 * w
Rc = math.sqrt(c**4 / (8 * math.pi * G * rho_b))
rhoP = c**7 / (hbar * G**2)
print(f"w = {w:.3e} m = {w/lP:.3e} l_P; |rho_band| = {rho_b:.3e} J/m^3 = {rho_b/rhoP:.3e} rho_Planck")
print(f"negative energy in band = {Eneg:.3e} J = {Eneg/c**2:.3e} kg; local curvature radius sqrt(c^4/(8 pi G rho)) = {Rc:.3e} m")
print(f"w / curvature radius = {w/Rc:.3e}; w / a = {w/a:.3e}")
