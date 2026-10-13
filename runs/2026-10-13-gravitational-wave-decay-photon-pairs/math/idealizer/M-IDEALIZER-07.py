"""M-IDEALIZER-07/08: scalar l = 2 multipole toy (F6, F14).

Natural units, k = w = 1, x = kr. Complex amplitude psi = F(x) P(theta) e^{i m phi}, field = Re(psi e^{-it}).
Outgoing: F = h2(x) = i e^{ix}/x (1 + 3i/x - 3/x^2). Standing (time-symmetric, same outgoing luminosity): F = 2 j2 = 2 Re h2.
Cycle-averaged stress in an orthonormal (t, r, theta, phi) frame, eta = diag(-1,1,1,1):
A_ab = (1/2) Re(D_a psi conj(D_b psi)), T_ab = A_ab - (1/2) eta_ab eta^cd A_cd, TT = sum (eta^aa eta^bb) T_ab^2.
L = x^2 Int dOmega (-A_tr) of the outgoing wave (constant in x). f(x) = x^4 Int dOmega TT / L^2.
Yield beyond x0 relative to the in-state total (12 pi/25) G^2 w L^2 T_dur, using Gamma = (2 pi/5) G^2 TT:
R(>x0) = (2pi/5)/(12pi/25) Int_{x0}^inf f/x^2 dx = (5/6) Int f/x^2 dx.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import identity, quantity, finish
import mpmath as mp
import sympy as sp

mp.mp.dps = 40
X = sp.symbols("x", positive=True)
h2s = sp.I * sp.exp(sp.I * X) / X * (1 + 3 * sp.I / X - 3 / X**2)
# check h2 against the spherical Bessel definitions (limit check of the closed form)
quantity(f"{float(sp.re(h2s.subs(X, sp.Rational(7, 3))).evalf())}", f"{float(sp.expand_func(sp.jn(2, sp.Rational(7, 3))).evalf())}", rel_tol=1e-12)
h2 = sp.lambdify(X, h2s, "mpmath"); dh2 = sp.lambdify(X, sp.diff(h2s, X), "mpmath")
nodes, weights = zip(*[(mp.mpf(n), mp.mpf(wt)) for n, wt in zip(*__import__("numpy").polynomial.legendre.leggauss(30))])
# Gauss-Legendre in u = cos(theta); integrands are polynomials in u (even powers of sin)

def angular(m):
    if m == 2:
        return (lambda u: (1 - u**2), lambda u: 2 * mp.sqrt(1 - u**2) * u, lambda u: mp.sqrt(1 - u**2))  # P, dP/dth, P/sin
    return (lambda u: 3 * u**2 - 1, lambda u: -6 * u * mp.sqrt(1 - u**2), lambda u: (3 * u**2 - 1) / mp.sqrt(1 - u**2))

def stress_integrals(F, dF, x, m):
    P, dP, Ps = angular(m)
    eta = [-1, 1, 1, 1]
    sTT = mp.mpf(0); sflux = mp.mpf(0)
    for u, wt in zip(nodes, weights):
        D = [-1j * F * P(u), dF * P(u), F * dP(u) / x, 1j * m * F * Ps(u) / x]
        A = [[mp.re(D[a] * mp.conj(D[b])) / 2 for b in range(4)] for a in range(4)]
        tr = sum(eta[a] * A[a][a] for a in range(4))
        T = [[A[a][b] - (eta[a] / 2 * tr if a == b else 0) for b in range(4)] for a in range(4)]
        sTT += wt * sum(eta[a] * eta[b] * T[a][b]**2 for a in range(4) for b in range(4))
        sflux += wt * (-A[0][1])
    return 2 * mp.pi * sTT, 2 * mp.pi * sflux

def L_out(m, x=mp.mpf(3)):
    return x**2 * stress_integrals(h2(x), dh2(x), x, m)[1]

def f(x, m, kind):
    x = mp.mpf(x)
    if kind == "out":
        F, dF = h2(x), dh2(x)
    else:
        F, dF = 2 * mp.re(h2(x)), 2 * mp.re(dh2(x))
    return x**4 * stress_integrals(F, dF, x, m)[0] / L_out(m)**2

if __name__ == "__main__":
    # flux constancy (conservation) check of the outgoing wave
    quantity(f"{L_out(2, mp.mpf(1))}", f"{L_out(2, mp.mpf(50))}", rel_tol=1e-20)
    print("x, f_out(m=2), f_out(m=0), f_standing(m=2)")
    for x in [1, 2, 5, 10, 100, 1000, 1e4, 1e5]:
        print(x, mp.nstr(f(x, 2, "out"), 6), mp.nstr(f(x, 0, "out"), 6), mp.nstr(f(x, 2, "st"), 6))
    # asymptotic coefficients: x^2 f_out -> const?
    for m, lens_c in [(2, 0.251), (0, 0.507)]:
        a1, a2 = f(1e4, m, "out") * mp.mpf(1e4)**2, f(1e5, m, "out") * mp.mpf(1e5)**2
        print(f"m={m}: x^2 f at 1e4, 1e5 = {mp.nstr(a1, 6)}, {mp.nstr(a2, 6)}; local slope 1e2->1e3 =",
              mp.nstr(mp.log(f(1e3, m, 'out') / f(1e2, m, 'out')) / mp.log(10), 5))
    # standing-wave plateau (cycle-averaged; average over a few periods in x to remove ripple)
    fs = mp.quad(lambda x: f(x, 2, "st"), [200, 200 + 2 * mp.pi * 5]) / (2 * mp.pi * 5)
    print("standing-wave plateau <f> near x = 200:", mp.nstr(fs, 6), "(lens -> 1.2)")
    print("lens value 1.21 (mean of five samples x = 4..64 of an oscillating f); x-average here:", mp.nstr(fs, 6))
    quantity(f"{fs}", "1.21", rel_tol=0.05)   # expected to FAIL: documents the discrepancy
    quantity(f"{fs}", "1.3641", rel_tol=0.005)  # analytic plateau 3 Int P^4/L^2 (M-08)
    raise SystemExit(finish())
