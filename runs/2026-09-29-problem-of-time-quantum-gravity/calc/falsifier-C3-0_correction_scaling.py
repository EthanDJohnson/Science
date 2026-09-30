"""Falsifier C3-0: does the Born-Oppenheimer/WKB correction really scale as (E/m_P)^2?

Three checks.
 (1) Toy model M2 (lens IDEALIZER F7, verified M-IDEALIZER-07): exact phase rate
     omega_n = -v*(sqrt(2M(M e0 - E_n)) - M sqrt(2 e0)); series in 1/M.
     The relative correction to E_n is E_n/(2 M v^2) = E_n/(4 K_heavy).
     Show it depends on the heavy kinetic energy K_heavy = M v^2/2, not on M alone:
     at fixed M, changing v changes the correction by (v1/v2)^2.
 (2) Kiefer-Kramer PRL 108, 021301 (2012) eq. (14) quoted:
     C_k = (1 - 43.56/k^3 * H^2/m_P^2)^(-3/2) (1 - 189.18/k^3 * H^2/m_P^2).
     Expand C_k^2 - 1 to first order and show the k-scaling is k^-3, i.e. the
     correction FALLS with mode energy, whereas "(E/m_P)^2" with E ~ k would RISE as k^2.
 (3) Lab Sr clock (SI): ratio E_S/E_grav for background regions of size L,
     E_grav ~ c^4 L / G (natural gravitational energy of a region L), and
     for the Hubble volume E_grav = c^5/(2 G H0). Compare with (E/E_P)^2 (Kiefer m_P).
     Show (E/m_P)^2 corresponds to L = hbar c / E (the transition's own reduced wavelength).
"""
import sympy as sp
import math

print("=== (1) Toy model M2: relative correction = E/(4 K_heavy) ===")
M, e0, E, v = sp.symbols('M e0 E v', positive=True)
eps = sp.symbols('eps', positive=True)  # eps = 1/M
omega = -sp.sqrt(2*e0)*(sp.sqrt(2*M*(M*e0 - E)) - M*sp.sqrt(2*e0))
ser = sp.series(omega.subs(M, 1/eps), eps, 0, 2).removeO()
ser = sp.simplify(ser)
print("omega_n series in eps=1/M:", ser)
vv = sp.sqrt(2*e0)
corr = sp.simplify(ser - E)
print("correction term:", corr, " ; equals E^2/(2 M v^2)?",
      sp.simplify(corr - (E**2*eps/(2*vv**2))) == 0)
Kh = sp.Rational(1, 2)*(1/eps)*vv**2
print("relative correction corr/E =", sp.simplify(corr/E),
      " = E/(4 K_heavy)?", sp.simplify(corr/E - E/(4*Kh)) == 0)
# numeric: same M, different v
for Mv, ev in [(1e4, 50.0), (1e4, 5.0), (1e4, 0.5)]:
    vnum = math.sqrt(2*ev)
    rel = 2.5/(2*Mv*vnum**2)
    print(f"  M={Mv:.0e} e0={ev:5.1f} (model units): relative correction for E=2.5 -> {rel:.3e}")
print("  -> at fixed M (the m_P^2 stand-in) the correction varies with the background kinetic")
print("     energy; it is not a function of E/sqrt(M) alone. Dimensionless ratio = E_S/(4 K_heavy).")

print("\n=== (2) Kiefer-Kramer eq. (14): k-scaling of the correction ===")
k, x = sp.symbols('k x', positive=True)  # x = H^2/m_P^2
Ck = (1 - sp.Rational(4356, 100)*x/k**3)**sp.Rational(-3, 2)*(1 - sp.Rational(18918, 100)*x/k**3)
lin = sp.series(Ck**2, x, 0, 2).removeO()
lin = sp.expand(lin - 1)
print("C_k^2 - 1 to O((H/m_P)^2):", lin)
coef = sp.simplify(lin/x*k**3)
print("  coefficient of (H/m_P)^2 / k^3:", float(coef))
for kk in [1, 10, 100]:
    print(f"  k={kk:4d}: (C_k^2-1)/(H/m_P)^2 = {float(lin.subs({k: kk, x: 1})):.4e}; "
          f"'(E/m_P)^2' ansatz with E proportional to k would scale as k^2 -> ratio to k=1: {kk**2}")
print("  -> within the source the candidate relies on, the correction scales as k^-3 (decreases");
print("     with mode energy at fixed H); (E/m_P)^2 holds only with E = H (horizon-crossing scale).")

print("\n=== (3) Lab Sr clock (SI) ===")
hbar = 1.054571817e-34; c = 2.99792458e8; G = 6.67430e-11
eV = 1.602176634e-19
E_S = 6.62607015e-34*429.228e12        # J, Sr clock transition
E_P_K = math.sqrt(3*math.pi*hbar*c**5/(2*G))   # J, Kiefer convention (2.65e19 GeV)
print(f"E_S = {E_S:.4e} J = {E_S/eV:.4f} eV; Kiefer m_P c^2 = {E_P_K/eV/1e9:.4e} GeV")
cand = (E_S/E_P_K)**2
print(f"candidate's (E/m_P)^2 = {cand:.3e} (dimensionless)")
lam = hbar*c/E_S
print(f"reduced wavelength hbar c/E_S = {lam:.3e} m")
# ratio E_S/E_grav with E_grav = (3 pi/2) c^4 L / G chosen so that L = hbar c/E reproduces (E/m_P)^2 exactly
pref = 3*math.pi/2
for L, name in [(lam, "L = hbar c/E_S (implicit choice)"), (1e-10, "L = 1e-10 m (atom)"),
                (1.0, "L = 1 m (lab)"), (6.371e6, "L = R_Earth")]:
    Eg = pref*c**4*L/G
    print(f"  {name:34s}: E_grav = {Eg:.3e} J ; E_S/E_grav = {E_S/Eg:.3e}")
H0 = 67.4e3/3.0857e22   # 1/s
Eg_H = c**5/(2*G*H0)
print(f"  Hubble volume: E_grav = c^5/(2 G H0) = {Eg_H:.3e} J ; E_S/E_grav = {E_S/Eg_H:.3e}")
print("  -> (E/m_P)^2 = 4.5e-57 is recovered only if the gravitational background scale is the")
print("     atom's own reduced wavelength; other background choices move it from ~1e3 larger")
print("     (atom-sized region) to ~32 orders smaller (Hubble volume). The number is fixed by the")
print("     background, not by E alone. 'Untestable' is unchanged; the scaling law is not.")
