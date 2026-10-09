"""M-CONSTRAINTS-07 (F7). Single-scale QI throat bound.
Statement: static geodesic observer at Phi = 0 throat sees constant rho = -1/(8 pi b0^2) (geometric, i.e.
rho_SI = -c^4/(8 pi G b0^2)). Ford-Roman Lorentzian QI (massless scalar, hbar = c = 1): rho_hat >= -C/tau0^4,
C_FR = 3/(32 pi^2) (literature constant, not derived here). Fewster-Eveson general bound
rho_hat >= -(1/16 pi^2) int (g'')^2 dt with g^2 = Lorentzian; its constant is derived here.
With tau0 = f b0: b0 <= sqrt(8 pi C) l_P / f^2. Claims: 4.89e3 l_P = 7.9e-32 m (FR), 1.83e3 l_P (FE) at f = 0.01;
excess at b0 = 1 m is 1.6e62 vs FR bound 3.0e-20 J/m^3; at 1.5e7 m, 3.6e76."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, quantity, inequality, finish

b0, f, lP, C, tau = sp.symbols("b0 f l_P C tau0", positive=True)
# saturate: 1/(8 pi b0^2) = C lP^2/(f b0)^4  (lP^2 = G hbar / c^3 converts the QI to geometric units)
sol = sp.solve(sp.Eq(1 / (8 * sp.pi * b0**2), C * lP**2 / (f * b0)**4), b0)
bmax = [s for s in sol if s.is_positive][0]
identity(bmax, sp.sqrt(8 * sp.pi * C) * lP / f**2)
CFR = sp.Rational(3, 32) / sp.pi**2
identity(bmax.subs(C, CFR), sp.sqrt(3 / (4 * sp.pi)) * lP / f**2)
# Fewster-Eveson constant for Lorentzian sampling g^2 = (tau0/pi)/(t^2+tau0^2)
tt = sp.symbols("t", real=True)
gfun = sp.sqrt(tau / sp.pi) / sp.sqrt(tt**2 + tau**2)
FE = sp.simplify(sp.integrate(sp.diff(gfun, tt, 2)**2, (tt, -sp.oo, sp.oo)) / (16 * sp.pi**2))
print("Fewster-Eveson Lorentzian constant:", FE, "=", sp.nsimplify(FE * tau**4), "/tau0^4")
CFE = sp.simplify(FE * tau**4)
nFR = float(bmax.subs({C: CFR, f: sp.Rational(1, 100), lP: 1}))
nFE = float(bmax.subs({C: CFE, f: sp.Rational(1, 100), lP: 1}))
print("b0_max/l_P: FR", nFR, " FE", nFE)
inequality(abs(nFR - 4.89e3) / 4.89e3, "<", 0.002)
inequality(abs(nFE - 1.83e3) / 1.83e3, "<", 0.003)
quantity(f"{nFR} * l_P", "7.9e-32 m", rel_tol=3e-3)
limit(sp.sqrt(3 / (4 * sp.pi)) * lP / f**2, "l_P", 0, "0")   # classical limit hbar -> 0: no throat allowed
# SI: required |rho| at 1 m and FR bound at tau0 = 0.01 m / c
quantity("c^4/G / (8 * 3.14159265 * (1 m)^2)", "4.8e42 J/m^3", rel_tol=0.01)
quantity("3 * hbar * c / (32 * 3.14159265^2 * (0.01 m)^4)", "3.0e-20 J/m^3", rel_tol=0.01)
quantity("0.01 m / c", "3.3e-11 s", rel_tol=0.02)
ratio1 = (1 / nFR / 1.616255e-35)**2     # (b0 / b0_max)^2 at b0 = 1 m
print("excess at 1 m:", ratio1, " at 1.5e7 m:", ratio1 * 1.5e7**2)
quantity("(c^4/G / (8 * 3.14159265 * (1 m)^2)) / (3 * hbar * c / (32 * 3.14159265^2 * (0.01 m)^4))", "1.6e62", rel_tol=0.01)
inequality(abs(ratio1 - 1.6e62) / 1.6e62, "<", 0.01)
inequality(abs(ratio1 * 2.25e14 - 3.6e76) / 3.6e76, "<", 0.01)
raise SystemExit(finish())
