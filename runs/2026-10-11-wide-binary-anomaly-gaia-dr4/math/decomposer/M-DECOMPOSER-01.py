"""M-DECOMPOSER-01: mass-bias scaling of an apparent gamma, and the gradient needed to fake 1.37.

Definitions (independent of the lens):
  v~ = v_p / sqrt(G M_est / s)  (dimensionless).  Under Keplerian dynamics with G -> gam*G,
  v_p = sqrt(gam G M_true / s) * u, with u the dimensionless orbit/projection factor whose
  distribution does not depend on M or gam (self-similarity of Kepler orbits).
  Mass bias b = M_est/M_true > 0.  Apparent gamma from a median estimator:
  gam_app = (median v~ / median v~_Newton-template)^2, template = Newtonian with true masses.
  Calibrated (differential) estimator: gam_diff = gam_app(TEST)/gam_app(CAL).
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, quantity, units, inequality, finish

gam, G, M, s, u, b, bT, bC, gT, gC = sp.symbols("gam G M s u b b_T b_C g_T g_C", positive=True)

vp = sp.sqrt(gam * G * M / s) * u
vt_obs = vp / sp.sqrt(G * b * M / s)
vt_template = sp.sqrt(G * M / s) * u / sp.sqrt(G * M / s)   # Newton, true mass
gam_app = sp.simplify((vt_obs / vt_template) ** 2)
# 1. gam_app = gam / b  (median is equivariant under a positive scale factor)
identity(gam_app, gam / b)
# 2. limit b -> 1 recovers gam
limit(gam / b, "b", 1, gam)
# 3. common-mode bias cancels in the calibrated ratio
ratio = (gT / bT) / (gC / bC)
identity(ratio.subs(bT, bC), gT / gC)
# 4. gradient needed: under Newton (gT = gC = 1) ratio = bC/bT = 1.37 -> bT/bC = 1/1.37
quantity("1/1.37", "0.730", rel_tol=1e-3)
quantity("1/1.368", "0.731", rel_tol=1e-3)
# 5. a low-g underestimate raises gamma (sign): bT < bC => ratio > 1
inequality(1 / sp.Symbol("x", positive=True), ">", 1, domain={"x": (0.5, 0.999)})
# 6. units: v / sqrt(G M / s) is dimensionless
units("(1 km/s) / (6.674e-11 m^3/(kg s^2) * 1.989e30 kg / (1.496e14 m))^0.5", "dimensionless")
raise SystemExit(finish())
