"""Dialectician lens: scale-vs-shape test and companion-veto ladder.

Synthesis 1 (C1): under the pseudo-Newtonian G_eff = gamma G model, a real boost RESCALES the
whole v~ distribution by sqrt(gamma), so gamma(p) = (Q_p,obs / Q_p,Newt)^2 is flat in the
quantile p. Unmodelled hidden companions change the SHAPE: gamma(p) rises with p.
Synthesis 3 (C3): a velocity-blind companion veto (wobble/RUWE-like) cannot remove a real
boost from pure binaries, but removes a contamination-made one; gamma vs veto strength is
flat (MOND) or falls toward 1 (Newton + triples).

Uses the run's generator (truth) and an independent clean Newtonian catalogue (same
population, same noise, f_triple = 0, other seed) as the calibration template.
Units: SI inside; g_N in m s^-2; wobble in mas. gamma dimensionless.
"""
import sys
import numpy as np
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import wide_binary_population as wbp  # noqa: E402

N = 120000
PS = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
LOW = (-11.0, -9.5)   # scoring-like bin, log10 g_N [m s^-2] (proxy g_N = G M_est/(1.2 s)^2)
HIGH = (-8.5, -7.5)   # Newtonian calibration bin
VC_CUT = 5.0          # drop v~ > 5 everywhere (emulates the El-Badry-type PM cut, crude)


def cat(gravity, f_triple, seed, release="DR3", ecc="htz"):
    return wbp.generate(N, gravity=gravity, f_triple=f_triple, seed=seed, release=release, ecc=ecc)


def sel(c, b, extra=None):
    lg = np.log10(c["gN"])
    m = (lg >= b[0]) & (lg < b[1]) & (c["vtilde"] < VC_CUT)
    if extra is not None:
        m &= extra
    return c["vtilde"][m]


def gprof(vt, vt_ref):
    return (np.quantile(vt, PS) / np.quantile(vt_ref, PS)) ** 2


def fmt(a):
    return " ".join(f"{x:6.3f}" for x in a)


for rel in ("DR3", "DR4"):
    print(f"===== release {rel} =====")
    ref = cat(1.0, 0.0, 999, rel)
    ref_lo, ref_hi = sel(ref, LOW), sel(ref, HIGH)
    print(f"template N(low bin) = {ref_lo.size}, N(high bin) = {ref_hi.size}")
    print("quantiles p:            " + fmt(PS))
    cases = [("Newton f_t=0.0", 1.0, 0.0), ("Newton f_t=0.1", 1.0, 0.1), ("Newton f_t=0.2", 1.0, 0.2),
             ("Newton f_t=0.3", 1.0, 0.3), ("MOND chae2024 f_t=0", "chae2024", 0.0),
             ("MOND chae2024 f_t=0.2", "chae2024", 0.2), ("const 1.4 f_t=0", 1.4, 0.0),
             ("const 1.4 f_t=0.2", 1.4, 0.2)]
    for i, (lab, gr, ft) in enumerate(cases):
        c = cat(gr, ft, 10 + i, rel)
        lo, hi = sel(c, LOW), sel(c, HIGH)
        gl, gh = gprof(lo, ref_lo), gprof(hi, ref_hi)
        S = gl[7] / gl[2]
        print(f"{lab:22s} LOW  gamma(p): {fmt(gl)} | median {gl[4]:.3f} | S=g(0.8)/g(0.3) {S:.3f} | N {lo.size}")
        print(f"{'':22s} HIGH gamma(p): {fmt(gh)} | median {gh[4]:.3f} | S {gh[7]/gh[2]:.3f}")
        if rel == "DR4" and ft > 0:
            # companion-veto ladder: veto pairs with photocentre wobble above threshold (mas)
            for thr in (np.inf, 1.0, 0.3, 0.1, 0.03, 0.01):
                keep = c["wobble_mas"] <= thr
                v = sel(c, LOW, keep)
                frac_trip = np.mean((c["flags"][keep] & 3) > 0)
                gm = (np.median(v) / np.median(ref_lo)) ** 2
                print(f"{'':22s}   veto wobble>{thr:<6} : gamma_med(low) {gm:.3f}  surviving triple frac {frac_trip:.3f}  N_low {v.size}")
    # scale-free check: eccentricity mismatch (truth uniform / alpha=2, template htz), Newton, no triples
    for lab, ecc in (("Newton ecc=uniform", "uniform"), ("Newton ecc=thermal", "thermal")):
        c = cat(1.0, 0.0, 77, rel, ecc=ecc)
        gl = gprof(sel(c, LOW), ref_lo)
        print(f"{lab:22s} LOW  gamma(p): {fmt(gl)} | median {gl[4]:.3f} | S {gl[7]/gl[2]:.3f}")
