"""Falsifier C4-2 (scale): what does interior dragging buy, at what cost, and is it the best use of the mass?
Units: SI unless marked 'geo' (G = c = 1).
"""
import math
from scipy.optimize import brentq

G = 6.674e-11; c = 2.998e8; g0 = 9.80665
ly = 9.4607e15; yr = 3.15576e7
M = 4.511e27          # kg, toolkit M_ADM of the Fuchs 2024 shell rebuild (input)
R1, R2 = 10.0, 20.0   # m
m_pay = 1e5           # kg payload (candidate slate convention)
d_aCen = 4.37 * ly
Lsun = 3.828e26

print("== A. Thin-shell (Israel) static shell: dominant energy condition p <= sigma ==")
# geo units, mass m=1: sigma = (1 - sqrt(1-2/R))/(4 pi R); p = [(1-1/R)/sqrt(1-2/R) - 1]/(8 pi R)
def sig(R): return (1 - math.sqrt(1 - 2/R)) / (4*math.pi*R)
def prs(R): return ((1 - 1/R)/math.sqrt(1 - 2/R) - 1) / (8*math.pi*R)
Rdec = brentq(lambda R: prs(R) - sig(R), 2.0001, 10)
print(f"DEC boundary R/M = {Rdec:.6f} (25/12 = {25/12:.6f}); compactness 2M/R = {2/Rdec:.4f} (24/25 = 0.96)")
for C in (0.335, 0.67, 8/9, 0.96, 0.99):
    R = 2/C
    print(f"  C={C:.3f}: p/sigma = {prs(R)/sig(R):.3f}  (DEC holds if <= 1)")

print("\n== B. Strong-field dragging proxy: Brill-Cohen rotational shell, omega/Omega = 4a(2-a)/((1+a)(3-a)), a = M/(2 r_iso) ==")
print("   (proxy only: Pfister et al. 2005 report linear dragging 'compares favourably' with rotational; kappa=1 only at R=2M)")
def kappa_BC(C):
    Rs = 2.0/C   # Schwarzschild areal radius in units of M
    # Rs = r (1 + 1/(2r))^2 -> solve for isotropic r
    r = brentq(lambda r: r*(1+1/(2*r))**2 - Rs, 0.5, 1e6)
    a = 1/(2*r)
    return 4*a*(2-a)/((1+a)*(3-a))
print(f"  check weak field C=1e-4: kappa_BC={kappa_BC(1e-4):.4e} vs Thirring 4M/(3R)=2C/3={2e-4/3:.4e}")
print(f"  check C->1: kappa_BC(0.999999)={kappa_BC(0.999999):.6f}")
for C in (0.335, 0.67, 8/9, 0.96):
    k = kappa_BC(C)
    print(f"  C={C:.3f}: kappa_BC = {k:.3f}; felt fraction 1-kappa = {1-k:.3f}; g-shield gain 1/(1-kappa) = {1/(1-k):.2f}")
print("  linear-theory coefficient used by C4 for comparison: kappa_lin = 2C = 0.67 (C=0.335), 1.34 (C=0.67)")

print("\n== C. alpha Cen trip, crew felt limit 1 g; shell acceleration A = g/f where f = felt fraction ==")
def trip(A):
    phi = math.acosh(1 + A*d_aCen/(2*c**2))      # peak rapidity, midpoint flip
    tau = 2*c/A*phi                               # proper time (lapse ignored)
    t = 2*c/A*math.sinh(phi)                      # coordinate time
    ratio = math.exp(2*phi)                       # ideal photon rocket m_i/m_f, accelerate+decelerate
    return phi, tau/yr, t/yr, ratio
cases = [("1 g rocket (payload feels A)", 1.0), ("f=0.5", 0.5), ("f=0.2", 0.2), ("f=0.1", 0.1), ("f=0.01", 0.01)]
for name, f in cases:
    A = g0/f
    phi, tau, t, ratio = trip(A)
    Eshell = (M + m_pay)*(ratio - 1)*c**2
    Epay = m_pay*(ratio - 1)*c**2
    print(f"  {name:30s}: A={A/g0:6.0f} g, peak rapidity {phi:.3f}, crew time {tau:.3f} yr, Earth time {t:.3f} yr, "
          f"photon-rocket mass ratio {ratio:.3e}; exhaust energy shell+payload {Eshell:.3e} J = {(M+m_pay)*(ratio-1)/1.989e30:.2e} M_sun; payload-only {Epay:.3e} J")
phi1, tau1, t1, r1 = trip(g0)
print(f"  crew-time saving of f=0.1 over a 1 g rocket: {tau1 - trip(g0/0.1)[1]:.2f} yr; Earth-time floor {d_aCen/c/yr:.2f} yr")
print(f"  photon push power at A = 10 g for the shell: P = M A c = {M*10*g0*c:.3e} W = {M*10*g0*c/Lsun:.2e} L_sun")

print("\n== D. Same mass used as an exterior gravity tow (payload in free fall beside the pushed mass) ==")
L = 2.0  # m, payload length
for Ag in (1, 10, 100, 1000):
    A = Ag*g0
    d = math.sqrt(G*M/A)
    tidal = 2*A*L/d
    print(f"  A={Ag:5d} g: tow distance d = sqrt(GM/A) = {d:.3e} m (> R2 = 20 m: {d > R2}); felt (free fall) ~ 0; tidal stretch over {L} m = {tidal:.2e} m/s^2 = {tidal/g0:.2e} g")
# minimum tow mass made of ordinary dense matter (osmium 2.26e4 kg/m^3), payload at the surface d = r
rho = 2.26e4
for Ag in (10, 100):
    A = Ag*g0
    r = A/(G*4/3*math.pi*rho)
    Mt = 4/3*math.pi*r**3*rho
    print(f"  ordinary-density tow body for A={Ag} g: radius {r:.3e} m, mass {Mt:.3e} kg = {Mt/M:.3e} x the C4 shell mass; tidal {2*A*L/r:.2e} m/s^2")

print("\n== E. Pusher contact pressure vs shell's own static stress (is the push the binding stress?) ==")
for Ag in (1, 10, 100):
    P = M*Ag*g0/(4*math.pi*R2**2)
    print(f"  A={Ag} g: M A /(4 pi R2^2) = {P:.2e} Pa; shell static p_t max 3.87e39 Pa (toolkit, M-CONSTRAINTS-12); ratio {P/3.87e39:.1e}; vs 1 TPa material: {P/1e12:.1e}x")
