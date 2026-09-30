"""M-STATISTICIAN-12: heavy tails (F12, candidate E). Two-sided Student-t tail P(|T_nu| > z), z = 4.63;
Gaussian 3.7e-6. Lens: nu = 2, 3, 4 -> 0.044, 0.019, 0.010; 'density ratio 400-1000' (t over Gaussian at the observed z)."""
import sys
sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/math/statistician")
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from _inputs import *
from math_checks import identity, limit, finish
import mpmath as mp
import sympy as sp

def t_pdf(x, nu):
    nu = mp.mpf(nu)
    return mp.gamma((nu + 1) / 2) / (mp.sqrt(nu * mp.pi) * mp.gamma(nu / 2)) * (1 + x**2 / nu) ** (-(nu + 1) / 2)
def t_p2(z, nu):
    return 2 * mp.quad(lambda x: t_pdf(x, nu), [z, mp.inf])
z = mp.mpf("4.63")
# closed form for nu = 2: p2 = 1 - z/sqrt(2 + z^2)
identity(f"{float(t_p2(z, 2)):.12f}", f"{float(1 - z / mp.sqrt(2 + z**2)):.12f}")
gpdf = mp.npdf(z)
for nu, lens in [(2, "0.044"), (3, "0.019"), (4, "0.010")]:
    pv = float(t_p2(z, nu)); r = float(t_pdf(z, nu) / gpdf)
    print(f"nu={nu}: p2 {pv:.4f} (lens {lens}); density ratio t/Gauss at z: {r:.0f}; tail ratio {pv/p2(4.63):.0f}")
    identity(f"{pv:.2g}", lens if lens != "0.010" else "0.01")
# limit: Student-t -> Gaussian as nu -> oo
x, nu = sp.symbols("x nu", positive=True)
limit((1 + x**2 / nu) ** (-(nu + 1) / 2), "nu", sp.oo, "exp(-x**2/2)")
raise SystemExit(finish())
