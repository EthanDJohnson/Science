"""M-ENGINEER-06 (F11): assembly heat ~ G M^2/Rbar with Rbar = 15 m (mid-wall), M = 4.51e27 kg:
9e43 J = 0.22 Mc^2 = 1.5e23 world-years (5.9e20 J/yr). Newtonian estimate. Cross-check against the exact
Newtonian self-energy of a uniform shell R1 = 10 m .. R2 = 20 m, U = Int_R1^R2 G m(r) 4 pi r^2 rho / r dr,
whose thin-shell limit is G M^2/(2R) and whose solid-sphere limit is 3GM^2/(5R)."""
import sys
import sympy as sp
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-01-warp-drive-without-negative-energy/math/engineer")
from common import *
from math_checks import identity, limit, quantity, finish

M, Rb = 4.511e27, 15.0
E = G * M**2 / Rb
rel("G M^2/Rbar (J)", E, 9e43, 0.02)
near("E/(M c^2)", E / (M * c**2), 0.22, 0.01)
rel("world-years", E / WORLD_YR, 1.5e23, 0.03)
quantity("G*(4.511e27 kg)^2/(15 m)", "9.05e43 J", rel_tol=0.01)
# exact uniform-shell Newtonian binding energy
r, a, b, Mm, Gg = sp.symbols("r a b M G_g", positive=True)
rho = 3 * Mm / (4 * sp.pi * (b**3 - a**3))
m = Mm * (r**3 - a**3) / (b**3 - a**3)
U = sp.simplify(sp.integrate(Gg * m * 4 * sp.pi * r**2 * rho / r, (r, a, b)))
limit(U.subs(a, 0) * b / (Gg * Mm**2), "b", 1, sp.Rational(3, 5))   # solid sphere
x = sp.symbols("x", positive=True)
limit(sp.simplify(U.subs(b, a * (1 + x)) * a / (Gg * Mm**2)), "x", 0, sp.Rational(1, 2))   # thin shell
Uex = float(U.subs({Gg: G, Mm: M, a: 10, b: 20}))
print(f"  exact uniform-shell Newtonian U = {Uex:.4g} J = {Uex/(M*c**2):.4f} Mc^2 (lens estimate 9e43 J)")
inequality(repr(abs(math.log10(Uex / E))), "<=", "0.3")   # same order
# GR: proper mass of the uniform shell minus its gravitating mass (static TOV shell, M = 4.49e27 kg)
import mpmath as mp
Mp, a_, b_ = 4.49e27, 10.0, 20.0
rho0 = 3 * Mp / (4 * math.pi * (b_**3 - a_**3))
mr = lambda x: Mp * (x**3 - a_**3) / (b_**3 - a_**3)
Mprop = mp.quad(lambda x: 4 * math.pi * x**2 * rho0 / mp.sqrt(1 - 2 * G * mr(x) / (c**2 * x)), [a_, b_])
dE = float(Mprop - Mp) * c**2
print(f"  GR proper-mass deficit (M_proper - M) c^2 = {dE:.4g} J = {dE/(Mp*c**2):.4f} Mc^2; world-years {dE/WORLD_YR:.3g}")
inequality(repr(abs(math.log10(dE / E))), "<=", "0.3")
# weak-field limit: proper-mass deficit -> Newtonian U
Mw = 4.49e17
mrw = lambda x: Mw * (x**3 - a_**3) / (b_**3 - a_**3)
rw = 3 * Mw / (4 * math.pi * (b_**3 - a_**3))
dEw = float(mp.quad(lambda x: 4 * math.pi * x**2 * rw * (1 / mp.sqrt(1 - 2 * G * mrw(x) / (c**2 * x)) - 1), [a_, b_])) * c**2
Uw = float(U.subs({Gg: G, Mm: Mw, a: 10, b: 20}))
rel("weak-field: GR deficit vs Newtonian U", dEw, Uw, 1e-3)
raise SystemExit(finish())
