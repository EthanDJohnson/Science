"""Constraints lens: energy-condition scan for the irrotational (potential-flow) Natario-class drive and Natario's
zero-expansion drive, same tanh profile (R = 1 m, sigma = 8 /m), v = 1. Geometric units. Uses the explicit tanh
profile (no abstract f) so the 4D Einstein tensor stays small. Prints per-point results as it goes.
Key question: where the Eulerian density is POSITIVE, does the NEC/WEC still fail for some observer?
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
V, Rb, S = 1, 1, 8
xi = x - V * t
rs = sp.sqrt(xi**2 + y**2 + z**2)
F = (sp.tanh(S * (rs + Rb)) - sp.tanh(S * (rs - Rb))) / (2 * sp.tanh(S * Rb))
fx, fy, fz = sp.diff(F, x), sp.diff(F, y), sp.diff(F, z)
which = sys.argv[1] if len(sys.argv) > 1 else "irrotational"
if which == "irrotational":
    X = [V * (F + xi * fx), V * xi * fy, V * xi * fz]
else:
    X = [V * (F + (y * fy + z * fz) / 2), -V * xi * fy / 2, -V * xi * fz / 2]
st = Spacetime.from_adm(1, [-c for c in X], sp.eye(3), [t, x, y, z])
rho = st.compile(st.energy_density())
pts = []
for xx in np.linspace(-1.3, 1.3, 7):
    for yy in np.linspace(0.1, 1.3, 5):
        if 0.7 < math.hypot(xx, yy) < 1.3:
            pts.append((0.0, float(xx), float(yy), 0.15))
print(f"{which}: {len(pts)} points; building stress-energy ...", flush=True)
fields = st._numeric_fields(None, None, None)
print(f"built in {time.time()-T0:.0f}s", flush=True)
counts = {"nec": 0, "wec": 0, "sec": 0, "dec": 0}
pos_rho_nec_fail = pos_rho = 0
types = {}
for p in pts:
    r = st._conditions_at(fields, p)
    er = float(rho(*p))
    for c in counts:
        counts[c] += 0 if r[c] else 1
    types[r["type"]] = types.get(r["type"], 0) + 1
    if er > 1e-6:
        pos_rho += 1
        pos_rho_nec_fail += 0 if r["nec"] else 1
    print(f"  {p[1]:+.2f},{p[2]:.2f},{p[3]:.2f}: Eulerian rho {er:+.4e} type {r['type']} NEC {r['nec']} WEC {r['wec']} "
          f"nec_min {r['nec_min']:+.3e} wec_min {r['wec_min']:+.3e}", flush=True)
print(f"violations {counts} of {len(pts)}; types {types}; points with Eulerian rho > 0: {pos_rho}, of which NEC fails at {pos_rho_nec_fail}")
print(f"done in {time.time()-T0:.0f}s")
