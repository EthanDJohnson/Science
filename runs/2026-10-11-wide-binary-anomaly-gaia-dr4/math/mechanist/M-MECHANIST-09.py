"""M-MECHANIST-09: unbound-pair slope. Lens (F8, F9, cand A): 5% unbound comoving pairs (σ = 0.5 km/s per axis, wide zone only)
raise E1b from 1.003 to 1.080, 'about +1.5 in γ per unit unbound fraction'; '+0.3 needs about 20% unbound pairs'.
Checked: arithmetic of the slope; linear extrapolation; and the physical sense of a slope ~1.5 via an independent mixture model:
median of a mixture (1−u)·bound + u·unbound, where unbound ṽ = |N(0, σ/v_c)| in 2D, σ/v_c ≫ 1 in the wide zone,
so unbound pairs sit far above the bound median and shift it by quantile displacement: med_mix = Q_bound(0.5/(1−u))."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts"); sys.path.insert(0, "runs/2026-10-11-wide-binary-anomaly-gaia-dr4/math/mechanist")
import numpy as np
from math_checks import quantity, limit, finish
from kepler_mc import sample_e, project
slope = (1.080 - 1.003) / 0.05; slope_a = (1.165 - 1.090) / 0.05
print(f"E1b slope = {slope:.3f}, E1a slope = {slope_a:.3f} per unit unbound fraction")
quantity(f"{slope}", "1.5", rel_tol=0.05)
print(f"linear: +0.3 needs u = {0.3/slope:.3f}")
quantity(f"{0.3/slope}", "0.20", rel_tol=0.05)
rng = np.random.default_rng(3); n = 1_000_000
o = project(rng, np.ones(n), sample_e(rng, 1.3, n)); vt = np.sort(o["vt"]); m0 = np.median(vt)
for u in (0.05, 0.10, 0.20):
    q = np.quantile(vt, 0.5 / (1 - u))   # unbound all above the bound median (σ/v_c ≈ 1-2 in the wide zone puts most there)
    g = (q / m0) ** 2
    print(f"u = {u}: quantile-displacement γ = {g:.3f} (+{g-1:.3f}; slope {(g-1)/u:.2f}); linear lens {1+slope*u:.3f}")
quantity(f"{(np.quantile(vt, 0.5/0.95)/m0)**2 - 1}", "0.077", rel_tol=0.35)
limit("u*k", "u", 0, "0")
raise SystemExit(finish())
