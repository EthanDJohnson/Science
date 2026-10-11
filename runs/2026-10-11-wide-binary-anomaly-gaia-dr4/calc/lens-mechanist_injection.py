#!/usr/bin/env python3
"""Mechanist lens: independent injection-recovery of the four estimator families.

Generator: tools wide_binary_population.generate (run's calculator, not Boufourou's code).
Estimators: wide_binary_estimators (never imports the generator).

Design (all SI internally; printed gamma dimensionless, s in kau, g_N in m s^-2):
  * TEST catalogue: observed s in [2, 30] kau, d in [10, 200] pc, constant injected gamma
    (1.0, 1.2, 1.4) -- "gamma above 2 kau", as in Boufourou's MOND truth.
  * CALIB catalogue: s in [0.2, 2] kau, gamma = 1 (Newtonian regime), same f_triple.
  * Quality cuts on both (fiducial, Boufourou-like): sigma_vtilde < 0.10; RUWE-like cut
    wobble_mas < WOB_CUT (assumed proxy for RUWE < ~1.4).
  * Scoring bin: log10 g_N proxy (G M_est / (1.2 s)^2) in [-11, -9.5] m s^-2.
  * Calibration bin: log10 g_N in [-8.5, -7.0] m s^-2 (Chae's ~1e-8 regime).
Estimators run in the scoring bin:
  E1a full-median, pure Newtonian template (noise-matched, no triples)
  E1b full-median, Chae-style empirical calibration: gamma = (med_low / med_calib)^2
  E1c full-median, template with f_multi calibrated in the high-g bin and carried over
  E2a tail-truncated threshold likelihood, v~ < 1.40 (Boufourou E2-like)
  E2b tail-truncated trimmed mean, p = 0.10
  E3  mixture likelihood (binary + triple-kick + chance), v~ < 5
  E4  simplified Bayesian deprojection, alpha_e marginalised over {0.8, 1.0, 1.3, 1.6}
Template eccentricity exponent alpha_e = 1.3 (Hwang+22 at 1-10 kau), lam = 1.6 (generator slope).
"""
import sys
import time
import math
import numpy as np

sys.path.insert(0, ".claude/skills/conundrum/scripts")
import wide_binary_population as wbp  # noqa: E402
import wide_binary_estimators as wbe  # noqa: E402

G = wbp.G
AU = wbp.AU
LOW_BIN = (-11.0, -9.5)
CAL_BIN = (-8.5, -7.0)
WOB_CUT = 0.10      # mas, RUWE-like cut (assumption)
SIG_CUT = 0.10      # sigma_vtilde cut
N_BOOT = 15
N_MODEL = 200000


def cuts(cat, wob_cut=WOB_CUT, sig_cut=SIG_CUT):
    vc = np.sqrt(G * cat["M_est"] / cat["s"])
    ok = (cat["sigma_vp"] / vc < sig_cut)
    if wob_cut is not None:
        ok &= cat["wobble_mas"] < wob_cut
    return ok


def binsel(cat, ok, b):
    lg = np.log10(cat["gN"])
    return ok & (lg >= b[0]) & (lg < b[1])


def vt_of(cat, m):
    return cat["v_p"][m] / np.sqrt(G * cat["M_est"][m] / cat["s"][m])


def run_case(f_triple, gamma_inj, ecc="htz", ecc_alpha=None, mass_bias=1.0, mass_bias_low=None,
             err_inflate=1.0, f_chance=0.0, f_unbound=0.0, tmpl_alpha=1.3, a_in_range=(0.1 * AU, 300 * AU),
             n_test=100000, n_cal=60000, seed=1, which=("E1a", "E1b", "E1c", "E2a", "E2b", "E3", "E4"),
             wob_cut=WOB_CUT, release="DR3"):
    """Return dict estimator -> (gamma, sigma_boot) in LOW_BIN, plus N."""
    mb_low = mass_bias if mass_bias_low is None else mass_bias_low
    test = wbp.generate(n_test, gravity=gamma_inj, ecc=ecc, ecc_alpha=ecc_alpha, f_triple=f_triple,
                        f_chance=f_chance, f_unbound=f_unbound, err_inflate=err_inflate,
                        mass_bias=mb_low, s_range=(2000 * AU, 30000 * AU), a_in_range=a_in_range,
                        release=release, seed=seed)
    cal = wbp.generate(n_cal, gravity=1.0, ecc=ecc, ecc_alpha=ecc_alpha, f_triple=f_triple,
                       f_chance=f_chance, f_unbound=0.0, err_inflate=err_inflate, mass_bias=mass_bias,
                       s_range=(200 * AU, 2000 * AU), a_in_range=a_in_range, release=release,
                       seed=seed + 1000)
    okt, okc = cuts(test, wob_cut), cuts(cal, wob_cut)
    mlow, mcal = binsel(test, okt, LOW_BIN), binsel(cal, okc, CAL_BIN)
    vt_low, vt_cal = vt_of(test, mlow), vt_of(cal, mcal)
    vc_low = np.sqrt(G * test["M_est"][mlow] / test["s"][mlow])
    vc_cal = np.sqrt(G * cal["M_est"][mcal] / cal["s"][mcal])
    sp_low = test["sigma_vp"][mlow] / vc_low
    sp_cal = cal["sigma_vp"][mcal] / vc_cal
    sm_low = np.full(vt_low.size, 0.07)   # two components each 0.05 in ln m -> ~0.035-0.05 on M; generous
    sm_cal = np.full(vt_cal.size, 0.07)
    tm = wbe.KeplerTemplate(alpha_e=tmpl_alpha, lam=1.6)
    out = dict(N_low=int(vt_low.size), N_cal=int(vt_cal.size),
               frac_trip_low=float(np.mean(test["flags"][mlow] & 3 > 0)),
               med_low=float(np.median(vt_low)), med_cal=float(np.median(vt_cal)))
    R = {}
    if "E1a" in which:
        r = wbe.run_estimator("median", vt_low, sp_low, sm_low, template=tm, n_model=N_MODEL, n_boot=N_BOOT)
        R["E1a"] = (r["gamma"], r["sigma_boot"])
    if "E1b" in which:
        g = (np.median(vt_low) / np.median(vt_cal)) ** 2
        rng = np.random.default_rng(5)
        bs = [(np.median(rng.choice(vt_low, vt_low.size)) / np.median(rng.choice(vt_cal, vt_cal.size))) ** 2
              for _ in range(100)]
        R["E1b"] = (float(g), float(np.std(bs)))
    if "E1c" in which:
        # calibrate f_multi so the template median returns gamma = 1 in the calibration bin
        fws = wbe._Forward(tm, sp_cal, sm_cal, n_model=N_MODEL, seed=11)
        fgrid = np.linspace(0.0, 0.6, 13)
        gcal = []
        for f in fgrid:
            gcal.append(wbe.est_full_median(vt_cal, fws, f_multi=f, n_boot=0)["gamma"]
                        if True else None)
        gcal = np.array(gcal)
        # gamma decreases with f; pick f where gcal crosses 1
        if gcal[0] <= 1.0:
            fcal = 0.0
        elif gcal[-1] >= 1.0:
            fcal = fgrid[-1]
        else:
            fcal = float(np.interp(1.0, gcal[::-1], fgrid[::-1]))
        r = wbe.run_estimator("median", vt_low, sp_low, sm_low, template=tm, n_model=N_MODEL,
                              n_boot=N_BOOT, f_multi=fcal)
        R["E1c"] = (r["gamma"], r["sigma_boot"])
        out["f_multi_cal"] = fcal
    if "E2a" in which:
        r = wbe.run_estimator("threshold", vt_low, sp_low, sm_low, template=tm, n_model=N_MODEL,
                              n_boot=N_BOOT, v_cut=1.40)
        R["E2a"] = (r["gamma"], r["sigma_boot"])
    if "E2b" in which:
        r = wbe.run_estimator("trimmed", vt_low, sp_low, sm_low, template=tm, n_model=N_MODEL,
                              n_boot=N_BOOT, p_trim=0.10)
        R["E2b"] = (r["gamma"], r["sigma_boot"])
    if "E3" in which:
        r = wbe.run_estimator("mixture", vt_low, sp_low, sm_low, template=tm, n_model=N_MODEL,
                              n_boot=N_BOOT, v_max=5.0)
        R["E3"] = (r["gamma"], r["sigma_boot"])
        out["E3_ftrip"] = r["f_triple"]
        out["E3_fca"] = r["f_ca"]
    if "E4" in which:
        r = wbe.run_estimator("bayes", vt_low, sp_low, sm_low, template=tm, n_model=N_MODEL,
                              n_boot=10, alphas=[0.8, 1.0, 1.3, 1.6], lam=1.6, v_max=5.0)
        R["E4"] = (r["gamma"], r["sigma_boot"])
    out["R"] = R
    return out


def fmt(out, label):
    s = " ".join(f"{k}={v[0]:.3f}±{v[1]:.3f}" for k, v in out["R"].items())
    extra = ""
    if "f_multi_cal" in out:
        extra += f" fmulti_cal={out['f_multi_cal']:.3f}"
    if "E3_ftrip" in out:
        extra += f" E3_ftrip={out['E3_ftrip']:.3f}"
    print(f"{label} | N_low={out['N_low']} N_cal={out['N_cal']} trip_frac_low_after_cuts="
          f"{out['frac_trip_low']:.3f} med_low={out['med_low']:.4f} med_cal={out['med_cal']:.4f}{extra} | {s}",
          flush=True)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "grid"
    t0 = time.time()
    if mode == "quick":
        o = run_case(0.2, 1.0, n_test=30000, n_cal=20000)
        fmt(o, "quick f=0.2 g=1.0")
    elif mode == "grid":
        print("GRID: rows f_triple x gamma_inj; columns estimator gamma in log g_N bin [-11,-9.5] m s^-2")
        for g in (1.0, 1.2, 1.4):
            for f in (0.0, 0.1, 0.2, 0.3):
                o = run_case(f, g, seed=int(100 * f + 10 * g))
                fmt(o, f"f_triple={f:.1f} gamma_inj={g:.1f}")
    elif mode == "nocut":
        print("NO RUWE-LIKE CUT (wobble cut off): Newtonian truth")
        for f in (0.1, 0.2, 0.3):
            o = run_case(f, 1.0, wob_cut=None, seed=int(100 * f) + 7)
            fmt(o, f"[no wobble cut] f_triple={f:.1f} gamma_inj=1.0")
    print(f"elapsed {time.time() - t0:.1f} s")
