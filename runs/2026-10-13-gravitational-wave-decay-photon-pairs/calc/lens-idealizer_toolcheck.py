#!/usr/bin/env python3
"""lens-idealizer_toolcheck: log, through math_run, the run tool's numbers this lens cites (F7) and test the
kinetic proxy behind F5/F6 against the coherent amplitude.

(1) Coherent two-cap yield (helicity +2 cap along x, -2 cap along y, angular width delta, Gaussian band sigma)
    vs the kinetic two-beam rate x position-space overlap 4-volume. Agreement means that, for crossing coherent
    beams, the coherent in-out yield IS the local kinetic rate integrated over the overlap: the geometric-optics
    rate density Gamma(x) = (2 pi/5) G^2 T_mu_nu T^mu_nu used in F5/F6 is the coherent result in that limit.
(2) Pattern coefficients c_tot (top hat, photons) for bo_real_sign, circular_binary, linear_quadrupole.
Natural units (hbar = c = 1, w = 1, G = 1 in the tool's internal calls).
"""
import sys
import time
import math

sys.path.insert(0, "runs/2026-10-13-gravitational-wave-decay-photon-pairs/tools")
import gw_coherent_fusion as gf  # noqa: E402
import qft_second_order as q2  # noqa: E402

PI = math.pi

print("=== (1) coherent caps vs kinetic beams x overlap ===")
for delta, sig in ((0.04, 0.002), (0.08, 0.004)):
    t0 = time.time()
    P, A = gf._two_cap_yield(delta, sig)
    br = q2.beams_pair_rate(1.0, 1e-3, 1.0, 1e-3, PI / 2, "R", "L", G=1.0)
    ref = br["pair_rate"] / (1e-3 / math.sqrt(32 * PI)) ** 4 * A ** 4 * gf._overlap_4volume(delta, sig)
    print(f"delta = {delta}, sigma = {sig}: caps P = {P:.6g}, kinetic beams x overlap = {ref:.6g}, "
          f"ratio = {P / ref:.5f} ({time.time() - t0:.1f} s)")

print("\n=== (2) pattern coefficients, top hat, photons ===")
for p in ("bo_real_sign", "circular_binary", "linear_quadrupole"):
    t0 = time.time()
    c = gf.coefficients(p, "tophat", "photon")
    print(f"{p:18s} c_tot = {c['c_tot']:.6g}  c_rate = {c['c_rate']:.6g}  rate/B&O = {c['ratio_to_BO']:.4g} "
          f"({time.time() - t0:.1f} s)")
