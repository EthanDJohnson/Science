#!/usr/bin/env python3
"""Decomposer lens: which premises can move gamma in a median (family-1) low-g bin, and by how much.

Computes, with the run's generator (tools/wide_binary_population.py), SI units internally:
 A. Apparent gamma from hidden triples in a CALIBRATION bin (g_N > 10^-8.5 m/s^2) and a TEST bin
    (10^-10.5 < g_N < 10^-9.5 m/s^2), Newtonian truth, DR3 noise, f_triple in {0,.1,.2,.3}.
    gamma_app(bin) = (median vt(f) / median vt(f=0, same bin))^2.  The ratio test/cal is what
    survives a calibration that fixes f on the Newtonian bin (premise 2 of the brief).
 B. Delta f_triple needed in the TEST bin (with f fixed at the calibration value) for the
    family-1 median to reproduce Chae 2024b Gamma = 0.068 (gamma = 1.37).
 C. Eccentricity gradient: apparent gamma in the TEST bin when the template is HTZ (alpha ~1.2-1.3)
    but the truth is alpha = 2 (Banik+24 fit) or uniform; and in the CAL bin, to get the
    differential.
 D. Tail truncation at vt < sqrt(2): fraction of bound pure binaries lost at gamma = 1 and at
    the MOND preset, and median shift of the truncated sample.
 E. Required differential mass bias to fake gamma = 1.37: M_est/M_true(test)/(cal) = 1/1.37.
"""
import sys
import numpy as np

sys.path.insert(0, "runs/2026-10-11-wide-binary-anomaly-gaia-dr4/tools")
import wide_binary_population as wbp  # noqa: E402

G = 6.674e-11
N = 120000
CAL = (10 ** -8.5, 1e-6)
TEST = (10 ** -10.5, 10 ** -9.5)


def vt(cat):
    return cat["v_p"] / np.sqrt(G * cat["M_est"] / cat["s"])


def binmask(cat, rng_):
    g = cat["gN"]
    return (g > rng_[0]) & (g <= rng_[1])


def med_bins(cat):
    v = vt(cat)
    out = {}
    for name, b in (("cal", CAL), ("test", TEST)):
        m = binmask(cat, b)
        out[name] = (np.median(v[m]), int(m.sum()))
    return out


def gen(**kw):
    base = dict(n=N, ecc="htz", release="DR3", seed=11, s_range=(200 * wbp.AU, 30000 * wbp.AU))
    base.update(kw)
    return wbp.generate(**base)


print("=== A. hidden triples, Newtonian truth, DR3 noise, HTZ eccentricities ===")
ref = med_bins(gen(gravity=1.0, f_triple=0.0))
print(f"f=0: median vt cal = {ref['cal'][0]:.4f} (N={ref['cal'][1]}), test = {ref['test'][0]:.4f} (N={ref['test'][1]})")
gam = {}
for f in (0.1, 0.2, 0.3):
    r = med_bins(gen(gravity=1.0, f_triple=f, seed=11 + int(100 * f)))
    gc = (r["cal"][0] / ref["cal"][0]) ** 2
    gt = (r["test"][0] / ref["test"][0]) ** 2
    gam[f] = (gc, gt)
    print(f"f_triple={f:.1f}: gamma_app cal = {gc:.3f}, test = {gt:.3f}, "
          f"differential test/cal = {gt / gc:.3f}  (dimensionless)")

print("\n=== B. Delta f_triple in TEST bin needed for median-ratio^2 = 1.37 (Gamma = 0.068) ===")
target = 10 ** (2 * 0.068)
print(f"target gamma = 10^(2*0.068) = {target:.3f}")
fs = np.array([0.0, 0.1, 0.2, 0.3])
gts = np.array([1.0] + [gam[f][1] for f in (0.1, 0.2, 0.3)])
for fcal in (0.0, 0.1, 0.2):
    gcal = np.interp(fcal, fs, gts)
    need = gcal * target
    if need <= gts.max():
        fneed = np.interp(need, gts, fs)
        print(f"f_cal={fcal:.1f}: test-bin gamma_app(f_cal)={gcal:.3f}; need test gamma_app={need:.3f} -> f_test ~ {fneed:.2f} (Delta f ~ {fneed - fcal:+.2f})")
    else:
        # extrapolate linearly from last two points
        slope = (gts[-1] - gts[-2]) / 0.1
        fneed = 0.3 + (need - gts[-1]) / slope
        print(f"f_cal={fcal:.1f}: need test gamma_app={need:.3f} > grid max; linear extrapolation f_test ~ {fneed:.2f} (Delta f ~ {fneed - fcal:+.2f})")

print("\n=== C. eccentricity truth vs HTZ template (Newtonian, f=0) ===")
for lab, kw in (("power alpha=2.0", dict(ecc="power", ecc_alpha=2.0)),
                ("power alpha=1.0 (thermal)", dict(ecc="power", ecc_alpha=1.0)),
                ("uniform", dict(ecc="uniform"))):
    r = med_bins(gen(gravity=1.0, f_triple=0.0, seed=21, **kw))
    gc = (r["cal"][0] / ref["cal"][0]) ** 2
    gt = (r["test"][0] / ref["test"][0]) ** 2
    print(f"truth {lab}: gamma_app cal = {gc:.3f}, test = {gt:.3f}, differential = {gt / gc:.3f}")
print("(HTZ truth in cal bin is alpha~1.2 at ~1 kau; a truth that becomes MORE eccentric only at wide s gives the 'test' column alone)")

print("\n=== D. truncation at vt < sqrt(2): pure binaries, DR3 noise ===")
for lab, grav in (("Newton", 1.0), ("MOND bz18_simple", "bz18_simple"), ("MOND chae2024", "chae2024")):
    c = gen(gravity=grav, f_triple=0.0, seed=31)
    v = vt(c)
    m = binmask(c, TEST)
    vv = v[m]
    frac = np.mean(vv > np.sqrt(2))
    print(f"{lab}: test-bin N={m.sum()}, median vt = {np.median(vv):.4f}, P(vt>sqrt2) = {frac:.4f}, "
          f"median of vt<sqrt2 = {np.median(vv[vv < np.sqrt(2)]):.4f}, mean gamma(truth) = {np.mean(c['gamma'][m]):.3f}")
gN0 = 1e-10
print(f"gamma_mond(1e-10 m/s^2): bz18_simple = {wbp.gamma_mond(gN0, model='bz18_simple'):.3f}, "
      f"chae2024 = {wbp.gamma_mond(gN0, model='chae2024'):.3f}, bz18_standard = {wbp.gamma_mond(gN0, model='bz18_standard'):.3f}")

print("\n=== E. mass bias needed ===")
print(f"differential M_est/M_true (test relative to cal) to fake gamma=1.37 under Newton: {1 / 1.37:.3f} (i.e. {100 * (1 - 1 / 1.37):.1f}% underestimate at low g only)")
print("a common-mode mass bias b multiplies gamma in every bin by 1/b and cancels in a calibrated ratio")
