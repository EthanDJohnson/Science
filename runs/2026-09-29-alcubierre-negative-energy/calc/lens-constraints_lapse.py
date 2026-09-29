"""Constraints lens: Loup-Waite-Halerewicz-type lapse. Metric ds^2 = -A^2 dt^2 + (dx - v f dt)^2 + dy^2 + dz^2 with
A = 1 + (A0 - 1) g(r), g a tanh top hat of radius RA enclosing the Alcubierre wall (R = 1, sigma = 8).
Geometric units (G = c = 1, metres). Computes:
 1. total / negative / positive Eulerian energy on the t = 0 slice vs A0 (n and 1.5n),
 2. the lapse bump alone (v = 0): Eulerian rho (should be 0) and energy-condition scan (the stresses it needs).
"""
import math
import sys
import time

import numpy as np
import sympy as sp

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from gr_tensors import Spacetime  # noqa: E402

T0 = time.time()
t, x, y, z = sp.symbols("t x y z", real=True)
v, R, sg, A0, RA, sA = sp.symbols("v R sigma A0 R_A sigma_A", positive=True)
f, g = sp.Function("f"), sp.Function("g")
xi = x - v * t
rs = sp.sqrt(xi**2 + y**2 + z**2)
A = 1 + (A0 - 1) * g(rs)
st = Spacetime.from_adm(A, [-v * f(rs), 0, 0], sp.eye(3), [t, x, y, z])
rr = sp.symbols("r", positive=True)
topf = sp.Lambda(rr, (sp.tanh(sg * (rr + R)) - sp.tanh(sg * (rr - R))) / (2 * sp.tanh(sg * R)))
topg = sp.Lambda(rr, (sp.tanh(sA * (rr + RA)) - sp.tanh(sA * (rr - RA))) / (2 * sp.tanh(sA * RA)))
funcs = {f: topf, g: topg}
rho = st.energy_density()
print(f"setup {time.time()-T0:.0f}s", flush=True)

print("=== 1. Eulerian energy vs lapse height A0 (R=1, sigma=8, v=1; lapse bump R_A=1.6, sigma_A=4) ===")
for a0 in (1.0, 3.0, 10.0):
    p = {v: 1.0, R: 1.0, sg: 8.0, A0: a0, RA: 1.6, sA: 4.0}
    out = []
    for n in (48, 72):
        parts = st.integrate_parts(rho, 0.0, [(-1.8, 1.8)] * 3, n=n, params=p, functions=funcs)
        out.append(f"n={n}: E_tot {parts['total']:+.5f} m, E_neg {parts['negative']:+.5f} m, E_pos {parts['positive']:+.5f} m")
    print(f"A0={a0}: " + " | ".join(out) + f"  [{time.time()-T0:.0f}s]", flush=True)

print("\n=== 2. Lapse bump alone (v = 0), A0 = 10: Eulerian rho and energy conditions ===")
p0 = {v: 0.0, R: 1.0, sg: 8.0, A0: 10.0, RA: 1.6, sA: 4.0}
pts = [(0.0, 0.0, rr_, 0.05) for rr_ in np.linspace(0.8, 2.4, 17)]
frho = st.compile(rho, p0, funcs)
print("Eulerian rho on the ray:", [f"{float(frho(*q)):+.2e}" for q in pts])
sc = st.scan_energy_conditions(pts, p0, funcs)
print(f"points {sc['points']}, violations {sc['violations']}, worst NEC {sc['worst']['nec_min'][0]:.3e}, worst SEC {sc['worst'].get('sec_min', ['n/a'])[0]}  [{time.time()-T0:.0f}s]")
