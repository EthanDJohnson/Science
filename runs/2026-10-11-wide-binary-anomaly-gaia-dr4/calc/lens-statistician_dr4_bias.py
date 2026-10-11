"""Statistician lens: per-family bias of gamma in the DR4 scoring bin, from the run's calculators.

Generator: wide_binary_population.generate (DR4 noise preset); estimators: wide_binary_estimators.
Scoring bin: log10(g_N [m s^-2]) in [-10.5, -9.5) (contains 1e-10, wholly below 10^-9.5), g_N proxy
= G M_est / (1.2 s)^2 as output by the generator. Calibration bin (Chae-style f_multi): [-8.5, -7.0).
Estimator template: KeplerTemplate(alpha_e=1.25, lam=1.6) (Hwang-type alpha at 1-10 kau [D-41]).
Usage: python3 ... [config names...]   (default: all)
"""
import sys
import time
import math
import numpy as np

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from wide_binary_population import generate, gamma_mond
from wide_binary_estimators import gamma_per_bin, KeplerTemplate, run_estimator, est_full_median, _Forward

N = 100000
BIN = (-10.5, -9.5)
CAL = (-8.5, -7.0)
TMPL = KeplerTemplate(alpha_e=1.25, lam=1.6, n=200000, seed=101)

CONFIGS = {
    "N_t0.1": dict(gravity=1.0, f_triple=0.1),
    "N_t0.2": dict(gravity=1.0, f_triple=0.2),
    "N_t0.3": dict(gravity=1.0, f_triple=0.3),
    "N_t0.2_thermal": dict(gravity=1.0, f_triple=0.2, ecc="thermal"),
    "N_t0.2_mass0.9": dict(gravity=1.0, f_triple=0.2, mass_bias=0.9),
    "N_t0.2_ca0.02": dict(gravity=1.0, f_triple=0.2, f_chance=0.01, f_unbound=0.01),
    "M_bz18_t0.2": dict(gravity="bz18_simple", f_triple=0.2),
    "M_chae_t0.2": dict(gravity="chae2024", f_triple=0.2),
    "M_bz18_t0.3": dict(gravity="bz18_simple", f_triple=0.3),
    "N_t0.2_seed2": dict(gravity=1.0, f_triple=0.2),
    "M_bz18_t0.2_seed2": dict(gravity="bz18_simple", f_triple=0.2),
    "N_t0.2_DR3": dict(gravity=1.0, f_triple=0.2, release="DR3"),
    "M_bz18_t0.2_DR3": dict(gravity="bz18_simple", f_triple=0.2, release="DR3"),
}


def vt_of(cat, mask):
    G = 6.674e-11
    vc = np.sqrt(G * cat["M_est"][mask] / cat["s"][mask])
    return cat["v_p"][mask] / vc


def run(name, cfg, seed):
    t0 = time.time()
    cfg = dict(cfg)
    rel = cfg.pop("release", "DR4")
    cat = generate(N, release=rel, d_range=(10 * 3.0857e16, 250 * 3.0857e16), seed=seed, **cfg)
    lg = np.log10(cat["gN"])
    mb = (lg >= BIN[0]) & (lg < BIN[1])
    mc = (lg >= CAL[0]) & (lg < CAL[1])
    true_g = float(np.median(cat["gamma"][mb]))
    common = dict(gN=cat["gN"], sigma_vp=cat["sigma_vp"], sigma_lnM=0.05, bins=BIN, template=TMPL,
                  n_model=100000)
    out = {}
    for est, kw in [("median", {}), ("threshold", dict(v_cut=1.4)), ("trimmed", dict(p_trim=0.1)),
                    ("mixture", dict(n_boot=30)),
                    ("bayes", dict(alphas=[0.8, 1.25, 2.0], lam=1.6, n_boot=10))]:
        r = gamma_per_bin(cat["s"], cat["v_p"], cat["M_est"], estimator=est, **common, **kw)
        out[est] = (r[0]["gamma"], r[0]["sigma_boot"], r[0]["N_bin"])
    # Chae-style: calibrate f_multi so that median-gamma = 1 in the high-acceleration bin, carry it over
    G = 6.674e-11
    vc = np.sqrt(G * cat["M_est"] / cat["s"])
    sp = cat["sigma_vp"] / vc
    sm = np.full(sp.shape, 0.05)
    fw_c = _Forward(TMPL, sp[mc], sm[mc], n_model=100000, seed=21)
    vtc = cat["v_p"][mc] / vc[mc]
    fgrid = [0.0, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4]
    gc = [est_full_median(vtc, fw_c, f_multi=f, n_boot=2)["gamma"] for f in fgrid]
    # gamma decreases with f_multi; interpolate f where gamma = 1
    f_cal = float(np.interp(1.0, gc[::-1], fgrid[::-1])) if min(gc) < 1 < max(gc) else (0.0 if max(gc) <= 1 else fgrid[-1])
    fw_b = _Forward(TMPL, sp[mb], sm[mb], n_model=100000, seed=22)
    rc = est_full_median(cat["v_p"][mb] / vc[mb], fw_b, f_multi=f_cal, n_boot=30)
    out["median_fcal"] = (rc["gamma"], rc["sigma_boot"], int(mb.sum()))
    # empirical ratio calibration (no forward model): (Q_data/Q_calib)^2
    re = est_full_median(cat["v_p"][mb] / vc[mb], calib_vt=vtc, n_boot=30)
    out["median_empcal"] = (re["gamma"], re["sigma_boot"], int(mb.sum()))
    print(f"\n[{name}] seed={seed} true median gamma in bin={true_g:.3f} N_bin={int(mb.sum())} N_cal={int(mc.sum())} "
          f"f_cal={f_cal:.3f} (cal-bin gammas {[round(x,3) for x in gc]}) t={time.time()-t0:.0f}s")
    for k, (g, sb, nb) in out.items():
        print(f"   {k:14s} gamma={g:.3f} sigma_boot={sb:.3f} N={nb} bias(gamma/true)={g/true_g:.3f}")
    return out


if __name__ == "__main__":
    print("MOND gamma at g_N=1e-10: bz18_simple", round(float(gamma_mond(1e-10, 'bz18_simple')), 3),
          " chae2024", round(float(gamma_mond(1e-10, 'chae2024')), 3), " at 10^-10.5:",
          round(float(gamma_mond(10**-10.5, 'bz18_simple')), 3), round(float(gamma_mond(10**-10.5, 'chae2024')), 3))
    names = sys.argv[1:] or list(CONFIGS)
    for i, nm in enumerate(names):
        run(nm, CONFIGS[nm], seed=1000 + i)
