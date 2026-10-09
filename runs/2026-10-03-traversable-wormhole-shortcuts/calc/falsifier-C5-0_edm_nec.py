"""Falsifier C5-0 (physics): does an Einstein-Dirac-Maxwell (EDM) static wormhole avoid exotic matter?

Brief's definition: exotic matter = matter violating the NEC classically.
Setup: static spherically symmetric metric in proper radial distance l (G = c = 1, metres):
    ds^2 = -e^{2 Phi(l)} dt^2 + dl^2 + r(l)^2 dOmega^2
Radial null vector k = (e^{-Phi}, 1, 0, 0) (affine up to a constant factor).
Steps
 1. G_kk for arbitrary Phi(l), r(l) (gr_tensors Spacetime); evaluate at a throat r'=0, r''>0.
 2. The most general static spherically symmetric Maxwell field (radial electric E(l), magnetic
    monopole P): T^EM_kk along radial null rays, symbolically.
 3. Hence T^Dirac_kk = G_kk/(8 pi) - T^EM_kk at the throat: sign.
 4. Radial ANEC of the Dirac sector on an asymmetric, asymptotically flat sample throat
    (numerical quadrature, convergence check), compared with the by-parts identity.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
import mpmath as mp
from gr_tensors import Spacetime

t, l, th, ph = sp.symbols("t l theta phi", real=True)
Phi = sp.Function("Phi")(l)
r = sp.Function("r")(l)
g = sp.diag(-sp.exp(2 * Phi), 1, r**2, r**2 * sp.sin(th) ** 2)
st = Spacetime(g, [t, l, th, ph])
G = st.einstein()
k = sp.Matrix([sp.exp(-Phi), 1, 0, 0])
Gkk = sp.simplify((k.T * G * k)[0, 0])
print("1. G_ab k^a k^b (radial null, arbitrary Phi(l), r(l)) =", Gkk)
rp, rpp, Php = sp.symbols("rp rpp Phip")
Gkk_sub = sp.simplify(Gkk.subs(sp.Derivative(r, (l, 2)), rpp).subs(sp.Derivative(r, l), rp)
                      .subs(sp.Derivative(Phi, l), Php))
print("   in symbols (rp=r', rpp=r'', Phip=Phi'):", sp.expand(Gkk_sub))
throat = sp.simplify(Gkk_sub.subs(rp, 0))
print("   at a throat (r'=0):", throat, " -> 8 pi T_kk; sign for r''>0, r>0:",
      "NEGATIVE" if sp.simplify(throat.subs({rpp: 1, r: 1})) < 0 else "check")
# identity check: Gkk == 2 Phi' r'/r - 2 r''/r
expected = 2 * Php * rp / r - 2 * rpp / r
print("   identity G_kk = 2 Phi' r'/r - 2 r''/r :", sp.simplify(Gkk_sub - expected) == 0)

# 2. Maxwell stress tensor, most general static spherical field
E = sp.Function("E")(l)  # radial electric field measured by static observer
P = sp.symbols("P", real=True)  # magnetic monopole charge
F = sp.zeros(4, 4)
F[0, 1] = -E * sp.exp(Phi)   # F_tl, orthonormal E_l = E
F[1, 0] = E * sp.exp(Phi)
F[2, 3] = P * sp.sin(th)     # F_theta phi -> B_r = P/r^2
F[3, 2] = -P * sp.sin(th)
ginv = g.inv()
Fup = ginv * F * ginv
F2 = sum(F[a, b] * Fup[a, b] for a in range(4) for b in range(4))
TEM = sp.zeros(4, 4)
Fmixed = F * ginv  # F_a^c
for a in range(4):
    for b in range(4):
        TEM[a, b] = (sum(F[a, c] * Fmixed[b, c] for c in range(4)) - g[a, b] * F2 / 4) / (4 * sp.pi)
TEM = TEM.applyfunc(sp.simplify)
TEMkk = sp.simplify((k.T * TEM * k)[0, 0])
rhoEM = sp.simplify(TEM[0, 0] * sp.exp(-2 * Phi))
print("2. Maxwell energy density (static observer) =", rhoEM, "(>= 0)")
print("   Maxwell T_kk along radial null rays =", TEMkk)
# also tangential null direction: Maxwell satisfies NEC there too
kt = sp.Matrix([sp.exp(-Phi), 0, 1 / r, 0])
print("   Maxwell T_kk along tangential null =", sp.simplify((kt.T * TEM * kt)[0, 0]), "(>= 0)")

# 3. Dirac sector at throat
print("3. => 8 pi T^Dirac_kk(throat) = G_kk - 8 pi T^EM_kk = -2 r''/r_0 - 0 < 0 for every flare-out throat,")
print("   any fermion number, mass, charge, frequency, symmetric or asymmetric: Dirac sector violates NEC.")

# 4. ANEC on an asymmetric, asymptotically flat sample (different Phi and r at the two ends)
mp.mp.dps = 30
b0 = mp.mpf(1)  # throat scale, metres (geometric units)
def r_f(x):
    return mp.sqrt(x**2 + b0**2) + mp.mpf("0.3") * b0 * (mp.tanh(x / b0) + 1)
def Phi_f(x):
    return -mp.mpf("0.4") * b0 / mp.sqrt(x**2 + 4 * b0**2) + mp.mpf("0.1") * mp.tanh(x / b0)
def integrand(x):
    rr = r_f(x); r1 = mp.diff(r_f, x); r2 = mp.diff(r_f, x, 2); P1 = mp.diff(Phi_f, x)
    Gkk_val = 2 * P1 * r1 / rr - 2 * r2 / rr
    # k^l = 1 with k_t = -e^{Phi}; affine k: K = e^{-Phi} k (E=1 normalisation): T_KK dlambda/dl = e^{-Phi} T_kk
    return mp.e**(-Phi_f(x)) * Gkk_val / (8 * mp.pi)
x_min = mp.findroot(lambda x: mp.diff(r_f, x), 0)
print("4. sample asymmetric throat: r' = 0 at l =", mp.nstr(x_min, 8), "m, r0 =", mp.nstr(r_f(x_min), 8), "m")
for L in (200, 400):
    val = mp.quad(integrand, [-L, -10, x_min, 10, L])
    print(f"   direct radial ANEC (Dirac sector = total, E=1) over |l|<{L} m: {mp.nstr(val, 12)} m^-1")
byparts = mp.quad(lambda x: -(1 / (4 * mp.pi)) * mp.e**(-Phi_f(x)) * (mp.diff(r_f, x) / r_f(x))**2,
                  [-mp.inf, -10, x_min, 10, mp.inf])
print("   by-parts value -(1/4pi) int e^{-Phi}(r'/r)^2 dl over R:", mp.nstr(byparts, 12), "m^-1 (strictly negative)")
