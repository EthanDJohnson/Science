"""M-EMPIRICIST-04: J-PARC tensions and internal scatter (F7). z = |x - J| / (sigma_J,side (+) sigma_x),
using the J-PARC sys side facing x (+4.0 upward, -3.6 downward) and stat 1.7 s. Inflation of stat by sqrt(15.8/3).
Per-condition values D-24 (stat only). Lifetimes in s."""
import sys
sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/math/empiricist")
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from _inputs import *
from math_checks import limit, units, finish

J, st = 877.2, 1.7
mp_, sp_ = wmean(PROTON)
up = q(st, 4.0)
z_p = (mp_ - J) / q(up, sp_); z_b = (D["BL1"][0] - J) / q(up, D["BL1"][1])
z_u = (D["UCNT"][0] - J) / q(up, 0.22, 0.17)   # UCNtau's downward side faces J-PARC
print(f"J-PARC vs proton mean {z_p:.3f}, vs BL1 {z_b:.3f}, vs UCNtau {z_u:.3f}")
agree("J vs proton", z_p, 2.24, 0.006); agree("J vs BL1", z_b, 2.15, 0.006); agree("J vs UCNtau", z_u, 0.14, 0.006)
limit("d/sqrt(s**2 + t**2)", "s", "oo", "0")
units("(887.97 s - 877.2 s)/((4.35 s)^2 + (2.04 s)^2)^0.5", "dimensionless")

cond = [(870.9, 3.5), (868.3, 4.0), (868.2, 7.7), (884.8, 2.4)]
w = [1 / s ** 2 for _, s in cond]; m = sum(wi * x for wi, (x, _) in zip(w, cond)) / sum(w)
c = sum(((x - m) / s) ** 2 for x, s in cond)
print(f"four conditions stat-only: mean {m:.3f}, chi2 {c:.3f}/3, p {pchi2(c,3):.3g}")
agree("stat-only chi2", c, 19.6, 0.06); agree("stat-only p", pchi2(c, 3), 2e-4, 0.6e-4)
S = (15.8 / 3) ** 0.5; up_i = q(st * S, 4.0)
zi_p = (mp_ - J) / q(up_i, sp_); zi_u = (D["UCNT"][0] - J) / q(up_i, 0.22, 0.17)
print(f"inflation {S:.4f}; inflated z vs proton {zi_p:.3f}, vs UCNtau {zi_u:.3f}")
agree("inflation", S, 2.29, 0.006); agree("inflated vs proton", zi_p, 1.81, 0.006)
agree("inflated vs UCNtau", zi_u, 0.11, 0.006)
c3 = cond[:3]; w3 = [1 / s ** 2 for _, s in c3]
m3 = sum(wi * x for wi, (x, _) in zip(w3, c3)) / sum(w3); s3 = sum(w3) ** -0.5
print(f"three consistent conditions {m3:.3f} +- {s3:.3f}; chi2 {sum(((x-m3)/s)**2 for x,s in c3):.3f}/2; "
      f"BL1 - outlier {D['BL1'][0]-884.8:.2f} s")
agree("three-condition mean", m3, 869.6, 0.06); agree("three-condition sigma", s3, 2.5, 0.06)
agree("BL1 - 884.8", D["BL1"][0] - 884.8, 2.9, 0.06)
raise SystemExit(finish())
