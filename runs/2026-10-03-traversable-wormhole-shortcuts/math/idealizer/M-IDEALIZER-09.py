"""M-IDEALIZER-09: payload cap and separation window in the Casimir-balanced long throat.

Assumption (MM's ship-mass condition as the lens uses it): payload m closes the throat once m > |E_neg|,
with |E_neg| = M (r_e/ell)^2 (M-IDEALIZER-08). Then ell <= r_e sqrt(M/m).
Long throat (no shortcut): through-time pi ell / c > d / c, so consistent separations d < pi r_e sqrt(M/m).
Proper crossing time tau ~ pi r_e / c (MM).
Numbers: r_e = 1.5e7 m, M = r_e c^2/G = 2.02e34 kg; human 70 kg: ell_max 2.7e7 ly, d < 8.5e7 ly, tau 0.157 s; 1 kg: d < 7e8 ly.
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, inequality, quantity, units, finish

re, M, m, ell = sp.symbols("r_e M m ell", positive=True)
cap = sp.solve(sp.Eq(M * (re / ell)**2, m), ell)[0]
identity(cap, re * sp.sqrt(M / m))
limit(cap, "m", 0, sp.oo)          # massless payload: no cap
# the cap exceeds r_e whenever m < M
inequality(cap, ">", re, domain={"M": (2, 10), "m": (0.1, 1.9), "r_e": (0.1, 10)})

G = 6.67430e-11; c = 299792458.0; ly = 9.4607304725808e15
r_e = 1.5e7
Mv = r_e * c**2 / G
for mass, claim_ell, claim_d in [(70.0, 2.7e7, 8.5e7), (1.0, None, 7e8)]:
    lmax = r_e * math.sqrt(Mv / mass)
    print(f"m = {mass} kg: ell_max = {lmax:.4g} m = {lmax/ly:.4g} ly; d < pi ell = {math.pi*lmax/ly:.4g} ly")
    if claim_ell:
        quantity(f"{lmax} m", f"{claim_ell} ly", rel_tol=0.02)
    quantity(f"{math.pi*lmax} m", f"{claim_d} ly", rel_tol=0.02)
quantity(f"pi_placeholder" if False else f"{math.pi * r_e} m / c", "0.157 s", rel_tol=0.005)
units("1 m / c", "time")
raise SystemExit(finish())
