"""M-CONSTRAINTS-13: Zych clock-interferometer visibility and Pikovski decoherence times (SI).

Zych: arms at heights differing by dh for time T: dtau = g dh T/c^2; a two-level clock with gap hbar omega in
(|0>+|1>)/sqrt2 has visibility V = |cos(omega dtau/2)|. Claims: dtau = 1.1e-18, 1.1e-17, 5.5e-17 s for
dh = 0.01, 0.1, 0.5 m (T = 1 s); V = 1.00000, 0.99989, 0.99730 for omega = 2 pi 429 THz.
Pikovski (dossier Q-07): tau_dec = sqrt(2/N) hbar c^2/(kB T g dx). Claims: 1.04e-3 s (N = 1e23, T = 300 K, dx = 1 um);
2.6e7 s (N = 6000, 500 K, 0.1 um); 3.2e2 s (diamond 1e-14 kg, N = 3 x atoms, 1 K, dx = 250 um).
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import math
import sympy as sp
from math_checks import identity, limit, quantity, units, finish

# visibility identity: |(1 + e^{i x})/2| = |cos(x/2)| for real x
x = sp.symbols("x", real=True)
identity(sp.sqrt(((1 + sp.cos(x)) / 2) ** 2 + (sp.sin(x) / 2) ** 2), sp.Abs(sp.cos(x / 2)), domain={"x": (-3, 3)})
limit("cos(x/2)", "x", 0, "1")
g, c, w = 9.80665, 299792458.0, 2 * math.pi * 429e12
for dh, dt_exp, V_exp in [(0.01, 1.1e-18, 1.00000), (0.1, 1.1e-17, 0.99989), (0.5, 5.5e-17, 0.99730)]:
    quantity(f"g0 * {dh} m * 1 s / c^2", f"{dt_exp} s", rel_tol=0.01)
    dtau = g * dh / c**2
    V = abs(math.cos(w * dtau / 2))
    print(f"dh={dh}: dtau={dtau:.4e} s, V={V:.6f}")
    quantity(f"{V}", f"{V_exp}", rel_tol=1e-5)
units("g0 * 1 m * 1 s / c^2", "s")
tau = "(2/{N})^0.5 * hbar * c^2 / (kB * {T} K * g0 * {dx} m)"
units(tau.format(N=1e23, T=300, dx=1e-6), "s")
quantity(tau.format(N=1e23, T=300, dx=1e-6), "1.04e-3 s", rel_tol=0.01)
quantity(tau.format(N=6000, T=500, dx=1e-7), "2.6e7 s", rel_tol=0.02)
Ndia = 3 * 1e-14 / (12.011 * 1.66053906660e-27)
print("diamond modes N =", Ndia)
quantity(tau.format(N=Ndia, T=1, dx=250e-6), "3.2e2 s", rel_tol=0.02)
raise SystemExit(finish())
