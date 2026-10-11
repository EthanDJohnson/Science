"""M-EMPIRICIST-05: C3PO and deep-bin distances; deep-bin acceleration range vs scoring bin (F5, F6).

C3PO s>3 kau gamma = 1.17 +0.37/-0.23: distance to 1.37 using the upper error 0.37 -> 0.54 sigma;
to 1.00 using the lower error 0.23 -> 0.74 sigma.
Boufourou deep bin 1.11 +- 0.07: 1.6 sigma above 1, 3.7 sigma below 1.37.
Deep bin g_N/a0 in [0.03, 0.3] with a0 = 1.2e-10 m s^-2 -> g_N = 3.6e-12 .. 3.6e-11 m s^-2,
log10 = -11.44 .. -10.44, which does not contain -10.
Scoring-bin rule: range wholly below 10^-9.5 and containing 10^-10. Chae 2025 bin [10^-11.0, 10^-9.5]
and Chae+26 bin g_N < 10^-9.5 qualify (upper edge equal to 10^-9.5, read as 'not above').
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import inequality, quantity, units, limit, finish

print(f"C3PO: to 1.37 {(1.37-1.17)/0.37:.3f}; to 1.00 {(1.17-1.00)/0.23:.3f}")
print(f"deep: above 1 {(1.11-1)/0.07:.3f}; below 1.37 {(1.37-1.11)/0.07:.3f}")
inequality(f"abs({(1.37-1.17)/0.37} - 0.54)", "<", "0.005")
inequality(f"abs({(1.17-1.00)/0.23} - 0.74)", "<", "0.005")
inequality(f"abs({(1.11-1)/0.07} - 1.6)", "<", "0.05")
inequality(f"abs({(1.37-1.11)/0.07} - 3.7)", "<", "0.05")

a0 = 1.2e-10  # m s^-2
lo, hi = 0.03 * a0, 0.3 * a0
print(f"deep bin g_N = {lo:.3e} .. {hi:.3e} m s^-2; log10 {math.log10(lo):.3f} .. {math.log10(hi):.3f}")
quantity("0.03 * 1.2e-10 m/s^2", "3.6e-12 m/s^2", rel_tol=1e-6)
quantity("0.3 * 1.2e-10 m/s^2", "3.6e-11 m/s^2", rel_tol=1e-6)
units("0.3 * 1.2e-10 m/s^2", "acceleration")
inequality(f"abs({math.log10(lo)} + 11.44)", "<", "0.005")
inequality(f"abs({math.log10(hi)} + 10.44)", "<", "0.005")
inequality(str(math.log10(hi)), "<", "-10")       # the upper edge lies below 1e-10, so 1e-10 is not in the bin
# a0 sensitivity: log10 of the upper edge is log10(0.3 a0); with a0 = 1.0e-10 or 1.4e-10 it stays below -10
for a in (1.0e-10, 1.4e-10):
    inequality(str(math.log10(0.3 * a)), "<", "-10")

def qualifies(lo_log, hi_log):
    return hi_log <= -9.5 and lo_log <= -10 <= hi_log
print("Chae 2025 [-11.0, -9.5]:", qualifies(-11.0, -9.5), "| Chae+26 (<-9.5):", qualifies(-99, -9.5),
      "| Boufourou deep:", qualifies(math.log10(lo), math.log10(hi)))
inequality(str(int(qualifies(-11.0, -9.5) and qualifies(-99, -9.5) and not qualifies(math.log10(lo), math.log10(hi)))), "==" if False else ">", "0")
raise SystemExit(finish())
