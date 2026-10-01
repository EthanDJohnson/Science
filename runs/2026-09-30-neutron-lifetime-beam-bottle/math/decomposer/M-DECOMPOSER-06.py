"""M-DECOMPOSER-06 (F6): required systematic sizes against budgets.
Beam: Delta = tau_BL1 - tau_UCNtau; ratios to 1.9, 1.7, 0.5 s. Bottle: r = 1/tau_s - 1/tau_true,
time constant 1/r; a lifetime error d at tau corresponds to a rate d/tau^2. SI (s, s^-1)."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/math/decomposer")
from math_checks import quantity, units, series, finish
from _inputs import *

D = BL1[0] - UCNT[0]
print(f"Delta {D:.3f} s = {D/BL1[0]*100:.3f}% of BL1")
near("fraction (%)", D / BL1[0] * 100, 1.11, 0.005)
near("x BL1 sys 1.9 s", D / 1.9, 5.2, 0.05)
near("x 1.7 s line", D / 1.7, 5.8, 0.05)
near("x 0.5 s fluence", D / 0.5, 20, 0.5)
r = 1 / UCNT[0] - 1 / BL1[0]
print(f"r = {r:.4e} s^-1, 1/r = {1/r:.4e} s = {1/r/86400:.3f} d")
near("loss rate 1e-5", r * 1e5, 1.27, 0.005)
near("time constant 1e4 s", 1 / r / 1e4, 7.9, 0.05)
near("time constant d", 1 / r / 86400, 0.91, 0.005)
rU = 0.2 / UCNT[0] ** 2; rG = 0.6 / GRAV[0] ** 2
print(f"UCNtau 0.2 s -> {rU:.3e} s^-1 (x{r/rU:.1f}); Gravitrap 0.6 s -> {rG:.3e} s^-1 (x{r/rG:.1f})")
near("UCNtau rate 1e-7", rU * 1e7, 2.6, 0.05)
near("x UCNtau", r / rU, 49, 0.5)
near("x Gravitrap", r / rG, 16, 0.5)
quantity("1/(1/(877.82 s) - 1/(887.7 s))", "78870 s", rel_tol=2e-3)
units("0.2 s/(877.82 s)^2", "Hz")
series("1/(t - d) - 1/t", "d", 0, 2, "d/t**2")
raise SystemExit(finish())
