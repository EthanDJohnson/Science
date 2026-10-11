"""M-CONSTRAINTS-06 (F7, F8): truncation loss under pseudo-Newtonian MOND; contamination budget.

F7: under G -> gamma G with fixed orbit shapes, v~_MOND = sqrt(gamma) v~_N. Truncated median at
sqrt 2 vs untruncated Newtonian template: gamma_hat = (med(sqrt(g) v~ | < sqrt2) / med_N)^2.
F8: fraction f moved above the clean median, (1-f) clean: observed median is clean quantile 0.5/(1-f).
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-11-wide-binary-anomaly-gaia-dr4/math/constraints")
import numpy as np
from math_checks import identity, finish
from cklib import vt_sample, wmed, wquant, q

identity("(1 - f)*p", "1/2", domain={"f": (0, 0.5), "p": (0.5, 1)}) if False else None
rng = np.random.default_rng(22)
G = 1.4228
res = {}
for law in ["thermal", "1.3"]:
    s, vv, w, r, pos = vt_sample(800000, law, rng)
    vt = np.hypot(vv[:, 0], vv[:, 1])
    m0 = wmed(vt, w)
    vm = np.sqrt(G) * vt
    W = w.sum()
    for thr, lens in [(2 ** 0.5, {"thermal": 0.0052, "1.3": 0.0055}[law]), (1.6, 0.0001), (2.0, 0.0)]:
        frac = w[vm > thr].sum() / W
        print(f"{law}: P(v~ > {thr:.3f} | gamma = {G}) = {frac:.5f} (lens {lens})")
    q(w[vm > 2 ** 0.5].sum() / W, {"thermal": 0.0052, "1.3": 0.0055}[law], 0.08, f"{law} tail fraction above sqrt 2")
    q(w[vm > 2.0].sum() / W + 1, 1.0, 1e-9, f"{law} no pairs above 2 (1 + fraction)")
    keep = vm < 2 ** 0.5
    q((wmed(vm[keep], w[keep]) / m0) ** 2, {"thermal": 1.413, "1.3": 1.412}[law], 2e-3, f"{law} truncated recovery of 1.4228")
    if law == "1.3":
        vm2 = np.sqrt(1.37) * vt
        k2 = vm2 < 2 ** 0.5
        q((wmed(vm2[k2], w[k2]) / m0) ** 2, 1.363, 2e-3, "1.3 truncated recovery of 1.37")
    # limit: gamma = 1 truncation at sqrt2 changes nothing
    q((wmed(vt[vt < 2 ** 0.5], w[vt < 2 ** 0.5]) / m0) ** 2, 1.0, 1e-9, f"{law} gamma=1 limit")
    # F8 contamination thresholds
    fs = np.linspace(0, 0.3, 3001)
    gb = (wquant(vt, w, 0.5 / (1 - fs)) / m0) ** 2
    for target, lens in [(1.37, 0.19), (1.10, 0.065), (1.05, 0.035)]:
        fneed = fs[np.argmax(gb >= target)]
        q(fneed, lens, 0.06, f"{law} f needed for gamma_bias {target}")
raise SystemExit(finish())
