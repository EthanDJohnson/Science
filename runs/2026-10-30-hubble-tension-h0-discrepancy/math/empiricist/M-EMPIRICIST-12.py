"""M-EMPIRICIST-12 (EMPIRICIST-B) and M-EMPIRICIST-14 (EMPIRICIST-A): magnitude decomposition of the gap.
Magnitude gaps are additive along a chain: 5log10(Ha/Hc) = 5log10(Ha/Hb) + 5log10(Hb/Hc).
EMPIRICIST-B: SH0ES-vs-rest ~3 km/s/Mpc (~0.1 mag) + rest-vs-early ~4 km/s/Mpc (~0.13 mag, ~6%).
EMPIRICIST-A: true local 70-72 'removes roughly half of the 0.195 mag gap'.
'Rest' = non-SH0ES local mean 71.56 (71.21 with lensed SNe, 71.47 correlated); early = CMB-SPA 67.19; SH0ES 73.49.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/empiricist")
import math
from math_checks import identity, inequality, finish
from _common import cmp


def dm(a, b):
    return 5 * math.log10(a / b)


identity("5*log(a/c)/log(10)", "5*log(a/b)/log(10) + 5*log(b/c)/log(10)")
total = dm(73.49, 67.19)
print(f"  total SH0ES-CMB gap {total:.4f} mag, {73.49 - 67.19:.2f} km/s/Mpc")
for rest in (71.56, 71.47, 71.21):
    a, b = dm(73.49, rest), dm(rest, 67.19)
    print(f"  rest = {rest}: SH0ES-rest {73.49 - rest:.2f} km/s/Mpc = {a:.4f} mag; rest-CMB {rest - 67.19:.2f} km/s/Mpc"
          f" = {b:.4f} mag ({100 * (rest / 67.19 - 1):.1f}%); sum {a + b:.4f}")
print(f"  SH0ES vs CCHP alone: {73.49 - 70.39:.2f} km/s/Mpc = {dm(73.49, 70.39):.4f} mag")
# the lens's two pieces cannot both hold, since they must sum to the total 0.195 mag / 6.30 km/s/Mpc
inequality("0.1 + 0.13", ">", str(total))
cmp("lens piece 2: rest-vs-CMB [mag] (rest = 71.21-71.56)", dm(71.4, 67.19), 0.13, 0.01)
cmp("lens piece 1: SH0ES-vs-rest [mag], rest = 71.56", dm(73.49, 71.56), 0.1, 0.02)   # expected FAIL
cmp("lens piece 1: SH0ES-vs-rest [km/s/Mpc], rest = 71.56", 73.49 - 71.56, 3.0, 0.5, "km/s/Mpc")  # expected FAIL

print("  M-EMPIRICIST-14: fraction of the 0.195 mag gap removed if the true local value is H:")
for h in (70.0, 70.39, 71.0, 71.21, 71.56, 72.0):
    print(f"    H = {h}: removes {dm(73.49, h):.4f} mag = {dm(73.49, h) / total:.2f} of the gap")
cmp("fraction removed at H = 71 (midpoint of 70-72)", dm(73.49, 71.0) / total, 0.5, 0.1)   # expected FAIL
cmp("fraction removed at H = 70 (low end)", dm(73.49, 70.0) / total, 0.5, 0.1)
raise SystemExit(finish())
