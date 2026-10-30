"""M-EMPIRICIST-01: magnitude form of the H0 gap.
Distance modulus mu = 5 log10(d_L/10 pc); at fixed redshift d_L ∝ 1/H0, so a ladder whose calibrated M_B is
brighter by Δm infers H0 larger by factor 10^(Δm/5): Δm = 5 log10(H_a/H_b) (mag, dimensionless).
Claims: SH0ES 73.49 vs CMB-SPA 67.19 -> 0.195 mag, 9.4%; non-SH0ES 71.56 vs 67.19 -> 0.137 mag, 6.5%.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/empiricist")
from math_checks import identity, limit, series, units, finish
import math
from _common import cmp

# symbolic: Hubble-law relation; mu(H) = 5 log10(c z / H / 10pc) => mu(Hb) - mu(Ha) = 5 log10(Ha/Hb)
identity("5*log(c*z/(Hb*d0))/log(10) - 5*log(c*z/(Ha*d0))/log(10)", "5*log(Ha/Hb)/log(10)")
# limit: equal H0 gives zero gap
limit("5*log(1+x)/log(10)", "x", 0, "0")
# small-gap expansion: Δm ≈ (5/ln10) * (ΔH/H)
series("5*log(1+x)/log(10)", "x", 0, 2, "5*x/log(10)")
# units: ratio of two H0 values is dimensionless
units("(73.49 km/s/Mpc)/(67.19 km/s/Mpc)", "dimensionless")

dm1 = 5 * math.log10(73.49 / 67.19)
dm2 = 5 * math.log10(71.56 / 67.19)
cmp("SH0ES vs CMB-SPA gap [mag]", dm1, 0.195, 0.0006)
cmp("SH0ES vs CMB-SPA fractional", 73.49 / 67.19 - 1, 0.094, 0.0006)
cmp("non-SH0ES vs CMB-SPA gap [mag]", dm2, 0.137, 0.0006)
cmp("non-SH0ES vs CMB-SPA fractional", 71.56 / 67.19 - 1, 0.065, 0.0006)
raise SystemExit(finish())
