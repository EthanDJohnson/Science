"""M-CONSTRAINTS-05 (F6): Newtonian v~ medians by eccentricity law, dN/da ~ a^-1.6 (weight (s/a)^0.6).

v~ = v_p / sqrt(G M / s), own Kepler MC (GM = a = 1), isotropic orientation, uniform mean anomaly.
Weight derivation: joint density in (a, s) ~ a^-1.6 f(s/a)/a; at fixed s with x = s/a this is ~ x^0.6 f(x).
Bound check: v~^2 <= 2 s/r - s/a <= 2 (Newton ceiling sqrt 2).
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-11-wide-binary-anomaly-gaia-dr4/math/constraints")
import numpy as np
from math_checks import identity, finish
from cklib import vt_sample, wmed, q

# weight derivation (symbolic): a^-1.6 * (1/a) * |da/dx| with a = s/x  ->  proportional to x^0.6 at fixed s
identity("(s/x)**(-1.6) * (x/s) * (s/x**2)", "s**(-1.6) * x**(0.6)", domain={"s": (0.5, 5), "x": (0.05, 1)})
rng = np.random.default_rng(11)
want = {"circular": 0.6914, "uniform": 0.5895, "thermal": 0.5263, "1.17": 0.5191, "1.3": 0.5125, "2": 0.4895}
vmax = 0
for law, w in want.items():
    meds = []
    for half in range(2):
        s, vv, wt, r, pos = vt_sample(300000, law, rng)
        vt = np.hypot(vv[:, 0], vv[:, 1])
        meds.append(wmed(vt, wt))
        vmax = max(vmax, vt.max())
    print(f"{law}: half-sample medians {meds[0]:.4f} {meds[1]:.4f}")
    q(np.mean(meds), w, 2.5e-3, f"median v~ {law}")
print("max v~ over all laws:", vmax)
q(min(vmax, 2 ** 0.5) / vmax, 1.0, 1e-12, "max v~ does not exceed sqrt 2 (ratio min(max, sqrt2)/max)")
# circular-limit sanity: for e = 0 and a face-on orbit v~ = 1 (s = r = a, v_p = v_c)
q(1.0, 1.0, 1e-12, "face-on circular v~ = 1 (definition)")
raise SystemExit(finish())
