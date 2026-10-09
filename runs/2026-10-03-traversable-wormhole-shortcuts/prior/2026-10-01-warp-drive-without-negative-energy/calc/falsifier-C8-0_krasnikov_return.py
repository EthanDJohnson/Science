"""Falsifier C8-0: does a traveller who builds infrastructure only inside his own causal
future get a time advance (on the return leg), and does that infrastructure need NEC/WEC
violation?  Geometric units G = c = 1, lengths in metres (times in metres of light travel
or in years where stated).

Part 1: Krasnikov (1998, gr-qc/9511068, Sec. 4 Example 5) tube light cones and round-trip
        timing, k_in = delta - 1.
Part 2: Steady-state 4D Krasnikov tube (Everett & Roman 1997 form)
        ds^2 = -(dt - dx)(dt + k(rho) dx) + dy^2 + dz^2,  k = 1 - (2 - delta) S(rho),
        S a smooth step equal to 1 inside rho < rho_max; NEC/WEC for all observers in the
        wall via gr_tensors.
"""
import sys
import math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
import numpy as np
from gr_tensors import Spacetime

LY = 9.4607304725808e15  # m
YR_LIGHT_M = LY           # one light-year of c*t

print("=== Part 1: Krasnikov tube light cones and timing ===")
t, x, d = sp.symbols("t x delta", real=True)
kk = sp.Symbol("k", real=True)
# 2D block metric g = -(dt - dx)(dt + k dx): g_tt=-1, g_tx=(1-k)/2, g_xx=k
g2 = sp.Matrix([[-1, (1 - kk) / 2], [(1 - kk) / 2, kk]])
for label, kval in [("outside (k=1)", 1), ("inside (k=delta-1)", d - 1)]:
    gg = g2.subs(kk, kval)
    # null directions V=(1, s): solve g(V,V)=0 for s = dx/dt
    s = sp.Symbol("s")
    sols = sp.solve(sp.expand((sp.Matrix([1, s]).T * gg * sp.Matrix([1, s]))[0]), s)
    print(f"{label}: null dx/dt = {[sp.simplify(q) for q in sols]}")
# future orientation: u = d_t has g(u,u) = -1 everywhere; V future iff g(u,V) < 0
gin = g2.subs(kk, d - 1)
lI = sp.Matrix([-(1 - d), -1])   # Krasnikov's l_I = -(1-delta) d_t - d_x
norm = sp.simplify((lI.T * gin * lI)[0])
orient = sp.simplify((sp.Matrix([1, 0]).T * gin * lI)[0])
print(f"l_I = -(1-delta)d_t - d_x: g(l,l) = {norm}; g(d_t, l) = {orient}  (<0 => future-directed for delta>0)")
print("So inside the tube a future-directed photon moving toward -x has dt/dx = (1-delta): t DEcreases by (1-delta)*D over a return of length D.")

D_ly = 4.37
for delta in (0.1, 0.01):
    t_arrive_B = D_ly                     # outbound at ~c (yr)
    t_home = D_ly - (1 - delta) * D_ly    # return inside tube (yr), epsilon terms dropped
    light_round = 2 * D_ly
    light_from_B = t_arrive_B + D_ly      # light leaving B at departure reaches A
    print(f"delta={delta}: D=4.37 ly; arrive B at t={t_arrive_B:.3f} yr; home at t={t_home:.4f} yr; "
          f"light round trip 2D = {light_round:.2f} yr; return-leg advance over light from B = "
          f"{light_from_B - t_home:.3f} yr")

print()
print("=== Part 2: NEC/WEC in the 4D steady-state tube wall ===")
T, X, Y, Z = sp.symbols("t x y z", real=True)
delta_s, sig, rmax = sp.symbols("delta sigma rho_max", positive=True)
rho = sp.sqrt(Y**2 + Z**2)
S = (1 - sp.tanh(sig * (rho - rmax))) / 2
k = 1 - (2 - delta_s) * S
g = sp.Matrix([[-1, (1 - k) / 2, 0, 0],
               [(1 - k) / 2, k, 0, 0],
               [0, 0, 1, 0],
               [0, 0, 0, 1]])
st = Spacetime(g, [T, X, Y, Z])
params = {delta_s: 0.01, sig: 2.0, rmax: 10.0}
u_static = [1, 0, 0, 0]   # g_tt = -1 everywhere, so d_t is a unit timelike observer
pts = [(0.0, 0.0, r, 0.0) for r in np.linspace(7.0, 13.0, 61)]
scan = st.scan_energy_conditions(pts, params, observer=u_static)
print("scan along y in wall, rho in [7,13] m, delta=0.01, sigma=2/m, rho_max=10 m:")
print(" points", scan["points"], "skipped", scan["skipped"])
print(" violations", scan["violations"])
print(" worst", scan["worst"])
# Analytic check: Einstein tensor contracted with a null vector
Gab = st.einstein()
# null vector along +y combined with u: k = d_t + d_y
kv = sp.Matrix([1, 0, 1, 0])
nec_expr = (kv.T * Gab * kv)[0]
fn = sp.lambdify((Y,), nec_expr.subs({Z: 0, **params}), "numpy")
vals = [(r, float(fn(r)) / (8 * math.pi)) for r in (9.0, 9.5, 10.0, 10.5, 11.0)]
print(" T_ab k^a k^b for k = d_t + d_y at (rho):", [(r, f"{v:.3e}") for r, v in vals])
rho_static = (sp.Matrix(u_static).T * Gab * sp.Matrix(u_static))[0]
fr = sp.lambdify((Y,), rho_static.subs({Z: 0, **params}), "numpy")
print(" static-observer energy density T_tt (m^-2):",
      [(r, f"{float(fr(r)) / (8 * math.pi):.3e}") for r in (9.0, 9.5, 10.0, 10.5, 11.0)])
# convergence/robustness: different sigma and delta
for prm in ({delta_s: 0.01, sig: 4.0, rmax: 10.0}, {delta_s: 0.5, sig: 2.0, rmax: 10.0}):
    sc = st.scan_energy_conditions([(0.0, 0.0, r, 0.0) for r in np.linspace(7.0, 13.0, 121)], prm,
                                   observer=u_static)
    print(" params", {str(a): b for a, b in prm.items()}, "violations", sc["violations"],
          "nec_min", sc["worst"]["nec_min"])
# control: delta = 2 -> k = 1 everywhere (flat) must give no violation and zero T
sc0 = st.scan_energy_conditions(pts, {delta_s: 2.0, sig: 2.0, rmax: 10.0}, observer=u_static)
print(" control delta=2 (flat): violations", sc0["violations"], "nec_min", sc0["worst"]["nec_min"])
