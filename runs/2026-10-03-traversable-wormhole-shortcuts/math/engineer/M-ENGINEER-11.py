"""M-ENGINEER-11: FGM 2019 support numbers.
(a) Schwarzschild Hawking temperature T_H = hbar c^3/(8 pi G M kB) equals 2.725 K at M = hbar c^3/(8 pi G kB 2.725 K).
(b) Two extremal holes of mass M and opposite charge at separation d >> GM/c^2: Newtonian attraction
G M^2/d^2 plus Coulomb attraction Q^2/(4 pi eps0 d^2) = G M^2/d^2 (extremal) = 2 G M^2/d^2.
A string of tension mu c^2 balancing it: G mu/c^2 = 2 (G M/(c^2 d))^2.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, quantity, units, finish

M, Gs, c, d, eps0 = sp.symbols("M G c d eps0", positive=True)
Q2 = 4 * sp.pi * eps0 * Gs * M**2                  # extremal Q^2
Fnet = Gs * M**2 / d**2 + Q2 / (4 * sp.pi * eps0 * d**2)
mu = Fnet / c**2                                    # tension mu c^2 = force
identity(Gs * mu / c**2, 2 * (Gs * M / (c**2 * d))**2)
identity((Gs * mu / c**2).subs(d, 1000 * Gs * M / c**2), sp.Rational(2, 10**6))
limit(Gs * mu / c**2, "d", "oo", "0")
units("c^4/G", "force")
quantity("hbar*c^3/(8*pi*G*kB*2.725 K)", "4.5e22 kg", rel_tol=1e-2)
units("hbar*c^3/(8*pi*G*kB*1 K)", "mass")
raise SystemExit(finish())
