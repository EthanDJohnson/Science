"""M-MECHANIST-03 (F4, O3): ratios of the needed 10.15 s to BL1 budget items (D-20, D-21). s (SI)."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import quantity, identity, finish

gap = 887.97 - 877.82
items = {"fluence 2013 unc": (0.5, 20), "non-fluence lump": (1.7, 6), "nonlinearity unc": (0.8, 12.7),
         "halo unc": (1.0, 10), "backscatter": (0.4, 25), "Si scattering": (0.5, 20),
         "nonlinearity correction": (5.3, 1.9), "6Li absorption correction": (5.4, 1.9)}
for name, (val, claim) in items.items():
    ratio = gap / val
    print(f"{name}: {gap:.2f}/{val} = {ratio:.3f} (lens {claim})")
    quantity(f"{ratio}", f"{claim}", rel_tol=0.03)
# sign flip of a 5.3 s correction moves tau by 2*5.3 s
print(f"sign flip of nonlinearity: {2*5.3} s; of absorption: {2*5.4} s")
quantity(f"{2*5.3} s", "10.6 s", rel_tol=1e-6)
# 2013 recalibration +1.4 s relative to 886.3 s
print(f"recalibration: 1.4/886.3 = {1.4/886.3*100:.3f} %")
quantity(f"{1.4/886.3}", "0.0016", rel_tol=0.02)
# 0.5 s as fraction of tau (O3 row 1: 0.056 %)
quantity(f"{0.5/887.7}", "0.00056", rel_tol=0.02)
identity("g/(g/k)", "k")
raise SystemExit(finish())
