"""M-CONSTRAINTS-05: the (t, x) block of an orthonormal-frame stress tensor (F6 mechanism).

Orthonormal frame, eta = diag(-1, 1). T_ab = [[rho, -J], [-J, p]] (J the momentum density; the
sign of J is irrelevant). Claims: NEC along k = (1, +-1) <=> |J| <= (rho + p)/2; the block is
Hawking-Ellis type I (real, distinct eigenvalues of T^a_b with a timelike eigenvector) <=> |J| < (rho + p)/2
when rho + p > 0.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, inequality, sign, finish

rho, p, J, lam = sp.symbols("rho p J lam", real=True)
T = sp.Matrix([[rho, -J], [-J, p]])
eta = sp.diag(-1, 1)
for s in (1, -1):
    k = sp.Matrix([1, s])
    identity(sp.expand((k.T * T * k)[0]), rho + p - 2 * s * J)
Tmix = eta * T          # T^a_b
disc = sp.discriminant(sp.expand((Tmix - lam * sp.eye(2)).det()), lam)
identity(sp.expand(disc), sp.expand((rho + p)**2 - 4 * J**2))
# timelike eigenvector when |J| < (rho+p)/2: eigenvector (1, w) has |w| < 1
dom = {"rho": (0.1, 10), "p": (-0.09, 10), "J": (-0.04, 0.04)}
ev = Tmix.eigenvects()
for val, mult, vecs in ev:
    vec = vecs[0]
    w = sp.simplify(vec[1] / vec[0])
    norm = sp.simplify(-1 + w**2)
    print("eigenvalue", val, " w =", w)
# numeric check of the timelike eigenvector inside the cap (rho + p >= 0.01 > 2|J| = 0.08? no): use a scaled domain
rr, pp, jj = sp.symbols("rr pp jj", positive=True)
# parametrise J = q (rho + p)/2 with |q| < 1
q = sp.symbols("q", real=True)
Tq = sp.Matrix([[-rr, q * (rr + pp) / 2], [-q * (rr + pp) / 2, pp]])
lam1 = (pp - rr) / 2 + (rr + pp) / 2 * sp.sqrt(1 - q**2)
lam0 = (pp - rr) / 2 - (rr + pp) / 2 * sp.sqrt(1 - q**2)
# eigenvector for lam0 is (1, w) with w = (lam0 + rr)/(q (rr+pp)/2)
w0 = (lam0 + rr) / (q * (rr + pp) / 2)
identity(sp.simplify((Tq * sp.Matrix([1, w0]) - lam0 * sp.Matrix([1, w0]))[0]), 0, domain={"q": (0.01, 0.99)})
inequality(w0**2, "<", 1, domain={"q": (0.01, 0.99), "rr": (0.1, 10), "pp": (0.1, 10)})
raise SystemExit(finish())
