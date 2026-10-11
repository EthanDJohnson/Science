"""M-CONSTRAINTS-18 (F16, K5, CONSTRAINTS-A): kick ratio kappa = Delta v / v_c(s) grows as sqrt(s)
for a fixed inner-binary photocentre velocity, and the ratio arithmetic of the F16 readings.
The F16 table entries themselves (inner-binary population model) are NOT re-simulated here.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-11-wide-binary-anomaly-gaia-dr4/math/constraints")
from math_checks import identity, limit, finish
from cklib import q

identity("dv/sqrt(G_*M/s)", "dv*sqrt(s)/sqrt(G_*M)", domain={"dv": (0.1, 10), "G_": (0.1, 10), "M": (0.1, 10), "s": (0.1, 10)})
limit("(dv/sqrt(G_*M/(4*s)))/(dv/sqrt(G_*M/s))", "s", 1, "2")
for num, den, lens in [(1.364, 1.238, 1.10), (1.137, 1.041, 1.09), (1.388, 1.238, 1.12), (1.437, 1.276, 1.13), (1.485, 1.276, 1.16)]:
    q(num / den, lens, 6e-3, f"{num}/{den}")
raise SystemExit(finish())
