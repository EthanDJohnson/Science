"""M-DIALECTICIAN-06: residual-gas charge exchange in a proton-counting trap.
Model: a fraction f of decay protons is lost undetected, so counted rate = (1-f) Gamma and
tau_meas = tau_true/(1-f). Loss probability small and linear in H2 partial pressure (Caylor: 0.3% at 1e-7 Pa, 10 ms, 40 K).
SI: s, Pa."""
import sys
sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/math/dialectician")
from _common import *  # noqa

gap = BL1 - UCN
f_need = 1 - UCN / BL1
print(f"gap = {gap:.2f} s; f_needed = {f_need*100:.4f} %")
num("f needed (%)", 100 * f_need, 1.113, unit="", abs_tol=0.0006)
shift03 = UCN / (1 - 0.003) - UCN
print(f"0.3% loss -> tau shift {shift03:.3f} s = {shift03/gap*100:.1f}% of gap (linear approx {UCN*0.003:.3f} s)")
num("0.3% -> shift", shift03, 2.64, abs_tol=0.006)
num("fraction of gap (%)", 100 * shift03 / gap, 27, unit="", abs_tol=0.6)
P_need = f_need / 0.003 * 1e-7
print(f"H2 pressure needed (linear): {P_need:.3e} Pa = {P_need/1e-7:.2f} x 1e-7 Pa")
num("pressure needed", P_need, 3.7e-7, unit="Pa", abs_tol=0.06e-7)
# With exponential survival exp(-k P) instead of linear: P = -ln(1-f)/k, k = -ln(0.997)/1e-7
import math as _m
P_exp = _m.log(1 - f_need) / _m.log(1 - 0.003) * 1e-7
print(f"(exponential-survival variant: {P_exp:.3e} Pa)")
print(f"<0.5 s is < {0.5/gap*100:.2f}% of the gap")
num("0.5 s share (%)", 100 * 0.5 / gap, 5.1, unit="", abs_tol=0.06)
# Limits and units
limit("T/(1 - f) - T", "f", 0, "0", domain={"T": (800, 900), "f": (0, 0.05)})
series("T/(1 - f) - T", "f", 0, 2, "T*f")
quantity("1.113/0.3 * 1e-7 Pa", "3.71e-7 Pa", rel_tol=2e-3)
units("877.82 s/(1 - 0.003) - 877.82 s", "time")
raise SystemExit(finish())
