"""M-ENGINEER-01: MMP energy minimisation (eq. 5.30-5.31, quoted) and the r_e form of |E_min|.
Units hbar = c = 1, G = lp^2. E(l) = r^3/(G l^2) - q/(8 l); r = r_e > 0, q > 0 (flux units), l > 0.
Extremal relation used by the lens: r_e = sqrt(pi) q lp / g, g > 0 the U(1) coupling.
Also the lens's N-species extension: Casimir term scaled by N, E = r^3/(G l^2) - N q/(8 l).
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, sign, quantity, units, finish

r, q, l, G, g, lp, Nn = sp.symbols("r q l G g lp Nn", positive=True)

E = r**3 / (G * l**2) - q / (8 * l)
crit = sp.solve(sp.diff(E, l), l)
print("critical l:", crit)
lstar = crit[0]
identity(lstar, 16 * r**3 / (G * q))
identity(sp.simplify(E.subs(l, lstar)), -G * q**2 / (256 * r**3))
# it is a minimum: second derivative positive
sign(sp.simplify(sp.diff(E, l, 2).subs(l, lstar)), "positive")

# Substitute G = lp^2, r_e = sqrt(pi) q lp / g
sub = {G: lp**2, r: sp.sqrt(sp.pi) * q * lp / g}
identity(lstar.subs(sub), 16 * sp.pi**sp.Rational(3, 2) * q**2 * lp / g**3)
Emin = (-G * q**2 / (256 * r**3)).subs(sub)
identity(Emin, -g**3 / (256 * sp.pi**sp.Rational(3, 2) * q * lp))
# in terms of r_e: q = g r / (sqrt(pi) lp)
Emin_r = (-g**3 / (256 * sp.pi**sp.Rational(3, 2) * q * lp)).subs(q, g * r / (sp.sqrt(sp.pi) * lp))
identity(Emin_r, -g**2 / (256 * sp.pi * r))
# scaling: |E_min| falls as 1/r_e at fixed g -> r * |E_min| independent of r
identity(sp.diff(r * Emin_r, r), 0)
# limit: as r_e -> oo at fixed g the binding goes to zero
limit(Emin_r, "r", "oo", "0")

# N-species extension
EN = r**3 / (G * l**2) - Nn * q / (8 * l)
lN = sp.solve(sp.diff(EN, l), l)[0]
identity(lN, 16 * r**3 / (G * q * Nn))
EminN = sp.simplify(EN.subs(l, lN))
identity(EminN, -G * Nn**2 * q**2 / (256 * r**3))
identity(EminN.subs(sub).subs(q, g * r / (sp.sqrt(sp.pi) * lp)), -Nn**2 * g**2 / (256 * sp.pi * r))
# N = 1 limit reproduces the paper's formula
identity(EminN.subs(Nn, 1), -G * q**2 / (256 * r**3))
# with g^2 N <= 1: |E_min| = N (g^2 N)/(256 pi r) <= N/(256 pi r)
x = sp.symbols("x", positive=True)   # x = g^2 N in (0, 1]
sign((Nn / (256 * sp.pi * r) - Nn**2 * g**2 / (256 * sp.pi * r)).subs(g, sp.sqrt(x / Nn)), "nonnegative",
     domain={"Nn": (1, 1e6), "x": (1e-6, 1), "r": (0.1, 10)})

# SI units of |E_min| = g^2 hbar c/(256 pi r_e)
units("hbar*c/(256*pi*1 m)", "energy")
quantity("0.06^2*hbar*c/(256*pi*(hbar*c/(1 TeV)))", "7.17e-13 J", rel_tol=5e-3)
raise SystemExit(finish())
