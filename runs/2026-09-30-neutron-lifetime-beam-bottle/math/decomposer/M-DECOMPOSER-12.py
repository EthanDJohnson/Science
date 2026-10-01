"""M-DECOMPOSER-12 (F13, candidate E): leave-one-out tensions and fractions of the gap.
Storage without UCNtau: 6 results, error scaled by S. Fractions: 0.003*tau_BL1 / Delta; 5.35 s / Delta.
Two-sided Gaussian p at 4.36 sigma. SI (s)."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/math/decomposer")
from math_checks import limit, finish
from _inputs import *

ms, ss, _, S = wmean(STORAGE)
z1 = z(SIL, UCNT); z2 = (SIL[0] - ms) / q(SIL[1], S * ss)
print(f"SIL vs UCNtau {z1:.3f}; SIL vs storage {z2:.3f}")
near("SIL vs UCNtau", z1, 2.35, 0.005); near("SIL vs all storage", z2, 2.22, 0.005)
rest = [x for x in STORAGE if x is not UCNT]
m6, s6, c6, S6 = wmean(rest)
z3 = (BL1[0] - m6) / q(BL1[1], S6 * s6)
print(f"storage w/o UCNtau {m6:.3f} +- {s6:.3f}, S {S6:.3f} -> {S6*s6:.3f}; BL1 vs it {z3:.3f}")
near("storage w/o UCNtau mean", m6, 879.92, 0.005)
near("scaled sigma", S6 * s6, 0.64, 0.005); near("S", S6, 1.34, 0.005)
near("BL1 vs rest storage", z3, 3.33, 0.005)
near("BL1 vs Gravitrap", z(BL1, GRAV), 2.55, 0.005)
D = BL1[0] - UCNT[0]
h2 = 0.003 * BL1[0]
print(f"H2 0.3% = {h2:.3f} s = {h2/D:.3f} of gap; 5.3 s -> {5.3/D:.3f}, 5.4 s -> {5.4/D:.3f}")
near("H2 shift s", h2, 2.7, 0.05); near("H2 fraction", h2 / D, 0.27, 0.005)
near("100% of one correction, fraction", 5.35 / D, 0.54, 0.006)
p = p2(4.36)
print(f"two-sided p at 4.36 sigma = {p:.3e}")
near("p (1e-5)", p * 1e5, 1.0, 0.35)
limit("erfc(x/sqrt(2))", "x", 0, "1")
raise SystemExit(finish())
