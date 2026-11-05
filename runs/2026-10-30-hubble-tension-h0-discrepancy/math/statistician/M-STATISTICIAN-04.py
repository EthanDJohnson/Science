"""M-STATISTICIAN-04: M_B framing (F4, S9).
From 5 log10 H0 = M_B + 5 a_B + 25 at fixed a_B: Delta M_B = 5 log10(H0_1/H0_2). Magnitudes (mag)."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/statistician")
import mpmath as mp
import sympy as sp
from _common import quad, close
from math_checks import identity, series, units, finish

H1, H2, aB = sp.symbols("H1 H2 a_B", positive=True)
M = lambda H: 5 * sp.log(H, 10) - 5 * aB - 25
identity(M(H1) - M(H2), 5 * sp.log(H1 / H2, 10))
x = sp.symbols("x")
series("5*log(1+x)/log(10)", "x", 0, 2, "5*x/log(10)", domain={"x": (-0.5, 0.5)})  # small-gap limit
units("5 * 1", "dimensionless")

close("gap vs CMB-SPA, mag", 5 * mp.log10(73.49 / 67.19), 0.195, 0.001)
close("gap vs CMB-SPA, %", 100 * (73.49 / 67.19 - 1), 9.4, 0.05)
close("gap vs BAO+BBN, mag", 5 * mp.log10(73.49 / 68.50), 0.153, 0.001)
close("gap vs BAO+BBN, %", 100 * (73.49 / 68.50 - 1), 7.3, 0.05)
# M_B: ladder -19.253 +- 0.027 vs inverse ladder; inverse is lower so its upper error faces
d1 = -19.253 - (-19.375); d2 = -19.253 - (-19.394)
close("dM_B cosmography", d1, 0.122, 0.0005)
close("  z", d1 / quad(0.027, 0.018), 3.76, 0.01)
close("dM_B flat LCDM", d2, 0.141, 0.0005)
close("  z", d2 / quad(0.027, 0.017), 4.42, 0.01)
raise SystemExit(finish())
