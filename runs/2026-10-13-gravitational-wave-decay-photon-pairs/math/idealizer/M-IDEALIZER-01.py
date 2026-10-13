"""M-IDEALIZER-01: eq. 8 coefficient in B&O's ideal model, independent derivation.

Natural units (hbar = c = 1). Coherent state: amplitude alpha(k, lambda) = Theta (real, both
helicities) for |k| in [w - sig/2, w + sig/2], isotropic; states normalised with dk = d^3k/((2pi)^3 2|k|).
N = sum_lambda Int dk |alpha|^2 = Theta^2 w sig/(2 pi^2) (exact).
2->2 operator gives pair amplitude A(p1,p2) = (1/2) Int dk1 dk2 alpha alpha M_eff (2pi)^4 delta^4(k1+k2-K),
M_eff = sum over graviton helicities with real sign = 8 pi G (t^2+u^2)/s = 4 pi G s (1 + cos^2 Th_cm)
for each of the two opposite-helicity photon configurations. P = (1/2)(identical photons) sum_h Int dp1 dp2 |A|^2.
Graviton pair phase space for massless: dPhi2 = dOmega/(32 pi^2) (exact). Lab energies w1,2 = (K0 +- |K| c)/2,
c = cos(angle of graviton axis to K) in the CM frame, so the band forces |K| c in [-(sig-|d0|), sig-|d0|], d0 = K0 - 2w.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import identity, limit, quantity, finish
import sympy as sp
import numpy as np
from scipy import integrate

G, Th, w, sig, K, d0, a, ct, c = sp.symbols("G Theta w sigma K d0 a ct c", positive=True)
Nn = Th**2 * w * sig / (2 * sp.pi**2)

# ring integral over the graviton azimuth (graviton axis at polar c from K; photon at polar ct from K)
# cos Th_cm = c ct + sqrt(1-c^2) sqrt(1-ct^2) cos phi; Int dphi (1 + cos^2) =
ring = 2 * sp.pi * (1 + c**2 * ct**2 + (1 - c**2) * (1 - ct**2) / 2)
I_a = sp.integrate(ring, (c, -a, a))   # graviton-axis band |c| <= a
A = sp.Rational(1, 2) * Th**2 / (32 * sp.pi**2) * 4 * sp.pi * G * I_a   # times s (kept separately)

# narrow band: a = (sig - |d0|)/K << 1, keep leading order in a
I_lead = sp.series(I_a, a, 0, 2).removeO()
print("leading ring-band integral:", sp.simplify(I_lead), " (lens: 2a * 2pi(1 + sin^2/2))")
identity(I_lead, 2 * a * 2 * sp.pi * (1 + (1 - ct**2) / 2))

# P = (1/2)*2 configs * Int d^4K/(2pi)^4 * dOmega*/(32pi^2) |A|^2 ; d^4K = dd0 * 4 pi K^2 dK; s = 4w^2 - K^2
Asq_ang = sp.integrate(2 * sp.pi * (A.subs(I_a, I_lead).subs(a, 1))**2, (ct, -1, 1))  # angular part with a factored out
Asq_ang = sp.integrate(2 * sp.pi * (sp.Rational(1, 2) * Th**2 / (32 * sp.pi**2) * 4 * sp.pi * G * I_lead)**2, (ct, -1, 1))
P_expr = (1 / (2 * sp.pi)**4) * (1 / (32 * sp.pi**2)) * Asq_ang * 4 * sp.pi * K**2 * (4 * w**2 - K**2)**2
P_expr = P_expr.subs(a, (sig - d0) / K)          # d0 >= 0 half, doubled below
P = 2 * sp.integrate(sp.integrate(P_expr, (K, 0, 2 * w)), (d0, 0, sig))
c_tot = sp.simplify(P / (G**2 * Nn**2 * w**3 * sig))
print("narrow-band c_tot =", c_tot)
identity(c_tot, sp.Rational(4, 25))

# B&O bookkeeping T_eff = 2 pi Int (a*a)^2 / (Int a)^4 for a top hat of full width sig
u = sp.symbols("u", real=True)
tri = sig - sp.Abs(u)
T_eff = 2 * sp.pi * 2 * sp.integrate((sig - u)**2, (u, 0, sig)) / sig**4
print("T_eff =", sp.simplify(T_eff))
identity(T_eff, 4 * sp.pi / (3 * sig))
identity(sp.Rational(4, 25) / T_eff * sig**0, 3 * sig / (25 * sp.pi))   # eq. 8 coefficient: rate = c * G^2 N^2 w^3 sig^2
# limit: the rate coefficient times T_eff returns the total for any sig
limit((3 * sig**2 / (25 * sp.pi)) * (4 * sp.pi / (3 * sig)) / sig, "sig", 0, sp.Rational(4, 25))

# exact (finite-band) kinematics, numeric: G = Theta = w = 1
Ia_f = sp.lambdify((a, ct), I_a, "numpy")
def c_exact(sg):
    def inner(Kv, dd):
        aa = min(1.0, (sg - abs(dd)) / Kv) if Kv > 0 else 1.0
        cts, wts = np.polynomial.legendre.leggauss(8)
        vals = (0.5 / (32 * np.pi**2) * 4 * np.pi * Ia_f(aa, cts))**2
        ang = 2 * np.pi * np.sum(wts * vals)
        K0 = 2 + dd
        s = K0**2 - Kv**2
        return (1 / (2 * np.pi)**4) / (32 * np.pi**2) * ang * 4 * np.pi * Kv**2 * s**2
    val, err = integrate.dblquad(lambda Kv, dd: inner(Kv, dd), -sg, sg, lambda dd: 0.0, lambda dd: 2 + dd,
                                 epsabs=1e-13, epsrel=1e-7)
    N = sg / (2 * np.pi**2)
    return val / (N**2 * sg)

for sg, lens in [(0.1, 0.1526), (0.03, 0.1577), (0.01, 0.1592)]:
    ce = c_exact(sg)
    print(f"sigma/w = {sg}: exact-kinematics c_tot = {ce:.5f} (lens {lens})")
    quantity(f"{ce}", f"{lens}", rel_tol=3e-3)
raise SystemExit(finish())
