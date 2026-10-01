"""M-STATISTICIAN-13: Sellke-Bayarri-Berger bound B_min = -e p ln p (p < 1/e) and Gaussian bound exp(-z^2/2);
prior needed for posterior 50%: prior odds = B_min, prior = B_min/(1+B_min). Dimensionless.
Lens: S1 (p 3.7e-6) max odds 8.0e3 (7969), Gaussian bound 2.2e-5, prior 1.3e-4; S2 (2.24 sigma) 4:1, prior 0.20;
S3 (2.95 sigma) 20:1, prior 0.047; S4 (3.49 sigma) 100:1, prior 0.010; S7 (p 0.155) 1.3:1."""
import sys, math
sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/math/statistician")
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from _inputs import *
from math_checks import identity, limit, inequality, finish
import sympy as sp

pp = sp.symbols("p", positive=True)
limit(-sp.E * pp * sp.log(pp), "p", 0, "0")
limit(-sp.E * pp * sp.log(pp), "p", sp.exp(-1), "1")   # bound reaches 1 at p = 1/e
inequality(-sp.E * pp * sp.log(pp), "<=", "1", domain={"p": (1e-9, 0.3678)})
def B(p): return -math.e * p * math.log(p)
z1 = (wmean(PROTON)[0] - wmean(STORAGE)[0]) / q(wmean(PROTON)[1], wmean(STORAGE)[1] * wmean(STORAGE)[4])
for lab, p, lo, lpr in [("S1", p2(z1), "8.0e+03", "1.3e-04"), ("S2", p2(2.24), "4", "0.20"), ("S3", p2(2.95), "20", "0.047"),
                         ("S4", p2(3.49), "1e+02", "0.010"), ("S7", 0.155, "1.3", None)]:
    b = B(p); odds = 1 / b; prior = b / (1 + b)
    print(f"{lab}: p {p:.3g}, max odds {odds:.4g} (lens {lo}), prior needed {prior:.3g} (lens {lpr})")
    identity(f"{odds:.2g}", lo)
    if lpr: identity(f"{prior:.2g}", lpr)
print("Gaussian bound exp(-z^2/2):", math.exp(-z1**2 / 2)); identity(f"{math.exp(-z1**2/2):.1e}", "2.2e-5")
raise SystemExit(finish())
