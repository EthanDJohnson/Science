"""M-CONSTRAINTS-01 (F1): gap sizes. Inputs (dossier, quoted): H0DN 73.264+-0.806 [D-22], CMB-SPA 67.19+-0.38 [D-44],
DESI BAO+BBN 68.50+-0.58 [D-45], SH0ES 73.49+-0.93 [D-20]; all km/s/Mpc.
Definitions: gap = H_loc - H_early; frac = gap/H_early; Delta mag = 5 log10(H_loc/H_early) (from 5 log10 H0 = M_B + 5 a_B + 25);
naive sigma = gap / sqrt(s1^2 + s2^2) (uncorrelated Gaussian)."""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/constraints")
from math_checks import identity, limit, units, finish
from _bg import near

def g(hl, sl, he, se):
    d = hl - he
    return d, d / he, 5 * math.log10(hl / he), d / math.hypot(sl, se)

for lab, args, want in [("H0DN-SPA", (73.264, .806, 67.19, .38), (6.07, .090, .188, 6.8)),
                        ("H0DN-BAO+BBN", (73.264, .806, 68.50, .58), (4.76, .070, .146, 4.8)),
                        ("SH0ES-SPA", (73.49, .93, 67.19, .38), (6.30, .0938, .195, 6.3))]:
    d, fr, mag, s = g(*args)
    print(lab)
    near("gap km/s/Mpc", d, want[0], 0.006)
    near("fraction", fr, want[1], 0.0006)
    near("mag", mag, want[2], 0.0006)
    near("sigma", s, want[3], 0.06)
# magnitude formula: small-gap limit 5 log10(1+x) -> (5/ln10) x, and identity with the M_B relation
identity("5*log(Hl/He)/log(10)", "(5*log(Hl)/log(10) - 25) - (5*log(He)/log(10) - 25)")
limit("5*log(1+x)/log(10)/x", "x", 0, "5/log(10)")
units("6.074 km/s/Mpc / (67.19 km/s/Mpc)", "dimensionless")
raise SystemExit(finish())
