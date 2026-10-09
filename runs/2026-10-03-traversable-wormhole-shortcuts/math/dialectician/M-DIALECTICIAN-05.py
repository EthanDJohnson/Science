"""M-DIALECTICIAN-05: enhancement of the time-advancing chirality at the shortcut onset.

From M-04: enhancement = (L/(L - Delta))^2. Loop of light-length L = T_thru + d (throat then exterior),
offset at onset Delta_s = T_thru - d  =>  L - Delta_s = 2d. With T_thru = pi*ell (MM, c = 1):
d = ell, ell/3, ell/30. Dimensionless.
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, finish

T, d = sp.symbols("T d", positive=True)
enh = ((T + d) / ((T + d) - (T - d)))**2
identity(enh, ((T + d) / (2 * d))**2)
# limit d -> T (wormhole no longer long, Delta_s -> 0): enhancement -> 1
limit(enh, "d", T, "1", domain={"T": (1, 10), "d": (0.1, 10)})
ell = 1.0
for frac, claim in [(1, 4.288), (1 / 3, 27.17), (1 / 30, 2268)]:
    dv = frac * ell
    val = ((math.pi * ell + dv) / (2 * dv))**2
    print(f"d = ell*{frac:.4g}: enhancement = {val:.6g} (claim {claim})")
    identity(f"{val:.4g}", f"{claim:.4g}")
raise SystemExit(finish())
