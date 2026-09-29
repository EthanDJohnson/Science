#!/usr/bin/env python3
"""lens-constraints: is negative energy unavoidable for flat-slice, unit-lapse warp drives? ([D-02] check)

Class: ds^2 = -dt^2 + delta_ij (dx^i + b^i dt)(dx^j + b^j dt)  (Natario class; Alcubierre is b = (-v f, 0, 0)).
Units: geometric G = c = 1, lengths in metres.

Derivation checked numerically here: with flat slices K_ij = (d_i b_j + d_j b_i)/2 and the Hamiltonian
constraint gives rho = [(tr K)^2 - K_ij K_ij]/(16 pi) = (1/16 pi) [ div(...) - |curl b|^2 / 2 ], where
(d.b)^2 - d_i b_j d_j b_i = d_i(b_i d_j b_j) - d_j(b_i d_i b_j) is a total divergence.  Hence for any shift that
decays at infinity:  E_Eul = int rho d^3x = -(1/32 pi) int |curl b|^2 d^3x <= 0,  with E_Eul = 0 only for an
irrotational shift, which still needs rho < 0 somewhere unless rho = 0 everywhere.
 1. Pointwise: gr_tensors rho vs [(tr K)^2 - K_ij K_ij]/(16 pi).
 2. Integrals (n and 1.5n): int rho vs -(1/32 pi) int |curl b|^2.
 3. Irrotational bubble b = grad(-v xi F(r)): total zero, local negative regions, NEC scan at the minimum.
Run: python3 runs/smoke-constraints/calc/lens-constraints_natario_class.py
"""
import math
import sys
import time
import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning)   # removable 1/r_s singularity at the bubble centre

sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
import sympy as sp
from gr_tensors import Spacetime, metrics

print(__doc__.split(" 1.")[0])
t, x, y, z = sp.symbols("t x y z", real=True)
vv = sp.Rational(3, 2)            # bubble speed v = 1.5 (units of c); rho scales as v^2 in this class
xi = x - vv * t
r = sp.sqrt(xi**2 + y**2 + z**2)
_, s0 = metrics.alcubierre()
top = metrics.alcubierre_top_hat(s0)
F = top(r).subs({s0["R"]: 1, s0["sigma"]: 4})     # tanh top hat, R = 1 m, sigma = 4 /m
gauss = sp.exp(-(r**2))

Phi = -vv * xi * F
shifts = {
    "A generic (curl and div nonzero)": ([-vv * gauss * (1 + sp.Rational(3, 10) * y), sp.Rational(2, 5) * vv * xi * z * gauss,
                                          -sp.Rational(1, 5) * vv * y * gauss], 4.5, 72),
    "B irrotational bubble b = grad(-v xi F)": ([sp.diff(Phi, x), sp.diff(Phi, y), sp.diff(Phi, z)], 2.4, 80),
    "C Alcubierre b = (-v F, 0, 0)": ([-vv * F, 0, 0], 2.4, 80),
}

pending = []
for name, (b, half, n1) in shifts.items():
    print(f"\n== {name}   (v = {float(vv)} c)")
    t0 = time.time()
    st = Spacetime.from_adm(1, b, sp.eye(3), [t, x, y, z])
    # Workaround: sympy's Matrix.inv() on these explicit shifts did not finish in 10 min, so inject the
    # closed-form ADM inverse for N = 1, h = delta: g^00 = -1, g^0i = b^i, g^ij = delta^ij - b^i b^j.
    gi = sp.zeros(4, 4)
    gi[0, 0] = -1
    for i in range(3):
        gi[0, i + 1] = gi[i + 1, 0] = b[i]
        for j in range(3):
            gi[i + 1, j + 1] = (1 if i == j else 0) - b[i] * b[j]
    chk = (st.g * gi).subs({t: 0, x: 0.3, y: 0.7, z: -0.2}).evalf()
    assert max(abs(float(chk[i, j]) - (1.0 if i == j else 0.0)) for i in range(4) for j in range(4)) < 1e-12
    st._cache["ginv"] = gi
    rho = st.energy_density()
    Xs = [x, y, z]
    K = sp.Matrix(3, 3, lambda i, j: (sp.diff(b[j], Xs[i]) + sp.diff(b[i], Xs[j])) / 2)
    rhoK = (K.trace() ** 2 - sum(K[i, j] ** 2 for i in range(3) for j in range(3))) / (16 * sp.pi)
    curl = [sp.diff(b[2], y) - sp.diff(b[1], z), sp.diff(b[0], z) - sp.diff(b[2], x), sp.diff(b[1], x) - sp.diff(b[0], y)]
    curl2 = sum(c**2 for c in curl)
    print(f"   symbolic setup {time.time() - t0:.1f} s", flush=True)
    # 1. pointwise
    f_rho, f_rhoK = st.compile(rho), st.compile(rhoK)
    worst = 0.0
    for pt in [(0.0, 0.3, 0.9, 0.2), (0.0, -0.8, 0.5, -0.4), (0.0, 0.95, 0.1, 0.3)]:
        a_, b_ = float(f_rho(*pt)), float(f_rhoK(*pt))
        worst = max(worst, abs(a_ - b_) / max(abs(b_), 1e-12))
    print(f"   1. max rel. diff gr_tensors rho vs Hamiltonian-constraint rho at 3 points: {worst:.1e}")
    # 2. integrals (sqrt(h) = 1).  integrate_on_slice recompiles on every call, so the negative part is
    #    summed on the same midpoint grid from the already-compiled rho (checked against the toolkit's total).
    for n in (n1, int(round(1.5 * n1))):
        t0 = time.time()
        E = st.integrate_on_slice(rho, 0.0, [(-half, half)] * 3, n=n)
        Ew = st.integrate_on_slice(-curl2 / (32 * sp.pi), 0.0, [(-half, half)] * 3, n=n)
        h = 2 * half / n
        ax = -half + h * (np.arange(n) + 0.5)
        yy, zz = np.meshgrid(ax, ax, indexing="ij")
        tot = neg = 0.0
        for xv in ax:
            vals = np.broadcast_to(f_rho(0.0, np.full_like(yy, xv), yy, zz), yy.shape)
            tot += float(np.sum(vals))
            neg += float(np.sum(np.minimum(vals, 0.0)))
        print(f"   2. n={n:3d}: int rho = {E:+.6e} m (own sum {tot * h**3:+.6e}); -(1/32pi) int |curl b|^2 = {Ew:+.6e} m; "
              f"negative part int min(rho,0) = {neg * h**3:+.6e} m  [{time.time() - t0:.1f} s]", flush=True)
    # 3. most negative point (even grid: avoids r_s = 0, where 1/r_s terms give NaN)
    grid = np.linspace(-half * 0.9, half * 0.9, 40)
    X3, Y3, Z3 = np.meshgrid(grid, grid, grid, indexing="ij")
    vals = np.broadcast_to(f_rho(0.0, X3, Y3, Z3), X3.shape)
    i = np.unravel_index(np.nanargmin(vals), vals.shape)
    pmin = (0.0, float(X3[i]), float(Y3[i]), float(Z3[i]))
    print(f"   3. min rho on a 40^3 grid = {vals[i]:+.4e} /m^2 at (x,y,z) = ({pmin[1]:+.3f},{pmin[2]:+.3f},{pmin[3]:+.3f}) m;"
          f" max rho = {np.nanmax(vals):+.4e} /m^2", flush=True)
    pending.append((name, st, pmin))

# 4. toolkit energy-condition scans at the minima (slow for the tanh shifts: compiles the full T_ab)
for name, st, pmin in pending:
    t0 = time.time()
    scan = st.energy_condition_scan(pmin)
    print(f"\n== scan {name}: rho = {scan['rho']:+.4e}, min T(k,k) = {scan['nec_min']:+.4e}, "
          f"WEC ok = {scan['wec_ok']}, NEC ok = {scan['nec_ok']}  [{time.time() - t0:.1f} s]", flush=True)

# 5. NEC search for the irrotational bubble (the minimum-rho point above passes the NEC, so search the wall).
#    T_ab is compiled once; the toolkit's energy_condition_scan would recompile it (~30 s) at every point.
name, stB, _ = pending[1]
t0 = time.time()
fT, fg, fn = stB.compile(stB.stress_energy()), stB.compile(stB.g), stB.compile(stB.eulerian_observer())
print(f"\n== 5. NEC search, {name}: compiled T_ab once in {time.time() - t0:.1f} s")
gold = math.pi * (3 - math.sqrt(5))
dirs = []
for k in range(64):
    zc = 1 - 2 * (k + 0.5) / 64
    rr_ = math.sqrt(1 - zc * zc)
    dirs.append((rr_ * math.cos(gold * k), rr_ * math.sin(gold * k), zc))
worst, n_viol, n_pts = (math.inf, None), 0, 0
for r_ in np.linspace(0.55, 1.6, 22):
    for th in np.linspace(0.07, math.pi - 0.07, 15):
        for ph in (0.3, 1.9):
            pt = (0.0, r_ * math.cos(th), r_ * math.sin(th) * math.cos(ph), r_ * math.sin(th) * math.sin(ph))
            T_ = np.array(fT(*pt), dtype=float).reshape(4, 4)
            g_ = np.array(fg(*pt), dtype=float).reshape(4, 4)
            u_ = np.array(fn(*pt), dtype=float).reshape(4)
            u_ = u_ / math.sqrt(-u_ @ g_ @ u_)
            tri = []
            for i in range(1, 4):
                e = np.zeros(4)
                e[i] = 1.0
                e = e + (e @ g_ @ u_) * u_
                for q_ in tri:
                    e = e - (e @ g_ @ q_) * q_
                tri.append(e / math.sqrt(e @ g_ @ e))
            m = min(float((u_ + sum(c * q_ for c, q_ in zip(d, tri))) @ T_ @ (u_ + sum(c * q_ for c, q_ in zip(d, tri)))) for d in dirs)
            n_pts += 1
            if m < -1e-10:
                n_viol += 1
            if m < worst[0]:
                worst = (m, pt)
print(f"   {n_pts} wall points (r = 0.55..1.6 m): NEC violated at {n_viol}; most negative T(k,k) = {worst[0]:+.4e} /m^2 at "
      f"(x,y,z) = ({worst[1][1]:+.3f},{worst[1][2]:+.3f},{worst[1][3]:+.3f}) m  [{time.time() - t0:.1f} s total]")
