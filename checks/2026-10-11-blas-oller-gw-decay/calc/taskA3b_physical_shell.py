#!/usr/bin/env python3
"""Task A(3), part 2 (and A(2) for the shell): eq. S6 in B&O's own approximations (narrow band, |k_i| = omega_s in
denominators, 2 pi delta(0) -> T, same N normalisation) but with the PHYSICAL tree amplitude for a DEFINITE coherent
state: H(n) = sum_l f_l(n) eps_l(n) with all phases, inserted into the full multilinear amplitude.

Output: C in dP/dt = C G^2 N^2 omega^3 sigma^2 (B&O eq. 8: C = 3/(25 pi) = 0.0381972), for the patterns
  bo_plus  : f_+ = f_- = real constant in the e_+- = (-+e_th - i e_ph)/sqrt2 convention = linear 'plus' along the
             meridians of a polar axis, isotropic magnitude (the literal reading of B&O's real f's; singular at poles)
  bo_cross : f_+ = -f_- (linear 'cross'), isotropic;  circ: pure helicity +2, isotropic;
  binary   : Lambda(n)(x+iy)(x+iy) (circular binary seen from all directions);  linear: Lambda(n) z z.
Engines: spinor closed form (bo_common, independent of qft_second_order) for the production numbers; the module's
amplitude_gg_to_photons on a coarse identical grid as a cross-check.  Usage: --part {bo_plus, smooth, aux, module}."""
import argparse
import math
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", ".claude", "skills", "conundrum", "scripts"))
import bo_ring as br  # noqa: E402

PI = math.pi
REF = 3 / (25 * PI)


def run(pat, grid, engine="spinor", **kw):
    t0 = time.time()
    if engine == "spinor":
        f = lambda k1, k2, q1, q2, s: br.m_photon_physical(k1, k2, q1, q2, s, pat)  # noqa: E731
    else:
        f = lambda k1, k2, q1, q2, s: br.m_photon_physical_module(k1, k2, q1, q2, s, pat)  # noqa: E731
    out = br.coefficient(f, **grid, **kw)
    return out, time.time() - t0


ap = argparse.ArgumentParser()
ap.add_argument("--part", required=True, choices=["bo_plus", "smooth", "aux", "module"])
ap.add_argument("--grid", type=int, default=0, help="bo_plus only: 1 or 2 runs one grid (0 = both)")
a = ap.parse_args()

if a.part == "bo_plus":
    print("pattern bo_plus (B&O-literal isotropic real-f shell), physical amplitudes, two grids:")
    grids = [dict(NK=8, NthK=8, nth=8, nph=24, na=32, c_pole=16),
             dict(NK=12, NthK=12, nth=10, nph=32, na=32, c_pole=24)]
    if a.grid:
        grids = [grids[a.grid - 1]]
    for grid in grids:
        (C, Ks, jK), dt = run("bo_plus", grid, return_K=True)
        print(f"   grid {grid}: C = {C:.7f};  C/(3/(25 pi)) = {C/REF:.5f}   [{dt:.0f} s]")
    # K-resolved comparison with the B&O model on the last grid's K nodes
    _, Ks2, jBO = br.coefficient(lambda k1, k2, q1, q2, s: br.m_photon_bo(k1, k2, q1, q2, s, "bo_plus"),
                                 NK=grid["NK"], NthK=4, nth=8, nph=16, na=32, return_K=True)
    print("   K-resolved ratio dC_phys/dK / dC_B&O/dK at the Gauss nodes (K in units of omega_s; s = 4 - K^2):")
    for K, jp, jb in zip(Ks, jK, jBO):
        print(f"      K = {K:.4f}:  {jp/jb:.4f}")

if a.part == "smooth":
    for pat in ("binary", "linear"):
        print(f"pattern {pat}, physical amplitudes, two grids:")
        for grid in (dict(NK=8, NthK=8, nth=8, nph=24, na=32),
                     dict(NK=12, NthK=12, nth=10, nph=32, na=48)):
            C, dt = run(pat, grid, splitK=False)
            print(f"   grid {grid}: C = {C:.8f};  C/(3/(25 pi)) = {C/REF:.6f}   [{dt:.0f} s]")
    Cbo = br.coefficient(lambda k1, k2, q1, q2, s: br.m_photon_bo(k1, k2, q1, q2, s, "linear"),
                         NK=16, NthK=16, nth=10, nph=32, na=64, splitK=False)
    print(f"   B&O model with the same linear-quadrupole profile: C = {Cbo:.8f} (C/(3/(25 pi)) = {Cbo/REF:.6f});"
          f"  physical/B&O-model for this profile = {C/Cbo:.5f}")

if a.part == "aux":
    g = dict(NK=6, NthK=6, nth=6, nph=16, na=32, c_pole=8)
    Cp, _ = run("bo_plus", g)
    Cc, _ = run("bo_cross", g)
    Ci, _ = run("circ", g)
    print(f"coarse grid {g}:  bo_plus C/(3/(25pi)) = {Cp/REF:.10f};  bo_cross = {Cc/REF:.10f}"
          f" (identical: only f_+(k1) f_-(k2) products enter and (-i)(+i) = 1);  circ = {Ci:.3e} (exact zero:"
          " no opposite-helicity pairs)")
    for pat, kw in (("bo_plus", dict(c_pole=8)), ("binary", {})):
        g2 = dict(NK=6, NthK=6, nth=6, nph=16, na=32)
        C0 = br.coefficient(lambda k1, k2, q1, q2, s: br.m_photon_physical(k1, k2, q1, q2, s, pat), **g2, **kw)
        C1 = br.coefficient(lambda k1, k2, q1, q2, s: br.m_photon_physical(k1, k2, q1, q2, s, pat), **g2, **kw,
                            phiK=0.7)
        print(f"axisymmetry check {pat}: C(phi_K = 0) = {C0:.10f}, C(phi_K = 0.7) = {C1:.10f}")

if a.part == "module":
    g = dict(NK=3, NthK=3, nth=3, nph=8, na=16, c_alpha=4.0)
    for pat, kw in (("bo_plus", dict(c_pole=4)), ("binary", {}), ("linear", dict(splitK=False))):
        Cs, ts = run(pat, g, "spinor", **kw)
        Cm, tm = run(pat, g, "module", **kw)
        print(f"identical coarse grid {g} {kw}: {pat}: spinor C = {Cs:.12e}, module C = {Cm:.12e},"
              f" rel. diff = {abs(Cs/Cm-1):.1e}   [{ts:.0f} s, {tm:.0f} s]")
