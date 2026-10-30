"""M-DIALECTICIAN-05: naive CCHP tensions (F4).

z = |H1 - H2| / sqrt(s1^2 + s2^2), independent Gaussian errors.
CCHP total: 1.22 (stat), 1.33 (sys), 0.70 (SN) in quadrature [D-24]; JWST-only 68.81 +- 1.80 [D-25];
SH0ES 73.49 +- 0.93 [D-20]; CMB-SPA 67.19 +- 0.38 [D-44]. Units km/s/Mpc throughout.
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import limit, inequality, units, finish

# limit: when one error vanishes, z reduces to the single-measurement significance
limit("d/sqrt(a**2 + b**2)", "b", 0, "d/a")

tot = math.sqrt(1.22**2 + 1.33**2 + 0.70**2)
print(f"CCHP total sigma = {tot:.3f}")
inequality(f"abs({tot} - 1.94)", "<=", "0.005")
z = lambda a, sa, b, sb: abs(a - b) / math.hypot(sa, sb)
cases = [("70.39 vs SH0ES", z(70.39, tot, 73.49, 0.93), 1.44), ("70.39 vs SPA", z(70.39, tot, 67.19, 0.38), 1.62),
         ("68.81 vs SH0ES", z(68.81, 1.80, 73.49, 0.93), 2.31), ("68.81 vs SPA", z(68.81, 1.80, 67.19, 0.38), 0.88)]
for name, got, want in cases:
    print(f"{name}: z = {got:.3f} (lens {want})")
    inequality(f"abs({got} - {want})", "<=", "0.006")
units("3.10 km/s/Mpc / (2.15 km/s/Mpc)", "dimensionless")
raise SystemExit(finish())
