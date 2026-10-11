"""M-CONSTRAINTS-09 (F11): spurious gamma from an eccentricity-law mismatch, full median.

gamma_fake(alpha_true; alpha_tmpl) = (med_alpha_true / med_alpha_tmpl)^2, f(e) ~ e^alpha (alpha > -1).
Lens: tmpl 1.3 vs true 1.17 -> 1.026; true 2 -> 0.912; faking 1.37 needs alpha ~ 0.0 (tmpl 1.2 and 1.3);
1.20 needs 0.31 (0.39); 1.10 needs 0.69 (0.80).
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-11-wide-binary-anomaly-gaia-dr4/math/constraints")
import numpy as np
from math_checks import finish
from cklib import vt_sample, wmed, q

rng = np.random.default_rng(55)
med = {}
alphas = [-0.9, -0.7, -0.5, -0.3, 0.0, 0.2, 0.31, 0.39, 0.5, 0.69, 0.8, 1.0, 1.17, 1.2, 1.3, 2.0]
for a in alphas:
    s, vv, w, r, pos = vt_sample(500000, str(a), rng)
    med[a] = wmed(np.hypot(vv[:, 0], vv[:, 1]), w)
for tmpl in [1.2, 1.3]:
    print(f"template alpha {tmpl}: " + ", ".join(f"a={a}: {(med[a]/med[tmpl])**2:.3f}" for a in alphas))
q((med[1.17] / med[1.3]) ** 2, 1.026, 5e-3, "tmpl 1.3, true 1.17")
q((med[2.0] / med[1.3]) ** 2, 0.912, 5e-3, "tmpl 1.3, true 2")
q((med[0.31] / med[1.2]) ** 2, 1.20, 1e-2, "tmpl 1.2, true 0.31 -> 1.20")
q((med[0.39] / med[1.3]) ** 2, 1.20, 1e-2, "tmpl 1.3, true 0.39 -> 1.20")
q((med[0.69] / med[1.2]) ** 2, 1.10, 1e-2, "tmpl 1.2, true 0.69 -> 1.10")
q((med[0.80] / med[1.3]) ** 2, 1.10, 1e-2, "tmpl 1.3, true 0.80 -> 1.10")
q((med[0.0] / med[1.3]) ** 2, 1.37, 1e-2, "tmpl 1.3, true alpha 0 (uniform) -> lens says 1.37 needs alpha ~ 0")
q((med[0.0] / med[1.2]) ** 2, 1.37, 1e-2, "tmpl 1.2, true alpha 0 (uniform)")
q(med[1.3] / med[1.3], 1.0, 1e-12, "matched-template limit")
raise SystemExit(finish())
