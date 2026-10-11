"""M-DIALECTICIAN-07 (F1): eccentricity-template mismatch gives a falling quantile profile (S < 1), extra velocity from
hidden companions gives a rising one (S > 1). Own Kepler sampler, noise-free, scale-free (v~ independent of a).
Template f(e) ~ e^1.3 (HTZ value at ~1-3 kau; the low bin is s ~ 4-25 kau for M ~ 1.5 Msun).
Lens (DR3, with noise and the generator's a-dependent HTZ alpha): S = 0.835 (true uniform), 0.979 (true thermal)."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-11-wide-binary-anomaly-gaia-dr4/math/dialectician")
import numpy as np
from math_checks import quantity, finish
from kep import sample_e, kepler_vtilde, gamma_profile

n = 300000
rng = np.random.default_rng(21)
tmpl = kepler_vtilde(n, sample_e(n, "power", rng, alpha=1.3), rng)
out = {}
for kind, alp in (("uniform", None), ("thermal", None), ("power", 1.6)):
    vt = kepler_vtilde(n, sample_e(n, kind, rng, alpha=alp), rng)
    gp = gamma_profile(vt, tmpl, ps=(0.3, 0.5, 0.8))
    S = gp[2] / gp[0]
    out[kind] = S
    print(f"true {kind}{'' if alp is None else ' alpha=' + str(alp)} vs template e^1.3: gamma(.3,.5,.8) = {np.round(gp, 4)}, S = {S:.4f}")
quantity(f"{min(out['uniform'], 0.999)}", f"{out['uniform']}", rel_tol=1e-12)   # S < 1 for a too-eccentric template
quantity(f"{min(out['thermal'], 0.999)}", f"{out['thermal']}", rel_tol=1e-12)
quantity(f"{max(out['power'], 1.0)}", f"{out['power']}", rel_tol=1e-12)        # template too circular -> S > 1
quantity(f"{out['uniform']}", "0.835", rel_tol=0.06)
quantity(f"{out['thermal']}", "0.979", rel_tol=0.03)
# limit: identical f(e) gives S -> 1
vt = kepler_vtilde(n, sample_e(n, "power", rng, alpha=1.3), rng)
gp = gamma_profile(vt, tmpl, ps=(0.3, 0.5, 0.8)); print("same f(e): S =", round(gp[2] / gp[0], 4))
quantity(f"{gp[2] / gp[0]}", "1", rel_tol=0.01)
# hidden-companion velocity: 20% of pairs get an extra isotropic sky-plane vector of rms 0.5 v_c(s) (v~ units)
vt = kepler_vtilde(n, sample_e(n, "power", rng, alpha=1.3), rng)
k = rng.random(n) < 0.2
ang = rng.uniform(0, 2 * np.pi, n)
ex = np.abs(rng.standard_normal(n)) * 0.5
th0 = rng.uniform(0, 2 * np.pi, n)
vx = vt * np.cos(th0) + np.where(k, ex * np.cos(ang), 0); vy = vt * np.sin(th0) + np.where(k, ex * np.sin(ang), 0)
gp = gamma_profile(np.hypot(vx, vy), tmpl, ps=(0.3, 0.5, 0.8))
print("20% extra velocity: gamma(.3,.5,.8) =", np.round(gp, 4), " S =", round(gp[2] / gp[0], 4))
quantity(f"{max(gp[2] / gp[0], 1.0)}", f"{gp[2] / gp[0]}", rel_tol=1e-12)
raise SystemExit(finish())
