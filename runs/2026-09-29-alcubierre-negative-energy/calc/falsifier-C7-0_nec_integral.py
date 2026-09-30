"""Falsifier C7-0: decisive test part 2. Worst-null-direction NEC integral
    I_NEC = int min(0, min_k T_ab k^a k^b) d^3x   (k = (1, n) in the Eulerian orthonormal frame)
for Alcubierre (A0 = 1) vs Loup-type lapse (A0 = 3, 10), and the lapse hill alone (v = 0),
compared with the Eulerian total E_Eul (lens values -0.22334, -0.02516, -0.00228 m).
Units: geometric (G = c = 1), metres; T in m^-2, integrals in m. v = 1, R = 1 m, sigma = 8 /m,
lapse bump R_A = 1.6 m, sigma_A = 4 /m (same as lens-constraints_lapse.py). Slice t = 0.
Axisymmetric about x: sample points (x, s, 0), weight 2 pi s ds dx.
Analytic cross-check for the lapse hill alone: static -A^2 dt^2 + dx^2 gives
    min_n G(k,k) = (sum of the two smaller Hessian eigenvalues of A)/A, eigenvalues A'', A'/r, A'/r.
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
print(f"setup {time.time()-T0:.0f}s", flush=True)


def nec_integral(pars, h, L=3.0):
    fields = st._numeric_fields(pars, funcs, None)
    xs = np.arange(-L, L + 1e-12, h)
    ss = np.arange(h / 2, L, h)
    tot, neg_rho = 0.0, 0.0
    for xv in xs:
        for sv in ss:
            r = st._conditions_at(fields, (0.0, float(xv), float(sv), 0.0))
            w = 2 * math.pi * sv * h * h
            tot += min(0.0, r["nec_min"]) * w
            neg_rho += r["rho_observer"] * w
    return tot, neg_rho


def lapse_alone_analytic(a0, L=3.0, n=200001):
    r = np.linspace(1e-4, L * math.sqrt(3), n)
    s = 4.0
    ra = 1.6
    gfun = (np.tanh(s * (r + ra)) - np.tanh(s * (r - ra))) / (2 * math.tanh(s * ra))
    gp = s * ((1 / np.cosh(s * (r + ra)))**2 - (1 / np.cosh(s * (r - ra)))**2) / (2 * math.tanh(s * ra))
    gpp = -2 * s * s * ((np.tanh(s * (r + ra)) / np.cosh(s * (r + ra))**2)
                        - (np.tanh(s * (r - ra)) / np.cosh(s * (r - ra))**2)) / (2 * math.tanh(s * ra))
    Af = 1 + (a0 - 1) * gfun
    e1, e2 = (a0 - 1) * gpp, (a0 - 1) * gp / r
    eig = np.stack([e1, e2, e2])
    eig.sort(axis=0)
    nec = (eig[0] + eig[1]) / Af / (8 * math.pi)
    dens = np.minimum(0.0, nec)
    return np.trapezoid(4 * math.pi * r**2 * dens, r), nec.min()


print("\n=== Analytic lapse hill alone (v=0): NEC integral, worst NEC density ===")
for a0 in (3.0, 10.0, 100.0):
    I, wmin = lapse_alone_analytic(a0)
    print(f"A0={a0:6.1f}: I_NEC = {I:+.4f} m   worst NEC density = {wmin:+.4f} m^-2 (continuous min over n)")

cases = [("Alcubierre A0=1 ", {v: 1.0, R: 1.0, sg: 8.0, A0: 1.0, RA: 1.6, sA: 4.0}, -0.22334),
         ("Loup A0=3        ", {v: 1.0, R: 1.0, sg: 8.0, A0: 3.0, RA: 1.6, sA: 4.0}, -0.02516),
         ("Loup A0=10       ", {v: 1.0, R: 1.0, sg: 8.0, A0: 10.0, RA: 1.6, sA: 4.0}, -0.00228),
         ("lapse alone A0=10", {v: 0.0, R: 1.0, sg: 8.0, A0: 10.0, RA: 1.6, sA: 4.0}, 0.0)]
print("\n=== Numerical (gr_tensors, 64 sampled null directions), two grids ===")
for name, p, eeul in cases:
    out = []
    for h in (0.05, 0.035):
        I, Er = nec_integral(p, h)
        out.append((h, I, Er))
    (h1, I1, E1), (h2, I2, E2) = out
    print(f"{name}: I_NEC(h={h1})={I1:+.4f} m, I_NEC(h={h2})={I2:+.4f} m | E_Eul grid={E2:+.5f} m (lens {eeul:+.5f})"
          f" | I_NEC/E_Eul = {I2/eeul if eeul else float('nan'):.2f}  [{time.time()-T0:.0f}s]", flush=True)
