"""M-STATISTICIAN-14: precision needed (Precision section; S1, S2, S4 data-needed column). Lifetimes in s, lambda dimensionless.
Separation of a new result sigma from a pole P at the other pole's value: n = Delta/sqrt(sigma^2 + sigma_P^2), Delta = 9.65 s.
Lens: 3.22 / 1.93 s budgets; vs storage 3.19 / 1.88 s; vs proton 2.49 s, 5 sigma impossible; BL2/LiNA 1 s 8.8/4.2;
BL3 0.3 s 18/4.7; UCNProBe 1.5 s 6.2/3.8, 2 s 4.7/3.4; LiNA 7 sigma with proton pole 0.9 s;
BL1-type data max 4.95 sigma; SM route sigma_lambda <= 0.00156 (0.12%) for 5 sigma, 0.00274 for 3 sigma;
Nab: sigma_lambda <= 0.0018 (0.14%) separates aSPECT from PERKEO III at 5 sigma; at 0.0005, ~13 sigma."""
import sys, math
sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/math/statistician")
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from _inputs import *
from math_checks import identity, limit, inequality, finish
import sympy as sp

D = 9.65; sS = 0.43; sB = 2.04
identity(f"{D/3:.2f}", "3.22"); identity(f"{D/5:.2f}", "1.93")
identity(f"{math.sqrt((D/3)**2 - sS**2):.2f}", "3.19"); identity(f"{math.sqrt((D/5)**2 - sS**2):.2f}", "1.88")
identity(f"{math.sqrt((D/3)**2 - sB**2):.2f}", "2.49"); inequality(f"{D/5}", "<", f"{sB}")   # 5 sigma impossible vs proton pole
for lab, s, a, b in [("BL2/LiNA", 1.0, "8.8", "4.2"), ("BL3", 0.3, "18", "4.7"), ("UCNProBe", 1.5, "6.2", "3.8"), ("UCNProBe", 2.0, "4.7", "3.4")]:
    zs, zb = D / q(s, sS), D / q(s, sB); print(f"{lab} {s} s: {zs:.2f} / {zb:.2f} (lens {a} / {b})")
    identity(f"{zs:.2g}" if a == "18" else f"{zs:.1f}", a); identity(f"{zb:.1f}", b)
z = D / q(1.0, 0.9); print("LiNA vs proton pole at 0.9 s", z); identity(f"{z:.0f}", "7")
zf = D / q(1.9, sS); print("BL1-type floor (sys 1.9 s, stat -> 0, gap held at 9.65 s)", zf); identity(f"{zf:.2f}", "4.95")
# SM route: sigma_tau^2 = (dtau/dlam sigma_lam)^2 + sVud^2 + sK^2 + sS^2 <= (D/n)^2
tau0, lam0 = 878.50, 1.27641
dtdl = 6 * lam0 / (1 + 3 * lam0**2) * tau0
sv = 2 * 0.00032 / 0.97361 * tau0; sk = 0.19
for n, lens in [(5, "0.00156"), (3, "0.00274")]:
    sl = math.sqrt((D / n) ** 2 - sv**2 - sk**2 - sS**2) / dtdl
    print(f"{n} sigma: sigma_lambda <= {sl:.5f} (lens {lens}); rel {sl/lam0:.4%}; naive D/n/dtdl = {D/n/dtdl:.5f}")
    identity(f"{sl:.5f}", lens)
# Nab thresholds
dl = 1.27641 - 1.2668; sP3 = q(0.00045, 0.00033)
sN = math.sqrt((dl / 5) ** 2 - sP3**2); print("Nab 5 sigma threshold", sN, sN / 1.2668)
identity(f"{sN:.4f}", "0.0018"); identity(f"{100*sN/1.2668:.2f}", "0.14")
zN = dl / q(0.0005, sP3); print("Nab at 0.0005:", zN); identity(f"{zN:.0f}", "13")
s_ = sp.symbols("s", positive=True)
limit(9.65 / sp.sqrt(s_**2 + sp.Rational(43, 100)**2), "s", 0, "9.65/0.43")
raise SystemExit(finish())
