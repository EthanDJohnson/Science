"""falsifier-C2-0: is the shell's shift cap set by compactness alone?

Geometric units for curvature (T = G/8pi in m^-2); SI for M [kg], radii [m]; beta in units of c.
Fixed compactness C = 2GM/(c^2 R2) = 0.333 (M = 4.49e27 kg, R2 = 20 m), vary the wall thickness
Delta = R2 - R1. Toolkit rebuild (runs/<slug>/tools/warp_shell.py, default smoothing span 0.1*Delta),
FD Einstein tensor and all-null-direction NEC copied from math/constraints/M-CONSTRAINTS-06.py
(6002 null directions). Bisect beta_crit (first NEC failure) on the y axis (perpendicular to the
shift) and on the 45-degree line, dense radial sampling through the wall. Second part: fixed
Delta/R2 = 0.5 but different C (different M) to compare against the scaling beta ~ k C Delta/R2.
Also prints zero-shift max(|p|)/eps (exact static DEC ratio) per configuration.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-01-warp-drive-without-negative-energy/tools")
import numpy as np

src = open("runs/2026-10-01-warp-drive-without-negative-energy/math/constraints/M-CONSTRAINTS-06.py").read()
src = src.split("rs = np.arange")[0]
ns = {}
exec(src, ns)
build_shell, einstein, make_g, DIRS = ns["build_shell"], ns["einstein"], ns["make_g"], ns["DIRS"]
KK = np.hstack([np.ones((len(DIRS), 1)), DIRS])


def min_nec(M, R1, R2, beta, P, h):
    sh = build_shell(M, R1, R2, beta_warp=beta)
    Gab, G = einstein(make_g(sh), P, h)
    T = Gab / (8 * np.pi)
    worst = (np.inf, None)
    for k in range(len(P)):
        gk = G[k]; Gi = np.linalg.inv(gk)
        N = 1 / np.sqrt(-Gi[0, 0]); n = -N * Gi[:, 0]
        S = np.linalg.inv(np.linalg.cholesky(gk[1:, 1:])).T
        E = np.zeros((4, 4)); E[0] = n
        for A in range(3):
            E[A + 1, 1:] = S[:, A]
        Tf = E @ T[k] @ E.T
        m = np.einsum("na,ab,nb->n", KK, Tf, KK).min()
        if m < worst[0]:
            worst = (m, P[k])
    return worst


def static_dec_ratio(M, R1, R2):
    sh = build_shell(M, R1, R2)
    eps, pr, pt = sh.eps, sh.p_r, sh.p_t
    msk = eps > 1e-6 * eps.max()
    return float(np.max(np.maximum(np.abs(pr[msk]), np.abs(pt[msk])) / eps[msk]))


def beta_crit(M, R1, R2, nsteps=9):
    D = R2 - R1
    h = 0.0025 * D
    rs = np.linspace(R1 - 0.05 * D, R2 + 0.05 * D, 241)
    ang = np.pi / 4
    P = np.vstack([np.stack([np.zeros_like(rs), rs, np.zeros_like(rs)], 1),
                   np.stack([rs * np.cos(ang), rs * np.sin(ang), np.zeros_like(rs)], 1)])
    m0, _ = min_nec(M, R1, R2, 0.0, P, h)
    lo, hi = 0.0, 0.08
    mh, _ = min_nec(M, R1, R2, hi, P, h)
    if mh >= 0:
        return None, m0
    for _ in range(nsteps):
        mid = 0.5 * (lo + hi)
        m, p = min_nec(M, R1, R2, mid, P, h)
        if m < 0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi), m0


Gc, cc = 6.674e-11, 2.998e8
print("Part 1: fixed compactness, varying wall thickness")
M, R2 = 4.49e27, 20.0
C = 2 * Gc * M / (cc ** 2 * R2)
for R1 in (10.0, 15.0, 17.5, 18.5):
    D = R2 - R1
    bc, m0 = beta_crit(M, R1, R2)
    dec = static_dec_ratio(M, R1, R2)
    k = bc / (C * D / R2) if bc else float("nan")
    print(f"C = {C:.4f}, R1 = {R1:5.1f} m, Delta = {D:4.1f} m: beta_crit(NEC) = {bc:.5f}; "
          f"beta_crit/C = {bc / C:.4f}; k = beta_crit/(C Delta/R2) = {k:.3f}; zero-shift min NEC {m0:+.2e} m^-2; "
          f"static max|p|/eps = {dec:.3f}")

print("Part 2: fixed Delta/R2 = 0.5 (R1 = 10, R2 = 20 m), varying compactness")
for f in (0.25, 0.5, 1.0, 1.5, 2.0):
    Mf = f * 4.49e27
    Cf = 2 * Gc * Mf / (cc ** 2 * R2)
    try:
        bc, m0 = beta_crit(Mf, 10.0, 20.0)
        dec = static_dec_ratio(Mf, 10.0, 20.0)
        print(f"M = {Mf:.3e} kg, C = {Cf:.4f}: beta_crit(NEC) = {bc:.5f}; beta_crit/C = {bc / Cf:.4f}; "
              f"static max|p|/eps = {dec:.3f}")
    except Exception as e:  # noqa: BLE001
        print(f"M = {Mf:.3e} kg, C = {Cf:.4f}: build failed: {e}")
