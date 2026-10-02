"""M-DECOMPOSER-02: if E >= |P| (ADM energy-momentum, geometric units c = 1, E > 0) then the
centre-of-mass speed v = |P| c / E <= c; if E = 0 then |P| <= 0 so P = 0. Pure inequalities.
Write E = |P| + d, d >= 0."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import inequality, limit, units, finish
inequality("Pm/(Pm + d)", "<=", "1", domain={"Pm": (0, 10), "d": (0, 10)})
limit("Pm/(Pm + d)", "d", 0, "1", direction="+", domain={"Pm": (0.1, 10)})      # equality only when E = |P|
inequality("-Pm", "<=", "0", domain={"Pm": (0, 10)})  # E = 0: |P| <= E = 0, with |P| >= 0 -> P = 0
# SI: the lens writes "|P|c/E <= c". |P| c / E is dimensionless (it is v/c); the speed is |P| c^2 / E.
units("(1 kg m/s) * (3e8 m/s) / (1 J)", "dimensionless")
units("(1 kg m/s) * (3e8 m/s)^2 / (1 J)", "m/s")
raise SystemExit(finish())
