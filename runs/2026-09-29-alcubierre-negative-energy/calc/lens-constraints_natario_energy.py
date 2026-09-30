"""Constraints lens: Natario-class drives (unit lapse, flat slices) -- Natario zero-expansion vs Alcubierre vs an
irrotational (potential-flow) drive with the same profile f. Geometric units G = c = 1, lengths in metres.

Shifts (exterior-frame velocity field X; metric ds^2 = -dt^2 + sum (dx^i - X^i dt)^2; toolkit shift b = -X):
  Alcubierre   X = v f x_hat
  Natario      X = v [ f + (y f_y + z f_z)/2 , -(xi/2) f_y , -(xi/2) f_z ]   (div X = 0; equals Natario's
               v d(n r^2 sin^2 theta dphi) with n = f/2 about the x axis)
  Irrotational X = v grad(xi f) = v [ f + xi f_x , xi f_y , xi f_z ]  (curl X = 0)
with xi = x - v t, f = Alcubierre tanh top hat of radius R, steepness sigma.

Identity checked: for unit lapse + flat slices, integrated Eulerian energy = -(1/32 pi) int |curl X|^2 d^3x plus a
boundary term that vanishes for compactly supported X. So Natario-class drives with Minkowski exteriors have
E_tot <= 0, and irrotational ones have E_tot = 0 exactly (positive and negative parts cancel).
"""
import math
import sys
import time

import numpy as np
import sympy as sp

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from gr_tensors import Spacetime, metrics  # noqa: E402

T0 = time.time()
t, x, y, z = sp.symbols("t x y z", real=True)
v, R, sg = sp.symbols("v R sigma", positive=True)
f = sp.Function("f")
xi = x - v * t
rs = sp.sqrt(xi**2 + y**2 + z**2)
F = f(rs)
fx, fy, fz = sp.diff(F, x), sp.diff(F, y), sp.diff(F, z)
shifts = {
    "alcubierre": [v * F, 0, 0],
    "natario": [v * (F + (y * fy + z * fz) / 2), -v * xi * fy / 2, -v * xi * fz / 2],
    "irrotational": [v * (F + xi * fx), v * xi * fy, v * xi * fz],
}
rr = sp.symbols("r", positive=True)
top = sp.Lambda(rr, (sp.tanh(sg * (rr + R)) - sp.tanh(sg * (rr - R))) / (2 * sp.tanh(sg * R)))
params = {v: 1.0, R: 1.0, sg: 8.0}
funcs = {f: top}

sts = {}
for name, X in shifts.items():
    st = Spacetime.from_adm(1, [-c for c in X], sp.eye(3), [t, x, y, z])
    sts[name] = st
    # divergence and curl of X (check the construction)
    Xs = [sp.sympify(c) for c in X]
    div = sum(sp.diff(Xs[i], q) for i, q in enumerate((x, y, z)))
    curl = [sp.diff(Xs[2], y) - sp.diff(Xs[1], z), sp.diff(Xs[0], z) - sp.diff(Xs[2], x), sp.diff(Xs[1], x) - sp.diff(Xs[0], y)]
    curl2 = sum(c**2 for c in curl)
    fdiv = st.compile(div, params, funcs)
    fc2 = st.compile(curl2, params, funcs)
    pts = [(0.0, 0.3, 0.9, 0.2), (0.0, -0.7, 0.6, 0.1), (0.0, 0.95, 0.1, 0.3)]
    print(f"[{name}] div X at samples: {[round(float(fdiv(*p)), 12) for p in pts]} ; |curl X|^2 at samples: {[round(float(fc2(*p)), 6) for p in pts]}")
    rho = st.energy_density()
    for n in (64, 96):
        parts = st.integrate_parts(rho, 0.0, [(-1.8, 1.8)] * 3, n=n, params=params, functions=funcs)
        curlint = st.integrate_parts(-curl2 / (32 * sp.pi), 0.0, [(-1.8, 1.8)] * 3, n=n, params=params, functions=funcs)
        print(f"  n={n}: E_tot {parts['total']:+.5f} m  E_neg {parts['negative']:+.5f} m  E_pos {parts['positive']:+.5f} m ;"
              f"  -(1/32pi) int|curl X|^2 = {curlint['total']:+.5f} m")
    # pointwise extremes of Eulerian rho on a fine plane grid (z = 0 and z = 0.4)
    frho = st.compile(rho, params, funcs)
    g = np.linspace(-1.6, 1.6, 321)
    XX, YY = np.meshgrid(g, g, indexing="ij")
    vals = np.concatenate([np.asarray(frho(0.0, XX, YY, 0.0 * XX + zz), dtype=float).ravel() for zz in (0.0, 0.4)])
    vals = vals[np.isfinite(vals)]
    print(f"  pointwise Eulerian rho: min {vals.min():+.4e} /m^2, max {vals.max():+.4e} /m^2  [{time.time()-T0:.0f}s]", flush=True)

import sys as _s; _s.exit(0)
print("\n=== Energy-condition scans over the wall (v = 1 and 10) ===")
pts = []
for xx in np.linspace(-1.5, 1.5, 11):
    for yy in np.linspace(0.05, 1.5, 9):
        if 0.6 < math.hypot(xx, yy) < 1.4:
            pts.append((0.0, xx, yy, 0.0))
pts += [(0.0, 0.3, 0.6, 0.6), (0.0, -0.4, 0.5, 0.7), (0.0, 0.9, 0.2, 0.3)]
for name in ("natario", "irrotational"):
    st = sts[name]
    for vv in (1.0, 10.0):
        pv = {v: vv, R: 1.0, sg: 8.0}
        sc = st.scan_energy_conditions(pts, pv, funcs)
        fields = st._numeric_fields(pv, funcs, None)
        types = {}
        for q in pts:
            r_ = st._conditions_at(fields, q)
            types[r_["type"]] = types.get(r_["type"], 0) + 1
        print(f"[{name}] v={vv}: {sc['points']} pts, violations {sc['violations']}, types {types}, worst NEC {sc['worst']['nec_min'][0]:.3e}, worst WEC {sc['worst']['wec_min'][0]:.3e}  [{time.time()-T0:.0f}s]", flush=True)
