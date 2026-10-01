"""M-ENGINEER-10 (F3): Archimedes. Torque: required 1e-13 N m/sqrt(Hz) vs demonstrated minimum
7e-13 N m/sqrt(Hz) => 0.85 orders. Force: 3e-12 N/sqrt(Hz) integrated 1e6 s => 1 sigma ~ ASD/sqrt(T)
= 3e-15 N (single-sided-convention factors of sqrt(2) aside) against a 5e-16 N signal => 0.78 orders. SI."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-01-warp-drive-without-negative-energy/math/engineer")
from common import *
from math_checks import units, quantity, finish

near("torque gap (minimum noise)", lg(7e-13 / 1e-13), 0.85, 0.01)
print(f"  torque gap at 10 mHz (2e-12): {lg(2e-12/1e-13):.2f} orders")
sig = 3e-12 / math.sqrt(1e6)
rel("1 sigma force over 1e6 s (N)", sig, 3e-15, 1e-6)
near("force gap vs 5e-16 N", lg(sig / 5e-16), 0.78, 0.01)
print(f"  with sqrt(2) one-sided convention: {lg(sig*math.sqrt(2)/5e-16):.2f}; vs 2e-16 N ('few' low end): {lg(sig/2e-16):.2f}")
units("1 N/Hz^0.5 / (1 s)^0.5", "N")
quantity("3e-12 N/Hz^0.5 / (1e6 s)^0.5", "3e-15 N", rel_tol=1e-6)
raise SystemExit(finish())
