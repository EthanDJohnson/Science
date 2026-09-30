"""M-STATISTICIAN-01: class means (F3).
Claim: inverse-variance mean m = sum(w_i x_i)/sum(w_i), w_i = 1/sigma_i^2, sigma_m = (sum w_i)^-1/2,
chi2 = sum w_i (x_i - m)^2, PDG scale S = sqrt(chi2/(N-1)) if > 1. Lifetimes in s (SI).
Lens: proton 887.97 +- 2.04 (chi2 0.08/1); material 880.03 +- 0.49 (0.70 scaled), 8.19/4 p=0.085, S=1.43;
magnetic 877.82 +- 0.27, 0.09/2; storage 878.32 +- 0.23 (0.43 scaled), 24.0/7 p=0.0011, S=1.85;
J-PARC +4.35/-3.98."""
import sys
sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/math/statistician")
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from _inputs import *
from math_checks import identity, limit, quantity, finish
import sympy as sp

# symbolic: two-point weighted mean has the right limits
x1, x2, s1, s2 = sp.symbols("x1 x2 s1 s2", positive=True)
m2 = (x1 / s1**2 + x2 / s2**2) / (1 / s1**2 + 1 / s2**2)
limit(m2, "s2", sp.oo, "x1")          # a result with infinite error drops out
identity(m2.subs(s2, s1), "(x1+x2)/2")  # equal errors -> arithmetic mean
# units: mean of seconds is seconds
quantity("887.7 s * 0.5 + 889.2 s * 0.5", "888.45 s")

res = {}
for name, rows, lens in [("proton", PROTON, (887.97, 2.04, 0.08, 1)),
                         ("material", MATERIAL, (880.03, 0.49, 8.19, 4)),
                         ("magnetic", MAGNETIC, (877.82, 0.27, 0.09, 2)),
                         ("storage", STORAGE, (878.32, 0.23, 24.0, 7))]:
    m, s, c, d, S = wmean(rows)
    res[name] = (m, s, c, d, S)
    print(f"{name}: mean {m:.3f} s, err {s:.3f} s, scaled {s*S:.3f} s, chi2 {c:.3f}/{d}, p {chi2_sf(c,d):.4g}, S {S:.3f}  (lens {lens})")
    identity(f"{m:.2f}", f"{lens[0]}")
    identity(f"{s:.2f}", f"{lens[1]}")
    identity(f"{round(c, 2 if c < 10 else 1)}", f"{lens[2]}")

identity(f"{res['material'][4]:.2f}", "1.43")
identity(f"{res['material'][1]*res['material'][4]:.2f}", "0.70")
identity(f"{res['storage'][4]:.2f}", "1.85")
identity(f"{res['storage'][1]*res['storage'][4]:.2f}", "0.43")
identity(f"{chi2_sf(*res['material'][2:4]):.3f}", "0.085")
identity(f"{chi2_sf(*res['storage'][2:4]):.4f}", "0.0011")
# BL1 weight share
wb = 1 / BL1[2]**2; ws = 1 / SUS[2]**2
print("BL1 weight share", wb / (wb + ws))
identity(f"{wb/(wb+ws):.2f}", "0.82")
# J-PARC asymmetric totals
identity(f"{JP_UP:.2f}", "4.35"); identity(f"{JP_DN:.2f}", "3.98")
# Pattie 18 omitted: storage mean shift
m7 = wmean([r for r in STORAGE if r[0] != "Pattie18"])[0]
print("storage without Pattie18 shift", m7 - res["storage"][0])
identity(f"{m7-res['storage'][0]:.2f}", "0.06")
raise SystemExit(finish())
