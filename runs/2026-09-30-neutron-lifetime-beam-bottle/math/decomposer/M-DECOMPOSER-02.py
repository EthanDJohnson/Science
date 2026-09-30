"""M-DECOMPOSER-02 (F2): gap tensions, fractional gap and missing rate.
z = |x_a - x_b| / (sigma_a (+) sigma_b); fraction f = 1 - tau_s/tau_p = Delta/tau_p;
missing rate r = 1/tau_s - 1/tau_p = Delta/(tau_s tau_p). Storage error scaled by S. SI (s, s^-1)."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/math/decomposer")
from math_checks import identity, series, units, quantity, finish
from _inputs import *

mp_, sp_, _, _ = wmean(PROTON)
ms, ss, c2s, Ss = wmean(STORAGE)
d1 = BL1[0] - UCNT[0]; s1 = q(BL1[1], UCNT[1])
print(f"BL1-UCNtau: {d1:.3f} +- {s1:.3f} s, {d1/s1:.3f} sigma")
near("BL1-UCNtau Delta (s)", d1, 9.88, 0.005)
near("BL1-UCNtau sigma (s)", s1, 2.27, 0.005)
near("BL1-UCNtau z", d1 / s1, 4.36, 0.005)
z2 = z((mp_, sp_), UCNT); print(f"BL1+SIL vs UCNtau {z2:.3f}")
near("BL1+SIL vs UCNtau z", z2, 4.93, 0.005)
z3 = (mp_ - ms) / q(sp_, Ss * ss)
print(f"storage 7: {ms:.3f} +- {ss:.3f} (S={Ss:.3f} -> {Ss*ss:.3f}); BL1+SIL vs storage {z3:.3f}")
near("BL1+SIL vs all storage (scaled) z", z3, 4.57, 0.005)
f_lo = d1 / BL1[0]; f_hi = (mp_ - UCNT[0]) / mp_
r_lo = 1 / UCNT[0] - 1 / BL1[0]; r_hi = 1 / UCNT[0] - 1 / mp_
print(f"fractions {f_lo:.5f} {f_hi:.5f}; rates {r_lo:.4e} {r_hi:.4e} s^-1")
near("fraction low", f_lo, 0.0111, 0.00005)
near("fraction high", f_hi, 0.0114, 0.00005)
near("rate low (1e-5 s^-1)", r_lo * 1e5, 1.27, 0.005)
near("rate high (1e-5 s^-1)", r_hi * 1e5, 1.30, 0.005)
identity("1/ts - 1/tp", "(tp - ts)/(ts*tp)")
series("1/t - 1/(t + d)", "d", 0, 2, "d/t**2")
units("1/(877.82 s) - 1/(887.7 s)", "Hz")
quantity("1/(877.82 s) - 1/(887.7 s)", "1.268e-5 Hz", rel_tol=2e-3)
raise SystemExit(finish())
