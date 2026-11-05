"""M-STATISTICIAN-03: one-step tensions (facing-side errors) and inverse-variance means (F3, S5).
Mean = sum(w x)/sum(w), w = 1/sigma^2 (asymmetric errors symmetrised by the mean of the sides)."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/statistician")
from _common import tension, wmean, quad, close
from math_checks import limit, units, finish

TD = (71.1, 2.4, 2.3)
close("TD vs CMB-SPA", tension(*TD, 67.19, .38, .38), 1.68, 0.01)
close("TD vs PR4", tension(*TD, 67.64, .52, .52), 1.47, 0.01)
close("TD vs H0DN", tension(*TD, 73.264, .806, .806), 0.85, 0.01)
close("TD vs SH0ES", tension(*TD, 73.49, .93, .93), 0.93, 0.01)
close("masers vs SPA", tension(71.6, 3.7, 3.7, 67.19, .38, .38), 1.19, 0.01)
close("sirens vs SPA", tension(71.7, 9.4, 7.5, 67.19, .38, .38), 0.60, 0.01)

m1, s1, c1 = wmean([71.1, 71.6, 71.7], [2.35, 3.7, 8.45])
close("one-step mean", m1, 71.27, 0.01); close("one-step sigma", s1, 1.93, 0.01)
close("one-step within chi2", c1, 0.02, 0.006)
me, se, ce = wmean([67.19, 68.50], [0.38, 0.58])
close("early mean", me, 67.58, 0.01); close("early sigma", se, 0.32, 0.005)
close("early internal z (CMB-SPA vs BAO+BBN)", abs(67.19 - 68.50) / quad(.38, .58), 1.89, 0.01)
close("one-step vs early z", (m1 - me) / quad(s1, se), 1.88, 0.01)

# limit: weighted mean of two equal-error values is the plain mean with sigma/sqrt(2)
limit("(x/s**2 + y/t**2)/(1/s**2 + 1/t**2)", "t", "s", "(x+y)/2")
units("3.69 km/s/Mpc / (1.957 km/s/Mpc)", "dimensionless")
raise SystemExit(finish())
