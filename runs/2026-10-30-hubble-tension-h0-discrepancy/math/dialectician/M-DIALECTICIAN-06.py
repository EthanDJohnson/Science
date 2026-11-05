"""M-DIALECTICIAN-06: required r_d and the M_B offset (F5).

BAO measures h*r_d with h = H0/(100 km/s/Mpc). r_d = (h r_d)/h; sigma(r_d) from h r_d alone = 0.73/h.
DESI DR2 h r_d = 101.54 +- 0.73 Mpc [D-45]; CMB-SPA r_d = 147.00 Mpc [D-44]; DESI+BBN H0 = 68.50.
Ladder relation (brief): 5 log10 H0 = M_B + 5 a_B + 25 => H0 ratio = 10^(0.2 dM_B).
M_B: ladder -19.253, inverse -19.375 (cosmography) / -19.394 (flat LCDM) [D-21].
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import identity, limit, inequality, quantity, units, finish
import sympy as sp

# identity: H0 ratio from the ladder relation (a_B fixed)
M1, M2, a = sp.symbols("M1 M2 a", real=True)
H = lambda M: 10 ** ((M + 5 * a + 25) / 5)
identity(sp.simplify(H(M1) / H(M2)), 10 ** ((M1 - M2) / 5), domain={"M1": (-20, -19), "M2": (-20, -19), "a": (0.6, 0.8)})
# limit: equal M_B gives equal H0
limit(10 ** (sp.Symbol("d") / 5), "d", 0, 1)

quantity("101.54 Mpc / 0.73264", "138.6 Mpc", rel_tol=5e-4)
quantity("0.73 Mpc / 0.73264", "1.0 Mpc", rel_tol=0.01)
rd = 101.54 / 0.73264
cut_spa = 1 - rd / 147.00
rd_bbn = 101.54 / 0.685
cut_bbn = 1 - rd / rd_bbn
print(f"r_d(73.264) = {rd:.2f} Mpc; cut vs 147.00 = {100*cut_spa:.2f}%; r_d(68.50) = {rd_bbn:.2f} Mpc; cut = {100*cut_bbn:.2f}%")
inequality(f"abs({rd_bbn} - 148.2)", "<=", "0.06")
inequality(f"abs({100*cut_spa} - 5.7)", "<=", "0.05")
inequality(f"abs({100*cut_bbn} - 6.5)", "<=", "0.05")
d1 = -19.253 - (-19.375); d2 = -19.253 - (-19.394)
r1 = 10 ** (0.2 * d1); r2 = 10 ** (0.2 * d2)
print(f"dM_B = {d1:.3f}, {d2:.3f} mag -> H0 ratio {r1:.4f}, {r2:.4f}")
inequality(f"abs({r1} - 1.058)", "<=", "0.0006")
inequality(f"abs({r2} - 1.067)", "<=", "0.0006")
# sign: ladder M_B is less negative (fainter-calibrated larger), so ladder H0 is higher: ratio > 1
inequality(f"{r1}", ">", "1")
units("101.54 Mpc / 0.73264", "length")
raise SystemExit(finish())
