"""Falsifier C6-1: branch (b) of C6 (null incompleteness / singular sources).

Checks, in geometric units (G = c = 1, lengths in metres):
1. Schwarzschild with mass parameter m of either sign is vacuum (Einstein tensor = 0)
   on its regular domain r > max(0, 2m): pointwise NEC/WEC hold there trivially.
2. For m < 0 the spacetime is null-incomplete (naked singularity at r = 0, Kretschmann
   48 m^2 / r^6 diverges) and radial light is ADVANCED relative to flat space; for m > 0
   it is delayed.  So 'escaping null completeness' does produce a time advance with no
   pointwise negative energy on the regular manifold -- but only by putting negative
   ADM mass in the singularity (Penrose-Sorkin-Woolgar: negative total mass advances).
3. Weak-field transit excess at impact parameter b between rest points at -D and +D:
   dt_excess = 4 m [ln(2D/b)] + O(m) style sign check via exact quadrature.
"""
import sympy as sp
import numpy as np
from scipy.integrate import quad

t, r, th, ph, m = sp.symbols('t r theta phi m', real=True)
f = 1 - 2*m/r
g = sp.diag(-f, 1/f, r**2, r**2*sp.sin(th)**2)
X = [t, r, th, ph]
ginv = g.inv()
n = 4
Gam = [[[sp.simplify(sum(ginv[a, d]*(sp.diff(g[d, b], X[c]) + sp.diff(g[d, c], X[b]) - sp.diff(g[b, c], X[d])) for d in range(n))/2)
         for c in range(n)] for b in range(n)] for a in range(n)]
def Riem(a, b, c, d):
    e = sp.diff(Gam[a][d][b], X[c]) - sp.diff(Gam[a][c][b], X[d])
    e += sum(Gam[a][c][k]*Gam[k][d][b] - Gam[a][d][k]*Gam[k][c][b] for k in range(n))
    return sp.simplify(e)
R = sp.zeros(4)
for b in range(n):
    for d in range(n):
        R[b, d] = sp.simplify(sum(Riem(a, b, a, d) for a in range(n)))
print("Ricci tensor (any sign of m):", R)
print("=> vacuum, T_ab = 0 pointwise on the regular domain for m > 0 and m < 0")

# Kretschmann
Rl = {}
K = 0
for a in range(n):
    for b in range(n):
        for c in range(n):
            for d in range(n):
                val = Riem(a, b, c, d)
                if val != 0:
                    Rl[(a, b, c, d)] = val
# lower first index and contract: K = R_abcd R^abcd
Rdown = lambda a, b, c, d: sum(g[a, e]*Rl.get((e, b, c, d), 0) for e in range(n))
Rup = lambda a, b, c, d: sum(ginv[b, p]*ginv[c, q]*ginv[d, s]*Rl.get((a, p, q, s), 0)
                              for p in range(n) for q in range(n) for s in range(n))
for a in range(n):
    for b in range(n):
        for c in range(n):
            for d in range(n):
                K += Rdown(a, b, c, d)*Rup(a, b, c, d)
print("Kretschmann:", sp.simplify(K), "(diverges at r = 0 for either sign: null-incomplete)")

# Radial light travel time between static rest points r1 < r2, in asymptotic time t
r1, r2 = sp.symbols('r1 r2', positive=True)
dt = sp.integrate(1/(1 - 2*m/r), (r, r1, r2))
print("radial t(r1->r2) =", sp.simplify(dt))
for mv in (-1000.0, +1000.0):
    val = float(dt.subs({m: mv, r1: 1.0e4, r2: 1.0e9}))
    print(f"m = {mv:+.0f} m (geo): radial coordinate time - (r2 - r1) = {val - (1e9 - 1e4):+.1f} m "
          f"= {(val - (1e9 - 1e4))/2.998e8*1e6:+.3f} microseconds  ({'ADVANCE' if val < 1e9 - 1e4 else 'delay'})")

# Non-radial pass with impact parameter b between rest points at x = -D and +D,
# weak-field (isotropic) light: dt/dx = 1 + 2|Phi| for Phi = -m/rho  (sign follows m)
def excess(mv, b, D):
    integrand = lambda x: 2*mv/np.sqrt(x*x + b*b)
    val, err = quad(integrand, -D, D, limit=200)
    return val
for mv in (-1000.0, +1000.0):
    for D in (1e8, 1e10):
        e = excess(mv, 1e5, D)
        print(f"weak-field pass: m={mv:+.0f} m, b=1e5 m, D={D:.0e} m: excess = {e:+.1f} m = {e/2.998e8*1e6:+.3f} us "
              f"(analytic 4m ln(2D/b) = {4*mv*np.log(2*D/1e5):+.1f} m)")
print("Conclusion: an advance appears only for m < 0 (negative ADM mass hidden in the singularity).")
