"""M-CONSTRAINTS-01: eq. 14 coefficient from isotropic kinetic theory.
Natural units hbar = c = 1. Gravitons isotropic, unpolarised (R and L equally populated),
number density n = rho/omega for a monochromatic background. Cross sections (input, toolkit):
sigma(R,L) = sigma(L,R) = (4/5) pi G^2 s, sigma(R,R) = sigma(L,L) = 0, s = 2 w1 w2 (1 - c).
Pair production rate per volume (identical particles -> factor 1/2):
Gamma = (1/2) * sum over helicity pairs (1/4 each) n^2 < sigma (1 - c) >_angles.
Claim: Gamma = (8 pi/15) G^2 rho^2, independent of the spectrum.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, finish

G, n, w, c = sp.symbols("G n w c", positive=True)
cc = sp.symbols("cc", real=True)
s = 2 * w * w * (1 - cc)
sig_avg = sp.Rational(1, 4) * 2 * sp.Rational(4, 5) * sp.pi * G**2 * s   # RL+LR, RR=LL=0
flux = 1 - cc                                                             # relative velocity factor
ang = sp.integrate(sig_avg * flux, (cc, -1, 1)) / 2                       # isotropic average over cos
Gamma = sp.Rational(1, 2) * n**2 * ang
rho = n * w
print("Gamma =", sp.simplify(Gamma), "; Gamma/(G^2 rho^2) =", sp.simplify(Gamma / (G**2 * rho**2)))
identity(sp.simplify(Gamma / (G**2 * rho**2)), 8 * sp.pi / 15)

# spectrum independence: two-line spectrum n1 at w1, n2 at w2; sigma ~ s = 2 w1 w2 (1-c)
n1, n2, w1, w2 = sp.symbols("n1 n2 w1 w2", positive=True)
def pair_rate(na, wa, nb, wb, same):
    sab = 2 * wa * wb * (1 - cc)
    a = sp.integrate(sp.Rational(1, 2) * sp.Rational(4, 5) * sp.pi * G**2 * sab * (1 - cc), (cc, -1, 1)) / 2
    return (sp.Rational(1, 2) if same else 1) * na * nb * a
tot = pair_rate(n1, w1, n1, w1, True) + pair_rate(n2, w2, n2, w2, True) + pair_rate(n1, w1, n2, w2, False)
identity(sp.simplify(tot), 8 * sp.pi / 15 * G**2 * (n1 * w1 + n2 * w2)**2)

# limit: as one line vanishes, reduce to monochromatic
limit(sp.simplify(tot / (G**2 * (n1 * w1)**2)), "n2", 0, 8 * sp.pi / 15)

# cross-check numerically by Gauss-Legendre (independent of sympy integration)
import numpy as np
x, wt = np.polynomial.legendre.leggauss(10)
val = 0.5 * np.sum(wt * 0.5 * (4 / 5) * np.pi * 2 * (1 - x) * (1 - x)) / 2
print("Gauss-Legendre coefficient:", val, " 8pi/15 =", 8 * np.pi / 15)
identity(sp.Float(val, 30), sp.N(8 * sp.pi / 15, 30))
raise SystemExit(finish())
