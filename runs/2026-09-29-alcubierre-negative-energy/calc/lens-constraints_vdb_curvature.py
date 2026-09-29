"""Constraints lens: invariant curvature radius in Van Den Broeck region II vs the coordinate-component value.
Metric in region II (comoving coords): diag(-1, B^2, B^2, B^2), B = alpha(-(n-1)w^n + n w^(n-1)) + 1,
w = (R~ + D~ - r)/D~, alpha = 1e17, n = 80, R~ = D~ = 1e-15 m. Geometric units (metres).
 - orthonormal sectional curvatures of h = B^2 delta: K_rt = R_rr/2, K_tp = R_tt - R_rr/2 (3D identities), with
   R_ij = -(om_ij - om_i om_j) - (lap om + |grad om|^2) delta_ij (om = ln B), divided by B^2
 - Cartesian all-lower coordinate components R_ijkl = B^4 x (orthonormal), which are NOT invariant
 - toolkit curvature_at at sample points (float64) as a cross-check
 - throat: minimum of the area radius A = B r inside region II
 - QI check with tau0 = 0.1 r_c for both r_c choices
"""
import math
import sys

import mpmath as mp
import sympy as sp

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from gr_tensors import Spacetime, to_si, PLANCK_LENGTH, qi  # noqa: E402

mp.mp.dps = 50
al, n, Rt, Dt = mp.mpf(10) ** 17, 80, mp.mpf("1e-15"), mp.mpf("1e-15")
KGM = to_si.mass_kg(1.0)


def Bf(r):
    w = (Rt + Dt - r) / Dt
    return 1 + al * (-(n - 1) * w**n + n * w ** (n - 1))


def dB(r):
    w = (Rt + Dt - r) / Dt
    return -(al / Dt) * n * (n - 1) * (w ** (n - 2) - w ** (n - 1))


def d2B(r):
    w = (Rt + Dt - r) / Dt
    return (al / Dt**2) * n * (n - 1) * ((n - 2) * w ** (n - 3) - (n - 1) * w ** (n - 2))


def sect(r):
    b, b1, b2 = Bf(r), dB(r), d2B(r)
    o1, o2 = b1 / b, b2 / b - (b1 / b) ** 2
    lap = o2 + 2 * o1 / r
    Rrr = (-(o2 - o1**2) - (lap + o1**2)) / b**2
    Rtt = (-(o1 / r) - (lap + o1**2)) / b**2
    return Rrr / 2, Rtt - Rrr / 2, Rrr, Rtt


N = 40000
maxK, rK, maxCoord, rC = mp.mpf(0), None, mp.mpf(0), None
Amin, rA = mp.inf, None
for i in range(N):
    r = Rt + Dt * mp.mpf(i + 0.5) / N
    k1, k2, _, _ = sect(r)
    k = max(abs(k1), abs(k2))
    if k > maxK:
        maxK, rK = k, r
    kc = k * Bf(r) ** 4
    if kc > maxCoord:
        maxCoord, rC = kc, r
    A = Bf(r) * r
    if A < Amin:
        Amin, rA = A, r
rc_inv = 1 / mp.sqrt(maxK)
rc_coord = 1 / mp.sqrt(maxCoord)
print(f"orthonormal max |sectional curvature| = {float(maxK):.3e} /m^2 at r = {float(rK):.5e} m (B = {float(Bf(rK)):.3g})"
      f" -> invariant r_c = {float(rc_inv):.3e} m = {float(rc_inv/PLANCK_LENGTH):.3e} L_P")
print(f"Cartesian coordinate components B^4|K| max = {float(maxCoord):.3e} /m^2 at r = {float(rC):.5e} m (B = {float(Bf(rC)):.3g})"
      f" -> 'r_c' = {float(rc_coord):.3e} m = {float(rc_coord/PLANCK_LENGTH):.2f} L_P")
print(f"area radius A = B r: minimum {float(Amin):.4e} m at r = {float(rA):.6e} m (outer edge value {float(Rt+Dt):.1e} m): "
      f"{'interior minimum => throat' if rA < Rt + Dt * (1 - mp.mpf(1)/N) else 'minimum at edge'}")
_, _, Rrr_thr, _ = sect(rA)
print(f"  3R_rr (orthonormal) at the throat = {float(Rrr_thr):.3e} /m^2 -> rho + p_r = {float(Rrr_thr)/(8*math.pi):.3e} /m^2")

# toolkit cross-check at two points (float64), metric diag(-1, B^2, B^2, B^2) with B the polynomial in r
t, x, y, z = sp.symbols("t x y z", real=True)
r = sp.sqrt(x**2 + y**2 + z**2)
w = (sp.Float("2e-15") - r) / sp.Float("1e-15")
Bs = 1 + sp.Float("1e17") * (-(n - 1) * w**n + n * w ** (n - 1))
st = Spacetime.from_adm(1, [0, 0, 0], Bs**2 * sp.eye(3), [t, x, y, z])
for rv in (float(rK), 1.9e-15):
    c = st.curvature_at((0.0, 0.0, rv, 0.0))
    k1, k2, _, _ = sect(mp.mpf(rv))
    print(f"toolkit curvature_at r = {rv:.4e} m: max frame component {c['max_frame_component']:.4e} /m^2, r_c = {c['curvature_radius']:.4e} m;"
          f" mpmath max|K| {float(max(abs(k1), abs(k2))):.4e}")
rho = st.energy_density()
pc = st.precision_check(rho, [(0.0, 0.0, float(rK), 0.0), (0.0, 0.0, 1.05e-15, 0.0)])
print(f"precision_check of Eulerian rho: max rel err {pc['max_rel_error']:.2e}, sign flips {pc['sign_flips']}, values {[(v[1], v[2]) for v in pc['values']]}")

# QI both ways; LHS = peak |rho| (orthonormal, invariant) from lens-constraints_vdb.py: 1.759e32 /m^2
rho_pk = 1.759e32
for label, rc in (("invariant", float(rc_inv)), ("coordinate", float(rc_coord))):
    b = qi.ford_roman_geometric(0.1 * rc)
    print(f"QI with r_c({label}) = {rc:.3e} m: bound {b:.3e} /m^2 = {b*KGM:.3e} kg/m^3 ; |rho_pk| = {rho_pk*KGM:.3e} kg/m^3 ;"
          f" {'satisfied' if rho_pk < abs(b) else 'VIOLATED by factor %.1e' % (rho_pk/abs(b))}")
