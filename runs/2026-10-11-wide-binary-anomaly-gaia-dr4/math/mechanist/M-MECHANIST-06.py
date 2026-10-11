"""M-MECHANIST-06: eccentricity effects on median-based γ (Newton, no triples, no noise).
Claims (F6, F8): (a) with the HTZ α(sep) gradient, a Chae-style calibrated median γ = (med ṽ_low / med ṽ_cal)^2 is biased
LOW by ≈ 0.06 (lens grid E1b at f = 0: 0.938), because the calibration zone is more circular (higher median ṽ);
(b) sensitivity ratios vs the reference row for a template-median with template α = 1.3:
truth thermal (α = 1) → ×1.028 (1.121/1.090); truth uniform (α = 0) → ×1.261 (1.374/1.090); thermal template on
HTZ truth → ×0.951 (1.037/1.090).
Set-up: GM_tot = 1.5 Msun; dN/da ∝ a^-1.6; α(a) interpolated from the HTZ table (log10 a [au], α) used by the run;
zones selected by g_N proxy G M / s^2: calibration log10 g ∈ [-8.5, -7.0], scoring log10 g ∈ [-11, -9.5] (m s^-2, SI).
Independent Kepler MC (kepler_mc.py), not the run's generator."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts"); sys.path.insert(0, "runs/2026-10-11-wide-binary-anomaly-gaia-dr4/math/mechanist")
import numpy as np
from math_checks import quantity, sign, finish
from kepler_mc import sample_e, project
rng = np.random.default_rng(7)
GM = 1.3271244e20 * 1.5; AU = 1.495978707e11
HTZ = np.array([(1.75, 0.08), (2.125, 0.59), (2.375, 0.82), (2.625, 0.94), (2.875, 1.20), (3.25, 1.30), (3.75, 1.32), (4.25, 1.17)])
N = 2_000_000
# log a uniform-weighted by a^-0.6 on [100 au, 60 kau]: inverse CDF for dN/da ∝ a^-1.6
lo, hi, k = 100.0, 6e4, -0.6
u = rng.random(N); a_au = (lo**k + u * (hi**k - lo**k)) ** (1 / k)
alpha = np.interp(np.log10(a_au), HTZ[:, 0], HTZ[:, 1])
e = sample_e(rng, alpha, N)
o = project(rng, a_au * AU, e, GM=GM)
lg = np.log10(GM / o["s"]**2)
cal = (lg >= -8.5) & (lg <= -7.0); low = (lg >= -11) & (lg <= -9.5)
print(f"N_cal = {cal.sum()}, N_low = {low.sum()}; s range cal {o['s'][cal].min()/AU:.0f}-{o['s'][cal].max()/AU:.0f} au, low {o['s'][low].min()/AU:.0f}-{o['s'][low].max()/AU:.0f} au")
print(f"mean α: cal {alpha[cal].mean():.3f}, low {alpha[low].mean():.3f}")
m_cal, m_low = np.median(o["vt"][cal]), np.median(o["vt"][low])
g_cal = (m_low / m_cal) ** 2
# bootstrap-free error estimate: median SE ≈ 1.2533 * sd / sqrt(n)
se = 2 * g_cal * np.hypot(1.2533 * o["vt"][cal].std() / np.sqrt(cal.sum()) / m_cal, 1.2533 * o["vt"][low].std() / np.sqrt(low.sum()) / m_low)
print(f"median ṽ cal = {m_cal:.4f}, low = {m_low:.4f}; calibrated γ = {g_cal:.4f} ± {se:.4f} (lens E1b f=0: 0.938)")
sign(f"{g_cal} - 1", "negative")          # direction: calibrated median biased low
quantity(f"{1 - g_cal}", "0.06", rel_tol=0.6)  # size of order 0.06 (accept 0.024-0.096)
# constant-α medians
def med(al, n=1_000_000):
    ee = sample_e(rng, al, n); oo = project(rng, np.ones(n), ee); return np.median(oo["vt"])
M = {al: med(al) for al in (0.0, 1.0, 1.3)}
for al, v in M.items(): print(f"α = {al}: median ṽ = {v:.4f}")
m_htz_low = m_low
r_th = (M[1.0] / M[1.3]) ** 2; r_un = (M[0.0] / M[1.3]) ** 2; r_tt = (m_htz_low / M[1.0]) ** 2; r_ref = (m_htz_low / M[1.3]) ** 2
print(f"template α=1.3 on HTZ low-zone truth: γ = {r_ref:.4f}")
print(f"truth thermal / template 1.3: {r_th:.4f} (lens ratio 1.028); truth uniform / template 1.3: {r_un:.4f} (lens ratio 1.261);")
print(f"thermal template on HTZ truth (relative to α=1.3 template): {r_tt / r_ref:.4f} (lens 0.951); absolute {r_tt:.4f}")
print(f"D-49 cross-check: thermal template vs true α=1.3 -> {(M[1.3]/M[1.0])**2:.4f} (quoted 0.950); α=1.3 template vs true uniform -> {r_un:.4f} (quoted 1.319)")
sign(f"{M[0.0]} - {M[1.0]}", "positive"); sign(f"{M[1.0]} - {M[1.3]}", "positive")  # median ṽ falls as orbits get more eccentric
quantity(f"{r_th}", "1.028", rel_tol=0.03)
quantity(f"{r_un}", "1.261", rel_tol=0.06)
quantity(f"{r_tt / r_ref}", "0.951", rel_tol=0.03)
raise SystemExit(finish())
