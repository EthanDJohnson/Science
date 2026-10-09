#!/usr/bin/env python3
"""Constraints lens: the largest interior shift beta_crit a positive-energy warp shell allows
before the NEC fails anywhere (all observers, exact type-I tests where type I), as a function
of the shell's compactness, transition buffer Rb and smoothing span. Built with warp_shell.py
(Fuchs et al. 2024 construction) and numeric_stress_energy.py (FD, h = 0.05 m).
Geometric units for T (1/m^2). Bisection on beta over a dense (r, angle) grid of the shift
transition region; a point counts as a violation only on the robust verdict.
Also checks the scale invariance: (M, R1, R2) -> (10 M, 10 R1, 10 R2) must give the same beta_crit.
"""
import math
import sys
import time

import numpy as np

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from numeric_stress_energy import NumericSpacetime  # noqa: E402
from warp_shell import build_shell  # noqa: E402

C, G = 299792458.0, 6.67430e-11
M0, R1, R2 = 4.49e27, 10.0, 20.0


def gfun(shell):
    def g(t, x, y, z):
        G4 = shell.metric_cartesian(t, x, y, z)
        return [[G4[..., a, b] for b in range(4)] for a in range(4)]
    return g


def grid(R1, R2, nr=30, nth=21):
    rr = np.linspace(R1 + 0.005 * (R2 - R1), R2 - 0.005 * (R2 - R1), nr)
    th = np.linspace(0.02, math.pi - 0.02, nth)
    return np.array([(0.0, a * math.cos(b), a * math.sin(b), 0.0) for a in rr for b in th])


def nviol(M, R1, R2, beta, Rb=0.0, span_P=None, h=None):
    kw = dict(beta_warp=beta, Rb=Rb)
    if span_P is not None:
        kw["span_P"] = span_P
    shell = build_shell(M, R1, R2, **kw)
    hh = h if h is not None else 0.005 * (R2 - R1)
    st = NumericSpacetime(gfun(shell), h=hh)
    sc = st.scan_energy_conditions(grid(R1, R2))
    return sc["violations"]["nec"], sc["violations"]["dec"], sc["unconverged"], sc["points"]


def beta_crit(M, R1, R2, Rb=0.0, span_P=None, lo=0.0, hi=0.2, it=9):
    n_hi = nviol(M, R1, R2, hi, Rb, span_P)[0]
    if n_hi == 0:
        return None, hi
    for _ in range(it):
        mid = 0.5 * (lo + hi)
        if nviol(M, R1, R2, mid, Rb, span_P)[0] > 0:
            hi = mid
        else:
            lo = mid
    return lo, hi


def main():
    t0 = time.time()
    print("published shell M = 4.49e27 kg, R1 = 10 m, R2 = 20 m, Rb = 0, default smoothing:")
    for b in (0.02, 0.025, 0.03, 0.035, 0.04):
        n, d, u, p = nviol(M0, R1, R2, b)
        print(f"  beta {b:.3f}: NEC violations {n}/{p}, DEC {d}, unconverged {u}")
    lo, hi = beta_crit(M0, R1, R2)
    print(f"  beta_crit in [{lo:.4f}, {hi:.4f}]  [{time.time()-t0:.0f}s]")
    print("  h check at beta = 0.03 and 0.033: ", [nviol(M0, R1, R2, b, h=hh)[:3] for b in (0.03, 0.033) for hh in (0.1, 0.05, 0.025)])
    print("sensitivity to compactness (same R1, R2):")
    for fac in (0.25, 0.5, 1.0, 1.5):
        comp = 2 * G * M0 * fac / (C ** 2 * R2)
        try:
            lo, hi = beta_crit(M0 * fac, R1, R2)
            print(f"  M = {fac:.2f} x published (2GM/c^2R2 = {comp:.3f}): beta_crit in [{lo:.4f}, {hi:.4f}];"
                  f" beta_crit/compactness = {0.5*(lo+hi)/comp:.4f}")
        except ValueError as exc:
            print(f"  M = {fac:.2f} x: refused ({exc})")
    print("sensitivity to the transition buffer Rb and the smoothing span (published M):")
    for Rb in (1.0, 2.0):
        lo, hi = beta_crit(M0, R1, R2, Rb=Rb)
        print(f"  Rb = {Rb} m: beta_crit in [{lo:.4f}, {hi:.4f}]")
    for sp_ in (0.5, 2.0):
        lo, hi = beta_crit(M0, R1, R2, span_P=sp_)
        print(f"  span_P = {sp_} m: beta_crit in [{lo:.4f}, {hi:.4f}]")
    print("scale invariance: (M, R1, R2) x 10 (payload radius 100 m):")
    lo, hi = beta_crit(10 * M0, 10 * R1, 10 * R2)
    print(f"  M = 4.49e28 kg, R1 = 100 m, R2 = 200 m: beta_crit in [{lo:.4f}, {hi:.4f}]  [{time.time()-t0:.0f}s total]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
