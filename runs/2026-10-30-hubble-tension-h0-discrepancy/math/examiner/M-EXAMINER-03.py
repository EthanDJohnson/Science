"""M-EXAMINER-03: inverse-variance combinations without SH0ES (F3).
Non-Cepheid local: CCHP, SBF, TF, TD, masers, sirens (symmetrised errors, independent).
One-step: TD, masers, sirens."""
import sys, math
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/examiner")
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from common import *
from math_checks import identity, limit, quantity, finish

# check: weighted mean of two equal-error measurements is the arithmetic mean, error s/sqrt(2)
a, b, s = sp.symbols("a b s", positive=True)
w = 1 / s**2
identity((w * a + w * b) / (2 * w), (a + b) / 2)
identity(1 / sp.sqrt(2 * w), s / sp.sqrt(2))
# limit: one very precise member dominates
s2 = sp.symbols("s2", positive=True)
limit((a / s**2 + b / s2**2) / (1 / s**2 + 1 / s2**2), "s2", 0, b)

nonC = [sym(m) for m in (CCHP, SBF, TF, TD, MASER, SIREN)]
mu, sig, chi = wmean(nonC)
print(f"non-SH0ES local: {mu:.3f} +- {sig:.3f}, chi2 {chi:.2f}/5")
zc = (mu - CMB[0]) / math.hypot(sig, CMB[1]); zb = (mu - BAOBBN[0]) / math.hypot(sig, BAOBBN[1]); zs = (SH0ES[0] - mu) / math.hypot(sig, SH0ES[1])
print(f"  vs CMB-SPA {zc:.3f}, vs BAO+BBN {zb:.3f}, below SH0ES {zs:.3f}")
quantity(f"{mu}", "71.69", rel_tol=2e-4); quantity(f"{sig}", "1.14", rel_tol=5e-3)
quantity(f"{zc}", "3.74", rel_tol=3e-3); quantity(f"{zb}", "2.49", rel_tol=3e-3); quantity(f"{zs}", "1.22", rel_tol=5e-3)
one = [sym(m) for m in (TD, MASER, SIREN)]
mu1, sig1, chi1 = wmean(one)
z1c = (mu1 - CMB[0]) / math.hypot(sig1, CMB[1]); z1s = (SH0ES[0] - mu1) / math.hypot(sig1, SH0ES[1])
print(f"one-step: {mu1:.3f} +- {sig1:.3f}; vs CMB {z1c:.3f}; below SH0ES {z1s:.3f}")
quantity(f"{mu1}", "71.27", rel_tol=2e-4); quantity(f"{sig1}", "1.93", rel_tol=5e-3)
quantity(f"{z1c}", "2.07", rel_tol=5e-3); quantity(f"{z1s}", "1.04", rel_tol=6e-3)
# facing-side variant for TD/sirens inside a combination is not defined; report sensitivity using lower errors
nonC_low = [(m[0], m[2]) for m in (CCHP, SBF, TF, TD, MASER, SIREN)]
print("sensitivity (lower-side errors):", wmean(nonC_low))
raise SystemExit(finish())
