"""falsifier-C1-2 (part 3): weak-field rows of the thick-wall design scan; helpers copied from part 2.
toward a vanishing cavity and the Buchdahl end, and check sampling convergence.

Same definitions and units as part 1 (geometric for curvature, SI masses; beta covariant shift
in units of c). beta_NEC is a sampled upper bound on the NEC-safe shift; beta_int =
(1 - e^{2a(0)})/2 is a NECESSARY (not sufficient) shift for any one-way light advance.
"""
import sys
import math
import time
sys.path.insert(0, "runs/2026-10-01-warp-drive-without-negative-energy/tools")
sys.path.insert(0, "runs/2026-10-01-warp-drive-without-negative-energy/calc")
import numpy as np
from warp_shell import build_shell
import importlib.util

spec = importlib.util.spec_from_file_location(
    "dg", "runs/2026-10-01-warp-drive-without-negative-energy/calc/falsifier-C1-2_design_gap.py")
# re-implement the helpers instead of importing (the part-1 module runs its table on import)
from numeric_stress_energy import NumericSpacetime

G = 6.67430e-11
c = 2.99792458e8


def make_pts(R1, R2, n=40, angles=(90.0, 45.0)):
    rs = np.linspace(max(R1 - 0.05 * (R2 - R1), 0.2), R2 + 0.05 * (R2 - R1), n)
    pts = []
    for ang in angles:
        th = math.radians(ang)
        for r in rs:
            pts.append([0.0, r * math.cos(th), 0.0, r * math.sin(th)])
    return np.array(pts)


def nec_viol(shell, beta, pts, h):
    shell.beta_warp = beta

    def g(t, x, y, z):
        return np.moveaxis(shell.metric_cartesian(t, x, y, z), [-2, -1], [0, 1])
    s = NumericSpacetime(g, h=h).scan_energy_conditions(pts)
    return s["violations"]["nec"]


def beta_nec(shell, pts, h, hi=0.7, steps=11):
    if nec_viol(shell, 0.0, pts, h) > 0:
        return None
    if nec_viol(shell, hi, pts, h) == 0:
        return float("inf")
    lo = 0.0
    for _ in range(steps):
        mid = 0.5 * (lo + hi)
        if nec_viol(shell, mid, pts, h) > 0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


def row(R1, R2, Cc, n=40, hfrac=0.005, angles=(90.0, 45.0), label=""):
    t0 = time.time()
    M = Cc * c ** 2 * R2 / (2 * G)
    try:
        shell = build_shell(M=M, R1=R1, R2=R2, beta_warp=0.0)
    except Exception as e:  # noqa
        print(f"{R1:5.2f} {R2:5.1f} | {Cc:.3f} | build failed: {e}")
        return None
    lapse = float(shell.lapse_static(0.0))
    b_int = (1 - lapse ** 2) / 2
    bn = beta_nec(shell, make_pts(R1, R2, n, angles), hfrac * (R2 - R1))
    if bn is None:
        print(f"{R1:5.2f} {R2:5.1f} | {Cc:.3f} | lapse {lapse:.4f} | beta_int {b_int:.4f} | beta=0 sample not NEC-clean (FD noise) {label}")
        return None
    print(f"{R1:5.2f} {R2:5.1f} | {Cc:.3f} | lapse {lapse:.4f} | beta_int {b_int:.4f} | beta_NEC {bn:.4f} | beta_NEC/C {bn/Cc:.4f} | required/achievable {b_int/bn:.2f} {label} [{time.time()-t0:.0f}s]")
    return b_int / bn


print("part 3: weak-field limit, thick walls (same definitions as part 2)")
fac = []
for R1 in (0.5, 2.0, 10.0):
    for Cc in (0.01, 0.1):
        fac.append(row(R1, 20.0, Cc))
fac = [f for f in fac if f is not None]
print(f"smallest required/achievable factor in part 3: {min(fac):.2f}")
