"""M-DIALECTICIAN-08 (F2, cand C): light-based mass deficit. A component of mass m with an unresolved companion q m
(0 < q <= 1) has L = m^3.5 (1 + q^3.5), so m_est = m (1 + q^3.5)^(1/3.5) <= m (1 + q). Then v~_obs = v~_N sqrt(R),
R = M_true/M_est >= 1, per system (a per-system rescaling). The lens says this is *the cause* of the p = 0.3 shift
gamma(0.3) = 1.133 (low bin) and ~1.096 (high bin) at f_triple = 0.2 in the generator.
Here: the size of the mass-only shift, with the generator's stated population (mB/mA ~ U(0.2, 1), q_in ~ U(0.1, 1),
companion in A or B with equal probability, L ~ m^3.5), and an own Kepler sampler."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-11-wide-binary-anomaly-gaia-dr4/math/dialectician")
import numpy as np
import sympy as sp
from math_checks import inequality, limit, quantity, finish
from kep import sample_e, kepler_vtilde, gamma_profile

q = sp.symbols("q", positive=True)
inequality("1 + q", ">=", "(1 + q**3.5)**(1/3.5)", domain={"q": (0, 1)})
limit("(1 + q**3.5)**(1/3.5)", "q", 0, 1)        # no companion: no deficit

n = 300000
rng = np.random.default_rng(31)
mA = np.ones(n); mB = rng.uniform(0.2, 1.0, n)
qin = rng.uniform(0.1, 1.0, n); inB = rng.random(n) < 0.5
Mtrue = mA + mB + qin * np.where(inB, mB, mA)
Mest = np.where(inB, mA + mB * (1 + qin ** 3.5) ** (1 / 3.5), mA * (1 + qin ** 3.5) ** (1 / 3.5) + mB)
R = Mtrue / Mest
print(f"R = M_true/M_est for a triple: mean {R.mean():.4f}, median {np.median(R):.4f}, 10-90% {np.quantile(R, [0.1, 0.9]).round(4)}")
tmpl = kepler_vtilde(n, sample_e(n, "power", rng, alpha=1.3), rng)
vt = kepler_vtilde(n, sample_e(n, "power", rng, alpha=1.3), rng)
for f in (0.1, 0.2, 0.3):
    trip = rng.random(n) < f
    obs = vt * np.sqrt(np.where(trip, R, 1.0))
    gp = gamma_profile(obs, tmpl, ps=(0.3, 0.5, 0.8))
    print(f"mass-only, f={f}: gamma(.3,.5,.8) = {np.round(gp, 4)}, S = {gp[2] / gp[0]:.4f}")
    if f == 0.2:
        g03 = gp[0]
# compare with the lens's generator values at f=0.2: 1.133 (low), 1.096 (high)
print(f"mass-only gamma(0.3) excess {g03 - 1:.4f} vs lens low-bin 0.133, high-bin 0.096 -> fraction {((g03 - 1) / 0.133):.2f} / {((g03 - 1) / 0.096):.2f}")
quantity(f"{g03}", "1.133", rel_tol=0.03)        # expected to FAIL if the mass channel alone is too small
raise SystemExit(finish())
