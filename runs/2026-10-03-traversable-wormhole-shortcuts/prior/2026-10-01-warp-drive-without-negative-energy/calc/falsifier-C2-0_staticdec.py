"""falsifier-C2-0 part 2: zero-shift (static) DEC of the Fuchs-type uniform-density shell vs compactness.

SI units (eps, p in Pa = J/m^3); C = 2GM/(c^2 R2) dimensionless. Toolkit rebuild warp_shell.build_shell,
default smoothing (span_P = 0.1 Delta, span_rho = 1.72 span_P, 4 passes). Static, diagonal T: type I, so
DEC <=> eps >= |p_r|, eps >= |p_t| exactly (toolkit profiles: p_t from the anisotropic TOV identity).
Reports max(|p_r|,|p_t|)/eps over the wall (eps > 1e-3 eps_max, to exclude tails) and its location, the
threshold compactness C_DEC where it reaches 1, for wall thickness Delta/R2 = 0.5, 0.25, 0.125, 0.075.
Convergence: grid N = 8001 vs 16001.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-01-warp-drive-without-negative-energy/tools")
import numpy as np
from warp_shell import build_shell

Gc, cc = 6.674e-11, 2.998e8
R2 = 20.0


def ratio(M, R1, N=8001, cut=1e-3):
    sh = build_shell(M, R1, R2, N=N)
    eps, pr, pt, r = sh.eps, sh.p_r, sh.p_t, sh.r
    msk = eps > cut * eps.max()
    q = np.maximum(np.abs(pr[msk]), np.abs(pt[msk])) / eps[msk]
    j = np.argmax(q)
    return float(q[j]), float(r[msk][j]), float(pt[msk][j]), float(pr[msk][j])


def Cof(M):
    return 2 * Gc * M / (cc ** 2 * R2)


Mbuch = (8 / 9) * cc ** 2 * R2 / (2 * Gc)
for frac in (0.5, 0.25, 0.125, 0.075):
    R1 = R2 * (1 - frac)
    print(f"--- Delta/R2 = {frac} (R1 = {R1} m) ---")
    for C in (0.1667, 0.3334, 0.4, 0.45, 0.5, 0.6, 0.7, 0.8, 0.85):
        M = C * cc ** 2 * R2 / (2 * Gc)
        try:
            q, rq, pt, pr = ratio(M, R1)
            q2 = ratio(M, R1, N=16001)[0]
            print(f"C = {C:.4f}: static max|p|/eps = {q:.3f} at r = {rq:.2f} m (N=16001: {q2:.3f}); "
                  f"p_t there {pt:.3e} Pa, p_r {pr:.3e} Pa; DEC {'holds' if q <= 1 else 'FAILS'} at zero shift")
        except Exception as e:  # noqa: BLE001
            print(f"C = {C:.4f}: build failed: {e}")
    # bisect C_DEC
    lo, hi = 0.1667, 0.85
    if ratio(hi * cc ** 2 * R2 / (2 * Gc), R1)[0] > 1:
        for _ in range(20):
            mid = 0.5 * (lo + hi)
            q = ratio(mid * cc ** 2 * R2 / (2 * Gc), R1)[0]
            lo, hi = (mid, hi) if q <= 1 else (lo, mid)
        print(f"C_DEC (zero shift, Delta/R2 = {frac}) = {0.5 * (lo + hi):.4f}")
    else:
        print(f"C_DEC > 0.85 for Delta/R2 = {frac}")
