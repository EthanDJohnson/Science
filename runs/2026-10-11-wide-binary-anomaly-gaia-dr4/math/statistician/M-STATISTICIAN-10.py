"""M-STATISTICIAN-10: gap decomposition arithmetic (finding 11) and the size of the mass-bias and
eccentricity-template shifts (finding 9, failure modes, cand E).
v~ = v_p / sqrt(G M_est / s) (dimensionless). gamma_est = (median v~_obs / median v~_template)^2.
Independent Kepler Monte Carlo, units G = M = a = 1 (dimensionless), pure binaries, no triples, no noise:
random mean anomaly, isotropic orientation, f(e) = (alpha+1) e^alpha."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
import sympy as sp
from math_checks import identity, limit, finish
from _h import report

ok = []
# --- gap decomposition (finding 11)
ok += [report("total gap 1.37-1.045", 1.37 - 1.045, 0.33, 0.006),
       report("median-vs-robust low", 1.12 - 1.045, 0.07, 0.006), report("median-vs-robust high", 1.20 - 1.045, 0.15, 0.006),
       report("pipeline low", 1.37 - 1.20, 0.17, 0.001), report("pipeline high", 1.37 - 1.12, 0.25, 0.001)]

# --- mass scaling: v~ propto M_est^(-1/2) so gamma_est propto 1/M_est
M, Me, v, s = sp.symbols("M_true M_est v s", positive=True)
gam = (v / sp.sqrt(Me / s)) ** 2 / (v / sp.sqrt(M / s)) ** 2
identity(gam, M / Me)
limit(gam, "M_est", M, 1)
fac = 1 / 0.9
print(f"10% mass underestimate multiplies gamma_est by {fac:.4f}")
print(f"  applied to the lens's own f_t=0.2 baselines: median 1.11-1.15 -> {1.11*fac:.3f}-{1.15*fac:.3f} "
      f"(increment {1.11*fac-1.11:.3f}-{1.15*fac-1.15:.3f}); mixture 1.01-1.04 -> {1.01*fac:.3f}-{1.04*fac:.3f} "
      f"(increment {1.01*fac-1.01:.3f}-{1.04*fac-1.04:.3f})")
print("  lens cand E states the mass shift as '+0.28 (median) and +0.15 (mixture)': these equal total gamma-1 "
      "at f_t=0.2 (1.28, 1.15), not the increment due to mass.")

# --- eccentricity template shift, independent Kepler MC
rng = np.random.default_rng(7)


def vtilde(alpha, n=1_000_000):
    e = rng.random(n) ** (1 / (alpha + 1))
    Mn = rng.random(n) * 2 * np.pi
    E = Mn.copy()
    for _ in range(60):
        E -= (E - e * np.sin(E) - Mn) / (1 - e * np.cos(E))
    rr = 1 - e * np.cos(E)
    pos = np.stack([np.cos(E) - e, np.sqrt(1 - e**2) * np.sin(E), np.zeros(n)])
    vel = np.stack([-np.sin(E) / rr, np.sqrt(1 - e**2) * np.cos(E) / rr, np.zeros(n)])
    # isotropic rotation via random unit quaternion
    q = rng.normal(size=(4, n)); q /= np.linalg.norm(q, axis=0)
    w, x, y, z = q
    R = np.array([[1 - 2*(y*y+z*z), 2*(x*y-z*w), 2*(x*z+y*w)],
                  [2*(x*y+z*w), 1 - 2*(x*x+z*z), 2*(y*z-x*w)],
                  [2*(x*z-y*w), 2*(y*z+x*w), 1 - 2*(x*x+y*y)]])
    P = np.einsum("ijn,jn->in", R, pos); V = np.einsum("ijn,jn->in", R, vel)
    sp_ = np.hypot(P[0], P[1]); vp = np.hypot(V[0], V[1])
    # energy check: v^2 = 2/r - 1
    assert np.allclose((vel**2).sum(0), 2 / rr - 1, rtol=1e-8)
    return vp * np.sqrt(sp_), rr, e


vt_c, r_c, _ = vtilde(1.0)
print(f"self-check bound: max v~ = {vt_c.max():.4f} <= sqrt(2) = {2**0.5:.4f}")
ok.append(vt_c.max() <= 2**0.5 + 1e-9)
med = {a: np.median(vtilde(a)[0]) for a in (0.0, 1.0, 1.25, 1.3, 2.0)}
for a, m in med.items():
    print(f"  alpha={a}: median v~ = {m:.4f}")
shift = (med[1.0] / med[1.25]) ** 2
shift13 = (med[1.0] / med[1.3]) ** 2
print(f"thermal truth analysed with alpha=1.25 template: gamma_est = {shift:.4f} (shift {shift-1:+.3f}); "
      f"with alpha=1.3 template: {shift13:.4f} (shift {shift13-1:+.3f})")
print(f"  applied multiplicatively to the lens's f_t=0.2 median baseline 1.11-1.15: {1.11*shift:.3f}-{1.15*shift:.3f} "
      "(lens sim: 1.177)")
ok.append(report("lens claim 'thermal vs alpha=1.3 changes median by +0.18'", shift13 - 1, 0.18, 0.03))
# time-average check <r> = a(1 + e^2/2) for thermal: E[r] = 1 + E[e^2]/2 = 1 + 1/4
ok.append(report("<r>/a thermal = 1 + <e^2>/2 = 1.25", r_c.mean(), 1.25, 0.003))
print("ALL NUMERIC CHECKS OK" if all(ok) else "SOME NUMERIC CHECK DIFFERS")
raise SystemExit(finish())
