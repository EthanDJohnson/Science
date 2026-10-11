"""M-DIALECTICIAN-03 (F5, F7, F8): Gamma = log10 sqrt(gamma)  =>  gamma = 10^(2 Gamma).
Lens values: 0.068 -> 1.368; 0.042/0.057/0.085 -> 1.21/1.30/1.48; 0.102/0.132 -> 1.60/1.84."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, quantity, finish

Gm, gm = sp.symbols("Gm gm", positive=True)
identity(sp.log(sp.sqrt(10 ** (2 * Gm)), 10), Gm, domain={"Gm": (-0.5, 0.5)})   # inverse map round-trips
limit(10 ** (2 * Gm), "Gm", 0, 1)                                                     # Gamma = 0 is Newton
for G_, lens in ((0.068, 1.368), (0.042, 1.21), (0.057, 1.30), (0.085, 1.48), (0.102, 1.60), (0.132, 1.84)):
    val = 10 ** (2 * G_)
    print(f"Gamma={G_}: gamma={val:.4f}; lens {lens}")
    quantity(f"{val}", f"{lens}", rel_tol=0.004)
raise SystemExit(finish())
