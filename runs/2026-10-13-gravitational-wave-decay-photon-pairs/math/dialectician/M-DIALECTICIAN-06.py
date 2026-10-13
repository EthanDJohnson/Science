"""M-DIALECTICIAN-06: chirped-bin total and the over-count of B&O's bin recipe (F5).

Natural units. Rate R(sigma) = c G^2 N^2 w^3 sigma^2 (c = 3/(25 pi)); transform-limited top hat
total P_TL = R T_eff, T_eff = 4 pi/(3 sigma) (M-02); chirp factor 3 pi/(sigma t_b) for
sigma t_b >> 1 (M-05). Claim: P = 4 pi^2 c G^2 N^2 w^3 / t_b; B&O's Y = R(sigma_b) t_b;
Y/P = (sigma_b t_b/(2 pi))^2. Numbers: sigma_b = eps w, eps = 0.1:
GW170817 100 Hz, t_b = 0.60 s -> sigma_b t_b = 37.7, Y/P = 36; WD 6.2 mHz, t_b = 1e13 s -> 3.8e19.
Also K3: n equal bins each N/n, sigma/n, t/n: sum of yields = c N^2 sigma^2 t / n^4.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, quantity, inequality, finish

c, G, N0, w, s, tb, n, t = sp.symbols("c G N0 w s t_b n t", positive=True)
R = c * G**2 * N0**2 * w**3 * s**2
P_TL = R * 4 * sp.pi / (3 * s)
P = P_TL * 3 * sp.pi / (s * tb)
identity(P, 4 * sp.pi**2 * c * G**2 * N0**2 * w**3 / tb)
Y = R * tb
identity(Y / P, (s * tb / (2 * sp.pi)) ** 2)
# consistency limit: at the edge sigma t_b = 2 pi the two agree
identity((Y / P).subs(tb, 2 * sp.pi / s), 1)
# n-bin sum
Rbin = c * G**2 * (N0 / n) ** 2 * w**3 * (s / n) ** 2
identity(n * Rbin * t / n, c * G**2 * N0**2 * w**3 * s**2 * t / n**4)
# numbers (SI frequencies, rad/s; t_b in s; dimensionless product)
import math
for label, f, tbv, exp in (("GW170817 100 Hz", 100.0, 0.60, 36.0), ("WD 6.2 mHz", 6.2e-3, 1e13, 3.8e19)):
    sb = 0.1 * 2 * math.pi * f
    st = sb * tbv
    ratio = (st / (2 * math.pi)) ** 2
    print(f"{label}: sigma_b = {sb:.4e} rad/s, sigma_b t_b = {st:.4e}, Y/P = {ratio:.4e}")
    quantity(f"{ratio}", f"{exp}", rel_tol=2e-2)
quantity(f"{0.1*2*math.pi*100*0.60}", "37.7", rel_tol=2e-3)
raise SystemExit(finish())
