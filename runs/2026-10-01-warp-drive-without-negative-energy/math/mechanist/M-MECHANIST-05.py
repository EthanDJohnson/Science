"""M-MECHANIST-05: DEC-necessary ceiling |T^{0x}| <= eps for the published shell profile.

DEC: for an Eulerian observer the energy flux must be causal, so |j| <= rho (necessary).
Linear flat-slice j_x (own derivation, M-MECHANIST-01), geometric -> SI: T^{0x} c-units [J/m^3]
= j_geo c^4/G. Worst ratio over r in the wall and all angles; claimed 18.6 beta at r = 12.2 m,
so ceiling 1/18.6 = 0.054.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
from math_checks import quantity, inequality, finish
from warp_shell import build_shell, shift_profile, G, C

sh = build_shell(4.49e27, 10.0, 20.0, beta_warp=0.0)
r = np.linspace(10.0 + 1e-6, 20.0 - 1e-6, 200001)
S = shift_profile(r, 10.0, 20.0)
dS = np.gradient(S, r)
d2S = np.gradient(dS, r)
eps = np.interp(r, sh.r, sh.eps)
mu = np.linspace(-1, 1, 401)
jmax = np.zeros_like(r)
for k in range(len(r)):
    jx = (d2S[k] * (1 - mu**2) + dS[k] * (1 + mu**2) / r[k]) / (16 * np.pi)  # per unit beta
    jmax[k] = np.abs(jx).max()
ratio = jmax * C**4 / G / np.where(eps > 0, eps, np.inf)
k = int(np.argmax(ratio))
print(f"worst |T0x|/eps per unit beta = {ratio[k]:.3f} at r = {r[k]:.3f} m; eps there = {eps[k]:.3e} J/m^3")
print(f"ceiling beta = {1/ratio[k]:.4f}; at 0.02: {0.02*ratio[k]:.3f}; at 0.04: {0.04*ratio[k]:.3f}")
# where is eps tiny? check edges
for rr in [10.5, 11, 12.2, 15, 18, 19.5]:
    kk = np.searchsorted(r, rr)
    print(f"  r={rr}: ratio/beta={ratio[kk]:.3f}, eps={eps[kk]:.3e}")
quantity(f"{ratio[k]} m/m", "18.6 m/m", rel_tol=0.03)
quantity(f"{r[k]} m", "12.2 m", rel_tol=0.02)
quantity(f"{1/ratio[k]} m/m", "0.054 m/m", rel_tol=0.03)
# DEC necessary condition illustration: rho=1, j=a -> causal flux iff a<=1 ; type-I check of T = [[rho, j],[j, p]]
inequality("rho - j", ">=", "0", domain={"rho": (1, 2), "j": (0, 1)})
raise SystemExit(finish())
