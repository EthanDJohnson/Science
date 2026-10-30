"""M-CONSTRAINTS-15 (deciding-measurement separation): a single Gaussian measurement of global H0 with error sigma separates
H_a = 67.19 from H_b = 73.264 at k sigma when |H_b - H_a| / sigma >= k -> sigma <= 6.074/k. Lens: <= 2.0 (2.8%) at 3 sigma, <= 1.2 (1.7%) at 5."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/constraints")
from math_checks import inequality, finish
from _bg import near

d = 73.264 - 67.19
near("sigma for 3 sigma", d / 3, 2.0, 0.03); near("percent of 73.26", d / 3 / 73.264, 0.028, 0.0006)
near("sigma for 5 sigma", d / 5, 1.2, 0.03); near("percent", d / 5 / 73.264, 0.017, 0.0006)
inequality("d/s", ">=", "k", domain={"d": (6.074, 6.074), "k": (3, 5), "s": (0.1, 1.2)})
raise SystemExit(finish())
