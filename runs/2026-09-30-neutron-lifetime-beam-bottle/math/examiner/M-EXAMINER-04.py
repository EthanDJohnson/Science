"""M-EXAMINER-04: required sizes (F1, F7, lens table A 'settle'). SI: s, s^-1, d = 86400 s.
gap fraction f = 1 - tau_UCNtau/tau_BL1; missing rate r = 1/tau_UCNtau - 1/tau_BL1; time constant 1/r."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/math/examiner")
from math_checks import identity, units, quantity, finish
from _inputs import *
from _h import cmp

tb, tu = BL1[0], U_X
gap = tb - tu
f = 1 - tu / tb
r = 1 / tu - 1 / tb
T = 1 / r
print(f"gap {gap:.2f} s, fraction {f:.5f}, rate {r:.4e} s^-1, T {T:.4e} s = {T/86400:.3f} d")
cmp("fraction (%)", 100 * f, 1.113, 0.0005)
cmp("rate", r, 1.268e-5, 0.0005e-5, "1/s")
cmp("time constant", T, 7.89e4, 0.005e4, "s")
cmp("days", T / 86400, 0.91, 0.005)
cmp("gap / BL1 total", gap / BL1[1], 4.40, 0.005)
cmp("gap / BL1 sys 1.9", gap / 1.9, 5.20, 0.005)
cmp("gap / 1.7 s line", gap / 1.7, 5.81, 0.005)
cmp("gap / bound-state Br 4e-6", 0.011 / 4e-6, 2750, 0.5)
print(f"  exact: fraction/4e-6 = {f/4e-6:.0f}")
cmp("5 sigma precision gap/5", gap / 5, 1.98, 0.005, "s")
cmp("3 sigma precision gap/3", gap / 3, 3.29, 0.005, "s")
# with pole uncertainties (a new result compared with each pole): sigma_needed = sqrt((gap/n)^2 - sigma_pole^2)
for n in (3, 5):
    for pole, sp_ in (("UCNtau", UCNTAU[1]), ("BL1", BL1[1])):
        v = (gap / n) ** 2 - sp_**2
        print(f"  n={n}, vs {pole} pole (+-{sp_:.2f} s): needed sigma = {v**0.5 if v > 0 else float('nan'):.3f} s")
# identities and limits
import sympy as sp
a, b = sp.symbols("a b", positive=True)
identity(1 / a - 1 / b, (b - a) / (a * b))
identity(1 - a / b, (b - a) / b)
units("1/(877.82 s) - 1/(887.7 s)", "1/s")
quantity("1/(1/(877.82 s) - 1/(887.7 s))", "78870 s", rel_tol=2e-4)
raise SystemExit(finish())
