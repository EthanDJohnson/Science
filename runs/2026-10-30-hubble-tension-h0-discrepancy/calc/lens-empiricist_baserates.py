"""Empiricist lens: base rates for persistent disagreements between established precision methods.

Part A: heavy-tailed error distributions. Bailey 2017 (RSOS 4 160600) finds uncertainty-normalised
differences between measurements of the same quantity follow Student's t with nu ~ 2-4 (almost Cauchy).
We compute the two-sided tail probability of a disagreement of z nominal sigma for Student's t with unit
scale (an ILLUSTRATION: Bailey's fitted core widths differ from 1 and are not reproduced here) and for a
Gaussian, at the H0 z-values computed in lens-empiricist_replication.py.

Part B: a tally of historical cases (this lens's classification; cases and outcomes as described in
the analysis file, several from background knowledge and labelled there). Fractions with Wilson 95% CIs.
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from stats_tools import sigma_to_p, wilson_interval

def student_t_sf2(z, nu):
    """Two-sided tail P(|T| > z) for Student's t with nu dof, unit scale (regularised incomplete beta)."""
    x = nu / (nu + z * z)
    # I_x(nu/2, 1/2) by continued fraction (Numerical Recipes betacf)
    a, b = nu / 2.0, 0.5
    def betacf(a, b, x):
        MAXIT, EPS, FPMIN = 500, 3e-16, 1e-300
        qab, qap, qam = a + b, a + 1, a - 1
        c, d = 1.0, 1 - qab * x / qap
        d = 1 / (d if abs(d) > FPMIN else FPMIN); h = d
        for m in range(1, MAXIT + 1):
            m2 = 2 * m
            aa = m * (b - m) * x / ((qam + m2) * (a + m2))
            d = 1 + aa * d; d = 1 / (d if abs(d) > FPMIN else FPMIN)
            c = 1 + aa / c; c = c if abs(c) > FPMIN else FPMIN
            h *= d * c
            aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
            d = 1 + aa * d; d = 1 / (d if abs(d) > FPMIN else FPMIN)
            c = 1 + aa / c; c = c if abs(c) > FPMIN else FPMIN
            de = d * c; h *= de
            if abs(de - 1) < EPS:
                break
        return h
    lbeta = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log(1 - x)
    return math.exp(lbeta) * betacf(a, b, x) / a

# check: nu=1 (Cauchy) two-sided tail at z=1 is 0.5
chk = student_t_sf2(1.0, 1)
print(f"check Cauchy P(|T|>1) = {chk:.6f} (exact 0.5) -> {'PASS' if abs(chk-0.5)<1e-9 else 'FAIL'}")
chk2 = student_t_sf2(2.0, 2)   # exact: 1 - z/sqrt(z^2+2) = 1 - 2/sqrt(6)
ex2 = 1 - 2 / math.sqrt(6)
print(f"check t2 P(|T|>2) = {chk2:.6f} (exact {ex2:.6f}) -> {'PASS' if abs(chk2-ex2)<1e-9 else 'FAIL'}")

print("\nPart A: two-sided probability of a z-sigma disagreement arising with no real effect")
print("  z      Gaussian     t(nu=2)   t(nu=3)   t(nu=4)   [unit scale; illustration]")
for label, z in [("one-step vs CMB", 2.07), ("non-SH0ES local vs CMB", 3.24), ("SH0ES vs CMB", 6.27), ("5 sigma", 5.0)]:
    print(f"  {z:4.2f} {sigma_to_p(z, two_sided=True):11.3g}  {student_t_sf2(z,2):8.3g}  {student_t_sf2(z,3):8.3g}  {student_t_sf2(z,4):8.3g}   {label}")

print("\nPart B: historical cases, outcome tally (this lens's classification)")
cases = [
    # (name, structure, outcome)
    ("Hubble 1929 H0~500 vs ages; Baade 1952 Cepheid populations", "ladder-internal", "systematic"),
    ("Sandage vs de Vaucouleurs H0 50 vs 100 (1970s-1990s)", "two-team ladder", "systematic"),
    ("1990s age crisis: GC ages vs 1/H0", "multi-method", "mixed"),
    ("Solar neutrino deficit (1968-2001)", "multi-method", "new physics"),
    ("Atmospheric neutrino anomaly (1988-1998)", "multi-method", "new physics"),
    ("Accelerating expansion (1998)", "multi-method", "new physics"),
    ("Proton radius puzzle (2010-2019)", "multi-method", "systematic"),
    ("Muon g-2 vs data-driven SM (2006-2025)", "multi-method", "shared input"),
    ("CDF W mass 2022", "single-experiment", "systematic"),
    ("Reactor antineutrino anomaly (2011-2021)", "single-input", "shared input"),
    ("LHCb R_K (2014-2022)", "single-experiment", "systematic"),
    ("OPERA superluminal neutrinos (2011)", "single-experiment", "systematic"),
    ("BICEP2 B-modes (2014)", "single-experiment", "systematic"),
    ("Pioneer anomaly", "single-experiment", "systematic"),
    ("Planck A_L lensing excess (PR3)", "single-experiment", "statistical/analysis"),
    ("S8 weak-lensing tension (KiDS-1000 era)", "multi-survey", "statistical/analysis"),
    ("PTB 1996 G_N, 50 sigma (Bailey 2017)", "single-experiment", "systematic"),
    ("CODATA 2006 vs 2010 alpha, 6.5 sigma (Bailey 2017)", "single-input", "shared input"),
    ("Neutron lifetime beam vs bottle", "two-method", "unresolved"),
    ("Newton's G spread", "multi-method", "unresolved"),
    ("Gallium anomaly (BEST)", "multi-experiment", "unresolved"),
]
resolved = [c for c in cases if c[2] != "unresolved"]
def frac(sel, name):
    n = len(sel); k = sum(1.0 if c[2] == "new physics" else 0.5 if c[2] == "mixed" else 0.0 for c in sel)
    lo, hi = wilson_interval(int(round(k)), n)
    print(f"  {name:55s} n={n:2d}  new-physics share = {k:.1f}/{n} = {k/n:.2f}  (Wilson 95% on {int(round(k))}/{n}: {lo:.2f}-{hi:.2f})")
frac(resolved, "all resolved cases")
frac([c for c in resolved if c[1] == "multi-method"], "resolved, anomaly seen by >=2 independent methods")
frac([c for c in resolved if c[1] != "multi-method"], "resolved, single experiment/team/input")
sys_like = [c for c in resolved if c[2] in ("systematic", "shared input", "statistical/analysis")]
print(f"  resolved cases ending as systematic/shared input/statistics: {len(sys_like)}/{len(resolved)}")
print(f"  of which the cause was a shared input (model/flux/theory term): {sum(c[2]=='shared input' for c in resolved)}")
print("PASS: completed")
