#!/usr/bin/env python3
"""Decomposer lens: does DR4 remove the triple lever? Split hidden inner binaries by inner semi-major
axis: a_in in [0.1, 5] au (P_in <~ 11 yr for ~1 Msun, i.e. within ~2x the DR4 66-month baseline,
plausibly flagged by DR4 epoch astrometry / acceleration solutions) vs a_in in [5, 300] au
(P_in >~ 11 yr; mostly NOT flagged). Newtonian truth, DR4 noise preset, HTZ f(e), f_triple = 0.3
assigned wholly to one sub-population at a time, and to the full log-uniform [0.1, 300] au range.
Output: apparent gamma (median-vt ratio squared) in CAL (g_N > 10^-8.5 m/s^2) and TEST
(10^-10.5..10^-9.5 m/s^2) bins, and their ratio (the part a Newtonian-bin calibration can't remove).
Note: log-uniform a_in on [0.1, 300] au puts ln(50)/ln(3000) = 49% of inner binaries below 5 au
before the stability cut.
"""
import sys
import numpy as np

sys.path.insert(0, "runs/2026-10-11-wide-binary-anomaly-gaia-dr4/tools")
import wide_binary_population as wbp  # noqa: E402

G = 6.674e-11
AU = wbp.AU
N = 120000
CAL = (10 ** -8.5, 1e-6)
TEST = (10 ** -10.5, 10 ** -9.5)


def meds(cat):
    v = cat["v_p"] / np.sqrt(G * cat["M_est"] / cat["s"])
    g = cat["gN"]
    return [np.median(v[(g > lo) & (g <= hi)]) for lo, hi in (CAL, TEST)]


def gen(**kw):
    base = dict(n=N, gravity=1.0, ecc="htz", release="DR4", seed=5)
    base.update(kw)
    return wbp.generate(**base)


ref = meds(gen(f_triple=0.0))
print(f"DR4 noise, pure Newtonian: median vt CAL = {ref[0]:.4f}, TEST = {ref[1]:.4f}")
for lab, rng_ in (("all a_in 0.1-300 au", (0.1 * AU, 300 * AU)),
                  ("short a_in 0.1-5 au (DR4-flaggable)", (0.1 * AU, 5 * AU)),
                  ("long a_in 5-300 au (not flagged)", (5 * AU, 300 * AU))):
    m = meds(gen(f_triple=0.3, a_in_range=rng_, seed=6))
    gc, gt = (m[0] / ref[0]) ** 2, (m[1] / ref[1]) ** 2
    print(f"f_triple=0.3, {lab}: gamma_app CAL = {gc:.3f}, TEST = {gt:.3f}, TEST/CAL = {gt / gc:.3f}")
# DR3 vs DR4 noise for the full population
ref3 = meds(gen(f_triple=0.0, release="DR3"))
m3 = meds(gen(f_triple=0.3, release="DR3", seed=6))
print(f"DR3 noise, f=0.3 all a_in: CAL = {(m3[0] / ref3[0]) ** 2:.3f}, TEST = {(m3[1] / ref3[1]) ** 2:.3f}, "
      f"TEST/CAL = {(m3[1] / ref3[1]) ** 2 / (m3[0] / ref3[0]) ** 2:.3f}")
