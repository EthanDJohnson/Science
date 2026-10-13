"""Constraints lens: energy conditions and invariants of exact plane (pp) gravitational waves.

Purpose: the plane-wave no-go results [D-56, D-57, D-58] and the kinematic statement s = 0 for a single plane
wave [D-55] rest on the wave's stress-energy being null (support on q^2 = 0). Check with gr_tensors:
 (1) vacuum plane wave H = A(u)(x^2 - y^2) + 2 B(u) x y: G_ab = 0, Kretschmann = 0 (all scalar invariants vanish);
 (2) null-dust plane wave H = F(u)(x^2 + y^2) (exact analogue of the Isaacson effective stress tensor of a
     GW beam): T_ab = rho k_a k_b, NEC/WEC/SEC/DEC hold for F >= 0, T^a_a = 0, T_ab T^ab = 0: its momentum is null,
     so it cannot supply the time-like q (s > 0) that pair production needs;
 (3) the effective momentum of two crossing null beams k1, k2: q^2 = 2 k1.k2 (time-like unless parallel).
Metric: ds^2 = -dt^2 + dx^2 + dy^2 + dz^2 + H(u, x, y) (dt - dz)^2, u = t - z; geometric units G = c = 1.
"""
import sys
import math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
import numpy as np
from gr_tensors import Spacetime

t, x, y, z, uu = sp.symbols('t x y z u', real=True)
A, B, F = sp.Function('A'), sp.Function('B'), sp.Function('F')
u = t - z

def pp_metric(H):
    g = sp.Matrix(sp.diag(-1, 1, 1, 1))
    g[0, 0] += H; g[3, 3] += H; g[0, 3] -= H; g[3, 0] -= H
    return g

def kretschmann(st):
    Rup = st.riemann()
    gi, g, n = st.ginv, st.g, 4
    Rl = [[[[sum(g[a, e] * Rup[e][b][c][d] for e in range(n)) for d in range(n)] for c in range(n)] for b in range(n)] for a in range(n)]
    nz = [(a, b, c, d) for a in range(n) for b in range(n) for c in range(n) for d in range(n) if sp.expand(Rl[a][b][c][d]) != 0]
    K = 0
    for (a, b, c, d) in nz:
        up = 0
        for (e, f, gg, h) in nz:
            co = gi[a, e] * gi[b, f] * gi[c, gg] * gi[d, h]
            if co != 0:
                up += co * Rl[e][f][gg][h]
        K += Rl[a][b][c][d] * up
    return sp.simplify(sp.expand(K)), len(nz)

print("=== (1) vacuum plane wave H = A(u)(x^2 - y^2) + 2 B(u) x y ===")
st1 = Spacetime(pp_metric(A(u) * (x**2 - y**2) + 2 * B(u) * x * y), [t, x, y, z])
G1 = st1.einstein()
nonzero = [(i, j) for i in range(4) for j in range(4) if sp.simplify(G1[i, j]) != 0]
print("  Einstein tensor nonzero components:", nonzero or "none (vacuum)")
K1, nnz = kretschmann(st1)
print(f"  nonzero lowered Riemann components: {nnz}; Kretschmann R_abcd R^abcd = {K1}")
print("  R^x_{t x t} =", sp.simplify(st1.riemann()[1][0][1][0]))

print("\n=== (2) null-dust plane wave H = F(u)(x^2 + y^2) ===")
st2 = Spacetime(pp_metric(F(u) * (x**2 + y**2)), [t, x, y, z])
G2 = st2.einstein().applyfunc(sp.simplify)
print("  G_ab =", G2.tolist())
gi2 = st2.ginv
trace = sp.simplify(sum(gi2[i, j] * G2[i, j] for i in range(4) for j in range(4)))
Gup = (gi2 * G2 * gi2).applyfunc(sp.simplify)
sq = sp.simplify(sum(G2[i, j] * Gup[i, j] for i in range(4) for j in range(4)))
print("  trace G^a_a =", trace, "; G_ab G^ab =", sq, "(null dust: both zero)")
pts = [(tt, xx, yy, zz) for tt in (-0.5, 0.0, 0.3, 0.9) for xx in (-1.0, 0.5) for yy in (0.0, 1.0) for zz in (0.0, 0.2)]
for sign in (+1, -1):
    prof = sp.Lambda(uu, sign * 1e-2 * sp.exp(-uu**2))
    scan = st2.scan_energy_conditions(pts, {}, {F: prof})
    print(f"  F(u) = {sign:+d}e-2 exp(-u^2): scan over {scan['points']} points (skipped {scan['skipped']}): violations {scan['violations']}; "
          f"worst {{{', '.join(f'{k}: {v[0]:.3e}' for k, v in scan['worst'].items())}}}")
    ec = st2.energy_conditions((0.0, 0.5, 0.0, 0.0), {}, {F: prof})
    print(f"    point (0, 0.5, 0, 0): type {ec.get('type')}, NEC {ec.get('nec')}, WEC {ec.get('wec')}, SEC {ec.get('sec')}, DEC {ec.get('dec')}")
rho = st2.energy_density()
print("  Eulerian energy density =", sp.simplify(rho), "(in this sign convention >= 0 iff F <= 0: F < 0 is ordinary null dust, F > 0 exotic)")

print("\n=== (3) effective momentum of two crossing null beams ===")
for th_deg in (0.0, 1.0, 10.0, 90.0, 180.0):
    th = math.radians(th_deg)
    k1 = np.array([1.0, 0, 0, 1.0])
    k2 = np.array([1.0, math.sin(th), 0, math.cos(th)])
    q = k1 + k2
    q2 = q[0]**2 - q[1]**2 - q[2]**2 - q[3]**2
    print(f"  opening angle {th_deg:6.1f} deg: s = q^2 = {q2:.6f} (2 w1 w2 (1 - cos) = {2*(1-math.cos(th)):.6f})")
