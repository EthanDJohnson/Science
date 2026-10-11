"""M-MECHANIST-01: v_c(s) = sqrt(G M / s), M = 1.5 Msun (SI), and fixed-km/s kicks in ṽ units.
Lens (F2): v_c = 0.816/0.516/0.365/0.258/0.211 km/s at s = 2/5/10/20/30 kau; 0.1 km/s = 0.12 v_c (2 kau),
0.39 v_c (20 kau); 0.5 km/s = 0.61 v_c (2 kau), 1.94 v_c (20 kau); kick in ṽ units grows as sqrt(s)."""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import quantity, units, identity, limit, finish
GM_sun = 1.3271244e20  # m^3 s^-2 (IAU nominal)
AU = 1.495978707e11    # m
M = 1.5
lens_vc = {2: 0.816, 5: 0.516, 10: 0.365, 20: 0.258, 30: 0.211}
for s_kau, v_l in lens_vc.items():
    vc = math.sqrt(GM_sun * M / (s_kau * 1e3 * AU)) / 1e3
    print(f"s = {s_kau} kau: v_c = {vc:.4f} km/s (lens {v_l})")
    quantity(f"(G*1.5*Msun/({s_kau}e3 au))^0.5", f"{v_l} km/s", rel_tol=2e-3)
units("(G*1.5*Msun/(2e3 au))^0.5", "m/s")
for kick, s_kau, lens in [(0.1, 2, 0.12), (0.1, 20, 0.39), (0.5, 2, 0.61), (0.5, 20, 1.94)]:
    vc = math.sqrt(GM_sun * M / (s_kau * 1e3 * AU)) / 1e3
    r = kick / vc
    print(f"kick {kick} km/s at {s_kau} kau = {r:.3f} v_c (lens {lens})")
    assert abs(r - lens) < 0.006, (r, lens)
# scaling: kick/v_c(s) = kick*sqrt(s/(G M)) -> ratio between s2 and s1 is sqrt(s2/s1)
k, s, G, Mm = sp.symbols("k s G M", positive=True)
identity((k / sp.sqrt(G * Mm / (10 * s))) / (k / sp.sqrt(G * Mm / s)), sp.sqrt(10))
limit(k / sp.sqrt(G * Mm / s), "s", 0, "0")  # small-separation limit: kick negligible
print("PASS-like: arithmetic asserts passed")
raise SystemExit(finish())
