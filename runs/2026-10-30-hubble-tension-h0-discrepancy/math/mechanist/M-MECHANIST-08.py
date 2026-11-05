"""M-MECHANIST-08 (F5 per experiment), M-MECHANIST-11 (F10), M-MECHANIST-13 (F12): ratio arithmetic.
08: n_i = (73.264 - H_i)/σ_i for Planck PR4 67.64 ± 0.52, ACT 66.51 ± 0.64, SPT 66.66 ± 0.60 [D-41..43].
11: fraction closed = (H_m - 67.19)/(73.264 - 67.19); residual = 5 log10(73.264/H_m).
13: (73.264 - 67.19)/0.31 [D-10].
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/mechanist")
from math_checks import identity, limit, finish
from mm_common import dmag, near

print("== M-MECHANIST-08 ==")
for name, h, s, claim in [("PR4", 67.64, 0.52, 10.8), ("ACT", 66.51, 0.64, 10.6), ("SPT", 66.66, 0.60, 11.0)]:
    near(f"{name} bias km/s/Mpc", 73.264 - h, round(73.264 - h, 2), 0.006)
    near(f"{name} sigma", (73.264 - h) / s, claim, 0.06)
print("== M-MECHANIST-11 ==")
gap = 73.264 - 67.19
limit("(x - 67.19)/(73.264 - 67.19)", "x", 73.264, "1")  # model reaching the local value closes 100%
identity("5*log(Hl/He)/log(10) - 5*log(Hl/Hm)/log(10)", "5*log(Hm/He)/log(10)")  # closed + residual = gap in mag
for name, hm, claim in [("ACT EDE", 69.9, 0.45), ("ACT PMF", 69.1, 0.31), ("ACT mod rec", 69.6, 0.40),
                        ("NPIPE EDE", 69.5, 0.38), ("ED fluct", 69.3, 0.35), ("Poulin", 71.0, 0.63),
                        ("eROSITA", 71.4, 0.69)]:
    near(f"{name} fraction", (hm - 67.19) / gap, claim, 0.006)
near("min residual mag (71.4)", dmag(73.264, 71.4), 0.056, 0.0006)
print("== M-MECHANIST-13 ==")
near("void sigma", gap / 0.31, 20, 0.5)
raise SystemExit(finish())
