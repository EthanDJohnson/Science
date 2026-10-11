"""M-MECHANIST-04: an unmodelled Gaussian noise σ per sky axis in ṽ units biases a median-based γ by
γ_obs/γ_true - 1 = (median|ṽ + n| / median|ṽ|)^2 - 1. Lens (F2, 'crude quadrature'): +1.3% at σ = 0.05,
+5.3% at σ = 0.10. Truth: Newtonian Kepler, p(e) ∝ e^α (α = 1.3 and α = 1.0 tested), isotropic, uniform mean anomaly.
Quadrature estimate: (m² + 2σ²)/m² - 1 = 2σ²/m², m = median ṽ."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts"); sys.path.insert(0, "runs/2026-10-11-wide-binary-anomaly-gaia-dr4/math/mechanist")
import numpy as np, sympy as sp
from math_checks import quantity, limit, identity, sign, finish
from kepler_mc import sample_e, project
rng = np.random.default_rng(1)
N = 1_000_000
# self-tests of the independent Kepler code: vis-viva and the bound ṽ <= sqrt(2)
e = sample_e(rng, 1.3, N); o = project(rng, np.ones(N), e)
visviva = np.max(np.abs(o["v"]**2 - (2 / o["r"] - 1)))
print(f"max |v^2 - (2/r - 1/a)| = {visviva:.2e}; max ṽ = {o['vt'].max():.4f} (bound sqrt2 = 1.4142)")
quantity(f"{visviva:.3e} + 1", "1", rel_tol=1e-8)
sign(f"{1.41421356 - o['vt'].max()}", "nonnegative")  # bound ṽ <= sqrt(2) holds
r_avg = np.mean(o["r"]); e2 = np.mean(e**2)
print(f"<r>/a (time-avg) = {r_avg:.4f} vs 1 + <e^2>/2 = {1 + e2/2:.4f}")
quantity(f"{r_avg}", f"{1 + e2/2}", rel_tol=3e-3)
for alpha in (1.3, 1.0):
    e = sample_e(rng, alpha, N); o = project(rng, np.ones(N), e)
    m = np.median(o["vt"])
    for sig, lens in ((0.05, 0.013), (0.10, 0.053)):
        noisy = np.linalg.norm(o["vt_vec"] + rng.normal(0, sig, size=(N, 2)), axis=1)
        b = (np.median(noisy) / m) ** 2 - 1
        quad = 2 * sig**2 / m**2
        print(f"alpha = {alpha}: median ṽ = {m:.4f}; sigma = {sig}: MC bias = {b:+.4f}, quadrature 2σ²/m² = {quad:+.4f}, lens {lens:+.3f}")
        if alpha == 1.3:
            quantity(f"{b}", f"{lens}", rel_tol=0.35)
# limit: bias -> 0 as σ -> 0 (quadrature form)
sg, mm = sp.symbols("sigma m", positive=True)
limit((mm**2 + 2*sg**2)/mm**2 - 1, "sigma", 0, "0")
raise SystemExit(finish())
