"""M-CONSTRAINTS-02 (F2, K1): bound-orbit ceiling on v~ in the EF-dominated MOND potential.

Statement: Phi = -(G M nu_e / r)(1 + K sin^2 th / 2), K in (-1/2, 0). Bound (E < 0), s <= r,
v_p <= v  =>  v~^2 = v_p^2 s/(G M) <= 2 nu_e (1 + K sin^2/2) s/r <= 2 nu_e. Same for AQUAL
(max |phi| r/GM = 1/mu_e = nu_e along the EF). Newton (nu_e = 1, K = 0): v~ <= sqrt 2.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-11-wide-binary-anomaly-gaia-dr4/math/constraints")
import mpmath as mp
from math_checks import inequality, sign, finish
from cklib import ef_state, qumond_ef, q

mp.mp.dps = 25
gx = mp.mpf("1.785")
# chain of inequalities (symbolic sampling): 2 nu (1 + K S/2) u <= 2 nu, S = sin^2 in [0,1], u = s/r in (0,1]
inequality("2*nu*(1 + K*w/2)*u", "<=", "2*nu", domain={"nu": (1, 2), "K": (-0.5, 0), "w": (0, 1), "u": (1e-6, 1)})
for name in ["simple", "MLS", "n1.5", "standard"]:
    ye, nue, K = ef_state(name, gx)
    sign(f"-({float(K)})", "positive")   # K < 0, so the max of eta(theta) is at theta = 0 (parallel)
    # AQUAL: L = -K/(1+K); max over theta of 1/(mu_e sqrt(1+L) sqrt(sin^2 + cos^2/(1+L)))
    L = -K / (1 + K)
    f = lambda c: nue / (mp.sqrt(1 + L) * mp.sqrt(1 - c * c + c * c / (1 + L)))
    amax = max(f(mp.mpf(i) / 1000) for i in range(0, 1001))
    q(amax, float(nue), 1e-6, f"{name} AQUAL max |phi| r/GM equals nu_e")
want = {"simple": 1.766, "MLS": 1.737, "n1.5": 1.589, "standard": 1.514}
for name, w in want.items():
    ye, nue, K = ef_state(name, gx)
    q(mp.sqrt(2 * nue), w, 6e-4, f"{name} v~_max")
# scalar-gamma ceiling and the 4.7% gap
ye, nue, K = ef_state("simple", gx)
g = qumond_ef("simple", gx)
q(mp.sqrt(2 * g), 1.687, 6e-4, "sqrt(2 gamma) simple")
q(mp.sqrt(2 * nue) / mp.sqrt(2 * g) - 1, 0.047, 0.03, "ceiling excess")
# ratio to Cookson 2.5 cut
q(2.5 / mp.sqrt(2 * nue), 1.4, 0.02, "2.5 / 1.766")
# Newton limit: nu_e = 1, K = 0 gives sqrt 2
q(mp.sqrt(2 * 1 * (1 + 0)), 1.41421356, 1e-8, "Newton ceiling")
raise SystemExit(finish())
