"""M-STAT-13  (statistician table row S8)

Claim checked, stated precisely.
  Row S8 reports "RMSE 0.322 -> 0.474 m for 35 -> >75 ms; log-log slope 0.51", i.e. the
  elasticity of tracking RMSE to end-to-end delay estimated from two points,
      slope = ln(RMSE_2/RMSE_1) / ln(tau_2/tau_1),
  with RMSE in m and tau in s (or ms: the ratio makes the slope dimensionless and independent of
  the time unit).
Domain: RMSE_i > 0 m, tau_i > 0 s.

Independent derivation: the two-point log-log slope from its definition, computed in ms and in s
to confirm unit-independence, plus the effect of the ">75 ms" censoring: because tau_2 is only
known to be at least 75 ms, a larger tau_2 lowers the slope, so 0.507 is an upper bound on the
slope, not an estimate of it.
"""
import sys

import numpy as np

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import finish, inequality, limit, quantity, units  # noqa: E402


def slope(r1, r2, t1, t2):
    return np.log(r2 / r1) / np.log(t2 / t1)


print("=== M-STAT-13: two-point log-log slope of RMSE (m) against delay (s) ===")
s_ms = slope(0.322, 0.474, 35.0, 75.0)
s_s = slope(0.322, 0.474, 0.035, 0.075)
print(f"slope with tau in ms: {s_ms:.4f}; with tau in s: {s_s:.4f} (must be identical)")
for t2 in (75.0, 100.0, 130.0, 220.0):
    print(f"  if tau_2 = {t2:5.1f} ms, slope = {slope(0.322, 0.474, 35.0, t2):.4f}")
print(f"RMSE ratio = {0.474 / 0.322:.4f}, delay ratio (75/35) = {75 / 35:.4f}")

units("0.322 m", "length")
units("0.035 s", "time")
units("1", "dimensionless")
quantity(f"{s_ms:.6f}", "0.51", rel_tol=1e-2)
inequality(f"abs({s_ms:.9f} - {s_s:.9f})", "<", "1e-12")           # unit-independent
inequality(f"{slope(0.322, 0.474, 35.0, 220.0):.6f}", "<", f"{s_ms:.6f}")  # censoring lowers it
# limit: if the delay barely changes, a fixed RMSE change implies an unbounded slope
limit("log(1.472)/log(1 + x)", "x", 0, "oo", domain={"x": (1e-9, 1.0)})
raise SystemExit(finish())
