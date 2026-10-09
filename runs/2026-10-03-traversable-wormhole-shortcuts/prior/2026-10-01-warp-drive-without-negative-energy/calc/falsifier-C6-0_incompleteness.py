#!/usr/bin/env python3
"""Falsifier C6-0, branch (b): what does breaking null completeness buy?

Units: geometric (G = c = 1), lengths in metres; delays in metres of light travel.

Test spacetime: Schwarzschild with mass parameter M of either sign (M < 0: naked singularity at r = 0,
null geodesically incomplete, so Gao-Wald's completeness hypothesis fails).
 1. gr_tensors: G_ab = 0 identically for any sign of M -> pointwise NEC/WEC hold trivially on r > 0.
 2. Kretschmann 48 M^2/r^6 -> diverges at r = 0 (incomplete, singular).
 3. Exact light-travel coordinate time from x=-D to x=+D at closest approach r0, versus flat 2 sqrt(D^2-b^2)
    at the same impact parameter b (b = r0/sqrt(f(r0))). Sign gives delay (+) or advance (-).
 4. Komar mass on every sphere = M: for M < 0 the 'source' is a distributional negative energy at r = 0
    (in the linearized/distributional sense, T_00 = M delta^3). So the advance comes with negative energy
    hidden in the singularity, which the brief counts ("including distributional contributions").
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
import numpy as np
from scipy.integrate import quad
from gr_tensors import Spacetime

t, r, th, ph = sp.symbols("t r theta phi", real=True)
M = sp.symbols("M", real=True)
f = 1 - 2 * M / r
st = Spacetime(sp.diag(-f, 1 / f, r**2, r**2 * sp.sin(th) ** 2), [t, r, th, ph], simplify=True)
G = st.einstein()
allzero = all(sp.simplify(G[i, j]) == 0 for i in range(4) for j in range(4))
print(("PASS" if allzero else "FAIL") + " Einstein tensor vanishes identically for real M of either sign (vacuum, NEC holds pointwise on r>0)")
Rm = st.riemann()  # R^a_bcd
ginv = st.ginv
g = st.g
# Kretschmann: R_abcd R^abcd
K = 0
for a in range(4):
    for b in range(4):
        for c in range(4):
            for d in range(4):
                if Rm[a][b][c][d] == 0 if isinstance(Rm, list) else Rm[a, b, c, d] == 0:
                    continue
                Rabcd = Rm[a][b][c][d] if isinstance(Rm, list) else Rm[a, b, c, d]
                # raise/lower with diagonal metric: R_abcd R^abcd = sum g_aa g^bb g^cc g^dd (R^a_bcd)^2
                K += g[a, a] * ginv[b, b] * ginv[c, c] * ginv[d, d] * Rabcd**2
K = sp.simplify(K)
print(f"INFO Kretschmann = {K}  (diverges at r=0 for M != 0)")

def delay(Mv, r0, D):
    fr = lambda rr: 1 - 2 * Mv / rr
    b = r0 / np.sqrt(fr(r0))
    # dt/dr = 1/(f sqrt(1 - b^2 f / r^2)); substitute r = r0 + u^2 to remove endpoint singularity
    def integrand(u):
        rr = r0 + u * u
        arg = 1 - b * b * fr(rr) / rr**2
        return 2 * u / (fr(rr) * np.sqrt(arg))
    T = 2 * quad(integrand, 0, np.sqrt(D - r0), limit=400, epsabs=1e-12, epsrel=1e-12)[0]
    flat = 2 * np.sqrt(D * D - b * b)
    return T - flat, b

print("\nM (m)     r0 (m)   D (m)     impact b (m)   delay T - T_flat (m)   weak-field 4M ln(2D/b) (m)")
res = {}
for Mv in (+1.0, -1.0):
    for r0 in (10.0, 100.0):
        for D in (1e4, 1e6):
            dly, b = delay(Mv, r0, D)
            res[(Mv, r0, D)] = dly
            print(f"{Mv:+5.1f}   {r0:7.1f}  {D:8.0e}   {b:10.3f}     {dly:+14.4f}          {4*Mv*np.log(2*D/b):+10.4f}")
adv = all(res[k] < 0 for k in res if k[0] < 0)
dl = all(res[k] > 0 for k in res if k[0] > 0)
print(("PASS" if adv else "FAIL") + " M<0 (incomplete, pointwise vacuum): every ray is ADVANCED relative to flat light")
print(("PASS" if dl else "FAIL") + " M>0: every ray is delayed (Shapiro)")
# Komar mass of a sphere for static metric with Killing xi = d_t: M_K = r^2 f'(r)/2 = M for all r
Mk = sp.simplify(r**2 * sp.diff(f, r) / 2)
print(f"INFO Komar mass on every sphere r: {Mk}  -> the enclosed (distributional) source has mass M; negative when M<0")
