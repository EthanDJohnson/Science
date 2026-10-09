"""falsifier-C1-2: required vs achievable shift across shell designs (scale attack on C1's FTL half).

Question: can a positive-energy (NEC-clean) warp shell of the Fuchs et al. 2024 family be
re-proportioned (wall thickness, compactness) so that its NEC-safe shift beta_NEC reaches the
shift needed for the interior forward light speed to exceed c, beta_int = (1 - e^{2a(0)})/2?
(beta_int is a NECESSARY condition for any one-way light advance through the shell; the net
advance between exterior rest points also has to beat the exterior Shapiro delay, so the true
requirement is higher -- see lens-decomposer_thresholds.py.)

Units: geometric (G = c = 1, lengths in m) for curvature; masses SI (kg). beta is the covariant
interior shift g_0x in units of c. Tools: the run's warp_shell rebuild and numeric_stress_energy
(all-observer NEC by finite differences). Sampling: two radial lines (90 and 45 deg to the shift
axis) across the wall; bisection on beta in [0, 0.6]. The resulting beta_NEC is an UPPER bound on
the true NEC cap (more points could only lower it).
"""
import sys
import math
import time
sys.path.insert(0, "runs/2026-10-01-warp-drive-without-negative-energy/tools")
import numpy as np
from warp_shell import build_shell
from numeric_stress_energy import NumericSpacetime

G = 6.67430e-11
c = 2.99792458e8


def make_pts(R1, R2, n=40):
    rs = np.linspace(max(R1 - 0.05 * (R2 - R1), 0.3), R2 + 0.05 * (R2 - R1), n)
    pts = []
    for ang in (90.0, 45.0):
        th = math.radians(ang)
        for r in rs:
            pts.append([0.0, r * math.cos(th), 0.0, r * math.sin(th)])
    return np.array(pts)


def nec_viol(shell, beta, pts, h):
    shell.beta_warp = beta

    def g(t, x, y, z):
        return np.moveaxis(shell.metric_cartesian(t, x, y, z), [-2, -1], [0, 1])
    st = NumericSpacetime(g, h=h)
    s = st.scan_energy_conditions(pts)
    return s["violations"]["nec"], s


def beta_nec(shell, pts, h, hi=0.6, steps=11):
    v0, _ = nec_viol(shell, 0.0, pts, h)
    if v0 > 0:
        return None, v0
    vhi, _ = nec_viol(shell, hi, pts, h)
    if vhi == 0:
        return float("inf"), 0
    lo = 0.0
    for _ in range(steps):
        mid = 0.5 * (lo + hi)
        v, _ = nec_viol(shell, mid, pts, h)
        if v > 0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi), 0


designs = [
    # (R1, R2, compactness C = 2GM/(c^2 R2))
    (10.0, 20.0, 0.3334),   # published geometry and mass (toolkit rebuild)
    (10.0, 20.0, 0.10),
    (10.0, 20.0, 0.60),
    (5.0, 20.0, 0.3334),    # thicker wall
    (2.0, 20.0, 0.3334),    # very thick wall, small cavity
    (16.0, 20.0, 0.3334),   # thin wall
    (5.0, 20.0, 0.70),      # thick wall, high compactness
]

print("R1[m] R2[m] | C=2GM/c^2R2 | M[kg] | lapse e^a(0) | beta_int=(1-e^2a)/2 | beta_NEC (sampled upper bound) | beta_NEC/C | required/achievable | runtime")
rows = []
for R1, R2, Cc in designs:
    t0 = time.time()
    M = Cc * c ** 2 * R2 / (2 * G)
    try:
        shell = build_shell(M=M, R1=R1, R2=R2, beta_warp=0.0)
    except Exception as e:  # noqa
        print(f"{R1:5.1f} {R2:5.1f} | {Cc:.4f} | build failed: {e}")
        continue
    lapse = float(shell.lapse_static(0.0))
    b_int = (1 - lapse ** 2) / 2
    h = 0.005 * (R2 - R1)
    pts = make_pts(R1, R2)
    bn, v0 = beta_nec(shell, pts, h)
    if bn is None:
        print(f"{R1:5.1f} {R2:5.1f} | {Cc:.4f} | {M:.3e} | {lapse:.4f} | {b_int:.4f} | beta=0 already shows {v0} NEC violations on the sample (FD noise or TOV sheet) | -- | -- | {time.time()-t0:.0f}s")
        continue
    ratio = b_int / bn if bn > 0 else float("inf")
    rows.append((R1, R2, Cc, lapse, b_int, bn))
    print(f"{R1:5.1f} {R2:5.1f} | {Cc:.4f} | {M:.3e} | {lapse:.4f} | {b_int:.4f} | {bn:.4f} | {bn/Cc:.4f} | {ratio:.1f} | {time.time()-t0:.0f}s")

# analytic thin-shell comparison: interior lapse sqrt(1-C) -> beta_int = C/2
print("\nthin-shell analytic (interior lapse sqrt(1-C)): beta_int = C/2; with the run's NEC cap ratio beta_NEC/C ~ 0.07-0.09 the required/achievable factor is 0.5/0.09 = %.1f to 0.5/0.07 = %.1f" % (0.5 / 0.09, 0.5 / 0.07))
print("Buchdahl end (C = 8/9): thin-shell beta_int = %.3f vs generous cap 0.08 -> factor %.1f" % (8 / 18, (8 / 18) / 0.08))
if rows:
    worst = min(r[4] / r[5] for r in rows if r[5] > 0)
    print(f"smallest required/achievable factor among sampled designs: {worst:.2f}")
