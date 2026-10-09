"""M-DIALECTICIAN-08: EDM scale arithmetic (F10). Quoted inputs: Kain R0/l_P = 75.28..498.4 (Q-18),
mu_bar = 0.2 (read as fermion mass in Planck units, lens's interpretation), Ford-Roman bound
l_P/(2 f^2) at f = 0.01 (Q-20, literature form, not re-derived). SI units via unit_tools (CODATA 2018).
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import quantity, identity, units, finish
from unit_tools import Q

lP = Q("(hbar*G/c^3)^0.5")
mP = Q("(hbar*c/G)^0.5")
print("l_P =", lP.to("m"), "m;  m_P =", mP.to("kg"), "kg")
quantity("75.28 * (hbar*G/c^3)^0.5", "1.2e-33 m", rel_tol=0.02)
quantity("498.4 * (hbar*G/c^3)^0.5", "8.1e-33 m", rel_tol=0.01)
fr = 1 / (2 * 0.01**2)
print("Ford-Roman l_P/(2 f^2) at f=0.01:", fr, "l_P =", fr * lP.to("m"), "m")
quantity("(hbar*G/c^3)^0.5 / (2 * 0.01^2)", "8.1e-32 m", rel_tol=0.01)
ratio = 498.4 / fr
print("largest throat / bound =", ratio)
identity(f"{ratio:.4f}", "0.0997")
quantity("0.2 * (hbar*c/G)^0.5", "4.35e-9 kg", rel_tol=0.005)
quantity("0.2 * (hbar*c/G)^0.5 / (9.1093837015e-31 kg)", "4.78e21", rel_tol=0.01)
quantity("(9.1093837015e-31 kg / (hbar*c/G)^0.5)^2", "1.75e-45", rel_tol=0.01)
units("(9.1093837015e-31 kg / (hbar*c/G)^0.5)^2", "dimensionless")
alpha = 7.2973525693e-3
print("sqrt(alpha) =", math.sqrt(alpha))
identity(f"{math.sqrt(alpha):.3f}", "0.085")
raise SystemExit(finish())
