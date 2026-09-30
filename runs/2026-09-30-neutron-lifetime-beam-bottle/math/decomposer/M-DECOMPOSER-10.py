"""M-DECOMPOSER-10 (F10): lambda precision for the SM prediction alone to separate 877.8 s from 887.7 s.
Condition: Delta / sqrt((|dtau/dlam| s_lam)^2 + s_fix^2) >= n, s_fix = 0.61 s (Vud + RC), Delta = 9.88 s.
=> s_lam <= sqrt((Delta/n)^2 - s_fix^2) / |dtau/dlam|. Nab: s_lam = 0.04% |lam|. SI (s)."""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/math/decomposer")
import sympy as sp
from math_checks import identity, limit, finish
from _inputs import near, q
from _sm import *

lP = LAM["PERKEO III"][0]; t = tau_beta(lP, C=C_TAN)
d = abs(dtau_dlam(lP, t))
print(f"|dtau/dlam| at PERKEO III = {d:.1f} s per unit lambda")
D = 887.7 - 877.82
for n, want in ((3, 0.0028), (5, 0.0016)):
    s = math.sqrt((D / n) ** 2 - 0.61 ** 2) / d
    print(f"{n} sigma: s_lam <= {s:.5f} ({s/lP*100:.3f}% relative)")
    near(f"s_lam at {n} sigma", s, want, 0.00006)
s3 = math.sqrt((D / 3) ** 2 - 0.61 ** 2) / d; s5 = math.sqrt((D / 5) ** 2 - 0.61 ** 2) / d
near("3 sigma relative (%)", s3 / lP * 100, 0.22, 0.006); near("5 sigma relative (%)", s5 / lP * 100, 0.13, 0.006)
nab = 0.0004 * 1.2668
print(f"Nab s_lam = {nab:.6f}; 0.0094/s = {0.0094/nab:.2f}; with the A-route 0.00050 in quadrature {0.0094/q(nab,0.0005):.2f}")
near("Nab separation", 0.0094 / nab, 18, 0.6)
# symbolic: the derivative and the lambda -> 0 limit of dtau/dlam
C, v, l = sp.symbols("C v l", positive=True)
tau = C / (v ** 2 * (1 + 3 * l ** 2))
identity(sp.diff(tau, l), -tau * 6 * l / (1 + 3 * l ** 2))
limit(sp.diff(tau, l), "l", 0, "0")
raise SystemExit(finish())
