"""M-CONSTRAINTS-12 (F14): relative-velocity noise in normalised units, DR3 vs DR4 (SI via unit_tools).

sigma_v~ (per axis) = d * sqrt2 * sigma_mu / v_c(s), v_c = sqrt(G M / s), M = 1.5 Msun.
4.74 km/s = 1 au/yr (i.e. 1 mas/yr at 1 kpc). sigma_mu(DR3) = sigma_mu(DR4)/0.42 (sourced, not checked).
Bias ~ sigma^2 at small sigma => DR3 -> DR4 reduction factor (1/0.42)^2.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-11-wide-binary-anomaly-gaia-dr4/math/constraints")
from math_checks import quantity, units, finish
from cklib import q

MAS = "4.8481368e-9"
quantity("1 au/(1 yr)", "4.74 km/s", rel_tol=2e-3)
units("200 pc * 0.0119*4.8481368e-9/(1 yr)", "m/s")
cases = [  # sigma_mu DR4 (mas/yr), d (pc), s (au), lens DR4, lens DR3
    (0.0119, 200, 10000, 0.044, 0.104),
    (0.0319, 200, 10000, 0.117, 0.279),
    (0.0319, 200, 20000, 0.166, 0.394),
]
for smu, d, s, l4, l3 in cases:
    expr4 = f"(2^(1/2))*{d} pc*{smu}*{MAS}/(1 yr)/(G*1.5*Msun/({s} au))^(1/2)"
    quantity(expr4, f"{l4}", rel_tol=1e-2)
    quantity(f"({expr4})/0.42", f"{l3}", rel_tol=1e-2)
# small-sigma bias scaling: (1/0.42)^2
q((1 / 0.42) ** 2, 6.0, 0.06, "noise-bias reduction factor DR3->DR4 ('about 6x')")
q(1 / 0.42, 2.4, 0.01, "proper-motion error ratio ('2.4x')")
raise SystemExit(finish())
